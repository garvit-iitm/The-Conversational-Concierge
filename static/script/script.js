const form = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatOutput = document.getElementById('chat-output');

//declare global
let uploadedFile = null;

// Handle file selection
document.getElementById('file-input').addEventListener('change', (e) => {
    uploadedFile = e.target.files[0];
    console.log("File selected:", uploadedFile.name);
});

// Handle file upload
document.getElementById('upload-button').addEventListener('click', () => {
    if (!uploadedFile) {
        alert('Please select a file to upload.');
        return;
    }
    const formData = new FormData();
    formData.append('file', uploadedFile);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.questions) {
            chatOutput.innerHTML += `<div class="text-left text-green-400 mb-2">
                <br>${data.questions.replace(/\n/g, "<br>")}
            </div>`;
        } else {
            alert(data.error || "Upload failed.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('File upload failed.');
    });
});

// Handle chat submit
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    chatOutput.innerHTML += `<div class="text-right text-blue-400 mb-2">You: ${message}</div>`;
    userInput.value = '';
});
