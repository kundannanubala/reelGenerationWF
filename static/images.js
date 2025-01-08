const apiUrl = "http://localhost:8000";

function showLoading(show) {
    document.getElementById("loading").style.display = show ? "block" : "none";
}

async function generateImages() {
    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/imageGen/generateImage?flashcard=${encodeURIComponent(generatedFlashcard)}&story=${encodeURIComponent(generatedStory)}`);
        const data = await response.json();
        
        // After successful generation, display the images
        await displayGeneratedImages();
        
        document.getElementById("generateVideoBtn").disabled = false;
        document.getElementById("deleteImagesBtn").disabled = false;
    } catch (error) {
        console.error("Error generating images:", error);
        alert("Error generating images");
    } finally {
        showLoading(false);
    }
}

async function deleteGeneratedImages() {
    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/imageGen/deleteGeneratedImages`);
        const data = await response.json();
        alert(data.message);
        
        // Refresh the image display
        await displayGeneratedImages();
    } catch (error) {
        console.error("Error deleting images:", error);
        alert("Error deleting images");
    } finally {
        showLoading(false);
    }
}

async function displayGeneratedImages() {
    try {
        const mediaOutput = document.getElementById("mediaOutput");
        const deleteButton = document.getElementById("deleteImagesBtn");
        mediaOutput.innerHTML = ''; // Clear existing content
        
        // Fetch the list of images from the backend
        const response = await fetch(`${apiUrl}/imageGen/listImages`);
        const data = await response.json();
        
        console.log('Received image data:', data); // Debug log
        
        // Enable delete button if there are images, disable if none
        deleteButton.disabled = !(data.images && data.images.length > 0);
        
        if (data.images && data.images.length > 0) {
            data.images.forEach((imagePath) => {
                // Create container for each image
                const imageContainer = document.createElement("div");
                imageContainer.className = "scene-container";
                
                // Add image using the media path
                const img = document.createElement("img");
                const fullImagePath = `/media/${imagePath}`;
                img.src = fullImagePath;
                img.alt = "Generated Scene";
                
                // Add debug info
                const debugInfo = document.createElement("div");
                debugInfo.className = "debug-info";
                debugInfo.textContent = `Path: ${fullImagePath}`;
                imageContainer.appendChild(debugInfo);
                
                // Add error handling
                img.onerror = () => {
                    console.error(`Failed to load image: ${fullImagePath}`);
                    debugInfo.textContent += ' (Failed to load)';
                };
                
                // Add load event
                img.onload = () => {
                    console.log(`Successfully loaded image: ${fullImagePath}`);
                    debugInfo.style.color = 'green';
                };
                
                imageContainer.appendChild(img);
                mediaOutput.appendChild(imageContainer);
            });
        } else {
            mediaOutput.innerHTML = '<p>No images found</p>';
            deleteButton.disabled = true;
        }
    } catch (error) {
        console.error("Error displaying images:", error);
        const mediaOutput = document.getElementById("mediaOutput");
        mediaOutput.innerHTML = `<p>Error loading images: ${error.message}</p>`;
        document.getElementById("deleteImagesBtn").disabled = true;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("generateImagesBtn").addEventListener("click", generateImages);
    document.getElementById("deleteImagesBtn").addEventListener("click", deleteGeneratedImages);
    
    // Display any existing images when the page loads
    displayGeneratedImages();
});
