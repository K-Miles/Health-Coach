<script setup lang="ts">
import { signInWithEmailAndPassword } from '@firebase/auth';


  const email = ref("")
  const password = ref("")

  async function login() {
    const auth = useFirebaseAuth()!
    const user = await signInWithEmailAndPassword(auth, email.value, password.value)
    useRouter().push('/')
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
      <h2 class="h2">Welcome to HealthCoach!</h2>
      <p class="p">You've got this! Enter the following info to login:</p>
      <div class="container">
        <form @submit.prevent="login" class="mt-2">
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
          
          <button type="submit" class="btn btn-success bg-lime-700 mr-1">Login</button>
          <a href="/register" class="btn btn-secondary bg-gray-500">Register</a>
        </form>
      </div>
  </div>
</template>