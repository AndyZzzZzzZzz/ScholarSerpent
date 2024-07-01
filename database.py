import sqlite3

class Database:
    def __init__(self, db_name="grade_calculator.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userID TEXT PRIMARY KEY,
                    userPassword TEXT NOT NULL
                )
            """)
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
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    userID TEXT,
                    courseID TEXT NOT NULL,
                    letterGrade TEXT NOT NULL,
                    prerequisiteStatus TEXT NOT NULL,
                    graduationStatus TEXT NOT NULL,
                    PRIMARY KEY (userID, courseID),
                    FOREIGN KEY (userID) REFERENCES users(userID)
                )
            """)

    def insert_user(self, userID, userPassword):
        with self.conn:
            self.conn.execute("""
                INSERT INTO users (userID, userPassword)
                VALUES (?, ?)
            """, (userID, userPassword))

    def insert_calculation(self, courseID, userID, component, percentage, grade):
        with self.conn:
            self.conn.execute("""
                INSERT INTO calculations (courseID, userID, component, percentage, grade)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(courseID, userID, component) DO UPDATE SET
                percentage=excluded.percentage, grade=excluded.grade
            """, (courseID, userID, component, percentage, grade))


    def insert_grade(self, userID, courseID, letterGrade, prerequisiteStatus, graduationStatus):
        with self.conn:
            self.conn.execute("""
                INSERT INTO grades (userID, courseID, letterGrade, prerequisiteStatus, graduationStatus)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(userID, courseID) DO UPDATE SET
                letterGrade=excluded.letterGrade, prerequisiteStatus=excluded.prerequisiteStatus, graduationStatus=excluded.graduationStatus
            """, (userID, courseID, letterGrade, prerequisiteStatus, graduationStatus))

    def get_user(self, userID):
        with self.conn:
            return self.conn.execute("SELECT * FROM users WHERE userID = ?", (userID,)).fetchone()

    def get_calculations(self, userID, courseID):
        with self.conn:
            return self.conn.execute("SELECT * FROM calculations WHERE userID = ? AND courseID = ?", (userID, courseID)).fetchall()

    def get_grades(self, userID, courseID):
        with self.conn:
            return self.conn.execute("SELECT * FROM grades WHERE userID = ? AND courseID = ?", (userID, courseID)).fetchone()
        
    def close(self):
        self.conn.close()
