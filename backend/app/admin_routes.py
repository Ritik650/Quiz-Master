from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Subject, Chapter, Quiz, Question, User, Score, db
from datetime import datetime, timedelta
from sqlalchemy import func
import redis

admin_bp = Blueprint('admin', __name__)
redis_client = redis.Redis(decode_responses=True)

# def admin_required():
#     def decorator(f):
#         @jwt_required()
#         def decorated_function(*args, **kwargs):
#             claims = get_jwt()
#             if claims.get('role') != 'admin':
#                 return jsonify({'message': 'Admin access required'}), 403
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

# Subject Management
@admin_bp.route('/subjects', methods=['GET'])
# @admin_required()
def get_subjects():
    # Check cache first
    cached_subjects = redis_client.get('subjects_list')
    if cached_subjects:
        import json
        return jsonify(json.loads(cached_subjects)), 200
    
    subjects = Subject.query.filter_by(is_active=True).all()
    subjects_data = [subject.to_dict() for subject in subjects]
    
    # Cache for 5 minutes
    import json
    redis_client.setex('subjects_list', 300, json.dumps(subjects_data))
    
    return jsonify(subjects_data), 200

@admin_bp.route('/subjects', methods=['POST'])
# @admin_required()
def create_subject():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'message': 'Subject name is required'}), 400
    
    subject = Subject(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(subject)
    db.session.commit()
    
    # Clear cache
    redis_client.delete('subjects_list')
    
    return jsonify(subject.to_dict()), 201

@admin_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
# @admin_required()
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    
    db.session.commit()
    redis_client.delete('subjects_list')
    
    return jsonify(subject.to_dict()), 200

@admin_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
# @admin_required()
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    subject.is_active = False
    
    db.session.commit()
    redis_client.delete('subjects_list')
    
    return jsonify({'message': 'Subject deleted successfully'}), 200

# Chapter Management
@admin_bp.route('/subjects/<int:subject_id>/chapters', methods=['GET'])
# @admin_required()
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id, is_active=True).all()
    return jsonify([chapter.to_dict() for chapter in chapters]), 200

@admin_bp.route('/subjects/<int:subject_id>/chapters', methods=['POST'])
# @admin_required()
def create_chapter(subject_id):
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'message': 'Chapter name is required'}), 400
    
    chapter = Chapter(
        name=data['name'],
        description=data.get('description', ''),
        subject_id=subject_id
    )
    
    db.session.add(chapter)
    db.session.commit()
    
    return jsonify(chapter.to_dict()), 201

# Quiz Management
@admin_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['POST'])
# @admin_required()
def create_quiz(chapter_id):
    data = request.get_json()
    
    required_fields = ['title', 'date_of_quiz', 'time_duration']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400
    
    quiz = Quiz(
        title=data['title'],
        description=data.get('description', ''),
        chapter_id=chapter_id,
        date_of_quiz=datetime.fromisoformat(data['date_of_quiz'].replace('Z', '+00:00')),
        time_duration=data['time_duration']
    )
    
    db.session.add(quiz)
    db.session.commit()
    
    return jsonify(quiz.to_dict()), 201

# Question Management
@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])
# @admin_required()
def add_question(quiz_id):
    data = request.get_json()
    
    required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400
    
    question = Question(
        quiz_id=quiz_id,
        question_statement=data['question_statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option'],
        marks=data.get('marks', 1)
    )
    
    db.session.add(question)
    
    # Update quiz total marks
    quiz = Quiz.query.get(quiz_id)
    quiz.total_marks += question.marks
    
    db.session.commit()
    
    return jsonify(question.to_dict(include_answer=True)), 201

# Dashboard Analytics
@admin_bp.route('/dashboard/stats', methods=['GET'])
# @admin_required()
def get_dashboard_stats():
    stats = {
        'total_users': User.query.filter_by(role='user').count(),
        'total_subjects': Subject.query.filter_by(is_active=True).count(),
        'total_quizzes': Quiz.query.filter_by(is_active=True).count(),
        'total_attempts': Score.query.count(),
        'recent_scores': []
    }
    
    # Get recent quiz attempts
    recent_scores = Score.query.order_by(Score.timestamp_of_attempt.desc()).limit(10).all()
    stats['recent_scores'] = [score.to_dict() for score in recent_scores]
    
    return jsonify(stats), 200


# Add these to your admin_routes.py

@admin_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    
    db.session.commit()
    return jsonify(chapter.to_dict()), 200

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter.is_active = False
    
    db.session.commit()
    return jsonify({'message': 'Chapter deleted successfully'}), 200

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([question.to_dict(include_answer=True) for question in questions]), 200

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Update quiz total marks
    quiz = Quiz.query.get(question.quiz_id)
    quiz.total_marks -= question.marks
    
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({'message': 'Question deleted successfully'}), 200

@admin_bp.route('/chapters', methods=['GET'])
def get_all_chapters():
    chapters = Chapter.query.filter_by(is_active=True).all()
    return jsonify([chapter.to_dict() for chapter in chapters]), 200


# Add to admin_routes.py

@admin_bp.route('/quizzes', methods=['GET'])
def get_all_quizzes():
    quizzes = Quiz.query.filter_by(is_active=True).all()
    return jsonify([quiz.to_dict() for quiz in quizzes]), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    quiz.title = data.get('title', quiz.title)
    quiz.description = data.get('description', quiz.description)
    quiz.date_of_quiz = datetime.fromisoformat(data['date_of_quiz'].replace('Z', '+00:00')) if data.get('date_of_quiz') else quiz.date_of_quiz
    quiz.time_duration = data.get('time_duration', quiz.time_duration)
    
    db.session.commit()
    return jsonify(quiz.to_dict()), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.is_active = False

    db.session.commit()
    return jsonify({'message': 'Quiz deleted successfully'}), 200


# ── Analytics endpoints ───────────────────────────────────────

@admin_bp.route('/analytics/overview', methods=['GET'])
def get_analytics_overview():
    # Average score % per quiz (top 10 by attempt count)
    quiz_perf = db.session.query(
        Quiz.title,
        func.round(func.avg(Score.total_scored * 100.0 / Score.total_marks), 2).label('avg_score'),
        func.count(Score.id).label('attempts')
    ).join(Score, Quiz.id == Score.quiz_id) \
     .group_by(Quiz.id) \
     .order_by(func.count(Score.id).desc()) \
     .limit(10).all()

    # Monthly attempt counts for the last 6 months
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly = db.session.query(
        func.strftime('%Y-%m', Score.timestamp_of_attempt).label('month'),
        func.count(Score.id).label('count')
    ).filter(Score.timestamp_of_attempt >= six_months_ago) \
     .group_by(func.strftime('%Y-%m', Score.timestamp_of_attempt)) \
     .order_by(func.strftime('%Y-%m', Score.timestamp_of_attempt)).all()

    # Subject-wise average score
    subj_perf = db.session.query(
        Subject.name,
        func.round(func.avg(Score.total_scored * 100.0 / Score.total_marks), 2).label('avg_score'),
        func.count(Score.id).label('attempts')
    ).join(Chapter, Subject.id == Chapter.subject_id) \
     .join(Quiz, Chapter.id == Quiz.chapter_id) \
     .join(Score, Quiz.id == Score.quiz_id) \
     .group_by(Subject.id).all()

    # Top 5 performers by avg score
    top_users = db.session.query(
        User.id,
        User.full_name,
        func.round(func.avg(Score.total_scored * 100.0 / Score.total_marks), 2).label('avg_score'),
        func.count(Score.id).label('total_attempts')
    ).join(Score, User.id == Score.user_id) \
     .filter(User.role == 'user') \
     .group_by(User.id) \
     .order_by(func.avg(Score.total_scored * 100.0 / Score.total_marks).desc()) \
     .limit(5).all()

    # Score distribution buckets
    all_scores = Score.query.all()
    dist = {'0-40': 0, '40-70': 0, '70-100': 0}
    for s in all_scores:
        if s.total_marks > 0:
            pct = (s.total_scored / s.total_marks) * 100
            if pct < 40:
                dist['0-40'] += 1
            elif pct < 70:
                dist['40-70'] += 1
            else:
                dist['70-100'] += 1

    return jsonify({
        'quiz_performance': [
            {'quiz_title': r.title, 'avg_score': float(r.avg_score or 0), 'attempts': r.attempts}
            for r in quiz_perf
        ],
        'monthly_attempts': [
            {'month': r.month, 'count': r.count}
            for r in monthly
        ],
        'subject_performance': [
            {'subject_name': r.name, 'avg_score': float(r.avg_score or 0), 'attempts': r.attempts}
            for r in subj_perf
        ],
        'top_users': [
            {'id': r.id, 'full_name': r.full_name, 'avg_score': float(r.avg_score or 0), 'total_attempts': r.total_attempts}
            for r in top_users
        ],
        'score_distribution': dist
    }), 200


@admin_bp.route('/analytics/users', methods=['GET'])
def get_all_users_analytics():
    rows = db.session.query(
        User.id,
        User.full_name,
        User.username,
        func.count(Score.id).label('total_attempts'),
        func.round(func.avg(Score.total_scored * 100.0 / Score.total_marks), 2).label('avg_score'),
        func.max(Score.timestamp_of_attempt).label('last_attempt')
    ).outerjoin(Score, User.id == Score.user_id) \
     .filter(User.role == 'user') \
     .group_by(User.id) \
     .order_by(func.count(Score.id).desc()).all()

    return jsonify([{
        'id': r.id,
        'full_name': r.full_name,
        'username': r.username,
        'total_attempts': r.total_attempts or 0,
        'avg_score': float(r.avg_score) if r.avg_score else 0,
        'last_attempt': r.last_attempt.isoformat() if r.last_attempt else None
    } for r in rows]), 200


@admin_bp.route('/analytics/user/<int:user_id>', methods=['GET'])
def get_single_user_analytics(user_id):
    user = User.query.get_or_404(user_id)
    scores = Score.query.filter_by(user_id=user_id) \
                        .order_by(Score.timestamp_of_attempt.asc()).all()

    total = len(scores)
    avg = round(sum((s.total_scored / s.total_marks) * 100 for s in scores) / total, 2) if total else 0

    # Chronological score trend
    score_trend = [{
        'date': s.timestamp_of_attempt.strftime('%b %d'),
        'percentage': round((s.total_scored / s.total_marks) * 100, 2),
        'quiz_title': s.quiz.title
    } for s in scores if s.total_marks > 0]

    # Subject-wise average
    subj_data = {}
    for s in scores:
        if s.total_marks > 0:
            subj = s.quiz.chapter.subject.name
            subj_data.setdefault(subj, []).append((s.total_scored / s.total_marks) * 100)

    subject_performance = [
        {'subject_name': k, 'avg_score': round(sum(v) / len(v), 2)}
        for k, v in subj_data.items()
    ]

    return jsonify({
        'user': user.to_dict(),
        'total_attempts': total,
        'avg_score': avg,
        'score_trend': score_trend,
        'subject_performance': subject_performance
    }), 200
