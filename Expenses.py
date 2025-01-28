MONTH_NAMES = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')

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
            "amt": amount,
            "date": self.input_date()
        }
        print(f"{expense['name']}, {expense['amt']}")
        self.expenses_list.append(expense)

    @staticmethod
    def input_date():
        print()
        while True:
            year = input("Year: ")
            if year.isdigit():
                year = str(int(year))
                break
        while True:
            month = input("Month: ")
            if (month.isdigit() and 1<=int(month)<=12):
                # strips leading zero if inputted
                month = str(int(month))
                break
            elif month.lower() in MONTH_NAMES:
                month = str(MONTH_NAMES.index(month.lower())+1)
                break
        while True:
            day = input("Day: ")
            if day.isdigit():
                if (month == '2' and int(day)==29):
                    if (int(year) % 4 == 0):
                        # strips leading zero if inputted
                        day = str(int(day))
                        break
                    else:
                        continue
    
                elif (1<=int(day)<=30 and month in "4 6 9 11".split()) or (
                      1<=int(day)<=31 and month in "1 3 5 7 8 10 12".split()) or (
                      1<=int(day)<=28 and month == '2'):
                    # strips leading zero if inputted
                    day = str(int(day))
                    break
        return [year, month, day]
        
    def remove_expense(self):
        pass
        
    def filter_expenses(self):
        pass
    def calculate_expenses(self):
        pass
        
if __name__ =="__main__":
    app = ExpensesApp()
    app.run()
