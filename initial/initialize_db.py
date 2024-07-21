import sqlite3
from datetime import datetime
import bcrypt

def populate_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert Users
    users = [
        ('123456789', 'Alice', 'Smith', 'IT', 'NYC', bcrypt.hashpw('password'.encode(), bcrypt.gensalt())),
        ('987654321', 'Bob', 'Brown', 'HR', 'LA', bcrypt.hashpw('password'.encode(), bcrypt.gensalt())),
        ('111222333', 'Charlie', 'Davis', 'Finance', 'Chicago', bcrypt.hashpw('password'.encode(), bcrypt.gensalt())),
        ('444555666', 'Diana', 'Evans', 'Marketing', 'Houston', bcrypt.hashpw('password'.encode(), bcrypt.gensalt()))
    ]

    c.executemany('INSERT INTO Users (cin, first_name, last_name, service, site, password_hash) VALUES (?, ?, ?, ?, ?, ?)', users)

    # Insert Quizzes
    quizzes = [
        ('General Knowledge', 'en'),
        ('Science Quiz', 'en'),
        ('History Quiz', 'en'),
        ('Geography Quiz', 'en')
    ]

    c.executemany('INSERT INTO Quizzes (title, language) VALUES (?, ?)', quizzes)

    # Insert Questions and Translations
    questions = [
        (1, 'What is the capital of France?'),
        (1, 'What is 2+2?'),
        (1, 'Who wrote Hamlet?'),
        (1, 'What is the boiling point of water?'),
        (1, 'Who painted the Mona Lisa?'),
        (1, 'What is the tallest mountain in the world?'),
        (1, 'What is the speed of light?'),
        (1, 'What is the chemical symbol for gold?'),
        (1, 'What is the largest ocean on Earth?'),
        (1, 'Who invented the telephone?')
    ]

    c.executemany('INSERT INTO Questions (quiz_id, title) VALUES (?, ?)', questions)

    question_translations = [
        (1, 'fr', 'Quelle est la capitale de la France?'),
        (1, 'ar', 'ما هي عاصمة فرنسا؟'),
        (2, 'fr', 'Quel est 2+2?'),
        (2, 'ar', 'ما هو ٢+٢؟'),
        (3, 'fr', 'Qui a écrit Hamlet?'),
        (3, 'ar', 'من كتب هاملت؟'),
        (4, 'fr', 'Quel est le point d\'ébullition de l\'eau?'),
        (4, 'ar', 'ما هي درجة غليان الماء؟'),
        (5, 'fr', 'Qui a peint la Joconde?'),
        (5, 'ar', 'من رسم الموناليزا؟'),
        (6, 'fr', 'Quelle est la plus haute montagne du monde?'),
        (6, 'ar', 'ما هو أطول جبل في العالم؟'),
        (7, 'fr', 'Quelle est la vitesse de la lumière?'),
        (7, 'ar', 'ما هي سرعة الضوء؟'),
        (8, 'fr', 'Quel est le symbole chimique de l\'or?'),
        (8, 'ar', 'ما هو الرمز الكيميائي للذهب؟'),
        (9, 'fr', 'Quel est le plus grand océan de la Terre?'),
        (9, 'ar', 'ما هو أكبر محيط على الأرض؟'),
        (10, 'fr', 'Qui a inventé le téléphone?'),
        (10, 'ar', 'من اخترع الهاتف؟')
    ]

    c.executemany('INSERT INTO QuestionTrans (question_id, language, title) VALUES (?, ?, ?)', question_translations)

    # Insert Options and Translations
    options = [
        (1, 'Paris', True),
        (1, 'London', False),
        (1, 'Rome', False),
        (1, 'Berlin', False),
        (2, '4', True),
        (2, '3', False),
        (2, '5', False),
        (2, '6', False),
        (3, 'Shakespeare', True),
        (3, 'Dickens', False),
        (3, 'Austen', False),
        (3, 'Tolkien', False),
        (4, '100°C', True),
        (4, '90°C', False),
        (4, '80°C', False),
        (4, '110°C', False),
        (5, 'Leonardo da Vinci', True),
        (5, 'Michelangelo', False),
        (5, 'Raphael', False),
        (5, 'Donatello', False),
        (6, 'Mount Everest', True),
        (6, 'K2', False),
        (6, 'Kangchenjunga', False),
        (6, 'Lhotse', False),
        (7, '299,792,458 m/s', True),
        (7, '150,000,000 m/s', False),
        (7, '3,000,000 m/s', False),
        (7, '30,000,000 m/s', False),
        (8, 'Au', True),
        (8, 'Ag', False),
        (8, 'Pb', False),
        (8, 'Fe', False),
        (9, 'Pacific Ocean', True),
        (9, 'Atlantic Ocean', False),
        (9, 'Indian Ocean', False),
        (9, 'Arctic Ocean', False),
        (10, 'Alexander Graham Bell', True),
        (10, 'Thomas Edison', False),
        (10, 'Nikola Tesla', False),
        (10, 'Guglielmo Marconi', False)
    ]

    c.executemany('INSERT INTO Options (question_id, text, is_correct) VALUES (?, ?, ?)', options)

    option_translations = [
        (1, 'fr', 'Paris'),
        (1, 'ar', 'باريس'),
        (2, 'fr', 'Londres'),
        (2, 'ar', 'لندن'),
        (3, 'fr', 'Rome'),
        (3, 'ar', 'روما'),
        (4, 'fr', 'Berlin'),
        (4, 'ar', 'برلين'),
        (5, 'fr', '4'),
        (5, 'ar', '٤'),
        (6, 'fr', '3'),
        (6, 'ar', '٣'),
        (7, 'fr', '5'),
        (7, 'ar', '٥'),
        (8, 'fr', '6'),
        (8, 'ar', '٦'),
        (9, 'fr', 'Shakespeare'),
        (9, 'ar', 'شكسبير'),
        (10, 'fr', 'Dickens'),
        (10, 'ar', 'ديكنز'),
        (11, 'fr', 'Austen'),
        (11, 'ar', 'أوستن'),
        (12, 'fr', 'Tolkien'),
        (12, 'ar', 'تولكين'),
        (13, 'fr', '100°C'),
        (13, 'ar', '١٠٠°م'),
        (14, 'fr', '90°C'),
        (14, 'ar', '٩٠°م'),
        (15, 'fr', '80°C'),
        (15, 'ar', '٨٠°م'),
        (16, 'fr', '110°C'),
        (16, 'ar', '١١٠°م'),
        (17, 'fr', 'Leonardo da Vinci'),
        (17, 'ar', 'ليوناردو دا فينشي'),
        (18, 'fr', 'Michelangelo'),
        (18, 'ar', 'ميكيلانجيلو'),
        (19, 'fr', 'Raphael'),
        (19, 'ar', 'رافائيل'),
        (20, 'fr', 'Donatello'),
        (20, 'ar', 'دوناتيلو'),
        (21, 'fr', 'Mount Everest'),
        (21, 'ar', 'جبل إيفرست'),
        (22, 'fr', 'K2'),
        (22, 'ar', 'كي٢'),
        (23, 'fr', 'Kangchenjunga'),
        (23, 'ar', 'كانغشينجونغا'),
        (24, 'fr', 'Lhotse'),
        (24, 'ar', 'لوتسي'),
        (25, 'fr', '299,792,458 m/s'),
        (25, 'ar', '٢٩٩،٧٩٢،٤٥٨ م/ث'),
        (26, 'fr', '150,000,000 m/s'),
        (26, 'ar', '١٥٠،٠٠٠،٠٠٠ م/ث'),
        (27, 'fr', '3,000,000 m/s'),
        (27, 'ar', '٣،٠٠٠،٠٠٠ م/ث'),
        (28, 'fr', '30,000,000 m/s'),
        (28, 'ar', '٣٠،٠٠٠،٠٠٠ م/ث'),
        (29, 'fr', 'Au'),
        (29, 'ar', 'أو'),
        (30, 'fr', 'Ag'),
        (30, 'ar', 'أي جي'),
        (31, 'fr', 'Pb'),
        (31, 'ar', 'بّي بّي'),
        (32, 'fr', 'Fe'),
        (32, 'ar', 'إف إي'),
        (33, 'fr', 'Pacific Ocean'),
        (33, 'ar', 'المحيط الهادئ'),
        (34, 'fr', 'Atlantic Ocean'),
        (34, 'ar', 'المحيط الأطلسي'),
        (35, 'fr', 'Indian Ocean'),
        (35, 'ar', 'المحيط الهندي'),
        (36, 'fr', 'Arctic Ocean'),
        (36, 'ar', 'المحيط المتجمد الشمالي'),
        (37, 'fr', 'Alexander Graham Bell'),
        (37, 'ar', 'ألكسندر غراهام بيل'),
        (38, 'fr', 'Thomas Edison'),
        (38, 'ar', 'توماس إديسون'),
        (39, 'fr', 'Nikola Tesla'),
        (39, 'ar', 'نيكولا تيسلا'),
        (40, 'fr', 'Guglielmo Marconi'),
        (40, 'ar', 'غولييلمو ماركوني')
    ]

    c.executemany('INSERT INTO OptionTrans (option_id, language, text) VALUES (?, ?, ?)', option_translations)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_db()
