
import type { Defu } from 'defu'


declare const inlineConfig = {
  "firebaseConfig": {
    "apiKey": ""
  },
  "vuefireOptions": {
    "optionsApiPlugin": false,
    "config": {
      "apiKey": ""
    }
  }
}
type ResolvedAppConfig = Defu<typeof inlineConfig, []>

declare module 'nuxt/schema' {
  interface AppConfig extends ResolvedAppConfig { }
}
