import os
import tkinter
import customtkinter
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from tkinter import *
import json
import time
from CTkTable import *

customtkinter.set_appearance_mode("dark")


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
                                                   fg_color="#47A641", hover_color="#3E9338")
        self.add_product.pack(side="left", padx=(10, 0))

        self.remove_product = customtkinter.CTkButton(self.header_frame, text="Remove Product", corner_radius=2,
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


class Add_Product:
    def __init__(self):
        # Variables

        # Functions
        self.BarcodeGUI()

    def BarcodeGUI(self):
        self.root = customtkinter.CTk()
        self.root.geometry("500x350")
        self.root.title("Product Scanning")
        self.root.resizable(False, False)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.root, height=100, corner_radius=0)
        self.header_frame.pack(fill="x")

        # Time
        self.header_clock = customtkinter.CTkLabel(self.header_frame, text="0:00", font=("calibri", 28))
        self.header_clock.pack(side="right", pady=(12, 12), padx=(0, 15))

        self.root.mainloop()

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_clock.configure(text=current_time)
        self.header_clock.after(1000, self.clock)


Main()
