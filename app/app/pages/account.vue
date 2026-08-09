<script setup>
const { data: sessionData } = useAuth()
</script>

<template>
  <UContainer>
    <h1>Account</h1>
    {{ sessionData }}
  </UContainer>
</template>
