<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const props = defineProps({
  refreshKey: {
    type: Number,
    default: 0,
  },
})

const API_BASE = 'http://192.168.177.130:8000'
const chartElement = ref(null)
const loading = ref(false)
const errorMessage = ref('')
const hasData = ref(true)

let chart = null

function resizeChart() {
  chart?.resize()
}

async function loadTrend() {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await axios.get(`${API_BASE}/stats/trend`)
    const trend = response.data || []

    hasData.value = trend.length > 0

    if (!hasData.value) {
      chart?.clear()
      return
    }

    await nextTick()

    if (!chart) {
      chart = echarts.init(chartElement.value)
    }

    chart.setOption({
      tooltip: {
        trigger: 'axis',
      },
      grid: {
        left: 48,
        right: 24,
        top: 32,
        bottom: 52,
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: trend.map((item) => item.time),
        axisLabel: {
          color: '#64748b',
          rotate: 28,
        },
        axisLine: {
          lineStyle: { color: '#cbd5e1' },
        },
      },
      yAxis: {
        type: 'value',
        minInterval: 1,
        axisLabel: { color: '#64748b' },
        splitLine: {
          lineStyle: { color: '#e2e8f0' },
        },
      },
      series: [
        {
          name: '日志数量',
          type: 'line',
          smooth: true,
          data: trend.map((item) => item.count),
          symbol: 'circle',
          symbolSize: 7,
          lineStyle: {
            width: 3,
            color: '#2563eb',
          },
          itemStyle: {
            color: '#2563eb',
          },
          areaStyle: {
            color: 'rgba(37, 99, 235, 0.12)',
          },
        },
      ],
    })
  } catch (error) {
    hasData.value = false
    errorMessage.value = '趋势数据加载失败，请检查后端服务。'
  } finally {
    loading.value = false
  }
}

watch(
  () => props.refreshKey,
  () => loadTrend(),
  { immediate: true },
)

window.addEventListener('resize', resizeChart)

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chart?.dispose()
  chart = null
})
</script>

<template>
  <section class="trend-panel">
    <div class="trend-header">
      <div>
        <h2>日志趋势</h2>
        <p>按小时统计已采集的容器日志数量</p>
      </div>
      <span v-if="loading" class="loading-text">加载中…</span>
    </div>

    <p v-if="errorMessage" class="state-message error-message">
      {{ errorMessage }}
    </p>
    <p v-else-if="!hasData && !loading" class="state-message">
      暂无趋势数据
    </p>
    <div v-show="hasData" ref="chartElement" class="trend-chart" />
  </section>
</template>

<style scoped>
.trend-panel {
  max-width: 1280px;
  margin: 0 auto 24px;
  padding: 24px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgb(15 23 42 / 6%);
}

.trend-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.trend-header h2,
.trend-header p {
  margin-top: 0;
}

.trend-header h2 {
  margin-bottom: 6px;
  font-size: 20px;
}

.trend-header p,
.loading-text,
.state-message {
  color: #64748b;
}

.trend-header p {
  margin-bottom: 0;
}

.loading-text {
  font-size: 14px;
}

.trend-chart {
  width: 100%;
  height: 300px;
  margin-top: 12px;
}

.state-message {
  padding: 48px 0 36px;
  margin: 0;
  text-align: center;
}

.error-message {
  color: #b91c1c;
}

@media (max-width: 760px) {
  .trend-panel {
    padding: 16px;
  }

  .trend-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .trend-chart {
    height: 260px;
  }
}
</style>
