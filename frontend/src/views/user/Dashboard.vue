<template>
  <div class="user-dash">
    <!-- Welcome banner -->
    <div class="welcome-banner">
      <div class="welcome-text">
        <h2>Welcome back, {{ user?.full_name || 'there' }}!</h2>
        <p>Here's a snapshot of your quiz activity.</p>
      </div>
      <router-link to="/quizzes" class="btn-start">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        Browse Quizzes
      </router-link>
    </div>

    <!-- Stats cards -->
    <div class="stats-grid">
      <div class="stat-card stat-accent-blue">
        <div class="stat-icon icon-blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <div>
          <div class="stat-value">{{ dashboardData.total_attempts }}</div>
          <div class="stat-label">Total Attempts</div>
        </div>
      </div>

      <div class="stat-card stat-accent-green">
        <div class="stat-icon icon-green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        </div>
        <div>
          <div class="stat-value">{{ dashboardData.average_score }}%</div>
          <div class="stat-label">Average Score</div>
        </div>
      </div>

      <div class="stat-card stat-accent-purple">
        <div class="stat-icon icon-purple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        </div>
        <div>
          <div class="stat-value">{{ dashboardData.available_quizzes }}</div>
          <div class="stat-label">Available Quizzes</div>
        </div>
      </div>

      <div class="stat-card stat-accent-amber">
        <div class="stat-icon icon-amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <div>
          <div class="stat-value">{{ monthlyAttempts }}</div>
          <div class="stat-label">This Month</div>
        </div>
      </div>
    </div>

    <!-- ── Analytics charts ──────────────────────────────────── -->
    <div class="analytics-section" v-if="analyticsLoaded">
      <div class="analytics-hdr">
        <div class="analytics-title">Your Analytics</div>
      </div>
      <div class="analytics-grid">

        <!-- Score trend -->
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div class="chart-title">Score Trend</div>
            <div class="chart-sub">Your scores over time</div>
          </div>
          <div class="chart-body">
            <Line v-if="trendData.labels.length" :data="trendData" :options="lineOpts" />
            <div v-else class="no-data">Take some quizzes to see your trend</div>
          </div>
        </div>

        <!-- Subject performance doughnut -->
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div class="chart-title">By Subject</div>
            <div class="chart-sub">Average score per subject</div>
          </div>
          <div class="chart-body chart-body-sm">
            <Doughnut v-if="subjData.labels.length" :data="subjData" :options="doughnutOpts" />
            <div v-else class="no-data">No subject data yet</div>
          </div>
          <div class="subj-legend" v-if="subjData.labels.length">
            <div class="subj-leg-item" v-for="(lbl, i) in subjData.labels" :key="i">
              <span class="leg-dot" :style="{ background: PALETTE[i % PALETTE.length] }"></span>
              <span class="leg-lbl">{{ lbl }}</span>
              <span class="leg-val">{{ analytics.subject_performance[i]?.avg_score }}%</span>
            </div>
          </div>
        </div>

        <!-- vs Class average grouped bar -->
        <div class="chart-card wide">
          <div class="chart-card-hdr">
            <div class="chart-title">You vs Class Average</div>
            <div class="chart-sub">Your score compared to all students per quiz</div>
          </div>
          <div class="chart-body">
            <Bar v-if="compData.labels.length" :data="compData" :options="barOpts" />
            <div v-else class="no-data">Attempt quizzes to see how you compare</div>
          </div>
        </div>

      </div>
    </div>

    <!-- ── Subject Progress ──────────────────────────────────── -->
    <div class="section-grid" v-if="subjectProgress.length">
      <!-- Subject Progress -->
      <div class="card-panel">
        <div class="panel-hdr">
          <span class="panel-title">Subject Progress</span>
        </div>
        <div class="subj-progress-list">
          <div v-for="s in subjectProgress" :key="s.subject" class="subj-row">
            <div class="subj-row-top">
              <span class="subj-name">{{ s.subject }}</span>
              <span class="subj-stats">{{ s.attempted }}/{{ s.total }} · {{ s.avg_score }}%</span>
            </div>
            <div class="subj-bar">
              <div class="subj-bar-fill" :style="{ width: s.pct_done + '%', background: subjectColor(s.subject) }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Leaderboard -->
      <div class="card-panel">
        <div class="panel-hdr">
          <span class="panel-title">Leaderboard</span>
          <span class="panel-tag">Top Students</span>
        </div>
        <div class="leaderboard-list">
          <div v-for="entry in leaderboard" :key="entry.rank" class="lb-item"
            :class="{ 'lb-me': entry.user_id === currentUserId }">
            <div class="lb-rank" :class="['lb-rank-' + Math.min(entry.rank, 4)]">{{ entry.rank }}</div>
            <div class="lb-avatar" :style="{ background: rankGradient(entry.rank) }">
              {{ entry.name.charAt(0).toUpperCase() }}
            </div>
            <div class="lb-info">
              <div class="lb-name">{{ entry.name }} <span v-if="entry.user_id === currentUserId" class="lb-you">You</span></div>
              <div class="lb-sub">{{ entry.attempts }} attempts</div>
            </div>
            <div class="lb-score" :style="{ color: scoreColor(entry.avg_score) }">{{ entry.avg_score }}%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Two-column layout -->
    <div class="lower-grid">
      <!-- Recent attempts -->
      <div class="card-panel recent-panel">
        <div class="panel-hdr">
          <span class="panel-title">Recent Attempts</span>
          <router-link to="/quizzes" class="panel-link">Browse more →</router-link>
        </div>

        <div v-if="dashboardData.recent_attempts.length === 0" class="panel-empty">
          <div class="empty-icon">🎯</div>
          <p>No attempts yet.</p>
          <router-link to="/quizzes" class="btn-start-sm">Take your first quiz</router-link>
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Quiz</th>
              <th>Score</th>
              <th>Date</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="attempt in dashboardData.recent_attempts" :key="attempt.id">
              <td class="cell-quiz">{{ attempt.quiz_title }}</td>
              <td>
                <span class="score-badge" :class="getScoreClass(attempt.percentage)">
                  {{ attempt.total_scored }}/{{ attempt.total_marks }} ({{ attempt.percentage }}%)
                </span>
              </td>
              <td class="cell-date">{{ formatDate(attempt.timestamp_of_attempt) }}</td>
              <td>
                <router-link :to="`/quiz/results/${attempt.id}`" class="btn-view">
                  View
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Right column: Profile + Actions -->
      <div class="side-col">
        <!-- Profile card -->
        <div class="card-panel">
          <div class="panel-hdr">
            <span class="panel-title">Profile</span>
          </div>
          <div class="profile-body">
            <div class="profile-avatar">{{ userInitial }}</div>
            <div class="profile-info">
              <div class="profile-name">{{ user?.full_name }}</div>
              <div class="profile-email">{{ user?.username }}</div>
              <div v-if="user?.qualification" class="profile-qual">{{ user.qualification }}</div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card-panel">
          <div class="panel-hdr">
            <span class="panel-title">Quick Actions</span>
          </div>
          <div class="actions-list">
            <router-link to="/quizzes" class="action-item">
              <div class="action-icon icon-blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
              </div>
              <span>Browse Quizzes</span>
              <svg class="action-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>

            <button @click="exportData" class="action-item action-btn">
              <div class="action-icon icon-green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </div>
              <span>Export My Data</span>
              <svg class="action-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {
  Chart as ChartJS,
  CategoryScale, LinearScale,
  BarElement, LineElement, PointElement,
  ArcElement,
  Title, Tooltip, Legend, Filler
} from 'chart.js'
import { Bar, Line, Doughnut } from 'vue-chartjs'

ChartJS.register(
  CategoryScale, LinearScale,
  BarElement, LineElement, PointElement,
  ArcElement,
  Title, Tooltip, Legend, Filler
)

const PALETTE = ['#4F46E5', '#7C3AED', '#10B981', '#F59E0B', '#EF4444', '#3B82F6', '#EC4899', '#14B8A6']

export default {
  name: 'UserDashboard',
  components: { Bar, Line, Doughnut },

  data() {
    return {
      PALETTE,
      dashboardData: {
        total_attempts: 0,
        average_score: 0,
        recent_attempts: [],
        available_quizzes: 0
      },
      analytics: {
        score_trend: [],
        subject_performance: [],
        comparison: []
      },
      analyticsLoaded: false,
      leaderboard: [],
      subjectProgress: []
    }
  },

  computed: {
    user()          { return this.$store.state.user },
    userInitial()   { return (this.user?.full_name || 'U').charAt(0).toUpperCase() },
    currentUserId() { return this.user?.id || null },
    monthlyAttempts() {
      const m = new Date().getMonth()
      return this.dashboardData.recent_attempts.filter(a =>
        new Date(a.timestamp_of_attempt).getMonth() === m
      ).length
    },

    // Score trend line chart
    trendData() {
      const d = this.analytics.score_trend
      return {
        labels: d.map(r => r.date),
        datasets: [{
          label: 'Score (%)',
          data: d.map(r => r.percentage),
          borderColor: '#4F46E5',
          backgroundColor: 'rgba(79,70,229,0.1)',
          borderWidth: 2,
          pointBackgroundColor: '#4F46E5',
          pointRadius: 4,
          tension: 0.4,
          fill: true
        }]
      }
    },

    // Subject doughnut
    subjData() {
      const d = this.analytics.subject_performance
      return {
        labels: d.map(r => r.subject_name),
        datasets: [{
          data: d.map(r => r.avg_score),
          backgroundColor: d.map((_, i) => PALETTE[i % PALETTE.length] + 'CC'),
          borderColor: d.map((_, i) => PALETTE[i % PALETTE.length]),
          borderWidth: 2
        }]
      }
    },

    // Comparison grouped bar
    compData() {
      const d = this.analytics.comparison
      return {
        labels: d.map(r => r.quiz_title.length > 18 ? r.quiz_title.slice(0, 18) + '…' : r.quiz_title),
        datasets: [
          {
            label: 'My Score',
            data: d.map(r => r.my_score),
            backgroundColor: 'rgba(79,70,229,0.8)',
            borderColor: '#4F46E5',
            borderWidth: 1,
            borderRadius: 4
          },
          {
            label: 'Class Avg',
            data: d.map(r => r.avg_score),
            backgroundColor: 'rgba(16,185,129,0.8)',
            borderColor: '#10B981',
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      }
    },

    lineOpts() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => ctx.parsed.y + '%' } }
        },
        scales: {
          y: { beginAtZero: true, max: 100,
               grid: { color: '#F1F5F9' },
               ticks: { color: '#64748B', font: { size: 11 } } },
          x: { grid: { display: false },
               ticks: { color: '#64748B', font: { size: 11 } } }
        }
      }
    },

    doughnutOpts() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        cutout: '62%'
      }
    },

    barOpts() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { font: { size: 11 }, usePointStyle: true, padding: 16 } },
          tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y + '%' } }
        },
        scales: {
          y: { beginAtZero: true, max: 100,
               grid: { color: '#F1F5F9' },
               ticks: { color: '#64748B', font: { size: 11 } } },
          x: { grid: { display: false },
               ticks: { color: '#64748B', font: { size: 11 } } }
        }
      }
    }
  },

  async mounted() {
    await Promise.all([
      this.fetchDashboard(),
      this.fetchAnalytics(),
      this.fetchLeaderboard(),
      this.fetchSubjectProgress(),
    ])
  },

  methods: {
    async fetchDashboard() {
      try {
        const res = await axios.get('/user/dashboard')
        this.dashboardData = res.data
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)
      }
    },
    async fetchAnalytics() {
      try {
        const res = await axios.get('/user/analytics')
        this.analytics = res.data
        this.analyticsLoaded = true
      } catch (err) {
        console.error('Failed to fetch analytics:', err)
        this.analyticsLoaded = true
      }
    },
    async fetchLeaderboard() {
      try { this.leaderboard = (await axios.get('/user/leaderboard')).data } catch (e) { console.error(e) }
    },
    async fetchSubjectProgress() {
      try { this.subjectProgress = (await axios.get('/user/subject-progress')).data } catch (e) { console.error(e) }
    },
    subjectColor(name) {
      const map = { Physics: '#3B82F6', Chemistry: '#10B981', Mathematics: '#4F46E5', Biology: '#059669', English: '#F59E0B' }
      return map[name] || '#64748B'
    },
    scoreColor(pct) {
      if (pct >= 70) return '#10B981'
      if (pct >= 40) return '#F59E0B'
      return '#EF4444'
    },
    rankGradient(rank) {
      if (rank === 1) return 'linear-gradient(135deg,#F59E0B,#FCD34D)'
      if (rank === 2) return 'linear-gradient(135deg,#94A3B8,#CBD5E1)'
      if (rank === 3) return 'linear-gradient(135deg,#C2410C,#F97316)'
      return 'linear-gradient(135deg,var(--qm-primary),var(--qm-secondary))'
    },
    getScoreClass(pct) {
      if (pct >= 70) return 'badge-green'
      if (pct >= 40) return 'badge-amber'
      return 'badge-red'
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    },
    async exportData() {
      try {
        await axios.post('/user/export-data')
        alert('Export started! You will receive an email when ready.')
      } catch (err) {
        console.error('Export failed:', err)
        alert('Export failed. Please try again.')
      }
    }
  }
}
</script>

<style scoped>
.user-dash {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── Welcome ──────────────────────────────────────────────── */
.welcome-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, var(--qm-primary) 0%, var(--qm-secondary) 100%);
  border-radius: var(--qm-radius-xl);
  padding: 28px 32px;
  gap: 16px;
  flex-wrap: wrap;
}

.welcome-text h2 {
  color: white;
  font-size: 1.375rem;
  margin-bottom: 4px;
}

.welcome-text p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
}

.btn-start {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  color: var(--qm-primary);
  border-radius: var(--qm-radius);
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
  flex-shrink: 0;
  white-space: nowrap;
}

.btn-start svg { width: 16px; height: 16px; }

.btn-start:hover {
  background: var(--qm-primary-light);
  transform: translateY(-1px);
}

/* ── Stats ────────────────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 16px;
}

.stat-card {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: var(--qm-shadow);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--qm-shadow-md);
}

.stat-icon {
  width: 46px;
  height: 46px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg { width: 20px; height: 20px; }

.icon-blue   { background: var(--qm-primary-light); color: var(--qm-primary); }
.icon-green  { background: var(--qm-success-light); color: var(--qm-success); }
.icon-purple { background: #F3E8FF; color: var(--qm-secondary); }
.icon-amber  { background: var(--qm-warning-light); color: var(--qm-warning); }

.stat-value {
  font-family: var(--qm-font-heading);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--qm-text);
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12.5px;
  color: var(--qm-text-muted);
  font-weight: 500;
}

/* ── Lower grid ───────────────────────────────────────────── */
.lower-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
  align-items: start;
}

.card-panel {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
}

.panel-hdr {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--qm-border-light);
}

.panel-title {
  font-family: var(--qm-font-heading);
  font-weight: 600;
  font-size: 14px;
  color: var(--qm-text);
}

.panel-link {
  font-size: 13px;
  color: var(--qm-primary);
  font-weight: 500;
  text-decoration: none;
}
.panel-link:hover { text-decoration: underline; }

/* Table */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead th {
  padding: 10px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--qm-text-muted);
  border-bottom: 1px solid var(--qm-border);
  background: var(--qm-bg);
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--qm-border-light);
  font-size: 14px;
  vertical-align: middle;
}

.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover { background: var(--qm-bg); }

.cell-quiz { font-weight: 500; color: var(--qm-text); }
.cell-date { color: var(--qm-text-muted); font-size: 13px; white-space: nowrap; }

.score-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-green { background: var(--qm-success-light); color: var(--qm-success); }
.badge-amber { background: var(--qm-warning-light); color: #92400E; }
.badge-red   { background: var(--qm-danger-light);  color: var(--qm-danger); }

.btn-view {
  padding: 5px 12px;
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-sm);
  font-size: 12px;
  font-weight: 500;
  color: var(--qm-primary);
  text-decoration: none;
  transition: all 0.15s;
  white-space: nowrap;
}
.btn-view:hover { background: var(--qm-primary-light); border-color: var(--qm-primary); }

/* Empty */
.panel-empty {
  padding: 40px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.empty-icon { font-size: 2.5rem; }

.panel-empty p {
  color: var(--qm-text-muted);
  font-size: 14px;
  margin: 0;
}

.btn-start-sm {
  padding: 8px 16px;
  background: var(--qm-primary);
  color: white;
  border-radius: var(--qm-radius);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  margin-top: 4px;
  transition: background 0.15s;
}
.btn-start-sm:hover { background: var(--qm-primary-dark); }

/* Side column */
.side-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Profile */
.profile-body {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--qm-font-heading);
  font-weight: 700;
  font-size: 20px;
  flex-shrink: 0;
}

.profile-name  { font-weight: 600; font-size: 14px; color: var(--qm-text); margin-bottom: 2px; }
.profile-email { font-size: 12.5px; color: var(--qm-text-muted); }
.profile-qual  { font-size: 12px; color: var(--qm-text-light); margin-top: 2px; }

/* Actions list */
.actions-list {
  display: flex;
  flex-direction: column;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  text-decoration: none;
  color: var(--qm-text);
  font-size: 14px;
  font-weight: 500;
  border-bottom: 1px solid var(--qm-border-light);
  transition: background 0.15s;
}

.action-item:last-child { border-bottom: none; }
.action-item:hover { background: var(--qm-bg); }

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--qm-font-body);
  width: 100%;
  text-align: left;
}

.action-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-icon svg { width: 16px; height: 16px; }

.action-arrow {
  width: 14px;
  height: 14px;
  color: var(--qm-text-light);
  margin-left: auto;
  flex-shrink: 0;
}

/* ── Analytics section ────────────────────────────────────── */
.analytics-section {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-xl);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
}

.analytics-hdr {
  padding: 16px 20px;
  border-bottom: 1px solid var(--qm-border-light);
  background: var(--qm-bg);
}

.analytics-title {
  font-family: var(--qm-font-heading);
  font-weight: 700;
  font-size: 14px;
  color: var(--qm-text);
}

.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1px;
  background: var(--qm-border-light);
}

.chart-card {
  background: var(--qm-surface);
  display: flex;
  flex-direction: column;
}

.chart-card.wide {
  grid-column: 1 / -1;
}

.chart-card-hdr {
  padding: 14px 18px 10px;
  border-bottom: 1px solid var(--qm-border-light);
}

.chart-title {
  font-family: var(--qm-font-heading);
  font-weight: 600;
  font-size: 13px;
  color: var(--qm-text);
  margin-bottom: 2px;
}

.chart-sub {
  font-size: 11.5px;
  color: var(--qm-text-muted);
}

.chart-body {
  padding: 14px 16px;
  min-height: 200px;
  position: relative;
}

.chart-body-sm {
  min-height: 150px;
  max-height: 165px;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 120px;
  color: var(--qm-text-light);
  font-size: 13px;
  text-align: center;
}

/* Subject legend */
.subj-legend {
  padding: 0 18px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.subj-leg-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.leg-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.leg-lbl {
  flex: 1;
  color: var(--qm-text-muted);
}

.leg-val {
  font-weight: 600;
  color: var(--qm-text);
}

/* ── Section Grid (subject progress + leaderboard) ───────── */
.section-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

/* Subject progress */
.subj-progress-list {
  padding: 8px 0;
}

.subj-row {
  padding: 10px 20px;
  border-bottom: 1px solid var(--qm-border-light);
}

.subj-row:last-child { border-bottom: none; }

.subj-row-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.subj-name {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--qm-text);
}

.subj-stats {
  font-size: 12px;
  color: var(--qm-text-muted);
}

.subj-bar {
  height: 6px;
  background: var(--qm-bg);
  border-radius: 3px;
  overflow: hidden;
}

.subj-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Leaderboard */
.panel-tag {
  padding: 2px 8px;
  border-radius: 20px;
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-size: 10.5px;
  font-weight: 700;
}

.leaderboard-list {
  padding: 6px 0;
}

.lb-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-bottom: 1px solid var(--qm-border-light);
  transition: background 0.15s;
}

.lb-item:last-child { border-bottom: none; }
.lb-item:hover { background: var(--qm-bg); }

.lb-me {
  background: var(--qm-primary-light) !important;
}

.lb-rank {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
  flex-shrink: 0;
  background: var(--qm-bg);
  color: var(--qm-text-muted);
  border: 1px solid var(--qm-border);
}

.lb-rank-1 { background: #FEF3C7; color: #92400E; border-color: #FCD34D; }
.lb-rank-2 { background: #F1F5F9; color: #475569; border-color: #CBD5E1; }
.lb-rank-3 { background: #FEF0E7; color: #9A3412; border-color: #FDBA74; }

.lb-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  color: white;
  flex-shrink: 0;
}

.lb-info { flex: 1; min-width: 0; }

.lb-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--qm-text);
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.lb-you {
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  background: var(--qm-primary);
  color: white;
  border-radius: 10px;
  flex-shrink: 0;
}

.lb-sub {
  font-size: 11px;
  color: var(--qm-text-muted);
}

.lb-score {
  font-family: var(--qm-font-heading);
  font-size: 14px;
  font-weight: 800;
  flex-shrink: 0;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 900px) {
  .lower-grid    { grid-template-columns: 1fr; }
  .analytics-grid { grid-template-columns: 1fr; }
  .chart-card.wide { grid-column: 1; }
  .section-grid  { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
  .welcome-banner { padding: 20px; }
  .stats-grid     { grid-template-columns: 1fr 1fr; }
}
</style>
