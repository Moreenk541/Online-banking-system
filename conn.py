from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 

DATABASE_URL = "sqlite:///bank.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)
