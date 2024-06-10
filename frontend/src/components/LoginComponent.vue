<template>
  <div class="login">
    <h1 class="display-4 mb-4">Login</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <input type="text" class="form-control" v-model="username" placeholder="Username" />
      </div>
      <div class="form-group">
        <input type="password" class="form-control" v-model="password" placeholder="Password" />
      </div>
      <button type="submit" class="btn btn-primary btn-block">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import eventBus from '../eventBus'; // Импорт шины событий

export default {
  name: 'LoginComponent',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      axios.post('/users/login/', {
        username: this.username,
        password: this.password
      })
          .then(response => {
            localStorage.setItem('token', response.data.token);
            eventBus.emit('user-authenticated'); // Вызов события аутентификации пользователя
            this.$router.push('/');
          })
          .catch(error => {
            console.error('Login failed', error);
            alert('Login failed!');
          });
    }
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 1em;
  border-radius: 5px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login h1 {
  margin-bottom: 1em;
}
</style>
