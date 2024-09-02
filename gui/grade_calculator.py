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
        self.course_entry.grid(row=0, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Component Percentage
        self.component_label = ttk.Label(input_frame, text=f"{self.selection} Percentage", style="Medium.TLabel")
        self.component_label.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.percentage_entry = ttk.Entry(input_frame)
        self.percentage_entry.grid(row=1, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Component Grade Entry
        grade_label = ttk.Label(input_frame, text=f"{self.selection} Grade", style="Medium.TLabel")
        grade_label.grid(row=2, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.grade_entry = ttk.Entry(input_frame)
        self.grade_entry.grid(row=2, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Component Grade Received
        grade_received = ttk.Label(input_frame, text=f"{self.selection} Grade", style="Medium.TLabel")
        grade_received.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=(10, 10))
        self.grade_received = ttk.Entry(input_frame)
        self.grade_received.grid(row=3, column=1, sticky="ew", pady=(10, 10), padx=(10, 10))

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
        gpa_input_label = ttk.Label(result_display, text="Letter Grade: ", style="Medium.TLabel")
        gpa_input_label.grid(row=6, column=0, sticky="w", pady=(5, 5))

        gpa_input_label = ttk.Label(result_display, text="Prerequisite Requirement: ", style="Medium.TLabel")
        gpa_input_label.grid(row=7, column=0, sticky="w", pady=(5, 5))

        gpa_input_label = ttk.Label(result_display, text="Graduation Requirement: ", style="Medium.TLabel")
        gpa_input_label.grid(row=8, column=0, sticky="w", pady=(5, 5))

        # GPA Calculate Frame (d)
        GPA_display = ttk.LabelFrame(middle_frame, text="GPA", bootstyle="primary", padding=10)
        GPA_display.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # GPA Meter
        self.gpa_meter = ttk.Meter(
            GPA_display,
            metersize=260,  # Increase the size of the meter
            padding=10,
            amountused=0,
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
        self.grade_label.config(text=f"{self.selection} Grade")

    def calculate_final_grade(self):
        total_grade = sum([self.results[comp][0] for comp in self.grading_components])
        self.final_grade = round(total_grade * (1 + self.curve_scale.get() / 100), 2)
        self.final_grade_label.config(text=f"Final Grade: {self.final_grade}")
        # Logic to determine letter grade
        for cutoff, grade in [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (50, "F")]:
            if self.final_grade >= cutoff:
                self.letter_grade_label.config(text=f"Letter Grade: {grade}")
                break

    def save_data(self):
        messagebox.showinfo("Save Data", "Data has been saved successfully.")

    def record_grade(self):
        messagebox.showinfo("Record Grade", "Grade has been recorded successfully.")

    def delete_last_entry(self):
        messagebox.showinfo("Delete Last Entry", "Last entry has been deleted.")

    def reset_fields(self):
        self.course_entry.delete(0, 'end')
        self.percentage_entry.delete(0, 'end')
        self.grade_entry.delete(0, 'end')
        self.curve_scale.set(0)
        self.final_grade_label.config(text="Final Grade: ")
        self.letter_grade_label.config(text="Letter Grade: ")

    def calculate_gpa(self):
        a = 10
