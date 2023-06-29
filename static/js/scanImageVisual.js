const filename = 'random_image';
// Create the Three.js scene
let scene, camera, renderer;
            scene = new THREE.Scene();

            // Create the camera
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

            // Create the renderer
            renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
// Create an XMLHttpRequest object
var xhr = new XMLHttpRequest();
xhr.open('POST', '/get_3d_scans', true);
xhr.setRequestHeader('Content-Type', 'application/json');

xhr.onreadystatechange = function () {
  if ( xhr.status === 200) {
    // Handle the response from the Flask app
    var response = JSON.parse(xhr.responseText);
console.log(response);
    // Get the array data from the response
    var numpyArray = response.array;
console.log(numpyArray);
draw3DImage(numpyArray);
    // Process the array data as needed
    // ...
  }
};

// Send the POST request without any payload
xhr.send();

function draw3DImage(numpyArray) {
  // Create a WebGL renderer
  var renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // Create a camera
  var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 2;

  // Create a scene
  var scene = new THREE.Scene();

  // Create a geometry
  var geometry = new THREE.BoxGeometry(1, 1, 1);

  // Iterate through the 3D array and draw the cubes
  for (var x = 0; x < numpyArray.length; x++) {
    for (var y = 0; y < numpyArray[x].length; y++) {
      for (var z = 0; z < numpyArray[x][y].length; z++) {
        // Get the value from the 3D array
        var value = numpyArray[x][y][z];

        // Create a material with color based on the value
        var material = new THREE.MeshBasicMaterial({ color: value });

        // Create a mesh for each cube
        var mesh = new THREE.Mesh(geometry, material);

        // Set the position of the mesh
        mesh.position.set(x, y, z);

        // Add the mesh to the scene
        scene.add(mesh);
      }
    }
  }

  // Render the scene
  renderer.render(scene, camera);
}

function processResponse(arrayBuffer) {
  console.log(arrayBuffer)
  // Procesconst array = new Float32Array(arrayBuffer);
  // Assuming 'arrayBuffer' contains the received ArrayBuffer
console.log("ok-2")
// Create a DataView from the ArrayBuffer
 const dataView = new DataView(arrayBuffer);
console.log("ok-1")
 // Determine the number of elements in the Float32Array
 const numElements = arrayBuffer.byteLength / Float32Array.BYTES_PER_ELEMENT;
console.log("ok-11")
 // Create a Float32Array with the correct length
 const floatArray = new Float32Array(numElements);
console.log("ok-111")
 // Fill the Float32Array with the data from the DataView
 for (let i = 0; i < numElements; i++) {
   floatArray[i] = dataView.getFloat32(i * Float32Array.BYTES_PER_ELEMENT, true);
 }
             // Determine the dimensions of the 3D image
             const width = 60;
             const height = 60;
             const depth = 40;
console.log("ok0")
             // Create Three.js geometry from the Float32Array
             const geometry = new THREE.BoxGeometry(width, height, depth);
             geometry.setAttribute('position', new THREE.BufferAttribute(floatArray, 3));
             console.log("ok1")
             // Create Three.js material
             const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
             console.log("ok2")
             const cube = new THREE.Mesh(geometry, material);
           scene.add(cube);
console.log("ok3")
           // Position and update the camera
           camera.position.z = Math.max(width, height, depth) * 2;
           camera.lookAt(scene.position);
console.log("ok4")
           render();


}
function render() {
  console.log("ok5")
  requestAnimationFrame(render);
  renderer.render(scene, camera);
  console.log("ok6")
}
