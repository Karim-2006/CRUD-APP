<script setup>
import ProductManager from './components/ProductManager.vue'
</script>

<template>
  <div class="app-container">
    <div class="bg-gradient"></div>
    <ProductManager />
  </div>
</template>

<style>
:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --secondary: #ec4899;
  --accent: #8b5cf6;
  --background: #f8fafc;
  --text-main: #1e293b;
  --text-light: #64748b;
  --card-bg: #ffffff;
  --danger: #ef4444;
  --success: #10b981;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--background);
  color: var(--text-main);
  line-height: 1.6;
}

.app-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: 
    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
    radial-gradient(at 0% 100%, rgba(16, 185, 129, 0.15) 0px, transparent 50%);
  filter: blur(40px);
}
</style>
