# menufather Ver 1.0
**menufather** is a simple and lightweight python library for creating console-based menus (windows / linux) . 

# INSTALLATION
it can installed using **pip** :
**Linux** : ```python3 -m pip install menufather```
or **Windows** : ``` pip install menufather```


# Creating the first menu !
![creating the first menu](https://github.com/mrpythonblog/menufather/raw/main/Pictures/source1.png)

at first we declare our menu items in the "items" list as strings . 
then we create a menu using ```menufather.Menu(title , items)``` function . after that , we can show our menu using ```menu.show()``` method. 
* we should make a loop in our program .
* in our while loop we should use a **sleep** (ex : 0.5s sleep)


```menu.get_selected_item()``` can be used for getting the selected item by user . it returns the index of selected item in "items" list if user has selected an item else it returns **None** 
once we get selected item by this function , the next round this function returns **None** until user selects another item so we should save the result of this function in a variable at the first of loop (```selected``` variable) .

Result : 
![result 1](https://github.com/mrpythonblog/menufather/raw/main/Pictures/result1.png)

# Locking and Unlocking Menu
the two methods ```menu.lock()``` and ```menu.unlock()``` , can lock or unlock the menu . when menu is locked , user can't navigate or select anything on it .

# Updating menu items
we can update an item in the menu using ```menu.updateItem(itemIndex , new)``` . ```itemIndex``` is the index of item in the "items" list that we want to update and ```new``` is the string value we want to replace .

example : ```menu.updateItem(2 , "Contact")```  . this changes item index 2 in the menu to "Contact" .

# ReCreating the menu
sometimes we want to have some items that can create a new menu when user selects that . ```menu.reCreate(new_title , new_items)``` can do this . ```new_title``` is the title of the new menu and ```new_items``` is a list that contains the items of new menu . 

example : 
![reCreate menu example](https://github.com/mrpythonblog/menufather/raw/main/Pictures/source2.png)

after running this source , if we select "goto menu 2" item , a new menu appears (menu 2) ...


# Auto Scrolling  
if your items are too many , don't worry ! menufather simulate a scrolling state for items !




‍




