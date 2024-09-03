import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="grade_calculator.db"):
        """
        Initialize the Database class.
        
        :param db_name: The name of the SQLite database file to connect to. Defaults to "grade_calculator.db".
        """
        self.conn = sqlite3.connect(db_name)  # Establish a connection to the SQLite database
        self.conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
        self.create_tables()  # Create the necessary tables if they don't already exist

    def create_tables(self):
        """
        Create tables in the SQLite database if they do not already exist.
        
        Tables created:
        - users: Stores user IDs and passwords.
        - calculations: Stores course component grades and their corresponding percentages.
        - grades: Stores final letter grades, prerequisite status, graduation status, and the date saved for courses.
        """
        with self.conn:
            # Create the users table with userID as the primary key and userPassword as a required field
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userID TEXT PRIMARY KEY,
                    userPassword TEXT NOT NULL
                )
            """)
            
            # Create the calculations table to store individual grade components for each course
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
            
            # Create the grades table to store final grades, course completion status, and the date the information was saved
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

            # Create indexes to optimize queries on grades and calculations tables
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_userid ON grades(userID)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_courseid ON grades(courseID)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_calc_userid ON calculations(userID)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_calc_courseid ON calculations(courseID)")

    def insert_user(self, userID, hashed_password):
        """
        Insert a new user into the users table.
        
        :param userID: The unique identifier for the user.
        :param hashed_password: The hashed password for the user.
        """
        with self.conn:
            self.conn.execute("""
                INSERT INTO users (userID, userPassword)
                VALUES (?, ?)
            """, (userID, hashed_password))
            



    def insert_calculation(self, courseID, userID, component, percentage, grade):
        """
        Insert a new grade calculation into the calculations table.
        If a record with the same courseID, userID, and component already exists, it updates the percentage and grade.
        
        :param courseID: The identifier for the course.
        :param userID: The identifier for the user.
        :param component: The specific component of the course (e.g., assignment, exam).
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
        Insert a new final grade into the grades table.
        If a record with the same userID and courseID already exists, it updates the letter grade,
        prerequisite status, graduation status, and the dateSaved.
        
        :param userID: The identifier for the user.
        :param courseID: The identifier for the course.
        :param letterGrade: The final letter grade for the course.
        :param prerequisiteStatus: The status of whether the course fulfills a prerequisite.
        :param graduationStatus: The status of whether the course fulfills a graduation requirement.
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
        Retrieve a user from the users table based on userID.
        
        :param userID: The identifier for the user.
        :return: A tuple representing the user's record or None if the user does not exist.
        """
        with self.conn:
            return self.conn.execute("SELECT * FROM users WHERE userID = ?", (userID,)).fetchone()

    def get_calculations(self, userID, courseID):
        """
        Retrieve all grade calculations for a specific user and course.
        
        :param userID: The identifier for the user.
        :param courseID: The identifier for the course.
        :return: A list of tuples representing the grade calculations or an empty list if none exist.
        """
        with self.conn:
            return self.conn.execute("SELECT * FROM calculations WHERE userID = ? AND courseID = ?", (userID, courseID)).fetchall()

    def get_grades(self, userID, courseID):
        """
        Retrieve the final grade and status for a specific user and course.
        
        :param userID: The identifier for the user.
        :param courseID: The identifier for the course.
        :return: A tuple representing the grade record or None if the grade does not exist.
        """
        with self.conn:
            return self.conn.execute("SELECT * FROM grades WHERE userID = ? AND courseID = ?", (userID, courseID)).fetchone()
        
    def close(self):
        """
        Close the connection to the SQLite database.
        """
        self.conn.close()

    def update_user_password(self, userID, new_hashed_password):
        """
        Update the password for an existing user.
        
        :param userID: The identifier for the user.
        :param new_hashed_password: The new hashed password for the user.
        """
        with self.conn:
            self.conn.execute("""
                UPDATE users
                SET userPassword = ?
                WHERE userID = ?
            """, (new_hashed_password, userID))
