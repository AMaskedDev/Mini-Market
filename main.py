# Imported libraries
import customtkinter
from CTkTable import *
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import tkinter

import json
import os
import time

import atexit
import threading


# Setting the appearance by default to light
customtkinter.set_appearance_mode("light")

# Checking if the `products.json` exists
if os.path.isfile("products.json"):
    print("Found products json file!")
else:
    open("products.json", "x")
    with open("products.json", "w") as file:
        file.write("{}")


class Main:
    def __init__(self):
        # Variables
        self.total_products_cost = 0
        self.buying_amount = 0

        # Start functions
        self.MainGUI()

    def MainGUI(self):
        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")
        self.application.geometry("1050x700")

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.application, height=100, corner_radius=0)
        self.Header.pack(fill="x")

        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Buying treeview
        self.ProductsTableFrame = customtkinter.CTkScrollableFrame(self.application)
        self.ProductsTableFrame.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)

        self.ProductsTable = CTkTable(self.ProductsTableFrame, row=0, column=0, values=[["Amount", "Product", "Cost"], ], font=("calibri", 20))
        self.ProductsTable.pack(fill=tkinter.X)

        # Barcode input
        self.BarcodeE = customtkinter.CTkEntry(self.application, placeholder_text="Enter barcode", corner_radius=0, font=("calibri", 22), width=270, height=40)
        self.BarcodeE.pack(pady=(0, 15))

        # Buttons
        self.AddProductB = customtkinter.CTkButton(self.application, text="Add Product", font=("calibri", 18), width=250, height=35, corner_radius=2, command=self.AddTableProduct)
        self.AddProductB.pack(pady=(0, 15))

        self.CheckinB = customtkinter.CTkButton( self.application, text="Check in", font=("calibri", 18), width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2, command=self.Checkin)
        self.CheckinB.pack(pady=(0, 4))

        self.ClearB = customtkinter.CTkButton(self.application, text="Clear", font=("calibri", 18), width=250, height=35, fg_color="#AB2525", hover_color="#942020", corner_radius=2, command=self.ClearTable)
        self.ClearB.pack(pady=(0, 15))

        # Storage Management Buttons
        self.Storage_AddProductB = customtkinter.CTkButton(self.Header, text="Add Product", corner_radius=0, fg_color="#47A641", hover_color="#3E9338", command=lambda: threading.Thread(target=Add_Product()).start())
        self.Storage_AddProductB.pack(side="left", padx=(10, 0))

        self.Storage_RemoveProductB = customtkinter.CTkButton(self.Header, text="Remove Product", corner_radius=2, fg_color="#D94B4B", hover_color="#B23D3D", command=lambda: threading.Thread(target=Remove_Product()).start())
        self.Storage_RemoveProductB.pack(side="left", padx=(10, 0))

        self.Storage_ViewProductB = customtkinter.CTkButton(self.Header, text="View Products", corner_radius=2, command=lambda: threading.Thread(target=View_Products()).start())
        self.Storage_ViewProductB.pack(side="left", padx=(10, 0))

        self.Storage_ViewProductB = customtkinter.CTkButton(self.Header, text="Settings", corner_radius=2, command=lambda: threading.Thread(target=View_Products()).start())
        self.Storage_ViewProductB.pack(side="right", padx=(0, 50))

        # Starting other methods
        self.Clock()

        # Binding commands / events to functions
        self.BarcodeE.bind("<Return>", self.AddTableProduct)

        self.application.protocol("WM_DELETE_WINDOW", self.Exit)
        atexit.register(self.ResetProducts)

        # Application rendering loop
        self.application.mainloop()

    def Checkin(self):
        # Check if there are any products to buy
        if self.total_products_cost < 0:
            messagebox.showinfo("Error", "Couldn't checkout. \nNo products to buy!")
            return

        # Reduce available products and reset the `runtime` variable
        data = None
        with open("products.json", "r") as read:
            data = json.load(read)
            for product_data in data.values():
                product_data["available"] -= self.buying_amount
                product_data["runtime"] = product_data["available"]

        with open("products.json", "w") as write:
            json.dump(data, write)

        # Print the total cost
        messagebox.showinfo("Check in", f"The total cost for every product is €{self.total_products_cost} \nThank you!")

        # Refreshing the table
        self.RefreshTable()

    def RefreshTable(self):
        # Destroy (Delete the values) and re-make the table
        self.ProductsTable.destroy()
        self.ProductsTable = CTkTable(self.ProductsTableFrame, row=0, column=0, values=[["Amount", "Product", "Cost"], ], font=("calibri", 20))
        self.ProductsTable.pack(fill=tkinter.X)

        self.BarcodeE.delete(0, tkinter.END)
        self.BarcodeE.focus_set()

    def ClearTable(self):
        if self.total_products_cost < 0:
            messagebox.showinfo("Error", "Couldn't clear. \nNo products to clear!")
            return

        # Resetting the `runtime` variable in the `products.json` file
        data = None
        with open("products.json", "r") as reading:
            data = json.load(reading)
            for product_data in data.values():
                product_data["available"] -= self.buying_amount
                product_data["runtime"] = product_data["available"]

        with open("products.json", "w") as dump:
            json.dump(data, dump)

        # Refreshing the table
        self.RefreshTable()

    def AddTableProduct(self, event=None):
        # Temporary variables
        barcode = self.BarcodeE.get()
        data = None

        # Empty and focus to the barcode input
        self.BarcodeE.delete(0, tkinter.END)
        self.BarcodeE.focus_set()

        # Read the `products.json` and put the data to the `data` var
        with open("products.json", "r") as file:
            data = json.load(file)
            file.close()
        
        # Adding the product to the table
        if len(barcode) < 0:
            messagebox.showerror("Error", "Please use a valid product ID.")
            return

        # Checking if the `products.json` file exists
        if not os.path.isfile("products.json"):
            messagebox.showerror("Error", "No products.json file found.")
            return

        # Getting the amount of products
        self.buying_amount = simpledialog.askinteger("Amount", "How many products?")

        # Checking if the amount is not above 0
        if self.buying_amount < 0:
            messagebox.showerror("Error", "Invalid product amount")
            return
        
        runtime = data[barcode].get("runtime")
        if runtime < self.buying_amount:
            messagebox.showerror("Error", "Insufficient products in the storage.")
            return

        # Checking if the barcode doesn't exist
        if barcode not in data:
            messagebox.showerror("Error", f"Product with barcode {barcode} not found in storage.")
            return

        # Getting information about the product
        data[barcode]["runtime"] -= self.buying_amount

        product = data[barcode]["name"]
        cost = data[barcode]["cost"]

        self.total_products_cost += data[barcode]["cost"] * self.buying_amount
        self.ProductsTable.add_row(values=[f"{self.buying_amount}", f"{product}", f"{cost * self.buying_amount}"])

        # Update product information
        with open("products.json", "w") as file:
            json.dump(data, file)

    def ResetProducts(self):
        # Temporary variable
        data = None

        # Reading every product and resetting its runtime to the available
        with open("products.json", "r") as file:
            data = json.load(file)
            for product_data in data.values():
                product_data["runtime"] = product_data["available"]

        with open("products.json", "w") as file:
            json.dump(data, file)

    def Exit(self):
        # Temporary variable
        data = None

        # Reading every product and resetting its runtime to the available
        with open("products.json", "r") as file:
            data = json.load(file)
            for product_data in data.values():
                product_data["runtime"] = product_data["available"]

        with open("products.json", "w") as file:
            json.dump(data, file)

        # Destroy root to exit
        self.application.destroy()

    def Clock(self):
        # Setting the format
        current_time = time.strftime("%I:%M %p")

        # Changing the text and recalling this function after 1 second
        self.ClockL.configure(text=current_time)
        self.ClockL.after(1000, self.Clock)


class View_Products:
    def __init__(self):
        self.product_barcode = None

        # Start functions
        self.MainGUI()

    def MainGUI(self):
        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")
        self.application.geometry("1050x600")

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.application, height=100, corner_radius=0)
        self.Header.pack(fill="x")

        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Buying treeview
        self.product_list_frame = customtkinter.CTkScrollableFrame(self.application)
        self.product_list_frame.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)

        self.ProductsTable = CTkTable(self.product_list_frame, row=0, column=0, values=[["Product", "Cost", "Available"], ], font=("calibri", 20))
        self.ProductsTable.pack(fill=tkinter.X)

        # Storage Management
        self.FindProductB = customtkinter.CTkButton(self.Header, text="Find product", corner_radius=0, fg_color="#47A641", hover_color="#3E9338", command=lambda: threading.Thread(target=self.FindProduct()).start())
        self.FindProductB.pack(side="left", padx=(10, 0))

        self.RemoveProductsB = customtkinter.CTkButton(self.Header, text="Remove All Product", corner_radius=2, fg_color="#D94B4B", hover_color="#B23D3D", command=self.RemoveAll)
        self.RemoveProductsB.pack(side="left", padx=(10, 0))

        self.RefreshTableB = customtkinter.CTkButton(self.Header, text="Refresh Products", corner_radius=2, command=lambda: threading.Thread(target=self.RefreshTable()).start())
        self.RefreshTableB.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.AddProducts()
        self.Clock()

        # Application rendering loop
        self.application.mainloop()

    def RemoveAll(self):
        # Verification
        verification = messagebox.askyesno("Continue", "Are you sure removing every product?")

        if not verification:
            messagebox.showinfo("Unsuccessful", "Canceled the operation.")
            return

        # Remove file and rewrite `{}`
        os.remove("products.json")

        open("products.json", "x")
        with open("products.json", "w") as file:
            file.write("{}")

        self.application.destroy()
        messagebox.showinfo("Success", "Removed every product in storage.")

    def AddProducts(self):
        data = None

        with open("products.json", "r") as file:
            data = json.load(file)
            file.close()

        for barcode, product_data in data.items():
            product_name = product_data.get("name", "")
            product_cost = product_data.get("cost", "")
            product_available = product_data.get("available", "")

            self.ProductsTable.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def FindProduct(self):
        self.root = customtkinter.CTk()
        self.root.geometry("500x250")
        self.root.title("Product Scanning")
        self.root.resizable(False, False)

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.root, height=100, corner_radius=0)
        self.Header.pack(fill="x", pady=(0, 30))

        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Barcode input
        self.ProductE = customtkinter.CTkEntry(self.root, placeholder_text="Product ID", font=("calibri", 20), width=250, height=35)
        self.ProductE.pack(pady=(10, 5))

        # Continue button
        self.ContinueB = customtkinter.CTkButton( self.root, text="Continue", font=("calibri", 18), command=self.Checkpoint_To_Scan, width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2 )
        self.ContinueB.pack(pady=(0, 4))

        self.ProductE.bind("<Return>", self.Checkpoint_To_Scan)

        # Starting other functions  
        self.ClockL()

        # Application rendering loop
        self.root.mainloop()

    def Checkpoint_To_Scan(self, event=None):
        # Getting the ID
        self.product_barcode = self.ProductE.get()

        # Check if the ID has any value
        if len(self.product_barcode) > 0:
            self.RefreshTable()
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid barcode")

    def RefreshTable(self):
        # Destroying and reconfigure the table
        self.ProductsTable.destroy()
        self.ProductsTable = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ], font=("calibri", 20))
        self.ProductsTable.pack(fill=tkinter.X)

        # Searching for the `self.product_barcode` inside `data`
        if os.path.isfile("products.json"):
            with open("products.json", "r") as file:
                data = json.load(file)

            if self.product_barcode in data:
                product_name = data[self.product_barcode]["name"]
                product_cost = data[self.product_barcode]["cost"]
                product_available = data[self.product_barcode]["available"]

                self.ProductsTable.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def Clock(self):
        # Setting the format
        current_time = time.strftime("%I:%M %p")

        # Changing the text and recalling this function after 1 second
        self.ClockL.configure(text=current_time)
        self.ClockL.after(1000, self.Clock)


class Remove_Product:
    def __init__(self):
        # Variables
        self.product_exists = False

        # Functions
        self.MainGUI()

    def MainGUI(self):
        self.root = customtkinter.CTk()
        self.root.geometry("500x250")
        self.root.title("Product Scanning")
        self.root.resizable(False, False)

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.root, height=100, corner_radius=0)
        self.Header.pack(fill="x", pady=(0, 30))

        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Barcode input
        self.ProductE = customtkinter.CTkEntry(self.root, placeholder_text="Product ID", font=("calibri", 20), width=250, height=35)
        self.ProductE.pack(pady=(10, 5))

        # Continue button
        self.ContinueB = customtkinter.CTkButton( self.root, text="Continue", font=("calibri", 18), command=self.Checkpoint_To_Info, width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2)
        self.ContinueB.pack(pady=(0, 4))

        self.ProductE.bind("<Return>", self.Checkpoint_To_Info)

        # Starting other functions
        self.Clock()

        # Application rendering loop
        self.root.mainloop()

    def Checkpoint_To_Info(self, event=None):
        # Variables
        self.barcode = self.ProductE.get()

        # Checking if the barcode is valid
        if self.barcode == "":
            messagebox.showerror("Checkpoint", "Please provide a valid product ID.")
        else:
            # Checking if it exists in the storage
            data = None
            with open("products.json", "r") as temp:
                data = json.load(temp)

            if self.barcode in data:
                self.product_exists = True
            else:
                self.product_exists = False

            # Destroying the `root` 
            self.root.destroy()
            self.RemoveProduct()

    def RemoveProduct(self, event=None):
        # Temporary variables
        file_data = None

        # Loading the json file to a temporary data variable
        with open("products.json", "r") as file:
            file_data = json.load(file)

        # Checking if the product exists
        if self.barcode in file_data:
            # Removing the whole `barcode` product
            del file_data[self.barcode]

            with open("products.json", "w") as file:
                json.dump(file_data, file)

            messagebox.showinfo("Product", "Product was removed from storage.")

        else:
            messagebox.showinfo("Product", "Product was not found in storage to remove.")

    def Clock(self):
        # Setting the format
        current_time = time.strftime("%I:%M %p")

        # Changing the text and recalling this function after 1 second
        self.ClockL.configure(text=current_time)
        self.ClockL.after(1000, self.Clock)


class Add_Product:
    def __init__(self):
        # Variables
        self.application = None
        self.barcode = None
        self.product_exists = False

        # Functions
        self.MainGUI()

    def MainGUI(self):
        self.root = customtkinter.CTk()
        self.root.geometry("500x250")
        self.root.title("Product Scanning")
        self.root.resizable(False, False)

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.root, height=100, corner_radius=0)
        self.Header.pack(fill="x", pady=(0, 30))

        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Barcode input
        self.ProductE = customtkinter.CTkEntry(self.root, placeholder_text="Product ID", font=("calibri", 20), width=250, height=35)
        self.ProductE.pack(pady=(10, 5))

        # Continue button
        self.ContinueB = customtkinter.CTkButton( self.root, text="Continue", font=("calibri", 18), command=self.Checkpoint_To_Info, width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2)
        self.ContinueB.pack(pady=(0, 4))

        # Binding commands / events to functions
        self.ProductE.bind("<Return>", self.Checkpoint_To_Info)

        # Starting other functions
        self.Clock()

        # Application rendering loop
        self.root.mainloop()

    def Checkpoint_To_Info(self, event=None):
        # Variables
        self.barcode = self.ProductE.get()

        # Checking if the barcode is valid
        if self.barcode == "":
            messagebox.showerror("Checkpoint", "Please provide a valid product ID.")
        else:

            # Checking if it exists in the storage
            data = None
            with open("products.json", "r") as temp:
                data = json.load(temp)

            if self.barcode in data:
                self.product_exists = True
            else:
                self.product_exists = False

            # Product info gui
            self.root.destroy()
            self.ProductInfoGUI()

    def ProductInfoGUI(self):
        self.application = customtkinter.CTk()
        self.application.geometry("600x350")
        self.application.title("Product Scanning")
        self.application.resizable(False, False)

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.application, height=100, corner_radius=0)
        self.Header.pack(fill="x", pady=(0, 30))

        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Title
        if self.product_exists: self.title = customtkinter.CTkLabel(self.Header, text="Edit product", font=("calibri", 24))
        else: self.title = customtkinter.CTkLabel(self.Header, text="Add product", font=("calibri", 24))

        self.title.pack(side="left", padx=(10, 0))

        # Product info

        self.ProductNameE = customtkinter.CTkEntry(self.application, placeholder_text="Product Name", font=("calibri", 20), width=250, height=35)
        self.ProductNameE.pack(pady=(10, 5))

        self.ProductCostE = customtkinter.CTkEntry(self.application, placeholder_text="Product Cost", font=("calibri", 20), width=250, height=35)
        self.ProductCostE.pack(pady=(10, 5))

        self.ProductAvailableE = customtkinter.CTkEntry(self.application, placeholder_text="Product Available", font=("calibri", 20), width=250, height=35)
        self.ProductAvailableE.pack(pady=(10, 30))

        self.ContinueB = customtkinter.CTkButton(self.application, text="Continue", font=("calibri", 18), width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2, command=self.AddProduct)
        self.ContinueB.pack(pady=(0, 4))

        # Binding commands / events to functions
        self.ProductAvailableE.bind("<Return>", self.AddProduct)

        # Staring other functions
        self.Clock()

        # Initializing the base window
        self.application.mainloop()

    def AddProduct(self):
        # Variables
        product_name = self.ProductNameE.get()
        product_cost = self.ProductCostE.get()
        product_available = self.ProductAvailableE.get()

        data = None

        # Checking if the product cost and availables are numbers
        try:
            float(product_cost)
            int(product_available)
        except ValueError:
            messagebox.showerror("Error", "Use only numbers in cost and availability.")
            return

        # Data variable
        product_data = {
            self.barcode: {
                "name": product_name,
                "cost": float(product_cost),
                "available": int(product_available),
                "runtime": int(product_available)
            }
        }

        # Read the json file `products.json`
        try:
            with open("products.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
            messagebox.showerror("Error", "An error occurred while opening file products.json")

        # Check if the product_id already exists in the data
        if self.barcode in data:
            # Product exists, update cost and availability
            data[self.barcode]["cost"] = int(product_cost)
            data[self.barcode]["available"] = int(product_available)
        else:
            # Product doesn't exist, add new product information
            data.update(product_data)

        with open("products.json", "w") as file:
            json.dump(data, file)

        if product_cost is not None and product_available is not None and product_available is not None:
            messagebox.showinfo("Valid Product Info", f"Product {product_name} was added to storage successfully.")
        else:
            messagebox.showerror("Invalid Product Info", f"Product was not added, invalid product information.")

        self.application.destroy()

    def Clock(self):
        # Setting the format
        current_time = time.strftime("%I:%M %p")

        # Changing the text and recalling this function after 1 second
        self.ClockL.configure(text=current_time)
        self.ClockL.after(1000, self.Clock)


# Start of the project
if __name__ == "__main__":
    Main()
