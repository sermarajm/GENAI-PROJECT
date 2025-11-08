document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');

    // Function to add a message to the chat
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'assistant-message');
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Function to send message to API (boilerplate)
    async function sendMessageToAPI(message) {
        // TODO: Replace with your actual API endpoint
        const API_ENDPOINT = 'http://127.0.0.1:5000/chat';

        try {
            // Show typing indicator
            showTypingIndicator();

            // Example API call using fetch
            // You should replace this with your actual API implementation
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log(data)
            // Assuming the API returns { response: "message" }
            return data.message || "I'm sorry, I didn't understand that.";
        } catch (error) {
            console.error('Error calling API:', error);
            return "Sorry, I'm having trouble connecting to the server right now.";
        } finally {
            hideTypingIndicator();
        }
    }

    // Handle sending message
    async function handleSendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';

        // Disable input while waiting for response
        userInput.disabled = true;
        sendButton.disabled = true;

        // Get response from API
        const botResponse = await sendMessageToAPI(message);

        // Add bot response to chat
        addMessage(botResponse);

        // Re-enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }

    // Event listeners
    sendButton.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    userInput.focus();
});