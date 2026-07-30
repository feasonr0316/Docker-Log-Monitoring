<script setup>
defineProps({
  errors: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

function statusClass(status) {
  const code = String(status || '').trim()

  if (code.startsWith('5')) return 'status-server-error'
  if (code.startsWith('4')) return 'status-client-error'
  if (code.startsWith('2') || code.startsWith('3')) return 'status-normal'

  return 'status-muted'
}

function levelClass(level) {
  const value = String(level || '').toUpperCase()

  if (['HIGH', 'ERROR', 'CRITICAL', 'FATAL'].includes(value)) {
    return 'level-high'
  }

  if (['MEDIUM', 'WARNING', 'WARN'].includes(value)) {
    return 'level-medium'
  }

  return 'level-low'
}
</script>

<template>
  <section class="panel">
    <div class="panel-header">
      <div>
        <h2>错误分析</h2>
        <p>独立展示后端返回的异常日志</p>
      </div>

      <span class="count-badge danger-badge">
        {{ errors.length }} 条
      </span>
    </div>

    <div class="table-wrapper">
      <table class="data-table error-table">
        <thead>
          <tr>
            <th>级别</th>
            <th>容器</th>
            <th>状态</th>
            <th>路径</th>
            <th>错误原因</th>
          </tr>
        </thead>

        <tbody v-if="!loading && errors.length">
          <tr v-for="item in errors" :key="item.error_id || item.id">
            <td>
              <span :class="['level-tag', levelClass(item.level)]">
                {{ item.level || 'ERROR' }}
              </span>
            </td>
            <td>{{ item.container || '-' }}</td>
            <td>
              <span :class="['status-tag', statusClass(item.status)]">
                {{ item.status || '-' }}
              </span>
            </td>
            <td class="path-cell" :title="item.path || '-'">
              {{ item.path || '-' }}
            </td>
            <td
              class="message-cell"
              :title="item.reason || item.message || '-'"
            >
              {{ item.reason || item.message || '-' }}
            </td>
          </tr>
        </tbody>

        <tbody v-else>
          <tr>
            <td colspan="5" class="empty-cell">
              {{ loading ? '错误数据加载中...' : '暂无错误日志' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.panel {
  max-width: 1280px;
  margin: 0 auto 24px;
  padding: 24px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgb(15 23 42 / 6%);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.panel-header h2,
.panel-header p {
  margin-top: 0;
}

.panel-header h2 {
  margin-bottom: 6px;
  font-size: 20px;
}

.panel-header p {
  margin-bottom: 0;
  color: #64748b;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}

.data-table {
  width: 100%;
  min-width: 820px;
  table-layout: fixed;
  border-collapse: collapse;
}

.data-table th {
  padding: 13px 16px;
  color: #475569;
  font-size: 13px;
  text-align: left;
  white-space: nowrap;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.data-table td {
  padding: 14px 16px;
  color: #334155;
  overflow: hidden;
  border-bottom: 1px solid #eef2f7;
}

.error-table th:nth-child(1) {
  width: 14%;
}

.error-table th:nth-child(2) {
  width: 18%;
}

.error-table th:nth-child(3) {
  width: 12%;
}

.error-table th:nth-child(4) {
  width: 16%;
}

.error-table th:nth-child(5) {
  width: 40%;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tbody tr:hover {
  background: #f8fafc;
}

.path-cell,
.message-cell {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-tag,
.level-tag,
.count-badge {
  display: inline-block;
  padding: 4px 9px;
  font-size: 12px;
  font-weight: 700;
  border-radius: 999px;
}

.status-server-error {
  color: #b91c1c;
  background: #fee2e2;
}

.status-client-error {
  color: #b45309;
  background: #fef3c7;
}

.status-normal {
  color: #047857;
  background: #d1fae5;
}

.status-muted {
  color: #475569;
  background: #e2e8f0;
}

.level-high {
  color: #b91c1c;
  background: #fee2e2;
}

.level-medium {
  color: #b45309;
  background: #fef3c7;
}

.level-low {
  color: #1d4ed8;
  background: #dbeafe;
}

.count-badge {
  color: #1d4ed8;
  background: #dbeafe;
}

.danger-badge {
  color: #b91c1c;
  background: #fee2e2;
}

.empty-cell {
  padding: 36px !important;
  color: #94a3b8 !important;
  text-align: center;
}

@media (max-width: 760px) {
  .panel {
    padding: 16px;
  }

  .panel-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
