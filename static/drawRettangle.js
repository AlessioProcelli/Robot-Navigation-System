
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
        });
	// posizione Robot
 	var centerMarker = new google.maps.Marker({
  	   position: map.getCenter(),
  	   map: map,
  	   title: 'Center Point',
	 scaledSize: new google.maps.Size(16, 16),	
	   });
	
       let rectangle = null;
let startPoint = null;
let endPoint = null;
let firstClick = false;
let secondClick= false;

// Add click event listener on the map
google.maps.event.addListener(map, "click", function (event) {
	  if (!firstClick) {
	    console.log("FirstClick: " );
	    // Set the start point of the rectangle
	    startPoint = event.latLng;
	    firstClick = true;
	  } else {
		console.log("SEcond: ");
	    	// Set the end point of the rectangle
	    	endPoint = event.latLng;
		secondClick=true
	    	// Calculate the rectangle bounds
	    	const bounds = new google.maps.LatLngBounds(startPoint, endPoint);
		// Create a new rectangle
	     	rectangle = new google.maps.Rectangle({
		      	strokeColor: "#FF0000",
		      	strokeOpacity: 0.8,
		      	strokeWeight: 2,
		      	fillColor: "#FF0000",
		      	fillOpacity: 0.35,
		      	map: map,
		      	bounds: bounds,
	    	});
	  // Retrieve rectangle coordinates
    const northEast = bounds.getNorthEast();
    const southWest = bounds.getSouthWest();
    const northWest = new google.maps.LatLng(northEast.lat(), southWest.lng());
    const southEast = new google.maps.LatLng(southWest.lat(), northEast.lng());

    // Print vertex coordinates
    console.log("Rectangle Vertex Coordinates:");
    console.log("North-East: " + northEast.lat() + ", " + northEast.lng());
    console.log("South-West: " + southWest.lat() + ", " + southWest.lng());
    console.log("North-West: " + northWest.lat() + ", " + northWest.lng());
    console.log("South-East: " + southEast.lat() + ", " + southEast.lng());

    // Send rectangle vertex coordinates to Flask
    const coordinates = {
      northEast: { lat: northEast.lat(), lng: northEast.lng() },
      southWest: { lat: southWest.lat(), lng: southWest.lng() },
      northWest: { lat: northWest.lat(), lng: northWest.lng() },
      southEast: { lat: southEast.lat(), lng: southEast.lng() },
    };

    // Make an AJAX request to your Flask route
    fetch("/process_rectangle", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(coordinates),
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from the Flask server
        console.log("Response from Flask:", data);
      })
      .catch(error => {
        console.error("Error:", error);
      });

	}
});
/*
// Add mousemove event listener on the map
google.maps.event.addListener(map, "mousemove", function (event) {
	if (firstClick && !secondClick) {
	    // Set the end point of the rectangle
		if (rectangle) {
		    // Remove existing rectangle
		    rectangle.setMap(null);
	  	}
        	endPoint = event.latLng;
	    	// Calculate the rectangle bounds
	    	const bounds = new google.maps.LatLngBounds(startPoint, endPoint);
	    	// Create a new rectangle
	    	rectangle = new google.maps.Rectangle({
		      strokeColor: "#FF0000",
		      strokeOpacity: 0.8,
		      strokeWeight: 2,
		      fillColor: "#FF0000",
		      fillOpacity: 0.35,
		      map: map,
		      bounds: bounds,
	    	});
  	}
});
*/
    }

