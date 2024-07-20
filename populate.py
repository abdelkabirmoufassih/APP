import sqlite3

conn = sqlite3.connect('quiz_results.db')
c = conn.cursor()

try:

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


    # Insert new quiz
    c.execute('''
    INSERT INTO Quizzes (title, language) VALUES ('History Quiz', 'en')
    ''')
    
    # Fetch the quiz ID (assuming it's the last inserted ID)
    quiz_id = c.lastrowid
    
    # Insert questions
    c.execute('''
    INSERT INTO Questions (quiz_id, title) VALUES 
    (?, 'Who was the first president of the United States?'),
    (?, 'In which year did the French Revolution begin?')
    ''', (quiz_id, quiz_id))
    
    # Fetch question IDs
    question_ids = c.execute('SELECT id FROM Questions WHERE quiz_id = ?', (quiz_id,)).fetchall()
    question_ids = [id[0] for id in question_ids]
    
    # Insert options
    c.execute('''
    INSERT INTO Options (question_id, text, is_correct) VALUES
    (?, 'George Washington', 1),
    (?, 'Thomas Jefferson', 0),
    (?, 'Abraham Lincoln', 0),
    (?, 'John Adams', 0),
    (?, '1789', 1),
    (?, '1776', 0),
    (?, '1804', 0),
    (?, '1815', 0)
    ''', (question_ids[0], question_ids[0], question_ids[0], question_ids[0], question_ids[1], question_ids[1], question_ids[1], question_ids[1]))
    
    # Fetch option IDs
    option_ids = c.execute('SELECT id FROM Options WHERE question_id IN (?, ?)', (question_ids[0], question_ids[1])).fetchall()
    option_ids = [id[0] for id in option_ids]
    
    # Insert Arabic translations
    c.execute('''
    INSERT INTO OptionTrans (option_id, language, text) VALUES
    (?, 'ar', 'جورج واشنطن'),
    (?, 'ar', 'توماس جيفرسون'),
    (?, 'ar', 'أبراهام لينكولن'),
    (?, 'ar', 'جون آدمز'),
    (?, 'ar', '1789'),
    (?, 'ar', '1776'),
    (?, 'ar', '1804'),
    (?, 'ar', '1815')
    ''', (option_ids[0], option_ids[1], option_ids[2], option_ids[3], option_ids[4], option_ids[5], option_ids[6], option_ids[7]))

    # Insert Arabic translations for questions
    c.execute('''
    INSERT INTO QuestionTrans (question_id, language, title) VALUES
    (?, 'ar', 'من كان أول رئيس للولايات المتحدة؟'),
    (?, 'ar', 'في أي سنة بدأت الثورة الفرنسية؟')
    ''', (question_ids[0], question_ids[1]))

    conn.commit()
finally:
    conn.close()
