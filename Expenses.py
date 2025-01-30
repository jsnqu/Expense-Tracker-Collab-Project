import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), "./include"))
import tGame, CONTROLS, KEY, Colour



class ExpensesApp:
    def __init__(self):
        self.expenses_list = []
        self.key_in = tGame.KeyboardInput()

    def __del__(self):
        tGame.end()
        
    def run(self):
        self.add_expense()
        
    def view_expenses(self):
        pass
    def add_expense(self):
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
        print(f"{expense['name']}, {expense['amt']}")
        self.expenses_list.append(obj)
        
    def remove_expense(self):
        pass
        
    def filter_expenses(self):
        pass
    def calculate_expenses(self):
        pass
        
if __name__ =="__main__":
    tGame.init()
    try:
        app = ExpensesApp()
        app.run()
    finally:
        tGame.end()
