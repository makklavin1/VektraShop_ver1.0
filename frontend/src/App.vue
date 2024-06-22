<template>
  <div id="app">
    <header class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container">
        <h1 class="navbar-brand">Вектра</h1>
        <nav class="nav">
          <router-link class="nav-link" to="/">Главная</router-link>
          <router-link v-if="isAuthenticated" class="nav-link" to="/profile">Личный кабинет</router-link>
          <router-link v-if="isAuthenticated" class="nav-link" to="/stats">Статистики</router-link>
          <router-link v-if="!isAuthenticated" class="nav-link" to="/login">Вход</router-link>
          <button v-if="isAuthenticated" class="btn btn-outline-danger ml-auto" @click="logout">Выйти</button>
        </nav>
      </div>
    </header>
    <main class="container mt-4">
      <router-view @update-cart="updateCart"/>
    </main>
    <CartComponent :cart-items="cartItems" @update-cart="updateCart" />
  </div>
</template>

<script>
import axios from 'axios';
import CartComponent from './components/CartComponent.vue';
import eventBus from './eventBus';

export default {
  name: 'App',
  components: {
    CartComponent
  },
  data() {
    return {
      cartItems: [],
      isAuthenticated: !!localStorage.getItem('token')
    }
  },
  created() {
    eventBus.on('user-authenticated', this.updateAuthenticationStatus);
    eventBus.on('cart-updated', this.loadCart);
  },
  methods: {
    updateCart(cart) {
      this.cartItems = cart;
    },
    loadCart() {
      let cart = localStorage.getItem('cart');
      this.cartItems = cart ? JSON.parse(cart) : [];
    },
    updateAuthenticationStatus() {
      this.isAuthenticated = !!localStorage.getItem('token');
      if (this.isAuthenticated) {
        axios.get('/users/profile/', {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        }).then(response => {
          this.$auth.setUser(response.data);
        }).catch(error => {
          console.error('Error fetching profile', error);
          this.$auth.clearUser();
          localStorage.removeItem('token');
          this.isAuthenticated = false;
        });
      } else {
        this.$auth.clearUser();
        localStorage.removeItem('token');
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$auth.clearUser();
      this.isAuthenticated = false;
      eventBus.emit('user-authenticated');
      this.$router.push('/');
    }
  },
  mounted() {
    this.loadCart();
    this.updateAuthenticationStatus();
  },
  beforeUnmount() {
    eventBus.off('user-authenticated', this.updateAuthenticationStatus);
    eventBus.off('cart-updated', this.loadCart);
  }
}
</script>

<style scoped>
/* Ваши стили здесь */
</style>
