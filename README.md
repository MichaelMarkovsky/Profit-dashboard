# Profit Dashboard
>A program in which you save the details of your products with their categories, add them to the table in which it saves to an excel , and in real time see your total profit and analize what product and category makes you the most money.

![pic1 copy](https://github.com/MichaelMarkovsky/Profit-dashboard/assets/133515749/0b878502-d6af-4c35-a8e0-b6608bfd3f41)



## Fetures
- Easy to use
- Saving your products to a category
- Saving your product's information and adding them faster
- Sorting the sales you have added by dates
- A label for total sales 
- Analazing:
  - Main table for all the sales
  - 2 tables for analazing what gets the most sales


## Overview
When first runing the program , it checks if the sqlite(database) and excel files exist, if not then it creates them.
It uses the sqlite for saving the categories and product information (the title of the table is the cartegory and the content is the products and their details:name of the product,time of subscription,price in shop,price of bought,profit)

when you add a categoty, it creates a in the sqlite a table name with the category's name that the user provided.

When you save a product, it adds a row in the table with the product's details (name of the product,time of subscription,price in shop,price of bought,profit) , but the profit in this window is calculated automaticly.

When you add a product to the with the add button , it saves the information as a row in the 



> REMEMBER: You cant use the program if the excel file is open! (it will not work)


## Installation
#### 1. For webscraping:
Download and install a specific selenuim version:
```
pip install selenium==4.9.0
```
Download and extract *chromedriver-win64* and *chrome-win64* to the script's folder:
https://googlechromelabs.github.io/chrome-for-testing/

#### 2. For GUI:
Download and install tkinter:
```
pip install tk
```

Download and install a custom version of tkinter(themed):
```
pip install sv-ttk
```
#### Essentials:
- main.py
- read_write.excel.py
- files_creation.py

## License
[MIT License](LICENSE)
