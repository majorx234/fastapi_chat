// TODO Login systen
// Generate a random ID for this session to simulate different users
const clientId = "User_" + Math.floor(Math.random() * 1000);
const socket = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
var inputField = document.getElementById('messageInput');
var typingDiv = document.getElementById('typing-indicator');
var messagesDiv = document.getElementById('messages');
let typingTimeout;

// Handle incoming messages
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'chat') {
        appendMessage(`${data.user}: ${data.content}`, false);
    } else if (data.type === 'system') {
        appendMessage(data.content, false);
    } else if (data.type === 'typing') {
        updateTypingStatus(data.user, data.is_typing);
    }
};

function appendMessage(text, isMe) {
    const div = document.createElement('div');
    div.className = `msg ${isMe ? 'me' : ''}`;
    div.innerText = text;
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function sendMessage() {
    const content = inputField.value;
    if (content) {
        socket.send(JSON.stringify({ type: 'chat', content: content }));
        appendMessage(`Me: ${content}`, true);
        inputField.value = '';
        sendTypingStatus(false); // Stop typing when sent
    }
}

function sendTypingStatus(isTyping) {
    socket.send(JSON.stringify({ type: 'typing', is_typing: isTyping }));
}

function updateTypingStatus(user, isTyping) {
    typingDiv.innerText = isTyping ? `${user} is typing...` : '';
}

inputField.addEventListener('input', () => {
    sendTypingStatus(true);
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        sendTypingStatus(false);
    }, 2000);
});

// Allow pressing Enter to send
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

console.log(`Connected as ${clientId}`);
