<script setup>
import { ref, onMounted } from 'vue'
import { useConfirm } from "primevue/useconfirm"
import { useToast } from "primevue/usetoast"
import { format } from 'date-fns'
import api from '@/services/apiService'
import UserFormModal from '@/components/UserFormModal.vue'

const confirm = useConfirm()
const toast = useToast()
const users = ref([])
const isModalVisible = ref(false)
const selectedUser = ref(null)
const tableFirst = ref(0)

onMounted(async () => {
    await loadUsers()
})

const loadUsers = async () => {
    try {
        const response = await api.getUsers()
        users.value = response.data
    } catch (error) {
        console.error("Error fetching users:", error)
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load users', life: 3000 })
    }
}

const openCreateModal = () => {
    selectedUser.value = null
    isModalVisible.value = true
}

const openEditModal = (user) => {
    selectedUser.value = user
    isModalVisible.value = true
}

const closeModal = () => {
    isModalVisible.value = false
}

const handleSave = async () => {
    await loadUsers()
    tableFirst.value = 0
    isModalVisible.value = false
}

const deleteUser = (userId) => {
    confirm.require({
        message: 'Are you sure you want to delete this user?',
        header: 'Delete Confirmation',
        accept: async () => {
            try {
                await api.deleteUser(userId)
                users.value = users.value.filter(u => u._id !== userId)
                tableFirst.value = 0
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
    <div class="users-container">
        <ConfirmDialog />
        <Toast position="top-right" />

        <div class="card">
            <div class="table-header">
                <h2 class="page-title">
                    <i class="pi pi-users" style="margin-right: 0.5rem"></i>
                    User Management
                </h2>
                <Button label="Create New User" icon="pi pi-plus" class="create-button"
                    @click="() => openCreateModal()" />
            </div>

            <DataTable 
            class="p-datatable-striped user-table"
            :value="users" 
            :key="users.length"
            :totalRecords="users.length"
            responsiveLayout="scroll"
            :paginator="true"
            :rows="10"
            :first="tableFirst"
            @page="(e) => tableFirst = e.first"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport
                RowsPerPageDropdown"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords} users"
            >
                <Column field="username" header="Username" headerClass="table-header" bodyClass="table-cell">
                    <template #body="{ data }">
                        <router-link :to="`/users/${data._id}`" class="user-link">
                            <i class="pi pi-user" style="margin-right: 0.5rem"></i>
                            {{ data.username }}
                        </router-link>
                    </template>
                </Column>

                <Column field="roles" header="Roles" headerClass="table-header" bodyClass="table-cell">
                    <template #body="{ data }">
                        <div class="roles-container">
                            <span class="empty-value">{{ data.roles?.join(', ') || '—' }}</span>
                        </div>
                    </template>
                </Column>

                <Column field="timezone" header="Timezone" headerClass="table-header" bodyClass="table-cell">
                    <template #body="{ data }">
                        <div class="timezone-container">
                            <i class="pi pi-clock" style="margin-right: 0.5rem"></i>
                            <span class="timezone-badge">
                                {{ data.preferences.timezone || '—' }}
                            </span>
                        </div>
                    </template>
                </Column>

                <Column field="isActive" header="Status" headerClass="table-header" bodyClass="table-cell">
                    <template #body="{ data }">
                        <div class="status-container">
                            <i class="pi pi-circle-fill"
                                :style="{ color: data.active ? '#4CAF50' : '#F44336', fontSize: '0.75rem', marginRight: '0.5rem' }"></i>
                            <span :style="{ color: data.active ? '#4CAF50' : '#F44336', fontWeight: '600' }">
                                {{ data.active ? 'Active' : 'Inactive' }}
                            </span>
                        </div>
                    </template>
                </Column>

                <Column field="updatedAt" header="Last Updated" headerClass="table-header" bodyClass="table-cell">
                    <template #body="{ data }">
                        <div class="timestamp-container">
                            <i class="pi pi-calendar" style="margin-right: 0.5rem"></i>
                            <span class="timestamp">
                                {{ format(new Date(data.updated_ts), 'yyyy-MM-dd HH:mm') }}
                            </span>
                        </div>
                    </template>
                </Column>

                <Column field="createdAt" header="Created At" headerClass="table-header" bodyClass="table-cell">
                    <template #body="{ data }">
                        <div class="timestamp-container">
                            <i class="pi pi-calendar" style="margin-right: 0.5rem"></i>
                            <span class="timestamp">
                                {{ format(new Date(data.created_ts), 'yyyy-MM-dd HH:mm') }}
                            </span>
                        </div>
                    </template>
                </Column>

                <Column header="Actions" headerClass="table-header" bodyClass="table-cell" style="min-width: 150px">
                    <template #body="{ data }">
                        <div class="actions-container">
                            <Button icon="pi pi-pencil"
                                class="p-button-rounded p-button-text p-button-success edit-button"
                                v-tooltip.top="'Edit user'" @click="() => openEditModal(data)">
                                Edit
                            </Button>
                            <Button icon="pi pi-trash"
                                class="p-button-rounded p-button-text p-button-danger delete-button"
                                v-tooltip.top="'Delete user'" @click="() => deleteUser(data._id)">
                                Delete
                            </Button>
                        </div>
                    </template>
                </Column>
            </DataTable>
        </div>

        <UserFormModal :visible="isModalVisible" :user="selectedUser" @close="closeModal" @save="handleSave" />
    </div>
</template>

<style scoped>
.users-container {
    padding: 2rem;
    background-color: #f8f9fa;
    min-height: 100vh;
}

.card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 2rem;
}

.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e0e0e0;
}

.page-title {
    color: #2c3e50;
    margin: 0;
    font-size: 1.75rem;
    font-weight: 700;
    display: flex;
    align-items: center;
}

.create-button {
    background-color: #4CAF50;
    border: none;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.create-button:hover {
    background-color: #3d8b40;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.user-table {
    font-size: 0.95rem;
}

.user-table :deep() .p-datatable-thead>tr>th {
    background-color: #f5f7fa;
    color: #4a5568;
    font-weight: 700;
    padding: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.8rem;
    width: clamp(100px, 80px + 15vw, 250px);
}

.user-table :deep() .p-datatable-tbody>tr>td {
    padding: 1.25rem 1rem;
    vertical-align: middle;
    border-color: #edf2f7 !important;
}

.user-table :deep() .p-datatable-tbody>tr:hover>td {
    background-color: #f8fafc !important;
}

.user-link {
    color: #4299e1;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
}

.user-link:hover {
    cursor: pointer;
    color: #2b6cb0;
    text-decoration: underline;
}

.roles-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.role-tag {
    background-color: #e2e8f0;
    color: #2d3748;
    font-weight: 500;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
}

.timezone-container {
    display: flex;
    align-items: center;
}

.timezone-badge {
    background-color: #ebf8ff;
    color: #3182ce;
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
}

.status-container {
    display: flex;
    align-items: center;
}

.timestamp-container {
    display: flex;
    align-items: center;
}

.timestamp {
    color: #718096;
    font-size: 0.9rem;
}

.empty-value {
    color: #a0aec0;
    font-style: italic;
}

.actions-container {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
}

.edit-button {
    color: #48bb78 !important;
    background-color: #f0fff4 !important;
    transition: all 0.2s ease;
    border: none;
}

.edit-button:hover {
    background-color: #c6f6d5 !important;
    transform: scale(1.1);
}

.delete-button {
    color: #f56565 !important;
    background-color: #fff5f5 !important;
    transition: all 0.2s ease;
    border: none;
}

.delete-button:hover {
    background-color: #fed7d7 !important;
    transform: scale(1.1);
}



/* Responsive adjustments */
@media screen and (max-width: 960px) {
    .users-container {
        padding: 1rem;
    }

    .card {
        padding: 1.5rem;
    }

    .table-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1.5rem;
    }

    .create-button {
        width: 100%;
    }
}

/* Pagination styling */
:deep() .p-paginator {
    padding: 1rem;
    background: transparent;
    border: none;
}

:deep() .p-paginator .p-paginator-pages .p-paginator-page.p-highlight {
    background: #4299e1;
    border-color: #4299e1;
    color: white;
}

:deep() .p-paginator {
    padding: 1.5rem 1rem;
    background: transparent;
    border-top: 1px solid #edf2f7;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

:deep() .p-paginator .p-paginator-current {
    color: #718096;
    font-size: 0.9rem;
    background: #f8fafc;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 500;
}

:deep() .p-paginator .p-paginator-pages .p-paginator-page {
    min-width: 2.5rem;
    height: 2.5rem;
    margin: 0 0.15rem;
    border-radius: 8px;
    transition: all 0.2s ease;
    color: #4a5568;
    font-weight: 600;
    border: 1px solid transparent;
}

:deep() .p-paginator .p-paginator-pages .p-paginator-page:hover {
    background: #ebf8ff !important;
    color: #4299e1 !important;
    border: 1px solid #bee3f8;
}

:deep() .p-paginator .p-paginator-pages .p-paginator-page.p-highlight {
    background: #4299e1 !important;
    border-color: #4299e1 !important;
    color: white !important;
    box-shadow: 0 2px 5px rgba(66, 153, 225, 0.3);
}

:deep() .p-paginator .p-paginator-first,
:deep() .p-paginator .p-paginator-prev,
:deep() .p-paginator .p-paginator-next,
:deep() .p-paginator .p-paginator-last {
    min-width: 2.5rem;
    height: 2.5rem;
    margin: 0 0.15rem;
    border-radius: 8px;
    transition: all 0.2s ease;
    color: #4a5568;
    border: 1px solid #e2e8f0;
}

:deep() .p-paginator .p-paginator-first:hover,
:deep() .p-paginator .p-paginator-prev:hover,
:deep() .p-paginator .p-paginator-next:hover,
:deep() .p-paginator .p-paginator-last:hover {
    background: #ebf8ff !important;
    color: #4299e1 !important;
    border: 1px solid #bee3f8;
}

:deep() .p-paginator .p-dropdown {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    height: 2.5rem;
}

:deep() .p-paginator .p-dropdown .p-dropdown-label {
    padding: 0.5rem 1rem;
    color: #4a5568;
    font-weight: 500;
}

:deep() .p-paginator .p-dropdown .p-dropdown-trigger {
    width: 2rem;
}

:deep() .p-paginator .p-dropdown:hover {
    border-color: #bee3f8;
}

:deep() .p-paginator .p-dropdown-panel {
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
}

:deep() .p-paginator .p-dropdown-items .p-dropdown-item {
    padding: 0.5rem 1rem;
    color: #4a5568;
    transition: all 0.2s ease;
}

:deep() .p-paginator .p-dropdown-items .p-dropdown-item:hover {
    background: #ebf8ff;
    color: #4299e1;
}

:deep() .p-paginator .p-dropdown-items .p-dropdown-item.p-highlight {
    background: #ebf8ff;
    color: #4299e1;
    font-weight: 600;
}

/* Responsive pagination */
@media (max-width: 768px) {
    :deep() .p-paginator {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }

    :deep() .p-paginator-left-content {
        order: 2;
        width: 100%;
        justify-content: center;
    }

    :deep() .p-paginator-right-content {
        order: 1;
        width: 100%;
        justify-content: center;
    }

    :deep() .p-paginator .p-dropdown {
        width: 100%;
    }
}
</style>
