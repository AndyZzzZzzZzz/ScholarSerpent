from tkinter import *
from PIL import Image, ImageTk
Image.CUBIC = Image.BICUBIC
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
import time 

# Initialize the main window with a specific theme and size.
main = ttk.Window(themename="superhero")
main.geometry('885x500')
main.title("SFU Grade Calculator")

# Define global variables for use across the application.
grading_components = [
    "Assignment", "Midterms", "Final Exam", "Term Project",
    "Participation", "Quizzes", "Presentation", "Others", "Bonus"
]
selection = grading_components[0]  # Default initial selection
result = []  # To store grading data
final_grade = 0 # Initialize the final grade to zero
sfu_grading = [  # SFU grading scale
    (95, "A+"), (90, "A"), (85, "A-"), (80, "B+"), (75, "B"), (70, "B-"),
    (65, "C+"), (60, "C"), (55, "C-"), (50, "D"), (45, "F"),
]
notepad_text = 1.0 # Initial line position for notepad text insertion

# Function to update the selected grading component.
def select(code):
    global selection
    selection = grading_components[code]
    current.configure(text=selection)

# Initialize buttons dynamically for each grading component.
def init_buttons():
    row = 0
    col = 0
    for idx, comp in enumerate(grading_components):
        button = ttk.Button(grade_module, text=comp, bootstyle="primary, outline", command=lambda idx=idx: select(idx))
        button.grid(row=row, column=col, padx=5, pady=5)
        col += 1

# Function to initialize or update the grade meter display. 
meter = None 
def init_meter(grade):
    global meter
    if meter is None:
        meter = ttk.Meter(
            output_space,
            metersize=180,
            padding=5,
            amountused=grade,
            metertype="semi",
            subtext="total course grade",
            textright="%",
            interactive=FALSE,
            bootstyle="danger",
            stripethickness=5
        )
        meter.grid(row=0, column=0, columnspan=2, rowspan=3)
    else:
        meter.configure(amountused=grade)

# Set the combo box items based on the number entered by the user.
def set_list():
    count = int(enter_amount.get())
    grade_combo.configure(state=ACTIVE, 
                            values=[selection + str(i) for i in range(1, count + 1)])

# Initialize a scrollable text box for output display.
def set_text_box():
    note_space = ttk.LabelFrame(text="Notes", bootstyle="primary")
    note_space.grid(row=1, column=4, columnspan=8, rowspan=4, padx=10, pady=10)

    global text_box
    text_box = ScrolledText(note_space, height=10, width=45, wrap=WORD, autohide=True, bootstyle="primary")
    text_box.grid(row=1, column=0, columnspan=8, rowspan=4, padx=5, pady=5)

    text_box.insert(END, 'User Input:\n')

# Calculate and update the grades based on user inputs.
def calculate():
    item = grade_combo.get()
    if item not in result:
        result.append((item, int(enter_percent.get()), int(enter_grade.get())))
    text_box.insert(END, item + ' weighs ' + enter_percent.get() + '%, recieves ' + enter_grade.get() + '%.\n')
    enter_percent.delete(0, END)
    enter_grade.delete(0,END)

    global notepad_text
    notepad_text += 1

# Update the display based on the calculated final grade.
def update_grade_display(final_grade):
    global letterGrade
    for item in sfu_grading:
        if final_grade >= item[0]:
            letter_grade.configure(text="Your letter grade: " + item[1])
            letterGrade = item[1]
            break
    global graduation_text
    global prereq_text 
    graduation_text = "pass" if final_grade >= 50 else "fail"
    prereq_text = "pass" if final_grade >= 55 else "fail"

    graduation.configure(text=f"Graduation Requirement: {graduation_text}")
    prereq.configure(text=f"Prerequisite Requirement: {prereq_text}")

# Final calculation and display update.
def final():
    global final_grade
    final_grade = sum((item[1]/100) * item[2] for item in result)
    init_meter(final_grade)
    update_grade_display(final_grade)

# Animate the progress bar and clear results.
def increment():
    progress['value'] = 0

    for x in range(40):
        progress['value'] += 2.5
        main.update_idletasks()  # Update the GUI to reflect changes
        time.sleep(0.1)  # Pause for a short period to see the progress bar update

    global result
    result = []

# Delete the last entry from results and update notepad.
def back():
    del result[-1]
    global notepad_text
    text_box.delete(str(notepad_text), END)
    notepad_text -= 1

# Save current results and notes into the text box.
def save():
    text_box.insert(END, 'final percentage: ' + str(final_grade)
                    + '% \n final letter grade:' + letterGrade
                    + '\nprerequisite requirement: ' + prereq_text
                    + '\ngraduation requirement: ' + graduation_text + '\n')
    text_box.insert(END, '-' * 50 + '\n')

    global notepad_text
    notepad_text += 5

# Validate that the input is a number.
def validate_number(x) -> bool:
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False
    
# Register the validation callback.
digit_func = main.register(validate_number)

# UI Layout Definitions
# Define various frames and layout components of the GUI.
grade_module = ttk.LabelFrame(text="Grading Module", bootstyle="info")
grade_module.grid(row=0, column=0, rowspan=1, columnspan=9, padx=10, pady=10)
input_space = ttk.LabelFrame(text="Data Input", bootstyle="primary")
input_space.grid(row=1, column=0, rowspan=3, columnspan=4, padx=10, pady=10)
output_space = ttk.LabelFrame(text="Results", bootstyle="primary")
output_space.grid(row=4, column=0, rowspan=3, columnspan=4, padx=10, pady=10)
utility_space = ttk.LabelFrame(text="Utility", bootstyle="primary")
utility_space.grid(row=5, column=4, columnspan=3, rowspan=4, padx=10, pady=10)

# User Input Frame Setup
current = ttk.Label(input_space, text=selection, bootstyle="light")
current.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

# Image display.
img = Image.open("technology.png")
resize = img.resize((100,100))
new_img = ImageTk.PhotoImage(resize)
my_label = Label(image = new_img, height = 100, width = 100)
my_label.grid(row = 5, column = 7, columnspan = 2, rowspan = 3, padx = 5, pady = 5)

# Button to confirm the number of items and update the combobox
confirm1 = ttk.Button(input_space, text="confirm", bootstyle="primary", command=set_list)
confirm1.grid(row=2, column=2, padx=5, pady=5)
# Button to confirm the entered grade and percentage
confirm2 = ttk.Button(input_space, text="confirm", bootstyle="primary", command=calculate)
confirm2.grid(row=3, column=2, padx=5, pady=5)

# Combobox to select specific grading items
grade_combo = ttk.Combobox(input_space, bootstyle="primary", state=DISABLED, width=15)
grade_combo.grid(row=2, column=0, padx=5, pady=5)

# Entry field to input the number of items
enter_amount = ttk.Entry(input_space, bootstyle="primary", width=8
                         ,validate="focus", validatecommand=(digit_func, '%P'))
enter_amount.grid(row=2, column=1, padx=5, pady=5)

# Entry fields for percentage and grade input
enter_percent = ttk.Entry(input_space, bootstyle="success", width=8
                          ,validate="focus", validatecommand=(digit_func, '%P'))
enter_percent.grid(row=3, column=0, padx=5, pady=5)
enter_grade = ttk.Entry(input_space, bootstyle="success", width=8
                        ,validate="focus", validatecommand=(digit_func, '%P'))
enter_grade.grid(row=3, column=1, padx=5, pady=5)

# Results Output Frame Setup
final_calc = ttk.Button(output_space, text="calculate", bootstyle="warning", command = final)
final_calc.grid(row=3, column=2, columnspan= 3, padx=5, pady=5)

# Labels for displaying calculated letter grade and requirements
letter_grade = ttk.Label(output_space, text= "Your letter grade:   ", bootstyle="info")
letter_grade.grid(row=0, column=2, padx=5, pady=5)
graduation = ttk.Label(output_space, text= "Graduation Requirement:     ", bootstyle="info")
graduation.grid(row=1, column=2, padx=5, pady=5)
prereq = ttk.Label(output_space, text= "Prerequisite Requirement:     ", bootstyle="info")
prereq.grid(row=2, column=2, padx=5, pady=5)


# Utility Buttons and Progress Bar
reset = ttk.Button(utility_space, text="reset", bootstyle="info, outline", command = increment)
reset.grid(row=0, column=0, padx=5, pady=5)
save = ttk.Button(utility_space, text="save", bootstyle="info, outline", command = save)
save.grid(row=0, column=1, padx=5, pady=5)
delete = ttk.Button(utility_space, text="delete", bootstyle="info, outline", command = back)
delete.grid(row=0, column=2, padx=5, pady=5)

# Progress bar to visually represent progress in tasks like resetting
progress = ttk.Progressbar(utility_space, bootstyle = "success striped",
                           maximum = 100,
                           mode = "determinate",
                           length = 260,
                           value = 0)
progress.grid(row=1, column=0, columnspan = 3, padx=5, pady=5)


# Initialization calls for setting up the UI components.
init_buttons()
set_text_box()
init_meter(final_grade)

# Main event loop to run the application.
main.mainloop()
