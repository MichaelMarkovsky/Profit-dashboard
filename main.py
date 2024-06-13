#IMPORTS FOR UI
#solves the issue of the UI being blurry
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
import tkinter
from tkinter import ttk#sub module to use themed widgests
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox 

import sv_ttk
import threading
from threading import Event


#IMPORTS FOR EXTERNAL FUNCTIONS
#create excel file:
import files_creation
#read the excel file:
import read_excel

#IMPORT FOR DATABASE
import sqlite3


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #setup
        #self.create_download_folder_if_not_exists()
        sv_ttk.use_dark_theme()
        self.title("Dashboard")
        #self.resizable(0,0)#Don't allow the screen to be resized
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

        self.interface()
        self.database_to_combo()
        self.table()




    def interface(self):
        main_interface_frame = ttk.LabelFrame(self,text="Main Interface")
        main_interface_frame.grid(row=0, column=0,padx=20,pady=10)

        interface_frame_section_1 = ttk.LabelFrame(main_interface_frame,text="Products")
        interface_frame_section_1.grid(row=0, column=0,padx=20,pady=10)        
        

        self.combo1 = ttk.Combobox(interface_frame_section_1, text="Name of Product", state="readonly", values=self.combo_list)
        self.combo1.grid(row=0,column=1,padx=10,pady=7, sticky="ew")
        self.combo1.bind('<<ComboboxSelected>>', self.combo_selected)
        
        def section_1_interface():
            #==================THE INFORMATION OF THE PRODUCTS INTERFACE===========================
            def labels():
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Type:', font=('calibre',9))
                self.name_label.grid(row=0,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Time of subscription:', font=('calibre',9))
                self.name_label.grid(row=1,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price in shop:', font=('calibre',9))
                self.name_label.grid(row=2,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price of bought:', font=('calibre',9))
                self.name_label.grid(row=3,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Profit:', font=('calibre',9))
                self.name_label.grid(row=4,column=0,padx=10,pady=7, sticky="ew")

            labels()

            def Entries():
                self.entry_widget_ts = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
                self.entry_widget_ts.grid(row=1,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_pis = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
                self.entry_widget_pis.grid(row=2,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_pob = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
                self.entry_widget_pob.grid(row=3,column=1,padx=10,pady=7, sticky="ew")
                self.entry_widget_p = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9),foreground="green")
                self.entry_widget_p.grid(row=4,column=1,padx=10,pady=7, sticky="ew")

            Entries()

            def Buttons():
                self.text_widget = ttk.Button(interface_frame_section_1, text="Add",command="")
                self.text_widget.grid(row=5,column=0,padx=20,pady=10, sticky="ew")
                self.text_widget = ttk.Button(interface_frame_section_1, text="Save Edit",command="")
                self.text_widget.grid(row=5,column=1,padx=20,pady=10, sticky="ew")

            Buttons()

        section_1_interface()

        interface_frame_section_2 = ttk.LabelFrame(main_interface_frame,text="Settings")
        interface_frame_section_2.grid(row=1, column=0,padx=20,pady=10)

        self.text_widget = ttk.Button(interface_frame_section_2, text="Add Product",command=self.open_secondary_window)
        self.text_widget.grid(row=0,column=0,padx=20,pady=7, sticky="ew")


    def open_secondary_window(self):
        # Create secondary (or popup) window.
        secondary_window = tk.Toplevel()
        secondary_window.title("Add item")

        interface_frame_section_1 = ttk.LabelFrame(secondary_window,text="Products")
        interface_frame_section_1.grid(row=0, column=0,padx=20,pady=10)

        def labels():
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Type:', font=('calibre',9))
                self.name_label.grid(row=0,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Time of subscription:', font=('calibre',9))
                self.name_label.grid(row=1,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price in shop:', font=('calibre',9))
                self.name_label.grid(row=2,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Price of bought:', font=('calibre',9))
                self.name_label.grid(row=3,column=0,padx=10,pady=7, sticky="ew")
                self.name_label = ttk.Label(interface_frame_section_1, text = 'Profit:', font=('calibre',9))
                self.name_label.grid(row=4,column=0,padx=10,pady=7, sticky="ew")

        labels()

        def Entries():
            self.entry_widget_type = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_type.grid(row=0,column=1,padx=10,pady=7, sticky="ew")
            self.entry_text_widget_Timeofsubscription = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_text_widget_Timeofsubscription.grid(row=1,column=1,padx=10,pady=7, sticky="ew")
            self.entry_widget_Priceinshop = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_Priceinshop.grid(row=2,column=1,padx=10,pady=7, sticky="ew")
            self.entry_widget_Priceofbought = ttk.Entry(interface_frame_section_1, width=20, font=('Arial', 9))
            self.entry_widget_Priceofbought.grid(row=3,column=1,padx=10,pady=7, sticky="ew")

        Entries()

        def Buttons():
            self.button_add_item_database = ttk.Button(interface_frame_section_1, text="Add",command=self.add_item)
            self.button_add_item_database.grid(row=5,column=0,padx=20,pady=10, sticky="ew")


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
        
        #if the prices are numbers
        try:
            int(self.entry_widget_Priceinshop.get())
        except:
            messagebox.showinfo("showerror", "Your Price In Shop entry is not a number")
            return
        
        try:
            int(self.entry_widget_Priceofbought.get())
        except:
            messagebox.showinfo("showerror", "Your Price Of Bought entry is not a number")
            return



        try:
            # Connect to the database
            conn = sqlite3.connect('products.db')

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()


            profit = int(self.entry_widget_Priceinshop.get()) - int(self.entry_widget_Priceofbought.get())

            values = (self.entry_widget_type.get(), self.entry_text_widget_Timeofsubscription.get(), self.entry_widget_Priceinshop.get(), self.entry_widget_Priceofbought.get(),str(profit))

            # Queries to INSERT records. 
            cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", values)            
            # Commit your changes in the database     
            conn.commit() 
            
            # Closing the connection 
            conn.close()

            self.database_to_combo()
            
            messagebox.showinfo("showinfo", "You have added a product!") 

        except:
            messagebox.showerror("showerror", "That product already exists") 
            print("That product already exists")     


    def on_scroll(self,*args):#will be called whenever the scrollbar is manipulated.    It calls the yview method of the table widget with the provided arguments, allowing the text widget to scroll vertically.
        self.table.yview(*args)

    def table(self):
        Tableframe = ttk.Frame(self)
        Tableframe.grid(row=0, column=1,padx=0,pady=10)

        tablescroll = ttk.Scrollbar(Tableframe,command=self.on_scroll)
        tablescroll.pack(side="right",fill="y")

        cols = ("Products","Time of subscription","Price in shop","Price of bought","Profit")
        self.table = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=13)
        self.table.column("Products",width=200)
        self.table.column("Time of subscription",width=200)
        self.table.column("Price in shop",width=120)
        self.table.column("Price of bought",width=120)
        self.table.column("Profit",width=120)

        # define headings
        self.table.heading('Products', text='Products')
        self.table.heading('Time of subscription', text='Time of subscription')
        self.table.heading('Price in shop', text='Price in shop')
        self.table.heading('Price of bought', text='Price of bought')
        self.table.heading('Profit', text='Profit')
        self.table.pack()


        self.update_table()

    
    def clear_table(self):
        self.table.delete(*self.table.get_children())

    def update_table(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()

        #Insert the data from the excel to the table:

        #get the length of the products list
        products_dic = read_excel.get_all_products()
        products_length = len(products_dic['Products'])


        for i in range(products_length):
            self.table.insert('', tk.END, values=(
                products_dic['Products'][i],
                products_dic['Time of subscription'][i],
                products_dic['Price in shop'][i],
                products_dic['Price of bought'][i],
                products_dic['Profit'][i]
            ))


    def database_to_combo(self):
        self.combo_list.clear()

        # Connecting to sqlite 
        conn = sqlite3.connect('products.db') 
        
        # Creating a cursor object using the cursor() method 
        cursor = conn.cursor() 

        data=cursor.execute('''SELECT * FROM products''') 
        for row in data:
            self.combo_list.append(row[0])
  

        self.combo1['values'] = self.combo_list

    def combo_selected(self,event):
      # Connecting to sqlite 
        conn = sqlite3.connect('products.db') 
        
        # Creating a cursor object using the cursor() method 
        cursor = conn.cursor() 

        name = str(self.combo1.get())
        print(name)

        # Execute the query with the correct parameter binding
        cursor.execute("SELECT * FROM products WHERE name=?", (name,))

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
