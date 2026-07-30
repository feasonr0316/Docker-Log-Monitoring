<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import StatsCard from './components/StatsCard.vue'
import LogsTable from './components/LogsTable.vue'
import ErrorsTable from './components/ErrorsTable.vue'
import LogTrend from './components/LogTrend.vue'

const API_BASE = 'http://192.168.177.130:8000'

const stats = ref({
  total_logs: 0,
  total_errors: 0,
  containers: 0,
})

const logs = ref([])
const errors = ref([])
const total = ref(0)
const loadingLogs = ref(false)
const loadingErrors = ref(false)
const requestError = ref('')
const trendRefreshKey = ref(0)

const query = ref({
  container: '',
  status: '',
  page: 1,
  size: 10,
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(total.value / query.value.size))
})

async function getStats() {
  try {
    const res = await axios.get(`${API_BASE}/stats`)
    stats.value = res.data
  } catch (error) {
    requestError.value = '统计数据加载失败，请检查后端服务是否启动。'
  }
}

async function getLogs() {
  loadingLogs.value = true
  requestError.value = ''

  try {
    const res = await axios.get(`${API_BASE}/logs`, {
      params: {
        page: query.value.page,
        size: query.value.size,
        container: query.value.container || null,
        status: query.value.status || null,
      },
    })

    logs.value = res.data.data || []
    total.value = res.data.total || 0
  } catch (error) {
    logs.value = []
    total.value = 0
    requestError.value = '日志加载失败，请检查后端接口。'
  } finally {
    loadingLogs.value = false
  }
}

async function getErrors() {
  loadingErrors.value = true

  try {
    const res = await axios.get(`${API_BASE}/errors`, {
      params: {
        page: 1,
        size: 10,
      },
    })

    errors.value = res.data.data || []
  } catch (error) {
    errors.value = []
    requestError.value = '错误分析数据加载失败，请检查后端接口。'
  } finally {
    loadingErrors.value = false
  }
}

function searchLogs() {
  query.value.page = 1
  getLogs()
}

function resetSearch() {
  query.value.container = ''
  query.value.status = ''
  query.value.page = 1
  getLogs()
}

function prevPage() {
  if (query.value.page > 1) {
    query.value.page--
    getLogs()
  }
}

function nextPage() {
  if (query.value.page < totalPages.value) {
    query.value.page++
    getLogs()
  }
}

function refreshData() {
  getStats()
  getLogs()
  getErrors()
  trendRefreshKey.value += 1
}

onMounted(() => {
  refreshData()
})
</script>

<template>
  <main class="dashboard">
    <header class="page-header">
      <div>
        <p class="eyebrow">DOCKER LOG MONITOR</p>
        <h1>Docker 日志监控平台</h1>
        <p class="subtitle">实时查看容器运行日志、错误信息和系统概况</p>
      </div>

      <button class="refresh-button" @click="refreshData">
        刷新数据
      </button>
    </header>

    <p v-if="requestError" class="request-error">
      {{ requestError }}
    </p>

    <section class="stats-grid">
      <StatsCard
        label="日志总数"
        :value="stats.total_logs"
        description="已采集日志记录"
      />

      <StatsCard
        label="错误数量"
        :value="stats.total_errors"
        description="需要重点关注"
        type="danger"
      />

      <StatsCard
        label="容器数量"
        :value="stats.containers"
        description="当前监控容器"
        type="primary"
      />
    </section>

    <LogTrend :refresh-key="trendRefreshKey" />

    <LogsTable
      v-model:container="query.container"
      v-model:status="query.status"
      :logs="logs"
      :total="total"
      :page="query.page"
      :total-pages="totalPages"
      :loading="loadingLogs"
      @search="searchLogs"
      @reset="resetSearch"
      @prev-page="prevPage"
      @next-page="nextPage"
    />

    <ErrorsTable
      :errors="errors"
      :loading="loadingErrors"
    />
  </main>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard {
  min-height: 100vh;
  padding: 36px;
  color: #1e293b;
  background:
    radial-gradient(circle at top right, #dbeafe 0, transparent 30%),
    #f8fafc;
}

.page-header {
  display: flex;
  max-width: 1280px;
  margin: 0 auto 28px;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2563eb;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
}

h1,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 8px;
  font-size: 30px;
}

.subtitle {
  margin-bottom: 0;
  color: #64748b;
}

.stats-grid {
  display: grid;
  max-width: 1280px;
  margin: 0 auto 24px;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.refresh-button {
  padding: 10px 16px;
  color: #fff;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  background: #2563eb;
  border: 1px solid #2563eb;
  border-radius: 8px;
}

.refresh-button:hover {
  background: #1d4ed8;
}

.request-error {
  max-width: 1280px;
  margin: 0 auto 18px;
  padding: 12px 16px;
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
}

@media (max-width: 760px) {
  .dashboard {
    padding: 20px 14px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
