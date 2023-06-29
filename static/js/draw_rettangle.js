var rectangleLayer = L.layerGroup().addTo(map);
var firstClick = null;
var ableDrawRectangle=true
map.on('zoomend', function() {
  if (map.getZoom() !== 19) {
    ableDrawRectangle = false;
  } else {
    ableDrawRectangle = true;
  }
}
)
map.on('click', function(event) {
  if(ableDrawRectangle){
    if (firstClick === null) {
        firstClick = event.latlng;
    } else {
        var secondClick = event.latlng;
        var bounds = L.latLngBounds(firstClick, secondClick);
        L.rectangle(bounds, { color: '#ff7800', weight: 1 }).addTo(rectangleLayer);
        firstClick = null;
        var northWest = bounds.getNorthWest();
               var northEast = bounds.getNorthEast();
               var southWest = bounds.getSouthWest();
               var southEast = bounds.getSouthEast();
        // Create an object with rectangle coordinates
        var rectangleData = {
            northWest: { lat: northWest.lat, lng: northWest.lng },
            northEast: { lat: northEast.lat, lng: northEast.lng },
            southWest: { lat: southWest.lat, lng: southWest.lng },
            southEast: { lat: southEast.lat, lng: southEast.lng }
        };

        // Send the rectangle coordinates to the Flask server
        fetch('/process_rectangle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(rectangleData)
        })
        .then(response => response.json())
            .then(data => {
                const vector = data.vector;
                // Use the vector in your JavaScript code
                console.log(vector);
                var polylinePoints = [];

// Assuming you have the vector data available in the `vector` variable
for (var i = 0; i < vector.length; i++) {
    var point = vector[i];
    polylinePoints.push([point.x, point.y]);
}

var polyline = L.polyline(polylinePoints, {
  color: 'red',
   weight: 2
}).addTo(map);
drawCriticalPoint();
            })











    }
  }
  else{
    alert("zoom must be max to draw rectangle")
  }
});
function drawCriticalPoint(){
  console.log("now");
  console.log("NOW")
  var xhr = new XMLHttpRequest();
  // Prepare the request
  xhr.open('POST', '/take_critical_point', true);
  xhr.onreadystatechange = function() {
    console.log("result");


          // Handle the successful response from Flask
          console.log("provo a leggere");
          var result = JSON.parse(xhr.responseText);
          console.log("cip");
          console.log(result);


       processPoints(result);
     console.log("PP");


    };

    // Send the request without a payload
    xhr.send();
}

function processPoints(points) {
  var customIcon = L.icon({
  iconUrl: 'static/images/icon-Path.png',
  iconSize: [10, 10], // Adjust the size of the icon as needed
});
  for (var i = 0; i < points.length; i++) {
   var cripoint = points[i];

   var marker = L.marker([cripoint.point.x, cripoint.point.y], {
  id: cripoint.unique_id,
  icon: customIcon, // Set the custom icon for the marker
}).addTo(map);
var popupContent = 'Not researched';
  var popup = L.popup().setContent(popupContent);

  // Bind the popup to the marker
  marker.bindPopup(popup);
   marker.on('click', function(e) {
  // Retrieve the clicked marker's coordinates
  var clickedMarker = e.target;
  // Retrieve the clicked marker's ID

  var markerId = clickedMarker.options.id;
  processCriticalPoint(markerId,clickedMarker)
  var clickedX = clickedMarker.getLatLng().lat;
  var clickedY = clickedMarker.getLatLng().lng;

  // Log the coordinates or perform any other desired action
  console.log('Clicked coordinates:', clickedX, clickedY);
  console.log('Clicked id:', markerId);
});
 }
}

// Define the external click function
function handleClick(x, y) {
 // Log the coordinates or perform any other desired action
 console.log('Clicked coordinates:', x, y);
}
function processCriticalPoint(id,targetMarker){
  $.ajax({
      url: '/process_critical_point',
      type: 'POST',
      data: JSON.stringify({'id': id}),
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
          var result = response;
          var isVisited = result.is_visited;

            if(isVisited==false){
             targetMarker.openPopup();} else {
                    // Open a new window with your HTML page
                    var newWindow = window.open('scan', '_blank');
                    if (newWindow) {
                        newWindow.focus();
                    }
                }
        console.log('Magic:',isVisited);
console.log('Magic:');
          // Display the result or perform any other action
          console.log('Result:', result);
      },
      error: function(error) {
          console.error('Error:', error);
      }
  });
}
