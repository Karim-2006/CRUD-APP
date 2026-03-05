<template>
  <div class="product-manager">
    <header class="app-header">
      <div class="logo-area">
        <div class="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd" d="M7.5 6v.75H5.513c-.96 0-1.764.724-1.865 1.679l-1.263 12A1.875 1.875 0 004.25 22.5h15.5a1.875 1.875 0 001.865-2.071l-1.263-12a1.875 1.875 0 00-1.865-1.679H16.5V6a4.5 4.5 0 10-9 0zM12 3a3 3 0 00-3 3v.75h6V6a3 3 0 00-3-3zm-3 8.25a3 3 0 106 0v-.75a.75.75 0 011.5 0v.75a4.5 4.5 0 11-9 0v-.75a.75.75 0 011.5 0v.75z" clip-rule="evenodd" />
          </svg>
        </div>
        <h1>Product<span class="highlight">Hub</span></h1>
      </div>
    </header>

    <main class="main-content">
      <!-- Toolbar -->
      <div class="toolbar glass-panel">
        <h2 class="section-title">Inventory</h2>
        <button class="btn-primary small add-product-btn" @click="toggleForm" :class="{ 'active': showForm }" aria-label="Toggle add product form">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 icon-transition" :class="{ 'rotate-45': showForm }">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          <span>{{ showForm ? 'Close' : 'Add Product' }}</span>
        </button>
      </div>
      <!-- Add/Edit Product Form -->
      <transition name="expand">
        <div v-if="showForm || isEditing" class="form-container">
          <div class="form-card glass-panel">
            <div class="form-header">
              <h2>{{ isEditing ? 'Edit Product' : 'New Product' }}</h2>
              <button @click="resetForm" class="close-icon-btn" aria-label="Close form">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <form @submit.prevent="handleSubmit" class="compact-form">
              <div class="form-grid">
                <div class="form-group full-width">
                  <label for="name">Product Name</label>
                  <input id="name" v-model="productForm.name" placeholder="e.g. Wireless Headphones" required />
                </div>
                
                <div class="form-group full-width">
                  <label for="description">Description</label>
                  <textarea id="description" v-model="productForm.description" placeholder="Product details..." required rows="2"></textarea>
                </div>

                <div class="form-group">
                  <label for="price">Price ($)</label>
                  <input id="price" v-model.number="productForm.price" type="number" step="0.01" placeholder="0.00" required />
                </div>
                
                <div class="form-group">
                  <label for="stock">Stock</label>
                  <input id="stock" v-model.number="productForm.stock" type="number" placeholder="0" required />
                </div>
              </div>

              <div class="form-actions">
                <button type="button" v-if="isEditing" @click="cancelEdit" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary" :disabled="loading">
                  {{ loading ? 'Saving...' : (isEditing ? 'Save' : 'Create') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>

      <!-- Stats Bar -->
      <div class="stats-bar glass-panel">
        <div class="stat-item">
          <span class="stat-label">Total Items</span>
          <span class="stat-value">{{ products.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Total Value</span>
          <span class="stat-value">${{ totalValue.toLocaleString() }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Low Stock</span>
          <span class="stat-value warning">{{ lowStockCount }}</span>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && products.length === 0" class="loading-state">
        <div class="spinner"></div>
        <p>Loading products...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="products.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
          </svg>
        </div>
        <h3>Inventory Empty</h3>
        <p>Add your first product to get started.</p>
        <button class="btn-primary small" @click="showForm = true">Add Product</button>
      </div>

      <!-- Product Grid -->
      <div v-else class="products-grid">
        <ProductCard 
          v-for="product in products" 
          :key="product.id" 
          :product="product" 
          @edit="editProduct" 
          @delete="confirmDelete" 
        />
      </div>
    </main>

    <ToastNotification />
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useProducts } from '../composables/useProducts';
import ProductCard from './ProductCard.vue';
import ToastNotification from './ui/ToastNotification.vue';

export default {
  components: {
    ProductCard,
    ToastNotification
  },
  setup() {
    const { 
      products, 
      loading, 
      totalValue, 
      lowStockCount, 
      fetchProducts, 
      addProduct, 
      updateProduct, 
      deleteProduct 
    } = useProducts();

    const showForm = ref(false);
    const isEditing = ref(false);
    const editingId = ref(null);
    const productForm = ref({
      name: '',
      description: '',
      price: null,
      stock: null
    });

    onMounted(() => {
      fetchProducts();
    });

    const toggleForm = () => {
      showForm.value = !showForm.value;
      if (!showForm.value) resetForm();
    };

    const handleSubmit = async () => {
      let success = false;
      if (isEditing.value) {
        success = await updateProduct(editingId.value, productForm.value);
      } else {
        success = await addProduct(productForm.value);
      }
      
      if (success) {
        resetForm();
      }
    };

    const editProduct = (product) => {
      productForm.value = { ...product };
      isEditing.value = true;
      editingId.value = product.id;
      showForm.value = true;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const confirmDelete = async (id) => {
      await deleteProduct(id);
    };

    const resetForm = () => {
      productForm.value = {
        name: '',
        description: '',
        price: null,
        stock: null
      };
      isEditing.value = false;
      editingId.value = null;
      showForm.value = false;
    };

    const cancelEdit = () => {
      resetForm();
    };

    return {
      products,
      loading,
      totalValue,
      lowStockCount,
      showForm,
      isEditing,
      productForm,
      toggleForm,
      handleSubmit,
      editProduct,
      confirmDelete,
      resetForm,
      cancelEdit
    };
  }
};
</script>

<style scoped>
/* Design System Variables */
:root {
  --primary: #f97316;
  --primary-hover: #ea580c;
  --bg-glass: rgba(255, 255, 255, 0.9);
  --border-glass: rgba(255, 255, 255, 0.8);
  --shadow-sm: 0 2px 8px rgba(249, 115, 22, 0.08);
  --shadow-md: 0 8px 24px rgba(249, 115, 22, 0.12);
  --radius-lg: 16px;
  --radius-md: 12px;
  --radius-sm: 8px;
  --space-unit: 8px;
}

.product-manager {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px;
  min-height: 100vh;
}

/* Glassmorphism */
.glass-panel {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border-radius: 16px;
}

/* Header */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 0 8px;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f97316, #fbbf24);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.app-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: #1c1917;
  letter-spacing: -0.5px;
}

.highlight { color: #f97316; }

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f97316;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  background: #ea580c;
  box-shadow: 0 6px 16px rgba(249, 115, 22, 0.4);
}

.add-btn.active {
  background: #ffffff;
  color: #ef4444;
  border: 1px solid #fee2e2;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.icon-transition { transition: transform 0.3s ease; }
.rotate-45 { transform: rotate(45deg); }

/* Toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 24px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: #1c1917;
}

.add-product-btn {
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-product-btn.active {
  background: #ffffff;
  color: #ef4444;
  border: 1px solid #fee2e2;
}

/* Form Section */
.form-container {
  margin-bottom: 32px;
  overflow: hidden;
}

.form-card {
  padding: 24px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.form-header h2 {
  font-size: 1.1rem;
  margin: 0;
  color: #334155;
}

.close-icon-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-icon-btn:hover {
  background: #f1f5f9;
  color: #64748b;
}

.compact-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 6px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px; /* Increased padding for better touch targets */
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem; /* Standard readable size */
  transition: all 0.2s ease-in-out;
  background: #ffffff; /* White background for better contrast */
  font-family: inherit;
  box-sizing: border-box;
  color: #000000; /* WCAG AAA Contrast */
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #64748b;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #6366f1;
  background: white;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 8px;
}

.btn-primary, .btn-secondary {
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #f97316;
  color: white;
}

.btn-primary:hover { background: #ea580c; }
.btn-primary:disabled { opacity: 0.7; cursor: not-allowed; }

.btn-secondary {
  background: white;
  border: 1px solid #cbd5e1;
  color: #475569;
}

.btn-secondary:hover { background: #f8fafc; }

/* Stats Bar */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px;
  margin-bottom: 32px;
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #94a3b8;
  font-weight: 600;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #334155;
}

.stat-value.warning { color: #f59e0b; }

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

/* Loading & Empty States */
.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top-color: #6366f1;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  width: 64px;
  height: 64px;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: #94a3b8;
}

.empty-icon svg { width: 32px; height: 32px; }

.empty-state h3 { margin: 0 0 8px; color: #1e293b; }
.empty-state p { margin: 0 0 25px; }

.btn-primary.small { padding: 8px 20px; }

/* Animations */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 500px;
  opacity: 1;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  margin-bottom: 0;
}

/* Responsive Breakpoints */

/* Mobile First (Base styles are mobile) */
.product-manager {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px;
  box-sizing: border-box;
}

.toolbar {
  flex-direction: row;
  padding: 12px 16px;
  gap: 12px;
}

.section-title {
  font-size: 1.1rem;
}

.form-grid {
  grid-template-columns: 1fr;
}

.form-group.full-width {
  grid-column: span 1;
}

.stats-bar {
  grid-template-columns: 1fr;
  text-align: left;
  gap: 12px;
}

.stat-item {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.products-grid {
  grid-template-columns: 1fr;
}

/* Tablet (>= 768px) */
@media (min-width: 768px) {
  .product-manager {
    padding: 24px;
  }

  .form-grid {
    grid-template-columns: 1fr 1fr;
  }

  .form-group.full-width {
    grid-column: span 2;
  }

  .stats-bar {
    grid-template-columns: repeat(3, 1fr);
    text-align: center;
    gap: 24px;
  }

  .stat-item {
    flex-direction: column;
    justify-content: center;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* Desktop (>= 1024px) */
@media (min-width: 1024px) {
  .product-manager {
    padding: 32px;
  }

  .products-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }
}

/* Large Desktop (>= 1280px) */
@media (min-width: 1280px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
