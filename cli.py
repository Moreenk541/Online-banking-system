from app import register_user,login,create_account,deposit,withdraw,view_transactions,transfer_funds
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
    accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
    if not accounts:
        acc_type = input("Create account - type(Savings/checking):")
        create_account(user,acc_type) 
        session.commit()  
        accounts = session.query(Bank_Account).filter_by(user_id = user.id).all()
    print('\n Your Accounts:')
    for i, acc in enumerate(accounts):  
        print(f'\n{i+1}. {acc.account_type.capitalize()} (Balance: {acc.balance})')  

    choice=int (input('Select account: ')) 
    account =accounts[choice-1]   
    while True:
        print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. Transactions\n5.Switch Account \n6.Create new Account \n7.Transfer funds \n8Logout")
        choice = input("> ")

        if choice == "1":
            
            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")
            choice = int(input("Select account: "))
            account = accounts[choice - 1]

            print(f"Balance: ${account.balance}")


        elif choice == "2":


            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")
            choice = int(input("Select account: "))
            account = accounts[choice - 1]




            amount = float(input("Deposit amount: "))
            deposit(session,account, amount) 
        elif choice == "3":
            amount = float(input("Withdraw amount: "))
            withdraw(session,account, amount)
        elif choice == "4":
            view_transactions(account)
        elif choice == "5":
            #switch accounts
            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")
            choice = int(input("Select account: "))
            account = accounts[choice - 1]

        elif choice =="6":
            #new account
            acc_type = input("Create account - type(Savings/checking):")
            create_account(user,acc_type) 
            session.commit()


        elif choice =="7":
            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")

            target_index = int(input("Select account to transfer TO: ")) - 1
            target_account = accounts[target_index]

            if target_account.id == account.id:
                print("You can't transfer to the same account.")
                continue

            amount = float(input("Amount to transfer: "))
            transfer_funds(session, account, target_account, amount)


        elif choice == "8":
            break
