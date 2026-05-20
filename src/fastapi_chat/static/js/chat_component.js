const template = document.createElement("template");
template.innerHTML = `
<style>
body {
    font-family: sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #f0f2f5;
}
h2 {
    display: flex;
    align-items: center;
}
#chat-container {
    width: 400px;
    background: white;
    padding: 20px;
    border-radius:
    10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-top: 50px;
}
#messages {
    height: 300px;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
}
.msg {
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 5px;
    background: #e9ecef;
    width: fit-content;
}
.msg.me {
    align-self: flex-end;
    background: #dcf8c6;
}
#typing-indicator {
    height: 20px;
    font-size: 0.8em;
    color: gray;
    font-style: italic;
    margin-bottom: 5px;
}
.input-area {
    display: flex;
    gap: 10px;
}
input {
    flex-grow: 1;
    padding: 8px;
}
</style>


<div id="chat-container">
    <h2><img src="logo.png" alt="logo" width="70" height="70">FastApi Chat</h2>
    <div id="messages"></div>
    <div id="typing-indicator"></div>
    <div class="input-area">
        <input type="text" id="messageInput" placeholder="Type a message..." autocomplete="off">
        <button id="send_msg">Send</button>
    </div>
</div>
<script src="js/chat.js"></script>
`;

/**
 * Class constructor of derived class
 * Let component be a Shadow DOM
 * chate interface
 */
class ChatComponent extends HTMLElement {
    constructor() {
        super();
        this._token = null;
        // TODO: better clientid handling
        this.clientId = "User_" + Math.floor(Math.random() * 1000);
        this.url = "ws://" + document.location.hostname + ":8000/ws/" + this.clientId;
        this.socket = new WebSocket(this.url);
        this.typingTimeout = 0;

        this.root = this.attachShadow({mode: "closed"});
        this.root.appendChild(template.content.cloneNode(true));
        this.global_token = "";
    }

    logEvent(log_msg) {
        this.dispatchEvent(new CustomEvent("log-event",{detail : log_msg} ));
    }

    appendMessage(text, isMe) {
        let messagesDiv = this.root.querySelector("#messages");
        const div = document.createElement('div');
        div.className = `msg ${isMe ? 'me' : ''}`;
        div.innerText = text;
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    sendMessage() {
        let inputField = this.root.querySelector("#messageInput");
        const content = inputField.value;
        if (content) {
            this.socket.send(JSON.stringify({ type: 'chat', content: content }));
            this.appendMessage(`Me: ${content}`, true);
            inputField.value = '';
            this.sendTypingStatus(false); // Stop typing when sent
        }
    }

    sendTypingStatus(isTyping) {
        this.socket.send(JSON.stringify({ type: 'typing', is_typing: isTyping }));
    }

    updateTypingStatus(user, isTyping) {
        let typingDiv = this.root.querySelector("#typing-indicator");
        typingDiv.innerText = isTyping ? `${user} is typing...` : '';
    }

    connectedCallback() {
        let token = this._token;
        let inputField = this.root.querySelector("#messageInput");

        // Handle incoming messages
        this.socket.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if (data.type === 'chat') {
                this.appendMessage(`${data.user}: ${data.content}`, false);
            } else if (data.type === 'system') {
                this.appendMessage(data.content, false);
            } else if (data.type === 'typing') {
                this.updateTypingStatus(data.user, data.is_typing);
            }
        };

        this.root.querySelector("#send_msg").onclick = (event) => {
            event.preventDefault();
            this.sendMessage();
        };

        inputField.addEventListener('input', () => {
            this.sendTypingStatus(true);
            clearTimeout(this.typingTimeout);
            this.typingTimeout = setTimeout(() => {
                this.sendTypingStatus(false);
            }, 2000);
        });

        // Allow pressing Enter to send
        inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        console.log(`Connected as ${this.clientId}`);

    }
}

customElements.define("chat-component", ChatComponent);
