from sqlalchemy import Column, Integer, String, Float,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()

def User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key =True)
    name = Column(String, nullable =False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False)

#one to many relationship user - accounts

def Bank_Account(Base):
    __tablename__ ="accounts"

    id = Column(Integer,primary_key =True)
    user_id = Column(Integer,ForeignKey('users.id'))
    account_type = column(String,nullable=False)
    balance = Column(Float, default =0.0)

#relationship    

