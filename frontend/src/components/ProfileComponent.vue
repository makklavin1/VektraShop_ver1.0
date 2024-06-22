<template>
  <div class="profile">
    <h1 class="display-4 mb-4">Личный кабинет</h1>
    <nav class="profile-nav">
      <button @click="currentSection = 'balance'" :class="{ active: currentSection === 'balance' }">Баланс</button>
      <button @click="currentSection = 'orders'" :class="{ active: currentSection === 'orders' }">Заказы</button>
      <button @click="currentSection = 'history'" :class="{ active: currentSection === 'history' }">История заказов</button>
    </nav>
    <div v-if="currentSection === 'balance'">
      <BalanceAndCards :user="user" />
    </div>
    <div v-if="currentSection === 'orders'">
      <ActiveOrdersComponent :orders="user.active_orders" />
    </div>
    <div v-if="currentSection === 'history'">
      <PurchaseHistoryComponent :purchaseHistory="user.purchase_history" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import BalanceAndCards from './BalanceComponent.vue';
import ActiveOrdersComponent from './ActiveOrdersComponent.vue';
import PurchaseHistoryComponent from './PurchaseHistoryComponent.vue';

export default {
  name: 'ProfileComponent',
  components: {
    BalanceAndCards,
    ActiveOrdersComponent,
    PurchaseHistoryComponent
  },
  data() {
    return {
      user: {},
      currentSection: 'balance',
      telegramLink: ''
    }
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('/users/profile/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      .then(response => {
        this.user = response.data;
        this.telegramLink = `https://t.me/vektrashop_bot?start=${response.data.telegram_token}`;
      })
      .catch(error => {
        console.error('Error fetching profile data', error.response.data);
        if (error.response.status === 401) {
          this.$router.push('/login');
        }
      });
    } else {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.profile {
  max-width: 800px;
  margin: 0 auto;
}

.profile-nav {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1em;
}

.profile-nav button {
  padding: 0.5em 1em;
  border: none;
  background-color: #f8f8f8;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.profile-nav button:hover {
  background-color: #e0e0e0;
}

.profile-nav button.active {
  background-color: #d0d0d0;
  font-weight: bold;
}

.profile-section {
  background-color: #fff;
  padding: 1em;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
