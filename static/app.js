// Set constraints for the video stream
var constraints = { video: { facingMode: "user" }, audio: false };
// Define constants
const cameraView = document.querySelector("#camera--view"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#camera--trigger")
// Access the device camera and stream to cameraView
function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream;
    })
    .catch(function(error) {
        console.error("Oops. Something is broken.", error);
    });
}
// Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/png");
    //cameraOutput.classList.add("taken");
    cameraView.classList.add("taken");
    
    var ImageURL = cameraOutput.src; // 'photo' is your base64 image
    
    // Split the base64 string in data and contentType
    var block = ImageURL.split(";");
    // Get the content type of the image
    var contentType = block[0].split(":")[1];
    // get the real base64 content of the file
    var realData = block[1].split(",")[1];
    
    var blob = b64toBlob(realData, contentType);
    
    // Create a FormData and append the file with "file" as parameter name
    var form = document.getElementById("myAwesomeForm");
    var formDataToUpload = new FormData(form);
    formDataToUpload.append("file", blob, "blob.png");

    //mostramos la barra de envio
    var x = document.getElementById("myDIV");
    x.style.display = "block";
    
    //escondemos el botón
    var y = document.getElementById("camera--trigger");
    y.style.display = "none";
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", form.target, true);
    
    xhr.onreadystatechange = function() { // Call a function when the state changes.
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        // Request finished. Do processing here.
        document.write(this.responseText);
        }
    }
    
    xhr.send(formDataToUpload);
    
};

function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data); // window.atob(b64Data)
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, {type: contentType});
    return blob;
}

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);
