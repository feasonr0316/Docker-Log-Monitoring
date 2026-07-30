<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    default: 0,
  },
  description: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'default',
  },
})
</script>

<template>
  <article :class="['stat-card', `stat-card-${type}`]">
    <span class="stat-label">{{ label }}</span>
    <strong>{{ value }}</strong>
    <small>{{ description }}</small>
  </article>
</template>

<style scoped>
.stat-card {
  padding: 22px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-top: 4px solid #64748b;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgb(15 23 42 / 6%);
}

.stat-card-danger {
  border-top-color: #ef4444;
}

.stat-card-primary {
  border-top-color: #2563eb;
}

.stat-label,
.stat-card small {
  display: block;
  color: #64748b;
}

.stat-card strong {
  display: block;
  margin: 12px 0 6px;
  color: #0f172a;
  font-size: 32px;
}
</style>
