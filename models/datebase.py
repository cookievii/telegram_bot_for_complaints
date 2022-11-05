import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
db_file = os.path.join(os.path.dirname(__file__), os.getenv("DATEBASE_NAME"))
engine = create_engine(f"sqlite:///{db_file}", echo=True)


def cretae_db():
    db_is_created = os.path.exists(os.getenv("DATEBASE_NAME"))
    if not db_is_created:
        Base.metadata.create_all(engine)


session = scoped_session(sessionmaker(bind=engine))
