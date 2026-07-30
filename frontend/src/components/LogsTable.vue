<script setup>
const props = defineProps({
  logs: {
    type: Array,
    default: () => [],
  },
  total: {
    type: Number,
    default: 0,
  },
  page: {
    type: Number,
    default: 1,
  },
  totalPages: {
    type: Number,
    default: 1,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  container: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    default: '',
  },
})

const emit = defineEmits([
  'update:container',
  'update:status',
  'search',
  'reset',
  'prev-page',
  'next-page',
])

function statusClass(status) {
  const code = String(status || '').trim()

  if (code.startsWith('5')) return 'status-server-error'
  if (code.startsWith('4')) return 'status-client-error'
  if (code.startsWith('2') || code.startsWith('3')) return 'status-normal'

  return 'status-muted'
}

function updateContainer(event) {
  emit('update:container', event.target.value)
}

function updateStatus(event) {
  emit('update:status', event.target.value)
}
</script>

<template>
  <section class="panel">
    <div class="panel-header">
      <div>
        <h2>日志查询</h2>
        <p>按容器名称或状态筛选运行日志</p>
      </div>

      <span class="count-badge">共 {{ total }} 条</span>
    </div>

    <div class="filter-bar">
      <input
        :value="container"
        type="text"
        placeholder="容器名称，例如 nginx"
        @input="updateContainer"
        @keyup.enter="emit('search')"
      >

      <input
        :value="status"
        type="text"
        placeholder="状态码，例如 200、500"
        @input="updateStatus"
        @keyup.enter="emit('search')"
      >

      <button class="primary-button" @click="emit('search')">
        查询日志
      </button>

      <button class="secondary-button" @click="emit('reset')">
        重置
      </button>
    </div>

    <div class="table-wrapper">
      <table class="data-table logs-table">
        <thead>
          <tr>
            <th>时间</th>
            <th>容器</th>
            <th>状态</th>
            <th>路径</th>
            <th>日志内容</th>
          </tr>
        </thead>

        <tbody v-if="!loading && logs.length">
          <tr v-for="log in logs" :key="log.id">
            <td>{{ log.time || '-' }}</td>
            <td>{{ log.container || '-' }}</td>
            <td>
              <span :class="['status-tag', statusClass(log.status)]">
                {{ log.status || '-' }}
              </span>
            </td>
            <td class="path-cell" :title="log.path || '-'">
              {{ log.path || '-' }}
            </td>
            <td class="message-cell" :title="log.message || '-'">
              {{ log.message || '-' }}
            </td>
          </tr>
        </tbody>

        <tbody v-else>
          <tr>
            <td colspan="5" class="empty-cell">
              {{ loading ? '日志加载中...' : '暂无日志数据' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button
        :disabled="page <= 1 || loading"
        @click="emit('prev-page')"
      >
        上一页
      </button>

      <span>第 {{ page }} / {{ totalPages }} 页</span>

      <button
        :disabled="page >= totalPages || loading"
        @click="emit('next-page')"
      >
        下一页
      </button>
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

.panel-header,
.filter-bar,
.pagination {
  display: flex;
  align-items: center;
}

.panel-header {
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

.filter-bar {
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
}

input {
  min-width: 210px;
  padding: 10px 12px;
  color: #1e293b;
  font: inherit;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  outline: none;
}

input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgb(37 99 235 / 12%);
}

button {
  padding: 10px 16px;
  color: #334155;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  background: #fff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
}

button:hover:not(:disabled) {
  background: #f1f5f9;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.primary-button {
  color: #fff;
  background: #2563eb;
  border-color: #2563eb;
}

.primary-button:hover:not(:disabled) {
  background: #1d4ed8;
}

.secondary-button {
  background: #f8fafc;
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

.logs-table th:nth-child(1) {
  width: 14%;
}

.logs-table th:nth-child(2) {
  width: 18%;
}

.logs-table th:nth-child(3) {
  width: 12%;
}

.logs-table th:nth-child(4) {
  width: 16%;
}

.logs-table th:nth-child(5) {
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

.count-badge {
  color: #1d4ed8;
  background: #dbeafe;
}

.empty-cell {
  padding: 36px !important;
  color: #94a3b8 !important;
  text-align: center;
}

.pagination {
  justify-content: center;
  gap: 14px;
  margin-top: 18px;
  color: #475569;
  font-size: 14px;
}

@media (max-width: 760px) {
  .panel {
    padding: 16px;
  }

  .panel-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .filter-bar input,
  .filter-bar button {
    width: 100%;
  }
}
</style>
