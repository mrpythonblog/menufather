import mmenu
import time

title = "Title of menu"
items = []
for i in range(1,101):
    items.append("Item {}".format(i))

menu = mmenu.Menu(title = title , items = items)
menu.show() # show the menu

while True: # our program main loop
    time.sleep(1) # this is important !!
    selected = menu.get_selected_item() 
    if selected != None : 
        break

print("selected item : {}".format(items[selected]))

