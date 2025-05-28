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
    accounts =relationship('Bank_Account', back_populates ='user')

def Bank_Account(Base):
    __tablename__ ="accounts"

    id = Column(Integer,primary_key =True)
    user_id = Column(Integer,ForeignKey('users.id'))
    account_type = Column(String,nullable=False)
    balance = Column(Float, default =0.0)

#relationships  
    user =relationship('User', back_populates = 'accounts')
    transactions = relationship('Transaction', back_populates ='account')

def Transcation(Base):
    __tablename__ = "transactions"

    id = Column(Integer,primary_key =True)
    account_id = Column(Integer,ForeignKey=('accounts.id'))
    type = Column (String, nullable= False)
    amount = Column(Float,nullale=False)
    timestamp=Column(DateTime,default =datetime.utcnow)

#relationship
    account = relationship('Bank_Account', back_populates='transactions')    
