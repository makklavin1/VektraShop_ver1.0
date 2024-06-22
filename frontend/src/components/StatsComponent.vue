<template>
  <div class="stats">
    <h1 class="display-4 mb-4"></h1>
    <div class="card p-3">
      <div class="card-body">
        <h6 class="mt-4">Статистика по компании</h6>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Имя</th>
              <th>Баланс</th>
              <th>Красные карточки</th>
              <th>Желтые карточки</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.balance }}</td>
              <td>{{ user.red_cards }}</td>
              <td>{{ user.yellow_cards }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StatsComponent',
  data() {
    return {
      users: []
    }
  },
  created() {
    axios.get('/users/stats/', {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    }).then(response => {
      this.users = response.data;
    }).catch(error => {
      console.error(error);
    });
  }
}
</script>

<style scoped>
.stats {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.table {
  margin-top: 20px;
}

.table th, .table td {
  text-align: center;
  vertical-align: middle;
}

.table th {
  background-color: #ff8c00;
  color: #fff;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(255, 140, 0, 0.1);
}
</style>
