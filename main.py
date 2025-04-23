class Category:

    #Instantiate 
    def __init__(self, name):
        self.name = name
        self.ledger = []

    #Print Output
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for entry in self.ledger:
            description = entry["description"][:23]
            amount = f"{entry['amount']:.2f}"
            items += f"{description:<23}{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

    #Deposit
    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})  

    #Withdraw
    def withdraw(self, amount, description = ''):
        if not self.check_funds(amount):
            return False
        else:
            amount = -amount
            self.ledger.append({'amount': amount, 'description': description})   
            return True         

    #Balance
    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    #Transfer
    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {category.name}")             
        category.deposit(amount, f"Transfer from {self.name}")            
        return True

    #Check Funds
    def check_funds(self, amount):
        total = sum(item['amount'] for item in self.ledger)
        return total >= amount

                           
#Spending Chart
def create_spend_chart(categories):
    category_withdrawals = {}

    #Calculate Withdrawals
    for category in categories:
        withdrawals = 0
        for transaction in category.ledger:
            amount = transaction['amount']
            if amount < 0:
                withdrawals += -amount  # Add the amount spent (negative for withdrawals)
        category_withdrawals[category.name] = withdrawals

    #Calculate Total Withdrawals
    total_withdrawals = sum(category_withdrawals.values())

    #Calculate Percentages Spent
    category_percentages = {}
    for name, withdrawals in category_withdrawals.items():
        category_percentages[name] = (withdrawals / total_withdrawals) * 100 if total_withdrawals > 0 else 0

    #Create Chart
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

    #Print Names
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
       


food = Category('Food')
clothing = Category('Clothing')
auto = Category('Auto')
business = Category('Business')

food.deposit(1000, 'deposit')
food.withdraw(100.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing.deposit(200, 'deposit')
clothing.withdraw(75, 'shirt and pants')

auto.deposit(1000, 'deposit')
auto.withdraw(150, 'Brakes')
auto.withdraw(80, 'oil change')

business.deposit(5000, 'deposit')
business.withdraw(300, 'car rental')
business.withdraw(200, 'plane ticket')
business.withdraw(600, 'hotel')

food.transfer(50, clothing)
food.transfer(100, auto)

print(f'{food}\n\n{clothing}\n\n{auto}\n\n{business}\n')
print(create_spend_chart([food, clothing, auto, business]))