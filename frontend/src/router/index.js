import { createRouter, createWebHistory } from 'vue-router'
import UsersView from '../views/UsersView.vue'
import UserView from '../views/UserView.vue'

const routes = [
  {
    path: '/',
    name: 'users',
    component: UsersView
  },
  {
    path: '/users/:id',
    name: 'user',
    component: UserView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router