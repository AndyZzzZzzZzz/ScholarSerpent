import sqlite3  # SQLite library for database interactions
import hashlib  # Hashing library for secure password storage

class Database:
    """
    This class manages all interactions with the SQLite database for the grade calculator application.
    It handles user registration, grade calculations, and storing final course grades.
    """

    def __init__(self, db_name="grade_calculator.db"):
        """
        Initialize the Database class by connecting to the specified SQLite database
        and creating the necessary tables if they don't exist.

        :param db_name: The name of the SQLite database file (defaults to "grade_calculator.db").
        """
        self.conn = sqlite3.connect(db_name)  # Connect to the SQLite database
        self.conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
        self.create_tables()  # Create the necessary tables

    def create_tables(self):
        """
        Create the required tables for storing user information, grade calculations, and final course grades.
        The following tables are created:
        - users: Stores user IDs and hashed passwords.
        - calculations: Stores individual grade components (e.g., assignments, exams) and their percentages.
        - grades: Stores final letter grades, prerequisite and graduation status, and the date saved.
        """
        with self.conn:
            # Create the users table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userID TEXT PRIMARY KEY,
                    userPassword TEXT NOT NULL
                )
            """)

            # Create the calculations table to store individual grade components
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS calculations (
                    courseID TEXT NOT NULL,
                    userID TEXT,
                    component TEXT NOT NULL,
                    percentage INTEGER NOT NULL,
                    grade INTEGER NOT NULL,
                    PRIMARY KEY (courseID, userID, component),
                    FOREIGN KEY (userID) REFERENCES users(userID)
                )
            """)

            # Create the grades table to store final course grades
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    userID TEXT,
                    courseID TEXT NOT NULL,
                    letterGrade TEXT NOT NULL,
                    prerequisiteStatus TEXT NOT NULL,
                    graduationStatus TEXT NOT NULL,
                    dateSaved TEXT NOT NULL DEFAULT (datetime('now')),
                    PRIMARY KEY (userID, courseID),
                    FOREIGN KEY (userID) REFERENCES users(userID)
                )
            """)

            # Create indexes to optimize query performance
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_userid ON grades(userID)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_courseid ON grades(courseID)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_calc_userid ON calculations(userID)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_calc_courseid ON calculations(courseID)")

    def insert_user(self, userID, hashed_password):
        """
        Insert a new user into the users table.

        :param userID: The unique identifier for the user.
        :param hashed_password: The securely hashed password for the user.
        """
        with self.conn:
            self.conn.execute("""
                INSERT INTO users (userID, userPassword)
                VALUES (?, ?)
            """, (userID, hashed_password))

    def insert_calculation(self, courseID, userID, component, percentage, grade):
        """
        Insert a new grade calculation into the calculations table, or update an existing record.

        :param courseID: The unique identifier for the course.
        :param userID: The unique identifier for the user.
        :param component: The specific component (e.g., assignment, exam).
        :param percentage: The weight of the component towards the final grade.
        :param grade: The grade achieved for this component.
        """
        with self.conn:
            self.conn.execute("""
                INSERT INTO calculations (courseID, userID, component, percentage, grade)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(courseID, userID, component) DO UPDATE SET
                percentage=excluded.percentage, grade=excluded.grade
            """, (courseID, userID, component, percentage, grade))

    def insert_grade(self, userID, courseID, letterGrade, prerequisiteStatus, graduationStatus):
        """
        Insert a final grade into the grades table, or update an existing record.

        :param userID: The unique identifier for the user.
        :param courseID: The unique identifier for the course.
        :param letterGrade: The final letter grade for the course.
        :param prerequisiteStatus: Whether the course fulfills a prerequisite.
        :param graduationStatus: Whether the course fulfills a graduation requirement.
        """
        with self.conn:
            self.conn.execute("""
                INSERT INTO grades (userID, courseID, letterGrade, prerequisiteStatus, graduationStatus)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(userID, courseID) DO UPDATE SET
                letterGrade=excluded.letterGrade, prerequisiteStatus=excluded.prerequisiteStatus, graduationStatus=excluded.graduationStatus, dateSaved=datetime('now')
            """, (userID, courseID, letterGrade, prerequisiteStatus, graduationStatus))

    def get_user(self, userID):
        """
        Retrieve a user's information from the users table based on the userID.

        :param userID: The unique identifier for the user.
        :return: A tuple containing the user's information, or None if the user is not found.
        """
        with self.conn:
            return self.conn.execute("SELECT * FROM users WHERE userID = ?", (userID,)).fetchone()

    def get_calculations(self, userID, courseID):
        """
        Retrieve all grade calculations for a specific user and course.

        :param userID: The unique identifier for the user.
        :param courseID: The unique identifier for the course.
        :return: A list of tuples representing the grade calculations, or an empty list if none exist.
        """
        with self.conn:
            return self.conn.execute("SELECT * FROM calculations WHERE userID = ? AND courseID = ?", (userID, courseID)).fetchall()

    def get_grades(self, userID, courseID):
        """
        Retrieve the final grade for a specific user and course.

        :param userID: The unique identifier for the user.
        :param courseID: The unique identifier for the course.
        :return: A tuple representing the final grade record, or None if the grade is not found.
        """
        with self.conn:
            return self.conn.execute("SELECT * FROM grades WHERE userID = ? AND courseID = ?", (userID, courseID)).fetchone()

    def update_user_password(self, userID, new_hashed_password):
        """
        Update the password for an existing user in the users table.

        :param userID: The unique identifier for the user.
        :param new_hashed_password: The new hashed password to be set for the user.
        """
        with self.conn:
            self.conn.execute("""
                UPDATE users
                SET userPassword = ?
                WHERE userID = ?
            """, (new_hashed_password, userID))

    def close(self):
        """
        Close the connection to the SQLite database.
        """
        self.conn.close()
