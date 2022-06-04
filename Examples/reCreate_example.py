import climenu
import time

title1 = "Title of menu 1"
title2 = "Title of menu 2"
items1 = ["goto menu 2" , "alaki" , "About" , "Exit"]
items2 = ["first item" , "second item" , "back"]
menu = climenu.Menu(title = title1 , items = items1)
menu.show() # show the menu

while True: # our program main loop
    time.sleep(1) # this is important !!
    selected = menu.get_selected_item() 
    if selected == 0: # (goto menu 2) item
        menu.reCreate(title2 , items2)


