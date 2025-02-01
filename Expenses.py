import os,sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "./include"))
import tGame, CONTROLS, KEY, Colour
from Menu import Keypad

MONTH_NAMES = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')

HINT_COLOUR = Colour.getCodeRGB((100, 20, 7), Colour.COLOUR_OPTION.FOREGROUND)
INVALID_COLOUR = Colour.getCodeBasic("RED", Colour.COLOUR_OPTION.AUTO_BACK)

class ExpensesApp:
    def __init__(self):
        self.key_in = tGame.KeyboardInput()

        self.main_menu = Keypad(
                ["Add Expense", "Remove Expense", "View Expense", "Exit"])
        self.main_menu.format(x=2,y=7,
                              layout=Keypad.LAYOUT.VERTICAL,
                              text_colour=(100,100,150))
        self.remove_menu = Keypad(
                ["Back to Input", "View Expenses", "Exit"])
        self.remove_menu.format(x=2,y=8,
                              layout=Keypad.LAYOUT.HORIZONTAL,
                              padding=2,
                              text_colour=(100, 20, 7))

        self.expenses_list = []

    def __del__(self):
        tGame.end()
        
    def run(self):
        tGame.setTitle("Expense tracker") # Window title

        tGame.screenClear()
        tGame.setCursor(2,2) # Starts topleft at (j,1)
        tGame.render("Welcome to expense tracker!\n"+"_"*29) # Appends to tGame.render_buffer (str)

        tGame.renderCopy() # sys.stdout.write(tGame.render_buffer)
        # tGame.render_buffer contains anything from tGame.render() (check tGame.py)

        while True:
            self.main_menu.index = 0 # Sets current choice to first option

            tGame.setCursor(2,5)
            tGame.render("What would you like to do?")

            self.main_menu.draw() # Draws before the blocking input call
            tGame.renderCopy()

            while True:
                self.key_in.clearPipe() # Clears input prevents accidental choice (from holding button)
                action = self.main_menu.update(self.key_in.keyNext()) # Redraws by default
                tGame.renderCopy() # Required for Keypad draws including the one called by update(input_, draw=True)

                if not action: # CONTROLS.ACTION wasn't pressed, nothing submitted
                    continue
                else:
                    break
                    
            # Keypad.update() returns tuple: (choice_index, choice_name)
            # choice_index is recommended bc it's has to be unique
            match action[0]: 
                case 0:
                    self.add_expense() # New scene
                case 1:
                    self.remove_menu.index = 0 # Refer line 44 (sets to first option)
                    self.remove_expense() # New scene
                case 2:
                    tGame.setCursor(2,12)
                    tGame.renderCopy()

                    self.view_expenses() # Not new scene (yet?) TODO
                    self.key_in.keyNext() # Waits for any input before screenClear() is called
                case 3:
                    return
            time.sleep(0.1)
            tGame.screenClear()

    def view_expenses(self):
        tGame.moveCursor('D', 500)
        tGame.renderCopy()
        if len(self.expenses_list) == 0: #user has no expenses
            print("You currently have no expenses.")
        else:
            reminder_number = 1
            for expense in self.expenses_list:
                print(f"{reminder_number}. {expense['name']}: {expense['amt']} ({expense['date']})")
                reminder_number+=1

    def add_expense(self):
        tGame.screenClear()
        tGame.setCursor(2,5)
        tGame.render("What is your expense?")
        tGame.renderCopy()

        name = tGame.textInput(self.key_in, 2, 6)
        if name == CONTROLS.ESCAPE or name == KEY.QUIT:
            return
        name = name.title().strip()
        while True:
            tGame.setCursor(2, 7)
            tGame.render("How much is your expense? ")
            tGame.setCursor(2, 8)
            tGame.render("\033[2K")
            tGame.renderCopy()

            amount = tGame.textInput(self.key_in, 2, 8)
            if amount == CONTROLS.ESCAPE or name == KEY.QUIT:
                return

            if amount.isdigit():
                amount = int(amount)
                break
            else:
                tGame.setCursor(2, 9)
                tGame.render(INVALID_COLOUR+"Invalid Amount"+ Colour.RESET)
                tGame.renderCopy()
        tGame.setCursor(1, 11)
        tGame.renderCopy()
        expense = {
            "name": name,
            "amt": amount,
            "date": self.input_date()
        }
        self.expenses_list.append(expense)

    @staticmethod
    def input_date():
        today = time.strftime("%Y %m %d").split()
        print("Leave blank for current date")

        # Year
        while True:
            year = input("Year: ").strip()
            if year.isdigit():
                year = str(int(year))
                break
            elif len(year) == 0:
                year = str(int(today[0]))
                break

        # Month
        while True:
            month = input("Month: ").strip()
            if (month.isdigit() and 1<=int(month)<=12):
                # strips leading zero if inputted
                month = str(int(month))
                break
            elif month.lower() in MONTH_NAMES:
                month = str(MONTH_NAMES.index(month.lower())+1)
                break
            elif len(month) == 0:
                month = str(int(today[1]))
                break

        # Day
        while True:
            day = input("Day: ").strip()
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
            elif len(day) == 0:
                day = str(int(today[2]))
                break
        return [year, month, day]      

    def remove_expense(self):
        tGame.screenClear()
        tGame.setCursor(2,5)

        tGame.render(Colour.FOREGROUND["RED"]+"Which one would you like to remove?"+Colour.RESET)

        tGame.setCursor(2,8)
        tGame.render(HINT_COLOUR+"(ESCAPE) for options" + Colour.RESET)

        tGame.setCursor(2,9)
        tGame.renderCopy()

        self.view_expenses()

        while True:
            tGame.setCursor(2,6)
            tGame.render("\033[2K")

            choice = tGame.textInput(self.key_in, 2, 6)

            if choice == CONTROLS.ESCAPE or choice == KEY.QUIT:
                tGame.setCursor(1,8)
                tGame.render("\033[2K")
                self.remove_menu.draw()
                tGame.renderCopy()
                while self.key_in.keyIn():
                    action = self.remove_menu.update(self.key_in.pressed)
                    tGame.renderCopy()
                    if action:
                        match action[0]:
                            case 0: break
                            case 1:
                                tGame.setCursor(2,9)
                                tGame.renderCopy()
                                self.view_expenses()
                            case 2: return

            elif choice.isdigit() and int(choice) in range (1,len(self.expenses_list)+1):
                choice = int(choice)
                self.expenses_list.pop(choice-1)

                tGame.screenClear()
                tGame.setCursor(2,2)
                tGame.render("Your remaining expenses are:")
                tGame.setCursor(2,4)
                tGame.renderCopy()
                self.view_expenses()

                tGame.render(HINT_COLOUR+"(ANY KEY) to continue\n\n"+Colour.RESET)
                tGame.renderCopy()
                self.key_in.keyIn()
                break

            else:
                tGame.setCursor(2, 7)
                tGame.render(INVALID_COLOUR+
                             "Invalid Option" + Colour.RESET)
                tGame.renderCopy()

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
