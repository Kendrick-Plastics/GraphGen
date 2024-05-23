var socket = io();

function sendMessage() {
    var message = 'Hello from client';
    socket.emit('message', message);
}

socket.on('response', function(message) {
    console.log('Received response:', message);
});

document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('upload');
    button.addEventListener('click', function() {
        sendMessage();
    });
  });

document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('download');
    button.addEventListener('click', function() {
    });
  });

document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('generate');
    button.addEventListener('click', function() {
    });
  });