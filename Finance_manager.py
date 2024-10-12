import json
import pandas as pd
from datetime import datetime
import os

# User Class: To handle user registration and login
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_user(self):
        # Check if the users.json file exists, if not create one with an empty dictionary
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                users = json.load(file)
        else:
            users = {}

        # Add or update user in the dictionary
        users[self.username] = self.password

        # Write the updated users dictionary back to users.json
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)
        print(f"User {self.username} registered successfully!")

    @staticmethod
    def login(username, password):
        # Ensure the users.json file exists
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                users = json.load(file)
                if username in users and users[username] == password:
                    return True
                return False
        else:
            print("No users registered.")
            return False

# FinanceRecord Class: To manage individual finance records (income/expenses)
class FinanceRecord:
    def __init__(self, username, description, amount, category, date=None):
        self.username = username
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def save_record(self):
        # Ensure the finances.json file exists
        if os.path.exists('finances.json'):
            with open('finances.json', 'r') as file:
                finances = json.load(file)
        else:
            finances = {}

        # Add a new list for the user if not already present
        if self.username not in finances:
            finances[self.username] = []

        # Add the new record to the user's financial records
        finances[self.username].append({
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'date': self.date
        })

        # Write the updated finances dictionary back to finances.json
        with open('finances.json', 'w') as file:
            json.dump(finances, file, indent=4)
        print("Record added successfully!")

# FinanceManager Class: To handle operations like adding records, generating reports
class FinanceManager:
    def __init__(self, username):
        self.username = username

    def add_record(self, description, amount, category):
        record = FinanceRecord(self.username, description, amount, category)
        record.save_record()

    def generate_report(self):
        # Ensure the finances.json file exists
        if os.path.exists('finances.json'):
            with open('finances.json', 'r') as file:
                finances = json.load(file)
                if self.username in finances:
                    df = pd.DataFrame(finances[self.username])
                    return df
                else:
                    return pd.DataFrame([])
        else:
            print("No financial records found.")
            return pd.DataFrame([])

# Function to load data
def load_json_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

# Main function
if __name__ == "__main__":
    users_data = load_json_data('users.json')
    finances_data = load_json_data('finances.json')

    print("Welcome to Personal Finance Manager!")
    action = input("Do you want to login or register? (login/register): ").strip().lower()

    if action == 'register':
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        new_user = User(username, password)
        new_user.save_user()

    elif action == 'login':
        username = input("Enter username: ")
        password = input("Enter password: ")

        if User.login(username, password):
            print(f"Welcome back, {username}!")
            manager = FinanceManager(username)
            
            while True:
                print("\nOptions: add (Add record), report (Generate Report), exit (Exit)")
                option = input("Choose an option: ").strip().lower()

                if option == 'add':
                    desc = input("Enter description: ")
                    amount = float(input("Enter amount: "))
                    category = input("Enter category (e.g. groceries, salary, rent): ")
                    manager.add_record(desc, amount, category)

                elif option == 'report':
                    df = manager.generate_report()
                    if df.empty:
                        print("No financial records found.")
                    else:
                        print(df)
                        print("Total Income/Expenses by Category:")
                        print(df.groupby('category')['amount'].sum())

                elif option == 'exit':
                    break
                else:
                    print("Invalid option, please try again.")
        else:
            print("Login failed. Incorrect username or password.")
