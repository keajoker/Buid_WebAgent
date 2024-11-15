// Get references to HTML elements
const menuIcon = document.getElementById('menuIcon');
const sidebar = document.getElementById('sidebar');
const toggleDarkModeButton = document.getElementById('toggleDarkMode');
const openChatInNewTabButton = document.getElementById('openChatInNewTab');
const refreshPageButton = document.getElementById('refreshPage');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');
const voiceButton = document.querySelector('.voice-button');
const voiceButtonImage = voiceButton.querySelector('img');
const readAloudButton = document.getElementById('readAloudButton');
let isDarkMode = true;
let isReading = false;
let isSending = false;

// Toggle sidebar visibility
menuIcon.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    document.querySelector('.chat-box').style.left = sidebar.classList.contains('active') ? '60px' : '20%';
});

// Toggle between dark and light mode
toggleDarkModeButton.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    toggleDarkModeButton.textContent = isDarkMode ? 'Dark Mode' : 'Light Mode';
    isDarkMode = !isDarkMode;
});

// Open chat in a new tab and save chat history
openChatInNewTabButton.addEventListener('click', () => {
    const chatHistory = chatMessages.innerHTML;
    localStorage.setItem('chatHistory', chatHistory);
    window.open('index.html', '_blank');
});

// Refresh the page
refreshPageButton.addEventListener('click', () => {
    location.reload();
});

// Function to create clickable links
function linkify(text) {
    const urlPattern = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    const emailPattern = /(([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+))/ig;
    return text
        .replace(urlPattern, '<a href="$1" target="_blank">$1</a>')
        .replace(emailPattern, '<a href="mailto:$1">$1</a>');
}

// Send message to the bot
const sendMessage = async () => {
    if (isSending) return;
    isSending = true;

    let userMessage = chatInput.value.trim();
    if (!userMessage) {
        isSending = false;
        return;
    }

    userMessage = userMessage.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");

    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'user-message';
    userMessageElement.textContent = userMessage;
    chatMessages.appendChild(userMessageElement);
    chatInput.value = '';

    const botMessageElement = document.createElement('div');
    botMessageElement.className = 'bot-message';
    botMessageElement.textContent = 'Loading...';
    chatMessages.appendChild(botMessageElement);

    console.log('Sending message to backend:', userMessage);

    try {
        const response = await fetch('https://f7w3h7d5-8000.inc1.devtunnels.ms/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userMessage }),
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Response from backend:", result);
            botMessageElement.innerHTML = linkify(result.answer || "I'm not sure how to respond to that.");
        } else {
            console.error("Server responded with an error:", response.status);
            botMessageElement.textContent = "Sorry, there was an error processing your request.";
        }
    } catch (error) {
        console.error("Fetch error:", error);
        botMessageElement.textContent = "Network error. Please try again.";
    }

    isSending = false;
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

document.querySelector('.send-button').addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') sendMessage();
});

// Load chat history if it exists
window.onload = () => {
    const chatHistory = localStorage.getItem('chatHistory');
    if (chatHistory) {
        chatMessages.innerHTML = chatHistory;
        localStorage.removeItem('chatHistory');
    }
};

// Voice recognition setup
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        voiceButtonImage.src = 'listening.png';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
        sendMessage();
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event);
    };

    recognition.onend = () => {
        voiceButtonImage.src = 'mic.png';
    };

    voiceButton.addEventListener('click', () => {
        recognition.start();
    });
} else {
    voiceButton.style.display = 'none';
    console.warn('Speech recognition not supported in this browser.');
}

// Read Aloud functionality
readAloudButton.addEventListener('click', () => {
    if (isReading) {
        speechSynthesis.cancel();
        readAloudButton.textContent = 'Read Aloud';
        isReading = false;
    } else {
        const latestBotMessage = chatMessages.querySelector('.bot-message:last-child');
        if (latestBotMessage) {
            const textContent = latestBotMessage.innerText;
            const utterance = new SpeechSynthesisUtterance(textContent);
            utterance.onend = () => {
                isReading = false;
                readAloudButton.textContent = 'Read Aloud';
            };
            speechSynthesis.speak(utterance);
            readAloudButton.textContent = 'Stop Reading';
            isReading = true;
        }
    }
});
