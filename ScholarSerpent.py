# ScholarSerpent.py
# Main entry point for the ScholarSerpent Tkinter-based GUI application.
# This script initializes the main window, configures styles, and starts the GUI loop.

from tkinter import *  # Import basic Tkinter widgets
from gui.main_window import MainWindow  # Import MainWindow class from gui module
import ttkbootstrap as ttk  # Import ttkbootstrap for theming and widgets
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL to handle image files

def configure_styles():
    """
    Configure custom styles for various widgets in the application.
    Styles include button appearance, labels, hover effects, and fonts to match the superhero theme.
    """
    style = ttk.Style()  # Create a style object to configure styles

    # Custom style for large buttons with a flat appearance and superhero theme colors
    style.configure(
        'Large.TButton', 
        font=('Helvetica', 18), 
        background="#2c3e50",  # Dark background
        foreground="#ecf0f1",  # Light text for contrast
        borderwidth=0,         # No border for a flat appearance
        focuscolor="#2c3e50", 
        relief="flat"          # Flat button style
    )
    
    # Custom style for medium labels with superhero theme colors
    style.configure(
        'Medium.TLabel', 
        font=('Helvetica', 14), 
        foreground="#ecf0f1"  # Light text for labels
    )

    # Custom style for utility buttons with an outlined appearance and hover effect
    style.configure(
        'CustomOutline.TButton',
        font=('Helvetica', 16),  # Medium font size
        background='#1c2833',    # Dark background for utility buttons
        foreground='#bdc3c7',    # Light text color for visibility
        borderwidth=2,           # Outline border
        relief='ridge',          # Slightly raised appearance
        focuscolor='none',       
        highlightbackground='#34495e',  # Border color to match theme
        highlightthickness=1,    # Border thickness
        padding=(5, 5)           # Padding inside the button
    )
    
    # Hover effect for utility buttons: darker background and brighter text
    style.map(
        'CustomOutline.TButton',
        background=[('active', '#2e4053')],  # Darker background on hover
        foreground=[('active', '#f0b27a')],  # Brighter text color on hover
        relief=[('pressed', 'sunken')]       # Pressed appearance on click
    )

    # Custom style for medium buttons with superhero theme colors and hover effects
    style.configure(
        "CustomM.TButton",
        font=("Helvetica", 18),  # Larger font for important buttons
        background="#2c3e50",    # Dark background
        foreground="#f0f3f4",    # Slightly brighter text for contrast
        borderwidth=3,           # Thicker border for emphasis
        relief="ridge",          # Raised appearance
        padding=(15, 10)         # Increased padding for a substantial button
    )

    # Hover effect for medium buttons: lighter background and golden text
    style.map(
        "CustomM.TButton",
        background=[('active', '#34495e')],  # Lighter background on hover
        foreground=[('active', '#f39c12')],  # Golden text on hover
        relief=[('pressed', 'sunken')]       # Pressed appearance for click
    )


def main():
    """
    Main function to initialize the Tkinter application, configure styles, and start the main loop.
    """
    # Create the main application window using the 'superhero' theme from ttkbootstrap
    root = ttk.Window(themename="superhero")
    
    # Configure the custom styles for widgets
    configure_styles()

    # Set the window icon using an image file (must be located in the 'image' folder)
    icon = ImageTk.PhotoImage(file="image/serpent.png")
    root.iconphoto(False, icon)  # Set the window icon

    # Create an instance of the MainWindow class and pass the root window as an argument
    app = MainWindow(root)

    # Display the 'LoginFrame' as the initial frame when the application starts
    app.show_frame("LoginFrame")

    # Start the Tkinter main event loop to keep the application running
    root.mainloop()

# Check if this script is being executed directly (rather than being imported as a module)
if __name__ == "__main__":
    # Call the main function to launch the application
    main()
