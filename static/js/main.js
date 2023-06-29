
Vue.component('open-map', {
  template: '<div id="map"></div>',
  mounted() {
    const map = new OpenMap.Map('map', {
      center: [0, 0],
      zoom: 10
    });

    // Add your OpenMap customization and interaction here
  }
});

new Vue({
  el: '#app'
});
