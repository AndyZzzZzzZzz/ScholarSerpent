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

        # Frame dimensions
        frame_width = 865
        frame_height = 500
        num_buttons = 3
        button_width = 180  # Set a fixed width for buttons
        button_height = 50
        padding = 10

        total_button_width = (button_width + padding) * num_buttons - padding
        x_offset = (frame_width - total_button_width) // 2
        y_position = (frame_height - button_height) // 2

        buttons = [
            ("Performance Calculator", lambda: self.controller.show_frame("GradeCalculatorFrame")),
            ("History", lambda: print("History clicked")),
            ("Analysis and Report", lambda: print("Analysis and Report clicked"))
        ]

        for idx, (text, command) in enumerate(buttons):
            button = ttk.Button(self, text=text, bootstyle="primary, outline", command=command)
            button.place(x=x_offset + (button_width + padding) * idx, y=y_position, width=button_width, height=button_height)
