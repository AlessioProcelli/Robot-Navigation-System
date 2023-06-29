var map = L.map('map', {
     
    scrollWheelZoom: false, // Disable scroll wheel zoom
}).setView([initialLatitude, initialLongitude], 19);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 19,
}).addTo(map);


    var robotmarker = null;

    function updateMarkerPosition(latitude, longitude) {
      if (robotmarker == null) {

  robotmarker = L.marker([latitude, longitude]).addTo(map);
} else {
  // Move the robot marker to the new position
  const newPosition = L.latLng(latitude, longitude);

    if ( newPosition.distanceTo(robotmarker.getLatLng()) > 0) {

        line = L.polyline([robotmarker.getLatLng(), newPosition], { color: 'black', weight: 1 }).addTo(map);



    // Customize the different marker properties or add it to a different layer, if needed

  robotmarker.setLatLng([latitude, longitude]);
}}
// Set the view to the current position
map.setView([latitude, longitude]);
}
    function getNewCoordinates() {
        // Send an AJAX request to the Flask app to get new coordinates
        // Replace '/get_coordinates' with the endpoint in your Flask app that returns the coordinates
        // You may need to adjust the data format and method based on your Flask app's implementation
        $.ajax({
            url: '/get_robot_position',
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                var latitude = response.latitude;
                var longitude = response.longitude;
                 console.log('Received coordinates:', latitude, longitude);
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
   /*map.on('click', function(e) {
            var lat = e.latlng.lat;
            var lng = e.latlng.lng;

            // Send the coordinates to the Flask backend
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/coordinates', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ 'lat': lat, 'lng': lng }));
        });
*/
