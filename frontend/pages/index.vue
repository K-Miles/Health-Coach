<script setup>
const user = await getCurrentUser()
</script>

<template>
  <div class="container mt-10 p-4 bg-gray-200 rounded-md">
    <h1 class="h1">Hi {{ user.displayName ?? 'there' }},</h1>
    <p class="p">What would you like to do today?</p>
    <div class="mt-4 grid grid-cols-2">
      <a href="/workout" class="bg-white rounded-md border-2 border-gray-100 text-center p-8 mr-2">
        <i class="text-blue-500 text-6xl fa-solid fa-dumbbell"></i>
        <h2 class="mt-4 h2">Work Out</h2>
      </a>
      <a href="/nutrition" class="bg-white rounded-md border-2 border-gray-100 text-center p-8">
        <i class="text-blue-500 text-6xl fa-solid fa-apple-whole"></i>
        <h2 class="mt-4 h2">Track Nutrition</h2>
      </a>
    </div>
  </div>
</template>