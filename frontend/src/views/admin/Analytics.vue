<template>
  <div class="analytics-page">

    <!-- ── Overview charts ──────────────────────────────────── -->
    <div class="section-label">Platform Overview</div>

    <div class="charts-row">
      <!-- Quiz performance bar chart -->
      <div class="chart-card wide">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-title">Average Score per Quiz</div>
            <div class="chart-sub">Top quizzes by number of attempts</div>
          </div>
        </div>
        <div class="chart-body">
          <Bar v-if="quizPerfData.labels.length" :data="quizPerfData" :options="barOpts" />
          <div v-else class="no-data">No quiz attempt data yet</div>
        </div>
      </div>

      <!-- Monthly attempts line chart -->
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-title">Monthly Attempts</div>
            <div class="chart-sub">Last 6 months</div>
          </div>
        </div>
        <div class="chart-body">
          <Line v-if="monthlyData.labels.length" :data="monthlyData" :options="lineOpts" />
          <div v-else class="no-data">No data yet</div>
        </div>
      </div>
    </div>

    <div class="charts-row">
      <!-- Subject performance bar -->
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-title">Subject-wise Performance</div>
            <div class="chart-sub">Average score % by subject</div>
          </div>
        </div>
        <div class="chart-body">
          <Bar v-if="subjPerfData.labels.length" :data="subjPerfData" :options="barOpts" />
          <div v-else class="no-data">No data yet</div>
        </div>
      </div>

      <!-- Score distribution doughnut -->
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-title">Score Distribution</div>
            <div class="chart-sub">All attempts across all students</div>
          </div>
        </div>
        <div class="chart-body doughnut-body">
          <Doughnut v-if="distTotal > 0" :data="distData" :options="doughnutOpts" />
          <div v-else class="no-data">No data yet</div>
        </div>
        <!-- Legend -->
        <div v-if="distTotal > 0" class="dist-legend">
          <div class="legend-item" v-for="(item, i) in distLegend" :key="i">
            <span class="legend-dot" :style="{ background: item.color }"></span>
            <span class="legend-label">{{ item.label }}</span>
            <span class="legend-val">{{ item.value }} <span class="legend-pct">({{ item.pct }}%)</span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Top performers ────────────────────────────────────── -->
    <div class="section-label">Top Performers</div>
    <div class="top-users-grid">
      <div
        v-for="(u, i) in overview.top_users"
        :key="u.id"
        class="top-user-card"
        @click="openStudent(u.id)"
      >
        <div class="rank-badge" :class="`rank-${i + 1}`">{{ i + 1 }}</div>
        <div class="top-user-avatar">{{ u.full_name.charAt(0).toUpperCase() }}</div>
        <div class="top-user-info">
          <div class="top-user-name">{{ u.full_name }}</div>
          <div class="top-user-attempts">{{ u.total_attempts }} attempts</div>
        </div>
        <div class="top-user-score" :class="scoreColor(u.avg_score)">
          {{ u.avg_score }}%
        </div>
      </div>
    </div>

    <!-- ── All students ───────────────────────────────────────── -->
    <div class="section-label" style="margin-top:8px">
      All Students
      <span class="section-count">{{ users.length }}</span>
    </div>

    <div class="students-toolbar">
      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="search" type="text" placeholder="Search students…" class="search-input" />
      </div>
    </div>

    <div class="students-table-wrap">
      <table class="students-table">
        <thead>
          <tr>
            <th>Student</th>
            <th>Email</th>
            <th>Attempts</th>
            <th>Avg Score</th>
            <th>Last Active</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in filteredUsers" :key="u.id" @click="openStudent(u.id)" class="student-row">
            <td>
              <div class="student-cell">
                <div class="s-avatar">{{ u.full_name.charAt(0).toUpperCase() }}</div>
                <span class="s-name">{{ u.full_name }}</span>
              </div>
            </td>
            <td class="cell-muted">{{ u.username }}</td>
            <td>
              <span class="attempts-pill">{{ u.total_attempts }}</span>
            </td>
            <td>
              <div class="score-bar-wrap" v-if="u.total_attempts > 0">
                <div class="score-bar">
                  <div class="score-bar-fill" :class="scoreColor(u.avg_score)" :style="{ width: u.avg_score + '%' }"></div>
                </div>
                <span class="score-pct" :class="scoreColor(u.avg_score)">{{ u.avg_score }}%</span>
              </div>
              <span v-else class="cell-muted">—</span>
            </td>
            <td class="cell-muted">{{ formatDate(u.last_attempt) }}</td>
            <td>
              <button class="btn-profile" @click.stop="openStudent(u.id)">View</button>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="6" class="empty-cell">No students found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ── Student detail panel ──────────────────────────────── -->
    <div v-if="showPanel" class="panel-overlay" @click.self="closePanel">
      <div class="student-panel">
        <!-- Panel header -->
        <div class="panel-hdr">
          <div class="panel-user-info">
            <div class="panel-avatar">{{ selectedStudent?.user?.full_name?.charAt(0)?.toUpperCase() }}</div>
            <div>
              <div class="panel-name">{{ selectedStudent?.user?.full_name }}</div>
              <div class="panel-email">{{ selectedStudent?.user?.username }}</div>
            </div>
          </div>
          <button @click="closePanel" class="panel-close">&times;</button>
        </div>

        <!-- Summary stats -->
        <div class="panel-stats">
          <div class="panel-stat">
            <div class="ps-value">{{ selectedStudent?.total_attempts }}</div>
            <div class="ps-label">Attempts</div>
          </div>
          <div class="panel-stat">
            <div class="ps-value" :class="scoreColor(selectedStudent?.avg_score)">{{ selectedStudent?.avg_score }}%</div>
            <div class="ps-label">Avg Score</div>
          </div>
          <div class="panel-stat">
            <div class="ps-value">{{ selectedStudent?.subject_performance?.length }}</div>
            <div class="ps-label">Subjects</div>
          </div>
        </div>

        <div v-if="panelLoading" class="panel-loading">
          <div class="spinner"></div>
        </div>

        <template v-else-if="selectedStudent">
          <!-- Score trend line chart -->
          <div class="panel-chart-wrap">
            <div class="panel-chart-title">Score Trend</div>
            <div class="panel-chart-body">
              <Line
                v-if="studentTrendData.labels.length"
                :data="studentTrendData"
                :options="panelLineOpts"
              />
              <div v-else class="no-data">No attempts yet</div>
            </div>
          </div>

          <!-- Subject doughnut -->
          <div class="panel-chart-wrap">
            <div class="panel-chart-title">Performance by Subject</div>
            <div class="panel-chart-body doughnut-body-sm">
              <Doughnut
                v-if="studentSubjData.labels.length"
                :data="studentSubjData"
                :options="doughnutOpts"
              />
              <div v-else class="no-data">No subject data</div>
            </div>
          </div>
        </template>
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
  name: 'AdminAnalytics',
  components: { Bar, Line, Doughnut },

  data() {
    return {
      overview: {
        quiz_performance: [],
        monthly_attempts: [],
        subject_performance: [],
        top_users: [],
        score_distribution: { '0-40': 0, '40-70': 0, '70-100': 0 }
      },
      users: [],
      search: '',
      showPanel: false,
      panelLoading: false,
      selectedStudent: null,
    }
  },

  computed: {
    filteredUsers() {
      const q = this.search.toLowerCase()
      return this.users.filter(u =>
        u.full_name.toLowerCase().includes(q) ||
        u.username.toLowerCase().includes(q)
      )
    },

    // Quiz performance bar
    quizPerfData() {
      const d = this.overview.quiz_performance
      return {
        labels: d.map(r => this.shorten(r.quiz_title, 20)),
        datasets: [{
          label: 'Avg Score (%)',
          data: d.map(r => r.avg_score),
          backgroundColor: d.map((_, i) => PALETTE[i % PALETTE.length] + 'CC'),
          borderColor: d.map((_, i) => PALETTE[i % PALETTE.length]),
          borderWidth: 1,
          borderRadius: 6,
        }]
      }
    },

    // Monthly line
    monthlyData() {
      const d = this.overview.monthly_attempts
      return {
        labels: d.map(r => r.month),
        datasets: [{
          label: 'Attempts',
          data: d.map(r => r.count),
          borderColor: '#4F46E5',
          backgroundColor: 'rgba(79,70,229,0.12)',
          borderWidth: 2,
          pointBackgroundColor: '#4F46E5',
          pointRadius: 4,
          tension: 0.4,
          fill: true
        }]
      }
    },

    // Subject bar
    subjPerfData() {
      const d = this.overview.subject_performance
      return {
        labels: d.map(r => r.subject_name),
        datasets: [{
          label: 'Avg Score (%)',
          data: d.map(r => r.avg_score),
          backgroundColor: d.map((_, i) => PALETTE[i % PALETTE.length] + 'CC'),
          borderColor: d.map((_, i) => PALETTE[i % PALETTE.length]),
          borderWidth: 1,
          borderRadius: 6,
        }]
      }
    },

    // Distribution doughnut
    distTotal() {
      const d = this.overview.score_distribution
      return (d['0-40'] || 0) + (d['40-70'] || 0) + (d['70-100'] || 0)
    },
    distData() {
      const d = this.overview.score_distribution
      return {
        labels: ['Below 40%', '40–70%', 'Above 70%'],
        datasets: [{
          data: [d['0-40'], d['40-70'], d['70-100']],
          backgroundColor: ['#FEF2F2', '#FFFBEB', '#ECFDF5'],
          borderColor: ['#EF4444', '#F59E0B', '#10B981'],
          borderWidth: 2,
        }]
      }
    },
    distLegend() {
      const d = this.overview.score_distribution
      const t = this.distTotal || 1
      return [
        { label: 'Below 40%', value: d['0-40'], pct: Math.round(d['0-40'] / t * 100), color: '#EF4444' },
        { label: '40 – 70%',  value: d['40-70'], pct: Math.round(d['40-70'] / t * 100), color: '#F59E0B' },
        { label: 'Above 70%', value: d['70-100'], pct: Math.round(d['70-100'] / t * 100), color: '#10B981' },
      ]
    },

    // Student detail charts
    studentTrendData() {
      const d = this.selectedStudent?.score_trend || []
      return {
        labels: d.map(r => r.date),
        datasets: [{
          label: 'Score (%)',
          data: d.map(r => r.percentage),
          borderColor: '#4F46E5',
          backgroundColor: 'rgba(79,70,229,0.12)',
          borderWidth: 2,
          pointBackgroundColor: '#4F46E5',
          pointRadius: 4,
          tension: 0.4,
          fill: true
        }]
      }
    },
    studentSubjData() {
      const d = this.selectedStudent?.subject_performance || []
      return {
        labels: d.map(r => r.subject_name),
        datasets: [{
          data: d.map(r => r.avg_score),
          backgroundColor: d.map((_, i) => PALETTE[i % PALETTE.length] + 'CC'),
          borderColor: d.map((_, i) => PALETTE[i % PALETTE.length]),
          borderWidth: 2,
        }]
      }
    },

    // Chart options
    barOpts() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: '#F1F5F9' },
               ticks: { color: '#64748B', font: { size: 11 } } },
          x: { grid: { display: false },
               ticks: { color: '#64748B', font: { size: 11 } } }
        }
      }
    },
    lineOpts() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: '#F1F5F9' },
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
        cutout: '65%'
      }
    },
    panelLineOpts() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: ctx => ctx.parsed.y + '%' } } },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: '#F1F5F9' },
               ticks: { color: '#64748B', font: { size: 10 } } },
          x: { grid: { display: false },
               ticks: { color: '#64748B', font: { size: 10 }, maxRotation: 45 } }
        }
      }
    }
  },

  async mounted() {
    await Promise.all([this.fetchOverview(), this.fetchUsers()])
  },

  methods: {
    async fetchOverview() {
      try {
        const res = await axios.get('/admin/analytics/overview')
        this.overview = res.data
      } catch (e) {
        console.error('Failed to fetch overview:', e)
      }
    },
    async fetchUsers() {
      try {
        const res = await axios.get('/admin/analytics/users')
        this.users = res.data
      } catch (e) {
        console.error('Failed to fetch users:', e)
      }
    },
    async openStudent(userId) {
      this.showPanel = true
      this.panelLoading = true
      this.selectedStudent = null
      try {
        const res = await axios.get(`/admin/analytics/user/${userId}`)
        this.selectedStudent = res.data
      } catch (e) {
        console.error('Failed to fetch student analytics:', e)
      } finally {
        this.panelLoading = false
      }
    },
    closePanel() {
      this.showPanel = false
      this.selectedStudent = null
    },
    scoreColor(pct) {
      if (pct >= 70) return 'color-green'
      if (pct >= 40) return 'color-amber'
      return 'color-red'
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    },
    shorten(str, max) {
      return str && str.length > max ? str.slice(0, max) + '…' : (str || '')
    }
  }
}
</script>

<style scoped>
.analytics-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── Section labels ───────────────────────────────────────── */
.section-label {
  font-family: var(--qm-font-heading);
  font-size: 14px;
  font-weight: 700;
  color: var(--qm-text);
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--qm-border-light);
}

.section-count {
  padding: 2px 8px;
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

/* ── Chart rows ───────────────────────────────────────────── */
.charts-row {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 16px;
}

.chart-card {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  box-shadow: var(--qm-shadow);
  display: flex;
  flex-direction: column;
}

.chart-card.wide { /* inherits */ }

.chart-card-hdr {
  padding: 16px 20px 12px;
  border-bottom: 1px solid var(--qm-border-light);
}

.chart-title {
  font-family: var(--qm-font-heading);
  font-weight: 600;
  font-size: 14px;
  color: var(--qm-text);
  margin-bottom: 2px;
}

.chart-sub {
  font-size: 12px;
  color: var(--qm-text-muted);
}

.chart-body {
  flex: 1;
  padding: 16px;
  min-height: 220px;
  position: relative;
}

.doughnut-body {
  min-height: 160px;
  max-height: 180px;
}

.doughnut-body-sm {
  min-height: 140px;
  max-height: 160px;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 120px;
  color: var(--qm-text-light);
  font-size: 13px;
}

/* Distribution legend */
.dist-legend {
  padding: 0 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  color: var(--qm-text-muted);
  flex: 1;
}

.legend-val {
  font-weight: 600;
  color: var(--qm-text);
}

.legend-pct {
  font-weight: 400;
  color: var(--qm-text-muted);
}

/* ── Top performers ───────────────────────────────────────── */
.top-users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.top-user-card {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--qm-shadow);
}

.top-user-card:hover {
  border-color: var(--qm-primary);
  transform: translateY(-2px);
  box-shadow: var(--qm-shadow-md);
}

.rank-badge {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.rank-1 { background: #FEF3C7; color: #92400E; }
.rank-2 { background: #F1F5F9; color: #475569; }
.rank-3 { background: #FEF2F2; color: #B91C1C; }
.rank-4, .rank-5 { background: var(--qm-primary-light); color: var(--qm-primary); }

.top-user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
  flex-shrink: 0;
}

.top-user-info { flex: 1; min-width: 0; }
.top-user-name { font-weight: 600; font-size: 13px; color: var(--qm-text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.top-user-attempts { font-size: 11px; color: var(--qm-text-muted); margin-top: 2px; }

.top-user-score {
  font-family: var(--qm-font-heading);
  font-weight: 700;
  font-size: 15px;
  flex-shrink: 0;
}

/* ── Students table ───────────────────────────────────────── */
.students-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-wrap {
  position: relative;
  max-width: 300px;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 15px;
  height: 15px;
  color: var(--qm-text-light);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 32px;
  border: 1.5px solid var(--qm-border);
  border-radius: var(--qm-radius);
  font-size: 13px;
  color: var(--qm-text);
  font-family: var(--qm-font-body);
  background: var(--qm-surface);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.search-input:focus {
  border-color: var(--qm-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.students-table-wrap {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
}

.students-table {
  width: 100%;
  border-collapse: collapse;
}

.students-table thead th {
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

.students-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--qm-border-light);
  font-size: 13px;
  vertical-align: middle;
}

.students-table tbody tr:last-child td { border-bottom: none; }

.student-row {
  cursor: pointer;
  transition: background 0.1s;
}
.student-row:hover { background: var(--qm-bg); }

.student-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.s-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  flex-shrink: 0;
}

.s-name { font-weight: 500; color: var(--qm-text); }
.cell-muted { color: var(--qm-text-muted); font-size: 12px; }

.attempts-pill {
  display: inline-block;
  padding: 2px 10px;
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.score-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-bar {
  flex: 1;
  height: 6px;
  background: var(--qm-border-light);
  border-radius: 3px;
  overflow: hidden;
  min-width: 60px;
}

.score-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.color-green.score-bar-fill { background: var(--qm-success); }
.color-amber.score-bar-fill { background: var(--qm-warning); }
.color-red.score-bar-fill   { background: var(--qm-danger); }

.score-pct {
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  min-width: 36px;
  text-align: right;
}

.color-green { color: var(--qm-success); }
.color-amber { color: var(--qm-warning); }
.color-red   { color: var(--qm-danger); }

.btn-profile {
  padding: 5px 12px;
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-sm);
  background: none;
  font-size: 12px;
  font-weight: 500;
  color: var(--qm-primary);
  cursor: pointer;
  transition: all 0.15s;
}
.btn-profile:hover { background: var(--qm-primary-light); border-color: var(--qm-primary); }

.empty-cell {
  text-align: center;
  padding: 40px 24px;
  color: var(--qm-text-muted);
  font-size: 13px;
}

/* ── Student detail panel ────────────────────────────────── */
.panel-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  z-index: 200;
  display: flex;
  justify-content: flex-end;
  backdrop-filter: blur(2px);
}

.student-panel {
  width: 440px;
  max-width: 95vw;
  background: var(--qm-surface);
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  box-shadow: var(--qm-shadow-xl);
  animation: slideIn 0.25s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to   { transform: translateX(0); }
}

.panel-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--qm-border);
  position: sticky;
  top: 0;
  background: var(--qm-surface);
  z-index: 10;
}

.panel-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.panel-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  flex-shrink: 0;
}

.panel-name  { font-weight: 700; font-size: 15px; color: var(--qm-text); }
.panel-email { font-size: 12px; color: var(--qm-text-muted); margin-top: 2px; }

.panel-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--qm-text-muted);
  padding: 4px 8px;
  border-radius: var(--qm-radius-sm);
  transition: all 0.15s;
  line-height: 1;
}
.panel-close:hover { background: var(--qm-bg); color: var(--qm-text); }

.panel-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--qm-border-light);
  border-bottom: 1px solid var(--qm-border);
}

.panel-stat {
  background: var(--qm-surface);
  padding: 16px;
  text-align: center;
}

.ps-value {
  font-family: var(--qm-font-heading);
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--qm-text);
  line-height: 1;
  margin-bottom: 4px;
}

.ps-label {
  font-size: 11px;
  color: var(--qm-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 500;
}

.panel-loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--qm-border);
  border-top-color: var(--qm-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.panel-chart-wrap {
  padding: 20px 24px;
  border-bottom: 1px solid var(--qm-border-light);
}

.panel-chart-title {
  font-family: var(--qm-font-heading);
  font-weight: 600;
  font-size: 13px;
  color: var(--qm-text);
  margin-bottom: 12px;
}

.panel-chart-body {
  position: relative;
  min-height: 180px;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 1024px) {
  .charts-row { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .top-users-grid { grid-template-columns: 1fr 1fr; }
  .student-panel  { width: 100%; }
}
</style>
