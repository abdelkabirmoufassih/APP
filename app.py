from flask import Flask, render_template, request,redirect, url_for,session
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#Client routes

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/information/<language>', methods=['GET'])
def information(language):
    session['language'] = language
    if language == "en":
        return render_template('information_en.html')
    elif language == "fr":
        return render_template('information_fr.html')
    elif language == "ar":
        return render_template('information_ar.html')
    else: 
        return("language not supported",404)

@app.route('/<language>/user', methods=['POST', 'GET'])
def submit_1(language):
    
    emp_id = request.form.get('emp_id')
    cin = request.form.get('cin')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    service = request.form.get('service')  
    site = request.form.get('site')

    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS employee_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT,
        cin TEXT,
        first_name TEXT,
        last_name TEXT,
        service TEXT,
        site TEXT
    )
    ''')
    c.execute('''
    INSERT INTO employee_info (emp_id, cin, first_name, last_name, service, site)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (emp_id, cin, first_name, last_name, service, site))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    session['user_id'] = user_id
    return redirect(url_for('quizzes'))

def get_questions_and_options(quiz_id, language):

    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    if language == 'en':
        # Fetch questions and options directly for English
        query_questions = '''
        SELECT q.id, q.title 
        FROM Questions q
        WHERE q.quiz_id = ?
        '''
        c.execute(query_questions, (quiz_id,))
        questions = c.fetchall()
        
        question_ids = [q[0] for q in questions]
        if not question_ids:
            print("No questions found.")
            return []

        query_options = f'''
        SELECT o.id, o.question_id, o.text, o.is_correct 
        FROM Options o
        WHERE o.question_id IN ({','.join('?' for _ in question_ids)})
        '''
        c.execute(query_options, question_ids)
        options = c.fetchall()
    else:
        # Fetch questions with translations for other languages
        query_questions = '''
        SELECT q.id, qt.title 
        FROM Questions q
        JOIN QuestionTrans qt ON q.id = qt.question_id
        WHERE q.quiz_id = ? AND qt.language = ?
        '''
        c.execute(query_questions, (quiz_id, language))
        questions = c.fetchall()
        # Fetch options with translations
        question_ids = [q[0] for q in questions]
        if not question_ids:
            print("No questions found.")
            return []

        query_options = f'''
        SELECT o.id, o.question_id, ot.text, o.is_correct 
        FROM Options o
        JOIN OptionTrans ot ON o.id = ot.option_id
        WHERE ot.language = ? AND o.question_id IN ({','.join('?' for _ in question_ids)})
        '''
        c.execute(query_options, [language] + question_ids)
        options = c.fetchall()

    conn.close()

    # Organize the options by question_id
    options_dict = {}
    for option_id, question_id, text, is_correct in options:
        if question_id not in options_dict:
            options_dict[question_id] = []
        options_dict[question_id].append({
            'text': text,
            'option_id': option_id,
            'is_correct': is_correct
        })

    # Combine questions and their respective options
    quiz_data = []
    for question_id, question_title in questions:
        quiz_data.append({
            'question_id': question_id,
            'question_title': question_title,
            'options': options_dict.get(question_id, [])
        })
    return quiz_data

@app.route('/quizzes')
def quizzes():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    try:
        # Fetch all quizzes
        c.execute('''
        SELECT id, title FROM Quizzes
        ''')
        quizzes = c.fetchall()
        return render_template('quizzes.html', quizzes=quizzes)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching quizzes", 500
    finally:
        conn.close()

@app.route('/quiz/<int:quiz_id>/', methods=['POST','GET'])
def quiz(quiz_id):
    language = session['language']
    if 'start_time' not in session:
        session['start_time'] = datetime.now(pytz.utc).isoformat()
    quiz_data = get_questions_and_options(quiz_id, language)
    print(quiz_data)
    if language :
        return render_template(f'quiz_{session["language"]}.html', questions=quiz_data, enumerate=enumerate, quiz_id=quiz_id,start_time=session['start_time'])
    return("language not supported",404)

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    user_id = session.get('user_id')
    start_time = datetime.fromisoformat(session.get('start_time'))
    end_time = datetime.utcnow()

    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    # Define the passing score threshold (as a percentage)
    PASSING_SCORE_PERCENTAGE = 25  # Example: 25% passing score

    # Calculate score
    final_score = 0
    question_scores = {}

    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = int(key.split('_')[1])
            selected_options = request.form.getlist(key)
            question_scores[question_id] = {'correct': 0, 'incorrect': 0}

            print(f"Processing question {question_id}")
            print(f"Selected options: {selected_options}")

            # Count correct and incorrect options
            for option_id in selected_options:
                c.execute('SELECT is_correct FROM Options WHERE id = ?', (option_id,))
                is_correct = c.fetchone()[0]

                if is_correct:
                    question_scores[question_id]['correct'] += 1
                else:
                    question_scores[question_id]['incorrect'] += 1

            correct_count = question_scores[question_id]['correct']
            incorrect_count = question_scores[question_id]['incorrect']

            # Debug prints
            print(f"Correct options count: {correct_count}")
            print(f"Incorrect options count: {incorrect_count}")

            # Determine the score for this question
            total_options = c.execute('SELECT COUNT(*) FROM Options WHERE question_id = ?', (question_id,)).fetchone()[0]
            correct_options_count = c.execute('SELECT COUNT(*) FROM Options WHERE question_id = ? AND is_correct = 1', (question_id,)).fetchone()[0]

            print(f"Total options for question {question_id}: {total_options}")
            print(f"Correct options for question {question_id}: {correct_options_count}")

            if incorrect_count == 0:
                if correct_count == correct_options_count:
                    # All correct options selected and no incorrect options
                    print("Scoring: All correct options selected")
                    final_score += 4
                else:
                    # All selected options are correct but not all correct options are selected
                    print("Scoring: Some correct options selected")
                    final_score += correct_count
            else:
                if correct_count == 0:
                    # Only incorrect options selected
                    print("Scoring: Only incorrect options selected")
                    final_score += -incorrect_count
                else:
                    # Some correct and some incorrect options selected
                    print("Scoring: Some correct and some incorrect options selected")
                    final_score += correct_count - incorrect_count

            # Debug print for final score of the question
            print(f"Score for question {question_id}: {final_score}")

    # Calculate total possible score
    total_questions = len(question_scores)
    max_score = total_questions * 4  # 4 points per question

    # Calculate percentage of score
    if max_score > 0:
        percentage_score = (final_score / max_score) * 100
    else:
        percentage_score = 0

    # Determine if the user passes or fails
    status = 'Passed' if percentage_score >= PASSING_SCORE_PERCENTAGE else 'Failed'

    # Debug print for final score and percentage
    print(f"Total Score: {final_score}")
    print(f"Max Score: {max_score}")
    print(f"Percentage Score: {percentage_score:.2f}%")
    print(f"Passing Percentage: {PASSING_SCORE_PERCENTAGE}%")
    print(f"Status: {status}")

    # Debug print before insertion
    print(f"Inserting into Attempts with status: {status}")

    # Insert attempt into the database
    c.execute('''
    INSERT INTO Attempts (user_id, quiz_id, score, status, time)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, quiz_id, final_score, status, end_time))
    attempt_id = c.lastrowid

    # Debug print after insertion
    c.execute('SELECT * FROM Attempts WHERE id = ?', (attempt_id,))
    attempt_record = c.fetchone()
    print(f"Inserted attempt record: {attempt_record}")

    # Insert answers into the database
    for question_id in question_scores.keys():
        selected_options = request.form.getlist(f'question_{question_id}')
        for option_id in selected_options:
            c.execute('SELECT is_correct FROM Options WHERE id = ?', (option_id,))
            is_correct = c.fetchone()[0]
            c.execute('''
            INSERT INTO Answers (attempt_id, question_id, option_id, is_correct)
            VALUES (?, ?, ?, ?)
            ''', (attempt_id, question_id, option_id, is_correct))

    conn.commit()
    conn.close()

    session.pop('start_time', None)  # Clear the start_time from session after submission

    return redirect(url_for('results', attempt_id=attempt_id))


@app.route('/results/<int:attempt_id>')
def results(attempt_id):
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    try:
        # Fetch attempt details
        c.execute('''
        SELECT quiz_id, score, status, time FROM Attempts WHERE id = ?
        ''', (attempt_id,))
        attempt = c.fetchone()
        if attempt is None:
            return "Attempt not found", 404

        quiz_id, score, status, time = attempt

        # Fetch questions, selected options, and correctness with language support
        c.execute('''
        SELECT q.id AS question_id, 
               COALESCE(qt.title, q.title) AS question_title, 
               o.id AS option_id, 
               COALESCE(ot.text, o.text) AS option_text, 
               a.is_correct
        FROM Answers a
        JOIN Questions q ON a.question_id = q.id
        JOIN Options o ON a.option_id = o.id
        LEFT JOIN QuestionTrans qt ON q.id = qt.question_id AND qt.language = 'ar'
        LEFT JOIN OptionTrans ot ON o.id = ot.option_id AND ot.language = 'ar'
        WHERE a.attempt_id = ?
        ''', (attempt_id,))
        results = c.fetchall()

        # Convert the results to a list of dictionaries
        answers = []
        for row in results:
            answer = {
                'question_id': row[0],
                'question_title': row[1],
                'option_id': row[2],
                'option_text': row[3],
                'is_correct': row[4]
            }
            answers.append(answer)

        # Fetch quiz title and passing grade
        c.execute('''
        SELECT title, passing_grade FROM Quizzes WHERE id = ?
        ''', (quiz_id,))
        quiz_info = c.fetchone()
        quiz_title = quiz_info[0]
        passing_grade = quiz_info[1]

        # Return the results to the template
        return render_template(f'finish_{session["language"]}.html', quiz_title=quiz_title, score=score, status=status, time=time, answers=answers)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching results", 500
    finally:
        conn.close()


@app.route('/graphs')
def graph():
    conn = sqlite3.connect('quiz_results.db')
    df = pd.read_sql_query("SELECT * from results", conn)
    conn.close()
    fig_individual = px.bar(df, x=df.index, y='success_percentage', title='Individual Success Percentage')
    fig_individual.update_layout(xaxis_title='Employee', yaxis_title='Success Percentage')

    avg_success_percentage = df['success_percentage'].mean()
    fig_all = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_success_percentage,
        title={'text': "Average Success Percentage"},
        gauge={'axis': {'range': [None, 100]}}
    ))
    individual_graph = fig_individual.to_html(full_html=False)
    all_graph = fig_all.to_html(full_html=False)
    pie_charts = {}
    for employee_id in df['emp_id'].unique():
        employee_data = df[df['emp_id'] == employee_id].iloc[0]
        labels = ['Correct', 'Wrong']
        values = [employee_data['correct'], employee_data['wrong']]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title_text=f'Employee {employee_id} Results')
        pie_charts[employee_id] = fig.to_html(full_html=False)
    return render_template('graphs.html', individual_graph=individual_graph, all_graph=all_graph,pie_charts=pie_charts)

@app.route('/export')
def export():
    conn = sqlite3.connect('quiz_results.db')
    df = pd.read_sql_query("SELECT * FROM results", conn)
    df.to_csv('results.csv', index=False)
    conn.close()
    return 'Results exported to results.csv'

@app.route('/view_results')
def view_results():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    c.execute('SELECT * FROM results')
    rows = c.fetchall()
    conn.close()
    return render_template('view_results.html', results=rows)


#Boss routes
@app.route('/admin/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        default_language = request.form['language']

        conn = sqlite3.connect('quiz_results.db')
        c = conn.cursor()

        # Insert the quiz title
        c.execute('INSERT INTO Quizzes (title, language) VALUES (?, ?)', (title, default_language))
        quiz_id = c.lastrowid

        question_index = 1
        while f'question_text_{question_index}' in request.form:
            question_text = request.form[f'question_text_{question_index}']
            
            # Insert the question
            c.execute('INSERT INTO Questions (quiz_id, title) VALUES (?, ?)', (quiz_id, question_text))
            question_id = c.lastrowid
            
            # Insert translations for the question
            for lang in ['es', 'fr', 'ar']:
                trans_text = request.form.get(f'question_text_{question_index}_{lang}', '')
                if trans_text:
                    c.execute('INSERT INTO QuestionTrans (question_id, language, title) VALUES (?, ?, ?)', 
                              (question_id, lang, trans_text))

            option_index = 1
            while f'option_text_{question_index}_{option_index}' in request.form:
                option_text = request.form[f'option_text_{question_index}_{option_index}']
                
                # Insert the option
                c.execute('INSERT INTO Options (question_id, text) VALUES (?, ?)', (question_id, option_text))
                option_id = c.lastrowid

                # Insert translations for the option
                for lang in ['es', 'fr', 'ar']:
                    trans_text = request.form.get(f'option_text_{question_index}_{option_index}_{lang}', '')
                    if trans_text:
                        c.execute('INSERT INTO OptionTrans (option_id, language, text) VALUES (?, ?, ?)', 
                                  (option_id, lang, trans_text))

                # Insert correct option status
                is_correct = f'correct_{question_index}_{option_index}' in request.form
                c.execute('UPDATE Options SET is_correct = ? WHERE id = ?', (is_correct, option_id))

                option_index += 1

            question_index += 1

        conn.commit()
        conn.close()
    return render_template('admin_create_quiz.html')

@app.route('/clear_all')
def clear_all():
    session.clear()  # Clear all session data
    return render_template('landing.html')