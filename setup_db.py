import sqlite3

def initialize_db():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    # Create tables
    c.execute('''
    CREATE TABLE IF NOT EXISTS Quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        language TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        title TEXT,
        FOREIGN KEY (quiz_id) REFERENCES Quizzes (id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS QuestionTrans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        language TEXT,
        title TEXT,
        FOREIGN KEY (question_id) REFERENCES Questions (id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        text TEXT,
        is_correct BOOLEAN,
        FOREIGN KEY (question_id) REFERENCES Questions (id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS OptionTrans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        option_id INTEGER,
        language TEXT,
        text TEXT,
        FOREIGN KEY (option_id) REFERENCES Options (id)
    )
    ''')


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
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
