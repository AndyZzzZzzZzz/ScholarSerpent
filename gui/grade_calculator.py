from tkinter import Frame, Label, Entry, Button, messagebox
from PIL import Image, ImageTk
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import Database

class GradeCalculatorFrame(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.database = Database()  # Initialize the database attribute
        self.init_ui()

    def init_ui(self):
        self.configure()

        # Define global variables for use across the application
        self.grading_components = [
            "HW", "Midterm", "Exam", "Project",
            "Particip.", "Quiz", "Talk", "Other", "Bonus"
        ]
        self.selection = self.grading_components[0]  # Default initial selection
        self.result = []  # To store grading data
        self.final_grade = 0 # Initialize the final grade to zero
        self.sfu_grading = [  # SFU grading scale
            (95, "A+"), (90, "A"), (85, "A-"), (80, "B+"), (75, "B"), (70, "B-"),
            (65, "C+"), (60, "C"), (55, "C-"), (50, "D"), (45, "F"),
        ]

        # Initialize an empty dictionary to store computation results
        self.results = {
            "HW": [0, []],
            "Midterm": [0, []],
            "Exam": [0, []],
            "Project": [0, []],
            "Particip.": [0, []],
            "Quiz": [0, []],
            "Talk": [0, []],
            "Other": [0, []],
            "Bonus": [0, []]
        }

        # Grading Module
        self.grade_module = ttk.LabelFrame(self, text="Grading Module", bootstyle="info")
        self.grade_module.place(x=10, y=10, width=865, height=60)

        # Initialize buttons dynamically for each grading component
        self.init_buttons()

        # Data Input Frame
        self.input_space = ttk.LabelFrame(self, text="Data Input", bootstyle="primary")
        self.input_space.place(x=10, y=80, width=420, height=250)

        # CourseCode
        # Information for entries - Number, Percentage, Grade (each on the same row as their entry boxes)
        self.Course = ttk.Label(self.input_space, text= "Course Code: ", bootstyle="info")
        self.Course.place(x=10, y=10, width=150, height=25)
        self.enter_course = ttk.Entry(self.input_space, bootstyle="primary")
        self.enter_course.place(x=220, y=10, width=180, height=25)
        self.enter_course.bind("<Return>", self.on_enter_course_id)

        # Information for entries - Number, Percentage, Grade (each on the same row as their entry boxes)
        self.Percentage = ttk.Label(self.input_space, text=self.selection + " Percentage: ", bootstyle="info")
        self.Percentage.place(x=10, y=50, width=150, height=25)
        self.enter_percent = ttk.Entry(self.input_space, bootstyle="primary", validate="focus", validatecommand=(self.register(lambda x: x.isdigit() or x == ""), '%P'))
        self.enter_percent.place(x=220, y=50, width=180, height=25)
        self.enter_percent.bind("<Return>", self.on_enter_percentage)

        self.Number = ttk.Label(self.input_space, text=self.selection + " Total: ", bootstyle="info")
        self.Number.place(x=10, y=90, width=150, height=25)
        self.enter_number = ttk.Entry(self.input_space, bootstyle="success", validate="focus", validatecommand=(self.register(lambda x: x.isdigit() or x == ""), '%P'))
        self.enter_number.place(x=220, y=90, width=180, height=25)
        self.enter_number.bind("<Return>", self.on_enter_number_and_grade)

        self.Grade = ttk.Label(self.input_space, text=self.selection + " Grade: ", bootstyle="info")
        self.Grade.place(x=10, y=130, width=150, height=25)
        self.enter_grade = ttk.Entry(self.input_space, bootstyle="success", validate="focus", validatecommand=(self.register(lambda x: x.isdigit() or x == ""), '%P'))
        self.enter_grade.place(x=220, y=130, width=180, height=25)
        self.enter_grade.bind("<Return>", self.on_enter_number_and_grade)
        
        self.Curve = ttk.Label(self.input_space, text="Curve Preference: ", bootstyle="info")
        self.Curve.place(x=10, y=170, width=150, height=25)
        self.enter_curve= ttk.Scale(self.input_space, bootstyle="success", from_ = -10, to = 20, orient= HORIZONTAL)
        self.enter_curve.place(x=220, y=170, width=180, height=25)

        # Results Frame
        self.output_space = ttk.LabelFrame(self, text="Results", bootstyle="primary")
        self.output_space.place(x=450, y=80, width=425, height=250)

        self.letter_grade = ttk.Label(self.output_space, text= "Your letter grade:      ", bootstyle="info")
        self.letter_grade.place(x=10, y=10, width=200, height=25 )

        self.graduation = ttk.Label(self.output_space, text= "Graduation Requirement:     ", bootstyle="info")
        self.graduation.place(x=10, y=45, width=200, height=25)

        self.prereq = ttk.Label(self.output_space, text= "Prerequisite Requirement:     ", bootstyle="info")
        self.prereq.place(x=10, y=80, width=200, height=25)

        self.final_calc = ttk.Button(self.output_space, text="calculate", bootstyle="warning", command=self.calculate_final_grade)
        self.final_calc.place(x=260, y=190, width=100, height=30)

        # Utility Frame
        self.utility_space = ttk.LabelFrame(self, text="Utility", bootstyle="primary")
        self.utility_space.place(x=10, y=340, width=865, height=90)

        self.reset = ttk.Button(self.utility_space, text="reset", bootstyle="info, outline", command=self.reset_fields)
        self.reset.place(x=240, y=10, width=100, height=30)

        self.save_btn = ttk.Button(self.utility_space, text="save", bootstyle="info, outline", command=self.save_data)
        self.save_btn.place(x=360, y=10, width=100, height=30)


        self.delete = ttk.Button(self.utility_space, text="delete", bootstyle="info, outline", command=self.delete_last_entry)
        self.delete.place(x=480, y=10, width=100, height=30)

        self.menu = ttk.Button(self.utility_space, text="menu", bootstyle="info, outline", command=lambda: self.controller.show_frame("CustomButtonFrame"))
        self.menu.place(x=120, y=10, width=100, height=30)

        self.record_btn = ttk.Button(self.utility_space, text="record", bootstyle="info, outline", command=self.record_grade)
        self.record_btn.place(x=600, y=10, width=100, height=30)


        # Initialize the grade meter display
        self.meter = None
        self.init_meter(self.final_grade)

    # Initialize buttons dynamically for each grading component
    def init_buttons(self):
        num_buttons = len(self.grading_components)
        frame_width = 865  # Width of the grade_module frame
        button_width = (frame_width - 10 * (num_buttons + 1)) // num_buttons  # Calculate button width

        x_position = 10  # Starting position with padding

        for idx, comp in enumerate(self.grading_components):
            button = ttk.Button(self.grade_module, text=comp, bootstyle="primary, outline", command=lambda idx=idx: self.select(idx))
            button.place(x=x_position, y=5, width=button_width, height=30)
            x_position += button_width + 10  # Move to the next position with padding

    def select(self, idx):
        # Save the current percentage if it is disabled
        if self.enter_percent["state"] == "disabled":
            percentage = self.enter_percent.get()
            if percentage.isdigit():
                percentage = int(percentage)
                self.results[self.selection][0] = percentage

        # Change the selected grading component
        self.selection = self.grading_components[idx]

        # Update labels
        self.Percentage.configure(text=self.selection + " Percentage: ")
        self.Number.configure(text=self.selection + " Total: ")
        self.Grade.configure(text=self.selection + " Grade: ")

        # Enable the percentage entry box for new input
        self.enter_percent.configure(state="normal")
        self.enter_percent.delete(0, 'end')

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
            self.meter.place(x=220, y=10, width=180, height=180)
        else:
            self.meter.configure(amountused=grade)

    def on_enter_percentage(self, event):
        percentage = self.enter_percent.get()
        if not percentage.isdigit():
            messagebox.showwarning("Invalid Input", "Percentage must be an integer.")
            return
        
        percentage = int(percentage)
        
        total_percentage = sum(self.results[component][0] for component in self.results)
        total_percentage += percentage - self.results[self.selection][0]  # Adjust the current component's percentage

        if total_percentage > 100:
            messagebox.showwarning("Invalid Input", "Total percentage for all components cannot exceed 100.")
            return

        self.results[self.selection][0] = percentage
        self.enter_percent.configure(state="disabled")



    def on_enter_number_and_grade(self, event):
        total = self.enter_number.get()
        grade = self.enter_grade.get()

        if not total or not grade:
            messagebox.showwarning("Invalid Input", "Both total grade and grade received must have values.")
            return

        if total.isdigit() and (lambda x: x.replace('.', '', 1).isdigit() and x.count('.') < 2)(grade):
            total = int(total)
            grade = float(grade)

            if grade > total:
                messagebox.showwarning("Invalid Input", "Grade received cannot exceed total grade.")
                return

            self.results[self.selection][1].append((total, grade))
            self.enter_number.delete(0, 'end')
            self.enter_grade.delete(0, 'end')
        else:
            messagebox.showwarning("Invalid Input", "Total grade must be an integer and grade received must be a numeric value.")




    def calculate_final_grade(self):
        total_grade = 0
        for component, (percentage, scores) in self.results.items():
            if scores:
                avg_score = sum(score / total for total, score in scores) / len(scores)
                component_grade = avg_score * percentage
                total_grade += component_grade

        # Apply the curve adjustment
        curve_value = self.enter_curve.get()
        curve_multiplier = 1 + (curve_value / 100)  # Calculate the curve multiplier
        self.final_grade = round(total_grade * curve_multiplier, 2)  # Round to two decimal places

        self.init_meter(self.final_grade)
        self.update_grade_display(self.final_grade)

    def update_grade_display(self, final_grade):
        for item in self.sfu_grading:
            if final_grade >= item[0]:
                self.letter_grade.configure(text="Your letter grade: " + item[1])
                self.letterGrade = item[1]
                break
        self.graduation_text = "pass" if final_grade >= 50 else "fail"
        self.prereq_text = "pass" if final_grade >= 55 else "fail"

        self.graduation.configure(text=f"Graduation Requirement: {self.graduation_text}")
        self.prereq.configure(text=f"Prerequisite Requirement: {self.prereq_text}")
    
    def save_data(self):
        courseID = self.enter_course.get()
        userID = self.controller.current_user
        component = self.selection
        percentage = self.results[component][0]

        # Calculate the average grade for the component
        grades = self.results[component][1]
        if grades:
            average_grade = sum(grade / total for total, grade in grades) / len(grades)
        else:
            average_grade = 0

        # Save the data to the database
        self.database.insert_calculation(courseID, userID, component, percentage, average_grade)

        messagebox.showinfo("Save Successful", "Your data has been saved successfully!")

    def on_enter_course_id(self, event):
        self.courseID = self.enter_course.get()
        self.enter_course.configure(state="disabled")

    def record_grade(self):
        userID = self.controller.current_user
        courseID = self.enter_course.get()
        letterGrade = self.letter_grade.cget("text").split(": ")[1]
        prerequisiteStatus = self.prereq.cget("text").split(": ")[1]
        graduationStatus = self.graduation.cget("text").split(": ")[1]

        # Save the data to the database
        self.database.insert_grade(userID, courseID, letterGrade, prerequisiteStatus, graduationStatus)

        messagebox.showinfo("Record Successful", "Your grade information has been recorded successfully!")

    def reset_fields(self):
        # Clear the current course name and enable the course entry box
        self.enter_course.configure(state="normal")
        self.enter_course.delete(0, 'end')

        # Reset the results dictionary to default state
        self.results = {
            "HW": [0, []],
            "Midterm": [0, []],
            "Exam": [0, []],
            "Project": [0, []],
            "Particip.": [0, []],
            "Quiz": [0, []],
            "Talk": [0, []],
            "Other": [0, []],
            "Bonus": [0, []]
        }

        # Clear the entry boxes
        self.enter_percent.configure(state="normal")
        self.enter_percent.delete(0, 'end')
        self.enter_number.delete(0, 'end')
        self.enter_grade.delete(0, 'end')

        # Clear the grade meter
        self.init_meter(0)

        # Clear the graduation and prerequisite requirements labels
        self.graduation.configure(text="Graduation Requirement: ")
        self.prereq.configure(text="Prerequisite Requirement: ")
        self.letter_grade.configure(text="Your letter grade: ")

        # Set the curve scale to 0
        self.enter_curve.set(0)

        # Clear any stored final grade
        self.final_grade = 0

    def delete_last_entry(self):
        # Get the current grading component
        component = self.selection

        # Check if there are any scores to delete
        if self.results[component][1]:
            # Remove the last score entry
            self.results[component][1].pop()

            # Provide feedback to the user
            messagebox.showinfo("Delete Successful", "The last entry has been deleted successfully.")
        else:
            messagebox.showinfo("No Entries", "There are no entries to delete.")



