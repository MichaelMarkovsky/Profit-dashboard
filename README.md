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

When first running the program, it checks if the SQLite database and Excel files exist. If not, it creates them.

The program uses SQLite to store categories and product information. Each table's title corresponds to a category, and the table's content includes the details of the products within that category (name of the product, time of subscription, price in shop, price bought, and profit).

### Categories and Products

- **Adding a Category**: When you add a category, the program creates a table in SQLite with the name of the category provided by the user.
- **Saving a Product**: When you save a product, it adds a row in the corresponding category table with the product's details (name of the product, time of subscription, price in shop, price bought, profit). The profit is automatically calculated.
- **Adding a Product**: When you add a product using the "Add" button, the program saves the information as a row in the Excel file. Then, it reads the information into the table, automatically sorts it into the analyzing tables, and calculates all the profits.

### Analyzing Tables

The program features two analyzing tables:
1. **Products and Profits**: This table has two columns (products and profits) and lists all products, summing up the profits for each. The table is sorted from the most profitable to the least profitable products.
2. **Categories and Profits**: This table also has two columns (categories and profits) and lists all categories, summing up the profits for each. The table is sorted from the most profitable to the least profitable categories.

These analyzing tables provide a clear overview of which products and categories generate the most profit, helping you make informed decisions.




> REMEMBER: You cant use the program if the excel file is open! (it will not work)


## Installation
#### 1. For Excel:
Download and install a library for interaction with Excel:
```
pip install openpyxl
```

#### 2. For GUI:
Download and install tkinter:
```
pip install tk
```

Download and install a custom version of tkinter(themed):
```
pip install sv-ttk
```

Download and install a PickADate widget for tkinter(themed):
```
pip install tkcalendar
```
#### 3. For EXE (Optional)
I have encounterd an issue with exporting the project as a onefile exe format,
with the the error being not finding the ussage of libraries.
This will resolve the issue:
```
pip install Babel
```
#### Essentials:
- main.py
- read_write.excel.py
- files_creation.py , Creates:
  - products.db
  - ExcelData.xlsx
  

## License
[MIT License](LICENSE)
