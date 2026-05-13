# Quiz Master V2

A full-stack web application for creating and taking quizzes, with role-based access for administrators and students, analytics dashboards, and a live leaderboard.

---

## Features

### Student
- Browse quizzes organised by subject and chapter
- Timed exam interface with question palette and live countdown
- Instant results with per-question answer review
- Personal analytics: score trend, subject performance, comparison with class average
- Subject progress tracking and leaderboard

### Admin
- Full CRUD for subjects, chapters, quizzes, and questions
- Platform analytics with charts: quiz performance, monthly activity, score distribution
- Individual student drill-down with attempt history and subject breakdown

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, Vuex 4, Vue Router 4 |
| UI | Bootstrap 5.3, custom CSS design system |
| Charts | Chart.js 4, vue-chartjs 5 |
| HTTP client | Axios |
| Backend | Flask 2.3, Flask-JWT-Extended 4.5 |
| Database | SQLite via Flask-SQLAlchemy |
| Auth | JWT Bearer tokens (24h expiry) |
| Caching | Redis (5-min TTL on subject listings) |
| Password hashing | bcrypt |
| Async tasks | Celery + Flask-Mail |

---

## Project Structure

```
MAD2_23f2004634/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # App factory, JWT config, CORS, error handlers
│   │   ├── models.py          # User, Subject, Chapter, Quiz, Question, Score
│   │   ├── auth.py            # /api/auth — login, register
│   │   ├── admin_routes.py    # /api/admin — CRUD + analytics
│   │   ├── user_routes.py     # /api/user — dashboard, quizzes, leaderboard
│   │   └── quiz_routes.py     # /api/quiz — start, submit, results
│   ├── seed.py                # Populates DB with sample data
│   └── run.py                 # Entry point
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── style.css          # Global CSS custom properties
│   │   ├── store/index.js     # Vuex — auth state, axios defaults
│   │   ├── router/index.js    # Routes with JWT role guards
│   │   ├── layouts/
│   │   │   ├── AdminLayout.vue
│   │   │   └── UserLayout.vue
│   │   └── views/
│   │       ├── Login.vue
│   │       ├── Register.vue
│   │       ├── admin/
│   │       │   ├── Dashboard.vue
│   │       │   ├── SubjectManagement.vue
│   │       │   ├── ChapterManagement.vue
│   │       │   ├── QuizManagement.vue
│   │       │   └── Analytics.vue
│   │       └── user/
│   │           ├── Dashboard.vue
│   │           ├── QuizList.vue
│   │           ├── TakeQuiz.vue
│   │           └── QuizResults.vue
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── requirements.txt
└── README.md
```
**SnapShots:-**
Admin Dashboard
<img width="1919" height="917" alt="image" src="https://github.com/user-attachments/assets/f7a4463d-a4e7-43a6-b661-8f655883b9ce" />
<img width="1919" height="908" alt="image" src="https://github.com/user-attachments/assets/f6952419-1fa6-4eb1-aad0-9f14c5d6492e" />
<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/f04c2f6e-09f3-4e13-a4a5-57464dc2a2e1" />
<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/4e73c286-1ba9-46f2-9b51-b43d120754f4" />

User Dashboard:-
<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/2164f044-d95e-4be1-8168-deafa49e282d" />
<img width="1919" height="912" alt="image" src="https://github.com/user-attachments/assets/c98b9872-a801-4d75-81e3-13cb35e56f54" />
<img width="1919" height="911" alt="image" src="https://github.com/user-attachments/assets/835e5524-902e-414c-9d45-96bc2576dfbe" />

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis *(optional — used for caching)*

### Backend

```bash
cd backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

API runs at `http://localhost:5000`. An admin account is created automatically on first run:

| Username | Password |
|---|---|
| `admin` | `admin123` |

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`.

### Seed Sample Data

```bash
cd backend
source venv/bin/activate
python seed.py
```

This creates sample subjects, chapters, quizzes with questions, and student accounts (`password: student123`).

---

## API Reference

### Auth — `/api/auth`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Returns JWT access token and user object |
| POST | `/register` | Create a new student account |

### User — `/api/user` *(JWT required)*

| Method | Endpoint | Description |
|---|---|---|
| GET | `/dashboard` | Summary stats and recent attempts |
| GET | `/subjects` | List active subjects |
| GET | `/chapters` | List all chapters |
| GET | `/quizzes` | List all active quizzes |
| GET | `/scores` | Current user's attempt history |
| GET | `/analytics` | Score trend, subject averages, vs class comparison |
| GET | `/leaderboard` | Top 10 students by average score |
| GET | `/subject-progress` | Per-subject completion and average score |

### Quiz — `/api/quiz` *(JWT required)*

| Method | Endpoint | Description |
|---|---|---|
| GET | `/<id>/start` | Load quiz with questions (no correct answers) |
| POST | `/<id>/submit` | Submit answers and receive score |
| GET | `/results/<score_id>` | Detailed results with per-question breakdown |

### Admin — `/api/admin` *(JWT required)*

| Method | Endpoint | Description |
|---|---|---|
| GET / POST | `/subjects` | List or create subjects |
| PUT / DELETE | `/subjects/<id>` | Update or delete a subject |
| GET / POST | `/chapters` | List or create chapters |
| PUT / DELETE | `/chapters/<id>` | Update or delete a chapter |
| GET / POST | `/quizzes` | List or create quizzes |
| PUT / DELETE | `/quizzes/<id>` | Update or delete a quiz |
| GET / POST | `/quizzes/<id>/questions` | List or add questions |
| PUT / DELETE | `/questions/<id>` | Update or delete a question |
| GET | `/users` | All student accounts with attempt stats |
| GET | `/analytics/overview` | Platform-wide analytics data |
| GET | `/analytics/users` | All students with aggregate stats |
| GET | `/analytics/user/<id>` | Single student analytics |

---

## Environment Variables

Create `backend/.env` to override defaults:

```env
SECRET_KEY=change-me
JWT_SECRET_KEY=change-me-jwt
DATABASE_URL=sqlite:///quiz_master.db
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=app-password
```

---

## Notes

- Redis is optional. If unavailable, the app logs a connection warning but continues to work without caching.
- Celery async tasks (email reminders, data export) are scaffolded in `tasks.py` but disabled by default. Run a Celery worker separately to enable them.
