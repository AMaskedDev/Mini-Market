import os
import tkinter
import customtkinter
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from tkinter import *
import json
import time
from CTkTable import *

customtkinter.set_appearance_mode("dark")

if os.path.isfile("products.json"):
    pass
else:
    file_create = open("products.json", "x")

    with open("products.json", "w") as file:
        file.write("{}")
        file.close()


class Add_Storage():
    def __init__(self):
        self.barcode = None
        self.enter_product_id()

        self.product_exists = False

    def enter_product_id(self):
        # Initializing the base window
        self.root = customtkinter.CTk()
        self.root.title("Enter product ID")

        self.root.geometry("450x250")
        self.root.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.root, height=100,
                                                   corner_radius=0)
        self.header_frame.pack(fill="x")

        # Barcode input
        self.barcode_input = customtkinter.CTkEntry(self.root, placeholder_text="Scan barcode",
                                                    corner_radius=0,
                                                    font=("calibri", 22), width=270, height=40)
        self.barcode_input.pack(pady=(50, 5))

        # Button
        self.continue_button = customtkinter.CTkButton(
            self.root, text="Continue", font=("calibri", 18),
            width=175, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2, command=self.check_barcode
        )
        self.continue_button.pack(pady=(0, 4))

        # Time
        self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                  text_color='#7D7D7D', font=("calibri", 28))
        self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Starting other methods
        self.clock()

        self.barcode_input.bind("<Return>", self.check_barcode)

        # Application rendering loop
        self.root.mainloop()

    def check_barcode(self, event=None):
        self.barcode = self.barcode_input.get()

        if len(self.barcode) > 0:

            with open("products.json", "r") as file:
                data = json.load(file)

            if self.barcode in data:
                self.product_exists = True

            else:
                self.product_exists = False

            self.root.destroy()
            self.add_product()
        else:
            messagebox.showerror("Error", "Please enter a valid product id.")

    def add_product(self):
        if self.product_exists:
            # Initializing the base window
            self.application = customtkinter.CTk()
            self.application.title("Edit product")

            self.application.geometry("450x300")
            self.application.resizable(False, False)

            # Header Frame
            self.header_frame = customtkinter.CTkFrame(self.application, height=100,

                                                       corner_radius=0)
            self.header_frame.pack(fill="x")

            # Product Information
            self.product_name = customtkinter.CTkEntry(self.application, placeholder_text="Edited product name",
                                                       corner_radius=0,
                                                       font=("calibri", 22), width=270,
                                                       height=40)
            self.product_name.pack(pady=(5, 0))

            self.product_cost = customtkinter.CTkEntry(self.application, placeholder_text="Edited product cost",
                                                       corner_radius=0,
                                                       font=("calibri", 22), width=270,
                                                       height=40)
            self.product_cost.pack(pady=(5, 0))

            self.product_available = customtkinter.CTkEntry(self.application,
                                                            placeholder_text="Edited products available",
                                                            corner_radius=0,

                                                            font=("calibri", 22), width=270,
                                                            height=40)
            self.product_available.pack(pady=(5, 0))

            # Button
            self.add_product_button = customtkinter.CTkButton(
                self.application, text="Edit product", font=("calibri", 18),
                width=175, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2,
                command=self.save_new_product
            )
            self.add_product_button.pack(pady=(15, 4))

            # Time
            self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                      text_color='#7D7D7D', font=("calibri", 28))
            self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

            # Starting other methods
            self.clock()

            # Application rendering loop
            self.application.mainloop()
        else:
            # Initializing the base window
            self.application = customtkinter.CTk()
            self.application.title("Create new product")

            self.application.geometry("450x300")
            self.application.resizable(False, False)

            # Header Frame
            self.header_frame = customtkinter.CTkFrame(self.application, height=100,

                                                       corner_radius=0)
            self.header_frame.pack(fill="x")

            # Product Information
            self.product_name = customtkinter.CTkEntry(self.application, placeholder_text="New product name",
                                                       corner_radius=0,
                                                       font=("calibri", 22), width=270, height=40)
            self.product_name.pack(pady=(5, 0))

            self.product_cost = customtkinter.CTkEntry(self.application, placeholder_text="New product cost",
                                                       corner_radius=0,
                                                       font=("calibri", 22), width=270, height=40)
            self.product_cost.pack(pady=(5, 0))

            self.product_available = customtkinter.CTkEntry(self.application, placeholder_text="New products available",
                                                            corner_radius=0,
                                                            font=("calibri", 22), width=270,
                                                            height=40)
            self.product_available.pack(pady=(5, 0))

            # Button
            self.add_product_button = customtkinter.CTkButton(
                self.application, text="Add product", font=("calibri", 18),
                width=175, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2,
                command=self.save_new_product
            )
            self.add_product_button.pack(pady=(15, 4))

            # Time
            self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                      text_color='#7D7D7D', font=("calibri", 28))
            self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

            # Starting other methods
            self.clock()

            # Application rendering loop
            self.application.mainloop()

    def save_new_product(self):
        product_name = self.product_name.get()
        product_cost = self.product_cost.get()
        product_available = self.product_available.get()

        try:
            float(product_cost)
            int(product_available)
        except ValueError:
            messagebox.showerror("Error", "Use only numbers in cost and availability.")
            return

        product_data = {
            "name": product_name,
            "cost": float(product_cost),
            "available": int(product_available),
            "runtime_available": int(product_available),
        }

        data = None

        with open("products.json", "r") as products_file:
            data = json.load(products_file)

        barcode = self.barcode if self.barcode else str(
            int(time.time()))  # Use a timestamp as a barcode if not provided

        with open("products.json", "w") as products_file:
            if barcode in data:
                # Product already exists, update it
                data[barcode].update(product_data)
                messagebox.showinfo("Product", "Product was edited in the storage.")
                if self.root:
                    try:
                        self.root.destroy()
                    except:
                        print("fuck you.")
            else:
                json.dump(data, products_file)
                messagebox.showinfo("Product", "Product was added to storage.")
                if self.root:
                    try:
                        self.root.destroy()
                    except:
                        print("fuck you.")


    def clock(self):
        current_time = time.strftime("%I:%M %p")

        if self.header_time:
            self.header_time.configure(text=current_time)
            self.header_time.after(1000, self.clock)


class Delete_Storage():
    def __init__(self):
        self.barcode = None
        self.enter_product_id()

        self.product_exists = False

    def enter_product_id(self):
        # Initializing the base window
        self.root = customtkinter.CTk()
        self.root.title("Enter product ID")

        self.root.geometry("450x250")
        self.root.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.root, height=100,
                                                   corner_radius=0)
        self.header_frame.pack(fill="x")

        # Barcode input
        self.barcode_input = customtkinter.CTkEntry(self.root, placeholder_text="Scan barcode",
                                                    corner_radius=0,
                                                    font=("calibri", 22), width=270, height=40)
        self.barcode_input.pack(pady=(50, 5))

        # Button
        self.continue_button = customtkinter.CTkButton(
            self.root, text="Continue", font=("calibri", 18),
            width=175, height=35, fg_color="#47A641", hover_color="#3E9338", corner_radius=2,
            command=self.delete_product
        )
        self.continue_button.pack(pady=(0, 4))

        # Time
        self.header_time = customtkinter.CTkLabel(self.header_frame, text="0:00",
                                                  text_color='#7D7D7D', font=("calibri", 28))
        self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Starting other methods
        self.clock()

        self.barcode_input.bind("<Return>", lambda event=None: self.delete_product())

        # Application rendering loop
        self.root.mainloop()

    def check_barcode(self, event=None):
        self.barcode = self.barcode_input.get()

        self.root.destroy()

        with open("products.json", "r") as file:
            data = json.load(file)

        if self.barcode in data:
            self.product_exists = True

        else:
            self.product_exists = False

        self.delete_product()

    def delete_product(self):
        self.barcode = self.barcode_input.get()
        if len(self.barcode) > 0:

            with open("products.json", "r") as products_file:
                data = json.load(products_file)

            if self.barcode in data:
                del data[self.barcode]
                messagebox.showinfo("Product", "Product was removed from the storage.")
                self.root.destroy()
            else:
                messagebox.showinfo("Product", "Product was not found in storage.")

            with open("products.json", "w") as products_file:
                json.dump(data, products_file)
        else:
            messagebox.showerror("Error", "Please input a product id.")

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        if self.header_time:
            self.header_time.configure(text=current_time)
            self.header_time.after(1000, self.clock)


class Main:
    def __init__(self):
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
        self.products_list = CTkTable(self.product_list_frame, row=0, column=0, values=(["Amount", "Product", "Cost"],),
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
                                                   command=lambda: Add_Storage())
        self.add_product.pack(side="left", padx=(10, 0))

        self.remove_product = customtkinter.CTkButton(self.header_frame, text="Remove Product", corner_radius=2,
                                                      command=lambda: Delete_Storage(),
                                                      fg_color="#D94B4B", hover_color="#B23D3D")
        self.remove_product.pack(side="left", padx=(10, 0))

        self.view_product = customtkinter.CTkButton(self.header_frame, text="View Products", corner_radius=2, )
        self.view_product.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.clock()

        # Application rendering loop
        self.application.mainloop()

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_time.configure(text=current_time)
        self.header_time.after(1000, self.clock)


Main()
