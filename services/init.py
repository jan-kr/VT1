import db
import seed_data


def init_db():
    if db.init_db():
        seed_data.init()
