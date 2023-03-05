<script setup>
const saveBtn = ref("Change")
const user = await getCurrentUser()
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
const accountInfo = ref(resp.data.value)

async function saveAccount () {
    saveBtn.value="Changing..."
    const resp = await useFetch('http://localhost:5001/account_save', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            uid: user.uid,
            data: accountInfo.value
        })
    })
    saveBtn.value="Regenerating..."
    const resp2 = await useFetch('http://localhost:5001/regenerate', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            uid: user.uid,
        })
    })
    saveBtn.value="Change"
}
</script>

<template>
    <div v-if="saveBtn=='Change'" class="container bg-gray-100 rounded-md mt-5 p-4">
        <h2 class="h2">Account Information and Current Goals</h2>
        <div class="mb-3 ">
            <label for="staticEmail" class="col-sm-2 col-form-label">Email</label>
            <div class="col-sm-3">
                <input type="text"  class="form-control" id="staticEmail" v-model="accountInfo.email" >
            </div>
        </div>
        <!---->
        <div class="mb-3">
            <label for="fname" class="col-sm-2 col-form-label">First Name</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" v-model="accountInfo.fname" >
            </div>
        </div>
        <!---->
        <div class="mb-3 ">
            <label for="lname" class="col-sm-2 col-form-label">Last Name</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" v-model="accountInfo.lname" >
            </div>
        </div>
        <!---->
        <div class="mb-3">
            <label for="age" class="col-sm-2 col-form-label">Age</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" v-model="accountInfo.age" >
            </div>
        </div>
        <!---->
        <div class="col-auto">
              <label for="inputGender" class="col-form-label fw-bold">Gender: </label>
            </div>
            <div class="flex mb-2">
              <div class="form-check mr-5">
                <input class="form-check-input" type="radio" value="m" v-model="accountInfo.gender">
                <label class="form-check-label" for="flexRadioDefault1">
                  M
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="radio" value="f" v-model="accountInfo.gender">
                <label class="form-check-label" for="flexRadioDefault2">
                  F
                </label>
              </div>
            </div>
        <!---->
        <div class="mb-3">
            <label for="weight" class="col-sm-2 col-form-label">Weight</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" v-model="accountInfo.weight" >
            </div>
        </div>
        <!---->
        <div class="mb-3 ">
            <label for="height" class="col-sm-2 col-form-label">Height</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" v-model="accountInfo.height" >
            </div>
        </div>
        <!---->
            <div class="">
                <h4>Are you happy with your current weight?</h4>
                <div class="form-check mt-1 ml-4">
                    <input class="form-check-input" type="radio" value="same" v-model="accountInfo.goal">
                    <label class="form-check-label" for="flexRadioDefault1">
                    Yes
                    </label>
                </div>
                <div class="form-check ml-4">
                    <input class="form-check-input" type="radio" value="lose" v-model="accountInfo.goal">
                    <label class="form-check-label" for="flexRadioDefault2">
                    No, I want to lose weight
                    </label>
                </div>
                <div class="form-check ml-4">
                    <input class="form-check-input" type="radio" value="gain" v-model="accountInfo.goal">
                    <label class="form-check-label" for="flexRadioDefault3">
                    No, I want to gain weight/muscle
                    </label>
                </div>
            </div>

            <!-- QUESTION #3-->
            <div v-if="accountInfo.goal == 'lose' || accountInfo.goal == 'same'" class="">
                <h4>Do you want build muscle</h4>
                <div class="form-check">
                    <input class="form-check-input" type="radio" value="build" v-model="accountInfo.buildMuscle" >
                    <label class="form-check-label">
                    Yes
                    </label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" value="not build" v-model="accountInfo.buildMuscle" >
                    <label class="form-check-label">
                    No
                    </label>
                </div>
            </div>

            <!-- QUESTION #4-->
            <div v-if="accountInfo.goal == 'gain' || accountInfo.buildMuscle == 'build'" class="mt-3">
                <h4>Do you want to focus on muscle size or strength?</h4>
                <div class="form-check mt-1 ml-4">
                    <input class="form-check-input" type="radio" value="size" v-model="accountInfo.muscleType">
                    <label class="form-check-label" for="flexRadioDefault1">
                    Size
                    </label>
                </div>
                <div class="form-check ml-4">
                    <input class="form-check-input" type="radio" value="strength" v-model="accountInfo.muscleType">
                    <label class="form-check-label" for="flexRadioDefault2">
                    Strength
                    </label>
                </div>
            </div>

            <!-- QUESTION #5-->
            <div v-if="!(accountInfo.goal == 'same' && accountInfo.buildMuscle == 'not build') && (accountInfo.buildMuscle == 'not build'|| accountInfo.muscleType != '')" class="mt-3" >
                <select class="form-select col-sm-3" aria-label="Default select example" v-model="accountInfo.days">
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

            <div v-if="(accountInfo.days != 0 || accountInfo.buildMuscle == 'false') || (accountInfo.goal == 'same' && accountInfo.buildMuscle == 'not build')" class="mt-4">
                <button @click="saveAccount" type="submit" class="btn btn-success bg-lime-700">{{ saveBtn }}</button>
            </div>
    </div>
    <div v-if="saveBtn != 'Change'" class="container bg-gray-100 rounded-md mt-5 p-4">
        <div class="flex flex-col justify-center">
            <h2 class="h2 px-4 pt-4 mb-2 text-center">
                Just a moment, we're saving your changes and building a new workout routine!
            </h2>
            <p class="p font-sans text-center mb-4">This should take no longer than 20 seconds.</p>
            <div class="spinner-border mx-auto text-center mb-4" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>
</template>