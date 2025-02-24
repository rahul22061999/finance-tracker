from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

CATEGORIES = {
    "I":"Income",
    "E":"Expense"
}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")  
    try:
        valid_date = datetime.strptime(date_str, "%d-%m-%Y")  
        return valid_date.strftime("%d-%m-%Y")  
    except ValueError:
        print("Invalid date format! Please enter in DD-MM-YYYY format.")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("Amount must be not be 0 or negative")
        return amount
    except ValueError as e:
        print("Error",e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for income or 'E' for Expense)".upper())
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category please enter 'I' for income or 'E' for Expense")
    return get_category()

def get_description():
    return input("Enter a description")

def plot_transactions(df):
    df.set_index('date', inplace =True)

    income_df = df[df['category']=="Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df['category']=="Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color='g')

    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color='r')
    plt.legend()
    plt.grid(True)
    plt.show()