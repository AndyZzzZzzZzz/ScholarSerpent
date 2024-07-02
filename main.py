from tkinter import Tk
from gui.main_window import MainWindow
import ttkbootstrap as ttk
from PIL import Image, ImageTk

def main():
    # Initialize the main window with a specific theme.
    root = ttk.Window(themename="superhero")
    
    # Set the window icon
    icon = ImageTk.PhotoImage(file="image/serpent.png")
    root.iconphoto(False, icon) 

    # Create an instance of the MainWindow class, passing the root window as an argument
    app = MainWindow(root)

    # Show the user login frame first
    app.show_frame("LoginFrame")

    # Start the Tkinter main event loop to keep the application running
    root.mainloop()

# Check if this script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    # Call the main function to start the application
    main()
