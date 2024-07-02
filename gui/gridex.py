from tkinter import Frame, Label, Entry, Button
from PIL import Image, ImageTk
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk

class GradeCalculatorFrame(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.configure()

        # Define global variables for use across the application
        self.grading_components = [
            "Assignment", "Midterms", "Final Exam", "Term Project",
            "Participation", "Quizzes", "Presentation", "Other", "Bonus"
        ]
        self.selection = self.grading_components[0]  # Default initial selection
        self.result = []  # To store grading data
        self.final_grade = 0 # Initialize the final grade to zero
        self.sfu_grading = [  # SFU grading scale
            (95, "A+"), (90, "A"), (85, "A-"), (80, "B+"), (75, "B"), (70, "B-"),
            (65, "C+"), (60, "C"), (55, "C-"), (50, "D"), (45, "F"),
        ]
        self.notepad_text = 1.0 # Initial line position for notepad text insertion

        # Grading Module
        self.grade_module = ttk.LabelFrame(self, text="Grading Module", bootstyle="info")
        self.grade_module.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


        # Initialize buttons dynamically for each grading component
        self.init_buttons()

       # Data Input Frame
        self.input_space = ttk.LabelFrame(self, text="Data Input", height=200, width=300, bootstyle="primary")
        self.input_space.grid_propagate(0)
        self.input_space.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Current selection display
        self.current = ttk.Label(self.input_space, text=self.selection, bootstyle="light")
        self.current.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Information for entries - Number, Percentage, Grade (each on the same row as their entry boxes)
        self.Number = ttk.Label(self.input_space, text=self.selection + " Number: ", bootstyle="info")
        self.Number.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.enter_amount = ttk.Entry(self.input_space, bootstyle="primary", width=12, validate="focus", validatecommand=(self.register(self.validate_number), '%P'))
        self.enter_amount.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        self.Percentage = ttk.Label(self.input_space, text=self.selection + " Percentage: ", bootstyle="info")
        self.Percentage.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.enter_percent = ttk.Entry(self.input_space, bootstyle="success", width=12, validate="focus", validatecommand=(self.register(self.validate_number), '%P'))
        self.enter_percent.grid(row=2, column=2, padx=5, pady=5, sticky="e")

        self.Grade = ttk.Label(self.input_space, text=self.selection + " Grade: ", bootstyle="info")
        self.Grade.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.enter_grade = ttk.Entry(self.input_space, bootstyle="success", width=12, validate="focus", validatecommand=(self.register(self.validate_number), '%P'))
        self.enter_grade.grid(row=3, column=2, padx=5, pady=5, sticky="e")

        # # Button to confirm the entered grade and percentage
        # self.confirm2 = ttk.Button(self.input_space, text="confirm", bootstyle="primary", command=self.calculate)
        # self.confirm2.pack(pady=5)

       # Results Frame
        self.output_space = ttk.LabelFrame(self, text="Results", bootstyle="primary")
        self.output_space.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


        self.letter_grade = ttk.Label(self.output_space, text= "Your letter grade:      ", bootstyle="info")
        self.letter_grade.grid(row = 0, column = 0, columnspan = 2, padx=10, pady=10 )

        self.graduation = ttk.Label(self.output_space, text= "Graduation Requirement:     ", bootstyle="info")
        self.graduation.grid(row = 1, column = 0, columnspan = 2, padx=10, pady=10)

        self.prereq = ttk.Label(self.output_space, text= "Prerequisite Requirement:     ", bootstyle="info")
        self.prereq.grid(row = 2, column = 0, columnspan = 2, padx=10, pady=10)

        self.final_calc = ttk.Button(self.output_space, text="calculate", bootstyle="warning")
        self.final_calc.grid(row = 3, column = 0, columnspan = 2, padx=10, pady=10)

        # Utility Frame
        self.utility_space = ttk.LabelFrame(self, text="Utility", bootstyle="primary")
        self.utility_space.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure grid weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.reset = ttk.Button(self.utility_space, text="reset", bootstyle="info, outline")
        self.reset.grid(row = 0, column = 0, padx = 5, pady=5)

        self.save_btn = ttk.Button(self.utility_space, text="save", bootstyle="info, outline")
        self.save_btn.grid(row = 0, column = 1, padx = 5, pady=5)

        self.delete = ttk.Button(self.utility_space, text="delete", bootstyle="info, outline")
        self.delete.grid(row = 0, column = 2, padx = 5, pady=5)

        # self.progress = ttk.Progressbar(self.utility_space, bootstyle="success striped", maximum=100, mode="determinate", length=260, value=0)
        # self.progress.pack(pady=5)

        # Initialize the grade meter display
        self.meter = None
        self.init_meter(self.final_grade)

    #     # Image display
    #     img = Image.open("technology.png")
    #     resize = img.resize((100, 100))
    #     new_img = ImageTk.PhotoImage(resize)
    #     self.my_label = Label(self, image=new_img, height=100, width=100, bg="yellow")
    #     self.my_label.image = new_img  # Keep a reference to avoid garbage collection
    #     self.my_label.pack(pady=10)

    # # Function to update the selected grading component
    # def select(self, code):
    #     self.selection = self.grading_components[code]
    #     self.current.configure(text=self.selection)

    # Initialize buttons dynamically for each grading component
    def init_buttons(self):
        col = 0
        for idx, comp in enumerate(self.grading_components):
            button = ttk.Button(self.grade_module, text=comp, bootstyle="primary, outline", command=lambda idx=idx: self.select(idx))
            button.grid(row= 0, column=col, padx=5, pady=5)
            col += 1

    # Initialize or update the grade meter display
    def init_meter(self, grade):
        if self.meter is None:
            self.meter = ttk.Meter(
                self.output_space,
                metersize=180,
                padding=5,
                amountused=grade,
                metertype="semi",
                subtext="total course grade",
                textright="%",
                interactive=False,
                bootstyle="danger",
                stripethickness=5
            )
            self.meter.grid(row = 0, column = 3, columnspan= 3, rowspan= 2, padx = 5, pady=5)
        else:
            self.meter.configure(amountused=grade)

    # Set the combo box items based on the number entered by the user
    def set_list(self):
        count = int(self.enter_amount.get())
        self.grade_combo.configure(state=ACTIVE, values=[self.selection + str(i) for i in range(1, count + 1)])

   

    # Calculate and update the grades based on user inputs
    # def calculate(self):
    #     item = self.grade_combo.get()
    #     if item not in self.result:
    #         self.result.append((item, int(self.enter_percent.get()), int(self.enter_grade.get())))
    #     self.text_box.insert(END, item + ' weighs ' + self.enter_percent.get() + '%, recieves ' + self.enter_grade.get() + '%.\n')
    #     self.enter_percent.delete(0, END)
    #     self.enter_grade.delete(0, END)
    #     self.notepad_text += 1

    # # Update the display based on the calculated final grade
    # def update_grade_display(self, final_grade):
    #     for item in self.sfu_grading:
    #         if final_grade >= item[0]:
    #             self.letter_grade.configure(text="Your letter grade: " + item[1])
    #             self.letterGrade = item[1]
    #             break
    #     self.graduation_text = "pass" if final_grade >= 50 else "fail"
    #     self.prereq_text = "pass" if final_grade >= 55 else "fail"

    #     self.graduation.configure(text=f"Graduation Requirement: {self.graduation_text}")
    #     self.prereq.configure(text=f"Prerequisite Requirement: {self.prereq_text}")

    # # Final calculation and display update
    # def final(self):
    #     self.final_grade = sum((item[1] / 100) * item[2] for item in self.result)
    #     self.init_meter(self.final_grade)
    #     self.update_grade_display(self.final_grade)

    # # Animate the progress bar and clear results
    # def increment(self):
    #     self.progress['value'] = 0
    #     for x in range(40):
    #         self.progress['value'] += 2.5
    #         self.update_idletasks()  # Update the GUI to reflect changes
    #         time.sleep(0.1)  # Pause for a short period to see the progress bar update
    #     self.result = []

    # # Delete the last entry from results and update notepad
    # def back(self):
    #     del self.result[-1]
    #     self.text_box.delete(str(self.notepad_text), END)
    #     self.notepad_text -= 1

    # # Save current results and notes into the text box
    # def save(self):
    #     self.text_box.insert(END, 'final percentage: ' + str(self.final_grade) + '% \n final letter grade:' + self.letterGrade + '\nprerequisite requirement: ' + self.prereq_text + '\ngraduation requirement: ' + self.graduation_text + '\n')
    #     self.text_box.insert(END, '-' * 50 + '\n')
    #     self.notepad_text += 5

    # Validate that the input is a number
    def validate_number(self, x) -> bool:
        if x.isdigit():
            return True
        elif x == "":
            return True
        else:
            return False
