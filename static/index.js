const apiUrl = "http://localhost:8000";
let generatedStory = "";
let generatedFlashcard = "";
let generatedImagePaths = [];
let isStorySaved = false;

async function generateStory() {
    const context = document.getElementById("context").value;
    if (!context) {
        alert("Please enter a context for the story");
        return;
    }

    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/storyGen/generateStory?context=${encodeURIComponent(context)}`);
        const data = await response.json();
        document.getElementById("story").innerText = data.story;
        generatedStory = data.story;
        
        document.getElementById("generateFlashcardBtn").disabled = false;
        document.getElementById("clearStoryBtn").disabled = false;
        updateSaveButtonState();
    } catch (error) {
        console.error("Error generating story:", error);
        alert("Error generating story");
    } finally {
        showLoading(false);
    }
}

async function generateFlashcard() {
    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/storyGen/generateFlashcard?story=${encodeURIComponent(generatedStory)}`);
        const data = await response.json();
        document.getElementById("flashcard").innerText = data.flashcard;
        generatedFlashcard = data.flashcard;
        
        document.getElementById("clearFlashcardBtn").disabled = false;
        updateSaveButtonState();
    } catch (error) {
        console.error("Error generating flashcard:", error);
        alert("Error generating flashcard");
    } finally {
        showLoading(false);
    }
}

async function saveStoryFlashcard() {
    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/storyGen/saveStoryFlashcard?story=${encodeURIComponent(generatedStory)}&flashcard=${encodeURIComponent(generatedFlashcard)}`);
        const data = await response.json();
        alert(data.message);
        isStorySaved = true;
        
        document.getElementById("deleteStoryFlashcardBtn").disabled = false;
        document.getElementById("generateImagesBtn").disabled = false;
    } catch (error) {
        console.error("Error saving story and flashcard:", error);
        alert("Error saving story and flashcard");
    } finally {
        showLoading(false);
    }
}

async function deleteStoryFlashcard() {
    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/storyGen/deleteStoryFlashcard`);
        const data = await response.json();
        alert(data.message);
        isStorySaved = false;
        
        clearStory();
        clearFlashcard();
        
        document.getElementById("deleteStoryFlashcardBtn").disabled = true;
        document.getElementById("generateImagesBtn").disabled = true;
        document.getElementById("deleteImagesBtn").disabled = true;
    } catch (error) {
        console.error("Error deleting story and flashcard:", error);
        alert("Error deleting story and flashcard");
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
        
        // Clear the media output
        document.getElementById("mediaOutput").innerHTML = '';
        document.getElementById("deleteImagesBtn").disabled = true;
    } catch (error) {
        console.error("Error deleting images:", error);
        alert("Error deleting images");
    } finally {
        showLoading(false);
    }
}

async function generateAudio() {
    try {
        showLoading(true);
        const response = await fetch(`${apiUrl}/audioGen/generateAudio?text=${encodeURIComponent(generatedStory)}`);
        const data = await response.json();
        
        // Add audio player to media output
        const audioPlayer = document.createElement("audio");
        audioPlayer.controls = true;
        audioPlayer.src = data.audio;
        document.getElementById("mediaOutput").appendChild(audioPlayer);
    } catch (error) {
        console.error("Error generating audio:", error);
        alert("Error generating audio");
    } finally {
        showLoading(false);
    }
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

async function generateVideo() {
    try {
        showLoading(true);
        
        if (!generatedImagePaths || generatedImagePaths.length === 0) {
            throw new Error("No images generated yet");
        }

        const videoRequest = {
            image_paths: generatedImagePaths,
            audio_path: "audio.mp3",
            flashcard: generatedFlashcard,
            output_path: "output_video.mp4"
        };

        const response = await fetch(`${apiUrl}/videoGen/generateVideo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(videoRequest)
        });
        
        const data = await response.json();
        
        if (data.message) {
            alert(data.message);
        } else {
            alert("Video generated successfully!");
        }
    } catch (error) {
        console.error("Error generating video:", error);
        alert("Error generating video: " + error.message);
    } finally {
        showLoading(false);
    }
}

function showLoading(show) {
    document.getElementById("loading").style.display = show ? "block" : "none";
}

function clearStory() {
    generatedStory = "";
    document.getElementById("story").innerText = "";
    document.getElementById("clearStoryBtn").disabled = true;
    document.getElementById("generateFlashcardBtn").disabled = true;
    updateSaveButtonState();
}

function clearFlashcard() {
    generatedFlashcard = "";
    document.getElementById("flashcard").innerText = "";
    document.getElementById("clearFlashcardBtn").disabled = true;
    updateSaveButtonState();
}

function updateSaveButtonState() {
    const saveButton = document.getElementById("saveStoryFlashcardBtn");
    saveButton.disabled = !(generatedStory && generatedFlashcard);
}

// Function to display images from the media folder
async function displayGeneratedImages() {
    try {
        const mediaOutput = document.getElementById("mediaOutput");
        mediaOutput.innerHTML = ''; // Clear existing content
        
        // Fetch the list of images from the backend
        const response = await fetch(`${apiUrl}/imageGen/listImages`);
        const data = await response.json();
        
        if (data.images && data.images.length > 0) {
            data.images.forEach((imagePath) => {
                // Create container for each image
                const imageContainer = document.createElement("div");
                imageContainer.className = "scene-container";
                
                // Add image using the media path instead of static
                const img = document.createElement("img");
                img.src = `/media/${imagePath}`; // Using media path for generated images
                img.alt = "Generated Scene";
                imageContainer.appendChild(img);
                
                mediaOutput.appendChild(imageContainer);
            });
            
            // Enable delete button if images are displayed
            document.getElementById("deleteImagesBtn").disabled = false;
        }
    } catch (error) {
        console.error("Error displaying images:", error);
    }
}

// Move all event listeners inside a DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function() {
    // Story Generation
    document.getElementById("generateStoryBtn").addEventListener("click", generateStory);
    document.getElementById("clearStoryBtn").addEventListener("click", clearStory);
    
    // Flashcard Generation
    document.getElementById("generateFlashcardBtn").addEventListener("click", generateFlashcard);
    document.getElementById("clearFlashcardBtn").addEventListener("click", clearFlashcard);
    
    // Story & Flashcard Management
    document.getElementById("saveStoryFlashcardBtn").addEventListener("click", saveStoryFlashcard);
    document.getElementById("deleteStoryFlashcardBtn").addEventListener("click", deleteStoryFlashcard);
    
    // Image Generation
    document.getElementById("generateImagesBtn").addEventListener("click", generateImages);
    document.getElementById("deleteImagesBtn").addEventListener("click", deleteGeneratedImages);
    
    // Audio & Video Generation
    document.getElementById("generateAudioBtn")?.addEventListener("click", generateAudio);
    document.getElementById("generateVideoBtn")?.addEventListener("click", generateVideo);
    
    // Display any existing images when the page loads
    displayGeneratedImages();
});
