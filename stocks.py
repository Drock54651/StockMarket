import customtkinter as ctk
from settings import *

import yfinance as yf
from datetime import datetime


try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = BG_COLOR)
        self.geometry('900x800')
        self.title('')
        self.iconbitmap('empty.ico')
        self.title_bar_color()


        #* DATA
        self.input_string = ctk.StringVar(value = 'AAPL')
        self.time_string = ctk.StringVar(value = TIME_OPTIONS[0])

        #* WIDGETS
        InputPanel(self, self.input_string, self.time_string)

        #* EVENT
        self.bind('<Return>', self.input_handler)

        #* RUN
        self.mainloop()


    def input_handler(self,event = None):
        ticker = yf.Ticker(self.input_string.get()) #! takes name of company stock
        start = datetime(1950,1,1)
        end = datetime.today()
        self.max = ticker.history(start = start, end = end, period = '1d') #! period is how often the stock was checked
        self.year = self.max.iloc[-260:]    #! iloc gets indexed rows using an indexing system so the first row would be index 0
                                            #! gets the last 260 rows aka the whole year minus the weekends

        #TODO: create 6 months, 1 months, one week, all of them to today, exclude weekends
        self.six_months = self.max.iloc[-130:]
        self.one_month = self.max.iloc[-22:]
        self.one_week = self.max.iloc[-5:]
        
        #print(self.max['Close'])
        #print(self.max.columns)



    def title_bar_color(self):

        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(TITLE_HEX_COLOR)), sizeof(c_int))
        except:
            pass


class InputPanel(ctk.CTkFrame):
    def __init__(self, parent, input_string, time_string):
        super().__init__(parent, fg_color = INPUT_BG_COLOR, corner_radius = 0)
        self.pack(fill = 'both', side = 'bottom')

        #* WIDGETS  
        ctk.CTkEntry(self, textvariable = input_string, fg_color = BG_COLOR, border_color = TEXT_COLOR, border_width = 1).pack(side = 'left', padx = 10, pady = 10)

        #TODO: create one textbutton for evey string inside of Time_Options
        self.buttons = [TextButton(self, text, time_string) for text in TIME_OPTIONS] #! here text and time_string both refer to the stuff in TIME_OPTIONS

        time_string.trace('w', self.unselect_all_buttons)

    def unselect_all_buttons(self, *args):
        for button in self.buttons:
            button.unselect()


class TextButton(ctk.CTkLabel):
    def __init__(self, parent, text, time_string):
        super().__init__(parent, text = text, text_color = TEXT_COLOR)
        self.pack(side = 'right', padx = 10, pady = 10)
        self.time_string = time_string
        self.text = text
        #TODO: turn the label into a button
        self.bind('<Button>', self.select_handler)

        if time_string.get() == text: #! time_string is defaulted to "Max", since max is the first item in the settings, this would match in the first button created in the loop in line 47
            self.select_handler()

    def select_handler(self, event = None): #! clicking on label turns it blue
        self.time_string.set(self.text) #! Triggers trace and the unselect method, after all that, then does the config below
        self.configure(text_color = HIGHLIGHT_COLOR)

    def unselect(self):
        self.configure(text_color = TEXT_COLOR)

App()