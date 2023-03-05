<script setup>
const loadingNewFood = ref(false)
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

const userData = ref(resp.data.value.data)

async function addFood() {
  loadingNewFood.value = true
  const resp = await useFetch('http://localhost:5001/nutrition', {
    method: "POST",
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        uid: user.uid,
        food: food.value
    })
  })
  loadingNewFood.value = false
  userData.value.nutritionLog.push({
    foodData: resp.data.value.data,
    time: new Date().toISOString()
  })
}
</script>

<template>
  <div class="container mt-10 p-4 bg-gray-100 rounded-md">
    <div class="flex flex-row justify-between">
      <div>
         <h1 class="h1">Nutrition Journal</h1>
         <p class="p font-sans">{{ user.displayName ?? "Hiya" }}, keep track of your nutritional data here:</p>
      </div>
      <div>
         <button type="button" data-bs-toggle="modal" data-bs-target="#addFood" class="mt-2 btn btn-primary bg-gray-100 rounded-full hover:bg-gray-200 active:bg-gray-300 border-none text-black"><i class="fa-solid fa-plus"></i></button>
      </div>
   </div>

    <div class="modal fade" id="addFood" tabindex="-1" aria-labelledby="addFood" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Meal Info</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body font-sans">
            <input v-model="food" type="text" class="form-control font-sans" placeholder="Enter food in natural language..."/>
            <p class="text-xs ml-1 mt-1 text-gray-500">We use AI to calculate a rough estimate of nutritional data. This will take ~10 seconds.</p>
          </div>
          <div class="modal-footer font-sans">
            <button type="button" class="btn btn-secondary bg-gray-500" data-bs-dismiss="modal">Close</button>
            <button @click="addFood" type="button" class="btn btn-success bg-lime-700" data-bs-dismiss="modal">Add</button>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4 grid grid-cols-1 xl:grid-cols-3">
      <div v-for="meal of userData.nutritionLog" class="bg-white rounded-md border-2 border-gray-200 p-4 mb-2 xl:mr-2">
        <h5 class="h5">{{ JSON.parse(meal.foodData).food}} &bull; {{ new Date(meal.time).toLocaleDateString() }}</h5>
        <div class="font-sans font-sm text-gray-500">
          <p>Calories &bull; {{ JSON.parse(meal.foodData).calories }}</p>
          <p>Protein &bull; {{ JSON.parse(meal.foodData).protein }}</p>
          <p>Carbs &bull; {{ JSON.parse(meal.foodData).carbs }}</p>
          <p>Fats &bull; {{ JSON.parse(meal.foodData).fats }}</p>
          <p>Sodium &bull; {{ JSON.parse(meal.foodData).sodium }}</p>
          <p>Sugar &bull; {{ JSON.parse(meal.foodData).sugar }}</p>
        </div>
      </div>
      <div v-if="loadingNewFood" class="w-full animate-pulse bg-white rounded-md border-2 border-gray-200 p-4 mb-2 xl:mr-2">
        <h5 class="h5 rounded-md bg-gray-300 animate-pulse">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h5>
        <div class="mt-3 grid grid-cols-2">
          <div>
            <p v-for="i in 5" class="mb-2 bg-gray-300 animate-pulse rounded-md">&nbsp;</p>
          </div>
          <div></div>
        </div>
      </div>
    </div>
  </div>
</template>