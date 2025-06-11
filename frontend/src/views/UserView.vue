<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useConfirm } from "primevue/useconfirm"
import axios from 'axios'
import api from '@/services/apiService'
import UserFormModal from '@/components/UserFormModal.vue'

const route = useRoute()
const user = ref(null)
const selectedUser = ref(null)
const isModalVisible = ref(false)
const confirm = useConfirm()

onMounted(async () => {
  const response = await api.getUser(route.params.id)
  user.value = response.data
})

function formatDate(timestamp) {
  if (!timestamp) return '—'
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(timestamp).toLocaleString(undefined, options)
}

const openEditModal = (user) => {
  selectedUser.value = user
  isModalVisible.value = true
}

const closeModal = () => {
    isModalVisible.value = false
}


const deleteUser = (userId) => {
  confirm.require({
    message: 'Are you sure you want to delete this user?',
    header: 'Delete Confirmation',
    accept: async () => {
      try {
        await api.deleteUser(userId)
        toast.add({ severity: 'success', summary: 'Success', detail: 'User deleted', life: 3000 })
      } catch (error) {
        console.error("Error deleting user:", error)
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete user', life: 3000 })
      }
    }
  })
}

</script>

<template>
  <div class="user-view">
    <ConfirmDialog />
    <div v-if="user" class="user-card">
      <h2 class="username">{{ user.username }}</h2>
      <ul class="user-details">
        <li>
          <strong>Roles:</strong>
          <span>{{ user.roles?.length ? user.roles.join(', ') : '—' }}</span>
        </li>
        <li>
          <strong>Status:</strong>
          <span>{{ (user.active ? "Active" : "Inactive") }}</span>
        </li>
        <li>
          <strong>Created At:</strong>
          <span>{{ formatDate(user.created_ts) }}</span>
        </li>
        <li>
          <strong>Updated At:</strong>
          <span>{{ formatDate(user.updated_ts) }}</span>
        </li>
        <li>
          <strong>Timezone:</strong>
          <span>{{ user.preferences.timezone }}</span>
        </li>
      </ul>


      <div class="actions-container">
        <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-success edit-button"
          v-tooltip.top="'Edit user'" @click="() => openEditModal(user)">
          Edit
        </Button>
        <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger delete-button"
          v-tooltip.top="'Delete user'" @click="() => deleteUser(user._id)">
          Delete
        </Button>
      </div>

    </div>
    <div v-else class="loading">
      Loading user data...
    </div>

    <UserFormModal :visible="isModalVisible" :user="selectedUser" @close="closeModal" @save="handleSave" />
  </div>
</template>

<style scoped>

.user-view {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f7f9fc;
  padding: 20px;
}

.user-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  padding: 30px 40px;
  max-width: 400px;
  width: 100%;
  color: #333;
  transition: box-shadow 0.3s ease;
}

.user-card:hover {
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
}

.username {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 8px;
}

.user-details {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-details li {
  margin-bottom: 14px;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #e1e8ed;
  padding-bottom: 8px;
}

.user-details li strong {
  color: #555;
}

.loading {
  font-size: 1.3rem;
  color: #999;
  font-style: italic;
}

.actions-container {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
}

.edit-button {
  cursor: pointer;
  color: #48bb78 !important;
  background-color: #f0fff4 !important;
  transition: all 0.2s ease;
  border: none;
  padding: .8em 1.5em;
}

.edit-button:hover {
  background-color: #c6f6d5 !important;
  transform: scale(1.1);
}

.delete-button {
  cursor: pointer;
  color: #f56565 !important;
  background-color: #fff5f5 !important;
  transition: all 0.2s ease;
  border: none;
  padding: .8em 1.5em;
}

.delete-button:hover {
  background-color: #fed7d7 !important;
  transform: scale(1.1);
}
</style>
