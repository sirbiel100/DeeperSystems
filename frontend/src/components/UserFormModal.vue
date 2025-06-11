<script setup>
import { ref, watch, computed } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';
import api from '@/services/apiService';
import InputSwitch from 'primevue/inputswitch';

const props = defineProps({
    user: Object,
    visible: Boolean
});

const emit = defineEmits(['close', 'save']);

const formData = ref({});
const submitted = ref(false);


const dialogHeader = computed(() =>
    props.user && props.user.id ? 'Edit User' : 'Create User'
);


watch(
    () => props.user,
    (newUser) => {
        formData.value = newUser
            ? { ...newUser, id: newUser._id }
            : {
                username: '',
                password: '',
                is_user_admin: false,
                is_user_manager: false,
                is_user_tester: false,
                user_timezone: '',
                is_user_active: true,
            };
        submitted.value = false;
    },
    { immediate: true } // Run immediately on component mount
);

const onSave = async () => {
    submitted.value = true;

    if (!formData.value.username || (!formData.value.id && formData.value.password.trim() === '')) {
        console.error("Validation failed: Username and Password are required for new users.");
        return;
    }

    const roles = [];
    if (formData.value.is_user_admin) roles.push('admin');
    if (formData.value.is_user_manager) roles.push('manager');
    if (formData.value.is_user_tester) roles.push('tester');

    const userPayload = {
        username: formData.value.username,
        password: formData.value.password,
        active: formData.value.is_user_active,
        preferences: {
            timezone: formData.value.user_timezone
        },
        roles
    };

    // Remove empty password on update
    if (formData.value.id && userPayload.password.trim() === '') {
        delete userPayload.password;
    }

    try {
        let response;
        if (formData.value.id) {
            response = await api.updateUser(formData.value.id, userPayload);
            console.log('User updated:', response.data);
        } else {
            response = await api.createUser(userPayload);
            console.log('User created:', response.data);
        }

        emit('save', response.data);
        closeModal();
    } catch (error) {
        console.error("Error saving user:", error);
    }
};


const closeModal = () => {
    emit('close');
};
</script>

<template>

    <Dialog :visible="visible" :modal="true" :header="dialogHeader" class="p-fluid" @update:visible="closeModal">
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeModal" />
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="onSave" />
        </template>

        <div class="p-fluid p-formgrid p-grid">
            <div class="p-field p-col-12 p-md-6">
                <label for="username">Username</label>
                <InputText id="username" v-model="formData.username" />
            </div>

            <div class="p-field p-col-12 p-md-6">
                <label for="password">Password</label>
                <Password id="password" v-model="formData.password" toggleMask :required="!formData.id" />
            </div>

            <div class="p-field p-col-12">
                <label>Roles</label>
                <div class="p-d-flex p-flex-wrap">
                    <div class="p-field-checkbox p-mr-4">
                        <Checkbox id="adminRole" v-model="formData.is_user_admin" :binary="true" />
                        <label for="adminRole">Admin</label>
                    </div>

                    <div class="p-field-checkbox p-mr-4">
                        <Checkbox id="managerRole" v-model="formData.is_user_manager" :binary="true" />
                        <label for="managerRole">Manager</label>
                    </div>

                    <div class="p-field-checkbox p-mr-4">
                        <Checkbox id="testerRole" v-model="formData.is_user_tester" :binary="true" />
                        <label for="testerRole">Tester</label>
                    </div>
                </div>
            </div>

            <div class="p-field-checkbox p-mr-4">
                <label for="activeSwitch">Active</label><br />
                <InputSwitch id="activeSwitch" v-model="formData.is_user_active" />
            </div>

            <div class="p-field p-col-12">
                <label for="timezone">Timezone</label>
                <InputText id="timezone" v-model="formData.user_timezone" placeholder="e.g., America/New_York" />
            </div>
        </div>
    </Dialog>
</template>
