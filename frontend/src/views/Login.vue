<template>
  <div class="auth-page">
    <!-- Left decorative panel -->
    <div class="auth-left">
      <div class="auth-brand">
        <div class="logo-icon">Q</div>
        <span class="logo-text">Quiz Master</span>
      </div>
      <div class="auth-hero">
        <h1>Test your knowledge, track your progress</h1>
        <p>A modern quiz platform for learners and educators alike.</p>
        <ul class="feature-list">
          <li>
            <span class="feature-dot"></span>
            Quizzes across multiple subjects and chapters
          </li>
          <li>
            <span class="feature-dot"></span>
            Instant results with detailed feedback
          </li>
          <li>
            <span class="feature-dot"></span>
            Admin dashboard for content management
          </li>
        </ul>
      </div>
    </div>

    <!-- Right form panel -->
    <div class="auth-right">
      <div class="auth-card">
        <h2>Welcome back</h2>
        <p class="auth-sub">Sign in to continue to Quiz Master</p>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="username">Username or Email</label>
            <input
              id="username"
              type="text"
              v-model="credentials.username"
              placeholder="you@example.com"
              required
              autocomplete="username"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              type="password"
              v-model="credentials.password"
              placeholder="••••••••"
              required
              autocomplete="current-password"
            />
          </div>

          <div v-if="error" class="auth-error" role="alert">
            {{ error }}
          </div>

          <button type="submit" class="auth-btn" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Signing in…' : 'Sign in' }}
          </button>
        </form>

        <p class="auth-footer">
          Don't have an account?
          <router-link to="/register">Create one</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      credentials: { username: '', password: '' },
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error   = null
      const result = await this.$store.dispatch('login', this.credentials)
      if (result.success) {
        this.$router.push(result.user.role === 'admin' ? '/admin' : '/dashboard')
      } else {
        this.error = result.message
      }
      this.loading = false
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
}

/* ── Left panel ───────────────────────────────────────────── */
.auth-left {
  flex: 1;
  background: linear-gradient(145deg, var(--qm-primary) 0%, var(--qm-secondary) 100%);
  padding: 40px 48px;
  display: flex;
  flex-direction: column;
  color: white;
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: auto;
}

.logo-icon {
  width: 40px;
  height: 40px;
  border-radius: 11px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-family: var(--qm-font-heading);
  font-weight: 800;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-family: var(--qm-font-heading);
  font-weight: 700;
  font-size: 18px;
  color: white;
}

.auth-hero {
  margin-bottom: 64px;
}

.auth-hero h1 {
  font-family: var(--qm-font-heading);
  font-size: 2.25rem;
  font-weight: 800;
  color: white;
  line-height: 1.2;
  margin-bottom: 16px;
}

.auth-hero p {
  font-size: 1.0625rem;
  opacity: 0.85;
  margin-bottom: 32px;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0.9;
  font-size: 0.9375rem;
}

.feature-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  flex-shrink: 0;
}

/* ── Right panel ──────────────────────────────────────────── */
.auth-right {
  width: 480px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
  background: var(--qm-surface);
}

.auth-card {
  width: 100%;
  max-width: 360px;
}

.auth-card h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--qm-text);
}

.auth-sub {
  color: var(--qm-text-muted);
  margin-bottom: 32px;
  font-size: 0.9375rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--qm-text);
}

.form-group input {
  padding: 10px 14px;
  border: 1.5px solid var(--qm-border);
  border-radius: var(--qm-radius);
  font-size: 14px;
  color: var(--qm-text);
  font-family: var(--qm-font-body);
  background: var(--qm-surface);
  transition: border-color 0.15s, box-shadow 0.15s;
  outline: none;
}

.form-group input:focus {
  border-color: var(--qm-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.form-group input::placeholder {
  color: var(--qm-text-light);
}

.auth-error {
  padding: 10px 14px;
  border-radius: var(--qm-radius);
  background: var(--qm-danger-light);
  color: var(--qm-danger);
  font-size: 13px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.auth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 11px;
  width: 100%;
  background: var(--qm-primary);
  color: white;
  border: none;
  border-radius: var(--qm-radius);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--qm-font-body);
  margin-top: 4px;
}

.auth-btn:hover:not(:disabled) {
  background: var(--qm-primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--qm-shadow-md);
}

.auth-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--qm-text-muted);
}

.auth-footer a {
  color: var(--qm-primary);
  font-weight: 500;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 900px) {
  .auth-hero h1 { font-size: 1.75rem; }
}

@media (max-width: 768px) {
  .auth-page   { flex-direction: column; }
  .auth-left   { padding: 28px 24px; }
  .auth-hero   { margin-bottom: 8px; }
  .auth-hero h1 { font-size: 1.5rem; }
  .feature-list { display: none; }
  .auth-right  { width: 100%; padding: 32px 20px; }
  .auth-card   { max-width: 100%; }
}
</style>
