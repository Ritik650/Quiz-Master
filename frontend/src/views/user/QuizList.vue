<template>
  <div class="quiz-list-page">

    <!-- Page Header -->
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-heading">Browse Quizzes</h1>
        <p class="page-sub">Select a subject, pick a chapter, and start practising</p>
      </div>
      <div class="header-stats">
        <div class="hstat">
          <span class="hstat-val">{{ allQuizzes.length }}</span>
          <span class="hstat-lbl">Total Quizzes</span>
        </div>
        <div class="hstat">
          <span class="hstat-val">{{ userScores.length }}</span>
          <span class="hstat-lbl">Completed</span>
        </div>
        <div class="hstat">
          <span class="hstat-val">{{ allQuizzes.length - userScores.length }}</span>
          <span class="hstat-lbl">Remaining</span>
        </div>
      </div>
    </div>

    <!-- Subject Tabs -->
    <div class="subject-tabs-wrap">
      <button
        class="subject-tab"
        :class="{ active: !selectedSubject }"
        @click="selectSubject(null)"
      >
        <span class="tab-icon tab-all">All</span>
        All Subjects
      </button>
      <button
        v-for="subject in subjects"
        :key="subject.id"
        class="subject-tab"
        :class="{ active: selectedSubject?.id === subject.id }"
        @click="selectSubject(subject)"
      >
        <span class="tab-icon" :style="{ background: subjectColor(subject.name) + '22', color: subjectColor(subject.name) }">
          {{ subject.name.charAt(0) }}
        </span>
        {{ subject.name }}
        <span class="tab-badge">{{ subject.chapters_count }}</span>
      </button>
    </div>

    <!-- Main body: chapter sidebar + quiz cards -->
    <div class="content-body">

      <!-- Left: Chapter sidebar -->
      <aside class="chapter-sidebar">
        <div class="sidebar-heading">Chapters</div>
        <div v-if="filteredChapters.length === 0" class="chapter-empty">
          No chapters found
        </div>
        <button
          v-for="ch in filteredChapters"
          :key="ch.id"
          class="chapter-item"
          :class="{ active: selectedChapter?.id === ch.id }"
          @click="selectChapter(ch)"
        >
          <div class="chapter-item-inner">
            <div class="chapter-num" :style="{ background: selectedChapter?.id === ch.id ? subjectColor(ch.subject_name) : '' }">
              {{ filteredChapters.indexOf(ch) + 1 }}
            </div>
            <div>
              <div class="chapter-name">{{ ch.name }}</div>
              <div class="chapter-meta">{{ ch.quizzes_count }} quizzes</div>
            </div>
          </div>
          <div class="chapter-progress-bar">
            <div
              class="chapter-progress-fill"
              :style="{ width: chapterProgress(ch) + '%', background: subjectColor(ch.subject_name) }"
            ></div>
          </div>
        </button>
      </aside>

      <!-- Right: Quiz cards -->
      <div class="quiz-area">

        <!-- Empty state: no chapter selected -->
        <div v-if="!selectedChapter" class="quiz-empty-state">
          <div class="empty-illustration">
            <svg viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="12" y="8" width="72" height="80" rx="8" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
              <rect x="24" y="28" width="48" height="4" rx="2" fill="#A5B4FC"/>
              <rect x="24" y="40" width="36" height="4" rx="2" fill="#C7D2FE"/>
              <rect x="24" y="52" width="42" height="4" rx="2" fill="#C7D2FE"/>
              <rect x="24" y="64" width="28" height="4" rx="2" fill="#E0E7FF"/>
              <circle cx="67" cy="67" r="20" fill="#4F46E5" opacity="0.15"/>
              <path d="M58 67l5 5 9-9" stroke="#4F46E5" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="empty-title">Pick a Chapter</div>
          <div class="empty-sub">Select a chapter from the left to view available quizzes</div>
        </div>

        <!-- Quiz grid when chapter selected -->
        <template v-else>
          <div class="quiz-area-header">
            <div>
              <div class="quiz-area-title">
                <span class="breadcrumb-pill" :style="{ background: subjectColor(selectedChapter.subject_name) + '22', color: subjectColor(selectedChapter.subject_name) }">
                  {{ selectedChapter.subject_name }}
                </span>
                {{ selectedChapter.name }}
              </div>
              <div class="quiz-count-sub">{{ filteredQuizzes.length }} quizzes available</div>
            </div>
          </div>

          <div v-if="filteredQuizzes.length === 0" class="quiz-empty-state">
            <div class="empty-title">No Quizzes Yet</div>
            <div class="empty-sub">This chapter doesn't have any quizzes yet</div>
          </div>

          <div v-else class="quiz-grid">
            <div
              v-for="quiz in filteredQuizzes"
              :key="quiz.id"
              class="quiz-card"
              :class="{ 'quiz-card--done': !!getUserAttempt(quiz.id) }"
            >
              <!-- Color accent bar -->
              <div class="quiz-accent" :style="{ background: subjectColor(selectedChapter.subject_name) }"></div>

              <div class="quiz-card-body">
                <div class="quiz-card-top">
                  <div class="quiz-title">{{ quiz.title }}</div>
                  <span class="status-pill" :class="statusClass(quiz)">{{ getStatus(quiz) }}</span>
                </div>

                <p v-if="quiz.description" class="quiz-desc">{{ quiz.description }}</p>

                <!-- Meta badges -->
                <div class="quiz-meta">
                  <div class="meta-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    {{ quiz.time_duration }} min
                  </div>
                  <div class="meta-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                    {{ quiz.questions_count }} Qs
                  </div>
                  <div class="meta-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                    {{ quiz.total_marks }} marks
                  </div>
                </div>

                <!-- Previous attempt progress bar -->
                <div v-if="getUserAttempt(quiz.id)" class="attempt-info">
                  <div class="attempt-row">
                    <span class="attempt-label">Best score</span>
                    <span class="attempt-score" :style="{ color: scoreColor(getUserAttempt(quiz.id).percentage) }">
                      {{ getUserAttempt(quiz.id).total_scored }}/{{ getUserAttempt(quiz.id).total_marks }}
                      ({{ getUserAttempt(quiz.id).percentage }}%)
                    </span>
                  </div>
                  <div class="attempt-bar">
                    <div
                      class="attempt-fill"
                      :style="{ width: getUserAttempt(quiz.id).percentage + '%', background: scoreColor(getUserAttempt(quiz.id).percentage) }"
                    ></div>
                  </div>
                </div>

                <!-- Action row -->
                <div class="quiz-card-footer">
                  <span class="quiz-date">{{ formatDate(quiz.date_of_quiz) }}</span>
                  <button
                    class="btn-quiz"
                    :class="getUserAttempt(quiz.id) ? 'btn-retake' : 'btn-start'"
                    :disabled="!canStart(quiz)"
                    @click="startQuiz(quiz)"
                    :style="canStart(quiz) && !getUserAttempt(quiz.id) ? { background: subjectColor(selectedChapter.subject_name) } : {}"
                  >
                    {{ getUserAttempt(quiz.id) ? 'Retake' : 'Start Quiz' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

const SUBJECT_COLORS = {
  'Physics':      '#3B82F6',
  'Chemistry':    '#10B981',
  'Mathematics':  '#4F46E5',
  'Biology':      '#059669',
  'English':      '#F59E0B',
}
const DEFAULT_COLOR = '#64748B'

export default {
  name: 'QuizList',
  data() {
    return {
      subjects: [],
      allChapters: [],
      allQuizzes: [],
      userScores: [],
      selectedSubject: null,
      selectedChapter: null,
    }
  },
  computed: {
    filteredChapters() {
      if (!this.selectedSubject) return this.allChapters
      return this.allChapters.filter(c => c.subject_id === this.selectedSubject.id)
    },
    filteredQuizzes() {
      if (!this.selectedChapter) return []
      return this.allQuizzes.filter(q => q.chapter_id === this.selectedChapter.id)
    }
  },
  async mounted() {
    await Promise.all([
      this.fetchSubjects(),
      this.fetchChapters(),
      this.fetchQuizzes(),
      this.fetchUserScores(),
    ])
  },
  methods: {
    async fetchSubjects() {
      try { this.subjects = (await axios.get('/user/subjects')).data } catch (e) { console.error(e) }
    },
    async fetchChapters() {
      try { this.allChapters = (await axios.get('/user/chapters')).data } catch (e) { console.error(e) }
    },
    async fetchQuizzes() {
      try { this.allQuizzes = (await axios.get('/user/quizzes')).data } catch (e) { console.error(e) }
    },
    async fetchUserScores() {
      try { this.userScores = (await axios.get('/user/scores')).data } catch (e) { console.error(e) }
    },

    selectSubject(subject) {
      this.selectedSubject = subject
      this.selectedChapter = null
    },
    selectChapter(chapter) {
      this.selectedChapter = chapter
    },

    subjectColor(name) {
      return SUBJECT_COLORS[name] || DEFAULT_COLOR
    },

    chapterProgress(chapter) {
      const chapterQuizzes = this.allQuizzes.filter(q => q.chapter_id === chapter.id)
      if (!chapterQuizzes.length) return 0
      const completed = chapterQuizzes.filter(q => this.getUserAttempt(q.id)).length
      return Math.round((completed / chapterQuizzes.length) * 100)
    },

    getUserAttempt(quizId) {
      return this.userScores.find(s => s.quiz_id === quizId) || null
    },

    getStatus(quiz) {
      const now = new Date()
      const quizDate = new Date(quiz.date_of_quiz)
      if (quizDate > now) return 'Upcoming'
      if (!quiz.questions_count) return 'No Questions'
      if (this.getUserAttempt(quiz.id)) return 'Completed'
      return 'Available'
    },

    statusClass(quiz) {
      const s = this.getStatus(quiz)
      return {
        'Available':    'pill-green',
        'Completed':    'pill-blue',
        'Upcoming':     'pill-amber',
        'No Questions': 'pill-gray',
      }[s] || 'pill-gray'
    },

    canStart(quiz) {
      return new Date(quiz.date_of_quiz) <= new Date() && quiz.questions_count > 0
    },

    scoreColor(pct) {
      if (pct >= 70) return '#10B981'
      if (pct >= 40) return '#F59E0B'
      return '#EF4444'
    },

    formatDate(d) {
      return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    },

    startQuiz(quiz) {
      if (this.canStart(quiz)) this.$router.push(`/quiz/${quiz.id}/take`)
    }
  }
}
</script>

<style scoped>
.quiz-list-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── Page Header ──────────────────────────────────────────── */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 16px;
}

.page-heading {
  font-family: var(--qm-font-heading);
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--qm-text);
  margin: 0 0 4px;
}

.page-sub {
  font-size: 14px;
  color: var(--qm-text-muted);
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 24px;
}

.hstat {
  text-align: center;
}

.hstat-val {
  display: block;
  font-family: var(--qm-font-heading);
  font-size: 1.375rem;
  font-weight: 800;
  color: var(--qm-primary);
  line-height: 1;
  margin-bottom: 2px;
}

.hstat-lbl {
  font-size: 11.5px;
  color: var(--qm-text-muted);
  font-weight: 500;
}

/* ── Subject Tabs ─────────────────────────────────────────── */
.subject-tabs-wrap {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: none;
}

.subject-tabs-wrap::-webkit-scrollbar { display: none; }

.subject-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 100px;
  border: 1.5px solid var(--qm-border);
  background: var(--qm-surface);
  color: var(--qm-text-muted);
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s;
}

.subject-tab:hover {
  border-color: var(--qm-primary);
  color: var(--qm-primary);
}

.subject-tab.active {
  border-color: var(--qm-primary);
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-weight: 600;
}

.tab-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.tab-all {
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-size: 10px;
}

.tab-badge {
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  background: var(--qm-bg);
  color: var(--qm-text-muted);
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}

.subject-tab.active .tab-badge {
  background: var(--qm-primary);
  color: white;
}

/* ── Content Body ─────────────────────────────────────────── */
.content-body {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 20px;
  align-items: start;
}

/* ── Chapter Sidebar ──────────────────────────────────────── */
.chapter-sidebar {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
  position: sticky;
  top: calc(var(--qm-navbar-h) + 16px);
}

.sidebar-heading {
  padding: 14px 16px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--qm-text-muted);
  border-bottom: 1px solid var(--qm-border-light);
  background: var(--qm-bg);
}

.chapter-empty {
  padding: 24px 16px;
  text-align: center;
  font-size: 13px;
  color: var(--qm-text-light);
}

.chapter-item {
  display: block;
  width: 100%;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  text-align: left;
  border-bottom: 1px solid var(--qm-border-light);
  transition: background 0.15s;
}

.chapter-item:last-child { border-bottom: none; }
.chapter-item:hover { background: var(--qm-bg); }
.chapter-item.active { background: var(--qm-primary-light); }

.chapter-item-inner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px 8px;
}

.chapter-num {
  min-width: 22px;
  height: 22px;
  border-radius: 6px;
  background: var(--qm-border);
  color: var(--qm-text-muted);
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
  transition: background 0.15s, color 0.15s;
}

.chapter-item.active .chapter-num {
  color: white;
}

.chapter-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--qm-text);
  line-height: 1.3;
}

.chapter-item.active .chapter-name { color: var(--qm-primary); font-weight: 600; }

.chapter-meta {
  font-size: 11.5px;
  color: var(--qm-text-muted);
  margin-top: 2px;
}

.chapter-progress-bar {
  height: 3px;
  background: var(--qm-border-light);
  margin: 0 14px;
  border-radius: 2px;
  overflow: hidden;
}

.chapter-progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease;
}

/* ── Quiz Area ────────────────────────────────────────────── */
.quiz-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.quiz-area-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.quiz-area-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--qm-font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--qm-text);
}

.breadcrumb-pill {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 11.5px;
  font-weight: 600;
}

.quiz-count-sub {
  font-size: 12.5px;
  color: var(--qm-text-muted);
  margin-top: 4px;
}

/* ── Empty State ──────────────────────────────────────────── */
.quiz-empty-state {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-xl);
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.empty-illustration svg {
  width: 96px;
  height: 96px;
}

.empty-title {
  font-family: var(--qm-font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--qm-text);
}

.empty-sub {
  font-size: 13.5px;
  color: var(--qm-text-muted);
  max-width: 280px;
}

/* ── Quiz Grid ────────────────────────────────────────────── */
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* ── Quiz Card ────────────────────────────────────────────── */
.quiz-card {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
  display: flex;
  flex-direction: column;
  transition: transform 0.18s, box-shadow 0.18s;
}

.quiz-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--qm-shadow-md);
}

.quiz-card--done {
  border-color: #D1FAE5;
}

.quiz-accent {
  height: 4px;
  flex-shrink: 0;
}

.quiz-card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.quiz-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.quiz-title {
  font-family: var(--qm-font-heading);
  font-size: 14px;
  font-weight: 700;
  color: var(--qm-text);
  line-height: 1.3;
  flex: 1;
}

.quiz-desc {
  font-size: 12.5px;
  color: var(--qm-text-muted);
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Status pills */
.status-pill {
  padding: 2px 9px;
  border-radius: 20px;
  font-size: 10.5px;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}

.pill-green { background: #D1FAE5; color: #065F46; }
.pill-blue  { background: #DBEAFE; color: #1E40AF; }
.pill-amber { background: #FEF3C7; color: #92400E; }
.pill-gray  { background: var(--qm-bg); color: var(--qm-text-muted); }

/* Meta chips */
.quiz-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.meta-chip {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 6px;
  background: var(--qm-bg);
  border: 1px solid var(--qm-border-light);
  font-size: 11.5px;
  color: var(--qm-text-muted);
  font-weight: 500;
}

.meta-chip svg {
  width: 11px;
  height: 11px;
  flex-shrink: 0;
}

/* Attempt info */
.attempt-info {
  background: #F0FDF4;
  border: 1px solid #D1FAE5;
  border-radius: var(--qm-radius);
  padding: 8px 10px;
}

.attempt-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.attempt-label {
  font-size: 11.5px;
  color: var(--qm-text-muted);
}

.attempt-score {
  font-size: 12px;
  font-weight: 700;
}

.attempt-bar {
  height: 4px;
  background: #D1FAE5;
  border-radius: 2px;
  overflow: hidden;
}

.attempt-fill {
  height: 100%;
  border-radius: 2px;
}

/* Card footer */
.quiz-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 4px;
}

.quiz-date {
  font-size: 11.5px;
  color: var(--qm-text-light);
}

.btn-quiz {
  padding: 6px 16px;
  border-radius: var(--qm-radius);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: opacity 0.15s, transform 0.15s;
}

.btn-quiz:hover:not(:disabled) {
  opacity: 0.88;
  transform: translateY(-1px);
}

.btn-quiz:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.btn-start {
  color: white;
  background: var(--qm-primary);
}

.btn-retake {
  background: #DBEAFE;
  color: #1E40AF;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 900px) {
  .content-body {
    grid-template-columns: 1fr;
  }

  .chapter-sidebar {
    position: static;
    max-height: 260px;
    overflow-y: auto;
  }
}

@media (max-width: 600px) {
  .header-stats { display: none; }
  .quiz-grid    { grid-template-columns: 1fr; }
}
</style>
