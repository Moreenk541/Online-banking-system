from app import register_user,login,create_account,deposit,withdraw,view_transactions
from models import Bank_Account

current_user =None


def main_menu():
    while True:
        print("\n1. Register \n2. Login \n 3. Exit")
        choice = input(">")


        if choice =="1":
            name = input('Name: ')
            email = input('Email: ')
            password = input('Password: ')

            register_user(name,email,password)

        elif  choice =="2"  :
            email=input('Email: ')
            password = input('Password: ')
            user = login(email,password)
            if user :
                user_menu(user)

        elif choice=="3":
            break


def user_menu(user):
    from conn import SessionLocal  
    session = SessionLocal()   
    account = session.query(Bank_Account).filter_by(user_id=user.id).first()
    if not account:
        acc_type = input("Create account - type(Savings/checking):")
        create_account(user,acc_type)   
        account = session.query(Bank_Account).filter_by(user_id = user.id).first()
    while True:
        print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. Transactions\n5. Logout")
        choice = input("> ")

        if choice == "1":
            print(f"Balance: ${account.balance}")
        elif choice == "2":
            amount = float(input("Deposit amount: "))
            deposit(account, amount) 

        elif choice == "3":
            amount = float(input("Withdraw amount: "))
            withdraw(account, amount)
        elif choice == "4":
            view_transactions(account)
        elif choice == "5":
            break
