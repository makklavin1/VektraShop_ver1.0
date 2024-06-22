<template>
  <div class="cart" @mouseenter="expandCart" @mouseleave="shrinkCart">
    <div class="cart-icon-container">
      <i class="fas fa-shopping-cart cart-icon"></i>
      <span class="cart-count" v-if="totalItems">{{ totalItems }}</span>
    </div>
    <transition name="fade">
      <div v-if="expanded" class="cart-details p-3">
        <h5>Корзина</h5>
        <div v-for="item in cartItems" :key="item.id" class="cart-item d-flex justify-content-between align-items-center mb-2">
          <div>
            <p class="mb-0">{{ item.name }}</p>
            <small>{{ item.price }} x {{ item.quantity }}</small>
          </div>
          <div class="cart-item-controls">
            <button class="btn btn-sm btn-outline-secondary" @click="decreaseQuantity(item)">-</button>
            <button class="btn btn-sm btn-outline-secondary" @click="increaseQuantity(item)">+</button>
            <button class="btn btn-sm btn-danger" @click="removeItem(item)">Удалить</button>
          </div>
        </div>
        <button class="btn btn-primary btn-block mt-3" @click="checkout">Оформить заказ</button>
      </div>
    </transition>
    <transition name="fade">
      <div v-if="showSuccessPopup" class="overlay">
        <div class="popup success-popup">
          <p>Заказ успешно оформлен</p>
          <button class="btn btn-primary btn-block" @click="goToProfile">Личный кабинет</button>
        </div>
      </div>
    </transition>
    <transition name="fade">
      <div v-if="showErrorPopup" class="overlay">
        <div class="popup error-popup">
          <p>{{ errorMessage }}</p>
          <button class="btn btn-primary btn-block" @click="showErrorPopup = false">Закрыть</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import eventBus from '../eventBus';

export default {
  name: 'CartComponent',
  data() {
    return {
      cartItems: [],
      expanded: false,
      iconLoaded: false,
      showSuccessPopup: false,
      showErrorPopup: false,
      errorMessage: ''
    }
  },
  computed: {
    totalItems() {
      return this.cartItems.reduce((sum, item) => sum + item.quantity, 0);
    }
  },
  created() {
    this.loadCart();
    eventBus.on('cart-updated', this.loadCart);
  },
  methods: {
    loadCart() {
      let cart = localStorage.getItem('cart');
      this.cartItems = cart ? JSON.parse(cart) : [];
    },
    expandCart() {
      this.expanded = true;
    },
    shrinkCart() {
      this.expanded = false;
    },
    checkout() {
      axios.post('/users/checkout/', {
        cart_items: this.cartItems
      }, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`
        }
      }).then(() => {
        this.cartItems = [];
        this.saveCart();
        eventBus.emit('cart-updated');
        this.showSuccessPopup = true;
      }).catch(error => {
        console.error(error);
        this.errorMessage = error.response.data.error || 'Purchase failed!';
        this.showErrorPopup = true;
      });
    },
    removeItem(item) {
      this.cartItems = this.cartItems.filter(cartItem => cartItem.id !== item.id);
      this.saveCart();
      eventBus.emit('cart-updated');
    },
    increaseQuantity(item) {
      item.quantity++;
      this.saveCart();
      eventBus.emit('cart-updated');
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity--;
      } else {
        this.removeItem(item);
      }
      this.saveCart();
      eventBus.emit('cart-updated');
    },
    saveCart() {
      localStorage.setItem('cart', JSON.stringify(this.cartItems));
    },
    goToProfile() {
      this.$router.push('/profile');
      this.showSuccessPopup = false;
    }
  },
  watch: {
    cartItems: {
      handler() {
        this.saveCart();
      },
      deep: true
    }
  },
  beforeUnmount() {
    eventBus.off('cart-updated', this.loadCart);
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

.cart-icon-container {
  position: relative;
}

.cart-icon {
  font-size: 36px;
  color: orange;
}

.cart-count {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: black;
  color: white;
  border-radius: 12px;
  padding: 2px 6px;
  font-size: 14px;
  display: inline-block;
  min-width: 24px;
  text-align: center;
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

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s;
}

.success-popup {
  border: 2px solid green;
}

.error-popup {
  border: 2px solid red;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
