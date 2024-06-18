#IMPORTS FOR UI
#solves the issue of the UI being blurry
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
import tkinter
from tkinter import ttk#sub module to use themed widgests
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox 

from tkcalendar import Calendar, DateEntry

import sv_ttk

#IMPORTS FOR EXTERNAL FUNCTIONS
#create excel file:
import files_creation
#read the excel file:
import read_write_excel

#IMPORT FOR DATABASE
import sqlite3

#provides localization and internationalization utilities for Python (solved an issue while trying to convert the python file to exe)
import babel.numbers


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #setup
        #self.create_download_folder_if_not_exists()
        sv_ttk.use_dark_theme()

        self.title("Dashboard")
        self.resizable(0,0)#Don't allow the screen to be resized
        #self.iconbitmap("Icon.ico")#replace the defult icon with a Transparent Icon

        #widgets
        self.widgets = Widgets(self)

        #run
        self.mainloop()#the loop of the application



class Widgets (ttk.Frame):
    def __init__(self,parent):#inherants the window
        super().__init__(parent)
        self.pack()


        #Create excel if it doesnt exist within the code's folder:
        files_creation.create_excel()
        files_creation.create_database() #creates it if it doesnt exist

        self.combo_list =[]
        self.combo_list_categories =[]

        self.interface()
        self.database_to_combo()
        self.database_to_combo_category()
        self.table()
        self.tables()




    def interface(self):
        main_interface_frame = ttk.LabelFrame(self,text="Main Interface")
        main_interface_frame.grid(row=0, column=0,padx=20,pady=10)

        

        interface_frame_section_1 = ttk.LabelFrame(main_interface_frame,text="Products")
        interface_frame_section_1.grid(row=0, column=0,padx=20,pady=10)        

        
        
        #Solution for the comboboxes changing with the same value:
        #when you change selection in one Combobox then it changes value in StringVar which automatically changes selection in all Combobox which use the same ID.
        self.a1 = tk.StringVar(self)
        self.a2 = tk.StringVar(self)


        self.combo1 = ttk.Combobox(interface_frame_section_1, text="Name of Product",state="readonly", values=self.combo_list , textvariable=self.a1)
        self.combo1.grid(row=1,column=1,padx=10,pady=7, sticky="ew")
        self.combo1.bind('<<ComboboxSelected>>', self.combo_selected)

        self.combo1_category = ttk.Combobox(interface_frame_section_1, text="Name of Product", state="readonly", values="" , textvariable=self.a2)
        self.combo1_category.grid(row=0,column=1,padx=10,pady=7, sticky="ew")
        self.combo1_category.bind('<<ComboboxSelected>>', self.database_to_combo_category_selected)
        
        
        def section_1_interface():
            #==================THE INFORMATION OF THE PRODUCTS INTERFACE===========================
            def labels():
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Category:', font=('calibre',9))
                self.name_label.grid(row=0,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Type:', font=('calibre',9))
                self.name_label.grid(row=1,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Date:', font=('calibre',9))
                self.name_label.grid(row=2,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Time of subscription:', font=('calibre',9))
                self.name_label.grid(row=3,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price in shop:', font=('calibre',9))
                self.name_label.grid(row=4,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price of bought:', font=('calibre',9))
                self.name_label.grid(row=5,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Profit:', font=('calibre',9))
                self.name_label.grid(row=6,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Times:', font=('calibre',9))
                self.name_label.grid(row=7,column=0,padx=10,pady=7, sticky="ew")

                
                
                
                

            labels()

            def Entries():
                self.entry_widget_date = DateEntry(interface_frame_section_1,date_pattern='dd/mm/y',state='readonly')
                self.entry_widget_date.grid(row=2,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_ts = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
                self.entry_widget_ts.grid(row=3,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_pis = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
                self.entry_widget_pis.grid(row=4,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_pob = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
                self.entry_widget_pob.grid(row=5,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_p = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9),foreground="green")
                self.entry_widget_p.grid(row=6,column=1,padx=10,pady=7, sticky="ew")

                self.entry_widget_times = ttk.Entry(interface_frame_section_1, width=1, justify="center", font=('Arial', 9),foreground="pink")
                self.entry_widget_times.grid(row=7,column=1,padx=70,pady=7, sticky="ew")
                
                self.entry_widget_times.insert(0, "1") #This is the default text

            Entries()

            def Buttons():
                self.text_widget = ttk.Button(interface_frame_section_1, text="Add",command=self.add_product_excel)
                self.text_widget.grid(row=8,column=1,padx=10,pady=10, sticky="ew")
                self.text_widget = ttk.Button(interface_frame_section_1, text="Save Edit",command=self.save_product_edit)
                self.text_widget.grid(row=8,column=0,padx=10,pady=10, sticky="ew")

                self.button_widget_dsc = ttk.Button(interface_frame_section_1, text="Delete Selected Category",command=self.delete_category_table, width=20)
                self.button_widget_dsc.grid(row=9,column=0,padx=10,pady=10, sticky="ew")
                self.button_widget_dsp = ttk.Button(interface_frame_section_1, text="Delete Selected Product",command=self.delete_product, width=10)
                self.button_widget_dsp.grid(row=9,column=1,padx=10,pady=10, sticky="ew")

            Buttons()

        section_1_interface()


        interface_frame_section_2 = ttk.LabelFrame(main_interface_frame,text="Settings")
        interface_frame_section_2.grid(row=1, column=0,padx=20,pady=10)

        self.text_widget = ttk.Button(interface_frame_section_2, text="Add Product",command=self.open_secondary_window)
        self.text_widget.grid(row=0,column=0,padx=20,pady=7, sticky="ew")

        self.text_widget_addCategory = ttk.Button(interface_frame_section_2, text="Add Category",command=self.open_secondary_window_ac)
        self.text_widget_addCategory.grid(row=0,column=1,padx=20,pady=7, sticky="ew")
    


    def add_product_excel(self):

        #error for not choosing the product:
        if(self.combo1.get()==''):
            messagebox.showerror("showerror", "Nothing to add") 
            return

        times = self.entry_widget_times.get()

        #error for if the times value is not a number
        try:
            int(times)
        except:
            messagebox.showerror("showerror", "Invalid Entry: Times,type") 
            return

        if(int(times)>0 and int(times)<=100):
            for x in range(int(times)):
                read_write_excel.add_product_row(self.combo1.get(),self.combo1_category.get(),self.entry_widget_date.get(),self.entry_widget_ts.get(),self.entry_widget_pis.get(),self.entry_widget_pob.get(),self.entry_widget_p.get())
                self.update_table()
                self.update_tables()

            messagebox.showinfo("showinfo", "You have added the Product\s!") 
        else:
            messagebox.showerror("showerror", "Invalid Entry: Times,range") 

    def open_secondary_window_ac(self):
        # Create secondary (or popup) window.
        secondary_window = tk.Toplevel()
        secondary_window.title("Add Category")

        interface_frame_section_1 = ttk.LabelFrame(secondary_window,text="Products")
        interface_frame_section_1.grid(row=0, column=0,padx=20,pady=10)


        def labels():
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Name of Category:', font=('calibre',9))
                self.name_label.grid(row=0,column=0,padx=10,pady=7, sticky="ew")


        labels()

        def Entries():
            self.entry_widget_category = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_category.grid(row=0,column=1,padx=10,pady=7, sticky="ew")

        Entries()

        def Buttons():
            self.button_add_item_database = ttk.Button(interface_frame_section_1, text="Add",command=self.add_category)
            self.button_add_item_database.grid(row=5,column=0,padx=20,pady=10, sticky="ew")


        Buttons()


    def add_category(self):
        #Check for errors:
        #if the entries are empty:
        if(self.entry_widget_category.get()==""):
            messagebox.showinfo("showerror", "Your category entry is empty") 
            return

        try:
           # Get the category from the entry widget
            category = self.entry_widget_category.get()

            # Create the SQL query with the category
            sql_query = f"""
            CREATE TABLE IF NOT EXISTS {category} (
                name TEXT PRIMARY KEY,
                timesubscription TEXT NOT NULL,
                priceinshop TEXT NOT NULL,
                priceofbought TEXT NOT NULL,
                profit TEXT NOT NULL
            );
            """

            # Define the database file name
            db_name = 'products.db'

            # Create a new database connection
            conn = sqlite3.connect(db_name)
            
            #create table
            conn.execute(sql_query)
            # Commit the changes
            conn.commit()

            # Close the connection
            conn.close()

            self.database_to_combo_category()
            
            messagebox.showinfo("showinfo", "You have added a category!") 

        except:
            messagebox.showerror("showerror", "Error") 


    def open_secondary_window(self):
        # Create secondary (or popup) window.
        secondary_window = tk.Toplevel()
        secondary_window.title("Add item")

        interface_frame_section_1 = ttk.LabelFrame(secondary_window,text="Products")
        interface_frame_section_1.grid(row=0, column=0,padx=20,pady=10)


        self.combo1_category_s = ttk.Combobox(interface_frame_section_1, text="Name of Product", state="readonly", values=self.combo_list_categories)
        self.combo1_category_s.grid(row=0,column=1,padx=10,pady=7, sticky="ew")

        def labels():
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Category:', font=('calibre',9))
                self.name_label.grid(row=0,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Name of Product:', font=('calibre',9))
                self.name_label.grid(row=1,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Time of subscription:', font=('calibre',9))
                self.name_label.grid(row=2,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price in shop:', font=('calibre',9))
                self.name_label.grid(row=3,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price of bought:', font=('calibre',9))
                self.name_label.grid(row=4,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Profit:', font=('calibre',9))
                self.name_label.grid(row=5,column=0,padx=10,pady=7, sticky="ew")

        labels()

        def Entries():
            self.entry_widget_type = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_type.grid(row=1,column=1,padx=10,pady=7, sticky="ew")
            self.entry_text_widget_Timeofsubscription = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_text_widget_Timeofsubscription.grid(row=2,column=1,padx=10,pady=7, sticky="ew")
            self.entry_widget_Priceinshop = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_Priceinshop.grid(row=3,column=1,padx=10,pady=7, sticky="ew")
            self.entry_widget_Priceofbought = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_Priceofbought.grid(row=4,column=1,padx=10,pady=7, sticky="ew")

        Entries()

        def Buttons():
            self.button_add_item_database = ttk.Button(interface_frame_section_1, text="Add",command=self.add_item)
            self.button_add_item_database.grid(row=6,column=0,padx=20,pady=10, sticky="ew")


        Buttons()

    def add_item(self):
        #Check for errors:
        #if the entries are empty:
        if(self.entry_widget_Priceinshop.get()==""):
            messagebox.showinfo("showerror", "Your Price In Shop entry is empty") 
            return
        if(self.entry_widget_Priceofbought.get()==""):
            messagebox.showinfo("showerror", "Your Price Of Bought entry is empty") 
            return
        
        #if you didnt choose the category:
        if(self.combo1_category_s.get()==""):
            messagebox.showinfo("showerror", "You did not choose the category") 
            return
        
        #if the prices are numbers
        try:
            float(self.entry_widget_Priceinshop.get())
        except:
            messagebox.showinfo("showerror", "Your Price In Shop entry is not a number")
            return
        
        try:
            float(self.entry_widget_Priceofbought.get())
        except:
            messagebox.showinfo("showerror", "Your Price Of Bought entry is not a number")
            return
        
        



        try:
            # Connect to the database
            conn = sqlite3.connect('products.db')

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()


            profit = round(float(self.entry_widget_Priceinshop.get()) - float(self.entry_widget_Priceofbought.get()),3)

            values = (self.entry_widget_type.get(), self.entry_text_widget_Timeofsubscription.get(), self.entry_widget_Priceinshop.get(), self.entry_widget_Priceofbought.get(),str(profit))

            table_name = self.combo1_category_s.get()

            query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?)"

            # Execute the query with the correct parameters
            cursor.execute(query, values)
            
            # Commit your changes in the database     
            conn.commit() 
            
            # Closing the connection 
            conn.close()

            self.database_to_combo()
            
            messagebox.showinfo("showinfo", "You have added a product!") 

        except:
            messagebox.showerror("showerror", "That product already exists") 

    def on_scroll_3(self,*args):#will be called whenever the scrollbar is manipulated.    It calls the yview method of the table widget with the provided arguments, allowing the text widget to scroll vertically.
        self.table_3.yview(*args)

    def on_scroll_2(self,*args):#will be called whenever the scrollbar is manipulated.    It calls the yview method of the table widget with the provided arguments, allowing the text widget to scroll vertically.
        self.table_2.yview(*args)

    def on_scroll(self,*args):#will be called whenever the scrollbar is manipulated.    It calls the yview method of the table widget with the provided arguments, allowing the text widget to scroll vertically.
        self.table.yview(*args)

    def tables(self):
        main_interface_frame_3 = ttk.LabelFrame(self,text="Analysis")
        main_interface_frame_3.grid(row=0, column=2,padx=20,pady=10)

        interface_frame_section_3 = ttk.LabelFrame(main_interface_frame_3,text="Total profit")
        interface_frame_section_3.grid(row=0, column=0,padx=20,pady=10)

        def table_2():#category
            Tableframe = ttk.Frame(interface_frame_section_3)
            Tableframe.grid(row=0, column=2,padx=10,pady=10)

            tablescroll = ttk.Scrollbar(Tableframe,command=self.on_scroll_2)
            tablescroll.pack(side="right",fill="y")

            cols = ("Category","Profit")
            self.table_2 = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=5)
            
            self.table_2.column("Category",width=150,anchor=tk.CENTER)#anchor=tk.CENTER == text is centered within the cells
            self.table_2.column("Profit",width=120,anchor=tk.CENTER)

            # define headings
            self.table_2.heading('Category', text='Category')
            self.table_2.heading('Profit', text='Profit')
            self.table_2.pack()


        table_2()

        def table_3():#products
            Tableframe = ttk.Frame(interface_frame_section_3)
            Tableframe.grid(row=1, column=2,padx=10,pady=10)

            tablescroll = ttk.Scrollbar(Tableframe,command=self.on_scroll_3)
            tablescroll.pack(side="right",fill="y")

            cols = ("Products","Profit")
            self.table_3 = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=5)
            
            self.table_3.column("Products",width=150,anchor=tk.CENTER)#anchor=tk.CENTER == text is centered within the cells
            self.table_3.column("Profit",width=120,anchor=tk.CENTER)

            # define headings
            self.table_3.heading('Products', text='Products')
            self.table_3.heading('Profit', text='Profit')
            self.table_3.pack()


        table_3()

        self.total_profit_label_2 = ttk.Label(main_interface_frame_3, text = 'Total Profit:', font=('calibre',12))
        self.total_profit_label_2.grid(row=1,column=0,padx=120,pady=7, sticky="ew")

        self.total_profit_label = ttk.Label(main_interface_frame_3, text = '', font=('calibre',11),foreground="green")
        self.total_profit_label.grid(row=2,column=0,padx=150,pady=7, sticky="ew")


        self.update_table()
        self.update_tables()


        

    def update_tables(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_tables()

        

        def update_table_products():
            #Insert the data from the excel to the table:
            #get the length of the products list
            products_dic = read_write_excel.get_all_products()
            products_length = len(products_dic['Products'])

            # New dictionary to store summed profits
            summed_profits = {}

            # Iterate over the length of the product list
            for i in range(len(products_dic['Products'])):
                product = products_dic['Products'][i]
                profit = products_dic['Profit'][i]
                
                if product in summed_profits:
                    summed_profits[product] += profit
                else:
                    summed_profits[product] = profit



            # SORT IT:
            def sort_profits(summed_profits):
                # Combine products with their corresponding profits into a list of tuples
                product_profit_list = list(summed_profits.items())

                # Sort the list by profit in descending order
                sorted_product_profit_list = sorted(product_profit_list, key=lambda x: x[1], reverse=True)

                return sorted_product_profit_list

                
            # Get the sorted product-profit list
            sorted_product_profit_list = sort_profits(summed_profits)

            # Insert the summed profits into the treeview
            for product, profit in sorted_product_profit_list:
                self.table_3.insert('', tk.END, values=(product, str(round((profit),3))))

        update_table_products()

        def update_table_category():
            #Insert the data from the excel to the table:
            #get the length of the products list
            products_dic = read_write_excel.get_all_products()
            products_length = len(products_dic['Category'])

            # New dictionary to store summed profits
            summed_profits = {}

            # Iterate over the length of the product list
            for i in range(len(products_dic['Category'])):
                product = products_dic['Category'][i]
                profit = products_dic['Profit'][i]
                
                if product in summed_profits:
                    summed_profits[product] += profit
                else:
                    summed_profits[product] = profit


            # SORT IT:
            def sort_profits(summed_profits):
                # Combine products with their corresponding profits into a list of tuples
                product_profit_list = list(summed_profits.items())

                # Sort the list by profit in descending order
                sorted_product_profit_list = sorted(product_profit_list, key=lambda x: x[1], reverse=True)

                return sorted_product_profit_list


             # Get the sorted product-profit list
            sorted_product_profit_list = sort_profits(summed_profits)

            # Insert the summed profits into the treeview
            for product, profit in sorted_product_profit_list:
                self.table_2.insert('', tk.END, values=(product, str(round((profit),3))))

        update_table_category()



    def clear_tables(self):
        self.table_2.delete(*self.table_2.get_children())
        self.table_3.delete(*self.table_3.get_children())


       
    def table(self):
        Tableframe = ttk.Frame(self)
        Tableframe.grid(row=0, column=1,padx=0,pady=10)

        tablescroll = ttk.Scrollbar(Tableframe,command=self.on_scroll)
        tablescroll.pack(side="right",fill="y")

        cols = ("Products","Category","Date","Time of subscription","Price in shop","Price of bought","Profit")
        self.table = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=20)
        
        self.table.column("Products",width=150,anchor=tk.CENTER)#anchor=tk.CENTER == text is centered within the cells
        self.table.column("Category",width=100,anchor=tk.CENTER)
        self.table.column("Date",width=100,anchor=tk.CENTER)
        self.table.column("Time of subscription",width=200,anchor=tk.CENTER)
        self.table.column("Price in shop",width=120,anchor=tk.CENTER)
        self.table.column("Price of bought",width=120,anchor=tk.CENTER)
        self.table.column("Profit",width=120,anchor=tk.CENTER)

        # define headings
        self.table.heading('Products', text='Products',command=lambda : self.sort_treeview(self.table, "Products", False))
        self.table.heading('Category', text='Category',command=lambda : self.sort_treeview(self.table, "Category", False))
        self.table.heading('Date', text='Date',command=lambda : self.sort_treeview(self.table, "Date", False))
        self.table.heading('Time of subscription', text='Time of subscription',command=lambda : self.sort_treeview(self.table, "Time of subscription", False))
        self.table.heading('Price in shop', text='Price in shop')
        self.table.heading('Price of bought', text='Price of bought')
        self.table.heading('Profit', text='Profit')
        self.table.pack()


        
    # Function to sort the Treeview by column
    def sort_treeview(self,tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not descending))



    def clear_table(self):
        self.table.delete(*self.table.get_children())


    def update_table(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()

        #Insert the data from the excel to the table:

        #get the length of the products list
        products_dic = read_write_excel.get_all_products()
        products_length = len(products_dic['Products'])


        for i in range(products_length):
            self.table.insert('', tk.END, values=(
                products_dic['Products'][i],
                products_dic['Category'][i],
                products_dic['Date'][i],
                products_dic['Time of subscription'][i],
                products_dic['Price in shop'][i],
                products_dic['Price of bought'][i],
                products_dic['Profit'][i]
            ))

        self.calc_total_profit()

    def calc_total_profit(self):
        total = 0
        for item in self.table.get_children():
            value = self.table.set(item, 6)
            if value is not None:
                try:
                    total += float(value)
                except ValueError:
                    print(f"Warning: Could not convert value '{value}' to float.")
        self.total_profit_label.config(text = str(round((total),3)))

        
    def save_product_edit(self):
        #1.error check if a product was selected
        #2.save the information to the database where the name the category is selected, where the name is the selected product

        if(self.combo1.get()!=""):
            # Connect to the SQLite database
            conn = sqlite3.connect('products.db')

            # Create a cursor object to interact with the database
            cursor = conn.cursor()

            # Table and column names
            table_name = self.combo1_category.get()
            name_product = self.combo1.get()  # The value to find the row to update

            # Construct the SQL query to update the row
            sql_update_query = f'''
            UPDATE {table_name}
            SET timesubscription = ?, priceinshop = ?, priceofbought = ?, profit = ?
            WHERE name = ?
            '''

            # Execute the query with the specified values
            cursor.execute(sql_update_query, (self.entry_widget_ts.get(),self.entry_widget_pis.get(), self.entry_widget_pob.get(),self.entry_widget_p.get(),name_product))

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and the connection
            cursor.close()
            conn.close()
            messagebox.showinfo("showinfo", "You have saved a product!") 
    
        else:
            messagebox.showinfo("showerror", "You did not choose a product")

    

    def delete_product(self):
        if(self.combo1.get()!=""):
            # Connect to the SQLite database
            conn = sqlite3.connect('products.db')

            # Create a cursor object to interact with the database
            cursor = conn.cursor()

            # Table and column names
            table_name = self.combo1_category.get()
            name_product = self.combo1.get()  # The value to find the row to update

           # Construct the SQL query to delete the row
            sql_delete_query = f'''
            DELETE FROM {table_name}
            WHERE name = ?
            '''

            # Execute the query with the specified values
            cursor.execute(sql_delete_query, (name_product,))

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and the connection
            cursor.close()
            conn.close()

             #clear the previous text first
            self.entry_widget_ts.delete(0, tk.END)
            self.entry_widget_pis.delete(0, tk.END)
            self.entry_widget_pob.delete(0, tk.END)
            self.entry_widget_p.delete(0, tk.END)

            def delete_selected_value():
                # Get the current selection
                selected_value = self.combo1.get()
                # Get the current list of values
                values = list(self.combo1['values'])
                # Remove the selected value from the list
                if selected_value in values:
                    values.remove(selected_value)
                # Update the combobox with the new list of values
                self.combo1['values'] = values
                # Clear the current selection in the combobox
                self.combo1.set('')

            delete_selected_value()

            messagebox.showinfo("showinfo", "You have deleted a product!") 

        else:
            messagebox.showinfo("showerror", "You did not choose a product")
    

    def delete_category_table(self):
        try:
            msg_box = tk.messagebox.askquestion(
                "Delete action",
                "Are you sure you want to delete the category?",
                icon="warning",
            )
            if msg_box == "yes":
               
                
                # Connect to the database
                conn = sqlite3.connect('products.db')
                cursor = conn.cursor()

                # Execute the DROP TABLE command
                cursor.execute(f'DROP TABLE IF EXISTS {self.combo1_category.get()}')
                conn.commit()

            

                #clear the previous text first
                self.entry_widget_ts.delete(0, tk.END)
                self.entry_widget_pis.delete(0, tk.END)
                self.entry_widget_pob.delete(0, tk.END)
                self.entry_widget_p.delete(0, tk.END)

                self.combo1['values'] = []
                self.combo1.set('')

                def delete_selected_value():
                    # Get the current selection
                    selected_value = self.combo1_category.get()
                    # Get the current list of values
                    values = list(self.combo1_category['values'])
                    # Remove the selected value from the list
                    if selected_value in values:
                        values.remove(selected_value)
                    # Update the combobox with the new list of values
                    self.combo1_category['values'] = values
                    # Clear the current selection in the combobox
                    self.combo1_category.set('')

                

                messagebox.showinfo("showinfo", f"Category '{self.combo1_category.get()}' was deleted successfully.")

                delete_selected_value()

        except:
            messagebox.showinfo("showerror", "You did not choose a category")

    def database_to_combo(self):
        try:
            self.combo_list.clear()

            # Connecting to sqlite 
            conn = sqlite3.connect('products.db') 
            
            # Creating a cursor object using the cursor() method 
            cursor = conn.cursor() 

            #Get all products from all tables
            data=cursor.execute("SELECT * FROM (?);",str(self.combo1.get()))
            for row in data:
                self.combo_list.append(row[0])
        except:
            pass

        self.combo1['values'] = self.combo_list


    


    def database_to_combo_category(self):
        #clear values, then add the new values(update)
        self.combo_list.clear()
        self.combo_list_categories.clear()

        self.combo1_category['values'] = []

        # Connecting to sqlite 
        conn = sqlite3.connect('products.db') 
        
        # Creating a cursor object using the cursor() method 
        cursor = conn.cursor() 

        # Retrieve the list of all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            self.combo_list_categories.append(table[0])

        
        self.combo1_category['values'] = self.combo_list_categories
  

    def database_to_combo_category_selected(self,event):
        try:
            self.combo_list.clear()

            # Connecting to sqlite 
            conn = sqlite3.connect('products.db') 
            
            # Creating a cursor object using the cursor() method 
            cursor = conn.cursor() 

            # Get all products from all tables
            table_name = self.combo1_category.get()
            query = f"SELECT * FROM {table_name};"

            # Execute the query
            cursor.execute(query)

            # Fetch all rows
            rows = cursor.fetchall()

            # Process the rows
            for row in rows:
                self.combo_list.append(row[0])

            #clear the previous text first
            self.entry_widget_ts.delete(0, tk.END)
            self.entry_widget_pis.delete(0, tk.END)
            self.entry_widget_pob.delete(0, tk.END)
            self.entry_widget_p.delete(0, tk.END)

            self.combo1.set('')
        except:
            print('Error')

        #clear the previous text first
        self.combo1['values'] = []  # Clear the list of values

        self.combo1['values'] = self.combo_list

    def combo_selected(self,event):
      # Connecting to sqlite 
        conn = sqlite3.connect('products.db') 
        
        # Creating a cursor object using the cursor() method 
        cursor = conn.cursor() 

        table_name = self.combo1_category.get()
        name = self.combo1.get()

        # Construct the SQL query with the correct table name
        query = f"SELECT * FROM {table_name} WHERE name=?"
        
        # Execute the query with the correct parameter binding
        cursor.execute(query, (name,))

        # Fetch the results
        data = cursor.fetchall()

        #clear the previous text first
        self.entry_widget_ts.delete(0, tk.END)
        self.entry_widget_pis.delete(0, tk.END)
        self.entry_widget_pob.delete(0, tk.END)
        self.entry_widget_p.delete(0, tk.END)

        #insert the new text
        self.entry_widget_ts.insert(0,data[0][1])
        self.entry_widget_pis.insert(0,data[0][2])
        self.entry_widget_pob.insert(0,data[0][3])
        self.entry_widget_p.insert(0,data[0][4])

App()#run
