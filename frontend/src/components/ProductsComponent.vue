<template>
  <div>
    <h1 class="display-4 mb-4"></h1>
    <div class="row">
      <div class="col-md-4 mb-4" v-for="product in products" :key="product.id">
        <div class="card h-100">
          <img :src="getImageUrl(product.image)" class="card-img-top" alt="Product image">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="card-text">Цена {{ product.price }}</p>
            <div class="stock-info">
              <p v-if="product.stock > 0" class="card-text">В наличии: {{ product.stock }}</p>
            </div>
            <button
              :class="['btn', 'btn-block', product.stock > 0 ? 'btn-primary' : 'btn-secondary']"
              :disabled="product.stock === 0"
              @click="addToCart(product)">
              {{ product.stock > 0 ? 'В корзину' : 'Нет в наличии' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import eventBus from '../eventBus';

export default {
  name: 'ProductsComponent',
  data() {
    return {
      products: []
    }
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('/products/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      }).then(response => {
        this.products = response.data;
      }).catch(error => {
        console.error('Error fetching products', error);
      });

      eventBus.on('product-purchased', this.updateStock);
    }
  },
  methods: {
    getImageUrl(image) {
      return `${image}`; // Обновите путь в зависимости от вашего каталога медиа файлов
    },
    addToCart(product) {
      let cart = localStorage.getItem('cart');
      cart = cart ? JSON.parse(cart) : [];
      const existingProduct = cart.find(item => item.id === product.id);
      if (existingProduct) {
        existingProduct.quantity++;
      } else {
        cart.push({...product, quantity: 1});
      }
      localStorage.setItem('cart', JSON.stringify(cart));
      this.$emit('update-cart', cart);
      eventBus.emit('cart-updated', cart);
    },
    updateStock({id, quantity}) {
      const product = this.products.find(p => p.id === id);
      if (product) {
        product.stock -= quantity;
      }
    }
  },
  beforeUnmount() {
    eventBus.off('product-purchased', this.updateStock);
  }
}
</script>

<style scoped>
.card-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.stock-info {
  height: 24px; /* высота текста с наличием */
  margin-bottom: 10px; /* отступ между текстом и кнопкой */
}

.btn-block {
  margin-top: auto;
}
</style>
