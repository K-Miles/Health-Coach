<script setup>
const loadingNewFood = ref(false)
const waterOrFood = ref("")
const water = ref()
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

const areDatesOnSameDay = (a, b) => // https://logfetch.com/js-check-if-dates-are-on-same-day/
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate();

const userData = ref(resp.data.value)

for (const entry of userData.value.nutritionLog) {
  if (areDatesOnSameDay(new Date(entry.time), new Date())) {
    userData.value.target.food -= Number((JSON.parse(entry.foodData).calories).match(/(\d+)/)[0]); // regex: https://www.geeksforgeeks.org/extract-a-number-from-a-string-using-javascript/
    userData.value.target.protein -= Number((JSON.parse(entry.foodData).protein).match(/(\d+)/)[0]); // regex: https://www.geeksforgeeks.org/extract-a-number-from-a-string-using-javascript/
  }
}

if (userData.value.target.food < 0) {
  userData.value.target.food = 0
}
if (userData.value.target.protein < 0) {
  userData.value.target.protein = 0
}
if (userData.value.target.water < 0) {
  userData.value.target.water = 0
}

async function addFood() {
  if (waterOrFood.value == 'water') {
    const resp = await useFetch('http://localhost:5001/waterLog', {
      method: "POST",
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          uid: user.uid,
          water: water.value
      })
    })
    console.log(userData.value.target)
    userData.value.target.water -= water.value
  } else if (waterOrFood.value == 'food') {
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
  water = ref()
  food.value = ""
  waterOrFood.value = ""
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

   <div class="grid grid-cols-3 mt-3" >
      <div class="text-center">
        <h3 class="h3 mb-0">{{ userData.target.food }}</h3>
        <p class="font-xs mt-0 font-sans">calories remaining today</p>
      </div>
      <div class="text-center">
        <h3 class="h3 mb-0">{{ userData.target.protein }}</h3>
        <p class="font-xs mt-0 font-sans">grams of protein needed today</p>
      </div>
      <div class="text-center">
        <h3 class="h3 mb-0">{{ userData.target.water }}</h3>
        <p class="font-xs mt-0 font-sans">ounces of water needed today</p>
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
            <div class="mb-3">
              <div class="col-auto">
                <label for="inputGender" class="col-form-label">What would you like to log?</label>
              </div>
              <div class="ml-4 form-check">
                <input class="form-check-input" type="radio" value="food" v-model="waterOrFood">
                <label class="form-check-label" for="flexRadioDefault1">
                  Food
                </label>
              </div>
              <div class="ml-4 form-check">
                <input class="form-check-input" type="radio" value="water" v-model="waterOrFood">
                <label class="form-check-label" for="flexRadioDefault2">
                  Water
                </label>
              </div>
            </div>
            <div v-if="waterOrFood == 'food'">
              <input v-model="food" type="text" class="form-control font-sans" placeholder="Enter food in natural language..."/>
              <p class="text-xs ml-1 mt-1 text-gray-500">We use AI to calculate a rough estimate of nutritional data. This will take ~10 seconds.</p>
            </div>
            <div v-if="waterOrFood == 'water'">
              <input v-model="water" type="number" class="form-control font-sans" placeholder="Enter number of ounces of water..."/>
              <p class="text-xs ml-1 mt-1 text-gray-500">This will be subtracted straight off of your daily goal. Your goal resets daily.</p>
            </div>
          </div>
          <div class="modal-footer font-sans">
            <button type="button" class="btn btn-secondary bg-gray-500" data-bs-dismiss="modal">Close</button>
            <button @click="addFood" type="button" class="btn btn-success bg-lime-700" data-bs-dismiss="modal">Add</button>
          </div>
        </div>
      </div>
    </div>
    <h3 class="mt-3 h3">Meals:</h3>
    <div class="mt-1 grid grid-cols-1 xl:grid-cols-3">
      <div v-for="meal of userData.nutritionLog" class="bg-white rounded-md border-2 border-gray-200 p-4 mb-2 xl:mr-2">
        <h5 class="h5">{{ JSON.parse(meal.foodData).name}} &bull; {{ new Date(meal.time).toLocaleDateString() }}</h5>
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