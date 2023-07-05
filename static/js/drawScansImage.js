
var scale=3;
function draw3DLayer(layer){
var firstLayer = parsedImage.map(function(row) {
           return row.map(function(column) {
               return column[layer];
           });
       });

       // Get the canvas element
       var canvas = document.getElementById('canvas');
       var ctx = canvas.getContext('2d');

       // Loop through the first layer and draw the pixels on the canvas
       for (var i = 0; i < firstLayer.length; i++) {
           for (var j = 0; j < firstLayer[i].length; j++) {
               var pixelValue = firstLayer[i][j];
               posi=i*scale
               posj=j*scale
               // Set the pixel color as grayscale
               ctx.fillStyle = 'rgb(' + pixelValue + ', ' + pixelValue + ', ' + pixelValue + ')';
               ctx.fillRect(posi, posj, scale, scale);
           }
       }



     }
     function draw2DLayer(parsed2DImage,canvas_id){
     var firstLayer = parsed2DImage

            // Get the canvas element
            var canvas = document.getElementById(canvas_id);
            var ctx = canvas.getContext('2d');

            // Loop through the first layer and draw the pixels on the canvas
            for (var i = 0; i < firstLayer.length; i++) {
                for (var j = 0; j < firstLayer[i].length; j++) {
                    var pixelValue = firstLayer[i][j];
                    posi=i*scale
                    posj=j*scale
                    // Set the pixel color as grayscale
                    ctx.fillStyle = 'rgb(' + pixelValue + ', ' + pixelValue + ', ' + pixelValue + ')';
                    ctx.fillRect(posi, posj, scale, scale);
                }
            }



          }
     function slideRight(){
       if(currentLayer<parsedImageLenght-1){
     currentLayer=currentLayer+1;
     doSlide();
}
     }

     function slideLeft(){
       if(currentLayer>0){
     currentLayer=currentLayer-1;
     doSlide();
}
     }
     function doSlide(){
       var layerInfoLabel = document.getElementById("currentSlide");

      layerInfoLabel.textContent = currentLayer.toString() + " / " +parsedImageLenght.toString();
       draw3DLayer(currentLayer);
     }
