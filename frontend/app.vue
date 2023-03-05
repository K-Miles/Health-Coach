<template>
  <div class="font-serif bg-lime-900 min-h-screen">
    <Navbar />
    <NuxtPage />
  </div>
</template>

<script setup>

const router = useRouter()
const route = useRoute()
const user = useCurrentUser()

// we don't need this watcher on server
onMounted(() => {
  watch(user, (user, prevUser) => {
    console.log(user)
    if (prevUser && !user) {
      // user logged out
      router.push('/login')
    } else if (user && typeof route.query.redirect === 'string') {
      // user logged in
      router.push(route.query.redirect)
    } else if (!user) {
      if (route.name != "register") {
        router.push('/login')
      }
    }
  })
})
</script>