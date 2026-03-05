import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const productService = {
    async getAll() {
        const response = await api.get('/products');
        return response.data;
    },
    async create(product) {
        const response = await api.post('/product', product);
        return response.data;
    },
    async update(id, product) {
        const response = await api.put(`/product/${id}`, product);
        return response.data;
    },
    async delete(id) {
        const response = await api.delete(`/product/${id}`);
        return response.data;
    },
};

export default api;
