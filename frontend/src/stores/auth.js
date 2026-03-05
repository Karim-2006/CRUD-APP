import { defineStore } from 'pinia';
import api from '../services/api';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    currentUser: (state) => state.user,
  },

  actions: {
    async login(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await api.post('/login', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        const { access_token, refresh_token } = response.data;
        this.setTokens(access_token, refresh_token);
        this.user = jwtDecode(access_token);
        
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Login failed';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async register(username, email, password) {
      this.loading = true;
      this.error = null;
      try {
        await api.post('/signup', { username, email, password });
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Registration failed';
        return false;
      } finally {
        this.loading = false;
      }
    },

    logout() {
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },

    setTokens(access, refresh) {
      this.accessToken = access;
      this.refreshToken = refresh;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
    },
    
    initialize() {
       if (this.accessToken) {
           try {
               const decoded = jwtDecode(this.accessToken);
               const currentTime = Date.now() / 1000;
               if (decoded.exp < currentTime) {
                   this.logout();
               } else {
                   this.user = decoded;
               }
           } catch {
               this.logout();
           }
       }
    }
  },
});
