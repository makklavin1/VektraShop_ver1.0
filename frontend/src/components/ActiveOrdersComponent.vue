<template>
  <div class="active-orders">
    <h1 class="display-4 mb-4"></h1>
    <div v-if="activeOrders.length">
      <div v-for="order in activeOrders" :key="order.order_number" class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">Заказ № {{ order.order_number }}</h5>
          <p class="card-text">Дата заказа: {{ formatDate(order.created_at) }}</p>
          <h6 class="mt-3">Товары в заказе:</h6>
          <ul>
            <li v-for="item in order.items" :key="item.product.id">
              {{ item.product.name }} - {{ item.quantity }}
            </li>
          </ul>
          <p class="card-text">Статус заказа: {{ order.status }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>У вас нет активных заказов</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ActiveOrdersComponent',
  data() {
    return {
      activeOrders: []
    }
  },
  created() {
    this.fetchActiveOrders();
  },
  methods: {
    fetchActiveOrders() {
      axios.get('/orders/active-orders/', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`
        }
      }).then(response => {
        this.activeOrders = response.data;
      }).catch(error => {
        console.error('Error fetching active orders', error);
      });
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  }
}
</script>

<style scoped>
.active-orders {
  max-width: 600px;
  margin: 0 auto;
}

.card {
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.5em;
  font-weight: bold;
  color: #ff8c00;
}

.card-text {
  font-size: 1.2em;
  margin: 10px 0;
}
</style>
