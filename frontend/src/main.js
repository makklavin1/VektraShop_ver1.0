import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/styles.css';
import '@fortawesome/fontawesome-free/css/all.min.css'; // Импортируем стили Font Awesome

const app = createApp(App);

axios.defaults.baseURL = 'http://127.0.0.1:8000/api';

// Глобальное состояние аутентификации
app.config.globalProperties.$auth = {
  isAuthenticated: !!localStorage.getItem('token'),
  user: null,
  setUser(user) {
    this.user = user;
    this.isAuthenticated = true;
  },
  clearUser() {
    this.user = null;
    this.isAuthenticated = false;
  }
};

app.use(router);
app.mount('#app');
