<!-- OrderComponent.vue -->
<template>
  <div class="order">
    <h1>Orders</h1>
    <div v-for="order in orders" :key="order.order_number" class="order-item">
      <h2>Order {{ order.order_number }}</h2>
      <p>Status: {{ order.status }}</p>
      <ul>
        <li v-for="item in order.items" :key="item.product.id">{{ item.quantity }} x {{ item.product.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'OrderComponent',
  data() {
    return {
      orders: []
    };
  },
  created() {
    axios.get('/orders/', {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    }).then(response => {
      this.orders = response.data;
    }).catch(error => {
      console.error(error);
    });
  }
}
</script>
