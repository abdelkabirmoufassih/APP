import sqlite3
import hashlib


def populate_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert Quizzes
    quizzes = [
        ('General Knowledge Quiz', 'en'),
        ('Science Quiz', 'en'),
        ('History Quiz', 'en'),
        ('Geography Quiz', 'en')
    ]
    c.executemany('INSERT INTO Quizzes (title, language) VALUES (?, ?)', quizzes)

    # Get Quiz IDs
    c.execute('SELECT id FROM Quizzes WHERE title="General Knowledge Quiz"')
    general_knowledge_quiz_id = c.fetchone()[0]

    c.execute('SELECT id FROM Quizzes WHERE title="Science Quiz"')
    science_quiz_id = c.fetchone()[0]

    c.execute('SELECT id FROM Quizzes WHERE title="History Quiz"')
    history_quiz_id = c.fetchone()[0]

    c.execute('SELECT id FROM Quizzes WHERE title="Geography Quiz"')
    geography_quiz_id = c.fetchone()[0]

    # Insert Questions
    questions = [
        (general_knowledge_quiz_id, 'What is the capital of France?'),
        (general_knowledge_quiz_id, 'How many continents are there on Earth?'),
        (general_knowledge_quiz_id, 'Who wrote "Romeo and Juliet"?'),
        (general_knowledge_quiz_id, 'What is the boiling point of water?'),
        (general_knowledge_quiz_id, 'Who painted the Mona Lisa?'),
        (science_quiz_id, 'What is the tallest mountain in the world?'),
        (science_quiz_id, 'What is the speed of light?'),
        (science_quiz_id, 'What is the chemical symbol for gold?'),
        (science_quiz_id, 'What is the largest ocean on Earth?'),
        (science_quiz_id, 'Who invented the telephone?'),
        (history_quiz_id, 'Who was the first president of the United States?'),
        (history_quiz_id, 'In which year did World War II end?'),
        (history_quiz_id, 'Who discovered America?'),
        (history_quiz_id, 'Who was the first man to walk on the moon?'),
        (history_quiz_id, 'Which ancient civilization built the pyramids?'),
        (geography_quiz_id, 'What is the longest river in the world?'),
        (geography_quiz_id, 'Which continent is known as the Dark Continent?'),
        (geography_quiz_id, 'What is the largest desert in the world?'),
        (geography_quiz_id, 'Which country has the most natural lakes?'),
        (geography_quiz_id, 'What is the smallest country in the world?')
    ]
    c.executemany('INSERT INTO Questions (quiz_id, title) VALUES (?, ?)', questions)

    # Get Question IDs
    c.execute('SELECT id FROM Questions')
    question_ids = c.fetchall()

    question_translations = [
        (question_ids[0][0], 'fr', 'Quelle est la capitale de la France?'),
        (question_ids[0][0], 'ar', 'ما هي عاصمة فرنسا؟'),
        (question_ids[1][0], 'fr', 'Combien y a-t-il de continents sur Terre?'),
        (question_ids[1][0], 'ar', 'كم عدد القارات الموجودة على الأرض؟'),
        (question_ids[2][0], 'fr', 'Qui a écrit "Roméo et Juliette"?'),
        (question_ids[2][0], 'ar', 'من كتب "روميو وجولييت"؟'),
        (question_ids[3][0], 'fr', 'Quel est le point d\'ébullition de l\'eau?'),
        (question_ids[3][0], 'ar', 'ما هي درجة غليان الماء؟'),
        (question_ids[4][0], 'fr', 'Qui a peint la Joconde?'),
        (question_ids[4][0], 'ar', 'من رسم الموناليزا؟'),
        (question_ids[5][0], 'fr', 'Quelle est la plus haute montagne du monde?'),
        (question_ids[5][0], 'ar', 'ما هو أطول جبل في العالم؟'),
        (question_ids[6][0], 'fr', 'Quelle est la vitesse de la lumière?'),
        (question_ids[6][0], 'ar', 'ما هي سرعة الضوء؟'),
        (question_ids[7][0], 'fr', 'Quel est le symbole chimique de l\'or?'),
        (question_ids[7][0], 'ar', 'ما هو الرمز الكيميائي للذهب؟'),
        (question_ids[8][0], 'fr', 'Quel est le plus grand océan sur Terre?'),
        (question_ids[8][0], 'ar', 'ما هو أكبر محيط على الأرض؟'),
        (question_ids[9][0], 'fr', 'Qui a inventé le téléphone?'),
        (question_ids[9][0], 'ar', 'من اخترع الهاتف؟'),
        (question_ids[10][0], 'fr', 'Qui a été le premier président des États-Unis?'),
        (question_ids[10][0], 'ar', 'من كان أول رئيس للولايات المتحدة؟'),
        (question_ids[11][0], 'fr', 'En quelle année la Seconde Guerre mondiale s\'est-elle terminée?'),
        (question_ids[11][0], 'ar', 'في أي عام انتهت الحرب العالمية الثانية؟'),
        (question_ids[12][0], 'fr', 'Qui a découvert l\'Amérique?'),
        (question_ids[12][0], 'ar', 'من اكتشف أمريكا؟'),
        (question_ids[13][0], 'fr', 'Qui a été le premier homme à marcher sur la lune?'),
        (question_ids[13][0], 'ar', 'من كان أول رجل خطا على القمر؟'),
        (question_ids[14][0], 'fr', 'Quelle ancienne civilisation a construit les pyramides?'),
        (question_ids[14][0], 'ar', 'ما هي الحضارة القديمة التي بنت الأهرامات؟'),
        (question_ids[15][0], 'fr', 'Quel est le plus long fleuve du monde?'),
        (question_ids[15][0], 'ar', 'ما هو أطول نهر في العالم؟'),
        (question_ids[16][0], 'fr', 'Quel continent est connu sous le nom de continent noir?'),
        (question_ids[16][0], 'ar', 'ما هو القارة المعروفة باسم القارة السوداء؟'),
        (question_ids[17][0], 'fr', 'Quel est le plus grand désert du monde?'),
        (question_ids[17][0], 'ar', 'ما هو أكبر صحراء في العالم؟'),
        (question_ids[18][0], 'fr', 'Quel pays a le plus de lacs naturels?'),
        (question_ids[18][0], 'ar', 'ما هي الدولة التي تحتوي على أكبر عدد من البحيرات الطبيعية؟'),
        (question_ids[19][0], 'fr', 'Quel est le plus petit pays du monde?'),
        (question_ids[19][0], 'ar', 'ما هي أصغر دولة في العالم؟')
    ]
    c.executemany('INSERT INTO QuestionTrans (question_id, language, title) VALUES (?, ?, ?)', question_translations)

    options = [
        (question_ids[0][0], 'Paris', True),
        (question_ids[0][0], 'London', False),
        (question_ids[0][0], 'Berlin', False),
        (question_ids[0][0], 'Madrid', False),
        (question_ids[1][0], '7', True),
        (question_ids[1][0], '6', False),
        (question_ids[1][0], '5', False),
        (question_ids[1][0], '8', False),
        (question_ids[2][0], 'William Shakespeare', True),
        (question_ids[2][0], 'Charles Dickens', False),
        (question_ids[2][0], 'Ernest Hemingway', False),
        (question_ids[2][0], 'J.R.R. Tolkien', False),
        (question_ids[3][0], '100°C', True),
        (question_ids[3][0], '90°C', False),
        (question_ids[3][0], '80°C', False),
        (question_ids[3][0], '110°C', False),
        (question_ids[4][0], 'Leonardo da Vinci', True),
        (question_ids[4][0], 'Michelangelo', False),
        (question_ids[4][0], 'Raphael', False),
        (question_ids[4][0], 'Donatello', False),
        (question_ids[5][0], 'Mount Everest', True),
        (question_ids[5][0], 'K2', False),
        (question_ids[5][0], 'Kangchenjunga', False),
        (question_ids[5][0], 'Lhotse', False),
        (question_ids[6][0], '299,792,458 m/s', True),
        (question_ids[6][0], '150,000,000 m/s', False),
        (question_ids[6][0], '3,000,000 m/s', False),
        (question_ids[6][0], '30,000,000 m/s', False),
        (question_ids[7][0], 'Au', True),
        (question_ids[7][0], 'Ag', False),
        (question_ids[7][0], 'Pb', False),
        (question_ids[7][0], 'Fe', False),
        (question_ids[8][0], 'Pacific Ocean', True),
        (question_ids[8][0], 'Atlantic Ocean', False),
        (question_ids[8][0], 'Indian Ocean', False),
        (question_ids[8][0], 'Arctic Ocean', False),
        (question_ids[9][0], 'Alexander Graham Bell', True),
        (question_ids[9][0], 'Thomas Edison', False),
        (question_ids[9][0], 'Nikola Tesla', False),
        (question_ids[9][0], 'Guglielmo Marconi', False),
        (question_ids[10][0], 'George Washington', True),
        (question_ids[10][0], 'Thomas Jefferson', False),
        (question_ids[10][0], 'John Adams', False),
        (question_ids[10][0], 'James Madison', False),
        (question_ids[11][0], '1945', True),
        (question_ids[11][0], '1939', False),
        (question_ids[11][0], '1944', False),
        (question_ids[11][0], '1946', False),
        (question_ids[12][0], 'Christopher Columbus', True),
        (question_ids[12][0], 'Ferdinand Magellan', False),
        (question_ids[12][0], 'James Cook', False),
        (question_ids[12][0], 'Leif Erikson', False),
        (question_ids[13][0], 'Neil Armstrong', True),
        (question_ids[13][0], 'Buzz Aldrin', False),
        (question_ids[13][0], 'Yuri Gagarin', False),
        (question_ids[13][0], 'Michael Collins', False),
        (question_ids[14][0], 'Ancient Egyptians', True),
        (question_ids[14][0], 'Romans', False),
        (question_ids[14][0], 'Greeks', False),
        (question_ids[14][0], 'Mayans', False),
        (question_ids[15][0], 'Nile', True),
        (question_ids[15][0], 'Amazon', False),
        (question_ids[15][0], 'Yangtze', False),
        (question_ids[15][0], 'Mississippi', False),
        (question_ids[16][0], 'Africa', True),
        (question_ids[16][0], 'Asia', False),
        (question_ids[16][0], 'South America', False),
        (question_ids[16][0], 'Europe', False),
        (question_ids[17][0], 'Sahara', True),
        (question_ids[17][0], 'Gobi', False),
        (question_ids[17][0], 'Kalahari', False),
        (question_ids[17][0], 'Arabian', False),
        (question_ids[18][0], 'Canada', True),
        (question_ids[18][0], 'USA', False),
        (question_ids[18][0], 'Russia', False),
        (question_ids[18][0], 'Brazil', False),
        (question_ids[19][0], 'Vatican City', True),
        (question_ids[19][0], 'Monaco', False),
        (question_ids[19][0], 'San Marino', False),
        (question_ids[19][0], 'Liechtenstein', False)
    ]
    c.executemany('INSERT INTO Options (question_id, text, is_correct) VALUES (?, ?, ?)', options)

    # Get Option IDs
    c.execute('SELECT id FROM Options')
    option_ids = c.fetchall()

    option_translations = [
        (option_ids[0][0], 'fr', 'Paris'),
        (option_ids[0][0], 'ar', 'باريس'),
        (option_ids[1][0], 'fr', 'Londres'),
        (option_ids[1][0], 'ar', 'لندن'),
        (option_ids[2][0], 'fr', 'Berlin'),
        (option_ids[2][0], 'ar', 'برلين'),
        (option_ids[3][0], 'fr', 'Madrid'),
        (option_ids[3][0], 'ar', 'مدريد'),
        (option_ids[4][0], 'fr', '7'),
        (option_ids[4][0], 'ar', '٧'),
        (option_ids[5][0], 'fr', '6'),
        (option_ids[5][0], 'ar', '٦'),
        (option_ids[6][0], 'fr', '5'),
        (option_ids[6][0], 'ar', '٥'),
        (option_ids[7][0], 'fr', '8'),
        (option_ids[7][0], 'ar', '٨'),
        (option_ids[8][0], 'fr', 'William Shakespeare'),
        (option_ids[8][0], 'ar', 'وليام شكسبير'),
        (option_ids[9][0], 'fr', 'Charles Dickens'),
        (option_ids[9][0], 'ar', 'تشارلز ديكنز'),
        (option_ids[10][0], 'fr', 'Ernest Hemingway'),
        (option_ids[10][0], 'ar', 'إرنست هيمنجواي'),
        (option_ids[11][0], 'fr', 'J.R.R. Tolkien'),
        (option_ids[11][0], 'ar', 'جي. آر. آر. تولكين'),
        (option_ids[12][0], 'fr', '100°C'),
        (option_ids[12][0], 'ar', '١٠٠°م'),
        (option_ids[13][0], 'fr', '90°C'),
        (option_ids[13][0], 'ar', '٩٠°م'),
        (option_ids[14][0], 'fr', '80°C'),
        (option_ids[14][0], 'ar', '٨٠°م'),
        (option_ids[15][0], 'fr', '110°C'),
        (option_ids[15][0], 'ar', '١١٠°م'),
        (option_ids[16][0], 'fr', 'Leonardo da Vinci'),
        (option_ids[16][0], 'ar', 'ليوناردو دافنشي'),
        (option_ids[17][0], 'fr', 'Michelangelo'),
        (option_ids[17][0], 'ar', 'مايكل أنجلو'),
        (option_ids[18][0], 'fr', 'Raphael'),
        (option_ids[18][0], 'ar', 'رافائيل'),
        (option_ids[19][0], 'fr', 'Donatello'),
        (option_ids[19][0], 'ar', 'دوناتيلو'),
        (option_ids[20][0], 'fr', 'Mount Everest'),
        (option_ids[20][0], 'ar', 'قمة ايفرست'),
        (option_ids[21][0], 'fr', 'K2'),
        (option_ids[21][0], 'ar', 'كي٢'),
        (option_ids[22][0], 'fr', 'Kangchenjunga'),
        (option_ids[22][0], 'ar', 'كانغشينجونغا'),
        (option_ids[23][0], 'fr', 'Lhotse'),
        (option_ids[23][0], 'ar', 'لوتسي'),
        (option_ids[24][0], 'fr', '299,792,458 m/s'),
        (option_ids[24][0], 'ar', '٢٩٩٬٧٩٢٬٤٥٨ م/ث'),
        (option_ids[25][0], 'fr', '150,000,000 m/s'),
        (option_ids[25][0], 'ar', '١٥٠٬٠٠٠٬٠٠٠ م/ث'),
        (option_ids[26][0], 'fr', '3,000,000 m/s'),
        (option_ids[26][0], 'ar', '٣٬٠٠٠٬٠٠٠ م/ث'),
        (option_ids[27][0], 'fr', '30,000,000 m/s'),
        (option_ids[27][0], 'ar', '٣٠٬٠٠٠٬٠٠٠ م/ث'),
        (option_ids[28][0], 'fr', 'Au'),
        (option_ids[28][0], 'ar', 'Au'),
        (option_ids[29][0], 'fr', 'Ag'),
        (option_ids[29][0], 'ar', 'Ag'),
        (option_ids[30][0], 'fr', 'Pb'),
        (option_ids[30][0], 'ar', 'Pb'),
        (option_ids[31][0], 'fr', 'Fe'),
        (option_ids[31][0], 'ar', 'Fe'),
        (option_ids[32][0], 'fr', 'Pacific Ocean'),
        (option_ids[32][0], 'ar', 'المحيط الهادي'),
        (option_ids[33][0], 'fr', 'Atlantic Ocean'),
        (option_ids[33][0], 'ar', 'المحيط الأطلسي'),
        (option_ids[34][0], 'fr', 'Indian Ocean'),
        (option_ids[34][0], 'ar', 'المحيط الهندي'),
        (option_ids[35][0], 'fr', 'Arctic Ocean'),
        (option_ids[35][0], 'ar', 'المحيط المتجمد الشمالي'),
        (option_ids[36][0], 'fr', 'Alexander Graham Bell'),
        (option_ids[36][0], 'ar', 'ألكسندر جراهام بيل'),
        (option_ids[37][0], 'fr', 'Thomas Edison'),
        (option_ids[37][0], 'ar', 'توماس إديسون'),
        (option_ids[38][0], 'fr', 'Nikola Tesla'),
        (option_ids[38][0], 'ar', 'نيكولا تيسلا'),
        (option_ids[39][0], 'fr', 'Guglielmo Marconi'),
        (option_ids[39][0], 'ar', 'غوليلمو ماركوني'),
        (option_ids[40][0], 'fr', 'George Washington'),
        (option_ids[40][0], 'ar', 'جورج واشنطن'),
        (option_ids[41][0], 'fr', 'Thomas Jefferson'),
        (option_ids[41][0], 'ar', 'توماس جيفرسون'),
        (option_ids[42][0], 'fr', 'John Adams'),
        (option_ids[42][0], 'ar', 'جون آدامز'),
        (option_ids[43][0], 'fr', 'James Madison'),
        (option_ids[43][0], 'ar', 'جيمس ماديسون'),
        (option_ids[44][0], 'fr', '1945'),
        (option_ids[44][0], 'ar', '١٩٤٥'),
        (option_ids[45][0], 'fr', '1939'),
        (option_ids[45][0], 'ar', '١٩٣٩'),
        (option_ids[46][0], 'fr', '1944'),
        (option_ids[46][0], 'ar', '١٩٤٤'),
        (option_ids[47][0], 'fr', '1946'),
        (option_ids[47][0], 'ar', '١٩٤٦'),
        (option_ids[48][0], 'fr', 'Christopher Columbus'),
        (option_ids[48][0], 'ar', 'كريستوفر كولومبوس'),
        (option_ids[49][0], 'fr', 'Ferdinand Magellan'),
        (option_ids[49][0], 'ar', 'فرناندو ماجلان'),
        (option_ids[50][0], 'fr', 'James Cook'),
        (option_ids[50][0], 'ar', 'جيمس كوك'),
        (option_ids[51][0], 'fr', 'Leif Erikson'),
        (option_ids[51][0], 'ar', 'ليف إريكسون'),
        (option_ids[52][0], 'fr', 'Neil Armstrong'),
        (option_ids[52][0], 'ar', 'نيل أرمسترونج'),
        (option_ids[53][0], 'fr', 'Buzz Aldrin'),
        (option_ids[53][0], 'ar', 'باز ألدرين'),
        (option_ids[54][0], 'fr', 'Yuri Gagarin'),
        (option_ids[54][0], 'ar', 'يوري جاجارين'),
        (option_ids[55][0], 'fr', 'Michael Collins'),
        (option_ids[55][0], 'ar', 'مايكل كولينز'),
        (option_ids[56][0], 'fr', 'Ancient Egyptians'),
        (option_ids[56][0], 'ar', 'المصريون القدماء'),
        (option_ids[57][0], 'fr', 'Romans'),
        (option_ids[57][0], 'ar', 'الرومان'),
        (option_ids[58][0], 'fr', 'Greeks'),
        (option_ids[58][0], 'ar', 'اليونانيون'),
        (option_ids[59][0], 'fr', 'Mayans'),
        (option_ids[59][0], 'ar', 'المايا'),
        (option_ids[60][0], 'fr', 'Nile'),
        (option_ids[60][0], 'ar', 'النيل'),
        (option_ids[61][0], 'fr', 'Amazon'),
        (option_ids[61][0], 'ar', 'الأمازون'),
        (option_ids[62][0], 'fr', 'Yangtze'),
        (option_ids[62][0], 'ar', 'يانغتسي'),
        (option_ids[63][0], 'fr', 'Mississippi'),
        (option_ids[63][0], 'ar', 'المسيسبي'),
        (option_ids[64][0], 'fr', 'Africa'),
        (option_ids[64][0], 'ar', 'أفريقيا'),
        (option_ids[65][0], 'fr', 'Asia'),
        (option_ids[65][0], 'ar', 'آسيا'),
        (option_ids[66][0], 'fr', 'South America'),
        (option_ids[66][0], 'ar', 'أمريكا الجنوبية'),
        (option_ids[67][0], 'fr', 'Europe'),
        (option_ids[67][0], 'ar', 'أوروبا'),
        (option_ids[68][0], 'fr', 'Sahara'),
        (option_ids[68][0], 'ar', 'الصحراء الكبرى'),
        (option_ids[69][0], 'fr', 'Gobi'),
        (option_ids[69][0], 'ar', 'جوبي'),
        (option_ids[70][0], 'fr', 'Kalahari'),
        (option_ids[70][0], 'ar', 'كالاهاري'),
        (option_ids[71][0], 'fr', 'Arabian'),
        (option_ids[71][0], 'ar', 'العربية'),
        (option_ids[72][0], 'fr', 'Canada'),
        (option_ids[72][0], 'ar', 'كندا'),
        (option_ids[73][0], 'fr', 'USA'),
        (option_ids[73][0], 'ar', 'الولايات المتحدة'),
        (option_ids[74][0], 'fr', 'Russia'),
        (option_ids[74][0], 'ar', 'روسيا'),
        (option_ids[75][0], 'fr', 'Brazil'),
        (option_ids[75][0], 'ar', 'البرازيل'),
        (option_ids[76][0], 'fr', 'Vatican City'),
        (option_ids[76][0], 'ar', 'مدينة الفاتيكان'),
        (option_ids[77][0], 'fr', 'Monaco'),
        (option_ids[77][0], 'ar', 'موناكو'),
        (option_ids[78][0], 'fr', 'San Marino'),
        (option_ids[78][0], 'ar', 'سان مارينو'),
        (option_ids[79][0], 'fr', 'Liechtenstein'),
        (option_ids[79][0], 'ar', 'ليختنشتاين')
    ]
    c.executemany('INSERT INTO OptionTrans (option_id, language, text) VALUES (?, ?, ?)', option_translations)

    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    populate_db()