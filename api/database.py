from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

sql_url = 'postgresql://root:root@172.17.0.2/root'

engine = create_engine(sql_url)

Local_session = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


def get_db():
    db = Local_session()
    try:
        yield db
    except:
        db.close()

