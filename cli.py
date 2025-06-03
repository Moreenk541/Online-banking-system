from app import register_user,login,create_account,deposit,withdraw,view_transactions,transfer_funds,apply_for_loan,delete_account_feature
from models import Bank_Account, User

current_user =None


def main_menu():
    while True:
        print("\n1. Register \n2. Login \n 3. Exit")
        choice = input(">")


        if choice =="1":
            name = input('Name: ')
            contact= input('contact')
            email = input('Email: ')
            password = input('Password: ')

            register_user(name,contact,email,password)

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

    while True:
        try:
            choice = int(input('Select account: '))
            if 1 <= choice <= len(accounts):
                account = accounts[choice - 1]
                break
            else:
                print("Invalid account number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    while True:
        print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. Transactions\n5.Switch Account \n6.Create new Account \n7.Transfer funds \n8. Apply for Loan \n9. Delete Account \n10. Logout")
        choice = input("> ")

        if choice == "1":
            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")
            while True:
                try:
                    choice = int(input("Select account: "))
                    if 1 <= choice <= len(accounts):
                        account = accounts[choice - 1]
                        break
                    else:
                        print("Invalid account number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            print(f"Balance: ${account.balance}")


        elif choice == "2":
            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            # for i, acc in enumerate(accounts):
            #     print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")
            # while True:
            #     try:
            #         choice = int(input("Select account: "))
            #         if 1 <= choice <= len(accounts):
            #             account = accounts[choice - 1]
            #             break
            #         else:
            #             print("Invalid account number. Please try again.")
            #     except ValueError:
            #         print("Invalid input. Please enter a number.")

            amount = float(input("Deposit amount: "))
            deposit(session,account, amount) 
        elif choice == "3":
            amount = float(input("Withdraw amount: "))
            withdraw(session,account, amount)
            print(f'Successful withdraw of &{amount:.2f}')
        elif choice == "4":
            view_transactions(account)
        elif choice == "5":
            #switch accounts
            accounts = session.query(Bank_Account).filter_by(user_id=user.id).all()
            print("\nYour Accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")
            while True:
                try:
                    choice = int(input("Select account: "))
                    if 1 <= choice <= len(accounts):
                        account = accounts[choice - 1]
                        break
                    else:
                        print("Invalid account number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        elif choice =="6":
            #new account
            acc_type = input("Create account - type(Savings/checking):")
            create_account(user,acc_type) 
            session.commit()


        elif choice == "7":
            try:
                target_account_id = int(input('Enter target account ID to transfer TO: '))
                target_account = session.query(Bank_Account).filter_by(id=target_account_id).first()

                if not target_account:
                    print("Target account not found.")
                    continue

                if target_account.id == account.id:
                    print("You can't transfer to the same account.")
                    continue

                amount = float(input("Amount to transfer: "))
                transfer_funds(session, account, target_account, amount)
                print(f"\n You have successfully transferred ${amount:.2f} "
                f"from Account ID {account.id} to Account ID {target_account.id}.")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

       


        elif choice == "8":
            # Apply for Loan
            checking_accounts = [acc for acc in accounts if acc.account_type.lower() == 'checking']
            if not checking_accounts:
                print("You need a checking account to apply for a loan.")
                continue

            print("\nSelect a checking account for the loan application:")
            for i, acc in enumerate(checking_accounts):
                print(f"{i + 1}. {acc.account_type.capitalize()} (Balance: ${acc.balance})")

            selected_checking_account = None
            while True:
                try:
                    acc_choice = int(input("Select account: "))
                    if 1 <= acc_choice <= len(checking_accounts):
                        selected_checking_account = checking_accounts[acc_choice - 1]
                        break
                    else:
                        print("Invalid account number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            if selected_checking_account.balance < 5000:
                print("Your checking account balance must be at least $5,000 to apply for a loan.")
                continue

            try:
                loan_amount = float(input("Enter loan amount (up to $30,000): "))
                if not (0 < loan_amount <= 30000):
                    print("Invalid loan amount. Must be between $1 and $30,000.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number for the loan amount.")
                continue

            try:
                months = int(input("Enter repayment months (1-6): "))
                if not (0 < months <= 6):
                    print("Invalid number of months. Must be between 1 and 6.")
                    continue
            except ValueError:
                print("Invalid input. Please enter an integer for months.")
                continue

            apply_for_loan(session, user.id, selected_checking_account.id, loan_amount, months)

        elif choice == "9":
            # Delete Account
            confirm = input("Are you sure you want to delete this account? (yes/no): ").lower()
            if confirm == 'yes':
                if delete_account_feature(session, account):
                    # If account is deleted, break from the current account menu and go back to user menu
                    break 
            else:
                print("Account deletion cancelled.")
        elif choice == "10":
            break
