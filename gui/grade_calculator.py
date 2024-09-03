from tkinter import Frame, Label, Entry, messagebox
from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import Database

class GradeCalculatorFrame(Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.database = Database()
        self.init_ui()

    def init_ui(self):

        self.course_data = {
            "course_code": "",  # Store course code here
            "components": {
                "Assignment": {"percentage": 0, "grades": []},  # Component and grades list
                "Midterm": {"percentage": 0, "grades": []},
                "Final Exam": {"percentage": 0, "grades": []},
                "Term Project": {"percentage": 0, "grades": []},
                "Participation": {"percentage": 0, "grades": []},
                "Quiz": {"percentage": 0, "grades": []},
                "Presentation": {"percentage": 0, "grades": []},
                "Other Marks": {"percentage": 0, "grades": []},
                "Bonus Marks": {"percentage": 0, "grades": []}
            }
        }

        self.configure(bg="#1e1e2d")

        self.grading_components = ["Assignment", "Midterm", "Final Exam", "Term Project", "Participation", "Quiz", "Presentation", "Other Marks", "Bonus Marks"]
        self.selection = "Assignment"

        # Main container with pack layout
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # Grading Module (a)
        grade_module = ttk.LabelFrame(container, text="Grade Calculator", bootstyle="info", padding=10)
        grade_module.pack(side="top", fill="x", pady=10)

        self.init_buttons(grade_module)

        # Middle Frame for input, result, and GPA (b, c, d)
        middle_frame = Frame(container, bg="#1e1e2d")
        middle_frame.pack(side="top", fill="both", expand=True)

        # Data Input Frame (b)
        input_frame = ttk.LabelFrame(middle_frame, text="Data Input", bootstyle="primary", padding=10)
        input_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Course Code Entry
        course_label = ttk.Label(input_frame, text="Course Code", style="Medium.TLabel")
        course_label.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.course_entry = ttk.Entry(input_frame)
        self.course_entry.bind("<Return>", lambda event: self.store_course_code())
        self.course_entry.grid(row=0, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Component Percentage
        self.component_label = ttk.Label(input_frame, text=f"{self.selection} Percentage", style="Medium.TLabel")
        self.component_label.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.percentage_entry = ttk.Entry(input_frame)
        self.percentage_entry.bind("<Return>", lambda event: self.store_component_percentage())
        self.percentage_entry.grid(row=1, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

       # Component Grade Entry
        self.total_grade_label = ttk.Label(input_frame, text=f"{self.selection} Total", style="Medium.TLabel")
        self.total_grade_label.grid(row=2, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.grade_entry = ttk.Entry(input_frame)
        self.grade_entry.grid(row=2, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.grade_entry.bind("<Return>", lambda event: self.store_grades())

        # Component Grade Received
        self.grade_received_label = ttk.Label(input_frame, text=f"{self.selection} Grade", style="Medium.TLabel")
        self.grade_received_label.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.grade_received = ttk.Entry(input_frame)
        self.grade_received.grid(row=3, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.grade_received.bind("<Return>", lambda event: self.store_grades())



        # Curve Adjustment
        curve_label = ttk.Label(input_frame, text="Curve Adjustment", style="Medium.TLabel")
        curve_label.grid(row=4, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.curve_scale = ttk.Scale(input_frame, from_=-10, to=20, orient=HORIZONTAL, length=100)
        self.curve_scale.grid(row=4, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Results Frame (c)
        result_display = ttk.LabelFrame(middle_frame, text="Course Result", bootstyle="primary", padding=10)
        result_display.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Course Grade Meter
        self.course_meter = ttk.Meter(
            result_display,
            metersize=260,  # Increase the size of the meter
            padding=10,
            amountused=0,
            metertype="semi",
            subtext="Course Grade",
            textright="%",
            interactive=False,
            bootstyle="success",
            stripethickness=5
        )
        self.course_meter.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=(20, 10), pady=(20, 10))


        # Labels for Course Results
        self.letter_grade_label = ttk.Label(result_display, text="Letter Grade: ", style="Medium.TLabel")
        self.letter_grade_label.grid(row=6, column=0, sticky="w", pady=(5, 5))

        self.prereq_label = ttk.Label(result_display, text="Prerequisite Requirement: ", style="Medium.TLabel")
        self.prereq_label.grid(row=7, column=0, sticky="w", pady=(5, 5))

        self.grad_label = ttk.Label(result_display, text="Graduation Requirement: ", style="Medium.TLabel")
        self.grad_label.grid(row=8, column=0, sticky="w", pady=(5, 5))

        # Inside the Results Frame (c)
        confirm_grade_button = ttk.Button(result_display, text="Confirm Grade", style="CustomOutline.TButton", command=self.calculate_final_grade)
        confirm_grade_button.grid(row=9, column=1, sticky="we", pady=(10, 10), padx=(10, 10))


        # GPA Calculate Frame (d)
        GPA_display = ttk.LabelFrame(middle_frame, text="GPA", bootstyle="primary", padding=10)
        GPA_display.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # GPA Meter
        self.gpa_meter = ttk.Meter(
            GPA_display,
            metersize=260,  # Size of the meter
            padding=10,
            amountused=0,
            amounttotal=4.33,  # Set the total amount to 4.33 to represent the max GPA
            metertype="semi",
            subtext="GPA After Course",
            textright="",
            interactive=False,
            bootstyle="info",
            stripethickness=5
        )
        self.gpa_meter.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=(20, 10), pady=(20, 10))

        # Labels and Inputs for GPA Calculation
        gpa_input_label = ttk.Label(GPA_display, text="Current GPA: ", style="Medium.TLabel")
        gpa_input_label.grid(row=6, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.gpa_input = ttk.Entry(GPA_display)
        self.gpa_input.grid(row=6, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        credits_taken_label = ttk.Label(GPA_display, text="Credits Taken: ", style="Medium.TLabel")
        credits_taken_label.grid(row=7, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.credits_taken_input = ttk.Entry(GPA_display)
        self.credits_taken_input.grid(row=7, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        course_credits_label = ttk.Label(GPA_display, text="Course Credits: ", style="Medium.TLabel")
        course_credits_label.grid(row=8, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.course_credits_input = ttk.Entry(GPA_display)
        self.course_credits_input.grid(row=8, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Confirm Button
        confirm_button = ttk.Button(GPA_display, text="Confirm", style="CustomOutline.TButton", command=self.calculate_gpa)
        confirm_button.grid(row=10, column=1, sticky="we", pady=(10, 10), padx=(10, 10))

        # Utility Frame (e)
        utility_frame = ttk.Frame(container, padding=10)
        utility_frame.pack(side="top", fill="x", pady=10)

        save_button = ttk.Button(utility_frame, text="Save", style="CustomOutline.TButton",  command=self.save_data)
        save_button.pack(side="left", padx=10)

        record_button = ttk.Button(utility_frame, text="Record", style="CustomOutline.TButton", command=self.record_grade)
        record_button.pack(side="left", padx=10)

        delete_button = ttk.Button(utility_frame, text="Delete Last Entry", style="CustomOutline.TButton", command=self.delete_last_entry)
        delete_button.pack(side="left", padx=10)

        menu_button = ttk.Button(utility_frame, text="Menu", style="CustomOutline.TButton", command=lambda: self.controller.show_frame("CustomButtonFrame"))
        menu_button.pack(side="left", padx=10)

    def init_buttons(self, grade_module):
        num_buttons = len(self.grading_components)
        button_frame = ttk.Frame(grade_module)
        button_frame.pack(fill="x")

        for idx, component in enumerate(self.grading_components):
            button = ttk.Button(button_frame, text=component, style="Large.TButton", command=lambda idx=idx: self.select_component(idx))
            button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    def select_component(self, idx):
        self.selection = self.grading_components[idx]
        self.component_label.config(text=f"{self.selection} Percentage")
        self.total_grade_label.config(text=f"{self.selection} Total")
        self.grade_received_label.config(text=f"{self.selection} Grade")

    def calculate_final_grade(self):
        try:
            # Calculate total grade from all components
            total_grade = sum([self.course_data["components"][comp]["grades"][-1][1] for comp in self.grading_components if self.course_data["components"][comp]["grades"]])

            # Apply curve adjustment
            self.final_grade = round(total_grade * (1 + self.curve_scale.get() / 100), 2)
            
            # Ensure the final grade does not exceed 100%
            self.final_grade = min(self.final_grade, 100)
            
            # Determine letter grade based on final grade
            for cutoff, grade in [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (50, "F")]:
                if self.final_grade >= cutoff:
                    self.letter_grade_label.config(text=f"Letter Grade: {grade}")
                    break

            # Update course meter with the final grade percentage
            self.course_meter.configure(amountused=self.final_grade)

            return self.final_grade

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all grade inputs are numbers.")
            return None


    def save_data(self):
        messagebox.showinfo("Save Data", "Data has been saved successfully.")

    def record_grade(self):
        messagebox.showinfo("Record Grade", "Grade has been recorded successfully.")

    def delete_last_entry(self):
        messagebox.showinfo("Delete Last Entry", "Last entry has been deleted.")

    def reset_fields(self):
        self.course_entry.config(state="normal")
        self.percentage_entry.config(state="normal")
        self.course_entry.delete(0, 'end')
        self.percentage_entry.delete(0, 'end')
        self.grade_entry.delete(0, 'end')
        self.grade_received.delete(0, 'end')
        self.curve_scale.set(0)
        self.letter_grade_label.config(text="Letter Grade: ")

        # Reset the course_data structure
        self.course_data = {
            "course_code": "",
            "components": {component: {"percentage": 0, "grades": []} for component in self.grading_components}
    }



    def calculate_gpa(self):
        try:
            # Get user inputs
            current_gpa = float(self.gpa_input.get())
            current_credits = float(self.credits_taken_input.get())
            course_credits = float(self.course_credits_input.get())

            # Calculate the final course grade percentage
            final_percentage = self.calculate_final_grade()
            if final_percentage is None:
                return

            # Convert percentage to GPA scale (e.g., 90-100% -> 4.0, 80-89% -> 3.0, etc.)
            new_gpa = self.convert_percentage_to_gpa(final_percentage)

            # Calculate the new weighted GPA
            total_credits = current_credits + course_credits
            weighted_gpa = (current_credits * current_gpa + course_credits * new_gpa) / total_credits

            # Display the weighted GPA on the GPA meter, formatted to two decimal places
            self.gpa_meter.configure(amountused=round(weighted_gpa, 2), subtext=f"GPA: {weighted_gpa:.2f}")



        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all GPA and credit inputs are numbers.")

    def convert_percentage_to_gpa(self, percentage):
        """
        Convert a percentage grade to a GPA. This is a simplified conversion.
        Adjust the mapping according to your grading scale.
        """
        if percentage >= 90:
            return 4.0
        elif percentage >= 80:
            return 3.0
        elif percentage >= 70:
            return 2.0
        elif percentage >= 60:
            return 1.0
        else:
            return 0.0
    
    def store_course_code(self):
        course_code = self.course_entry.get().strip()
        if not course_code:
            messagebox.showerror("Input Error", "Course Code cannot be empty.")
        else:
            self.course_data["course_code"] = course_code
            self.course_entry.config(state="disabled")  # Disable the entry field

    
    def store_component_percentage(self):
        if not self.course_data["course_code"]:
            messagebox.showerror("Input Error", "Please enter and store a valid Course Code first.")
        else:
            component_percentage = self.percentage_entry.get().strip()
            try:
                component_percentage = float(component_percentage)
                if component_percentage <= 0 or component_percentage > 100:
                    messagebox.showerror("Input Error", "Component Percentage must be between 0 and 100.")
                else:
                    self.course_data["components"][self.selection]["percentage"] = component_percentage
                    self.percentage_entry.config(state="disabled")  # Disable the entry field
            except ValueError:
                messagebox.showerror("Input Error", "Component Percentage must be a valid number.")

    
    def store_grades(self):
        if not self.course_data["course_code"]:
            messagebox.showerror("Input Error", "Please enter and store a valid Course Code first.")
        elif not self.course_data["components"][self.selection]["percentage"]:
            messagebox.showerror("Input Error", "Please enter and store a valid Component Percentage first.")
        else:
            grade_total = self.grade_entry.get().strip()
            grade_received = self.grade_received.get().strip()

            try:
                grade_total = float(grade_total)
                grade_received = float(grade_received)
                # Store the grades in the list for the selected component
                self.course_data["components"][self.selection]["grades"].append((grade_total, grade_received))
            except ValueError:
                messagebox.showerror("Input Error", "Grades must be valid numbers.")
        self.grade_entry.delete(0, 'end')
        self.grade_received.delete(0, 'end')




