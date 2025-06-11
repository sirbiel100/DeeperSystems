// apiService.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',  // Point to your backend
  timeout: 5000
})

export default {
  getUsers() {
    return api.get('/users')
  },
  getUser(id) {
    return api.get(`/users/${id}`)
  },
  createUser(user) {
    return api.post('/users', user)
  },
  updateUser(id, user) {
    return api.patch(`/users/${id}`, user)
  },
  deleteUser(id) {
    return api.delete(`/users/${id}`)
  }
}