from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Quiz  # Import db from models

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
        # Fetch all quizzes using SQLAlchemy
        quizzes = Quiz.query.with_entities(Quiz.id, Quiz.title).all()
        return render_template('quizzes.html', quizzes=quizzes)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching quizzes", 500


