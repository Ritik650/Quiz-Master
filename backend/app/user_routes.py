import sqlite3
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Quiz, Subject, Chapter, Score, Question, User, db
from datetime import datetime
from sqlalchemy import func

user_bp = Blueprint('user', __name__)




@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_user_dashboard():
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
    return jsonify([score.to_dict() for score in scores]), 200


@user_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_user_analytics():
    user_id = int(get_jwt_identity())
    scores = Score.query.filter_by(user_id=user_id) \
                        .order_by(Score.timestamp_of_attempt.asc()).all()

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

    # My score vs class average per quiz (up to 8 quizzes)
    attempted_quiz_ids = list({s.quiz_id for s in scores})[:8]
    comparison = []
    for qid in attempted_quiz_ids:
        my = [s for s in scores if s.quiz_id == qid]
        all_q = Score.query.filter_by(quiz_id=qid).all()
        if my and all_q:
            my_avg = sum((s.total_scored / s.total_marks) * 100 for s in my) / len(my)
            all_avg = sum((s.total_scored / s.total_marks) * 100 for s in all_q) / len(all_q)
            comparison.append({
                'quiz_title': my[0].quiz.title,
                'my_score': round(my_avg, 2),
                'avg_score': round(all_avg, 2)
            })

    return jsonify({
        'score_trend': score_trend,
        'subject_performance': subject_performance,
        'comparison': comparison
    }), 200


@user_bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """Top 10 students by average score (min 3 attempts)."""
    rows = (
        db.session.query(
            User.id,
            User.full_name,
            func.count(Score.id).label('attempts'),
            func.round(func.avg(Score.total_scored * 100.0 / Score.total_marks), 1).label('avg_score')
        )
        .join(Score, Score.user_id == User.id)
        .filter(User.role == 'user')
        .group_by(User.id)
        .having(func.count(Score.id) >= 1)
        .order_by(func.avg(Score.total_scored * 100.0 / Score.total_marks).desc())
        .limit(10)
        .all()
    )
    return jsonify([
        {'rank': i + 1, 'user_id': r.id, 'name': r.full_name,
         'attempts': r.attempts, 'avg_score': float(r.avg_score or 0)}
        for i, r in enumerate(rows)
    ]), 200


@user_bp.route('/subject-progress', methods=['GET'])
@jwt_required()
def get_subject_progress():
    """Per-subject: quizzes attempted vs total, avg score for current user."""
    user_id = int(get_jwt_identity())
    subjects = Subject.query.filter_by(is_active=True).all()
    result = []
    for subj in subjects:
        total_quizzes = sum(len(ch.quizzes) for ch in subj.chapters)
        user_scores = [
            s for ch in subj.chapters
            for q in ch.quizzes
            for s in q.scores if s.user_id == user_id
        ]
        attempted = len({s.quiz_id for s in user_scores})
        avg = round(sum((s.total_scored / s.total_marks) * 100 for s in user_scores) / len(user_scores), 1) if user_scores else 0
        result.append({
            'subject': subj.name,
            'total': total_quizzes,
            'attempted': attempted,
            'avg_score': avg,
            'pct_done': round((attempted / total_quizzes) * 100) if total_quizzes else 0
        })
    return jsonify(result), 200
