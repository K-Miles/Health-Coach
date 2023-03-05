// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  app: {
    head: {
      link: [
        {
          href: "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css",
          rel: "stylesheet",
          integrity: "sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD",
          crossorigin: "anonymous",
        },
        {
          href: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css",
          rel: "stylesheet"
        }
      ],
      script: [
        {
          src: "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js",
          integrity: "sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN",
          crossorigin: "anonymous"
        }
      ]
    }
  },
  modules: ["@nuxtjs/tailwindcss", "nuxt-vuefire"],
  vuefire: {
    config: {
      apiKey: "AIzaSyCVwldFBQ2GFWWVKjoyjTwsWkZwixzBt7I",
      authDomain: "health-coach-e6d72.firebaseapp.com",
      projectId: "health-coach-e6d72",
      storageBucket: "health-coach-e6d72.appspot.com",
      messagingSenderId: "975650633087",
      appId: "1:975650633087:web:1241fa33baa8b48f87d64a"
    },
    auth: true
  }
})
