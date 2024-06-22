<template>
  <div>
    <h2></h2>
    <div v-for="order in purchaseHistory" :key="order.order_number" class="order">
      <h3>Заказ № {{ order.order_number }}</h3>
      <p>Дата заказа: {{ formatDate(order.created_at) }}</p>
      <p>Статус заказа: {{ order.status }}</p>
      <div>
        <h4>Товары в заказе:</h4>
        <ul>
          <li v-for="item in order.items" :key="item.product.id">
            {{ item.product.name }} - Количество: {{ item.quantity }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    purchaseHistory: {
      type: Array,
      required: true
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  }
}
</script>

<style scoped>
.order {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
