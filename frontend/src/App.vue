<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <div class="bg-gradient"></div>
    <RouterView />
  </div>
</template>

<style>
:root {
  --primary: #f97316; /* Orange-500 */
  --primary-dark: #ea580c; /* Orange-600 */
  --secondary: #facc15; /* Yellow-400 */
  --accent: #fbbf24; /* Amber-400 */
  --background: #fff7ed; /* Orange-50 */
  --text-main: #1c1917; /* Stone-900 */
  --text-light: #57534e; /* Stone-600 */
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
    radial-gradient(at 0% 0%, rgba(253, 186, 116, 0.2) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(254, 240, 138, 0.2) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(251, 146, 60, 0.1) 0px, transparent 50%),
    radial-gradient(at 0% 100%, rgba(252, 211, 77, 0.1) 0px, transparent 50%);
  filter: blur(60px);
}
</style>
