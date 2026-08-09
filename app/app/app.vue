<script setup lang="ts">
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.svg' }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})
const { data: sessionData } = useAuth()
const title = 'MDRF'
const description = 'Multi-Disaster Response Framework'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description
  // ogImage: 'https://ui.nuxt.com/assets/templates/nuxt/starter-light.png',
  // twitterCard: 'summary_large_image'
})

import type { NavigationMenuItem } from '@nuxt/ui'
const route = useRoute()
const items = computed<NavigationMenuItem[]>(() => [
  {
    label: 'Hazards',
    to: '/hazards',
    active: route.path.startsWith('/hazards')
  },
  {
    label: 'Disasters',
    to: '/disasters',
    active: route.path.startsWith('/disasters')
  },
  {
    label: 'Issues',
    to: '/issues',
    active: route.path.startsWith('/issues')
  },
  {
    label: 'Resources',
    to: '/resources',
    active: route.path.startsWith('/resources')
  }
])
</script>

<template>
  <UApp>
    <UHeader to="/">
      <template #title>MDRF</template>

      <UNavigationMenu :items="items" />

      <template #right>
        <UColorModeButton />
        <UButton
          to="/search"
          icon="line-md:search"
          color="neutral"
          variant="ghost"
        />
        <UButton
          to="/subscriptions"
          icon="line-md:bell"
          color="neutral"
          variant="ghost"
        />
        <template v-if="sessionData">
          <UButton
            to="/account"
            icon="line-md:account"
            color="neutral"
            variant="ghost"
          />
          <UButton
            to="/logout"
            icon="line-md:logout"
            color="neutral"
            variant="ghost"
          />
        </template>
        <template v-else>
          <UButton
            to="/login"
            icon="line-md:login"
            color="neutral"
            variant="ghost"
          />
        </template>
      </template>
    </UHeader>

    <UMain>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </UMain>

    <UFooter>
      <template #left>
        <p class="text-sm text-muted">
          Powered by <a target="_blank" href="https://codeforpakistan.org/">Code for Pakistan</a>
        </p>
      </template>

      <template #right>
        <UButton
          to="https://github.com/codeforpakistan/mdrf"
          target="_blank"
          icon="line-md:github"
          color="neutral"
          variant="ghost"
        />
      </template>
    </UFooter>
  </UApp>
</template>
