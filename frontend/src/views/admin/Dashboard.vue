<template>
  <div class="admin-dash">
    <!-- Stat cards -->
    <div class="stats-grid">
      <div class="stat-card stat-accent-blue">
        <div class="stat-icon icon-blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.total_users }}</div>
          <div class="stat-label">Total Users</div>
        </div>
      </div>

      <div class="stat-card stat-accent-purple">
        <div class="stat-icon icon-purple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        </div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.total_subjects }}</div>
          <div class="stat-label">Subjects</div>
        </div>
      </div>

      <div class="stat-card stat-accent-green">
        <div class="stat-icon icon-green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        </div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.total_quizzes }}</div>
          <div class="stat-label">Quizzes</div>
        </div>
      </div>

      <div class="stat-card stat-accent-amber">
        <div class="stat-icon icon-amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <div class="stat-body">
          <div class="stat-value">{{ stats.total_attempts }}</div>
          <div class="stat-label">Attempts</div>
        </div>
      </div>
    </div>

    <!-- Quick nav -->
    <div class="section-title">Manage Content</div>
    <div class="nav-grid">
      <router-link to="/admin/subjects" class="nav-card">
        <div class="nav-card-icon" style="background: var(--qm-primary-light); color: var(--qm-primary);">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        </div>
        <div>
          <div class="nav-card-title">Subjects</div>
          <div class="nav-card-desc">Create and organise learning subjects</div>
        </div>
        <svg class="nav-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
      </router-link>

      <router-link to="/admin/chapters" class="nav-card">
        <div class="nav-card-icon" style="background: #F3E8FF; color: var(--qm-secondary);">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <div>
          <div class="nav-card-title">Chapters</div>
          <div class="nav-card-desc">Group content into subject chapters</div>
        </div>
        <svg class="nav-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
      </router-link>

      <router-link to="/admin/quizzes" class="nav-card">
        <div class="nav-card-icon" style="background: var(--qm-success-light); color: var(--qm-success);">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        </div>
        <div>
          <div class="nav-card-title">Quizzes</div>
          <div class="nav-card-desc">Build quizzes and add questions</div>
        </div>
        <svg class="nav-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
      </router-link>
    </div>

    <!-- Recent attempts -->
    <div class="section-title">Recent Quiz Attempts</div>
    <div class="table-wrap">
      <div v-if="!stats.recent_scores || stats.recent_scores.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <p>No quiz attempts yet</p>
      </div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score in stats.recent_scores" :key="score.id">
            <td class="cell-user">{{ score.user_name }}</td>
            <td>{{ score.quiz_title }}</td>
            <td>
              <span class="score-badge" :class="getScoreClass(score.score, score.total_marks)">
                {{ score.score }}/{{ score.total_marks }}
              </span>
            </td>
            <td class="cell-date">{{ formatDate(score.timestamp_of_attempt) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        total_users: 0,
        total_subjects: 0,
        total_quizzes: 0,
        total_attempts: 0,
        recent_scores: []
      }
    }
  },
  async mounted() {
    await this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        const res = await axios.get('/admin/dashboard/stats')
        this.stats = res.data
      } catch (err) {
        console.error('Failed to fetch admin stats:', err)
      }
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    },
    getScoreClass(score, total) {
      if (!total) return 'badge-gray'
      const pct = (score / total) * 100
      if (pct >= 70) return 'badge-green'
      if (pct >= 40) return 'badge-amber'
      return 'badge-red'
    }
  }
}
</script>

<style scoped>
.admin-dash {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── Stat Cards ───────────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: var(--qm-shadow);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--qm-shadow-md);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg { width: 22px; height: 22px; }

.icon-blue   { background: var(--qm-primary-light); color: var(--qm-primary); }
.icon-purple { background: #F3E8FF; color: var(--qm-secondary); }
.icon-green  { background: var(--qm-success-light); color: var(--qm-success); }
.icon-amber  { background: var(--qm-warning-light); color: var(--qm-warning); }

.stat-value {
  font-family: var(--qm-font-heading);
  font-size: 1.875rem;
  font-weight: 800;
  color: var(--qm-text);
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: var(--qm-text-muted);
  font-weight: 500;
}

/* ── Section title ────────────────────────────────────────── */
.section-title {
  font-family: var(--qm-font-heading);
  font-size: 15px;
  font-weight: 700;
  color: var(--qm-text);
  padding-bottom: 4px;
  border-bottom: 2px solid var(--qm-border-light);
}

/* ── Nav grid ─────────────────────────────────────────────── */
.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}

.nav-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: var(--qm-shadow);
}

.nav-card:hover {
  border-color: var(--qm-primary);
  transform: translateY(-2px);
  box-shadow: var(--qm-shadow-md);
}

.nav-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-card-icon svg { width: 20px; height: 20px; }

.nav-card-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--qm-text);
  margin-bottom: 3px;
}

.nav-card-desc {
  font-size: 12px;
  color: var(--qm-text-muted);
}

.nav-arrow {
  width: 16px;
  height: 16px;
  color: var(--qm-text-light);
  margin-left: auto;
  flex-shrink: 0;
}

/* ── Table ────────────────────────────────────────────────── */
.table-wrap {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead th {
  padding: 11px 16px;
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
  padding: 13px 16px;
  border-bottom: 1px solid var(--qm-border-light);
  font-size: 14px;
  vertical-align: middle;
}

.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover { background: var(--qm-bg); }

.cell-user { font-weight: 500; color: var(--qm-text); }
.cell-date { color: var(--qm-text-muted); font-size: 13px; white-space: nowrap; }

.score-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge-green { background: var(--qm-success-light); color: var(--qm-success); }
.badge-amber { background: var(--qm-warning-light); color: #92400E; }
.badge-red   { background: var(--qm-danger-light);  color: var(--qm-danger); }
.badge-gray  { background: var(--qm-bg); color: var(--qm-text-muted); }

.empty-state {
  padding: 48px 24px;
  text-align: center;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.empty-state p {
  color: var(--qm-text-muted);
  font-size: 14px;
  margin: 0;
}
</style>
