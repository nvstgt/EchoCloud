function uploadTrack() {
    alert("Upload functionality temporarily disabled due to a cyberattack. Thank you for your understanding.");
}

document.addEventListener('DOMContentLoaded', () => {
    const audioPlayer = document.getElementById('audio-player');
    let currentTrackElem = null; // Reference to the currently playing track

    // Function to format seconds into MM:SS format
    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    // Update the progress bar and time remaining based on the audio player's current time
    audioPlayer.addEventListener('timeupdate', () => {
        if (currentTrackElem) {
            const progressBar = currentTrackElem.querySelector('.progress-bar');
            const timeRemainingElem = currentTrackElem.querySelector('.time-remaining');
            const duration = audioPlayer.duration;
            const currentTime = audioPlayer.currentTime;
            if (!isNaN(duration)) {
                progressBar.value = (currentTime / duration) * 100;
                timeRemainingElem.textContent = formatTime(duration - currentTime);
            }
        }
    });

    // Allow users to seek by moving the progress bar
    document.querySelectorAll('.progress-bar').forEach(bar => {
        bar.addEventListener('input', (e) => {
            if (audioPlayer.duration) {
                const newTime = (e.target.value / 100) * audioPlayer.duration;
                audioPlayer.currentTime = newTime;
            }
        });
    });

    // Set up play/pause functionality for each track
    const tracks = document.querySelectorAll('.track');
    tracks.forEach(track => {
        const playButton = track.querySelector('.play-button');
        const src = track.dataset.src;

        playButton.addEventListener('click', () => {
            // If another track is playing, pause it and reset its button
            if (currentTrackElem && currentTrackElem !== track) {
                const currentButton = currentTrackElem.querySelector('.play-button');
                currentButton.textContent = 'Play';
                audioPlayer.pause();
            }
            // If clicking the same track that's already playing, pause it
            if (currentTrackElem === track && !audioPlayer.paused) {
                audioPlayer.pause();
                playButton.textContent = 'Play';
            } else {
                // Play the new track
                audioPlayer.src = src;
                audioPlayer.play();
                playButton.textContent = 'Pause';
                currentTrackElem = track;
            }
        });
    });

    // When a track ends, reset its play button and progress bar
    audioPlayer.addEventListener('ended', () => {
        if (currentTrackElem) {
            const currentButton = currentTrackElem.querySelector('.play-button');
            currentButton.textContent = 'Play';
            const progressBar = currentTrackElem.querySelector('.progress-bar');
            progressBar.value = 0;
        }
    });
});
