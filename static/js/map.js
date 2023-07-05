//Create Leaflet Map
var map = L.map('map', {
    scrollWheelZoom: false, // Disable scroll wheel zoom
}).setView([initialLatitude, initialLongitude], 19);

//isert map by OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 19,
}).addTo(map);

//Marker for robot Position
var robotmarker = null;
//update robot position
function updateMarkerPosition(latitude, longitude) {
  if (robotmarker == null) {
    robotmarker = L.marker([latitude, longitude]).addTo(map);
  } else {
  // Move the robot marker to the new position
    const newPosition = L.latLng(latitude, longitude);
      if ( newPosition.distanceTo(robotmarker.getLatLng()) > 0) {
        //create a line between the old and new location
        line = L.polyline([robotmarker.getLatLng(), newPosition], { color: '#333333', weight: 1 }).addTo(map);
        robotmarker.setLatLng([latitude, longitude]);
      }
    }
// Set the center of view to the current position
  map.setView([latitude, longitude]);
}


function getNewCoordinates() {
// Send an AJAX request to the Flask app to get new coordinates
  $.ajax({
        url: '/get_robot_position',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            var latitude = response.latitude;
            var longitude = response.longitude;
            updateMarkerPosition(latitude, longitude);
            },
        error: function(xhr, status, error) {
               console.log('Error:', error);
             }
        });
}

getNewCoordinates();
// Call getNewCoordinates every X seconds to periodically update the marker position
setInterval(getNewCoordinates, 1000);
