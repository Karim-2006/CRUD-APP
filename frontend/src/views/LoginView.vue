<template>
  <div class="auth-container">
    <div class="auth-card glass-panel">
      <div class="auth-header">
        <div class="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-8 h-8">
            <path fill-rule="evenodd" d="M7.5 6v.75H5.513c-.96 0-1.764.724-1.865 1.679l-1.263 12A1.875 1.875 0 004.25 22.5h15.5a1.875 1.875 0 001.865-2.071l-1.263-12a1.875 1.875 0 00-1.865-1.679H16.5V6a4.5 4.5 0 10-9 0zM12 3a3 3 0 00-3 3v.75h6V6a3 3 0 00-3-3zm-3 8.25a3 3 0 106 0v-.75a.75.75 0 011.5 0v.75a4.5 4.5 0 11-9 0v-.75a.75.75 0 011.5 0v.75z" clip-rule="evenodd" />
          </svg>
        </div>
        <h2>Welcome Back</h2>
        <p>Sign in to manage your inventory</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="ENTER YOUR EMAIL"
            :class="{ 'error': errors.email }"
          />
          <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="••••••••"
            :class="{ 'error': errors.password }"
          />
          <span v-if="errors.password" class="error-msg">{{ errors.password }}</span>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary full-width" :disabled="authStore.loading">
            {{ authStore.loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </div>

        <div class="auth-footer">
          <p>Don't have an account? <router-link to="/register">Sign up</router-link></p>
        </div>
        
        <div v-if="authStore.error" class="api-error">
          {{ authStore.error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const errors = ref({});
const authStore = useAuthStore();
const router = useRouter();

const validate = () => {
  errors.value = {};
  if (!email.value) errors.value.email = 'Email is required';
  else if (!/\S+@\S+\.\S+/.test(email.value)) errors.value.email = 'Invalid email format';
  
  if (!password.value) errors.value.password = 'Password is required';
  
  return Object.keys(errors.value).length === 0;
};

const handleLogin = async () => {
  if (!validate()) return;
  
  const success = await authStore.login(email.value, password.value);
  if (success) {
    router.push('/');
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  border-radius: 24px;
  background: white;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f97316, #fbbf24);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 16px;
}

.auth-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1c1917;
  margin: 0 0 8px;
}

.auth-header p {
  color: #57534e;
  margin: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #4b5563;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f8fafc;
  box-sizing: border-box;
  color: #000000;
}

.form-group input:focus {
  outline: none;
  border-color: #f97316;
  background: white;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.form-group input.error {
  border-color: #ef4444;
}

.error-msg {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 4px;
  display: block;
}

.btn-primary {
  background: #f97316;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #ea580c;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.full-width {
  width: 100%;
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 0.875rem;
  color: #57534e;
}

.auth-footer a {
  color: #f97316;
  text-decoration: none;
  font-weight: 600;
}

.api-error {
  margin-top: 16px;
  padding: 12px;
  background: #fef2f2;
  color: #b91c1c;
  border-radius: 8px;
  font-size: 0.875rem;
  text-align: center;
}
</style>
