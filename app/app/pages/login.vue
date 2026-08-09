<!-- pages/login.vue -->
<script setup>
definePageMeta({
  auth: { unauthenticatedOnly: true, navigateAuthenticatedTo: '/' }
})

const { signIn } = useAuth()
const username = ref('')
const password = ref('')
const errorMessage = ref('')

async function handleLogin() {
  try {
    errorMessage.value = ''
    await signIn({ username: username.value, password: password.value }, { callbackUrl: '/' })
  } catch (err) {
    errorMessage.value = 'Invalid credentials. Please try again.'
  }
}
</script>

<template>
  <UContainer>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="username" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Sign In</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
  </UContainer>
</template>
