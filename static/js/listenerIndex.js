// Add a click event listener to the button
function stop_drive(){

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/del-action-goal');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function max_zoom(){
  var center = map.getCenter();
  map.setView(center, 19);
}

function clear_map(){
  map.eachLayer(function (layer) {
      if (layer instanceof L.Rectangle || layer instanceof L.Polyline
      ||layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
  });
  robotmarker = null
}

function unlock_rectangle(){
  blockrectangle=false;
}
