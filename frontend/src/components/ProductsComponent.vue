<template>
  <div>
    <h1 class="display-4 mb-4">Products</h1>
    <div class="row">
      <div class="col-md-4 mb-4" v-for="product in products" :key="product.id">
        <div class="card h-100">
          <img :src="getImageUrl(product.image)" class="card-img-top" alt="Product image">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="card-text">{{ product.price }}</p>
            <button class="btn btn-primary btn-block" @click="addToCart(product)">Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductsComponent',
  data() {
    return {
      products: []
    }
  },
  created() {
    const token = localStorage.getItem('token');
    axios.get('products/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    }).then(response => {
      this.products = response.data;
    }).catch(error => {
      console.error('Error fetching products', error);
      if (error.response.status === 401) {
        this.$router.push('/login');
      }
    });
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
    }
  }
}
</script>

<style scoped>
/* Ваши стили здесь */
</style>
