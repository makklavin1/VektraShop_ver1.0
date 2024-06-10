<template>
  <div class="profile">
    <h1 class="display-4 mb-4">Profile</h1>
    <div class="card p-3">
      <div class="card-body">
        <h5 class="card-title">Balance: {{ user.balance }}</h5>
        <p class="card-text">Red Cards: {{ user.red_cards }}</p>
        <p class="card-text">Yellow Cards: {{ user.yellow_cards }}</p>
        <h6 class="mt-4">Purchase History</h6>
        <ul class="list-group">
          <li class="list-group-item" v-for="history in user.purchase_history" :key="history.id">
            {{ history.product.name }} - {{ formatDate(history.date) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfileComponent',
  data() {
    return {
      user: {}
    }
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('users/profile/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      .then(response => {
        this.user = response.data;
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
  },
  methods: {
    formatDate(value) {
      if (value) {
        return new Date(value).toLocaleString();
      }
    }
  }
}
</script>

<style scoped>
.profile {
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

.list-group-item {
  background-color: #fff;
  border: none;
  border-bottom: 1px solid #ddd;
}

.list-group-item:last-child {
  border-bottom: none;
}
</style>
