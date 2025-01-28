
class ExpensesApp:
    def __init__(self):
        self.expenses_list = []
        
    def run(self):
        self.expenses_list
        self.add_expense()
        print(self.expenses_list)
        
    def view_expenses(self):
        pass
    def add_expense(self):
        self.expenses_list
        name = input("What is your expense? ").title().strip()
        while True:
            amount = input("How much is your expense? ").title().strip()
            if amount.isdigit():
                amount = int(amount)
                break
            else:
                print("Invalid Amount")
        expense = {
            "name": name,
            "amt": amount
        }
        print(f"{expense["name"]}, {expense["amt"]}")
        self.expenses_list.append(obj)
        
    def remove_expense(self):
        pass
        
    def filter_expenses(self):
        pass
    def calculate_expenses(self):
        pass
        
if __name__ =="__main__":
    app = ExpensesApp()
    app.run()