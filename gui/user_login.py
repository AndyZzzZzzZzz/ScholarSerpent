from tkinter import Frame, Label, Entry
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class LoginFrame(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.configure()

        # Main container frame
        container = ttk.Frame(self, bootstyle="dark", padding=20)
        container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)

        # User Icon
        img = Image.open("/Users/az/Desktop/Project/Grade-Calculator/incognito.png")  # Replace with the path to your icon image
        resize = img.resize((64, 64), Image.LANCZOS)
        new_img = ImageTk.PhotoImage(resize)
        self.user_icon = Label(container, image=new_img, bg="#1e1e2d")
        self.user_icon.image = new_img  # Keep a reference to avoid garbage collection
        self.user_icon.place(relx=0.5, rely=0.1, anchor='center')

        # Email ID
        email_label = ttk.Label(container, text="Email ID", bootstyle="light")
        email_label.place(relx=0.1, rely=0.25, anchor='w')
        self.email_entry = ttk.Entry(container, bootstyle="light")
        self.email_entry.place(relx=0.1, rely=0.3, relwidth=0.8, anchor='w')

        # Password
        password_label = ttk.Label(container, text="Password", bootstyle="light")
        password_label.place(relx=0.1, rely=0.4, anchor='w')
        self.password_entry = ttk.Entry(container, bootstyle="light", show="*")
        self.password_entry.place(relx=0.1, rely=0.45, relwidth=0.8, anchor='w')

        # Login Button
        login_button = ttk.Button(container, text="LOGIN", bootstyle="primary", command=self.login)
        login_button.place(relx=0.5, rely=0.6, anchor='center')

    def login(self):
        # Simulate login validation here (you can add your own logic)
        self.controller.show_frame("CustomButtonFrame")
