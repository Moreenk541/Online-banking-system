from conn import SessionLocal
from models import User, Bank_Account, Transaction

from sqlalchemy.exc import IntegrityError


session = SessionLocal()

#Registering

def register_user(name,email,password):
    user = User(name=name,email=email,password=password)

    try:
        session.add(user)
        session.commit()
        print("user registered successfully!")

    except IntegrityError:
        session.rollback()
        print('Email already exists.')  

#logging in          

def login(email, password):
    user = session.query(User).filter_by(email=email,password=password).first()

    if user:
        print(f'Welcome, {user.name}!')
        return user
    else:
        print('Invalid credentials.')
        return None
    
#creating account

def create_account(user, account_type):
    account = Bank_Account(user_id=user.id, account_type=account_type)
    session.add(account)
    session.commit()
    print(f'{account_type.capitalize()} account created successfully!')


#deposit
def deposit(session,account,amount):
    account.balance  += amount 
    transaction =Transaction(account_id =account.id, type ="deposit", amount=amount)
    session.add(transaction)
    session.commit()
    print(f"Deposited ${amount} successfully.")

#withdwraw
def withdraw(session,account,amount):
    if account.balance >= amount:
        account.balance -=amount
        transaction =Transaction(account_id=account.id,type='withdraw',amount=amount)
        session.add(transaction)
        session.commit()
        print(f"Successful withdrwal of ${amount}")

    else:
        print('Insufficient funds')    


#     Transactions
def view_transactions(account):
    transactions = session.query(Transaction).filter_by(account_id = account.id).all()
    for t in transactions:
        print(f'{t.timestamp} - {t.type} - ${t.amount}')
