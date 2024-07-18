#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
from tkinter import *
from tkinter import messagebox

# Connect to SQLite Database
conn = sqlite3.connect('billing.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Products (
             product_id INTEGER PRIMARY KEY,
             product_name TEXT,
             product_price REAL,
             product_quantity INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS Customers (
             customer_id INTEGER PRIMARY KEY,
             customer_name TEXT,
             customer_phone TEXT,
             customer_email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Transactions (
             transaction_id INTEGER PRIMARY KEY,
             customer_id INTEGER,
             product_id INTEGER,
             quantity INTEGER,
             total_price REAL,
             transaction_date TEXT,
             FOREIGN KEY(customer_id) REFERENCES Customers(customer_id),
             FOREIGN KEY(product_id) REFERENCES Products(product_id))''')

conn.commit()


# In[ ]:


class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        
        # Create Frames
        self.frame1 = Frame(root)
        self.frame1.pack(side=TOP)
        
        self.frame2 = Frame(root)
        self.frame2.pack(side=LEFT)
        
        self.frame3 = Frame(root)
        self.frame3.pack(side=RIGHT)
        
        # Frame1: Header
        self.header_label = Label(self.frame1, text="Billing Software", font=("Arial", 24))
        self.header_label.pack()
        
        # Frame2: Product Entry
        self.product_label = Label(self.frame2, text="Product Details", font=("Arial", 18))
        self.product_label.pack()
        
        self.product_name_label = Label(self.frame2, text="Product Name")
        self.product_name_label.pack()
        self.product_name_entry = Entry(self.frame2)
        self.product_name_entry.pack()
        
        self.product_price_label = Label(self.frame2, text="Product Price")
        self.product_price_label.pack()
        self.product_price_entry = Entry(self.frame2)
        self.product_price_entry.pack()
        
        self.product_quantity_label = Label(self.frame2, text="Product Quantity")
        self.product_quantity_label.pack()
        self.product_quantity_entry = Entry(self.frame2)
        self.product_quantity_entry.pack()
        
        self.add_product_button = Button(self.frame2, text="Add Product", command=self.add_product)
        self.add_product_button.pack()
        
        # Frame3: Customer Entry
        self.customer_label = Label(self.frame3, text="Customer Details", font=("Arial", 18))
        self.customer_label.pack()
        
        self.customer_name_label = Label(self.frame3, text="Customer Name")
        self.customer_name_label.pack()
        self.customer_name_entry = Entry(self.frame3)
        self.customer_name_entry.pack()
        
        self.customer_phone_label = Label(self.frame3, text="Customer Phone")
        self.customer_phone_label.pack()
        self.customer_phone_entry = Entry(self.frame3)
        self.customer_phone_entry.pack()
        
        self.customer_email_label = Label(self.frame3, text="Customer Email")
        self.customer_email_label.pack()
        self.customer_email_entry = Entry(self.frame3)
        self.customer_email_entry.pack()
        
        self.add_customer_button = Button(self.frame3, text="Add Customer", command=self.add_customer)
        self.add_customer_button.pack()
        
        # Frame1: Transaction and Billing
        self.transaction_label = Label(self.frame1, text="Transaction Details", font=("Arial", 18))
        self.transaction_label.pack()
        
        self.transaction_product_label = Label(self.frame1, text="Product ID")
        self.transaction_product_label.pack()
        self.transaction_product_entry = Entry(self.frame1)
        self.transaction_product_entry.pack()
        
        self.transaction_customer_label = Label(self.frame1, text="Customer ID")
        self.transaction_customer_label.pack()
        self.transaction_customer_entry = Entry(self.frame1)
        self.transaction_customer_entry.pack()
        
        self.transaction_quantity_label = Label(self.frame1, text="Quantity")
        self.transaction_quantity_label.pack()
        self.transaction_quantity_entry = Entry(self.frame1)
        self.transaction_quantity_entry.pack()
        
        self.generate_bill_button = Button(self.frame1, text="Generate Bill", command=self.generate_bill)
        self.generate_bill_button.pack()
        
    def add_product(self):
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        quantity = int(self.product_quantity_entry.get())
        
        c.execute("INSERT INTO Products (product_name, product_price, product_quantity) VALUES (?, ?, ?)",
                  (name, price, quantity))
        conn.commit()
        
        messagebox.showinfo("Success", "Product added successfully!")
        
    def add_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        
        c.execute("INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES (?, ?, ?)",
                  (name, phone, email))
        conn.commit()
        
        messagebox.showinfo("Success", "Customer added successfully!")
        
    def generate_bill(self):
        product_id = int(self.transaction_product_entry.get())
        customer_id = int(self.transaction_customer_entry.get())
        quantity = int(self.transaction_quantity_entry.get())
        
        c.execute("SELECT product_price FROM Products WHERE product_id=?", (product_id,))
        price = c.fetchone()[0]
        total_price = price * quantity
        
        c.execute("INSERT INTO Transactions (customer_id, product_id, quantity, total_price, transaction_date) VALUES (?, ?, ?, ?, DATE('now'))",
                  (customer_id, product_id, quantity, total_price))
        conn.commit()
        
        messagebox.showinfo("Success", "Bill generated successfully!")
        
root = Tk()
app = BillingApp(root)
root.mainloop()


# In[ ]:




