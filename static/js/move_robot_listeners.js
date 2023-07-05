
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

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/move_action');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({ action: action }));
}
