import subprocess
import os
from colorama import init ,Fore,Back,Style
import cursor
from sys import platform,stdin
from pynput import keyboard
import re 


def check_os():
    if platform.startswith("win32"): # windows
        global GetWindowText,GetForegroundWindow,msvcrt
        from win32gui import GetWindowText , GetForegroundWindow
        import msvcrt
        return "windows"
    elif platform.startswith("linux"): # linux
        global tcflush,TCIOFLUSH
        from termios import tcflush,TCIOFLUSH
        return "linux"

def Menu(title , items):
    if check_os() == "windows":
        return menu_windows(title, items)
    elif check_os() == "linux":
        return menu_linux(title , items)

class menu_windows:
    def __init__(self ,title, items):
        
        self.platform = "windows"
        self.item_per_menu = 10
        self.window_title = GetWindowText(GetForegroundWindow())
        self.title = title 
        self.items = items.copy()
        self.initItems() # make sure all items of items list have a fix and equal size . after every change in item list we should call this function
        self.current_item = 0
        self.current_item_section = 0
        self.selected_item = None
        self.locked = False
        self.statusbar = ""

        init() # Colorama init()
        listener = keyboard.Listener(on_press=self.on_press_key) # set keyboard listener
        listener.start()

    def show(self):
        self.banner = ""
        os.system("cls")
        cursor.hide()
        self.banner += "\n" #print()
        self.banner += self.title.center(os.get_terminal_size()[0]) + "\n" #print("Title".center(os.get_terminal_size()[0]))
        self.banner += ("-" * 30).center(os.get_terminal_size()[0]) + "\n" #print(("-" * 30).center(os.get_terminal_size()[0]))
        self.banner += "\n" #print()
        
        for item in self.items_sections[self.current_item_section]: # CHANGE FOR SCROLLING PROBLEM
            option = " "*10+"> "+Back.WHITE+Fore.BLACK if self.items.index(item) == self.current_item else " " 
            option += " "
            option += item
            option += ""+Style.RESET_ALL
            option = option.center(os.get_terminal_size()[0]) + "\n"
            self.banner += option
            
            
        if len(self.items) > 5 and self.current_item_section < len(self.items_sections) - 1:
            self.banner += (" "*12 + Back.WHITE + Fore.BLACK + ">>>" + Style.RESET_ALL).center(os.get_terminal_size()[0]) + "\n"
            
        self.banner = "\n"*(os.get_terminal_size()[1]//2 - self.banner.count("\n") // 2) + self.banner
        self.banner += self.statusbar
        print(self.banner)

    
    def on_press_key(self,key):
        if GetWindowText(GetForegroundWindow()) == self.window_title: # if user was on application's window
            try:
                char = key.char
            except:
                name = key.name
                if name == "up":
                    if not self.locked:
                        if self.current_item > 0 :
                            self.current_item -= 1
                            self.current_item_section = self.current_item // self.item_per_menu
                        self.show()
                elif name == "down":
                    if not self.locked:
                        if self.current_item < len(self.items) - 1:
                            self.current_item += 1
                            self.current_item_section = self.current_item // self.item_per_menu
                        self.show()
                elif name == "enter":
                    if not self.locked:
                        self.selected_item = self.current_item
            self.flush_buffer() # flush keyboard input buffer


    def flush_buffer(self):
        while msvcrt.kbhit():
            msvcrt.getch()

    def clear_selected_item(self):
        self.selected_item = None

    def get_selected_item(self):
        item = self.selected_item
        self.clear_selected_item()
        return item

    def updateItem(self , itemIndex , new):
        self.items[itemIndex] = new
        self.initItems(self.current_item_section)
        self.show()

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def reCreate(self ,new_title , new_items): # for clear and reCreate a new menu
        self.title = new_title
        self.items = new_items
        self.current_item = 0
        self.initItems() 
        self.clear_selected_item()
        self.show()
    
    def initItems(self,current_item_section = 0):
        max_length = 0
        for i in self.items:
            i = i.strip(" ")
            if len(i) > max_length:
                max_length = len(i)

        for i in range(len(self.items)):
            self.items[i] = self.items[i].strip(" ")
            self.items[i] += (max_length - len(self.items[i])) * " "
        
        
        self.current_item_section = current_item_section
        self.items_sections = []
        for i in range(0 , len(self.items) , self.item_per_menu):
            self.items_sections.append(self.items[i:i+self.item_per_menu])

        
    def setStatusBar(self,status):
        if len(status) > 0:
            self.statusbar = "\n"
            for line in (status.split("\n")):
                self.statusbar += line.center(os.get_terminal_size()[0])
                self.statusbar += "\n"
            
        else:
            self.statusbar = ""
        
        self.show()


class menu_linux:
    def __init__(self ,title, items):

        self.item_per_menu = 10
        self.platform = "linux"
        self.window_id = self.get_active_window()
        self.title = title 
        self.items = items.copy()
        self.initItems() # make sure all items of items list have a fix and equal size . after every change in item list we should call this function
        self.current_item = 0
        self.current_item_section = 0
        self.selected_item = None
        self.locked = False
        self.statusbar = ""

        init() # Colorama init()
        listener = keyboard.Listener(on_press=self.on_press_key) # set keyboard listener
        listener.start()
  

    def get_active_window(self):
        process = subprocess.Popen(["xprop" , "-root" , "_NET_ACTIVE_WINDOW"] , stdout = subprocess.PIPE)
        stdout = process.communicate()
        stdout = stdout[0].decode().strip("\n")
        window_id = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
        window_id = window_id.group(1)
        return window_id

    def show(self):
        self.banner = ""
        os.system("clear")
        cursor.hide()
        self.banner += "\n" #print()
        self.banner += self.title.center(os.get_terminal_size()[0]) + "\n" #print("Title".center(os.get_terminal_size()[0]))
        self.banner += ("-" * 30).center(os.get_terminal_size()[0]) + "\n" #print(("-" * 30).center(os.get_terminal_size()[0]))
        self.banner += "\n" #print()

        for item in self.items_sections[self.current_item_section]: # CHANGE FOR SCROLLING PROBLEM
            option = " "*10+"> "+Back.WHITE+Fore.BLACK if self.items.index(item) == self.current_item else " " 
            option += " "
            option += item
            option += ""+Style.RESET_ALL
            option = option.center(os.get_terminal_size()[0]) + "\n"
            self.banner += option
            
            
        if len(self.items) > 5 and self.current_item_section < len(self.items_sections) - 1:
            self.banner += (" "*12 + Back.WHITE + Fore.BLACK + ">>>" + Style.RESET_ALL).center(os.get_terminal_size()[0]) + "\n"
            
        self.banner = "\n"*(os.get_terminal_size()[1]//2 - self.banner.count("\n") // 2) + self.banner
        self.banner += self.statusbar
        print(self.banner)

    def on_press_key(self,key):
        if self.get_active_window() == self.window_id: # if user was on application's window
            try:
                char = key.char
            except:
                name = key.name
                if name == "up":
                    if not self.locked:
                        if self.current_item > 0 :
                            self.current_item -= 1
                            self.current_item_section = self.current_item // self.item_per_menu
                        self.show()
                elif name == "down":
                    if not self.locked:
                        if self.current_item < len(self.items) - 1:
                            self.current_item += 1
                            self.current_item_section = self.current_item // self.item_per_menu
                        self.show()
                elif name == "enter":
                    if not self.locked:
                        self.selected_item = self.current_item
            tcflush(stdin , TCIOFLUSH) # flush keyboard input buffer



    def clear_selected_item(self):
        self.selected_item = None

    def get_selected_item(self):
        item = self.selected_item
        self.clear_selected_item()
        return item

    def updateItem(self , itemIndex , new):
        self.items[itemIndex] = new
        self.initItems(self.current_item_section)
        self.show()

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def reCreate(self ,new_title , new_items): # for clear and reCreate a new menu
        self.title = new_title
        self.items = new_items
        self.current_item = 0
        self.initItems() 
        self.clear_selected_item()
        self.show()
    
    def initItems(self,current_item_section = 0):
        max_length = 0
        for i in self.items:
            i = i.strip(" ")
            if len(i) > max_length:
                max_length = len(i)

        for i in range(len(self.items)):
            self.items[i] = self.items[i].strip(" ")
            self.items[i] += (max_length - len(self.items[i])) * " "
        
        
        self.current_item_section = current_item_section
        self.items_sections = []
        for i in range(0 , len(self.items) , self.item_per_menu):
            self.items_sections.append(self.items[i:i+self.item_per_menu])
  
        
    def setStatusBar(self,status):
        if len(status) > 0:
            self.statusbar = "\n"
            for line in (status.split("\n")):
                self.statusbar += line.center(os.get_terminal_size()[0])
                self.statusbar += "\n"
            
        else:
            self.statusbar = ""
        
        self.show()
