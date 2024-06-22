<template>
  <div class="profile">
    <h1 class="display-4 mb-4"></h1>
    <nav class="nav nav-tabs">
      <router-link class="nav-item nav-link" :to="{ name: 'balance' }">Balance and Cards</router-link>
      <router-link class="nav-item nav-link" :to="{ name: 'activeOrders' }">Active Orders</router-link>
      <router-link class="nav-item nav-link" :to="{ name: 'purchaseHistory' }">Purchase History</router-link>
    </nav>
    <div class="profile-content mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile'
}
</script>

<style scoped>
.profile {
  max-width: 900px;
  margin: 0 auto;
}
.nav-tabs .nav-item {
  cursor: pointer;
}
.profile-content {
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
</style>
