from pathlib import Path
from tkinter import Frame, Label, Entry, Button, messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from database import Database
import os
import sys
import hashlib

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class LoginFrame(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.database = Database()
        self.init_ui()

    def init_ui(self):
        # Main container frame using grid for responsive layout
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")

        # Configure grid to expand with window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Top frame for logo and welcome message
        top_frame = ttk.Frame(container, padding=20)
        top_frame.grid(row=0, column=0, sticky="n", pady=(20, 10))

        # User Icon
        img = Image.open(resource_path("image/incognito.png"))  # Replace with the path to your icon image
        resize = img.resize((64, 64), Image.LANCZOS)
        new_img = ImageTk.PhotoImage(resize)
        self.user_icon = Label(top_frame, image=new_img)
        self.user_icon.image = new_img  # Keep a reference to avoid garbage collection
        self.user_icon.pack()

        # Welcome Message
        welcome_label = ttk.Label(top_frame, text="Welcome to ScholarSerpent", font=('Helvetica', 24))
        welcome_label.pack(pady=(10, 20))

        # Middle frame for user inputs and labels
        input_frame = ttk.Labelframe(container, text="Login Information", padding=20)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_rowconfigure(1, weight=1)

        # Configure input_frame to expand with window
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        # User ID
        email_label = ttk.Label(input_frame, text="User ID", font=('Helvetica', 18))
        email_label.grid(row=0, column=0, sticky="w", pady=(5, 5))
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=20, sticky="ew")
        self.email_entry.insert(0, "Enter your User ID")

        # Password
        password_label = ttk.Label(input_frame, text="Password", font=('Helvetica', 18))
        password_label.grid(row=1, column=0, sticky="w", pady=(5, 5))
        self.password_entry = ttk.Entry(input_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=20, sticky="ew")
        self.password_entry.insert(0, "Enter your Password")

        # Forgot Password
        forgot_password = ttk.Button(input_frame, text="Forgot Password?", style="Link.TButton", command=self.forgot_password)
        forgot_password.grid(row=2, column=1, sticky="e", pady=(10, 5))

        # Bottom frame for buttons
        bottom_frame = ttk.Frame(container, padding=20)
        bottom_frame.grid(row=2, column=0, sticky="s")
        container.grid_rowconfigure(2, weight=1)

        # Login Button
        login_button = ttk.Button(bottom_frame, text="LOGIN", style="CustomOutline.TButton", command=self.login_user)
        login_button.pack(side="left", padx=10)

        # Register Button
        register_button = ttk.Button(bottom_frame, text="REGISTER", style="CustomOutline.TButton", command=self.register_user)
        register_button.pack(side="right", padx=10)


    def register_user(self):
        userID = self.email_entry.get().strip()
        userPassword = self.password_entry.get().strip()

        if userID == "Enter your User ID" or not userID:
            messagebox.showerror("Input Error", "Please enter a valid User ID")
            return

        if userPassword == "Enter your Password" or not userPassword:
            messagebox.showerror("Input Error", "Please enter a valid Password")
            return

        user = self.database.get_user(userID)
        if user:
            messagebox.showerror("Registration Failed", "User ID already exists.")
        else:
            # Hash the password before sending it to the database
            hashed_password = hashlib.sha256(userPassword.encode()).hexdigest()
            self.database.insert_user(userID, hashed_password)
            messagebox.showinfo("Registration Success", "You have successfully registered!")


    def login_user(self):
        userID = self.email_entry.get().strip()
        userPassword = self.password_entry.get().strip()


        if userID == "Enter your User ID" or not userID:
            messagebox.showerror("Input Error", "Please enter your User ID")
            return

        if userPassword == "Enter your Password" or not userPassword:
            messagebox.showerror("Input Error", "Please enter your Password")
            return

        user = self.database.get_user(userID)
        if user:
            hashed_password = hashlib.sha256(userPassword.encode()).hexdigest()
            
            if user[1] == hashed_password:
                messagebox.showinfo("Login Success", "Welcome back!")
                self.controller.current_user = userID
                self.controller.show_frame("CustomButtonFrame")
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "User ID not found.")




    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Password recovery functionality to be implemented.")
