<template>
  <div>
    <h5></h5>
    <div class="card p-3">
      <div class="card-body">
        <h5 class="card-title">Баланс: {{ user.balance }}</h5>
        <p class="card-text">Красные карточки: {{ user.red_cards }}</p>
        <p class="card-text">Желтые карточки: {{ user.yellow_cards }}</p>
        <div class="telegram-link" v-if="!user.telegram_chat_id">
          <a :href="telegramLink" target="_blank" class="btn btn-telegram">
            <i class="fab fa-telegram-plane"></i> Привязать Telegram
          </a>
        </div>
        <div class="telegram-linked" v-else>
          <p>Telegram привязан</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BalanceComponent',
  data() {
    return {
      user: {},
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

.telegram-link {
  margin-top: 20px;
}

.btn-telegram {
  display: inline-flex;
  align-items: center;
  padding: 0.5em 1em;
  border: none;
  background-color: #0088cc;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-telegram i {
  margin-right: 0.5em;
}

.btn-telegram:hover {
  background-color: #007ab8;
}

.telegram-linked {
  margin-top: 20px;
  color: green;
  font-weight: bold;
}
</style>
