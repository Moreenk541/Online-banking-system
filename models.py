from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact=Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # One-to-many: One user has many accounts
    accounts = relationship('Bank_Account', back_populates='user')
    loans = relationship('Loan', back_populates='user')


class Bank_Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')
    loans = relationship('Loan', back_populates='account')


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    account = relationship('Bank_Account', back_populates='transactions')


class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    months = Column(Integer, nullable=False)
    monthly_payment = Column(Float, nullable=False)
    status = Column(String, default='pending')
    application_date = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='loans')
    account = relationship('Bank_Account', back_populates='loans')
