def calculate_passing_grade(quiz_id):
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    # Fetch the total number of questions for the quiz
    c.execute('SELECT COUNT(*) FROM Questions WHERE quiz_id = ?', (quiz_id,))
    total_questions = c.fetchone()[0]

    # Assuming each question can yield a maximum of 4 points
    max_points = total_questions * 4

    # Calculate the passing grade (e.g., 60% of max points)
    passing_grade = int(max_points * 0.6)

    # Update the passing grade in the Quizzes table
    c.execute('UPDATE Quizzes SET passing_grade = ? WHERE id = ?', (passing_grade, quiz_id))

    conn.commit()
    conn.close()

# Call this function when creating or updating a quiz
calculate_passing_grade(quiz_id)