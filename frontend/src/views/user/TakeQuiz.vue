<template>
  <div class="take-quiz-root">

    <!-- Loading -->
    <div v-if="loading" class="tq-loading">
      <div class="tq-spinner"></div>
      <p>Loading quiz…</p>
    </div>

    <!-- Quiz Interface -->
    <template v-else-if="quiz">

      <!-- Top bar -->
      <header class="tq-topbar">
        <div class="tq-topbar-left">
          <div class="tq-logo">Q</div>
          <div>
            <div class="tq-quiz-title">{{ quiz.quiz.title }}</div>
            <div class="tq-quiz-sub">{{ quiz.quiz.chapter_name }} · {{ quiz.quiz.subject_name }}</div>
          </div>
        </div>
        <div class="tq-topbar-center">
          <div class="tq-progress-wrap">
            <div class="tq-progress-bar" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <div class="tq-progress-label">{{ currentQuestionIndex + 1 }} / {{ quiz.questions.length }}</div>
        </div>
        <div class="tq-topbar-right">
          <div class="tq-timer" :class="{ 'tq-timer--warn': timeRemaining < 120, 'tq-timer--crit': timeRemaining < 30 }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {{ formatTime(timeRemaining) }}
          </div>
          <button class="tq-submit-top" @click="submitQuiz">Submit</button>
        </div>
      </header>

      <!-- Body -->
      <div class="tq-body">

        <!-- Question panel -->
        <main class="tq-main">
          <div class="tq-question-card">
            <div class="tq-qnum">Question {{ currentQuestionIndex + 1 }}</div>
            <div class="tq-qtext">{{ currentQuestion.question_statement }}</div>

            <div class="tq-options">
              <label
                v-for="(opt, idx) in getOptions(currentQuestion)"
                :key="idx"
                class="tq-option"
                :class="{ 'tq-option--selected': answers[currentQuestion.id] === idx + 1 }"
              >
                <input
                  type="radio"
                  :name="`q_${currentQuestion.id}`"
                  :value="idx + 1"
                  v-model="answers[currentQuestion.id]"
                />
                <span class="tq-opt-letter">{{ String.fromCharCode(65 + idx) }}</span>
                <span class="tq-opt-text">{{ opt }}</span>
              </label>
            </div>
          </div>

          <!-- Navigation buttons -->
          <div class="tq-nav">
            <button class="tq-nav-btn tq-nav-prev" @click="prevQ" :disabled="currentQuestionIndex === 0">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
              Previous
            </button>
            <button class="tq-skip" @click="clearAnswer">Clear Response</button>
            <button
              v-if="currentQuestionIndex < quiz.questions.length - 1"
              class="tq-nav-btn tq-nav-next"
              @click="nextQ"
            >
              Next
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
            <button v-else class="tq-nav-btn tq-nav-finish" @click="submitQuiz">
              Finish Quiz
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
            </button>
          </div>
        </main>

        <!-- Right sidebar: navigator -->
        <aside class="tq-sidebar">
          <div class="tq-sidebar-card">
            <div class="tq-sidebar-hdr">Question Palette</div>

            <div class="tq-palette-legend">
              <span class="tq-legend-item">
                <span class="tq-leg tq-leg--done"></span> Answered ({{ answeredCount }})
              </span>
              <span class="tq-legend-item">
                <span class="tq-leg tq-leg--skip"></span> Not Answered ({{ quiz.questions.length - answeredCount }})
              </span>
            </div>

            <div class="tq-palette">
              <button
                v-for="(q, i) in quiz.questions"
                :key="q.id"
                class="tq-palette-btn"
                :class="{
                  'tq-palette-btn--current': i === currentQuestionIndex,
                  'tq-palette-btn--done': !!answers[q.id] && i !== currentQuestionIndex,
                }"
                @click="goTo(i)"
              >{{ i + 1 }}</button>
            </div>

            <div class="tq-sidebar-stats">
              <div class="tq-sstat">
                <span class="tq-sstat-val">{{ quiz.questions.length }}</span>
                <span class="tq-sstat-lbl">Total</span>
              </div>
              <div class="tq-sstat">
                <span class="tq-sstat-val tq-green">{{ answeredCount }}</span>
                <span class="tq-sstat-lbl">Done</span>
              </div>
              <div class="tq-sstat">
                <span class="tq-sstat-val tq-muted">{{ quiz.questions.length - answeredCount }}</span>
                <span class="tq-sstat-lbl">Remaining</span>
              </div>
            </div>

            <button class="tq-submit-side" @click="submitQuiz">
              Submit Quiz
            </button>
          </div>
        </aside>

      </div>
    </template>

    <!-- Confirm Modal -->
    <div v-if="showConfirmDialog" class="tq-overlay" @click.self="showConfirmDialog = false">
      <div class="tq-modal">
        <div class="tq-modal-hdr">
          <div class="tq-modal-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </div>
          <div class="tq-modal-title">Submit Quiz?</div>
        </div>
        <div class="tq-modal-body">
          <div class="tq-modal-row">
            <span>Answered</span>
            <strong>{{ answeredCount }} / {{ quiz?.questions.length }}</strong>
          </div>
          <div class="tq-modal-row">
            <span>Unanswered</span>
            <strong>{{ (quiz?.questions.length || 0) - answeredCount }}</strong>
          </div>
          <div class="tq-modal-row">
            <span>Time Remaining</span>
            <strong>{{ formatTime(timeRemaining) }}</strong>
          </div>
          <p class="tq-modal-warn">You cannot change your answers after submission.</p>
          <div v-if="submitError" class="tq-error">{{ submitError }}</div>
        </div>
        <div class="tq-modal-footer">
          <button class="tq-btn-cancel" @click="showConfirmDialog = false" :disabled="submitting">Go Back</button>
          <button class="tq-btn-confirm" @click="confirmSubmit" :disabled="submitting">
            {{ submitting ? 'Submitting…' : 'Yes, Submit' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TakeQuiz',
  data() {
    return {
      quiz: null,
      loading: true,
      currentQuestionIndex: 0,
      answers: {},
      timeRemaining: 0,
      timer: null,
      submitting: false,
      submitError: null,
      showConfirmDialog: false
    }
  },
  computed: {
    currentQuestion() { return this.quiz?.questions[this.currentQuestionIndex] },
    progressPercentage() {
      if (!this.quiz) return 0
      return ((this.currentQuestionIndex + 1) / this.quiz.questions.length) * 100
    },
    answeredCount() { return Object.keys(this.answers).length }
  },
  async mounted() { await this.loadQuiz() },
  beforeUnmount() { clearInterval(this.timer) },
  methods: {
    async loadQuiz() {
      const quizId = this.$route.params.quizId
      try {
        const res = await axios.get(`/quiz/${quizId}/start`)
        this.quiz = res.data
        this.timeRemaining = this.quiz.quiz.time_duration * 60
        this.startTimer()
        this.loading = false
      } catch (e) {
        console.error('Failed to load quiz:', e)
        this.$router.push('/quizzes')
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.timeRemaining--
        if (this.timeRemaining <= 0) {
          clearInterval(this.timer)
          this.submitError = null
          this.confirmSubmit()
        }
      }, 1000)
    },
    formatTime(s) {
      const m = Math.floor(s / 60)
      const sec = s % 60
      return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
    },
    getOptions(q) { return [q.option1, q.option2, q.option3, q.option4] },
    prevQ() { if (this.currentQuestionIndex > 0) this.currentQuestionIndex-- },
    nextQ() { if (this.currentQuestionIndex < this.quiz.questions.length - 1) this.currentQuestionIndex++ },
    goTo(i) { this.currentQuestionIndex = i },
    clearAnswer() { delete this.answers[this.currentQuestion.id]; this.answers = { ...this.answers } },
    submitQuiz() { this.submitError = null; this.showConfirmDialog = true },
    async confirmSubmit() {
      this.submitting = true
      this.submitError = null
      this.showConfirmDialog = false
      const timeTaken = this.quiz.quiz.time_duration - Math.floor(this.timeRemaining / 60)
      try {
        const res = await axios.post(`/quiz/${this.quiz.quiz.id}/submit`, {
          answers: this.answers,
          timeTaken
        })
        clearInterval(this.timer)
        this.$router.push(`/quiz/results/${res.data.score.id}`)
      } catch (e) {
        this.submitError = e?.response?.data?.message || e.message || 'Failed to submit quiz.'
        this.showConfirmDialog = true
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
/* Full-page quiz layout — overrides the UserLayout padding */
.take-quiz-root {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  background: var(--qm-bg);
  z-index: 200;
  overflow: hidden;
}

/* ── Loading ──────────────────────────────────────────────── */
.tq-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 16px;
  color: var(--qm-text-muted);
}

.tq-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--qm-border);
  border-top-color: var(--qm-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Top bar ──────────────────────────────────────────────── */
.tq-topbar {
  height: 60px;
  background: var(--qm-surface);
  border-bottom: 1px solid var(--qm-border);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 16px;
  flex-shrink: 0;
  box-shadow: var(--qm-shadow);
  z-index: 10;
}

.tq-topbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 200px;
}

.tq-logo {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  font-weight: 800;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tq-quiz-title {
  font-family: var(--qm-font-heading);
  font-size: 14px;
  font-weight: 700;
  color: var(--qm-text);
  line-height: 1.2;
}

.tq-quiz-sub {
  font-size: 11px;
  color: var(--qm-text-muted);
}

.tq-topbar-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tq-progress-wrap {
  height: 6px;
  background: var(--qm-border);
  border-radius: 3px;
  overflow: hidden;
}

.tq-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--qm-primary), var(--qm-secondary));
  border-radius: 3px;
  transition: width 0.3s ease;
}

.tq-progress-label {
  font-size: 11px;
  color: var(--qm-text-muted);
  text-align: center;
}

.tq-topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 200px;
  justify-content: flex-end;
}

.tq-timer {
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: var(--qm-font-heading);
  font-size: 16px;
  font-weight: 700;
  color: var(--qm-text);
  background: var(--qm-bg);
  padding: 5px 12px;
  border-radius: var(--qm-radius);
  border: 1px solid var(--qm-border);
}

.tq-timer svg { width: 15px; height: 15px; }
.tq-timer--warn { color: #92400E; background: #FEF3C7; border-color: #FCD34D; }
.tq-timer--crit { color: var(--qm-danger); background: var(--qm-danger-light); border-color: #FCA5A5; animation: pulse 0.8s ease-in-out infinite; }

@keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:0.6 } }

.tq-submit-top {
  padding: 7px 16px;
  border-radius: var(--qm-radius);
  border: 1.5px solid var(--qm-primary);
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.tq-submit-top:hover {
  background: var(--qm-primary);
  color: white;
}

/* ── Body ─────────────────────────────────────────────────── */
.tq-body {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 0;
  flex: 1;
  overflow: hidden;
}

/* ── Main (question area) ─────────────────────────────────── */
.tq-main {
  display: flex;
  flex-direction: column;
  padding: 24px;
  overflow-y: auto;
  gap: 20px;
}

.tq-question-card {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-xl);
  padding: 28px;
  flex: 1;
  box-shadow: var(--qm-shadow);
}

.tq-qnum {
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--qm-primary);
  margin-bottom: 12px;
}

.tq-qtext {
  font-size: 17px;
  font-weight: 600;
  color: var(--qm-text);
  line-height: 1.6;
  margin-bottom: 28px;
}

/* Option cards */
.tq-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tq-option {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border: 1.5px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  cursor: pointer;
  transition: all 0.15s;
  background: var(--qm-surface);
}

.tq-option:hover {
  border-color: var(--qm-primary);
  background: var(--qm-primary-light);
}

.tq-option--selected {
  border-color: var(--qm-primary);
  background: var(--qm-primary-light);
}

.tq-option input[type="radio"] {
  display: none;
}

.tq-opt-letter {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--qm-bg);
  border: 1.5px solid var(--qm-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--qm-text-muted);
  flex-shrink: 0;
  transition: all 0.15s;
}

.tq-option--selected .tq-opt-letter {
  background: var(--qm-primary);
  border-color: var(--qm-primary);
  color: white;
}

.tq-opt-text {
  font-size: 14.5px;
  color: var(--qm-text);
  line-height: 1.4;
}

/* Navigation */
.tq-nav {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tq-nav-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 18px;
  border-radius: var(--qm-radius);
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s;
}

.tq-nav-btn svg { width: 14px; height: 14px; }
.tq-nav-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.tq-nav-prev {
  background: var(--qm-surface);
  border: 1.5px solid var(--qm-border);
  color: var(--qm-text-muted);
}

.tq-nav-prev:hover:not(:disabled) {
  border-color: var(--qm-primary);
  color: var(--qm-primary);
}

.tq-nav-next {
  background: var(--qm-primary);
  color: white;
  margin-left: auto;
}

.tq-nav-next:hover {
  background: var(--qm-primary-dark);
}

.tq-nav-finish {
  background: var(--qm-success);
  color: white;
  margin-left: auto;
}

.tq-nav-finish:hover {
  background: #059669;
}

.tq-skip {
  padding: 9px 16px;
  border-radius: var(--qm-radius);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 1.5px dashed var(--qm-border);
  background: none;
  color: var(--qm-text-muted);
  transition: all 0.15s;
}

.tq-skip:hover {
  border-color: var(--qm-danger);
  color: var(--qm-danger);
}

/* ── Sidebar ──────────────────────────────────────────────── */
.tq-sidebar {
  background: var(--qm-surface);
  border-left: 1px solid var(--qm-border);
  overflow-y: auto;
  padding: 16px;
}

.tq-sidebar-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.tq-sidebar-hdr {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--qm-text-muted);
}

.tq-palette-legend {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tq-legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--qm-text-muted);
}

.tq-leg {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  border: 1.5px solid var(--qm-border);
  flex-shrink: 0;
}

.tq-leg--done { background: #D1FAE5; border-color: #10B981; }
.tq-leg--skip { background: var(--qm-bg); }

/* Palette grid */
.tq-palette {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
}

.tq-palette-btn {
  aspect-ratio: 1;
  border-radius: var(--qm-radius-sm);
  border: 1.5px solid var(--qm-border);
  background: var(--qm-bg);
  color: var(--qm-text-muted);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tq-palette-btn:hover { border-color: var(--qm-primary); color: var(--qm-primary); }
.tq-palette-btn--done { background: #D1FAE5; border-color: #10B981; color: #065F46; }
.tq-palette-btn--current { background: var(--qm-primary); border-color: var(--qm-primary); color: white; }

/* Stats row */
.tq-sidebar-stats {
  display: flex;
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius);
  overflow: hidden;
}

.tq-sstat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 4px;
  border-right: 1px solid var(--qm-border);
  gap: 2px;
}

.tq-sstat:last-child { border-right: none; }

.tq-sstat-val {
  font-family: var(--qm-font-heading);
  font-size: 18px;
  font-weight: 800;
  color: var(--qm-text);
  line-height: 1;
}

.tq-sstat-lbl { font-size: 10px; color: var(--qm-text-muted); font-weight: 500; }
.tq-green  { color: var(--qm-success); }
.tq-muted  { color: var(--qm-text-muted); }

.tq-submit-side {
  width: 100%;
  padding: 11px;
  border-radius: var(--qm-radius);
  border: none;
  background: var(--qm-primary);
  color: white;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s;
}

.tq-submit-side:hover { background: var(--qm-primary-dark); }

/* ── Confirm Modal ────────────────────────────────────────── */
.tq-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
}

.tq-modal {
  background: var(--qm-surface);
  border-radius: var(--qm-radius-xl);
  width: 90%;
  max-width: 420px;
  box-shadow: var(--qm-shadow-xl);
  overflow: hidden;
}

.tq-modal-hdr {
  padding: 24px 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.tq-modal-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #FEF3C7;
  color: #92400E;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tq-modal-icon svg { width: 24px; height: 24px; }

.tq-modal-title {
  font-family: var(--qm-font-heading);
  font-size: 17px;
  font-weight: 800;
  color: var(--qm-text);
}

.tq-modal-body {
  padding: 0 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tq-modal-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--qm-bg);
  border-radius: var(--qm-radius);
  font-size: 14px;
  color: var(--qm-text-muted);
}

.tq-modal-warn {
  font-size: 12.5px;
  color: #92400E;
  background: #FEF3C7;
  padding: 8px 12px;
  border-radius: var(--qm-radius);
  margin: 4px 0 0;
}

.tq-error {
  background: var(--qm-danger-light);
  color: var(--qm-danger);
  padding: 10px 12px;
  border-radius: var(--qm-radius);
  font-size: 13px;
}

.tq-modal-footer {
  padding: 0 24px 24px;
  display: flex;
  gap: 10px;
}

.tq-btn-cancel,
.tq-btn-confirm {
  flex: 1;
  padding: 10px;
  border-radius: var(--qm-radius);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s;
}

.tq-btn-cancel {
  background: var(--qm-bg);
  color: var(--qm-text-muted);
  border: 1.5px solid var(--qm-border);
}

.tq-btn-cancel:hover:not(:disabled) { background: var(--qm-border-light); }

.tq-btn-confirm {
  background: var(--qm-primary);
  color: white;
}

.tq-btn-confirm:hover:not(:disabled) { background: var(--qm-primary-dark); }
.tq-btn-confirm:disabled,
.tq-btn-cancel:disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .tq-body       { grid-template-columns: 1fr; }
  .tq-sidebar    { border-left: none; border-top: 1px solid var(--qm-border); }
  .tq-qtext      { font-size: 15px; }
  .tq-quiz-sub   { display: none; }
}
</style>
