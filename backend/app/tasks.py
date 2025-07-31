from flask_mail import Message
from datetime import datetime, timedelta
from io import StringIO
import csv
from .models import db, User, Quiz, Score
from app import create_app, db, mail
from celery_worker import celery
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

app = create_app()
app.app_context().push()

@celery.task
def send_daily_reminders():
    users = User.query.all()
    for user in users:
        msg = Message("Daily Quiz Reminder",  recipients=[user.email])
        msg.body = "Reminder: You haven't attempted a quiz recently."
        mail.send(msg)

@celery.task
def send_monthly_report():
    users = User.query.all()
    for user in users:
        msg = Message("Monthly Report",  recipients=[user.email])
        msg.body = f"Your quiz performance summary for the month."
        mail.send(msg)

@celery.task
@jwt_required()
def export_user_csv():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    quizzes = Score.query.filter_by(user_id=user_id).all()
    user_email = user.email if user else None
    # Query quizzes attempted by this user
    scores = Score.query.filter_by(user_id=user_id).join(Quiz).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # CSV Header
    writer.writerow([
        'Quiz ID', 'Quiz Title', 'Chapter ID', 'Chapter Name',
        'Subject Name', 'Date of Quiz', 'Score'
    ])
    
    for score in scores:
        quiz = score.quiz
        chapter = quiz.chapter
        subject = chapter.subject
        writer.writerow([
            quiz.id,
            quiz.title,
            chapter.id,
            chapter.name,
            subject.name,
            quiz.date_of_quiz.strftime('%Y-%m-%d'),
            score.total_scored,
            # score.remarks or ''
        ])
    
    output.seek(0)
    
    # Send email with CSV
    msg = Message(
        subject="Your Quiz Report CSV Export",
        sender="your-email@gmail.com",
        recipients=[user_email]
    )
    msg.body = "Attached is your exported CSV of attempted quizzes."
    msg.attach("quiz_report.csv", "text/csv", output.getvalue())
    
    mail.send(msg)
    return jsonify({'message': 'CSV export task initiated'}), 200
