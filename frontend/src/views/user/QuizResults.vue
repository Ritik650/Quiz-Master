<template>
  <div class="results-page">

    <div v-if="loading" class="results-loading">
      <div class="rl-spinner"></div>
      <p>Loading results…</p>
    </div>

    <template v-else-if="results">

      <!-- Score hero -->
      <div class="score-hero" :class="heroClass">
        <div class="hero-inner">
          <div class="score-ring" :class="ringClass">
            <div class="score-pct">{{ results.score.percentage }}%</div>
            <div class="score-frac">{{ results.score.total_scored }}/{{ results.score.total_marks }}</div>
          </div>
          <div class="hero-info">
            <div class="hero-tag">Quiz Completed</div>
            <h2 class="hero-title">{{ results.quiz.title }}</h2>
            <div class="hero-meta">
              <span class="hero-chip">{{ results.quiz.subject_name }}</span>
              <span class="hero-sep">·</span>
              <span>{{ results.quiz.chapter_name }}</span>
            </div>
            <p class="hero-msg">{{ performanceMessage }}</p>
          </div>
        </div>
      </div>

      <!-- Stats row -->
      <div class="result-stats">
        <div class="rstat rstat--green">
          <div class="rstat-val">{{ correctAnswers }}</div>
          <div class="rstat-lbl">Correct</div>
        </div>
        <div class="rstat rstat--red">
          <div class="rstat-val">{{ wrongAnswers }}</div>
          <div class="rstat-lbl">Incorrect</div>
        </div>
        <div class="rstat rstat--gray">
          <div class="rstat-val">{{ unanswered }}</div>
          <div class="rstat-lbl">Unanswered</div>
        </div>
        <div class="rstat rstat--blue">
          <div class="rstat-val">{{ results.score.time_taken ?? '—' }}</div>
          <div class="rstat-lbl">Minutes Taken</div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="result-actions">
        <button class="ra-btn ra-primary" @click="retakeQuiz">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.26"/></svg>
          Retake Quiz
        </button>
        <router-link to="/quizzes" class="ra-btn ra-outline">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          Browse Quizzes
        </router-link>
        <router-link to="/dashboard" class="ra-btn ra-outline">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          Dashboard
        </router-link>
      </div>

      <!-- Detailed review -->
      <div class="detail-section">
        <div class="detail-header">
          <div class="detail-title">Question Review</div>
          <button class="toggle-btn" @click="showAnswers = !showAnswers">
            {{ showAnswers ? 'Hide' : 'Show' }} Answers
          </button>
        </div>

        <div v-if="showAnswers" class="qreview-list">
          <div
            v-for="(res, i) in results.detailed_results"
            :key="res.question.id"
            class="qreview-item"
            :class="res.is_correct ? 'qr--correct' : (res.user_answer ? 'qr--wrong' : 'qr--skip')"
          >
            <div class="qr-num-col">
              <div class="qr-num" :class="res.is_correct ? 'qr-num--green' : (res.user_answer ? 'qr-num--red' : 'qr-num--gray')">
                {{ i + 1 }}
              </div>
              <div class="qr-icon">
                <svg v-if="res.is_correct" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                <svg v-else-if="res.user_answer" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              </div>
            </div>

            <div class="qr-body">
              <div class="qr-statement">{{ res.question.question_statement }}</div>
              <div class="qr-opts">
                <div
                  v-for="(opt, oi) in getOptions(res.question)"
                  :key="oi"
                  class="qr-opt"
                  :class="getOptClass(oi + 1, res)"
                >
                  <span class="qr-opt-letter">{{ String.fromCharCode(65 + oi) }}</span>
                  <span class="qr-opt-text">{{ opt }}</span>
                  <span v-if="res.user_answer == oi + 1 && res.question.correct_option == oi + 1" class="qr-opt-badge qr-badge-correct">Correct ✓</span>
                  <span v-else-if="res.user_answer == oi + 1" class="qr-opt-badge qr-badge-wrong">Your answer ✗</span>
                  <span v-else-if="res.question.correct_option == oi + 1" class="qr-opt-badge qr-badge-answer">Correct answer</span>
                </div>
              </div>
              <div class="qr-footer">
                <span v-if="!res.user_answer" class="qr-skipped">Not attempted</span>
                <span class="qr-marks">{{ res.question.marks }} mark{{ res.question.marks > 1 ? 's' : '' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="detail-locked">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          <p>Click "Show Answers" to review each question</p>
        </div>
      </div>

    </template>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuizResults',
  data() {
    return { results: null, loading: true, showAnswers: false }
  },
  computed: {
    correctAnswers() { return this.results?.detailed_results.filter(r => r.is_correct).length || 0 },
    wrongAnswers()   { return this.results?.detailed_results.filter(r => !r.is_correct && r.user_answer).length || 0 },
    unanswered()     { return this.results?.detailed_results.filter(r => !r.user_answer).length || 0 },
    pct()            { return this.results?.score.percentage || 0 },
    heroClass() {
      if (this.pct >= 80) return 'hero-excellent'
      if (this.pct >= 60) return 'hero-good'
      if (this.pct >= 40) return 'hero-average'
      return 'hero-poor'
    },
    ringClass() {
      if (this.pct >= 80) return 'ring-green'
      if (this.pct >= 60) return 'ring-blue'
      if (this.pct >= 40) return 'ring-amber'
      return 'ring-red'
    },
    performanceMessage() {
      const p = this.pct
      if (p >= 90) return 'Outstanding! You have mastered this topic.'
      if (p >= 80) return 'Excellent work! Keep up the great performance.'
      if (p >= 70) return 'Great job! Solid understanding of the material.'
      if (p >= 60) return 'Good effort. Review a few topics to get even better.'
      if (p >= 40) return 'Fair attempt. Consider revisiting the study material.'
      return 'Keep practising — review the material and try again soon.'
    }
  },
  async mounted() { await this.fetchResults() },
  methods: {
    async fetchResults() {
      const scoreId = this.$route.params.scoreId
      try {
        this.results = (await axios.get(`/quiz/results/${scoreId}`)).data
      } catch (e) {
        console.error(e)
        this.$router.push('/dashboard')
      }
      this.loading = false
    },
    getOptions(q) { return [q.option1, q.option2, q.option3, q.option4] },
    getOptClass(n, res) {
      const isUser    = res.user_answer == n
      const isCorrect = res.question.correct_option == n
      if (isUser && isCorrect) return 'qr-opt--both'
      if (isUser) return 'qr-opt--user'
      if (isCorrect) return 'qr-opt--answer'
      return ''
    },
    retakeQuiz() { this.$router.push(`/quiz/${this.results.quiz.id}/take`) },
    formatDate(d) { return new Date(d).toLocaleString('en-IN') }
  }
}
</script>

<style scoped>
.results-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── Loading ──────────────────────────────────────────────── */
.results-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 12px;
  color: var(--qm-text-muted);
}

.rl-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--qm-border);
  border-top-color: var(--qm-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Score hero ───────────────────────────────────────────── */
.score-hero {
  border-radius: var(--qm-radius-xl);
  padding: 36px 32px;
  border: 1px solid var(--qm-border);
}

.hero-excellent { background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-color: #A7F3D0; }
.hero-good      { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-color: #BFDBFE; }
.hero-average   { background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-color: #FDE68A; }
.hero-poor      { background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%); border-color: #FECDD3; }

.hero-inner {
  display: flex;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
}

.score-ring {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 6px solid;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ring-green { border-color: var(--qm-success); background: #D1FAE5; color: #065F46; }
.ring-blue  { border-color: var(--qm-info);    background: #DBEAFE; color: #1E40AF; }
.ring-amber { border-color: var(--qm-warning); background: #FEF3C7; color: #92400E; }
.ring-red   { border-color: var(--qm-danger);  background: #FFE4E6; color: #9F1239; }

.score-pct  { font-family: var(--qm-font-heading); font-size: 28px; font-weight: 900; line-height: 1; }
.score-frac { font-size: 13px; font-weight: 600; opacity: 0.8; margin-top: 2px; }

.hero-tag {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--qm-text-muted);
  margin-bottom: 6px;
}

.hero-title {
  font-family: var(--qm-font-heading);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--qm-text);
  margin: 0 0 8px;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--qm-text-muted);
  margin-bottom: 12px;
}

.hero-chip {
  padding: 2px 10px;
  border-radius: 20px;
  background: white;
  font-weight: 600;
  font-size: 12px;
  color: var(--qm-primary);
}

.hero-sep { color: var(--qm-text-light); }

.hero-msg {
  font-size: 14px;
  color: var(--qm-text-muted);
  margin: 0;
  max-width: 440px;
}

/* ── Stats row ────────────────────────────────────────────── */
.result-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.rstat {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  padding: 18px 20px;
  text-align: center;
  box-shadow: var(--qm-shadow);
}

.rstat-val {
  font-family: var(--qm-font-heading);
  font-size: 2rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 4px;
}

.rstat-lbl {
  font-size: 12px;
  color: var(--qm-text-muted);
  font-weight: 500;
}

.rstat--green .rstat-val { color: var(--qm-success); }
.rstat--red   .rstat-val { color: var(--qm-danger); }
.rstat--gray  .rstat-val { color: var(--qm-text-muted); }
.rstat--blue  .rstat-val { color: var(--qm-info); }

/* ── Action buttons ───────────────────────────────────────── */
.result-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.ra-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 10px 18px;
  border-radius: var(--qm-radius);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
  border: none;
}

.ra-btn svg { width: 15px; height: 15px; }

.ra-primary {
  background: var(--qm-primary);
  color: white;
}

.ra-primary:hover { background: var(--qm-primary-dark); }

.ra-outline {
  border: 1.5px solid var(--qm-border);
  background: var(--qm-surface);
  color: var(--qm-text-muted);
}

.ra-outline:hover {
  border-color: var(--qm-primary);
  color: var(--qm-primary);
  background: var(--qm-primary-light);
}

/* ── Detail section ───────────────────────────────────────── */
.detail-section {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-xl);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 22px;
  border-bottom: 1px solid var(--qm-border-light);
  background: var(--qm-bg);
}

.detail-title {
  font-family: var(--qm-font-heading);
  font-weight: 700;
  font-size: 14px;
  color: var(--qm-text);
}

.toggle-btn {
  padding: 6px 14px;
  border-radius: var(--qm-radius);
  border: 1.5px solid var(--qm-primary);
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.toggle-btn:hover { background: var(--qm-primary); color: white; }

/* Locked state */
.detail-locked {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 48px;
  color: var(--qm-text-light);
}

.detail-locked svg { width: 36px; height: 36px; }
.detail-locked p   { font-size: 14px; margin: 0; }

/* ── Question review items ────────────────────────────────── */
.qreview-list { display: flex; flex-direction: column; }

.qreview-item {
  display: flex;
  gap: 16px;
  padding: 20px 22px;
  border-bottom: 1px solid var(--qm-border-light);
}

.qreview-item:last-child { border-bottom: none; }

.qr--correct { background: #FAFFFE; }
.qr--wrong   { background: #FFFBFB; }
.qr--skip    { background: var(--qm-bg); }

/* Number + icon column */
.qr-num-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  width: 36px;
}

.qr-num {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11.5px;
  font-weight: 700;
}

.qr-num--green { background: #D1FAE5; color: #065F46; }
.qr-num--red   { background: #FFE4E6; color: #9F1239; }
.qr-num--gray  { background: var(--qm-border-light); color: var(--qm-text-muted); }

.qr-icon svg { width: 14px; height: 14px; }
.qr--correct .qr-icon { color: var(--qm-success); }
.qr--wrong   .qr-icon { color: var(--qm-danger); }
.qr--skip    .qr-icon { color: var(--qm-text-light); }

/* Body */
.qr-body { flex: 1; min-width: 0; }

.qr-statement {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--qm-text);
  line-height: 1.5;
  margin-bottom: 14px;
}

.qr-opts { display: flex; flex-direction: column; gap: 7px; margin-bottom: 10px; }

.qr-opt {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: var(--qm-radius);
  border: 1px solid var(--qm-border-light);
  background: var(--qm-bg);
  font-size: 13.5px;
  color: var(--qm-text-muted);
}

.qr-opt--both   { border-color: #10B981; background: #ECFDF5; color: #065F46; }
.qr-opt--user   { border-color: #EF4444; background: #FFF1F2; color: #9F1239; }
.qr-opt--answer { border-color: #10B981; background: #ECFDF5; color: #065F46; }

.qr-opt-letter {
  width: 22px;
  height: 22px;
  border-radius: 5px;
  background: var(--qm-surface);
  border: 1.5px solid var(--qm-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10.5px;
  font-weight: 700;
  flex-shrink: 0;
}

.qr-opt-text { flex: 1; }

.qr-opt-badge {
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
  white-space: nowrap;
  flex-shrink: 0;
}

.qr-badge-correct { background: #D1FAE5; color: #065F46; }
.qr-badge-wrong   { background: #FFE4E6; color: #9F1239; }
.qr-badge-answer  { background: #D1FAE5; color: #065F46; }

.qr-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.qr-skipped {
  font-size: 12px;
  color: var(--qm-text-light);
  font-style: italic;
}

.qr-marks {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--qm-text-muted);
  background: var(--qm-bg);
  padding: 2px 8px;
  border-radius: 10px;
  border: 1px solid var(--qm-border-light);
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .result-stats { grid-template-columns: repeat(2, 1fr); }
  .hero-inner   { flex-direction: column; gap: 20px; text-align: center; }
  .hero-meta    { justify-content: center; }
  .hero-msg     { margin: 0 auto; }
}

@media (max-width: 480px) {
  .result-stats { grid-template-columns: 1fr 1fr; }
  .score-hero   { padding: 24px 20px; }
}
</style>
