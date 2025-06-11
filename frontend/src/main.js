import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'

import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'

import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog';
import Column from 'primevue/column'

const app = createApp(App)

app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)
app.use(router)

app.component('Toast', Toast)
app.component('ConfirmDialog', ConfirmDialog)
app.component('Button', Button)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog);

app.mount('#app')
