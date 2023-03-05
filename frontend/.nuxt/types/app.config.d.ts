
import type { Defu } from 'defu'


declare const inlineConfig = {
  "firebaseConfig": {
    "apiKey": "AIzaSyCVwldFBQ2GFWWVKjoyjTwsWkZwixzBt7I",
    "authDomain": "health-coach-e6d72.firebaseapp.com",
    "projectId": "health-coach-e6d72",
    "storageBucket": "health-coach-e6d72.appspot.com",
    "messagingSenderId": "975650633087",
    "appId": "1:975650633087:web:1241fa33baa8b48f87d64a"
  },
  "vuefireOptions": {
    "optionsApiPlugin": false,
    "config": {
      "apiKey": "AIzaSyCVwldFBQ2GFWWVKjoyjTwsWkZwixzBt7I",
      "authDomain": "health-coach-e6d72.firebaseapp.com",
      "projectId": "health-coach-e6d72",
      "storageBucket": "health-coach-e6d72.appspot.com",
      "messagingSenderId": "975650633087",
      "appId": "1:975650633087:web:1241fa33baa8b48f87d64a"
    },
    "auth": true
  }
}
type ResolvedAppConfig = Defu<typeof inlineConfig, []>

declare module 'nuxt/schema' {
  interface AppConfig extends ResolvedAppConfig { }
}
