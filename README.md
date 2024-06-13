# SFU Grade Calculator

SFU Grade Calculator is a desktop application built with Python and Tkinter, using the ttkbootstrap library for a modern and clean user interface. This application allows SFU students to calculate their final grades based on various grading components and provides a visual representation of their grades.

## Features

- **Dynamic Component Selection:** Choose from different grading components like Assignments, Midterms, Final Exam, etc.
- **Grade Meter:** Visual representation of the final grade.
- **Notes Section:** Scrollable text area to keep track of the user's input and results.
- **Validation:** Input validation to ensure only numbers are entered.
- **Progress Bar:** Visual progress bar to indicate tasks like resetting the application.
- **Save Functionality:** Save the final grade calculation results in the notes section.
- **Delete Functionality:** Delete the last entered grade component.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/sfu-grade-calculator.git
    ```
2. **Navigate to the project directory:**
    ```sh
    cd sfu-grade-calculator
    ```
3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**
    ```sh
    python sfu_grade_calculator.py
    ```
2. **Interacting with the application:**
   - Select a grading component from the dynamically generated buttons.
   - Enter the number of items for the selected component and confirm.
   - Enter the weight percentage and received grade for each item.
   - Confirm each entry to add it to the calculation.
   - Click on "Calculate" to compute the final grade.
   - The meter will display the total course grade, and the letter grade will be shown based on the SFU grading scale.


## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request.



## Acknowledgements

- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/) for the modern UI components.
- SFU grading scale for providing the basis of grade calculation.

## Contact

For any inquiries or issues, please contact [kza63@sfu.ca](mailto:kza63@sfu.ca).
