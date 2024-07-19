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

    # Insert sample data
    c.execute('''
    INSERT INTO Quizzes (title, language) VALUES
    ('General Knowledge', 'English'),
    ('Science', 'English')
    ''')

    c.execute('''
    INSERT INTO Questions (quiz_id, title) VALUES
    (1, 'What is the capital of France?'),
    (1, 'What is the largest planet in our solar system?')
    ''')

    c.execute('''
    INSERT INTO QuestionTrans (question_id, language, title) VALUES
    (1, 'French', 'Quelle est la capitale de la France?'),
    (2, 'French', 'Quelle est la plus grande planète de notre système solaire?')
    ''')

    c.execute('''
    INSERT INTO Options (question_id, text, is_correct) VALUES
    (1, 'Paris', 1),
    (1, 'London', 0),
    (2, 'Jupiter', 1),
    (2, 'Saturn', 0)
    ''')

    c.execute('''
    INSERT INTO OptionTrans (option_id, language, text) VALUES
    (1, 'French', 'Paris'),
    (2, 'French', 'Londres'),
    (3, 'French', 'Jupiter'),
    (4, 'French', 'Saturne')
    ''')
    # Insert Arabic question translations
    c.execute('''
    INSERT INTO QuestionTrans (question_id, language, title) VALUES
    (1, 'ar', 'ما هي عاصمة فرنسا?'),
    (2, 'ar', 'ما هو أكبر كوكب في نظامنا الشمسي?')
    ''')

    # Insert Arabic options
    c.execute('''
    INSERT INTO OptionTrans (option_id, language, text) VALUES
    (1, 'ar', 'باريس'),
    (2, 'ar', 'لندن'),
    (3, 'ar', 'المشتري'),
    (4, 'ar', 'زحل')
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
