<template>
  <div class="cart" @mouseenter="expandCart" @mouseleave="shrinkCart">
    <i class="fas fa-shopping-cart fa-2x" v-if="!iconLoaded" @load="iconLoaded = true"></i>
    <i v-else class="fas fa-shopping-cart fa-2x"></i>
    <transition name="fade">
      <div v-if="expanded" class="cart-details p-3">
        <h5>Cart</h5>
        <div v-for="item in localCartItems" :key="item.id" class="cart-item d-flex justify-content-between align-items-center mb-2">
          <div>
            <p class="mb-0">{{ item.name }}</p>
            <small>{{ item.price }} x {{ item.quantity }}</small>
          </div>
          <div class="cart-item-controls">
            <button class="btn btn-sm btn-outline-secondary" @click="decreaseQuantity(item)">-</button>
            <button class="btn btn-sm btn-outline-secondary" @click="increaseQuantity(item)">+</button>
            <button class="btn btn-sm btn-danger" @click="removeItem(item)">Remove</button>
          </div>
        </div>
        <button class="btn btn-primary btn-block mt-3" @click="checkout">Checkout</button>
      </div>
      <div v-else class="cart-summary">
        <p class="mb-0">{{ localCartItems.length }}</p>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import eventBus from '../eventBus'; // Импорт шины событий

export default {
  name: 'CartComponent',
  props: {
    cartItems: Array
  },
  data() {
    return {
      localCartItems: [...this.cartItems],
      expanded: false,
      iconLoaded: false
    }
  },
  watch: {
    cartItems: {
      handler(newVal) {
        this.localCartItems = [...newVal];
      },
      deep: true
    }
  },
  methods: {
    expandCart() {
      this.expanded = true;
    },
    shrinkCart() {
      this.expanded = false;
    },
    checkout() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('You must be logged in to checkout');
        return;
      }

      axios.post('/users/checkout/', {
        cart_items: this.localCartItems
      }, {
        headers: {
          'Authorization': `Token ${token}`
        }
      }).then(() => {
        alert('Purchase successful!');
        this.localCartItems = [];
        this.saveCart();
        eventBus.emit('cart-updated'); // Вызов события обновления корзины
        this.$router.push('/profile');
      }).catch(error => {
        console.error('Error during checkout', error);
        alert('Purchase failed!');
      });
    },
    removeItem(item) {
      this.localCartItems = this.localCartItems.filter(cartItem => cartItem.id !== item.id);
      this.saveCart();
      eventBus.emit('cart-updated'); // Вызов события обновления корзины
    },
    increaseQuantity(item) {
      item.quantity++;
      this.saveCart();
      eventBus.emit('cart-updated'); // Вызов события обновления корзины
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity--;
      } else {
        this.removeItem(item);
      }
      this.saveCart();
      eventBus.emit('cart-updated'); // Вызов события обновления корзины
    },
    saveCart() {
      localStorage.setItem('cart', JSON.stringify(this.localCartItems));
    }
  }
}
</script>

<style scoped>
.cart {
  position: fixed;
  bottom: 20px;
  right: 20px;
  border-radius: 50%;
  background-color: #f2f2f2;
  padding: 10px;
  cursor: pointer;
}
.cart .cart-details {
  position: absolute;
  bottom: 50px;
  right: 0;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
  z-index: 1000;
  opacity: 1;
  transform: translateY(0);
}

.cart-summary {
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cart-item-controls button {
  margin-left: 5px;
}
</style>
