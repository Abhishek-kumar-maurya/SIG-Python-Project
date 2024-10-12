import json
import pandas as pd
from datetime import datetime

# User class for handling user data
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }

# FinanceRecord class for handling individual records of income/expenses
class FinanceRecord:
    def __init__(self, description, amount, category):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Automatically set the current date and time

    def to_dict(self):
        return {
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'date': self.date
        }

# FinanceManager class to manage all financial data
class FinanceManager:
    def __init__(self, user_file='users.json', finance_file='finances.json'):
        self.user_file = user_file
        self.finance_file = finance_file
        self.users = self.load_users()
        self.finances = self.load_finances()
        self.current_user = None  # To track the logged-in user

    # Load user data from the JSON file
    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # Load finance data from the JSON file
    def load_finances(self):
        try:
            with open(self.finance_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # Save user data to the JSON file
    def save_users(self):
        with open(self.user_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    # Save financial data to the JSON file
    def save_finances(self):
        with open(self.finance_file, 'w') as file:
            json.dump(self.finances, file, indent=4)

    # User registration with interactive input
    def register_user(self):
        username = input("Enter a new username: ")
        if username in self.users:
            print(f"User {username} already exists.")
            return False
        password = input("Enter a password: ")
        self.users[username] = User(username, password).to_dict()
        self.save_users()
        print(f"User {username} registered successfully.")
        return True

    # User login with interactive input
    def login_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            print(f"Welcome {username}!")
            return True
        else:
            print("Invalid credentials.")
            return False

    # Logout current user
    def logout_user(self):
        if self.current_user:
            print(f"User {self.current_user} logged out.")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    # Check if a user is logged in
    def check_login(self):
        if self.current_user is None:
            print("Please log in first.")
            return False
        return True

    # Add income/expense record for the logged-in user (with input prompts)
    def add_record(self):
        if not self.check_login():
            return

        description = input("Enter a description for the transaction: ")
        amount = float(input("Enter the amount (positive for income, negative for expense): "))
        category = input("Enter the category (e.g., groceries, salary, rent): ")
        
        # Create a new record with the current date/time automatically
        record = FinanceRecord(description, amount, category).to_dict()

        if self.current_user not in self.finances:
            self.finances[self.current_user] = []  # Create a list for the user's records

        self.finances[self.current_user].append(record)
        self.save_finances()
        print("Record added successfully.")

    # Update an existing record for the logged-in user (with input prompts)
    def update_record(self):
        if not self.check_login():
            return

        self.list_records()  # Show all current records
        record_id = int(input("Enter the ID of the record you want to update: "))

        if self.current_user not in self.finances or record_id >= len(self.finances[self.current_user]):
            print("Invalid record ID.")
            return

        description = input("Enter a new description: ")
        amount = float(input("Enter the new amount: "))
        category = input("Enter the new category: ")

        # Automatically update the record with the new description, amount, category, and current date/time
        self.finances[self.current_user][record_id] = FinanceRecord(description, amount, category).to_dict()
        self.save_finances()
        print("Record updated successfully.")

    # Delete a record for the logged-in user (with input prompts)
    def delete_record(self):
        if not self.check_login():
            return

        self.list_records()  # Show all current records
        record_id = int(input("Enter the ID of the record you want to delete: "))

        if self.current_user not in self.finances or record_id >= len(self.finances[self.current_user]):
            print("Invalid record ID.")
            return

        del self.finances[self.current_user][record_id]
        self.save_finances()
        print("Record deleted successfully.")

    # List all records for the logged-in user
    def list_records(self):
        if not self.check_login():
            return

        if self.current_user not in self.finances or len(self.finances[self.current_user]) == 0:
            print("No records found for this user.")
            return

        for idx, record in enumerate(self.finances[self.current_user]):
            print(f"{idx}: {record}")

    # Generate financial reports for the logged-in user using pandas
    def generate_report(self):
        if not self.check_login():
            return

        if self.current_user not in self.finances or len(self.finances[self.current_user]) == 0:
            print("No records found for this user.")
            return

        # Load data into a pandas DataFrame
        df = pd.DataFrame(self.finances[self.current_user])

        # Total income and expenses
        print("\nTotal Income and Expenses:")
        print(df.groupby('category')['amount'].sum())

        # Spending distribution by category
        print("\nSpending Distribution by Category:")
        print(df.groupby('category')['amount'].sum() / df['amount'].sum() * 100)

        # Monthly or weekly trends
        df['date'] = pd.to_datetime(df['date'])
        print("\nMonthly Trends:")
        print(df.groupby(df['date'].dt.to_period('M'))['amount'].sum())

# Interactive menu to allow the user to select options
def main_menu():
    manager = FinanceManager()

    while True:
        if manager.current_user:
            # Menu shown when the user is logged in
            print("\n--- Personal Finance Manager (Logged in as {}) ---".format(manager.current_user))
            print("1. Add Record")
            print("2. Update Record")
            print("3. Delete Record")
            print("4. List Records")
            print("5. Generate Report")
            print("6. Logout")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                manager.add_record()
            elif choice == "2":
                manager.update_record()
            elif choice == "3":
                manager.delete_record()
            elif choice == "4":
                manager.list_records()
            elif choice == "5":
                manager.generate_report()
            elif choice == "6":
                manager.logout_user()
            elif choice == "7":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            # Menu shown when the user is not logged in
            print("\n--- Personal Finance Manager ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                manager.register_user()
            elif choice == "2":
                manager.login_user()
            elif choice == "3":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
