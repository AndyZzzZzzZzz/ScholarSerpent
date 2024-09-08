# Import necessary modules for UI, hashing, and database interactions
from pathlib import Path
from tkinter import Frame, Label, messagebox, Toplevel  # Basic Tkinter components
import ttkbootstrap as ttk  # Themed widgets from ttkbootstrap
from PIL import Image, ImageTk  # Image handling from PIL
from database.database import Database  # Custom database module
import os
import sys
import hashlib  # For password hashing

class PasswordResetDialog(Toplevel):
    """
    A dialog window for resetting the user password. 
    This window allows users to enter and confirm a new password, which is hashed and returned to the caller.
    """

    def __init__(self, parent, userID):
        """
        Initialize the password reset dialog window.
        
        :param parent: The parent window (usually the login frame).
        :param userID: The ID of the user requesting a password reset.
        """
        super().__init__(parent)
        self.userID = userID  # Store the userID for password reset
        self.title("Reset Password")  # Set window title

        # Calculate window size as 40% of the screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.4)
        self.geometry(f'{window_width}x{window_height}')

        # Center the window on the screen
        position_right = int(self.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.winfo_screenheight()/2 - window_height/2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.configure(bg='#2c3e50')  # Set background to match the theme

        # New Password Entry
        Label(self, text="Enter your new password:", font=('Helvetica', 14), bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
        self.new_password_entry = ttk.Entry(self, show="*")
        self.new_password_entry.pack(pady=10, padx=20, fill='x')

        # Confirm Password Entry
        Label(self, text="Confirm your new password:", font=('Helvetica', 14), bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
        self.confirm_password_entry = ttk.Entry(self, show="*")
        self.confirm_password_entry.pack(pady=10, padx=20, fill='x')

        # Buttons for confirm and cancel actions
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10, fill='x')

        confirm_button = ttk.Button(buttons_frame, text="Confirm", command=self.confirm)
        confirm_button.pack(side='left', padx=(20, 10))

        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side='right', padx=(10, 20))

        self.result = None  # Store the result (hashed password) after confirmation

    def confirm(self):
        """
        Confirm the password reset by checking if both password entries match.
        If they match, the password is hashed and stored.
        """
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password and new_password == confirm_password:
            # Hash the password using SHA-256
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.result = hashed_password  # Store the hashed password as the result
            self.destroy()  # Close the dialog
        else:
            messagebox.showerror("Error", "Passwords do not match or reset was cancelled.")

    def cancel(self):
        """
        Cancel the password reset operation and close the dialog.
        """
        self.result = None
        self.destroy()

def resource_path(relative_path):
    """
    Get the absolute path to resource, works for development and for bundled executables (PyInstaller).
    
    :param relative_path: The relative path to the resource.
    :return: The absolute path to the resource.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder path
    except Exception:
        base_path = os.path.abspath(".")  # Current directory path for development
    return os.path.join(base_path, relative_path)

class LoginFrame(Frame):
    """
    LoginFrame class to handle user login, registration, and password reset operations.
    It displays input fields for User ID and Password, and buttons for login, registration, and password reset.
    """

    def __init__(self, master=None, controller=None, **kwargs):
        """
        Initialize the login frame.
        
        :param master: The parent Tkinter widget (usually the root window).
        :param controller: The main controller (MainWindow) to switch between frames.
        """
        super().__init__(master, **kwargs)
        self.controller = controller  # Store controller for frame management
        self.database = Database()  # Instantiate the database class to manage user data
        self.init_ui()  # Initialize the UI components

    def init_ui(self):
        """
        Set up the user interface, including User ID and Password input fields, and buttons for login, 
        registration, and password reset.
        """
        # Main container frame with grid layout for responsive design
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout for responsive resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Top frame for logo and welcome message
        top_frame = ttk.Frame(container, padding=20)
        top_frame.grid(row=0, column=0, sticky="n", pady=(20, 10))

        # User icon (logo) in the top frame
        img = Image.open(resource_path("image/incognito.png"))  # Replace with the correct path to your icon image
        resize = img.resize((64, 64), Image.LANCZOS)
        new_img = ImageTk.PhotoImage(resize)
        self.user_icon = Label(top_frame, image=new_img)
        self.user_icon.image = new_img  # Keep a reference to avoid garbage collection
        self.user_icon.pack()

        # Welcome message
        welcome_label = ttk.Label(top_frame, text="Welcome to ScholarSerpent", font=('Helvetica', 24))
        welcome_label.pack(pady=(10, 20))

        # Middle frame for user inputs (User ID and Password)
        input_frame = ttk.Labelframe(container, text="Login Information", padding=20)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # User ID label and entry field
        email_label = ttk.Label(input_frame, text="User ID", font=('Helvetica', 18))
        email_label.grid(row=0, column=0, sticky="w", pady=(5, 5))
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=20, sticky="ew")
        self.email_entry.insert(0, "Enter your User ID")

        # Password label and entry field
        password_label = ttk.Label(input_frame, text="Password", font=('Helvetica', 18))
        password_label.grid(row=1, column=0, sticky="w", pady=(5, 5))
        self.password_entry = ttk.Entry(input_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=20, sticky="ew")
        self.password_entry.insert(0, "Enter your Password")

        # Forgot password link
        forgot_password = ttk.Button(input_frame, text="Forgot Password?", style="Link.TButton", command=self.forgot_password)
        forgot_password.grid(row=2, column=1, sticky="e", pady=(10, 5))

        # Bottom frame for login and register buttons
        bottom_frame = ttk.Frame(container, padding=20)
        bottom_frame.grid(row=2, column=0, sticky="s")

        # Login button
        login_button = ttk.Button(bottom_frame, text="LOGIN", style="CustomOutline.TButton", command=self.login_user)
        login_button.pack(side="left", padx=10)

        # Register button
        register_button = ttk.Button(bottom_frame, text="REGISTER", style="CustomOutline.TButton", command=self.register_user)
        register_button.pack(side="right", padx=10)

    def register_user(self):
        """
        Register a new user. The user ID and password are validated, and the password is hashed before being stored.
        """
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
            # Hash the password before saving it in the database
            hashed_password = hashlib.sha256(userPassword.encode()).hexdigest()
            self.database.insert_user(userID, hashed_password)
            messagebox.showinfo("Registration Success", "You have successfully registered!")

    def login_user(self):
        """
        Log in an existing user. The entered password is hashed and compared with the stored hash in the database.
        """
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
        """
        Handle the "Forgot Password" flow by opening a password reset dialog.
        """
        userID = self.email_entry.get().strip()

        if userID == "Enter your User ID" or not userID:
            messagebox.showerror("Input Error", "Please enter your User ID")
            return

        user = self.database.get_user(userID)
        if user:
            self.reset_password_dialog(userID)
        else:
            messagebox.showerror("Reset Failed", "User ID not found.")

    def reset_password_dialog(self, userID):
        """
        Open the PasswordResetDialog for the user to reset their password.
        """
        dialog = PasswordResetDialog(self.master, userID)
        self.master.wait_window(dialog)  # Wait for the dialog window to close
        
        if dialog.result:
            self.database.update_user_password(userID, dialog.result)
            messagebox.showinfo("Password Reset", "Your password has been successfully reset.")
