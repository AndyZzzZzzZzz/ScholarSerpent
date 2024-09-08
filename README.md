# ScholarSerpent

**ScholarSerpent** is a Python-based academic performance management application. It provides users with a user-friendly interface to track course grades, calculate GPA, manage course components (e.g., assignments, exams), and store final grades. The application supports user registration, login, and password management using a local SQLite database.

## Features
- **User Registration & Login**: Secure login and registration system with password hashing.
- **Grade Calculator**: Calculate course grades based on multiple components (assignments, exams, etc.).
- **GPA Calculation**: Calculate GPA after entering final grades.
- **Password Management**: Password reset functionality with secure SHA-256 password hashing.
- **Docker Support**: Easily run the application in a Docker container.

## Table of Contents
1. [Installation](#installation)
2. [Running the Application](#running-the-application)
3. [Project Structure](#project-structure)
4. [Docker Instructions](#docker-instructions)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

### Prerequisites
Ensure that you have the following installed on your system:
- **Python 3.8+**
- **Docker** (if you prefer to run in a Docker container)

### Clone the Repository
```bash
git clone https://github.com/yourusername/scholarserpent.git
cd scholarserpent
```

### Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
Install the required Python packages using pip:
```bash 
pip install -r requirements.txt
```

### Running Locally
Once the dependencies are installed, run the application:
```bash
python ScholarSerpent.py
```
The GUI will launch, and you can start interacting with the grade calculator.

## Running the Application
1. Running the Application
2. User Registration: Register a new user by entering a user ID and password.
3. Login: Log in using your registered credentials.
4. Grade Calculator: Navigate to the grade calculator to input your course grades, calculate GPA, and track progress.

## Project Structure 
```bash 
/scholarserpent
│
├── /gui                 # GUI-related scripts
│   ├── grade_calculator.py   # Grade Calculator frame
│   ├── main_window.py        # Main window controller
│   ├── menu.py               # Menu interface
│   └── user_login.py         # Login frame
│
├── /database            # Database-related scripts
│   └── database.py          # SQLite database management
│
├── /assets              # Static assets like images and icons
│   └── incognito.png        # Example icon for user login
│
├── ScholarSerpent.py    # Main entry point for the application
├── Dockerfile           # Docker configuration file
├── requirements.txt     # Dependencies for the project
├── .gitignore           # Ignored files and directories
└── README.md            # Documentation for the repository
```

## Docker Instructions
You can also run ScholarSerpent using Docker. The provided Dockerfile contains all the necessary instructions to set up the environment.

### Build the Docker Image
From the project root, build the Docker image:
```bash 
docker build -t scholarserpent-app .
```
### Run the Docker Container
After building the image, run the application in a container:
```bash
docker run -p 5000:5000 scholarserpent-app
```
This will start the application inside a Docker container and expose it on port 5000.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (```bash git checkout -b feature-branch ```).
3. Commit your changes (```bash git commit -m 'Add new feature' ```).
4. Push to the branch (```bash git push origin feature-branch ```).
5. Open a pull request.