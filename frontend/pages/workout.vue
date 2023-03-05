<script setup>
const regenButton = ref("Regenerate")
const user = await getCurrentUser()
console.log(user.uid)
const resp = await useFetch('http://localhost:5001/workout_plan', {
   method: "POST",
   headers: {
      'Content-Type': 'application/json'
   },
   body: JSON.stringify({
      uid: user.uid
   })
})
console.log(resp.data.value)
const workoutData = ref(JSON.parse(resp.data.value.message))
console.log(workoutData.value)

async function regenerate() {
   regenButton.value = "Regenerating..."
   const resp = await useFetch('http://localhost:5001/regenerate', {
      method: "POST",
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         uid: user.uid
      })
   })
   console.log(resp.data.value)
   workoutData.value = JSON.parse(resp.data.value.message)
   regenButton.value="Regenerate"
}
</script>

<template>
  <div class="container mt-2 p-4 bg-gray-200 rounded-md">
    <h1 class="h1">Gym Schedule</h1>
    <p class="p">Based on what you told us, {{ user.displayName ?? "man" }}, here's what we reccomend:</p>
    <button @click="regenerate" class="mt-2 btn btn-primary">{{ regenButton }}</button>
    <a class="mt-2 btn btn-primary ml" href="/profile">Edit Goals</a>
    <div class="mt-4 grid grid-cols-1">
      <div v-for="data of workoutData" class="bg-white rounded-md border-2 border-gray-100 p-4">
        <h5 class="h5">Day {{ data.day }}: <b>{{ data.focus }}</b></h5>
        <div v-for="workout of data.workouts" class="p">
          <p>Name: {{ workout.name }}</p>
          <p>Reps: {{ workout.reps }}</p>
          <p>Sets: {{ workout.sets }}</p>
        </div>
      </div>
    </div>
  </div>
</template>