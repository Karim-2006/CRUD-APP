<template>
  <div class="product-card glass-panel" tabindex="0">
    <div class="card-body">
      <div class="card-top">
        <h3 class="product-title" :title="product.name">{{ product.name }}</h3>
        <span class="price-badge">${{ product.price }}</span>
      </div>
      <p class="product-desc">{{ product.description }}</p>
      
      <div class="stock-mini-bar">
        <div class="progress-bg">
          <div class="progress-fill" :style="{ width: Math.min(product.stock, 100) + '%', backgroundColor: stockColor }"></div>
        </div>
        <span class="stock-label" :style="{ color: stockColor }">
          {{ product.stock }} left
        </span>
      </div>
    </div>

    <div class="card-actions">
      <button @click="$emit('edit', product)" class="action-btn edit">
        Edit
      </button>
      <button @click="$emit('delete', product.id)" class="action-btn delete">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  computed: {
    stockColor() {
      if (this.product.stock === 0) return '#ef4444';
      if (this.product.stock < 10) return '#f59e0b';
      return '#10b981';
    }
  }
};
</script>

<style scoped>
.product-card {
  position: relative;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(16px);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.08);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.15);
  border-color: rgba(249, 115, 22, 0.3);
}

.product-card:focus-visible {
  outline: 2px solid #f97316;
  outline-offset: 2px;
}

.card-body {
  padding: 20px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 12px;
}

.product-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  color: #1c1917;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price-badge {
  background: #fff7ed;
  color: #c2410c;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  white-space: nowrap;
  border: 1px solid #ffedd5;
}

.product-desc {
  font-size: 0.85rem;
  color: #57534e;
  margin: 0 0 16px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.5em;
}

.stock-mini-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-bg {
  flex-grow: 1;
  height: 4px;
  background: #e5e5e5;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.stock-label {
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 45px;
  text-align: right;
}

.card-actions {
  display: flex;
  border-top: 1px solid #f3f4f6;
  background: #fafaf9;
}

.action-btn {
  flex: 1;
  border: none;
  background: none;
  padding: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.action-btn.edit {
  color: #f97316;
  border-right: 1px solid #f3f4f6;
}

.action-btn.edit:hover {
  background: #fff7ed;
  color: #ea580c;
}

.action-btn.delete {
  color: #ef4444;
}

.action-btn.delete:hover {
  background: #fef2f2;
  color: #dc2626;
}
</style>
