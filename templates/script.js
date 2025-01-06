// Get elements
const startButton = document.getElementById("startButton");
const videoWrapper = document.querySelector(".video-wrapper");
const video = document.getElementById("video");

// Add event listener to the button to start the video when clicked
startButton.addEventListener("click", () => {
  videoWrapper.style.display = "block";  // Show the video
  video.play();  // Start playing the video
  startButton.style.display = "none";  // Hide the "Start" button
});
