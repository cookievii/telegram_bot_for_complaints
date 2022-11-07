import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

db_file = os.path.join(os.path.dirname(__file__), os.getenv("DATEBASE_NAME"))
engine = create_engine(f"sqlite:///{db_file}", echo=True)


def create_db():
    from models.user import User

    table_objects = [User.__table__]
    Base.metadata.create_all(engine, tables=table_objects)


session = scoped_session(sessionmaker(bind=engine))
