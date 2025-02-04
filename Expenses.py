import os,sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "./include"))
import tGame, CONTROLS, KEY, Colour
from Menu import Keypad

MONTH_NAMES = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')

HINT_COLOUR = Colour.getCodeRGB((100, 20, 7), Colour.COLOUR_OPTION.FOREGROUND)
INVALID_COLOUR = Colour.getCodeBasic("RED", Colour.COLOUR_OPTION.AUTO_BACK)

ORIGIN_POS = (2,2)

class ExpensesApp:
    def __init__(self):
        self.key_in = tGame.KeyboardInput()

        self.main_menu = Keypad(
                ["Add Expense", "Remove Expense", "View Expense", "Exit"])
        self.main_menu.format(x=ORIGIN_POS[0],y=ORIGIN_POS[1]+5,
                              layout=Keypad.LAYOUT.VERTICAL,
                              text_colour=(100,100,150))
        self.remove_menu = Keypad(
                ["Back to Input", "View Expenses", "Exit"])
        self.remove_menu.format(x=ORIGIN_POS[0],y=ORIGIN_POS[1]+3,
                              layout=Keypad.LAYOUT.HORIZONTAL,
                              padding=2,
                              text_colour=(100, 20, 7))

        self.expenses_list = []

    def __del__(self):
        tGame.end()
        
    def run(self):
        tGame.setTitle("Expense tracker") # Window title

        tGame.screenClear()
        tGame.setCursor(*ORIGIN_POS) # positions start topleft at (1,1)
        tGame.render("Welcome to expense tracker!\n"+"_"*29) # Appends to tGame.render_buffer (str)

        tGame.renderCopy() # sys.stdout.write(tGame.render_buffer)
        # tGame.render_buffer contains anything from tGame.render() (check tGame.py)
        first_entry = True

        while True:
            tGame.hideCursor()

            tGame.moveCursor('B', 2)
            tGame.setCursor(2)
            tGame.render("What would you like to do?")

            ExpensesApp.help_display(35,2)

            self.main_menu.index = 0 # Sets current choice to first option
            self.main_menu.draw() # Draws before the blocking input call

            tGame.renderCopy()

            while True:
                # Clears input prevents accidental choice (from holding button)
                self.key_in.clearPipe()

                # Redraws by default
                action = self.main_menu.update(self.key_in.keyNext()) 

                # Neither Keypad.draw nor Keypad.update call this automatically
                tGame.renderCopy() 

                # CONTROLS.ACTION wasn't pressed, nothing selected
                if not action: 
                    continue
                else:
                    if first_entry: self.main_menu.format(y=ORIGIN_POS[1]+3)
                    break
                    
            # Keypad.update() returns tuple: (choice_index, choice_name)
            # choice_index is used bc it has to be unique, unlike choice_name
            match action[0]: 
                case 0:
                    self.add_expense() # New scene
                case 1:
                    self.remove_menu.index = 0 # Sets to first option in menu
                    self.remove_expense() # New scene
                case 2:
                    tGame.setCursor(ORIGIN_POS[0],12)
                    tGame.renderCopy()

                    self.view_expenses() # Not new scene (yet?) TODO
                    self.key_in.keyNext() # Waits for any input before screenClear() is called
                case 3:
                    return # Quit app
            time.sleep(0.1)
            tGame.screenClear()
            tGame.setCursor(1,1)

    def view_expenses(self):
        tGame.setCursor(ORIGIN_POS[0])
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
        tGame.setCursor(*ORIGIN_POS)
        tGame.showCursor()

        tGame.render("What is your expense for?")

        tGame.setCursor(ORIGIN_POS[0], ORIGIN_POS[1]+1)
        tGame.renderCopy()

        name = tGame.textInput(self.key_in, ORIGIN_POS[0], ORIGIN_POS[1]+1)

        if name == CONTROLS.ESCAPE or name == KEY.QUIT:
            return
        name = name.title().strip()
        while True:
            tGame.setCursor(ORIGIN_POS[0], ORIGIN_POS[1]+3)
            tGame.render("How much is your expense?")
            tGame.setCursor(ORIGIN_POS[0], ORIGIN_POS[1]+4)
            tGame.renderCopy()

            amount = tGame.textInput(self.key_in,
                                     ORIGIN_POS[0], ORIGIN_POS[1]+4)

            if amount == CONTROLS.ESCAPE or name == KEY.QUIT:
                return

            elif amount.isdigit():
                amount = int(amount)
                break
            else:
                tGame.moveCursor('B', 1)
                tGame.render(INVALID_COLOUR+"Invalid Amount"+ Colour.RESET)

                # Reset to original position
                tGame.setCursor(ORIGIN_POS[0])
                tGame.moveCursor('A', 1)
                tGame.render("\033[2K")

                tGame.renderCopy()

        tGame.setCursor(y=ORIGIN_POS[1]+6)
        tGame.renderCopy()
        date = self.input_date()

        expense = {
            "name": name,
            "amt": amount,
            "date": date
        }
        self.expenses_list.append(expense)

    @staticmethod
    def input_date():
        today = time.strftime("%Y %m %d").split()
        print("Leave blank for current date")

        # Year
        while True:
            year = input("  Year: ").strip()
            if year.isdigit():
                year = str(int(year))
                break
            elif len(year) == 0:
                year = str(int(today[0]))
                break

        # Month
        while True:
            month = input("  Month: ").strip()
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
            day = input("  Day: ").strip()
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
        tGame.setCursor(*ORIGIN_POS)
        tGame.showCursor()

        tGame.render(Colour.FOREGROUND["RED"]+"Which one would you like to remove?"+Colour.RESET)

        tGame.setCursor(ORIGIN_POS[0], ORIGIN_POS[1]+3)
        tGame.render(HINT_COLOUR+"(ESCAPE) for options" + Colour.RESET)

        tGame.setCursor(ORIGIN_POS[0], 7)
        tGame.renderCopy()

        self.view_expenses()

        while True:
            tGame.setCursor(ORIGIN_POS[0],ORIGIN_POS[1]+1)
            tGame.render("\033[2K")

            choice = tGame.textInput(self.key_in,
                                     ORIGIN_POS[0], ORIGIN_POS[1]+1)

            if choice == CONTROLS.ESCAPE or choice == KEY.QUIT:
                # Clears options message
                tGame.setCursor(ORIGIN_POS[0],ORIGIN_POS[1]+3)
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
                                tGame.setCursor(ORIGIN_POS[0], 7)
                                tGame.renderCopy()
                                self.view_expenses()
                            case 2: return

            elif choice.strip().isdigit() and int(choice) in range (1,len(self.expenses_list)+1):
                choice = int(choice)
                self.expenses_list.pop(choice-1)

                tGame.screenClear()
                tGame.setCursor(*ORIGIN_POS)
                tGame.render("Your remaining expenses are:")
                tGame.setCursor(ORIGIN_POS[0], ORIGIN_POS[1]+2)
                tGame.renderCopy()
                self.view_expenses()

                tGame.setCursor(ORIGIN_POS[0])
                tGame.render(HINT_COLOUR+"(ANY KEY) to continue\n"+Colour.RESET)
                tGame.renderCopy()
                self.key_in.keyIn()
                break

            else:
                tGame.setCursor(ORIGIN_POS[0], ORIGIN_POS[1]+2)
                tGame.render(INVALID_COLOUR+
                             "Invalid Option" + Colour.RESET)
                tGame.renderCopy()

    def filter_expenses(self):
        pass
    def calculate_expenses(self):
        pass

    @staticmethod
    def help_display(x,y):
        if x<=0 or y<=0:
            raise ValueError(f"x and y must be integers above 0: found x:{x}, y:{y}")
        tGame.setCursor(x=x,y=y)
        tGame.renderCopy()
        tGame.render(tGame.import_image("sprites.txt",10,do_colour=True).replace('\n','\033[1B\033['+str(x)+'G'))
        tGame.renderCopy()

if __name__ =="__main__":
    tGame.init()
    try:
        app = ExpensesApp()
        app.run()
    finally:
        tGame.end()


