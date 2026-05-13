<template>
  <div class="user-layout">
    <!-- Top Navbar -->
    <header class="user-navbar">
      <div class="navbar-brand">
        <div class="logo-icon">Q</div>
        <span class="logo-text">Quiz Master</span>
      </div>

      <nav class="navbar-links">
        <router-link to="/dashboard" class="nav-link" active-class="nav-link--active">
          <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
          </svg>
          Dashboard
        </router-link>
        <router-link to="/quizzes" class="nav-link" active-class="nav-link--active">
          <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 11l3 3L22 4"/>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
          Quizzes
        </router-link>
      </nav>

      <div class="navbar-right">
        <div class="user-chip">
          <div class="user-avatar">{{ userInitial }}</div>
          <span class="user-name">{{ userName }}</span>
        </div>
        <button @click="logout" class="btn-logout">Logout</button>
      </div>
    </header>

    <!-- Page Content -->
    <main class="user-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'UserLayout',
  computed: {
    user()        { return this.$store.state.user },
    userName()    { return this.user?.full_name || 'User' },
    userInitial() { return (this.user?.full_name || 'U').charAt(0).toUpperCase() }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  background: var(--qm-bg);
  display: flex;
  flex-direction: column;
}

/* ── Navbar ───────────────────────────────────────────────── */
.user-navbar {
  height: var(--qm-navbar-h);
  background: var(--qm-surface);
  border-bottom: 1px solid var(--qm-border);
  display: flex;
  align-items: center;
  padding: 0 28px;
  gap: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--qm-shadow-sm);
  flex-shrink: 0;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.logo-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  font-family: var(--qm-font-heading);
  font-weight: 800;
  font-size: 17px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.logo-text {
  font-family: var(--qm-font-heading);
  font-weight: 700;
  font-size: 16px;
  color: var(--qm-text);
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 2px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: var(--qm-radius);
  color: var(--qm-text-muted);
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-link:hover {
  background: var(--qm-bg);
  color: var(--qm-text);
}

.nav-link--active {
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-weight: 600;
}

.link-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--qm-text);
}

.btn-logout {
  padding: 7px 14px;
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius);
  background: var(--qm-surface);
  color: var(--qm-text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-logout:hover {
  border-color: var(--qm-danger);
  color: var(--qm-danger);
  background: var(--qm-danger-light);
}

/* ── Content ──────────────────────────────────────────────── */
.user-content {
  flex: 1;
  padding: 28px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .user-navbar  { padding: 0 16px; gap: 12px; }
  .user-name    { display: none; }
  .user-content { padding: 16px; }
}
</style>
