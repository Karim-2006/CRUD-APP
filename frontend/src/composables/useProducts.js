import { ref, computed } from 'vue';
import { productService } from '../services/api';
import { useToast } from '../components/ui/ToastNotification.vue';

export function useProducts() {
    const products = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const { trigger } = useToast();

    // Helper for toast to avoid destructuring issues in templates if needed, 
    // though here we use it inside the composable.
    const toast = (msg, type) => trigger(msg, type);

    const totalValue = computed(() => {
        return products.value.reduce((acc, p) => acc + (p.price * p.stock), 0);
    });

    const lowStockCount = computed(() => {
        return products.value.filter(p => p.stock < 10).length;
    });

    const fetchProducts = async () => {
        loading.value = true;
        try {
            products.value = await productService.getAll();
            error.value = null;
        } catch (err) {
            console.error(err);
            error.value = 'Failed to fetch products';
            toast('Failed to load products', 'error');
        } finally {
            loading.value = false;
        }
    };

    const addProduct = async (product) => {
        try {
            await productService.create(product);
            await fetchProducts();
            toast('Product created successfully', 'success');
            return true;
        } catch (err) {
            console.error(err);
            toast('Failed to create product', 'error');
            return false;
        }
    };

    const updateProduct = async (id, product) => {
        try {
            await productService.update(id, product);
            await fetchProducts();
            toast('Product updated successfully', 'success');
            return true;
        } catch (err) {
            console.error(err);
            toast('Failed to update product', 'error');
            return false;
        }
    };

    const deleteProduct = async (id) => {
        if (!confirm('Are you sure you want to delete this product?')) return;
        
        try {
            await productService.delete(id);
            await fetchProducts();
            toast('Product deleted successfully', 'success');
        } catch (err) {
            console.error(err);
            toast('Failed to delete product', 'error');
        }
    };

    return {
        products,
        loading,
        error,
        totalValue,
        lowStockCount,
        fetchProducts,
        addProduct,
        updateProduct,
        deleteProduct
    };
}
