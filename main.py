import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_category, get_amount, get_description,plot_transactions


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date",
                 "amount",
                 "category",
                 "description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError as e:
            df = pd.DataFrame(cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount,category,description):
        new_entry = {
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }
        with open(cls.CSV_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")


        mask = (df["date"] >= start_date) & (df["date"] <= end_date) 
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No tranaction")
        else:
            print(f"Transaction from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x:x.strftime("%d-%m-%Y")}))

        total_income = filtered_df[filtered_df["category"]== "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] =="Expense"]["amount"].sum()
        print(f"\n Summary total income ${total_income} expense ${total_expense}")
        print(f"Net total {total_income-total_expense}")

        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction dd-mm-yyy", allow_default=True)
    amount = get_amount()
    category=get_category()
    description = get_description()
    CSV.add_entry( date,  amount,  category, description)


def main():
    while True:
        print("\n 1. Add new transaction")
        print(" 2. Print summary with date")
        print(" 3. Exit")
        choice = input("Enter your input ")

        if choice == "1":
            add()
        elif choice =="2":
            start_date = get_date("Enter a start date 'mm-dd-yyyy': ")
            end_date = get_date("Enter a end date 'mm-dd-yyyy': ")
            df = CSV.get_transactions(start_date,end_date)
            if input("Do you want to see a graph (y/n)".lower()) == "y":
                plot_transactions(df)
                continue
            else:
                break
        elif choice == "3":
            print("Exiting the program...")
            break
        else: 
            print("Invalid choice")


if __name__ == "__main__":
    main()
