<script setup>
const regenButton = ref("Regenerate")
const user = await getCurrentUser()
const food = ref("")
console.log(user.uid)
const resp = await useFetch('http://localhost:5001/account_info', {
   method: "POST",
   headers: {
      'Content-Type': 'application/json'
   },
   body: JSON.stringify({
      uid: user.uid
   })
})
console.log(resp.data.value)
const userData = ref(resp.data.value.data)

async function regenerate() {
   regenButton.value = "Regenerating..."
   const resp = await useFetch('http://localhost:5001/nutrition', {
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
    <h1 class="h1">Nutrition Journal</h1>
    <p class="p">{{ user.displayName ?? "Hiya" }}, keep track of your nutritional facts here. </p>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
      Add Meal
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Meal Info</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <input v-model="food" type="text" class="form-control-plaintext" placeholder="Enter food and amount"/>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
          </div>
        </div>
      </div>
    </div>
    <div v-for="meal of userData.nutritionLog" class="bg-white rounded-md border-2 border-gray-100 p-4">
      <h5 class="h5"></h5>
        <p>Name: {{ JSON.parse(meal) }}</p>
    </div>
  </div>
</template>