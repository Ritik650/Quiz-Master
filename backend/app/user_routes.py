import sqlite3
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Quiz, Subject, Chapter, Score, Question, db
from datetime import datetime

user_bp = Blueprint('user', __name__)




@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_user_dashboard():
    user_id = get_jwt_identity()
    print(user_id,"sdfjklskjf")
    # Get user's quiz attempts
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
    
    # Calculate statistics
    total_attempts = len(scores)
    avg_score = sum(score.total_scored / score.total_marks * 100 for score in scores) / total_attempts if total_attempts > 0 else 0
    
    dashboard_data = {
        'total_attempts': total_attempts,
        'average_score': round(avg_score, 2),
        'recent_attempts': [score.to_dict() for score in scores[:10]],
        'available_quizzes': Quiz.query.filter_by(is_active=True).count()
    }
    
    return jsonify(dashboard_data), 200



@user_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_available_subjects():
    subjects = Subject.query.filter_by(is_active=True).all()
    return jsonify([subject.to_dict() for subject in subjects]), 200

@user_bp.route('/chapters', methods=['GET'])
@jwt_required()
def get_subject_chapters():
    chapters = Chapter.query.filter_by( is_active=True).all()
    return jsonify([chapter.to_dict() for chapter in chapters]), 200

@user_bp.route('/quizzes', methods=['GET'])
@jwt_required()
def get_chapter_quizzes():
    quizzes = Quiz.query.filter_by( is_active=True).all()
    return jsonify([quiz.to_dict() for quiz in quizzes]), 200


@user_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
    return jsonify([score.to_dict() for score in scores]), 200


import io
import base64
import sqlite3
import matplotlib.pyplot as plt
from flask import send_file

# ... your existing imports and user_bp setup ...


import matplotlib.pyplot as plt
import os
from flask import send_file

@user_bp.route('/api/quiz-summary-chart')
@jwt_required()
def quiz_summary_chart():
    conn = sqlite3.connect('quiz_master.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT quiz_title, AVG(percentage)
        FROM attempts
        GROUP BY quiz_title
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        return jsonify({'error': 'No data found'}), 404

    quiz_titles = [row[0] for row in data]
    avg_scores = [row[1] for row in data]

    # Plot the bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(quiz_titles, avg_scores, color='skyblue')
    plt.xlabel('Quiz Title')
    plt.ylabel('Average Score (%)')
    plt.title('Average Score per Quiz')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save plot as image
    image_path = 'static/summary_chart.png'
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    plt.savefig(image_path)
    plt.close()

    return send_file('user/dashboard', mimetype='image/png')
