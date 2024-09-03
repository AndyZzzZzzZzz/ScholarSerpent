from tkinter import *
from gui.main_window import MainWindow
import ttkbootstrap as ttk
from PIL import Image, ImageTk

def configure_styles():
    style = ttk.Style()
    
    # Define all custom styles
    style.configure('Large.TButton', font=('Helvetica', 18), background="#2c3e50", foreground="#ecf0f1", borderwidth=0, focuscolor="#2c3e50", relief="flat")
    style.configure('Medium.TLabel', font=('Helvetica', 14), foreground="#ecf0f1")

     # Define the custom button style for utility buttons 
    style.configure(
        'CustomOutline.TButton',
        font=('Helvetica', 16),
        background='#1c2833',    # Background color matching the theme
        foreground='#bdc3c7',    # Text color that contrasts with the background
        borderwidth=2,           # Border width to create an outline effect
        relief='ridge',          # Slightly raised appearance
        focuscolor='none',       # No focus highlight
        highlightbackground='#34495e',  # Border color to match theme
        highlightthickness=1,    # Border thickness
        padding=(5, 5)           # Padding inside the button
    )
    
    # Hover effect
    style.map(
        'CustomOutline.TButton',
        background=[('active', '#2e4053')],  # Darker shade on hover
        foreground=[('active', '#f0b27a')],  # Maintain text color on hover
        relief=[('pressed', 'sunken')]       # Slightly pressed appearance on click
    )

    # Define a custom button style
    style.configure(
        "CustomM.TButton",
        font=("Helvetica", 18),  # Increased font size for better visibility
        background="#2c3e50",    # Background color darker to match superhero theme
        foreground="#f0f3f4",    # Slightly brighter text color for better contrast
        borderwidth=3,           # Slightly thicker border for a more defined button
        relief="ridge",
        padding=(15, 10)         # Increased padding for a more substantial button appearance
    )

    # Map the custom button style to add hover effects
    style.map(
        "CustomM.TButton",
        background=[('active', '#34495e')],  # Slightly lighter shade on hover
        foreground=[('active', '#f39c12')],  # Golden color for the text on hover for better contrast
        relief=[('pressed', 'sunken')]       # Pressed effect for click interaction
    )



def main():
    # Initialize the main window with a specific theme.
    root = ttk.Window(themename="superhero")
    
    configure_styles()

    # Set the window icon
    icon = ImageTk.PhotoImage(file= "image/serpent.png")
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