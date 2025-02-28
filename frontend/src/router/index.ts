import { createRouter, createWebHistory } from 'vue-router'
import PagamentosView from '@/views/PagamentosView.vue'
import PaymentDetailView from '@/views/PaymentDetailView.vue'
import PaymentFormView from '@/views/PaymentFormView.vue'

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
      name: 'payment-form',
      component: PaymentFormView,
    },
    {
      path: '/pagamentos/detalhe/:id',
      name: 'PaymentDetail',
      component: PaymentDetailView,
    },
  ],
})

export default router
