var socket = io();
let graphResponse = '';

// Receive and display the final graph
socket.on("graph_response", function(data) {
  const imageElement = document.getElementById('graph');
  graphResponse = data.image_data;
  imageElement.src = 'data:image/png;base64,' + data.image_data;
});

// Update the drop downs with the returned data
socket.on("headers", function(data) {
  const createdDropDown = document.getElementById("created");
  const resolvedDropDown = document.getElementById("resolved");
  const categoryDropDown = document.getElementById("category");

  createdDropDown.innerHTML = '';
  resolvedDropDown.innerHTML = '';
  categoryDropDown.innerHTML = '';

  // Update created dropdown
  data.forEach(item => {
    const optionChild = document.createElement("option")
    optionChild.value = item;
    optionChild.textContent = item;

    createdDropDown.appendChild(optionChild);
  });

  // Update resolved dropdown
  data.forEach(item => {
    const optionChild = document.createElement("option")
    optionChild.value = item;
    optionChild.textContent = item;

    resolvedDropDown.appendChild(optionChild);
  });
    
  // Update category dropdown
  data.forEach(item => {
    const optionChild = document.createElement("option")
    optionChild.value = item;
    optionChild.textContent = item;

    categoryDropDown.appendChild(optionChild);
  });
});
 
// Download the finished graph
function downloadImage () {
  document.getElementById('download').addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = 'data:image/png;base64,' + graphResponse;
    link.download = 'graph.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  })
}

// Gives the server the header selections and gens the graph
function generateGraph () {
  const createdDropDown = document.getElementById("created");
  const resolvedDropDown = document.getElementById("resolved");
  const categoryDropDown = document.getElementById("category");

  const data = {
    created: createdDropDown.value,
    resolved: resolvedDropDown.value,
    category: categoryDropDown.value
  };
  
  socket.emit("header-selection", data);
};

// The function that sends the uploaded file to the server
function uploadFile() {
  var fileInput = document.getElementById("image-upload-input");
  var file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function(event) {
      const fileData = event.target.result;
      socket.emit("file-upload", {name: file.name, data: fileData});
    } 

    reader.readAsArrayBuffer(file);
  } else {
    console.error("No file selected.");
  }
};

// Attach function to the upload button click button
document.addEventListener('DOMContentLoaded', function () {
  var button = document.getElementById('upload');
  button.addEventListener('click', function () {
    uploadFile();
  });
});

// Attach function to the download button click button
document.addEventListener('DOMContentLoaded', function () {
  var button = document.getElementById('download');
  button.addEventListener('click', function () {
    downloadImage();
  });
});

// Attach function to the generate button click button
document.addEventListener('DOMContentLoaded', function () {
  var button = document.getElementById('generate');
  button.addEventListener('click', function () {
    generateGraph();
  });
});