const apiUrl = "http://localhost:8000";
let generatedStory = "";
let generatedFlashcard = "";
let generatedImagePaths = [];

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
        
        // Enable other buttons
        document.getElementById("generateFlashcardBtn").disabled = false;
        document.getElementById("generateAudioBtn").disabled = false;
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
        
        // Enable image generation button
        document.getElementById("generateImagesBtn").disabled = false;
    } catch (error) {
        console.error("Error generating flashcard:", error);
        alert("Error generating flashcard");
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

        // Define the request payload
        const requestBody = {
            flashcard: generatedFlashcard,
            story: generatedStory
        };

        // Make the fetch call
        const response = await fetch(`${apiUrl}/imageGen/generateImage`, {  // Correct endpoint
            method: 'GET',  
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)  // Send the request body
        });

        // Handle the response
        const data = await response.json();
        if (data.scenes) {
            generatedImagePaths = data.scenes;
            const mediaOutput = document.getElementById("mediaOutput");
            data.scenes.forEach(([scene, imagePath]) => {
                const img = document.createElement("img");
                img.src = imagePath;
                img.alt = scene;
                mediaOutput.appendChild(img);
            });
        }

        // Enable video generation button
        document.getElementById("generateVideoBtn").disabled = false;
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
        alert("Video generated successfully!");
    } catch (error) {
        console.error("Error generating video:", error);
        alert("Error generating video");
    } finally {
        showLoading(false);
    }
}

function showLoading(show) {
    document.getElementById("loading").style.display = show ? "block" : "none";
}

// Event Listeners
document.getElementById("generateStoryBtn").addEventListener("click", generateStory);
document.getElementById("generateFlashcardBtn").addEventListener("click", generateFlashcard);
document.getElementById("generateAudioBtn").addEventListener("click", generateAudio);
document.getElementById("generateImagesBtn").addEventListener("click", generateImages);
document.getElementById("generateVideoBtn").addEventListener("click", generateVideo);
