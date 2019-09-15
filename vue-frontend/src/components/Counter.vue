<template>
  <div id = "counter">
    You have watched {{ counter }} episodes of "{{show_name}}"
    <button v-on:click="counter += 1">Add 1</button>
    <button v-on:click="counter -= 1">Minus 1</button>
  </div>
</template>

<script>
export default {
  props : ['count', 'show_name'],
  data() {
    return {
      counter: this.count
    };
  }
};
</script>

<style>
</style>

