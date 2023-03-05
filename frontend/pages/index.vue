<script setup>
import quotes from "@/public/quotes.json" // https://gist.github.com/Sacristan/3cdc5db13184df250349467e7a568e28
const user = await getCurrentUser()
const quote = quotes.quotes[Math.floor(Math.random()*quotes.quotes.length)] // https://stackoverflow.com/questions/5915096/get-a-random-item-from-a-javascript-array
</script>

<template>
  <div class="container mt-10 p-4 bg-gray-100 rounded-md">
    <h1 class="h1">Welcome back {{ user.displayName ?? 'there' }},</h1>
    <p class="p font-sans italic">✨ {{ quote }}</p>
    <div class="mt-4 grid grid-cols-2">
      <NuxtLink to="/workout" class="bg-white rounded-md border-2 border-slate-300 text-center p-8 mr-2">
        <i class="text-lime-600 text-6xl fa-solid fa-dumbbell"></i>
        <h2 class="mt-4 h2">Work Out</h2>
      </NuxtLink>
      <NuxtLink to="/nutrition" class="bg-white rounded-md border-2 border-slate-300 text-center p-8">
        <i class="text-lime-600 text-6xl fa-solid fa-apple-whole"></i>
        <h2 class="mt-4 h2">Track Nutrition</h2>
      </NuxtLink>
    </div>
  </div>
</template>