// Get references to the buttons
const goFrontButton = document.getElementById('go-front');
const goBackButton = document.getElementById('go-back');
const rotateLeftButton = document.getElementById('rotate-left');
const rotateRightButton = document.getElementById('rotate-right');

// Add event listeners to the buttons
goFrontButton.addEventListener('click', goFront);
goBackButton.addEventListener('click', goBack);
rotateLeftButton.addEventListener('click', rotateLeft);
rotateRightButton.addEventListener('click', rotateRight);

// Define the actions for each button
function goFront() {
  sendAction('go_front');
}

function goBack() {
  sendAction('go_back');
}

function rotateLeft() {
  sendAction('rotate_left');
}

function rotateRight() {
  sendAction('rotate_right');
}

// Send the action to the Flask app
function sendAction(action) {
  // Make an AJAX request to the Flask server
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/move_action');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({ action: action }));
}
