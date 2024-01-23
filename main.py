import os
import customtkinter
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from future.moves import tkinter
from future.moves import tkinter
import json
import time
from CTkTable import *

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
        self.total_cost = 0

        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")

        self.application.geometry("1050x600")
        self.application.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.application, height=100,
                                                   corner_radius=0)
        self.header_frame.pack(fill="x")

        self.product_list_frame = customtkinter.CTkScrollableFrame(self.application)
        self.product_list_frame.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)

        # Buying treeview
        self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"],],
                                      font=("calibri", 20))
        self.products_list.pack(fill=tkinter.X)

        # Barcode input
        self.barcode_input = customtkinter.CTkEntry(self.application, placeholder_text="Enter barcode",
                                                    corner_radius=0,
                                                    font=("calibri", 22), width=270, height=40)
        self.barcode_input.pack(pady=(0, 15))

        # Buttons
        self.checkin_button = customtkinter.CTkButton(
            self.application, text="Check in", font=("calibri", 18),
            width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2
        )
        self.checkin_button.pack(pady=(0, 4))

        self.clear_button = customtkinter.CTkButton(
            self.application, text="Clear order", font=("calibri", 18),
            fg_color="#D94B4B", hover_color="#B23D3D", width=250, height=35, corner_radius=2
        )
        self.clear_button.pack(pady=(0, 5))

        # Time
        self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                  font=("calibri", 28))
        self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Storage Management Buttons
        self.add_product = customtkinter.CTkButton(self.header_frame, text="Add Product", corner_radius=0,
                                                   fg_color="#47A641", hover_color="#3E9338",
                                                   command=lambda: Add_Product())
        self.add_product.pack(side="left", padx=(10, 0))

        self.remove_product = customtkinter.CTkButton(self.header_frame, text="Remove Product", corner_radius=2,
                                                      fg_color="#D94B4B", hover_color="#B23D3D",
                                                      command=lambda: Remove_Product())
        self.remove_product.pack(side="left", padx=(10, 0))

        self.view_product = customtkinter.CTkButton(self.header_frame, text="View Products", corner_radius=2)
        self.view_product.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.clock()
        self.barcode_input.bind("<Return>", self.AddProduct)

        # Application rendering loop
        self.application.mainloop()

    def AddProduct(self, event=None):
        # Temporary variables
        barcode = self.barcode_input.get()
        data = None

        # Visuals
        self.barcode_input.delete(0, tkinter.END)
        self.barcode_input.focus_set()

        # Adding to treeview

        if len(barcode) > 0:
            if os.path.isfile("products.json"):
                with open("products.json", "r") as file:
                    data = json.load(file)
                    file.close()

                if barcode in data:
                    amount = simpledialog.askinteger("Amount", "How many products?")

                    if amount > 0:
                        product = data[barcode]["name"]
                        cost = data[barcode]["cost"]

                        self.total_cost = data[barcode]["cost"] * amount
                        #value=([f"{amount}", f"{product}", f"{cost}"]
                        self.products_list.add_row(1, values=["Amount", "Product", "Cost"])

                    else:
                        messagebox.showerror("Error", "Invalid product amount")



        else:
            messagebox.showerror("Error", "Please use a valid product ID.")

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_time.configure(text=current_time)
        self.header_time.after(1000, self.clock)


class View_Products():
    def __init__(self):
        pass


class Remove_Product:
    def __init__(self):
        # Variables
        self.application = None
        self.barcode = None
        self.product_exists = False

        # Functions
        self.BarcodeGUI()

    def BarcodeGUI(self):
        self.root = customtkinter.CTk()
        self.root.geometry("500x250")
        self.root.title("Product Scanning")
        self.root.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.root, height=100, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(0, 30))
        #
        # Barcode input
        self.product_id = customtkinter.CTkEntry(self.root, placeholder_text="Product ID", font=("calibri", 20),
                                                 width=250, height=35)
        self.product_id.pack(pady=(10, 5))

        # Continue button
        self.continue_button = customtkinter.CTkButton(
            self.root, text="Continue", font=("calibri", 18), command=self.Checkpoint_To_Info,
            width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2
        )
        self.continue_button.pack(pady=(0, 4))

        self.product_id.bind("<Return>", self.Checkpoint_To_Info)

        # Time
        self.header_clock = customtkinter.CTkLabel(self.header_frame, text="0:00", font=("calibri", 28))
        self.header_clock.pack(side="right", pady=(12, 12), padx=(0, 15))

        self.Clock()

        self.root.mainloop()

    def Checkpoint_To_Info(self, event=None):
        self.barcode = self.product_id.get()

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

            # Displaying the info gui
            self.RemoveProduct()
            self.root.destroy()

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
        current_time = time.strftime("%I:%M %p")

        self.header_clock.configure(text=current_time)
        self.header_clock.after(1000, self.Clock)


class Add_Product:
    def __init__(self):
        # Variables
        self.application = None
        self.barcode = None
        self.product_exists = False

        # Functions
        self.BarcodeGUI()

    def BarcodeGUI(self):
        self.root = customtkinter.CTk()
        self.root.geometry("500x250")
        self.root.title("Product Scanning")
        self.root.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.root, height=100, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(0, 30))
        #
        # Barcode input
        self.product_id = customtkinter.CTkEntry(self.root, placeholder_text="Product ID", font=("calibri", 20),
                                                 width=250, height=35)
        self.product_id.pack(pady=(10, 5))

        # Continue button
        self.continue_button = customtkinter.CTkButton(
            self.root, text="Continue", font=("calibri", 18), command=self.Checkpoint_To_Info,
            width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2
        )
        self.continue_button.pack(pady=(0, 4))

        self.product_id.bind("<Return>", self.Checkpoint_To_Info)

        # Time
        self.header_clock = customtkinter.CTkLabel(self.header_frame, text="0:00", font=("calibri", 28))
        self.header_clock.pack(side="right", pady=(12, 12), padx=(0, 15))

        self.Clock()

        self.root.mainloop()

    def Checkpoint_To_Info(self, event=None):
        self.barcode = self.product_id.get()

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

            # Displaying the info gui
            self.root.destroy()
            self.InfoGUI()

    def InfoGUI(self):
        self.application = customtkinter.CTk()
        self.application.geometry("600x350")
        self.application.title("Product Scanning")
        self.application.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.application, height=100, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(0, 30))

        # Title
        if self.product_exists:
            self.title = customtkinter.CTkLabel(self.header_frame, text="Edit product", font=("calibri", 24))
        else:
            self.title = customtkinter.CTkLabel(self.header_frame, text="Add product", font=("calibri", 24))

        self.title.pack(side="left", padx=(10, 0))

        # Product info

        # Product name
        self.product_name = customtkinter.CTkEntry(self.application, placeholder_text="Product Name",
                                                   font=("calibri", 20),
                                                   width=250, height=35)
        self.product_name.pack(pady=(10, 5))

        # Product cost
        self.product_cost = customtkinter.CTkEntry(self.application, placeholder_text="Product Cost",
                                                   font=("calibri", 20),
                                                   width=250, height=35)
        self.product_cost.pack(pady=(10, 5))

        # Product available
        self.product_available = customtkinter.CTkEntry(self.application, placeholder_text="Product Available",
                                                        font=("calibri", 20),
                                                        width=250, height=35)
        self.product_available.pack(pady=(10, 30))

        # Continue button
        self.continue_button = customtkinter.CTkButton(
            self.application, text="Continue", font=("calibri", 18),
            width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2, command=self.AddProduct
        )
        self.continue_button.pack(pady=(0, 4))

        self.product_available.bind("<Return>", self.AddProduct)

        # Time
        self.header_clock = customtkinter.CTkLabel(self.header_frame, text="0:00", font=("calibri", 28))
        self.header_clock.pack(side="right", pady=(12, 12), padx=(0, 15))

        self.Clock()

        self.application.mainloop()

    def AddProduct(self, event=None):
        # Getting entries input
        product_name = self.product_name.get()
        product_cost = self.product_cost.get()
        product_available = self.product_available.get()

        # Temporary variables
        file_data = None
        product_data = {
            self.barcode: {
                "name": product_name,
                "cost": product_cost,
                "available": product_available,
                "runtime": product_available
            }
        }

        # Loading the json file to a temporary data variable
        with open("products.json", "r") as file:
            file_data = json.load(file)

        # Checking if the product exists
        if self.barcode in file_data:
            # Updating the `old` with the `new` info
            file_data[self.barcode].update(product_data)

            with open("products.json", "w") as file:
                json.dump(product_data, file)
                file.close()

            messagebox.showinfo("Product", "Product was edited to storage.")

        else:
            # Creating a new product
            with open("products.json", "w") as file:
                json.dump(product_data, file)
                file.close()

                messagebox.showinfo("Product", "New product was added to storage.")

        self.application.destroy()

    def Clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_clock.configure(text=current_time)
        self.header_clock.after(1000, self.Clock)


Main()
