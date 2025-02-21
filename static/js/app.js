document.addEventListener("DOMContentLoaded", function() {
    const uploadBox = document.getElementById("uploadBox");
    const fileInput = document.getElementById("fileInput");
    const previewImage = document.getElementById("previewImage");
    const selectFile = document.getElementById("selectFile");
    const uploadBtn = document.getElementById("uploadBtn");
    const predictionText = document.getElementById("predictionText");
    const resultImage = document.getElementById("resultImage");
    const resultDiv = document.getElementById("result");

    // Click to select file
    selectFile.addEventListener("click", () => fileInput.click());

    // Drag & Drop functionality
    uploadBox.addEventListener("dragover", (event) => {
        event.preventDefault();
        uploadBox.style.border = "2px solid green";
    });

    uploadBox.addEventListener("dragleave", () => {
        uploadBox.style.border = "2px dashed #007bff";
    });

    uploadBox.addEventListener("drop", (event) => {
        event.preventDefault();
        uploadBox.style.border = "2px dashed #007bff";

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            displayPreview(fileInput.files[0]);
        }
    });

    // Show image preview
    fileInput.addEventListener("change", function() {
        if (fileInput.files.length > 0) {
            displayPreview(fileInput.files[0]);
        }
    });

    function displayPreview(file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            previewImage.src = event.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    // Upload & Predict
    uploadBtn.addEventListener("click", function() {
        if (fileInput.files.length === 0) {
            alert("Please upload an image first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }
            predictionText.textContent = data.prediction;
            resultImage.src = URL.createObjectURL(fileInput.files[0]);
            resultDiv.classList.remove("hidden");
        })
        .catch(error => {
            console.error("Fetch Error:", error);
            alert("Error predicting image.");
        });
    });
});
