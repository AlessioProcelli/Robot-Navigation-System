// script.js

// Import the Google Maps API library
var script = document.createElement('script');
script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCEpkJBfGR2RWL83uvfcf417PGLPgFM4Wg&callback=initMap';
script.defer = true;
script.async = true;

// Append the script to the document
document.head.appendChild(script);
function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
            center: { lat:{{current_lat}}, lng:{{current_lng}} },
            zoom: 19,
	    scrollwheel: false, // Disable scrollwheel
            gestureHandling: "none",
	    tilt: 0,  // Set tilt to 0 (no tilt
	    mapTypeId: 'satellite', // Set map type to satellite
	    zoomControl: false,  // Disable zoom control button
    	    tiltControl: false,  // Disable tilt control button
	    streetViewControl: false, // Remove street view control options
	    fullscreenControl: false
        });}

    function initMarker(map) {

	// posizione Robot
 	var centerMarker = new google.maps.Marker({
  	   position: map.getCenter(),
  	   map: map,
  	   title: 'Center Point',
	 scaledSize: new google.maps.Size(16, 16),
	   });


    }
// script.js

function createMapAndMarker(latitude, longitude, mapId) {
  // Specify the coordinates for the center of the map
  const center = { lat: latitude, lng: longitude };

  // Create a new map instance
  const map = new google.maps.Map(document.getElementById(mapId), {
    zoom: 12,
    center: center,
  });

  // Create a marker and set its position
  const marker = new google.maps.Marker({
    position: center,
    map: map,
    title: "My Marker",
  });
}
function testGoogleMapsAPI() {
  console.log('Google Maps API has been imported successfully!');
}
