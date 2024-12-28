const sendButton = document.getElementById('send-btn');
const inputField = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages');

const emojiMapping = {
  joy: '😊',
  anger: '😠',
  fear: '😨',
  sadness: '😢',
  surprise: '😮',
  disgust: '🤢',
};

// Function to append messages
function appendMessage(message, sender, emotion) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', sender);
  
  const emoji = document.createElement('span');
  emoji.classList.add('emoji');
  emoji.innerText = emojiMapping[emotion] || '🙂';  // Default to neutral if no emotion is found
  
  const content = document.createElement('div');
  content.classList.add('content');
  content.innerText = message;
  
  messageElement.appendChild(emoji);
  messageElement.appendChild(content);
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Smooth scroll
}

// Handle sending a message
sendButton.addEventListener('click', async () => {
  const userMessage = inputField.value;
  if (userMessage.trim() === '') return;

  // Append user message
  appendMessage(userMessage, 'user', 'neutral');  // You can improve this by predicting emotion on frontend if needed

  inputField.value = ''; // Clear input field

  // Call the backend API to get the bot's response
  const response = await fetch('/send_message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: userMessage })
  });

  const data = await response.json();
  
  // Handle error response
  if (data.error) {
    console.error('Error:', data.error);
    return;
  }

  const botMessage = data.response;
  const botEmotion = data.emotion;
  
  // Append bot message with emotion
  appendMessage(botMessage, 'bot', botEmotion);
});
