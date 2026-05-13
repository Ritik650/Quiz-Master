<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">Q</div>
        <span class="logo-text">Quiz Master</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-item" :class="{ 'nav-item--active': $route.name === 'AdminDashboard' }">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
          </svg>
          Dashboard
        </router-link>

        <router-link to="/admin/subjects" class="nav-item" active-class="nav-item--active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          Subjects
        </router-link>

        <router-link to="/admin/chapters" class="nav-item" active-class="nav-item--active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          Chapters
        </router-link>

        <router-link to="/admin/quizzes" class="nav-item" active-class="nav-item--active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 11l3 3L22 4"/>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
          Quizzes
        </router-link>

        <router-link to="/admin/analytics" class="nav-item" active-class="nav-item--active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6"  y1="20" x2="6"  y2="14"/>
          </svg>
          Analytics
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="logout-btn">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- Main area -->
    <div class="admin-main">
      <!-- Top bar -->
      <header class="topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
          <nav class="breadcrumb-nav" v-if="showBreadcrumb">
            <router-link to="/admin" class="bc-link">Home</router-link>
            <span class="bc-sep">/</span>
            <span class="bc-current">{{ currentPageTitle }}</span>
          </nav>
        </div>
        <div class="topbar-right">
          <div class="admin-badge">Admin</div>
          <div class="avatar-wrap">
            <div class="admin-avatar">A</div>
            <div class="avatar-info">
              <span class="avatar-name">Administrator</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Content -->
      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  computed: {
    currentPageTitle() {
      const titles = {
        AdminDashboard:    'Dashboard',
        SubjectManagement: 'Subjects',
        ChapterManagement: 'Chapters',
        QuizManagement:    'Quizzes',
        AdminAnalytics:    'Analytics',
      }
      return titles[this.$route.name] || 'Admin'
    },
    showBreadcrumb() {
      return this.$route.name !== 'AdminDashboard'
    }
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
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--qm-bg);
}

/* ── Sidebar ──────────────────────────────────────────────── */
.sidebar {
  width: var(--qm-sidebar-w);
  min-height: 100vh;
  background: var(--qm-surface);
  border-right: 1px solid var(--qm-border);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
  box-shadow: var(--qm-shadow);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
  height: var(--qm-navbar-h);
  border-bottom: 1px solid var(--qm-border-light);
  flex-shrink: 0;
}

.logo-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  font-family: var(--qm-font-heading);
  font-weight: 800;
  font-size: 18px;
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

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--qm-radius);
  color: var(--qm-text-muted);
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-item:hover {
  background: var(--qm-bg);
  color: var(--qm-text);
}

.nav-item--active {
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-weight: 600;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid var(--qm-border-light);
  flex-shrink: 0;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  width: 100%;
  border-radius: var(--qm-radius);
  border: none;
  background: none;
  color: var(--qm-danger);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.logout-btn:hover {
  background: var(--qm-danger-light);
}

/* ── Main ─────────────────────────────────────────────────── */
.admin-main {
  flex: 1;
  margin-left: var(--qm-sidebar-w);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  height: var(--qm-navbar-h);
  background: var(--qm-surface);
  border-bottom: 1px solid var(--qm-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 50;
  flex-shrink: 0;
}

.topbar-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.page-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: var(--qm-text);
  line-height: 1.2;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  margin-top: 2px;
}

.bc-link {
  color: var(--qm-text-muted);
  text-decoration: none;
}
.bc-link:hover { color: var(--qm-primary); }
.bc-sep { color: var(--qm-text-light); }
.bc-current { color: var(--qm-text-muted); }

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-badge {
  padding: 3px 10px;
  border-radius: 20px;
  background: var(--qm-primary-light);
  color: var(--qm-primary);
  font-size: 11px;
  font-weight: 600;
}

.avatar-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.admin-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--qm-primary), var(--qm-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.avatar-info {
  display: flex;
  flex-direction: column;
}

.avatar-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--qm-text);
  line-height: 1;
}

.admin-content {
  flex: 1;
  padding: 28px;
  background: var(--qm-bg);
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .sidebar     { display: none; }
  .admin-main  { margin-left: 0; }
  .topbar      { padding: 0 16px; }
  .admin-content { padding: 16px; }
}
</style>
