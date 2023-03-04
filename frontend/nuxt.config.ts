// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      link: [
        {
          href: "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
          rel: "stylesheet",
          integrity: "sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3",
          crossorigin: "anonymous",
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
    }
  }
})
