# Import necessary modules from Tkinter and ttkbootstrap
from tkinter import Frame  # Basic Frame widget for organizing UI components
from ttkbootstrap.constants import *  # Import constants for ttkbootstrap styling
import ttkbootstrap as ttk  # ttkbootstrap for theming and styled widgets

class CustomButtonFrame(Frame):
    """
    CustomButtonFrame class responsible for displaying a menu of buttons to navigate between
    different sections of the application (e.g., Grade Calculator, Performance Analysis).
    The buttons are arranged in two rows, with functionality to switch between frames.
    """

    def __init__(self, master=None, controller=None, **kwargs):
        """
        Initialize the CustomButtonFrame.
        
        :param master: The parent Tkinter widget (usually the root window).
        :param controller: The main controller (usually MainWindow) to switch between frames.
        """
        super().__init__(master, **kwargs)
        self.controller = controller  # Store the controller to manage frame switching
        self.init_ui()  # Initialize the UI components

    def init_ui(self):
        """
        Set up the user interface for the CustomButtonFrame. Buttons are placed inside two rows,
        and each button is tied to a command that either switches frames or triggers an action.
        """
        self.configure()  # Configure the frame (add any additional options if needed)

        # Create a container frame to center the buttons both vertically and horizontally
        container = Frame(self)
        container.pack(expand=True, fill="both")  # Ensure the container fills the available space

        # Define the buttons and their respective commands
        buttons = [
            ("Grade Calculator", lambda: self.controller.show_frame("GradeCalculatorFrame")),  # Navigate to Grade Calculator frame
            ("Calculate History", lambda: print("Calculate History clicked")),  # Placeholder command for Calculate History
            ("Performance Analysis", lambda: print("Performance Analysis clicked")),  # Placeholder command for Performance Analysis
            ("Login", lambda: self.controller.show_frame("LoginFrame")),  # Navigate back to the Login frame
            ("Chat Bot", lambda: print("Chat Bot clicked")),  # Placeholder command for Chat Bot
            ("Official Links", lambda: print("Official Links clicked"))  # Placeholder command for Official Links
        ]

        # Create a frame for the top row of buttons
        top_frame = Frame(container)
        top_frame.pack(expand=True, fill="x", padx=20, pady=20)  # Add padding and ensure the top frame expands

        # Create a frame for the bottom row of buttons
        bottom_frame = Frame(container)
        bottom_frame.pack(expand=True, fill="x", padx=20, pady=20)  # Add padding and ensure the bottom frame expands

        # Add buttons to the top row (first 3 buttons)
        for i in range(3):
            button = ttk.Button(top_frame, text=buttons[i][0], style="CustomM.TButton", command=buttons[i][1])
            button.grid(row=0, column=i, padx=20, pady=10, sticky="ew")  # Arrange buttons with equal width and padding

        # Add buttons to the bottom row (last 3 buttons)
        for i in range(3, 6):
            button = ttk.Button(bottom_frame, text=buttons[i][0], style="CustomM.TButton", command=buttons[i][1])
            button.grid(row=0, column=i-3, padx=20, pady=10, sticky="ew")  # Arrange buttons with equal width and padding

        # Ensure all columns in both rows expand equally to make buttons fill the space evenly
        for i in range(3):
            top_frame.grid_columnconfigure(i, weight=1)  # Distribute space equally in the top row
            bottom_frame.grid_columnconfigure(i, weight=1)  # Distribute space equally in the bottom row
