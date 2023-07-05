var rectangleLayer = L.layerGroup().addTo(map);
var firstClick = null;
var ableDrawRectangle=true

//rettangle must draw only zoom is max
map.on('zoomend', function() {
  if (map.getZoom() !== 19) {
    ableDrawRectangle = false;
  } else {
    ableDrawRectangle = true;
  }
}
)

map.on('click', function(event) {
  if(ableDrawRectangle && (!blockrectangle)){
    if (firstClick === null) {
        firstClick = event.latlng;
    } else {
      // block retangle draw
        blockrectangle=true
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
              console.log(data.vector);
                const vector = data.vector;
                var polylinePoints = [];
                // draw greek path
                var point = vector[0];
                polylinePoints.push([point.x, point.y]);
                for (var i = 0; i < vector.length; i++) {
                    var point = vector[i];
                    polylinePoints.push([point.x, point.y]);
                }
                var polyline = L.polyline(polylinePoints, {
                    color: '#E74C3C',
                     weight: 2
                }).addTo(map);
                drawCriticalPoint();
            })
    }
  }
  else{
    alert("zoom must be max to draw rectangle and Unlock Rettangle must be pressed")
  }
});

//request for critical Point
function drawCriticalPoint(){
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/take_critical_point', true);
  xhr.onreadystatechange = function() {
      var result = JSON.parse(xhr.responseText);
       processPoints(result);
  };
  xhr.send();
}

function processPoints(points) {
  //draw point on map
  var customIcon = L.icon({
    iconUrl: 'static/images/icon-Path.png',
    iconSize: [10, 10],
  });
  for (var i = 0; i < points.length; i++) {
     var cripoint = points[i];
     var marker = L.marker([cripoint.point.x, cripoint.point.y], {
        id: cripoint.unique_id,
        icon: customIcon, // Set the custom icon for the marker
      }).addTo(map);
      var popupContent = 'Not researched';
      var popup = L.popup().setContent(popupContent);
      marker.bindPopup(popup);
      marker.on('click', function(e) {

        var clickedMarker = e.target;
        var markerId = clickedMarker.options.id;
        verifyPressedCriticalPoint(markerId,clickedMarker)
        var clickedX = clickedMarker.getLatLng().lat;
        var clickedY = clickedMarker.getLatLng().lng;

      });
  }
}

// use to redirect to  scan page
function verifyPressedCriticalPoint(id,targetMarker){
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
             targetMarker.openPopup();
           } else {
               var popupContent = 'researched';
               var popup = L.popup().setContent(popupContent);
               targetMarker.bindPopup(popup);
                    // Open a new window
                var paramValue = id;
                var newWindow = window.open('scan?param=' + encodeURIComponent(paramValue), '_blank');
                if (newWindow) {
                    newWindow.focus();
                }
            }

      },
      error: function(error) {
          console.error('Error:', error);
      }
  });
}
