<script setup>
const { data: sessionData } = useAuth()
</script>

<template>
  <UContainer>
    <h1>Welcome <span v-if="sessionData">{{ sessionData?.username }}</span></h1>
  </UContainer>
</template>
