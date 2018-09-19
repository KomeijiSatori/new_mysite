<template>
  <div class="container">
    <h1 v-if="error.statusCode === 404">Page Not Found</h1>
    <h1 v-else>Internal Server Error, {{ error }}</h1>
    <nuxt-link to="/">Home</nuxt-link>
  </div>
</template>

<script>
export default {
  props: ['error'],
}
</script>
