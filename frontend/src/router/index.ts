import { createRouter, createWebHistory } from 'vue-router'
import PagamentosView from '@/views/PagamentosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: PagamentosView,
    },
    {
      path: '/payment-form',
      name: 'about',
      component: () => import('../views/PaymentFormView.vue'),
    },
  ],
})

export default router
