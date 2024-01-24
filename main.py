import os
import customtkinter
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import tkinter
import json
import time
from CTkTable import *
import atexit
import threading

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

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.application, height=100,
                                                   corner_radius=0)
        self.header_frame.pack(fill="x")

        self.product_list_frame = customtkinter.CTkScrollableFrame(self.application)
        self.product_list_frame.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)

        # Buying treeview
        self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ],
                                      font=("calibri", 20))
        self.products_list.pack(fill=tkinter.X)

        # Barcode input
        self.barcode_input = customtkinter.CTkEntry(self.application, placeholder_text="Enter barcode",
                                                    corner_radius=0,
                                                    font=("calibri", 22), width=270, height=40)
        self.barcode_input.pack(pady=(0, 15))

        # Buttons
        self.add_button = customtkinter.CTkButton(
            self.application, text="Add Product", font=("calibri", 18),
            width=250, height=35, corner_radius=2, command=self.AddProduct
        )
        self.add_button.pack(pady=(0, 4))

        self.checkin_button = customtkinter.CTkButton(
            self.application, text="Check in", font=("calibri", 18),
            width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2, command=self.Checkin
        )
        self.checkin_button.pack(pady=(0, 4))

        self.clear_button = customtkinter.CTkButton(
            self.application, text="Clear", font=("calibri", 18),
            width=250, height=35, fg_color="#AB2525", hover_color="#942020", corner_radius=2, command=self.Clear
        )
        self.clear_button.pack(pady=(0, 15))

        # Time
        self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                  font=("calibri", 28))
        self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Storage Management Buttons
        self.add_product = customtkinter.CTkButton(self.header_frame, text="Add Product", corner_radius=0,
                                                   fg_color="#47A641", hover_color="#3E9338",
                                                   command=lambda: threading.Thread(target=Add_Product()).start())
        self.add_product.pack(side="left", padx=(10, 0))

        self.remove_product = customtkinter.CTkButton(self.header_frame, text="Remove Product", corner_radius=2,
                                                      fg_color="#D94B4B", hover_color="#B23D3D",
                                                      command=lambda: threading.Thread(target=Remove_Product()).start())
        self.remove_product.pack(side="left", padx=(10, 0))

        self.view_product = customtkinter.CTkButton(self.header_frame, text="View Products", corner_radius=2, command=lambda: threading.Thread(target=View_Products()).start())
        self.view_product.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.clock()

        self.barcode_input.bind("<Return>", self.AddProduct)
        self.application.protocol("WM_DELETE_WINDOW", self.ClearList)
        atexit.register(self.ClearList)

        # Application rendering loop
        self.application.mainloop()

    def Checkin(self):
        if self.total_cost > 0:
            messagebox.showinfo("Check in", f"The total cost for every product is €{self.total_cost} \nThank you!")

            # Reset the runtime back to available when closing the window
            data = None
            with open("products.json", "r") as file:
                data = json.load(file)
                for product_data in data.values():
                    product_data["available"] -= self.amount
                    product_data["runtime"] = product_data["available"]

            with open("products.json", "w") as file:
                json.dump(data, file)

            self.products_list.destroy()
            self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ],
                                          font=("calibri", 20))
            self.products_list.pack(fill=tkinter.X)

            self.barcode_input.delete(0, tkinter.END)
            self.barcode_input.focus_set()
        else:
            messagebox.showinfo("Error", "Couldn't checkout. \nNo products to buy!")

    def Clear(self):
        if self.total_cost > 0:
            # Reset the runtime back to available when closing the window
            data = None
            with open("products.json", "r") as file:
                data = json.load(file)
                for product_data in data.values():
                    product_data["available"] -= self.amount
                    product_data["runtime"] = product_data["available"]

            with open("products.json", "w") as file:
                json.dump(data, file)

            self.products_list.destroy()
            self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ],
                                          font=("calibri", 20))
            self.products_list.pack(fill=tkinter.X)

            self.barcode_input.delete(0, tkinter.END)
            self.barcode_input.focus_set()
        else:
            messagebox.showinfo("Error", "Couldn't clear. \nNo products to clear!")

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
                    self.amount = simpledialog.askinteger("Amount", "How many products?")

                    if self.amount > 0:
                        runtime = data[barcode].get("runtime", 0)  # Get the current runtime or default to 0
                        if runtime >= self.amount:
                            data[barcode]["runtime"] -= self.amount

                            product = data[barcode]["name"]
                            cost = data[barcode]["cost"]

                            self.total_cost += data[barcode]["cost"] * self.amount
                            self.products_list.add_row(values=[f"{self.amount}", f"{product}", f"{cost * self.amount}"])

                            # Update runtime in the file
                            with open("products.json", "w") as file:
                                json.dump(data, file)

                        else:
                            messagebox.showerror("Error", "Insufficient products in the storage.")
                    else:
                        messagebox.showerror("Error", "Invalid product amount")
                else:
                    messagebox.showerror("Error", f"Product with barcode {barcode} not found in storage.")
            else:
                messagebox.showerror("Error", "No products.json file found.")
        else:
            messagebox.showerror("Error", "Please use a valid product ID.")

    def ClearList(self):
        # Reset the runtime back to available when closing the window
        data = None
        with open("products.json", "r") as file:
            data = json.load(file)
            for product_data in data.values():
                product_data["runtime"] = product_data["available"]

        with open("products.json", "w") as file:
            json.dump(data, file)

        # Close the window
        self.application.destroy()

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_time.configure(text=current_time)
        self.header_time.after(1000, self.clock)


class View_Products:
    def __init__(self):
        self.product_barcode = None

        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")

        self.application.geometry("1050x600")

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.application, height=100,
                                                   corner_radius=0)
        self.header_frame.pack(fill="x")

        self.product_list_frame = customtkinter.CTkScrollableFrame(self.application)
        self.product_list_frame.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)

        # Buying treeview
        self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Product", "Cost", "Available"], ],
                                      font=("calibri", 20))
        self.products_list.pack(fill=tkinter.X)

        # Time
        self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                  font=("calibri", 28))
        self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Storage Management
        self.scan_barcode = customtkinter.CTkButton(self.header_frame, text="Scan barcode", corner_radius=0,
                                                    fg_color="#47A641", hover_color="#3E9338",
                                                    command=lambda: threading.Thread(target=self.BarcodeScan()).start())
        self.scan_barcode.pack(side="left", padx=(10, 0))

        self.remove_product = customtkinter.CTkButton(self.header_frame, text="Remove All Product", corner_radius=2,
                                                      fg_color="#D94B4B", hover_color="#B23D3D",
                                                      command=self.RemoveAll)
        self.remove_product.pack(side="left", padx=(10, 0))

        self.refresh_products = customtkinter.CTkButton(self.header_frame, text="Refresh Products", corner_radius=2, command=lambda: threading.Thread(target=self.Refresh()).start())
        self.refresh_products.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.clock()
        self.AddProducts()

        # Application rendering loop
        self.application.mainloop()

    def RemoveAll(self):
        verification = messagebox.askyesno("Continue", "Are you sure removing every product?")

        if verification:
            os.remove("products.json")

            open("products.json", "x")
            with open("products.json", "w") as file:
                file.write("{}")

            self.application.destroy()
            messagebox.showinfo("Success", "Removed every product in storage.")
        else:
            messagebox.showinfo("Unsuccessful", "Canceled the operation.")

    def AddProducts(self):
        data = None

        if os.path.isfile("products.json"):
            with open("products.json", "r") as file:
                data = json.load(file)

            for barcode, product_data in data.items():
                product_name = product_data.get("name", "")
                product_cost = product_data.get("cost", "")
                product_available = product_data.get("available", "")

                self.products_list.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def BarcodeScan(self):
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
            self.root, text="Continue", font=("calibri", 18), command=self.Checkpoint_To_Scan,
            width=250, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2
        )
        self.continue_button.pack(pady=(0, 4))

        self.product_id.bind("<Return>", self.Checkpoint_To_Scan)

        # Time
        self.header_clock = customtkinter.CTkLabel(self.header_frame, text="0:00", font=("calibri", 28))
        self.header_clock.pack(side="right", pady=(12, 12), padx=(0, 15))

        self.clock()

        self.root.mainloop()

    def Checkpoint_To_Scan(self, event=None):
        self.product_barcode = self.product_id.get()

        if len(self.product_barcode) > 0:
            self.Scan_Refresh()
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid barcode")

    def Scan_Refresh(self):
        self.products_list.destroy()
        self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ],
                                      font=("calibri", 20))
        self.products_list.pack(fill=tkinter.X)

        if os.path.isfile("products.json"):
            with open("products.json", "r") as file:
                data = json.load(file)

            if self.product_barcode in data:
                product_name = data[self.product_barcode]["name"]
                product_cost = data[self.product_barcode]["cost"]
                product_available = data[self.product_barcode]["available"]

                self.products_list.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def Refresh(self):
        self.products_list.destroy()
        self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=[["Amount", "Product", "Cost"], ],
                                      font=("calibri", 20))
        self.products_list.pack(fill=tkinter.X)

        data = None

        if os.path.isfile("products.json"):
            with open("products.json", "r") as file:
                data = json.load(file)

            for barcode, product_data in data.items():
                product_name = product_data.get("name", "")
                product_cost = product_data.get("cost", "")
                product_available = product_data.get("available", "")

                self.products_list.add_row(values=[f"{product_name}", f"{product_cost}", f"{product_available}"])

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_time.configure(text=current_time)
        self.header_time.after(1000, self.clock)


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

    def AddProduct(self):
        product_name = self.product_name.get()
        product_cost = self.product_cost.get()
        product_available = self.product_available.get()

        data = None

        try:
            float(product_cost)
            int(product_available)
        except ValueError:
            messagebox.showerror("Error", "Use only numbers in cost and availability.")
            return  # Exit the function if there's an error

        product_data = {
            self.barcode: {
                "name": product_name,
                "cost": float(product_cost),
                "available": int(product_available),
                "runtime": int(product_available)
            }
        }

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
        current_time = time.strftime("%I:%M %p")

        self.header_clock.configure(text=current_time)
        self.header_clock.after(1000, self.Clock)


main_thread = threading.Thread(target=lambda: Main())
main_thread.start()
