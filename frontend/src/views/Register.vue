<template>
  <div class="auth-page">
    <!-- Left decorative panel -->
    <div class="auth-left">
      <div class="auth-brand">
        <div class="logo-icon">Q</div>
        <span class="logo-text">Quiz Master</span>
      </div>
      <div class="auth-hero">
        <h1>Join thousands of learners today</h1>
        <p>Create your free account and start taking quizzes across dozens of subjects.</p>
        <ul class="feature-list">
          <li><span class="feature-dot"></span>Free to sign up, no credit card required</li>
          <li><span class="feature-dot"></span>Access hundreds of quizzes immediately</li>
          <li><span class="feature-dot"></span>Track your scores and improvement over time</li>
        </ul>
      </div>
    </div>

    <!-- Right form panel -->
    <div class="auth-right">
      <div class="auth-card">
        <h2>Create an account</h2>
        <p class="auth-sub">Fill in your details to get started</p>

        <form @submit.prevent="handleRegister" class="auth-form">
          <div class="form-row">
            <div class="form-group">
              <label for="email">Email Address</label>
              <input
                id="email"
                type="email"
                v-model="formData.username"
                placeholder="you@example.com"
                required
                autocomplete="email"
              />
            </div>
            <div class="form-group">
              <label for="fullName">Full Name</label>
              <input
                id="fullName"
                type="text"
                v-model="formData.full_name"
                placeholder="Your full name"
                required
                autocomplete="name"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="qualification">Qualification <span class="optional">(optional)</span></label>
              <input
                id="qualification"
                type="text"
                v-model="formData.qualification"
                placeholder="e.g. B.Tech, M.Sc"
              />
            </div>
            <div class="form-group">
              <label for="dob">Date of Birth <span class="optional">(optional)</span></label>
              <input
                id="dob"
                type="date"
                v-model="formData.dob"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="password">Password</label>
              <input
                id="password"
                type="password"
                v-model="formData.password"
                placeholder="Min. 6 characters"
                required
                minlength="6"
                autocomplete="new-password"
              />
            </div>
            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                v-model="confirmPassword"
                placeholder="Repeat password"
                required
                autocomplete="new-password"
              />
            </div>
          </div>

          <div v-if="error"   class="auth-error"   role="alert">{{ error }}</div>
          <div v-if="success" class="auth-success"  role="status">{{ success }}</div>

          <button type="submit" class="auth-btn" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Creating account…' : 'Create account' }}
          </button>
        </form>

        <p class="auth-footer">
          Already have an account?
          <router-link to="/login">Sign in</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      formData: {
        username: '',
        full_name: '',
        qualification: '',
        dob: '',
        password: ''
      },
      confirmPassword: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async handleRegister() {
      this.error   = null
      this.success = null

      if (this.formData.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }

      this.loading = true
      const result = await this.$store.dispatch('register', this.formData)

      if (result.success) {
        this.success = 'Account created! Redirecting to login…'
        setTimeout(() => this.$router.push('/login'), 1800)
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
}

.auth-hero {
  margin-bottom: 64px;
}

.auth-hero h1 {
  font-family: var(--qm-font-heading);
  font-size: 2rem;
  font-weight: 800;
  color: white;
  line-height: 1.2;
  margin-bottom: 14px;
}

.auth-hero p {
  font-size: 1rem;
  opacity: 0.85;
  margin-bottom: 28px;
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
  width: 560px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
  background: var(--qm-surface);
  overflow-y: auto;
}

.auth-card {
  width: 100%;
  max-width: 460px;
}

.auth-card h2 {
  font-size: 1.625rem;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--qm-text);
}

.auth-sub {
  color: var(--qm-text-muted);
  margin-bottom: 28px;
  font-size: 0.9375rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--qm-text);
}

.optional {
  font-weight: 400;
  color: var(--qm-text-muted);
}

.form-group input {
  padding: 9px 13px;
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

.auth-error,
.auth-success {
  padding: 10px 14px;
  border-radius: var(--qm-radius);
  font-size: 13px;
}

.auth-error {
  background: var(--qm-danger-light);
  color: var(--qm-danger);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.auth-success {
  background: var(--qm-success-light);
  color: var(--qm-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
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
  margin-top: 22px;
  font-size: 14px;
  color: var(--qm-text-muted);
}

.auth-footer a {
  color: var(--qm-primary);
  font-weight: 500;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 900px) {
  .auth-right { width: 480px; }
}

@media (max-width: 768px) {
  .auth-page       { flex-direction: column; }
  .auth-left       { padding: 28px 24px; }
  .auth-hero       { margin-bottom: 8px; }
  .auth-hero h1    { font-size: 1.5rem; }
  .feature-list    { display: none; }
  .auth-right      { width: 100%; padding: 28px 20px; }
  .form-row        { grid-template-columns: 1fr; }
}
</style>
