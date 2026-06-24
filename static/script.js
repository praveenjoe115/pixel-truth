const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const uploadPlaceholder = document.getElementById("uploadPlaceholder");

const openCameraBtn = document.getElementById("openCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const camera = document.getElementById("camera");
const canvas = document.getElementById("canvas");

const analysisForm = document.getElementById("analysisForm");
const scanningOverlay = document.getElementById("scanningOverlay");
const scannerLine = document.getElementById("scannerLine");

let stream = null;

// Image preview after choosing file
if (imageInput) {
    imageInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                if (uploadPlaceholder) {
                    uploadPlaceholder.style.display = "none";
                }

                previewImage.src = e.target.result;
                previewImage.style.display = "block";

                if (camera) {
                    camera.style.display = "none";
                }
            };

            reader.readAsDataURL(file);
        }
    });
}

// Open camera
if (openCameraBtn) {
    openCameraBtn.addEventListener("click", async function () {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });

            camera.srcObject = stream;
            camera.style.display = "block";

            if (uploadPlaceholder) {
                uploadPlaceholder.style.display = "none";
            }

            previewImage.style.display = "none";

        } catch (error) {
            alert("Camera access denied or not available.");
        }
    });
}

// Capture camera photo and attach it to file input
if (captureBtn) {
    captureBtn.addEventListener("click", function () {
        if (!stream) {
            alert("Please open camera first.");
            return;
        }

        canvas.width = camera.videoWidth;
        canvas.height = camera.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(camera, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(function (blob) {
            if (!blob) {
                alert("Failed to capture image. Please try again.");
                return;
            }

            const capturedFile = new File([blob], "captured_photo.png", {
                type: "image/png"
            });

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(capturedFile);
            imageInput.files = dataTransfer.files;

            const imageURL = URL.createObjectURL(blob);

            previewImage.src = imageURL;
            previewImage.style.display = "block";

            if (uploadPlaceholder) {
                uploadPlaceholder.style.display = "none";
            }

            camera.style.display = "none";

            stream.getTracks().forEach(track => track.stop());
            stream = null;

        }, "image/png");
    });
}

// Scanner effect while analyzing
if (analysisForm) {
    analysisForm.addEventListener("submit", function () {
        if (!imageInput.files || imageInput.files.length === 0) {
            alert("Please choose or capture an image first.");
            return;
        }

        if (scanningOverlay) {
            scanningOverlay.style.display = "block";
        }

        if (scannerLine) {
            scannerLine.style.display = "block";
        }
    });
}