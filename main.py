import string
import re


class Category:
    # Instantiate
    def __init__(self, name):
        self.name = name
        self.ledger = []

    # Print Output
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for entry in self.ledger:
            description = entry["description"][:23]
            amount = f"{entry['amount']:.2f}"
            items += f"{description:<23}{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

    # Deposit
    def deposit(self, amount, description='deposit'):
        self.ledger.append({'amount': amount, 'description': description})

    # Withdraw
    def withdraw(self, amount, description=''):
        if not self.check_funds(amount):
            return False
        else:
            amount = -amount
            self.ledger.append({'amount': amount, 'description': description})
            return True

    # Balance
    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    # Transfer
    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    # Check Funds
    def check_funds(self, amount):
        total = sum(item['amount'] for item in self.ledger)
        return total >= amount


# Spending Chart Function
def create_spend_chart(categories):
    category_spendings = {}

    # Calculate spending for each category (withdrawals)
    for category in categories:
        spendings = 0
        for transaction in category.ledger:
            amount = transaction['amount']
            if amount < 0:  
                spendings += -amount 
        category_spendings[category.name] = spendings

    # Calculate total withdrawals
    total_spendings = sum(category_spendings.values())

    # Calculate percentages spent for each category relative to the total amount in each category
    category_percentages = {}
    for category in categories:
        total_balance = category.get_balance()  # Get the total balance in the category
        spendings = category_spendings.get(category.name, 0)
        percentage = (spendings / total_balance) * 100 if total_balance > 0 else 0
        category_percentages[category.name] = percentage

    # Create the chart string
    chart_str = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        line = f"{i:3}| "
        for name in category_percentages:
            percent = category_percentages[name]
            if percent >= i:
                line += "o  "
            else:
                line += "   "
        chart_str += line + "\n"

    chart_str += "    " + "-" * (len(category_percentages) * 3 + 1) + "\n"

    # Print Names
    max_name_length = max(len(name) for name in category_percentages)
    for i in range(max_name_length):
        line = "     "
        for name in category_percentages:
            if i < len(name):
                line += name[i] + "  "
            else:
                line += "   "
        chart_str += line + "\n"

    return chart_str.rstrip("\n")


# Helper Choose Category for the Budget Menu 
def choose_category(prompt, categories):
    if not categories:
        print("No categories available. Please create one first.")
        return None

    print(f"\n{prompt}")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.name}")

    choice = int(input("Select a category by number: "))
    print(f'Choice= {choice}')
    clean_choice = clean_input(choice)
    print(f'Clean choice= {clean_choice}')
    if clean_choice.isdigit():
        choice = int(clean_choice)  
        if 1 <= choice <= len(categories):
            return categories[choice - 1]
        else:
            print("Invalid selection. Category not found.")
            return None
    else:
        print("Invalid input. Please enter a valid number.")
        return None


# Clean input
def clean_input(text):
    # Remove non-printable characters and spaces at the ends
    cleaned_text = ''.join(ch for ch in text if ch in string.printable and ch != '\x7f')
    cleaned_text = re.sub(r'\s+', '', cleaned_text) 
    
    if cleaned_text and cleaned_text[0].isdigit():
        return cleaned_text[0]  
    else:
        return "" 


# Budget Menu 
def print_menu():
    print("\n=== Budget Menu ===")
    print("1. Create New Category")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Print Ledger")
    print("6. Print Spending Chart")
    print("7. Exit")


categories = []  

while True:
    print_menu()
    choice = input("Enter your choice: ")
    clean_choice = clean_input(choice)

    # Check for empty input
    if clean_choice == "":
        print("Invalid input. Please enter a valid number.")
        continue 

    # Create category
    if clean_choice == "1":
        name = input("Enter new category name: ")
        if any(cat.name == name for cat in categories):
            print("Category already exists.")
        else:
            new_category = Category(name)
            categories.append(new_category)  
            print(f"Category '{name}' created.")

    # Deposit
    elif clean_choice == "2":
        category = choose_category("Select a category to deposit into:", categories)
        if category:
            amount = float(input("Amount: "))
            category.deposit(amount)

    # Withdraw
    elif clean_choice == "3":
        category = choose_category("Select a category to withdraw from:", categories)
        if category:
            amount = float(input("Amount: "))
            description = input("Description: ")
            if not category.withdraw(amount, description):
                print("Insufficient funds.")

    # Transfer
    elif clean_choice == "4":
        from_cat = choose_category("Select the category to transfer FROM:", categories)
        to_cat = choose_category("Select the category to transfer TO:", categories)
        if from_cat and to_cat:
            amount = float(input("Amount: "))
            if not from_cat.transfer(amount, to_cat):
                print("Insufficient funds.")

    # Print ledger
    elif clean_choice == "5":
        print("\n1. Print all categories")
        print("2. Print one category")
        sub_choice = input("Select an option: ")
        clean_sub_choice = clean_input(sub_choice)

        if clean_sub_choice == "1":
            if not categories:
                print("No categories available. Please create one first.")
            for cat in categories:
                print(f'\n{cat}\n')
        elif clean_sub_choice == "2":
            category = choose_category("Select a category to view its ledger:", categories)
            if category:
                print(f'\n{category}\n')
        else:
            print("Invalid selection.")

    # Print spending chart
    elif clean_choice == "6":
        if categories:
            print(create_spend_chart(categories))
        else:
            print("No categories available to display chart.")

    elif clean_choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")


   
