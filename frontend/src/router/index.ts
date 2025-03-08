import { createRouter, createWebHistory } from 'vue-router'
import PagamentosView from '@/views/PagamentosView.vue'
import PaymentDetailView from '@/views/PaymentDetailView.vue'
import PaymentFormView from '@/views/PaymentFormView.vue'
import Login from '@/views/Login.vue'
import axios from 'axios'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: '/payment-list',
      name: 'payments-list',
      component: PagamentosView,
    },
    { path: "/login", name: "Login", component: Login },
    { path: "/register", name: "Register", component: Register },
    {
      path: '/new-payment',
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


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({ name: "Login" });
    } else {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
      next();
    }
  } else {
    next();
  }
});

export default router
