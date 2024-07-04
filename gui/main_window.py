from tkinter import Frame
from gui.grade_calculator import GradeCalculatorFrame
from gui.user_login import LoginFrame
from gui.menu import CustomButtonFrame

class MainWindow:
    def __init__(self, root):
        # Store the root window instance
        self.root = root
        # Set the title of the main window
        self.root.title("ScholarSerpent")
        # Set main window geometry 
        self.root.geometry('885x500')

        self.frames = {}
        self.init_frames()

    def init_frames(self):
        self.frames["LoginFrame"] = LoginFrame(self.root, self)
        self.frames["LoginFrame"].place(relwidth=1, relheight=1)
        self.frames["CustomButtonFrame"] = CustomButtonFrame(self.root, self)
        self.frames["CustomButtonFrame"].place(relwidth=1, relheight=1)
        self.frames["GradeCalculatorFrame"] = GradeCalculatorFrame(self.root, self)
        self.frames["GradeCalculatorFrame"].place(relwidth=1, relheight=1)

        self.show_frame("LoginFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
