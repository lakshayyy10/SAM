// websocket.js
const socket = io();

// Listen for updates from the server
socket.on('update_event', function(data) {
    document.getElementById('status').innerText = data.status;
});

function sendUpdate() {
    const data = { status: 'Updated from client!' };
    socket.emit('update_event', data);
}

