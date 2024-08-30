from tkinter import Frame
from ttkbootstrap.constants import *
import ttkbootstrap as ttk

class CustomButtonFrame(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.configure()

        # Create a container frame to center the buttons vertically and horizontally
        container = Frame(self)
        container.pack(expand=True, fill="both")

        # Define buttons with their respective commands
        buttons = [
            ("Grade Calculator", lambda: self.controller.show_frame("GradeCalculatorFrame")),
            ("Calculate History", lambda: print("Calculate History clicked")),
            ("Performance Analysis", lambda: print("Performance Analysis clicked")),
            ("Login", lambda: print("Login clicked")),
            ("Chat Bot", lambda: print("Chat Bot clicked")),
            ("Official Links", lambda: print("Official Links clicked"))
        ]

        # Create a frame for the top row of buttons
        top_frame = Frame(container)
        top_frame.pack(expand=True, fill="x", padx=20, pady=20)  # Ensure the top frame expands to fill available space

        # Create a frame for the bottom row of buttons
        bottom_frame = Frame(container)
        bottom_frame.pack(expand=True, fill="x", padx=20, pady=20)  # Ensure the bottom frame expands to fill available space

        # Add buttons to the top row
        for i in range(3):
            button = ttk.Button(top_frame, text=buttons[i][0], style="CustomM.TButton", command=buttons[i][1])
            button.grid(row=0, column=i, padx=20, pady=10, sticky="ew")

        # Add buttons to the bottom row
        for i in range(3, 6):
            button = ttk.Button(bottom_frame, text=buttons[i][0], style="CustomM.TButton", command=buttons[i][1])
            button.grid(row=0, column=i-3, padx=20, pady=10, sticky="ew")

        # Expand the columns equally to make buttons fill the space evenly
        for i in range(3):
            top_frame.grid_columnconfigure(i, weight=1)
            bottom_frame.grid_columnconfigure(i, weight=1)
