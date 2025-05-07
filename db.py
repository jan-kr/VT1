from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///db.db')
Session = sessionmaker(bind=engine)


def init_db() -> bool:
    if not inspect(engine).get_table_names():
        Base.metadata.create_all(engine)
        return True
    return False