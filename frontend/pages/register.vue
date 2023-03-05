<script setup lang="ts">

  const submitBtn = ref("Submit")
  const stage = ref(0)
  const email = ref("")
  const fname = ref("")
  const lname = ref("")
  const password = ref("")
  const age = ref("")
  const gender = ref("")
  const weight = ref("")
  const height = ref("")
  const goal = ref("")
  const buildMuscle = ref("")
  const muscleType = ref("")
  const days = ref(0)

  async function submitBasicInfo() {
    stage.value = 1
  }
  async function submit() {
    submitBtn.value="Submitting..."
    console.log(muscleType)
    const data = new FormData()
    data.append("email", email.value)
    data.append("password", password.value)
    data.append("fname", fname.value)
    data.append("lname", lname.value)
    data.append("goal", goal.value)
    data.append("buildMuscle", buildMuscle.value)
    data.append("muscleType", muscleType.value)
    data.append("age", age.value)
    data.append("gender", gender.value)
    data.append("weight", weight.value)
    data.append("height", height.value)
    data.append("days", days.value.toString())
    const resp = await useFetch('http://localhost:5001/register', {
      method: "POST",
      body: data,
    })
    useRouter().push('/login')
  }
</script>

<style>
  .container {
    background-image: src="background.jpeg";
    width: 100%;
    height: 100%;
  }
</style>

<template>
  <div class="container bg-gray-100 rounded-md mt-5 p-4">
    <div v-if="stage == 0">
      <h2 class="h2">Welcome to HealthCoach!</h2>
      <p class="p">We need a little more info about you to create an account.</p>
      <div class="container">
        <form @submit.prevent="submitBasicInfo" class="mt-2">
          <div class="mb-3 row">
            <label for="fname" class="col-sm-2 col-form-label">First Name</label>
            <div class="col-sm-3">
              <input v-model="fname" type="text" class="form-control" placeholder="Enter your First Name..." required>
            </div>
          </div>
          <div class="mb-3 row">
            <label for="lname" class="col-sm-2 col-form-label">Last Name</label>
            <div class="col-sm-3">
              <input v-model="lname" type="text" class="form-control" placeholder="Enter your Last Name..." required>
            </div>
          </div>
          <div class="mb-3 row">
            <label for="lname" class="col-sm-2 col-form-label">Age</label>
            <div class="col-sm-1">
              <input v-model="age" type="text" class="form-control" placeholder="Age..." required>
            </div>
          </div>
            <div class="col-auto">
              <label for="inputGender" class="col-form-label fw-bold">Gender: </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" value="m" v-model="gender">
              <label class="form-check-label" for="flexRadioDefault1">
                M
              </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" value="f" v-model="gender">
              <label class="form-check-label" for="flexRadioDefault2">
                F
              </label>
            </div>
          <div class="mb-3 row">
            <label for="email" class="col-sm-2 col-form-label">Email</label>
            <div class="col-sm-4">
              <input v-model="email" type="email" class="form-control" placeholder="Enter your Email..." id="email" aria-describedby="emailHelp" required>
            </div>
          </div>
          <div class="mb-3 row">
            <label for="password" class="col-sm-2 col-form-label">Password</label>
            <div class="col-sm-4">
              <input v-model="password" type="password" class="form-control" placeholder="Enter your Password..." id="exampleInputPassword1" required>
            </div>
          </div>
          
          <button type="submit" class="btn btn-primary bg-blue-500">Create Account</button>
        </form>
      </div>
    </div>


    <!-- PAGE #2-->



    <div v-if="stage == 1">
      <h2 class="h2">Let's learn more about your goals:</h2>
      <form @submit.prevent="submit" class="mt-2">

        <!-- QUESTION #1-->
        <div class="container">
          <h4>What is your current Height and Weight?</h4>
          <div class="row g-3 align-items-center">

            <div class="col-auto">
              <label for="inputHeight" class="col-form-label fw-bold">Height (in): </label>
            </div>
            <div class="col-auto">
              <input type="height" id="inputWeight" class="form-control" v-model="height">
            </div>
            
            <div class="col-auto">
              <label for="inputWeight" class="col-form-label fw-bold">Weight (lbs): </label>
            </div>
            <div class="col-auto">
              <input type="weight" id="inputHeight" class="form-control" v-model="weight">
            </div>
          </div>
        </div>
        <!-- QUESTION #2-->
        <div class="container">
          <h4>Are you happy with your current weight?</h4>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="same" v-model="goal">
            <label class="form-check-label" for="flexRadioDefault1">
              Yes
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="lose" v-model="goal">
            <label class="form-check-label" for="flexRadioDefault2">
              No, I want to lose weight
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="gain" v-model="goal">
            <label class="form-check-label" for="flexRadioDefault3">
              No, I want to gain weight/muscle
            </label>
          </div>
        </div>

        <!-- QUESTION #3-->
        <div v-if="goal == 'lose' || goal == 'same'" class="container">
          <h4>Do you want build muscle</h4>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="build" v-model="buildMuscle" >
            <label class="form-check-label">
              Yes
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="not build" v-model="buildMuscle" >
            <label class="form-check-label">
              No
            </label>
          </div>
        </div>

        <!-- QUESTION #4-->
        <div v-if="goal == 'gain' || buildMuscle == 'build'" class="container">
          <h4>Do you want to focus on muscle size or strength?</h4>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="size" v-model="muscleType">
            <label class="form-check-label" for="flexRadioDefault1">
              Size
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="radio" value="strength" v-model="muscleType">
            <label class="form-check-label" for="flexRadioDefault2">
              Strength
            </label>
          </div>
        </div>

        <!-- QUESTION #5-->
        <div v-if="!(goal == 'same' && buildMuscle == 'not build') && (buildMuscle == 'not build'|| muscleType != '')" class="container" >
          <select class="form-select" aria-label="Default select example" v-model="days">
            <option value="0" selected>How many days per week do you want to workout?</option>
            <option value="1">One day</option>
            <option value="2">Two days</option>
            <option value="3">Three days</option>
            <option value="4">Four days</option>
            <option value="5">Five days</option>
            <option value="6">Six days</option>
            <option value="7">Seven days</option>
          </select>
        </div>

        <div v-if="(days != 0 || buildMuscle == 'false') || (goal == 'same' && buildMuscle == 'not build')" class="container">
          <button type="submit" class="btn btn-primary bg-blue-500">{{ submitBtn }}</button>
        </div>

      </form>
    </div>
  </div>
</template>