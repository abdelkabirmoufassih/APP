import sqlite3

def initialize_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    # Create Attempts table
    c.execute('''
    CREATE TABLE IF NOT EXISTS Attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quiz_id INTEGER,
        score INTEGER,
        status TEXT,
        time TIMESTAMP
    )
    ''')

    # Create Answers table
    c.execute('''
    CREATE TABLE IF NOT EXISTS Answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER,
        question_id INTEGER,
        option_id INTEGER,
        is_correct BOOLEAN,
        FOREIGN KEY (attempt_id) REFERENCES Attempts (id),
        FOREIGN KEY (question_id) REFERENCES Questions (id),
        FOREIGN KEY (option_id) REFERENCES Options (id)
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_db()
