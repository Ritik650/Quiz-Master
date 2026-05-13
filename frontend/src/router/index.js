import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import UserLayout from '../layouts/UserLayout.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import SubjectManagement from '../views/admin/SubjectManagement.vue'
import ChapterManagement from '../views/admin/ChapterManagement.vue'
import QuizManagement from '../views/admin/QuizManagement.vue'
import Analytics from '../views/admin/Analytics.vue'
import UserDashboard from '../views/user/Dashboard.vue'
import QuizList from '../views/user/QuizList.vue'
import TakeQuiz from '../views/user/TakeQuiz.vue'
import QuizResults from '../views/user/QuizResults.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login',    name: 'Login',    component: Login },
  { path: '/register', name: 'Register', component: Register },

  // Admin section — sidebar layout
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '',         name: 'AdminDashboard',    component: AdminDashboard },
      { path: 'subjects',  name: 'SubjectManagement', component: SubjectManagement },
      { path: 'chapters',  name: 'ChapterManagement', component: ChapterManagement },
      { path: 'quizzes',   name: 'QuizManagement',    component: QuizManagement },
      { path: 'analytics', name: 'AdminAnalytics',    component: Analytics },
    ]
  },

  // User section — top-navbar layout
  {
    path: '/',
    component: UserLayout,
    meta: { requiresAuth: true, role: 'user' },
    children: [
      { path: 'dashboard',              name: 'UserDashboard', component: UserDashboard },
      { path: 'quizzes',                name: 'QuizList',      component: QuizList },
      { path: 'quiz/:quizId/take',      name: 'TakeQuiz',      component: TakeQuiz },
      { path: 'quiz/results/:scoreId',  name: 'QuizResults',   component: QuizResults },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  const userRole        = store.getters.userRole

  // Check auth/role requirements from all matched route records
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth)
  const requiredRole = to.matched.find(r => r.meta.role)?.meta.role

  if (requiresAuth && !isAuthenticated) {
    return next('/login')
  }

  if (requiredRole && isAuthenticated && requiredRole !== userRole) {
    return next(userRole === 'admin' ? '/admin' : '/dashboard')
  }

  return next()
})

export default router
