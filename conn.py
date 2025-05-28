from sqlalchemy import create_engine
from sqlalchemy import sessionmaker

DATABASE_URL = "sqlite3:///bank.db"

engine = create_engine(DATABASE_URL, echo = True)
SessionLocal = sessionmaker(bind=engine)