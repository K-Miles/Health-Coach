<script setup>
const regenButton = ref(false)
const user = await getCurrentUser()

const resp = await useFetch('http://localhost:5001/workout_plan', {
   method: "POST",
   headers: {
      'Content-Type': 'application/json'
   },
   body: JSON.stringify({
      uid: user.uid
   })
})
const workoutData = ref(JSON.parse(resp.data.value.message))

// onMounted(() => {
   for (const data of workoutData.value) {
      for (const workout of data.workouts) {
         const { pending, data: data } = useLazyFetch('http://localhost:5001/videoSearch', {
            method: "POST",
            headers: {
               'Content-Type': 'application/json'
            },
            body: JSON.stringify({
               workout: workout.name
            })
         })
         watch(data, (newData) => {
            console.log(`update to ${newData.data}`)
            workout.video = newData.data
         })
      }
   }
// })

async function regenerate() {
   regenButton.value = true
   const resp = await useFetch('http://localhost:5001/regenerate', {
      method: "POST",
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         uid: user.uid
      })
   })
   workoutData.value = JSON.parse(resp.data.value.message)
   for (const data of workoutData.value) {
      for (const workout of data.workouts) {
         const resp = await useFetch('http://localhost:5001/videoSearch', {
            method: "POST",
            headers: {
               'Content-Type': 'application/json'
            },
            body: JSON.stringify({
               workout: workout.name
            })
         })
         workout.video = resp.data.value.data
      }
   }
   regenButton.value=false
}
</script>

<template>
  <div class="container mt-10 p-4 bg-gray-100 rounded-md">
   <div class="flex flex-row justify-between">
      <div>
         <h1 class="h1">Gym Schedule</h1>
         <p class="p font-sans">Based on what you told us, {{ user.displayName ?? "man" }}, here's what your AI coach reccomended:</p>
      </div>
      <div>
         <button @click="regenerate" class="mt-2 btn btn-primary bg-gray-100 rounded-full hover:bg-gray-200 active:bg-gray-300 border-none text-black"><i :class="(regenButton ? 'animate-spin ' : '') + 'fa-solid fa-arrows-rotate'"></i></button>
      </div>
   </div>
   <div :class="'mt-4 ' + (!regenButton ? 'grid grid-cols-1 xl:grid-cols-3' : '')">
      <div v-if="!regenButton" v-for="data of workoutData" class="bg-white rounded-md border-2 border-gray-300 p-4 mb-3 xl:mr-2">
         <h5 class="h5">Day {{ data.day }}: <b class="font-black">{{ data.focus }}</b></h5>
         <p class="text-sm text-gray-500 font-sans">Here's the plan for today:</p>
         <div v-for="workout of data.workouts" class="bg-slate-100 rounded-md border-2 border-slate-200 p-4 my-3 flex flex-row justify-between">
            <div class="my-auto"> 
               <h4 class="text-xl">{{ workout.name }}</h4>
               <p class="text-sm text-gray-500 font-sans">{{ workout.reps }} reps of {{ workout.sets }} sets</p>
            </div>
            <NuxtLink :to="workout.video ?? ''" target="_blank" class="text-slate-600 text-3xl bg-slate-300 p-2 rounded-md"><i class="mt-1.5 mx-1 fa-brands fa-youtube"></i></NuxtLink>
         </div>
      </div>
      <div v-else class="text-center">
         <h1 class="h1">Hang tight, {{ user.displayName ?? "man" }}.</h1>
         <p class="p font-sans">We're currently generating a brand new workout routine, just for you. This should take no longer than 20 seconds.</p>
      </div>
   </div>
  </div>
</template>