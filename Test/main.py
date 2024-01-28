# Imported libraries
import customtkinter
from CTkTable import *
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import tkinter

import configparser
import json
import os
import sys
import subprocess
import time

import atexit
import threading

existance = "402"
error = "404"
invalid = "401"

def Restart():
    # Getting script path
    script = sys.argv
    
    # Run a new instance of the script
    subprocess.Popen([sys.executable] + script)

    # Exit the current instance
    sys.exit()

# Checking if the settings file doesn't exit
settings_path = os.path.abspath("settings.ini")

if not os.path.isfile(settings_path):
    print("Error", "Settings file doesn't exist! Making new.")

    # Save the new settings to the file
    open(settings_path, 'x').close()

# Settings
darkethemed = None
time_format = None

# Create a ConfigParser object
config = configparser.ConfigParser()
if os.path.isfile(settings_path):
    config.read(settings_path)
    # Check if the 'Theme' section exists before retrieving values
    if 'Theme' in config:
        # Read values
        darkethemed = config.getboolean('Theme', 'darked-theme')
        time_format = config.getboolean('Theme', 'time-format')
    else:
        config['Theme'] = {'darked-theme': 0, 'time-format': 1}
        with open(settings_path, 'w') as config_file:
            config.write(config_file)
            
        Restart()
else:
    print("Error: settings.ini file not found\n Error Code " + existance)

# Setting the theme based on user settings
if darkethemed:
    customtkinter.set_appearance_mode("dark")
else:
    customtkinter.set_appearance_mode("light")

# Checking if the `products.json` exists
if os.path.isfile("products.json"):
    print("Found products json file!")
else:
    print("Error: products.json file not found\n Error Code " + existance)
    
    open("products.json", "x")
    with open("products.json", "w") as file:
        file.write("{}")


class Main:
    def __init__(self):
        # Variables
        self.total_products_cost = 0
        self.product_amount = 0

        # Start functions
        self.MainGUI()

    def MainGUI(self):
        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")
        self.application.geometry("1050x700")
        
        #self.application.wm_iconbitmap("favicon.ico")

        # Tabs
        self.ViewTab = customtkinter.CTkTabview(self.application, height=700, width=1050)
        self.ViewTab.pack()
        
        self.ViewTab.add("Main")
        self.ViewTab.add("Settings")
        
        # Application rendering loop
        self.application.mainloop()
        
        """ # Buying treeview
        self.ProductsTableFrame = customtkinter.CTkScrollableFrame(self.application)
        self.ProductsTableFrame.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)
        
        self.ProductsTable = CTkTable(self.ProductsTableFrame, row=0, column=0, values=[["Amount", "Product", "Cost", "Discount"], ], font=("calibri", 20))
        self.ProductsTable.pack(fill=tkinter.X)

        # Barcode input
        self.BarcodeE = customtkinter.CTkEntry(self.application, placeholder_text="Enter barcode", corner_radius=0, font=("calibri", 22), width=270, height=40)
        self.BarcodeE.pack(pady=(0, 15))

        # Buttons
        self.AddProductB = customtkinter.CTkButton(self.application, text="Add Product", font=("calibri", 18), width=250, height=35, corner_radius=2, command=self.Checkpoint_To_AddTableProduct)
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
        
        self.SettingsB = customtkinter.CTkButton(self.Header, text="Settings", corner_radius=2, command=lambda: threading.Thread(target=Settings()).start())
        self.SettingsB.pack(side="right", padx=(0, 50))

        # Starting other methods
        self.Clock()
        #self.SettingsView()

        # Binding commands / events to functions
        self.BarcodeE.bind("<Return>", self.Checkpoint_To_AddTableProduct)

        self.application.protocol("WM_DELETE_WINDOW", self.Exit)
        atexit.register(self.ResetProducts)

        # Application rendering loop
        self.application.mainloop() """

    def Checkin(self):
        if self.total_products_cost > 0:
            messagebox.showinfo("Check in", f"The total cost for every product is €{self.total_products_cost} \nThank you!")

            # Reduce available products and reset the `runtime` variable
            data = None
            with open("products.json", "r") as file:
                data = json.load(file)
                for product_data in data.values():
                    product_data["available"] -= self.amount
                    product_data["runtime"] = product_data["available"]

            with open("products.json", "w") as file:
                json.dump(data, file)

            # Refreshing the table
            self.RefreshTable()
            
        else:
            messagebox.showinfo("Error", "Couldn't checkout. \nNo products to buy!")

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
                product_data["available"] -= self.amount
                product_data["runtime"] = product_data["available"]

        with open("products.json", "w") as dump:
            json.dump(data, dump)

        # Refreshing the table
        self.RefreshTable()

    def Checkpoint_To_AddTableProduct(self, event=None):
        # Variales
        data = None
        barcode = self.BarcodeE.get()
        
        # Checking if the barcode is valid
        if barcode == "":
            messagebox.showerror("Error", "Please use a valid product ID.\nError Code " + invalid)
            return
        
        # Checking if the product exists
        with open("products.json", "r") as file:
            data = json.load(file)
            
        if not barcode in data:
            messagebox.showerror("Error", "Product doesn't exist in storage.\nError Code " + existance)
            return        
        
        self.AddTableProductGUI()
        
    def AddTableProductGUI(self):
        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")
        self.application.geometry("550x300")
        self.application.resizable(False, False)

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.application, height=100, corner_radius=0)
        self.Header.pack(fill="x")
        
        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Barcode input
        self.ProductAmountE = customtkinter.CTkEntry(self.application, placeholder_text="Enter amounts", corner_radius=0, font=("calibri", 22), width=270, height=40)
        self.ProductAmountE.pack(pady=(15, 0))
        
        self.DiscountAmountE = customtkinter.CTkEntry(self.application, placeholder_text="Enter discount", corner_radius=0, font=("calibri", 22), width=270, height=40)
        self.DiscountAmountE.pack(pady=(10, 15))

        # Button
        self.ContinueB = customtkinter.CTkButton(self.application, text="Add Product", font=("calibri", 18), width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2, command=lambda: self.AddTableProduct(amounts=self.ProductAmountE.get(), discount=self.DiscountAmountE.get()))
        self.ContinueB.pack(pady=(10, 0))

        self.ClearB = customtkinter.CTkButton(self.application, text="Clear", font=("calibri", 18), width=250, height=35, fg_color="#AB2525", hover_color="#942020", corner_radius=2, command=self.ClearTable)
        self.ClearB.pack(pady=(5, 15))
    
        # Starting other methods
        self.Clock()    
                
        # Binding commands / events to functions
        self.ProductAmountE.bind("<Return>", lambda: self.AddTableProduct(amounts=self.ProductAmountE.get(), discount=self.DiscountAmountE.get()))
        
        # Application rendering loop
        self.application.mainloop()
    
    def AddTableProduct(self, amounts, discount, event=None): 
        # Temporary variables
        barcode = self.BarcodeE.get()
        data = None
        

        # Empty and focus to the barcode input
        self.BarcodeE.delete(0, tkinter.END)
        self.BarcodeE.focus_set()
        
        # Converting the products amount to an integer
        try:
            amounts = int(amounts)
            discount = int(discount)
        except ValueError:
            messagebox.showerror("Error", "Invalid information \nError Code " + invalid)
            return

        # Reading the json file
        with open("products.json", "r") as file:
            data = json.load(file)
        
        # Getting information
        data[barcode]["runtime"] -= amounts
        product = data[barcode]["name"]
        cost = data[barcode]["cost"]

        # Adding product to table
        self.total_products_cost += data[barcode]["cost"] * (amounts / discount)
        self.ProductsTable.add_row(values=[f"x {amounts}", f"{product}", f"€{cost}", f"{discount}%"])

        # Update runtime in the file
        with open("products.json", "w") as file:
            json.dump(data, file)
            file.close()

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
        sys.exit(0)        

    def Clock(self):
        # Setting the format
        time_ampm = time.strftime("%I:%M %p")
        time_24h = time.strftime("%H:%M")

        # Changing the text and recalling this function after 1 second
        if time_format == 1:
            self.ClockL.configure(text=time_ampm)
        elif time_format == 0:
            self.ClockL.configure(text=time_24h)
            
        self.ClockL.after(1000, self.Clock)
        
    def SettingsView(self):
        if self.ViewTab.tab("Main"):
            self.application.destroy()
            Settings()
        
        self.application.after(73, self.SettingsView)


""" class Settings:
    def __init__(self):
        # Start functions
        self.MainGUI()
        
    def MainGUI(self):
        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")
        self.application.geometry("800x500")

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.application, height=100, corner_radius=0)
        self.Header.pack(fill="x")
        
        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))
        
        self.HelpB = customtkinter.CTkButton(self.Header, text="Help Menu", corner_radius=2, command=self.Help)
        self.HelpB.pack(side="left", padx=(10, 0))

        # Settings
        self.DarkThemedC = customtkinter.CTkCheckBox(self.application, text="Dark Themed", font=("calibri", 18))
        self.DarkThemedC.pack(pady=(10, 0))
        
        self.TimeFormatC = customtkinter.CTkCheckBox(self.application, text="Time Format (AM/PM / 24H)", font=("calibri", 18))
        self.TimeFormatC.pack(pady=(10, 0))
        
        # Buttons
        self.ExitB = customtkinter.CTkButton(self.application, text="Exit", font=("calibri", 18), width=250, height=35, fg_color="#AB2525", hover_color="#942020", corner_radius=2, command=lambda: Main())
        self.ExitB.pack(side="bottom", pady=(0, 20))
        
        self.AddProductB = customtkinter.CTkButton(self.application, text="Done", font=("calibri", 18), width=250, height=35, corner_radius=2, command=self.SaveSettings)
        self.AddProductB.pack(side="bottom", pady=(0, 5))
        
        # Label
        self.informationL = customtkinter.CTkLabel(self.application, text="Click `done` for changes to take effect", font=("calibri", 16))
        self.informationL.pack(side="bottom", pady=(0, 10))
        
        # Starting other methods
        self.Clock()
        
        # Application rendering loop
        self.application.mainloop()
        
    def Help(self):
        # Initializing the base window
        self.applicationt = customtkinter.CTk()
        self.applicationt.title("Help Menu")
        self.applicationt.geometry("900x600")

        # Header Frame
        self.Header = customtkinter.CTkFrame(self.applicationt, height=100, corner_radius=0)
        self.Header.pack(fill="x")
        
        # Clock
        self.ClockL = customtkinter.CTkLabel(self.Header, text="0:00", font=("calibri", 28))
        self.ClockL.pack(side="right", pady=(12, 12), padx=(0, 15))
        
        # Text
        self.ErrorCodesL = customtkinter.CTkLabel(self.applicationt, text="Error Codes", font=("calibri", 24))
        self.ErrorCodesL.pack(pady=(10, 0))
        
        self.InvalidL = customtkinter.CTkLabel(self.applicationt, text="Invalid error (example: Invalid product ID) => 401", font=("calibri", 16))
        self.InvalidL.pack(pady=(10, 0))
        
        self.GeneralError = customtkinter.CTkLabel(self.applicationt, text="General error (example: Error while..) => 404", font=("calibri", 16))
        self.GeneralError.pack(pady=(10, 0))
        
        self.ExistanceError = customtkinter.CTkLabel(self.applicationt, text="Existance error (example: File `settings.ini` wasen't found) => 404", font=("calibri", 16))
        self.ExistanceError.pack(pady=(10, 0))
         
        # Buttons
        self.ExitB = customtkinter.CTkButton(self.applicationt, text="Exit", font=("calibri", 18), width=250, height=35, fg_color="#AB2525", hover_color="#942020", corner_radius=2, command=lambda: self.applicationt.destroy())
        self.ExitB.pack(side="bottom", pady=(0, 25))
        
    def GetSettings(self):
        global darkethemed, time_format
        
        # Set the checkboxes acording to settings
        if darkethemed == 1: self.DarkThemedC.select()
        elif darkethemed == 0: self.DarkThemedC.deselect()
        
        if time_format == 1: self.TimeFormatC.select()
        elif time_format == 0: self.TimeFormatC.deselect()
        
    def SaveSettings(self):
        global settings_path
        
        if 'Theme' not in config:
            # If 'Theme' section is not present, create it with default values
            config['Theme'] = {'darked-theme': True, 'time-format': True}
            with open(settings_path, 'w') as config_file:
                config.write(config_file)
        
        # Getting the value of the settings
        darkthemed = self.DarkThemedC.get()
        timeformat = self.TimeFormatC.get()
        
        # Set the updated value in the configuration
        config.set('Theme', 'darked-theme', str(darkthemed))
        config.set('Theme', 'time-format', str(timeformat))
        
        # Save the changes back to the configuration file
        with open(settings_path, 'w') as config_file:
            config.write(config_file)
            
        if messagebox.askyesno("Continue", "Are you sure this will restart the program, \nany client-side changes will be removed."):
            Restart()
             
    def Clock(self):
        # Setting the format
        time_ampm = time.strftime("%I:%M %p")
        time_24h = time.strftime("%H:%M")

        # Changing the text and recalling this function after 1 second
        if time_format == 1:
            self.ClockL.configure(text=time_ampm)
        elif time_format == 0:
            self.ClockL.configure(text=time_24h)
         
        self.ClockL.after(1000, self.Clock)
        
    def Unneccessary(self):
        time_ampm = time.strftime("%I:%M %p")
        time_24h = time.strftime("%H:%M")
        
        if self.TimeFormatC.get() == 1:
            self.TimeFormatC.configure(text=f"Time Format ({time_ampm})")
        elif self.TimeFormatC.get() == 0:
            self.TimeFormatC.configure(text=f"Time Format ({time_24h})")
            
        if self.DarkThemedC.get() == 1:
            self.DarkThemedC.configure(text=f"Dark theme (Enabled)")
        elif self.DarkThemedC.get() == 0:
            self.DarkThemedC.configure(text=f"Dark theme (Disabled)")
            
        self.application.after(20, self.Unneccessary)
            

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

        self.RefreshTableB = customtkinter.CTkButton(self.Header, text="Refresh Products", corner_radius=2, command=lambda: threading.Thread(target=self.AddProducts()).start())
        self.RefreshTableB.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.AddProducts()
        self.Clock()

        # Application rendering loop
        self.application.mainloop()

    def RemoveAll(self):
        # Verification
        verification = messagebox.askyesno("Continue", "Are you sure removing every product?")

        if verification:
            # Remove file and rewrite `{}`
            os.remove("products.json")

            open("products.json", "x")
            with open("products.json", "w") as file:
                file.write("{}")

            self.application.destroy()
            messagebox.showinfo("Success", "Removed every product in storage.")
        else:
            messagebox.showinfo("Unsuccessful", "Canceled the operation.")

    def AddProducts(self):
        self.RefreshTable()
        
        data = None

        if os.path.isfile("products.json"):
            with open("products.json", "r") as file:
                data = json.load(file)
                file.close()

            for barcode, product_data in data.items():
                product_name = product_data.get("name", "")
                product_cost = product_data.get("cost", "")
                product_available = product_data.get("available", "")

                self.ProductsTable.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def RefreshTable(self):
        self.ProductsTable.destroy()
        self.ProductsTable = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ], font=("calibri", 20))
        self.ProductsTable.pack(fill=tkinter.X)

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
        if self.product_barcode == "":
            messagebox.showerror("Error", "Invalid barcode\nError Code" + invalid)
            
            self.root.destroy()
            return
        else:
            self.ScanSpesific()
            self.root.destroy()

    def ScanSpesific(self):
        # Destroying and reconfigure the table
        self.RefreshTable()

        # Searching for the `self.product_barcode` inside `data`
        if os.path.isfile("products.json"):
            with open("products.json", "r") as file:
                data = json.load(file)

            if not self.product_barcode in data:
                messagebox.showerror("Error", "Couldn't find product in storage with that ID\nError Code" + invalid)
                return
            
            product_name = data[self.product_barcode]["name"]
            product_cost = data[self.product_barcode]["cost"]
            product_available = data[self.product_barcode]["available"]

            self.ProductsTable.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def Clock(self):
        # Setting the format
        time_ampm = time.strftime("%I:%M %p")
        time_24h = time.strftime("%H:%M")

        # Changing the text and recalling this function after 1 second
        if time_format == 1:
            self.ClockL.configure(text=time_ampm)
        elif time_format == 0:
            self.ClockL.configure(text=time_24h)
            
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
            messagebox.showerror("Checkpoint", "Please provide a valid product ID.\nError Code " + invalid)
            return
        
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
        if not self.barcode in file_data:
            messagebox.showinfo("Product", "Product was not found in storage to remove.")
            return
        # Removing the whole `barcode` product
        del file_data[self.barcode]

        with open("products.json", "w") as file:
            json.dump(file_data, file)

        messagebox.showinfo("Product", "Product was removed from storage.")

    def Clock(self):
        # Setting the format
        time_ampm = time.strftime("%I:%M %p")
        time_24h = time.strftime("%H:%M")

        # Changing the text and recalling this function after 1 second
        if time_format == 1:
            self.ClockL.configure(text=time_ampm)
        elif time_format == 0:
            self.ClockL.configure(text=time_24h)
            
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
            messagebox.showerror("Checkpoint", "Please provide a valid product ID.\nError Code" + invalid)
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
            messagebox.showerror("Error", "Use only numbers in cost and availability.\nError Code" + invalid)
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
            messagebox.showerror("Error", "An error occurred while opening file products.json\nError Code" + error)

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
            messagebox.showerror("Invalid Product Info", f"Product was not added, invalid product information. \nError Code " + invalid)

        self.application.destroy()

    def Clock(self):
        # Setting the format
        time_ampm = time.strftime("%I:%M %p")
        time_24h = time.strftime("%H:%M")

        # Changing the text and recalling this function after 1 second
        if time_format == 1:
            self.ClockL.configure(text=time_ampm)
        elif time_format == 0:
            self.ClockL.configure(text=time_24h)
            
        self.ClockL.after(1000, self.Clock)
 """

# Start of the project
if __name__ == "__main__":
    Main()