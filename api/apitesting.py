from fastapi import FastAPI, Response, status, HTTPException

import psycopg2 as ps
from psycopg2.extras import RealDictCursor
from templates import post_template



app = FastAPI()

try: 
    conn = ps.connect(host = '172.17.0.1', database='root', user='root', password='root', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('success!')
except Exception as r:
    print("Connection failed")
    print('Error was ', r)
#%%

    

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: post_template):
    cursor.execute('''INSERT INTO public.posts ("Title", "Content", "Published") VALUES (%s, %s, %s) RETURNING *''', 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {'data': new_post}
    

@app.get('/posts')
def get_all():
    cursor.execute('''SELECT * from public.posts''')
    posts = cursor.fetchall()
    return posts

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    print(id, type(id ))
    cursor.execute('''SELECT * FROM public.posts WHERE "ID" = %s''' % id)
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='the id was not found')
    else:
        return {'data': post}
        

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM public.posts WHERE "ID" = %s RETURNING *''' % id)
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the id was not found')
    else:
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put('/posts/{id}')
def update_post(id: int, post: post_template):
    print(post.dict())
    cursor.execute('''UPDATE public.posts SET "Title" = '%s', "Content"  = '%s' WHERE "ID" = %s RETURNING *''' % (post.title, post.content, id))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the id was not found')
    conn.commit()
    return {'message': f'{data}'}
#%%
