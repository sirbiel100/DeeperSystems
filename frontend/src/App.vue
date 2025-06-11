<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
.p-dialog {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  max-width: 600px;
  width: 95%;
  background-color: #ffff;
}

.p-dialog-header-icon {
  display: none;
}

/* Header Style */
.p-dialog-header {
  background-color: #eff6ff;
  /* soft blue */
  color: #1e3a8a;
  font-weight: 600;
  font-size: 1.25rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dbeafe;
}

/* Content Area */
.p-dialog .p-dialog-content {
  padding: 1.5rem;
  font-size: 1rem;
  color: #1f2937;
}

.p-fluid{
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Footer */
.p-dialog-footer {
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1em;
}

.p-field-checkbox{
  display: flex;
  align-items: center;
}

/* Buttons */
.p-dialog .p-button {
  border: none;
  font-weight: 500;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.p-dialog .p-button.p-button-text {
  background-color: #e5e7eb;
  color: #1f2937;
}

.p-dialog .p-button.p-button-text:hover {
  background-color: #d1d5db;
}

.p-dialog .p-button.p-button-text.p-button-success {
  background-color: #10b981;
  color: white;
}

.p-dialog .p-button.p-button-text.p-button-success:hover {
  background-color: #059669;
}

/* Form Fields */
.p-field label {
  font-weight: 600;
  display: block;
  color: #374151;
  /* gray-700 */
}

.p-inputtext,
.p-password-input,
.p-dropdown {
  width: 50%;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  padding: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.p-password {
  display: flex;
  align-items: center;
  gap: 1em;
}

.p-inputtext:focus,
.p-password-input:focus,
.p-dropdown:focus {
  border-color: #3b82
}
</style>