from conn import SessionLocal
from models import User, Bank_Account, Transaction, Loan

from sqlalchemy.exc import IntegrityError


session = SessionLocal()

#Registering

def register_user(name,contact,email,password):
    user = User(name=name,contact=contact,email=email,password=password)

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
def transfer_funds(session, from_account, to_account, amount):
    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount

        # Record both transactions
        t1 = Transaction(account_id=from_account.id, type='transfer_out', amount=amount)
        t2 = Transaction(account_id=to_account.id, type='transfer_in', amount=amount)

        session.add_all([t1, t2])
        session.commit()
        print(f"Transferred ${amount} from {from_account.account_type} to {to_account.account_type}")
    else:
        print("Insufficient funds for transfer.")

def apply_for_loan(session, user_id, account_id, loan_amount, months):
    user = session.query(User).filter_by(id=user_id).first()
    account = session.query(Bank_Account).filter_by(id=account_id, user_id=user_id).first()

    if not user or not account:
        print("User or account not found.")
        return False

    if account.account_type.lower() != 'checking' or account.balance < 5000:
        print("Loan application requires a checking account with a balance of at least $5,000.")
        return False

    if not (0 < loan_amount <= 30000):
        print("Loan amount must be between $1 and $30,000.")
        return False

    if not (0 < months <= 6):
        print("Loan repayment period must be between 1 and 6 months.")
        return False

    interest_rate_per_month = 0.08
    monthly_payment = (loan_amount * (1 + interest_rate_per_month * months)) / months

    try:
        loan = Loan(
            user_id=user.id,
            account_id=account.id,
            amount=loan_amount,
            interest_rate=interest_rate_per_month,
            months=months,
            monthly_payment=monthly_payment,
            status='approved' # Automatically approve for simplicity
        )
        session.add(loan)

        # Add loan amount to account balance
        account.balance += loan_amount
        
        # Record transaction for loan
        transaction = Transaction(account_id=account.id, type='loan_credit', amount=loan_amount)
        session.add(transaction)

        session.commit()
        print(f"Loan of ${loan_amount} approved for {months} months. Monthly payment: ${monthly_payment:.2f}")
        return True
    except Exception as e:
        session.rollback()
        print(f"An error occurred during loan application: {e}")
        return False
