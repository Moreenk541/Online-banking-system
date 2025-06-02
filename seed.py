from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Bank_Account, Transaction
from datetime import datetime

# Database URL 
DATABASE_URL = "sqlite:///bank.db"

def seed_data():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
       
        if session.query(User).first():
            print("Database already seeded. Skipping seeding process.")
            return

        # Create Users
        user1 = User(name="Alice Smith", contact=1234567890, email="alice@example.com", password="password123")
        user2 = User(name="Bob Johnson", contact=9876543210, email="bob@example.com", password="securepass")

        session.add_all([user1, user2])
        session.commit()

        # Create Bank Accounts
        account1 = Bank_Account(user=user1, account_type="Savings", balance=1000.00)
        account2 = Bank_Account(user=user1, account_type="Checking", balance=500.00)
        account3 = Bank_Account(user=user2, account_type="Savings", balance=2500.00)

        session.add_all([account1, account2, account3])
        session.commit()

        # Create Transactions
        transaction1 = Transaction(account=account1, type="Deposit", amount=200.00, timestamp=datetime.utcnow())
        transaction2 = Transaction(account=account2, type="Withdrawal", amount=50.00, timestamp=datetime.utcnow())
        transaction3 = Transaction(account=account1, type="Transfer", amount=100.00, timestamp=datetime.utcnow())

        session.add_all([transaction1, transaction2, transaction3])
        session.commit()

        print("Database seeded successfully!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred during seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
