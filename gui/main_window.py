# Main window class to manage and display different frames within the ScholarSerpent application

from gui.grade_calculator import GradeCalculatorFrame  # Import the Grade Calculator frame
from gui.user_login import LoginFrame  # Import the User Login frame
from gui.menu import CustomButtonFrame  # Import the custom menu frame

class MainWindow:
    """
    MainWindow class responsible for managing the root window and switching between different frames.
    It sets up the main application window, initializes all the frames (e.g., Login, Menu, Grade Calculator),
    and handles the logic for displaying them.
    """
    
    def __init__(self, root):
        """
        Initialize the main window and set its properties, including title, size, and resizable options.
        This method also initializes the frames within the main window.
        
        :param root: The root Tkinter window for the application.
        """
        self.root = root  # Store the root window instance
        self.root.title("ScholarSerpent")  # Set the title of the main window
        
        # Calculate the window size as 60% of the screen's width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)
        
        # Set the geometry of the window to the calculated size
        self.root.geometry(f'{window_width}x{window_height}')

        # Make the window resizable both horizontally and vertically
        self.root.resizable(True, True)

        # Dictionary to store all the frames (LoginFrame, CustomButtonFrame, GradeCalculatorFrame)
        self.frames = {}
        
        # Initialize all the frames for the application
        self.init_frames()

    def init_frames(self):
        """
        Initialize and place all frames (LoginFrame, CustomButtonFrame, GradeCalculatorFrame) inside the root window.
        These frames are placed in the same window but only one will be visible at a time, controlled by `show_frame`.
        """
        # Initialize and store the LoginFrame
        self.frames["LoginFrame"] = LoginFrame(self.root, self)
        self.frames["LoginFrame"].place(relwidth=1, relheight=1)  # Make the frame cover the entire window

        # Initialize and store the CustomButtonFrame (Menu)
        self.frames["CustomButtonFrame"] = CustomButtonFrame(self.root, self)
        self.frames["CustomButtonFrame"].place(relwidth=1, relheight=1)

        # Initialize and store the GradeCalculatorFrame
        self.frames["GradeCalculatorFrame"] = GradeCalculatorFrame(self.root, self)
        self.frames["GradeCalculatorFrame"].place(relwidth=1, relheight=1)

        # Initially display the LoginFrame when the application starts
        self.show_frame("LoginFrame")

    def show_frame(self, frame_name):
        """
        Bring the specified frame to the front, making it visible to the user.
        
        :param frame_name: The name of the frame to be shown (e.g., 'LoginFrame', 'CustomButtonFrame', 'GradeCalculatorFrame').
        """
        frame = self.frames[frame_name]  # Retrieve the frame from the dictionary
        frame.tkraise()  # Bring the frame to the front to display it
