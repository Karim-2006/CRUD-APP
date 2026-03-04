<template>
  <div class="product-manager">
    <div class="header">
      <div class="logo-area">
        <div class="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
            <path fill-rule="evenodd" d="M7.5 6v.75H5.513c-.96 0-1.764.724-1.865 1.679l-1.263 12A1.875 1.875 0 004.25 22.5h15.5a1.875 1.875 0 001.865-2.071l-1.263-12a1.875 1.875 0 00-1.865-1.679H16.5V6a4.5 4.5 0 10-9 0zM12 3a3 3 0 00-3 3v.75h6V6a3 3 0 00-3-3zm-3 8.25a3 3 0 106 0v-.75a.75.75 0 011.5 0v.75a4.5 4.5 0 11-9 0v-.75a.75.75 0 011.5 0v.75z" clip-rule="evenodd" />
          </svg>
        </div>
        <h1>Product<span class="highlight">Hub</span></h1>
      </div>
      <button class="add-btn" @click="showForm = !showForm" :class="{ 'cancel-btn': showForm }">
        <span class="btn-icon" v-if="!showForm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
        </span>
        <span class="btn-icon" v-else>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </span>
        {{ showForm ? 'Close' : 'New Product' }}
      </button>
    </div>

    <!-- Add/Edit Product Form -->
    <transition name="slide-fade">
      <div v-if="showForm || isEditing" class="form-section">
        <div class="form-card glass-panel">
          <div class="form-header">
            <h2>{{ isEditing ? 'Edit Product' : 'Add New Product' }}</h2>
            <p class="form-subtitle">{{ isEditing ? 'Update the product details below' : 'Fill in the details to create a new product' }}</p>
          </div>
          
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>Product Name</label>
              <div class="input-wrapper">
                <input v-model="productForm.name" placeholder="e.g. Wireless Headphones" required />
                <span class="input-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z" />
                  </svg>
                </span>
              </div>
            </div>
            
            <div class="form-group">
              <label>Description</label>
              <textarea v-model="productForm.description" placeholder="Describe the features and benefits..." required rows="3"></textarea>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Price ($)</label>
                <div class="input-wrapper">
                  <input v-model.number="productForm.price" type="number" step="0.01" placeholder="0.00" required />
                  <span class="input-icon">$</span>
                </div>
              </div>
              <div class="form-group half">
                <label>Stock</label>
                <div class="input-wrapper">
                  <input v-model.number="productForm.stock" type="number" placeholder="0" required />
                  <span class="input-icon">#</span>
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" v-if="isEditing" @click="cancelEdit" class="cancel-btn-secondary">Cancel</button>
              <button type="submit" class="submit-btn">
                {{ isEditing ? 'Save Changes' : 'Create Product' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Product List -->
    <div class="list-section">
      <div class="section-header">
        <h2 class="section-title">Inventory</h2>
        <span class="badge-pill">{{ products.length }} Items</span>
      </div>
      
      <div v-if="products.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
          </svg>
        </div>
        <h3>No products yet</h3>
        <p>Get started by adding your first product to the inventory.</p>
        <button class="add-btn-small" @click="showForm = true">Add Product</button>
      </div>

      <div class="products-grid">
        <div v-for="product in products" :key="product.id" class="product-card glass-panel">
          <div class="card-content">
            <div class="card-header">
              <h3>{{ product.name }}</h3>
              <span class="price-tag">${{ product.price }}</span>
            </div>
            <p class="description">{{ product.description }}</p>
            
            <div class="stock-indicator">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: Math.min(product.stock, 100) + '%', backgroundColor: getStockColor(product.stock) }"></div>
              </div>
              <span class="stock-text" :style="{ color: getStockColor(product.stock) }">
                {{ product.stock }} in stock
              </span>
            </div>
          </div>

          <div class="card-footer">
            <button @click="editProduct(product)" class="action-btn edit" title="Edit">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
              </svg>
              Edit
            </button>
            <button @click="deleteProduct(product.id)" class="action-btn delete" title="Delete">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
      productForm: {
        name: '',
        description: '',
        price: null,
        stock: null
      },
      isEditing: false,
      editingId: null,
      showForm: false,
      apiUrl: 'http://localhost:8000'
    };
  },
  methods: {
    getStockColor(stock) {
      if (stock === 0) return '#ef4444'; // Red
      if (stock < 10) return '#f59e0b'; // Amber
      return '#10b981'; // Emerald
    },
    async fetchProducts() {
      try {
        const response = await axios.get(`${this.apiUrl}/products`);
        this.products = response.data;
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },
    async handleSubmit() {
      if (this.isEditing) {
        await this.updateProduct();
      } else {
        await this.addProduct();
      }
    },
    async addProduct() {
      try {
        await axios.post(`${this.apiUrl}/product`, this.productForm);
        this.resetForm();
        this.fetchProducts();
        this.showForm = false;
      } catch (error) {
        console.error("Error adding product:", error);
      }
    },
    async updateProduct() {
      try {
        await axios.put(`${this.apiUrl}/product/${this.editingId}`, this.productForm);
        this.resetForm();
        this.fetchProducts();
      } catch (error) {
        console.error("Error updating product:", error);
      }
    },
    async deleteProduct(id) {
      if (confirm('Are you sure you want to delete this product?')) {
        try {
          await axios.delete(`${this.apiUrl}/product/${id}`);
          this.fetchProducts();
        } catch (error) {
          console.error("Error deleting product:", error);
        }
      }
    },
    editProduct(product) {
      this.productForm = { ...product };
      this.isEditing = true;
      this.editingId = product.id;
      this.showForm = true;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.productForm = {
        name: '',
        description: '',
        price: null,
        stock: null
      };
      this.isEditing = false;
      this.editingId = null;
      if (!this.isEditing) this.showForm = false;
    }
  },
  mounted() {
    this.fetchProducts();
  }
};
</script>

<style scoped>
.product-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Glass Panel Effect */
.glass-panel {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
}

.logo-icon svg {
  width: 24px;
  height: 24px;
}

.header h1 {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
  color: var(--text-main);
  letter-spacing: -0.025em;
}

.highlight {
  color: var(--primary);
}

.add-btn {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
}

.add-btn.cancel-btn {
  background: white;
  color: var(--text-main);
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.btn-icon {
  display: flex;
  align-items: center;
}

.btn-icon svg {
  width: 20px;
  height: 20px;
}

/* Form Section */
.form-section {
  margin-bottom: 50px;
}

.form-card {
  padding: 40px;
  border-radius: 24px;
  max-width: 600px;
  margin: 0 auto;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
}

.form-header h2 {
  margin: 0 0 8px 0;
  color: var(--text-main);
  font-size: 1.5rem;
}

.form-subtitle {
  color: var(--text-light);
  margin: 0;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.9rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
  font-weight: 500;
}

.input-icon svg {
  width: 20px;
  height: 20px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  padding-right: 40px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f8fafc;
  color: var(--text-main);
  box-sizing: border-box;
  font-family: inherit;
}

.form-group textarea {
  padding-right: 16px;
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
  background: white;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-group.half {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.submit-btn {
  flex: 1;
  background: var(--text-main);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.submit-btn:hover {
  background: #0f172a;
  transform: translateY(-1px);
}

.cancel-btn-secondary {
  flex: 1;
  background: transparent;
  color: var(--text-light);
  border: 2px solid #e2e8f0;
  padding: 14px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn-secondary:hover {
  border-color: #cbd5e1;
  color: var(--text-main);
  background: white;
}

/* List Section */
.section-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
}

.badge-pill {
  background: #e0e7ff;
  color: var(--primary);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 24px;
  border: 2px dashed #cbd5e1;
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

.empty-icon svg {
  width: 32px;
  height: 32px;
}

.empty-state h3 {
  margin: 0 0 8px;
  color: var(--text-main);
}

.empty-state p {
  color: var(--text-light);
  margin: 0 0 25px;
}

.add-btn-small {
  background: var(--primary);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.add-btn-small:hover {
  background: var(--primary-dark);
}

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 30px;
}

.product-card {
  border-radius: 20px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(99, 102, 241, 0.3);
}

.card-content {
  padding: 24px;
  flex-grow: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 10px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--text-main);
  line-height: 1.4;
  font-weight: 700;
}

.price-tag {
  background: var(--text-main);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  white-space: nowrap;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.description {
  color: var(--text-light);
  margin-bottom: 24px;
  line-height: 1.6;
  font-size: 0.95rem;
}

.stock-indicator {
  margin-top: auto;
}

.progress-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.stock-text {
  font-size: 0.85rem;
  font-weight: 600;
}

.card-footer {
  display: flex;
  border-top: 1px solid #f1f5f9;
  background: rgba(248, 250, 252, 0.5);
}

.action-btn {
  flex: 1;
  background: none;
  border: none;
  padding: 16px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.action-btn.edit {
  color: var(--primary);
  border-right: 1px solid #f1f5f9;
}

.action-btn.edit:hover {
  background: rgba(99, 102, 241, 0.05);
}

.action-btn.delete {
  color: var(--danger);
}

.action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.05);
}

/* Animations */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* Responsive */
@media (max-width: 640px) {
  .header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .form-card {
    padding: 24px;
  }
}
</style>
