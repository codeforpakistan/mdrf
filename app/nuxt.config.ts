// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@nuxt/eslint', '@nuxt/ui', '@sidebase/nuxt-auth'],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    baseURL: 'https://localhost:8000'
  },

  routeRules: {
    '/': { prerender: true }
  },

  compatibilityDate: '2026-06-30',

  auth: {
    baseURL: 'http://localhost:8000',
    provider: {
      type: 'local',
      endpoints: {
        signIn: { path: '/auth/app/v1/auth/login', method: 'post' },
        signOut: { path: '/auth/app/v1/auth/logout', method: 'post' },
        // signUp: { path: '/register', method: 'post' },
        getSession: { path: '/auth/app/v1/auth/session', method: 'get' }
      },
      pages: {
        login: '/login'
      },
      token: {
        signInResponseTokenPointer: '/meta/access_token',
        type: 'Bearer',
        headerName: 'Authorization',
        maxAgeInSeconds: 3600
      },
      session: {
        // Maps django-allauth user response properties to your frontend user object
        dataType: {
          id: 'string',
          email: 'string',
          username: 'string'
        },
        // Path in Django json response to find the user profile data
        dataResponsePointer: '/data/user'
      }
    },
    sessionRefresh: {
      enablePeriodically: true,
      enableOnWindowFocus: true,
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
