import db
import seed_data


def init_db():
    if db.init_db():
        print("Starting Database initialization")
        seed_data.init()
        print("Database initialization complete")
