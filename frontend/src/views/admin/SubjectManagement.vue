<template>
  <div class="subject-mgmt">
    <!-- Page header -->
    <div class="page-header">
      <div>
        <p class="page-sub">Add and manage learning subjects</p>
      </div>
      <button @click="openCreate" class="btn-add">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add Subject
      </button>
    </div>

    <!-- Search + stats row -->
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Search subjects…"
          class="search-input"
        />
      </div>
      <div class="stats-row">
        <div class="stat-pill">
          <span class="stat-num">{{ subjects.length }}</span>
          <span class="stat-lbl">Total</span>
        </div>
        <div class="stat-pill">
          <span class="stat-num">{{ filteredSubjects.length }}</span>
          <span class="stat-lbl">Shown</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <div class="table-head-bar">
        <span class="table-title">Subjects</span>
        <button @click="fetchSubjects" class="btn-refresh" title="Refresh">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
          Refresh
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading subjects…</p>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Created</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subject in filteredSubjects" :key="subject.id">
            <td class="cell-name">{{ subject.name }}</td>
            <td class="cell-desc">{{ truncate(subject.description, 60) }}</td>
            <td class="cell-date">{{ formatDate(subject.created_at) }}</td>
            <td class="cell-actions">
              <button @click="openEdit(subject)" class="btn-edit" title="Edit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button @click="deleteSubject(subject.id)" class="btn-delete" title="Delete">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
              </button>
            </td>
          </tr>
          <tr v-if="filteredSubjects.length === 0">
            <td colspan="4" class="empty-state">
              <div class="empty-content">
                <div class="empty-icon">📚</div>
                <p>{{ searchTerm ? 'No subjects match your search' : 'No subjects yet — add one to get started' }}</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box" role="dialog" aria-modal="true">
        <div class="modal-hdr">
          <div>
            <h3 class="modal-title">{{ isEditing ? 'Edit Subject' : 'New Subject' }}</h3>
            <p class="modal-sub">{{ isEditing ? 'Update the subject details below' : 'Fill in the details for the new subject' }}</p>
          </div>
          <button @click="closeModal" class="btn-close" aria-label="Close">&times;</button>
        </div>

        <form @submit.prevent="saveSubject" class="modal-form">
          <div class="mform-group">
            <label>Subject Name <span class="req">*</span></label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="e.g. Mathematics"
              ref="nameInput"
            />
          </div>
          <div class="mform-group">
            <label>Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="Brief description of this subject…"
            ></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
            <button type="submit" class="btn-save" :disabled="saving">
              <span v-if="saving" class="spinner-sm"></span>
              {{ saving ? 'Saving…' : (isEditing ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubjectManagement',
  data() {
    return {
      subjects: [],
      searchTerm: '',
      loading: false,
      saving: false,
      showModal: false,
      isEditing: false,
      form: { id: null, name: '', description: '' }
    }
  },
  computed: {
    filteredSubjects() {
      const q = this.searchTerm.toLowerCase()
      return this.subjects.filter(s =>
        s.name.toLowerCase().includes(q) ||
        (s.description || '').toLowerCase().includes(q)
      )
    }
  },
  async mounted() {
    await this.fetchSubjects()
  },
  methods: {
    async fetchSubjects() {
      this.loading = true
      try {
        const res = await axios.get('/admin/subjects')
        this.subjects = res.data
      } catch (err) {
        console.error('Failed to fetch subjects:', err)
      } finally {
        this.loading = false
      }
    },
    openCreate() {
      this.form = { id: null, name: '', description: '' }
      this.isEditing = false
      this.showModal = true
      this.$nextTick(() => this.$refs.nameInput?.focus())
    },
    openEdit(subject) {
      this.form = { ...subject }
      this.isEditing = true
      this.showModal = true
      this.$nextTick(() => this.$refs.nameInput?.focus())
    },
    async saveSubject() {
      this.saving = true
      try {
        if (this.isEditing) {
          await axios.put(`/admin/subjects/${this.form.id}`, this.form)
        } else {
          await axios.post('/admin/subjects', this.form)
        }
        await this.fetchSubjects()
        this.closeModal()
      } catch (err) {
        console.error('Failed to save subject:', err)
      } finally {
        this.saving = false
      }
    },
    async deleteSubject(id) {
      if (!confirm('Delete this subject? This action cannot be undone.')) return
      this.loading = true
      try {
        await axios.delete(`/admin/subjects/${id}`)
        await this.fetchSubjects()
      } catch (err) {
        console.error('Failed to delete subject:', err)
      } finally {
        this.loading = false
      }
    },
    closeModal() {
      this.showModal = false
      this.form = { id: null, name: '', description: '' }
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    },
    truncate(text, max) {
      if (!text) return '—'
      return text.length > max ? text.slice(0, max) + '…' : text
    }
  }
}
</script>

<style scoped>
.subject-mgmt {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── Page header ──────────────────────────────────────────── */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.page-sub {
  color: var(--qm-text-muted);
  font-size: 14px;
  margin: 0;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  background: var(--qm-primary);
  color: white;
  border: none;
  border-radius: var(--qm-radius);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-add svg { width: 16px; height: 16px; }

.btn-add:hover {
  background: var(--qm-primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--qm-shadow-md);
}

/* ── Toolbar ──────────────────────────────────────────────── */
.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.search-wrap {
  position: relative;
  flex: 1;
  min-width: 200px;
  max-width: 360px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--qm-text-light);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 9px 12px 9px 36px;
  border: 1.5px solid var(--qm-border);
  border-radius: var(--qm-radius);
  font-size: 14px;
  color: var(--qm-text);
  font-family: var(--qm-font-body);
  background: var(--qm-surface);
  transition: border-color 0.15s, box-shadow 0.15s;
  outline: none;
}

.search-input:focus {
  border-color: var(--qm-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.stats-row {
  display: flex;
  gap: 10px;
}

.stat-pill {
  display: flex;
  align-items: baseline;
  gap: 4px;
  padding: 6px 14px;
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: 20px;
}

.stat-num {
  font-weight: 700;
  font-size: 15px;
  color: var(--qm-primary);
  font-family: var(--qm-font-heading);
}

.stat-lbl {
  font-size: 12px;
  color: var(--qm-text-muted);
}

/* ── Table ────────────────────────────────────────────────── */
.table-wrap {
  background: var(--qm-surface);
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius-lg);
  overflow: hidden;
  box-shadow: var(--qm-shadow);
}

.table-head-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--qm-border-light);
  background: var(--qm-bg);
}

.table-title {
  font-family: var(--qm-font-heading);
  font-weight: 600;
  font-size: 14px;
  color: var(--qm-text);
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: none;
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius);
  font-size: 13px;
  color: var(--qm-text-muted);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-refresh svg { width: 14px; height: 14px; }
.btn-refresh:hover { border-color: var(--qm-primary); color: var(--qm-primary); }

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

.data-table tbody tr {
  transition: background 0.1s;
}

.data-table tbody tr:hover {
  background: var(--qm-bg);
}

.data-table td {
  padding: 13px 16px;
  border-bottom: 1px solid var(--qm-border-light);
  font-size: 14px;
  vertical-align: middle;
}

.data-table tbody tr:last-child td { border-bottom: none; }

.cell-name {
  font-weight: 600;
  color: var(--qm-text);
}

.cell-desc {
  color: var(--qm-text-muted);
}

.cell-date {
  color: var(--qm-text-muted);
  font-size: 13px;
  white-space: nowrap;
}

.col-actions, .cell-actions { width: 100px; }

.cell-actions {
  display: flex;
  gap: 6px;
}

.btn-edit,
.btn-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: var(--qm-radius-sm);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-edit svg,
.btn-delete svg { width: 15px; height: 15px; }

.btn-edit {
  background: var(--qm-warning-light);
  color: var(--qm-warning);
}
.btn-edit:hover { background: #FDE68A; }

.btn-delete {
  background: var(--qm-danger-light);
  color: var(--qm-danger);
}
.btn-delete:hover { background: #FECACA; }

/* ── Loading / Empty ──────────────────────────────────────── */
.loading-state {
  padding: 56px 24px;
  text-align: center;
  color: var(--qm-text-muted);
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--qm-border);
  border-top-color: var(--qm-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  padding: 48px 24px;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.empty-icon {
  font-size: 2.5rem;
  line-height: 1;
}

.empty-content p {
  color: var(--qm-text-muted);
  font-size: 14px;
  margin: 0;
}

/* ── Modal ────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 24px;
  backdrop-filter: blur(3px);
}

.modal-box {
  background: var(--qm-surface);
  border-radius: var(--qm-radius-lg);
  width: 100%;
  max-width: 480px;
  box-shadow: var(--qm-shadow-xl);
  animation: modalIn 0.2s ease;
}

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.96) translateY(-8px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-hdr {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 24px 20px;
  border-bottom: 1px solid var(--qm-border-light);
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--qm-text);
}

.modal-sub {
  font-size: 13px;
  color: var(--qm-text-muted);
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
  color: var(--qm-text-muted);
  padding: 4px;
  border-radius: var(--qm-radius-sm);
  transition: all 0.15s;
  margin-left: 12px;
  flex-shrink: 0;
}
.btn-close:hover { background: var(--qm-bg); color: var(--qm-text); }

.modal-form {
  padding: 20px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mform-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.mform-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--qm-text);
}

.req { color: var(--qm-danger); margin-left: 2px; }

.mform-group input,
.mform-group textarea {
  padding: 10px 13px;
  border: 1.5px solid var(--qm-border);
  border-radius: var(--qm-radius);
  font-size: 14px;
  color: var(--qm-text);
  font-family: var(--qm-font-body);
  background: var(--qm-surface);
  transition: border-color 0.15s, box-shadow 0.15s;
  outline: none;
  resize: vertical;
}

.mform-group input:focus,
.mform-group textarea:focus {
  border-color: var(--qm-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--qm-border-light);
}

.btn-cancel {
  padding: 9px 18px;
  background: none;
  border: 1px solid var(--qm-border);
  border-radius: var(--qm-radius);
  font-size: 14px;
  font-weight: 500;
  color: var(--qm-text-muted);
  cursor: pointer;
  transition: all 0.15s;
}
.btn-cancel:hover { border-color: var(--qm-text-muted); color: var(--qm-text); }

.btn-save {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 20px;
  background: var(--qm-primary);
  color: white;
  border: none;
  border-radius: var(--qm-radius);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--qm-font-body);
  min-width: 90px;
  justify-content: center;
}
.btn-save:hover:not(:disabled) { background: var(--qm-primary-dark); }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner-sm {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}
</style>
