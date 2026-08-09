<script setup>
const { signOut } = useAuth()
async function handleSignOut() {
  await signOut({
    callbackUrl: '/login',
    redirect: true
  })
}
</script>

<template>
  <UContainer>
    <h1>Logout</h1>
    <UButton @click="handleSignOut">Sign Out</UButton>
  </UContainer>
</template>
