from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import settings

sql_url = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}'

engine = create_engine(sql_url)

Local_session = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


def get_db():
    db = Local_session()
    try:
        yield db
    except:
        db.close()

