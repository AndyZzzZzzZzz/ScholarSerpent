from tkinter import *
from PIL import Image
Image.CUBIC = Image.BICUBIC
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from pathlib import Path
from itertools import cycle
from PIL import Image, ImageTk

# Initializing main window
main = ttk.Window(themename="superhero")
main.geometry('885x500')
main.title("SFU Grade Calculator")

# Global variables
grading_components = [
    "Assignment", "Midterms", "Final Exam", "Term Project",
    "Participation", "Quizzes", "Presentation", "Others", "Bonus"
]
selection = grading_components[0]
result = []
global final_grade
final_grade = 0
sfu_grading = [(95, "A+"),(90, "A"),(85, "A-"),(80, "B+"),(75, "B"),(70, "B-"),
               (65, "C+"),(60, "C"),(55, "C-"),(50, "D"),(45, "F"),]
# Functions
def select(code):
    """Update the selection based on user interaction."""
    global selection
    selection = grading_components[code]
    current.configure(text=selection)

def init_buttons():
    """Initialize buttons for grading components."""
    row = 0
    col = 0
    for idx, comp in enumerate(grading_components):
        button = ttk.Button(grade_module, text=comp, bootstyle="primary, outline", command=lambda idx=idx: select(idx))
        button.grid(row=row, column=col, padx=5, pady=5)
        col += 1

meter = None  
def init_meter(grade):
    """Initialize or update the grade meter in the UI."""
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


def set_list():
    """Set list of items based on the number entered by user, clearing previous entries."""
    count = int(enter_amount.get())
    grade_combo.configure(state=ACTIVE, 
                            values=[selection + str(i) for i in range(1, count + 1)])

def calculate():
    """Calculate grades based on user entries."""
    item = grade_combo.get()
    if item not in result:
        result.append((item, int(enter_percent.get()), int(enter_grade.get())))
    
    enter_percent.delete(0, END)
    enter_grade.delete(0,END)

def set_text_box():
    """Initialize the scrollable text box for output display."""
    note_space = ttk.LabelFrame(text="Notes", bootstyle="primary")
    note_space.grid(row=1, column=4, columnspan=8, rowspan=4, padx=10, pady=10)

    text_box = ScrolledText(note_space, height=10, width=45, wrap=WORD, autohide=True, bootstyle="primary")
    text_box.grid(row=1, column=0, columnspan=8, rowspan=4, padx=5, pady=5)

def update_grade_display(final_grade):
    """Update the display with the final grade and other requirements."""
    for item in sfu_grading:
        if final_grade >= item[0]:
            letter_grade.configure(text="Your letter grade: " + item[1])
            break

    graduation_text = "pass" if final_grade >= 50 else "fail"
    prereq_text = "pass" if final_grade >= 55 else "fail"

    graduation.configure(text=f"Graduation Requirement: {graduation_text}")
    prereq.configure(text=f"Prerequisite Requirement: {prereq_text}")

def final():
    """Calculate final grade based on combo box results and update display."""
    global final_grade
    final_grade = sum((item[1]/100) * item[2] for item in result)
    init_meter(final_grade)
    update_grade_display(final_grade)

def increment():
    """Show animation of progress bar once press reset."""
    progress.start(5)
    

# UI Layout
# Grading Module Frame
grade_module = ttk.LabelFrame(text="Grading Module", bootstyle="info")
grade_module.grid(row=0, column=0, rowspan=1, columnspan=9, padx=10, pady=10)

# User Input Frame
input_space = ttk.LabelFrame(text="Data Input", bootstyle="primary")
input_space.grid(row=1, column=0, rowspan=3, columnspan=4, padx=10, pady=10)

current = ttk.Label(input_space, text=selection, bootstyle="light")
current.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

confirm1 = ttk.Button(input_space, text="confirm", bootstyle="primary", command=set_list)
confirm1.grid(row=2, column=2, padx=5, pady=5)

enter_amount = ttk.Entry(input_space, bootstyle="primary", width=8)
enter_amount.grid(row=2, column=1, padx=5, pady=5)

grade_combo = ttk.Combobox(input_space, bootstyle="primary", state=DISABLED, width=15)
grade_combo.grid(row=2, column=0, padx=5, pady=5)

enter_percent = ttk.Entry(input_space, bootstyle="success", width=8)
enter_percent.grid(row=3, column=0, padx=5, pady=5)

enter_grade = ttk.Entry(input_space, bootstyle="success", width=8)
enter_grade.grid(row=3, column=1, padx=5, pady=5)

confirm2 = ttk.Button(input_space, text="confirm", bootstyle="primary", command=calculate)
confirm2.grid(row=3, column=2, padx=5, pady=5)

# Results Output Frame
output_space = ttk.LabelFrame(text="Results", bootstyle="primary")
output_space.grid(row=4, column=0, rowspan=3, columnspan=4, padx=10, pady=10)

final_calc = ttk.Button(output_space, text="calculate", bootstyle="warning", command = final)
final_calc.grid(row=3, column=2, columnspan= 3, padx=5, pady=5)

letter_grade = ttk.Label(output_space, text= "Your letter grade:   ", bootstyle="info")
letter_grade.grid(row=0, column=2, padx=5, pady=5)

graduation = ttk.Label(output_space, text= "Graduation Requirement:     ", bootstyle="info")
graduation.grid(row=1, column=2, padx=5, pady=5)

prereq = ttk.Label(output_space, text= "Prerequisite Requirement:     ", bootstyle="info")
prereq.grid(row=2, column=2, padx=5, pady=5)

#Utility buttons
utility_space = ttk.LabelFrame(text="Utility", bootstyle="primary")
utility_space.grid(row=5, column=4, columnspan=3, rowspan=4, padx=10, pady=10)

reset = ttk.Button(utility_space, text="reset", bootstyle="info, outline", command = increment)
reset.grid(row=0, column=0, padx=5, pady=5)

save = ttk.Button(utility_space, text="save", bootstyle="info, outline")
save.grid(row=0, column=1, padx=5, pady=5)

delete = ttk.Button(utility_space, text="delete", bootstyle="info, outline")
delete.grid(row=0, column=2, padx=5, pady=5)

progress = ttk.Progressbar(utility_space, bootstyle = "success striped",
                           maximum = 100,
                           mode = "determinate",
                           length = 260,
                           value = 0)
progress.grid(row=1, column=0, columnspan = 3, padx=5, pady=5)

img = Image.open("technology.png")
resize = img.resize((100,100))
new_img = ImageTk.PhotoImage(resize)
my_label = Label(image = new_img, height = 100, width = 100)
my_label.grid(row = 5, column = 7, columnspan = 2, rowspan = 3, padx = 5, pady = 5)

# Initialization calls
init_buttons()
set_text_box()
init_meter(final_grade)
# Main loop
main.mainloop()
