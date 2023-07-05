var canvas = document.getElementById('canvasOrientation');
var ctx = canvas.getContext('2d');

function fetchYawAngle() {
    fetch('/get_yaw_angle')
        .then(response => response.json())
        .then(data => {
            var yawAngleInput = data.yaw_angle;
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const squareSize = 60;
            // Convert angle from degrees to radians
            const yawAngle = -yawAngleInput
            // Clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Draw the black square
            ctx.fillStyle = '#333333';
            ctx.fillRect(centerX - squareSize / 2, centerY - squareSize / 2, squareSize, squareSize);
            // Calculate the line endpoint
            const lineLength = squareSize * 0.5;
            const lineX = centerX + Math.cos(yawAngle) * lineLength / 2;
            const lineY = centerY + Math.sin(yawAngle) * lineLength / 2;
            // Draw the inclined line
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(lineX, lineY);
            ctx.strokeStyle = '#F5F5F5';
            ctx.lineWidth = 2;
            ctx.stroke();
              // Draw the head of the line
            ctx.beginPath();
            const headSize = 5;
            const headX = lineX - Math.cos(yawAngle) * headSize;
            const headY = lineY - Math.sin(yawAngle) * headSize;
            ctx.moveTo(lineX, lineY);
            ctx.lineTo(headX, headY);
            ctx.strokeStyle = '#E74C3C';
            ctx.lineWidth = 2;
            ctx.stroke();
          });
}

 // Fetch the initial yaw angle and update the line rotation
 fetchYawAngle();

 // Fetch the yaw angle every 1 second and update the line rotation
 setInterval(fetchYawAngle, 1000);
