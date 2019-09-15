<template>
  <!-- PART 4: Add your code here -->
  <div style="padding:10px">
    <span> {{name}} </span>
    <Counter count=0 v-bind:show_name="name"></Counter>
  </div>

</template>

<script>
// PART 4: Add your code here
import Counter from "./Counter"

export default {
  components: {
    Counter
  },
  props : ['id', 'name', 'episodes_seen']
};
</script>

<style>
</style>
