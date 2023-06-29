// Add a click event listener to the button
$(document).ready(function() {
    $('#stop_drive').click(function() {
        // Send an AJAX POST request to trigger the Flask action
        $.ajax({
            type: 'POST',
            url: '/del-action-goal',
            success: function(response) {
                // Handle the response from the Flask action
                console.log(response);
            },
            error: function(error) {
                // Handle any errors that occur during the AJAX request
                console.log(error);
            } });
 });
});
$(document).ready(function() {
    $('#zoom').click(function() {
      var center = map.getCenter(); // Get the current center coordinates
  map.setView(center, 19);
 });
});

$(document).ready(function() {
    $('#clear').click(function() {



  // Remove custom overlays
  map.eachLayer(function (layer) {
    if (layer instanceof L.Rectangle || layer instanceof L.Polyline
    ||layer instanceof L.Marker) {
      map.removeLayer(layer);

    }
      
    robotmarker = null
  });




 });
});
