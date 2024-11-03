#The following code basically allows users to login and track their expenses and they are saved in a database. 

from Expense import Expense
import sqlite3  
import calendar  
import datetime  

# Define the Expense class to create expense objects
class Expense:
    def __init__(self, name, category, amount):
        self.name = name  
        self.category = category  
        self.amount = amount  

# Function to create the database and necessary tables
def create_database():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to register a new user
def register_user():
    conn = sqlite3.connect('expense_tracker.db')  
    cursor = conn.cursor()

    # Get username and password from user input
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    try:
        
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()  
        print("User registered successfully!")  
    except sqlite3.IntegrityError:
        print("Username already exists. Please try a different one.")  
    finally:
        conn.close()  # Close the database connection

# Function to log in a user
def login_user():
    conn = sqlite3.connect('expense_tracker.db') 
    cursor = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Query the users table for matching credentials
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()  
    conn.close() 

    if user:
        print("Login successful!")  
        return user[0]  
    else:
        print("Invalid username or password.")  
        return None  

# Function to get expense details from the user
def get_user_expense():
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")

    # Input validation for expense amount
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the amount.")

    # List of expense categories
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Miscellaneous",
    ]

    # Loop until a valid category is selected
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
                return new_expense  # Exit the loop and return the expense
            else:
                print("Invalid category. Please try again!")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Function to save an expense to the database
def save_expense_to_db(expense: Expense, user_id):
    print(f"🎯 Saving User Expense: {expense.name} to the database")  
    conn = sqlite3.connect('expense_tracker.db')  
    cursor = conn.cursor()
    
    # Insert the expense details into the expenses table
    cursor.execute('INSERT INTO expenses (user_id, name, amount, category) VALUES (?, ?, ?, ?)',
                   (user_id, expense.name, expense.amount, expense.category))
    conn.commit() 
    conn.close()  

# Function to summarize the user's expenses
def summarize_expenses(user_id, budget):
    print("🎯 Summarizing User Expense")  
    conn = sqlite3.connect('expense_tracker.db')  
    cursor = conn.cursor()

    # Query the expenses for the logged-in user
    cursor.execute('SELECT name, amount, category FROM expenses WHERE user_id = ?', (user_id,))
    expenses = cursor.fetchall()  
    conn.close()  

    amount_by_category = {} 
    # Calculate total amounts by category
    for expense_name, expense_amount, expense_category in expenses:
        if expense_category in amount_by_category:
            amount_by_category[expense_category] += expense_amount  
        else:
            amount_by_category[expense_category] = expense_amount  

    print("Expenses By Category :")  
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")  

    total_spent = sum(amount_by_category.values()) 
    print(f"💵 Total Spent: ${total_spent:.2f}") 

    remaining_budget = budget - total_spent  
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")  

    now = datetime.datetime.now()  
    days_in_month = calendar.monthrange(now.year, now.month)[1] 
    remaining_days = days_in_month - now.day 

    if remaining_days > 0:  
        daily_budget = remaining_budget / remaining_days  
        print(f"👉 Budget Per Day: ${daily_budget:.2f}") 
    else:
        print("No remaining days in the month to calculate daily budget.")  

# Main function to run the expense tracker application
def main():
    create_database()  
    print("🎯 Running Expense Tracker!") 
    budget = 2000  #This is the default budget that the user has. 

    # User registration or login
    choice = input("Do you want to (1) Register or (2) Login? ")  
    if choice == '1':
        register_user() 
    
    user_id = login_user() 
    if user_id is None: 
        return  

    # Get user input for expense.
    expense = get_user_expense()  
    save_expense_to_db(expense, user_id) 
    summarize_expenses(user_id, budget)  

# Entry point for the program
if __name__ == "__main__":
    main()  

