<template>
  <div>
    <!-- PART 1: Pass in a "complete" prop here -->
    <Instructions complete="true"></Instructions>
    <!-- PART 4: Modify the Show component to accept all of these props -->
    <b-alert v-model="showAlert" variant="danger" dismissible>{{AlertText}}</b-alert>
    <input v-model="newShow" placeholder="Create a new show" />
    <button v-on:click="createNewShow(newShow)">Create new show</button>
    
    <Show
      v-for="show in shows"
      :key="show.id"
      :id="show.id"
      :name="show.name"
      :episodes_seen="show.episodes_seen"
    />

  </div>
</template>

<script>
import Instructions from "./Instructions.vue";
import Show from "./Show.vue";

let createNewShow = function(showName) {
  if (showName==="") {
    this.AlertText = "Please enter a show name"
    this.showAlert = true
  } else {
    this.showAlert = false
    this.AlertText = "";
    this.shows.push({
      id: this.shows.length + 1,
      name: showName,
      episodes_seen: 0
    });
  }
};

export default {
  components: {
    Instructions,
    Show
  },
  methods: {
    createNewShow: createNewShow
  },
  data() {
    return {
      shows: [
        { id: 1, name: "Game of Thrones", episodes_seen: 0 },
        { id: 2, name: "Naruto", episodes_seen: 220 },
        { id: 3, name: "Black Mirror", episodes_seen: 3 }
      ],
      newShow: "",
      AlertText: "",
      showAlert: false
    };
  }
};
</script>

<style>
</style>


