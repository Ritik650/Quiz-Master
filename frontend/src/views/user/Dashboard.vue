<template>
  <div class="container mt-4">
    <!-- Welcome Section -->
    <div class="row">
      <div class="col-12">
        <h2>Welcome, {{ user?.full_name }}!</h2>
        <p class="text-muted">Your Quiz Dashboard</p>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3" v-for="(stat, index) in statsCards" :key="index">
        <div :class="`card text-white ${stat.bg}`">
          <div class="card-body">
            <h5>{{ stat.label }}</h5>
            <h2>{{ stat.value }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Chart Image -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5>Matplotlib Summary Chart</h5>
          </div>
          <div class="text-center mt-4 ">
            <<img :src="matplotlibChartUrl" alt="Matplotlib Summary Chart" class="img-fluid rounded shadow-sm" style="max-height: 400px;" />
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Attempts -->
    <div class="row">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5>Recent Quiz Attempts</h5>
          </div>
          <div class="card-body">
            <div v-if="dashboardData.recent_attempts.length === 0" class="text-center text-muted">
              No quiz attempts yet. <router-link to="/quizzes">Start your first quiz!</router-link>
            </div>
            <div v-else>
              <table class="table">
                <thead>
                  <tr>
                    <th>Quiz</th>
                    <th>Score</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="attempt in dashboardData.recent_attempts" :key="attempt.id">
                    <td>{{ attempt.quiz_title }}</td>
                    <td>
                      <span class="badge" :class="getScoreBadgeClass(attempt.percentage)">
                        {{ attempt.total_scored }}/{{ attempt.total_marks }} ({{ attempt.percentage }}%)
                      </span>
                    </td>
                    <td>{{ formatDate(attempt.timestamp_of_attempt) }}</td>
                    <td>
                      <router-link :to="`/quiz/results/${attempt.id}`" class="btn btn-sm btn-outline-primary">
                        View Results
                      </router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions + Profile -->
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5>Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <router-link to="/quizzes" class="btn btn-primary">
                Browse Quizzes
              </router-link>
              <button @click="exportData" class="btn btn-outline-secondary">
                Export My Data
              </button>
              <button @click="showProfile = !showProfile" class="btn btn-outline-info">
                {{ showProfile ? 'Hide' : 'Show' }} Profile
              </button>
            </div>
          </div>
        </div>

        <!-- Profile Info -->
        <div v-if="showProfile" class="card mt-3">
          <div class="card-header">
            <h5>Profile Information</h5>
          </div>
          <div class="card-body">
            <p><strong>Email:</strong> {{ user.username }}</p>
            <p><strong>Full Name:</strong> {{ user.full_name }}</p>
            <p><strong>Qualification:</strong> {{ user.qualification || 'Not specified' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Leaderboard Chart -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5>Top Scoring Quizzes</h5>
          </div>
          <div class="card-body" style="min-height: 400px">
            <BarChart v-if="summaryData.length" :chart-data="chartData" :chart-options="chartOptions" />
            <p v-else class="text-muted text-center">Loading leaderboard chart or no data available.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'UserDashboard',
  components: {
    BarChart: {
      extends: Bar,
      props: ['chartData', 'chartOptions'],
      mounted() {
        this.renderChart(this.chartData, this.chartOptions)
      },
      watch: {
        chartData(newData) {
          this.renderChart(newData, this.chartOptions)
        }
      }
    }
  },
  data() {
    return {
      dashboardData: {
        total_attempts: 0,
        average_score: 0,
        recent_attempts: [],
        available_quizzes: 0
      },
      showProfile: false,
      chartImageUrl: '',
      summaryData: []
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    monthlyAttempts() {
      const currentMonth = new Date().getMonth()
      return this.dashboardData.recent_attempts.filter(attempt => {
        const attemptDate = new Date(attempt.timestamp_of_attempt)
        return attemptDate.getMonth() === currentMonth
      }).length
    },
    statsCards() {
      return [
        { label: 'Total Attempts', value: this.dashboardData.total_attempts, bg: 'bg-primary' },
        { label: 'Average Score', value: this.dashboardData.average_score + '%', bg: 'bg-success' },
        { label: 'Available Quizzes', value: this.dashboardData.available_quizzes, bg: 'bg-info' },
        { label: 'This Month', value: this.monthlyAttempts, bg: 'bg-warning' }
      ]
    },
    chartData() {
      return {
        labels: this.summaryData.map(item => item.quiz_title),
        datasets: [{
          label: 'Average Score (%)',
          backgroundColor: '#007bff',
          data: this.summaryData.map(item => item.average_score)
        }]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    }
  },
  async mounted() {
    await this.fetchDashboardData()
    await this.fetchSummaryData()
    this.chartImageUrl = '/api/quiz-summary-chart' + new Date().getTime()
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get('/user/dashboard')
        this.dashboardData = response.data
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      }
    },
    async fetchSummaryData() {
      try {
        const response = await axios.get('/api/quiz-summary')
        this.summaryData = response.data
      } catch (error) {
        console.error('Failed to fetch quiz summary:', error)
      }
    },
    getScoreBadgeClass(percentage) {
      if (percentage >= 80) return 'bg-success'
      if (percentage >= 60) return 'bg-warning'
      return 'bg-danger'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    async exportData() {
      try {
        await axios.post('/user/export-data')
        alert('Export job started! You will receive an email when ready.')
      } catch (error) {
        console.error('Export failed:', error)
        alert('Export failed. Please try again.')
      }
    }
  }
}
</script>

<style scoped>
.card-body img {
  max-height: 400px;
}
</style>
