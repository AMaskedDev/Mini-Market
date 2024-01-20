import tkinter
import customtkinter
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from tkinter import *
import json
import time
from CTkTable import *

customtkinter.set_appearance_mode("light")
class Main:
    def __init__(self):
        # Initializing the base window
        self.application = customtkinter.CTk()
        self.application.title("Mini Market")

        self.application.geometry("1050x600")
        self.application.resizable(False, False)

        # Header toolbar
        # self.header = tkinter.Menu(self.application)

        # self.storage_tools = tkinter.Menu(self.header, tearoff=0)
        # self.dangerous_tools = tkinter.Menu(self.header, tearoff=0)
        # self.help_menu = tkinter.Menu(self.header, tearoff=0)

        ## Adding commands to the storage tools
        # self.storage_tools.add_command(label="Add storage product")
        # self.storage_tools.add_command(label="Remove storage product")
        # self.storage_tools.add_command(label="View storage products")

        ## Adding commands to the dangerous tools
        # self.dangerous_tools.add_command(label="Remove all products")

        ## Adding commands to the help menu
        # self.help_menu.add_command(label="How to add new products")
        # self.help_menu.add_command(label="How to remove products")
        # self.help_menu.add_command(label="How to view all products")

        ## Creating the 'rendering' for the toolbar
        # self.header.add_cascade(label="Storage Management", menu=self.storage_tools)
        # self.header.add_cascade(label="Dangerous Tools", menu=self.dangerous_tools)
        # self.header.add_cascade(label="Help", menu=self.help_menu)

        # self.application.config(menu=self.header)

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self.application, height=100,
                                                   corner_radius=0)
        self.header_frame.pack(fill="x")

        # Buying treeview
        self.products_list = CTkTable(self.application,row=5,column=3,values=(["Amount","Product","Cost"],),font=("calibri",20))
        self.products_list.pack(pady=(25, 15), padx=(15, 15), fill=tkinter.BOTH, expand=True)
        # Barcode input
        self.barcode_input = customtkinter.CTkEntry(self.application, font=("calibri", 22), width=250)
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
                                                   text_color='#7D7D7D', font=("calibri", 28))
        self.header_time.pack(side="right", pady=(12, 12), padx=(0, 15))

        # Storage Management Buttons
        self.add_product = customtkinter.CTkButton(self.header_frame, text="Add Product", corner_radius=0,
                                                   fg_color="#47A641", hover_color="#3E9338")
        self.add_product.pack(side="left", padx=(10, 0))

        self.remove_product = customtkinter.CTkButton(self.header_frame, text="Remove Product", corner_radius=2,
                                                      fg_color="#D94B4B", hover_color="#B23D3D")
        self.remove_product.pack(side="left", padx=(10, 0))

        self.view_product = customtkinter.CTkButton(self.header_frame, text="View Products", corner_radius=2,)
        self.view_product.pack(side="left", padx=(10, 0))

        # Starting other methods
        self.clock()
        

        #self.dark_mode_toggle()
        # Application rendering loop
        self.application.mainloop()

    def add_product(self):
        pass

    def clock(self):
        current_time = time.strftime("%I:%M %p")

        self.header_time.configure(text=current_time)
        self.header_time.after(1000, self.clock)
    





Main()
