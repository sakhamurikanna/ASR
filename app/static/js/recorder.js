document.addEventListener("DOMContentLoaded", () => {
    let mediaRecorder;
    const recordButton = document.getElementById("record");
    const stopButton = document.getElementById("stop");
    const audioElement = document.getElementById("audio");
    const recordResultDiv = document.getElementById("record-result");
    const uploadButton = document.getElementById("upload-button");
    const audioFileInput = document.getElementById("audio-file");
    const uploadResultDiv = document.getElementById("upload-result");

    recordButton.addEventListener("click", async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordButton.disabled = true;
        stopButton.disabled = false;

        mediaRecorder.ondataavailable = async (event) => {
            const audioBlob = new Blob([event.data], { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioElement.src = audioUrl;

            const formData = new FormData();
            formData.append('audioFile', audioBlob, 'recording.wav');

            try {
                const response = await fetch('/upload/', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                recordResultDiv.textContent = result.text;
            } catch (error) {
                recordResultDiv.textContent = 'Upload failed.';
            }
        };
    });

    stopButton.addEventListener("click", () => {
        mediaRecorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
    });

    uploadButton.addEventListener("click", async () => {
        const file = audioFileInput.files[0];
        if (!file) {
            uploadResultDiv.textContent = 'Please select a file.';
            return;
        }

        const formData = new FormData();
        formData.append('audioFile', file);

        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            uploadResultDiv.textContent = result.text;
        } catch (error) {
            uploadResultDiv.textContent = 'Upload failed.';
        }
    });
});
