import { createRouter, createWebHistory } from 'vue-router';
import ProductsComponent from '@/components/ProductsComponent.vue';
import ProfileComponent from '@/components/ProfileComponent.vue';
import StatsComponent from '@/components/StatsComponent.vue';
import LoginComponent from '@/components/LoginComponent.vue';
import ActiveOrdersComponent from '@/components/ActiveOrdersComponent.vue';

const routes = [
  {
    path: '/',
    name: 'ProductsComponent',
    component: ProductsComponent
  },
  {
    path: '/profile',
    name: 'ProfileComponent',
    component: ProfileComponent
  },
  {
    path: '/stats',
    name: 'StatsComponent',
    component: StatsComponent
  },
  {
    path: '/login',
    name: 'LoginComponent',
    component: LoginComponent
  },
  {
    path: '/orders',
    name: 'ActiveOrdersComponent',
    component: ActiveOrdersComponent
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
