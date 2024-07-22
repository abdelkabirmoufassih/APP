from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Quiz, Question, QuestionTranslation, Option, OptionTranslation, Attempt, Answer  # Import db from models

from datetime import datetime
import pytz 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        emp_id = request.form.get('emp_id')
        cin = request.form.get('cin')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        service = request.form.get('service')
        site = request.form.get('site')
        password = request.form.get('password')

        if not emp_id or not cin or not first_name or not last_name or not service or not site or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)

        new_user = User(emp_id=emp_id, cin=cin, first_name=first_name, last_name=last_name,
                        service=service, site=site, password=hashed_password)
        print(new_user)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return render_template('login.html')
        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            print(f"Error: {e}")
            flash('An error occurred. Please try again.', 'error')
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('home'))  
    return render_template(f'register_{session["language"]}.html')



@auth_bp.route('/login', methods=['GET'])
def login_form():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect if already logged in
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    emp_id = request.form.get('emp_id')
    password = request.form.get('password')

    user = User.query.filter_by(emp_id=emp_id).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        print('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login failed. Check your emp_id and/or password.', 'error')
        return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    print('Logged out successfully!', 'success')
    return render_template('login.html')


@auth_bp.route('/quizzes')
def quizzes():
    try:
        quizzes = Quiz.query.with_entities(Quiz.id, Quiz.title).all()
        #return render_template('quizzes.html', quizzes=quizzes)
        return render_template('explanation.html')
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching quizzes", 500

@auth_bp.route('/quiz/<int:quiz_id>')
def quiz_detail(quiz_id):
    user_id = session.get('user_id')
    if user_id:
        # Check if the user has already attempted this quiz
        attempt = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
        if attempt:
            return redirect(url_for('auth.quiz_taken'))
    language = session.get('language', 'en')  # Default to English if no language is set
    if 'start_time' not in session:
        session['start_time'] = datetime.now(pytz.utc).isoformat()
    try:
        # Fetch quiz with related questions and options, including their translations
        quiz = Quiz.query.options(
            db.joinedload(Quiz.questions).joinedload(Question.options)
        ).get_or_404(quiz_id)

        # Fetch translations for questions and options
        questions_translations = (
            QuestionTranslation.query.filter(QuestionTranslation.language == language)
            .all()
        )
        options_translations = (
            OptionTranslation.query.filter(OptionTranslation.language == language)
            .all()
        )

        # Convert translations to dictionaries for easy lookup
        questions_translations_dict = {qt.question_id: qt.title for qt in questions_translations}
        options_translations_dict = {ot.option_id: ot.text for ot in options_translations}

        # Prepare data for rendering
        quiz_data = {
            'id': quiz.id,
            'title': quiz.title,
            'questions': [
                {
                    'id': question.id,
                    'title': questions_translations_dict.get(question.id, question.title),
                    'options': [
                        {
                            'id': option.id,
                            'text': options_translations_dict.get(option.id, option.text),
                            'is_correct': option.is_correct
                        }
                        for option in question.options
                    ]
                }
                for question in quiz.questions
            ]
        }

        template_name = f'quiz_{language}.html'
        response = make_response(render_template(template_name, quiz=quiz_data,start_time=session['start_time']))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching the quiz", 500
    
@auth_bp.route('/quiz_taken')
def quiz_taken():
    return render_template('quiz_taken.html')

@auth_bp.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    user_id = session.get('user_id')
    start_time_str = session.get('start_time')  # Get start_time from session
    end_time = datetime.utcnow()

    # Check if start_time is present and is a string
    if start_time_str:
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except ValueError:
            return "Invalid start time format", 400
    else:
        return "Start time not found in session", 400

    # Define the passing score threshold (as a percentage)
    PASSING_SCORE_PERCENTAGE = 25  # Example: 25% passing score

    final_score = 0
    question_scores = {}

    try:
        # Fetch the quiz and its related data
        quiz = Quiz.query.get_or_404(quiz_id)

        # Debugging: Print the entire form data
        print("Form data:", request.form)

        for key, value in request.form.items():
            if key.startswith('question_'):
                # Debugging: Print the key being processed
                print(f"Processing key: {key}")

                # Ensure key is properly formatted
                parts = key.split('_')
                if len(parts) != 2 or not parts[1].isdigit():
                    print(f"Skipping invalid key: {key}")
                    continue

                try:
                    question_id = int(parts[1])
                except ValueError:
                    print(f"Error converting key to question ID: {key}")
                    continue  # Skip invalid keys

                selected_options = request.form.getlist(key)
                question_scores[question_id] = {'correct': 0, 'incorrect': 0}

                question = Question.query.get_or_404(question_id)
                total_options = Option.query.filter_by(question_id=question_id).count()
                correct_options_count = Option.query.filter_by(question_id=question_id, is_correct=True).count()

                for option_id in selected_options:
                    # Ensure option_id can be converted to an integer
                    try:
                        option_id = int(option_id)
                    except ValueError:
                        print(f"Invalid option ID format: {option_id}")
                        continue  # Skip invalid option IDs

                    option = Option.query.get_or_404(option_id)

                    if option.is_correct:
                        question_scores[question_id]['correct'] += 1
                    else:
                        question_scores[question_id]['incorrect'] += 1

                correct_count = question_scores[question_id]['correct']
                incorrect_count = question_scores[question_id]['incorrect']

                if incorrect_count == 0:
                    if correct_count == correct_options_count:
                        final_score += 4
                    else:
                        final_score += correct_count
                else:
                    if correct_count == 0:
                        final_score -= incorrect_count
                    else:
                        final_score += correct_count - incorrect_count

        total_questions = len(question_scores)
        max_score = total_questions * 4

        percentage_score = (final_score / max_score) * 100 if max_score > 0 else 0
        status = 'Passed' if percentage_score >= PASSING_SCORE_PERCENTAGE else 'Failed'

        attempt = Attempt(
            user_id=user_id,
            quiz_id=quiz_id,
            score=final_score,
            status=status,
            time=end_time
        )
        db.session.add(attempt)
        db.session.commit()

        attempt_id = attempt.id

        for question_id in question_scores.keys():
            selected_options = request.form.getlist(f'question_{question_id}')
            for option_id in selected_options:
                # Ensure option_id can be converted to an integer
                try:
                    option_id = int(option_id)
                except ValueError:
                    print(f"Invalid option ID format: {option_id}")
                    continue  # Skip invalid option IDs

                option = Option.query.get_or_404(option_id)
                answer = Answer(
                    attempt_id=attempt_id,
                    question_id=question_id,
                    option_id=option_id,
                    is_correct=option.is_correct
                )
                db.session.add(answer)

        db.session.commit()

        session.pop('start_time', None)  # Clear the start_time from session after submission


        # Determine the language for the finish page
        language = session.get('language', 'en')
        template_name = f'finish_{language}.html'

        # Create a response to prevent caching
        response = make_response(render_template(template_name,status=attempt.status))
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        return response
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        print(f"Error occurred: {e}")
        return "An error occurred while processing your submission", 500










@auth_bp.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    options = Option.query.all()
    users = User.query.all()  # Assuming there's a User model

    users = db.session.query(User).all()
    user_attempts = db.session.query(User, Attempt, Quiz).join(Attempt, User.id == Attempt.user_id).join(Quiz, Attempt.quiz_id == Quiz.id).all()

    quiz_data = {
        'total_quizzes': len(quizzes),
        'total_questions': len(questions),
        'total_options': len(options),
        'total_users': len(users)
    }

    return render_template('admin_dashboard.html', users=users, user_attempts=user_attempts)



@auth_bp.route('/admin/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        default_language = request.form['language']

        # Insert the quiz title
        new_quiz = Quiz(title=title, language=default_language)
        db.session.add(new_quiz)
        db.session.commit()
        quiz_id = new_quiz.id

        question_index = 1
        while f'question_text_{question_index}' in request.form:
            question_text = request.form[f'question_text_{question_index}']
            
            # Insert the question
            new_question = Question(quiz_id=quiz_id, title=question_text)
            db.session.add(new_question)
            db.session.commit()
            question_id = new_question.id
            
            # Insert translations for the question
            for lang in ['es', 'fr', 'ar']:
                trans_text = request.form.get(f'question_text_{question_index}_{lang}', '')
                if trans_text:
                    new_question_trans = QuestionTranslation(question_id=question_id, language=lang, title=trans_text)
                    db.session.add(new_question_trans)

            option_index = 1
            while f'option_text_{question_index}_{option_index}' in request.form:
                option_text = request.form[f'option_text_{question_index}_{option_index}']
                
                # Insert the option
                new_option = Option(question_id=question_id, text=option_text)
                db.session.add(new_option)
                db.session.commit()
                option_id = new_option.id

                # Insert translations for the option
                for lang in ['es', 'fr', 'ar']:
                    trans_text = request.form.get(f'option_text_{question_index}_{option_index}_{lang}', '')
                    if trans_text:
                        new_option_trans = OptionTranslation(option_id=option_id, language=lang, text=trans_text)
                        db.session.add(new_option_trans)

                # Insert correct option status
                is_correct = f'correct_{question_index}_{option_index}' in request.form
                new_option.is_correct = is_correct

                option_index += 1

            db.session.commit()
            question_index += 1

    return render_template('admin_create_quiz.html')

















