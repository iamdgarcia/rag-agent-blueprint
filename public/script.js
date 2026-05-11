// RAG Agent Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const sourcesList = document.getElementById('sources-list');
    let conversationHistory = [];
    
    function addMessage(content, type = 'assistant') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = content;
        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function displaySources(sources) {
        sourcesList.innerHTML = '';
        if (sources.length === 0) {
            sourcesList.innerHTML = '<p style="color: #7f8c8d;">No relevant documents found.</p>';
            return;
        }
        sources.forEach(source => {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'source-item';
            sourceDiv.innerHTML = `<div class="doc-name">${source.document}</div><div class="doc-content">${source.content.substring(0, 150)}...</div><div class="relevance">Relevance: ${source.relevance_score}</div>`;
            sourcesList.appendChild(sourceDiv);
        });
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        userInput.disabled = true;
        sendButton.disabled = true;
        sendButton.textContent = 'Searching...';
        addMessage(message, 'user');
        userInput.value = '';
        
        try {
            const response = await fetch('/.netlify/functions/rag-agent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, history: conversationHistory })
            });
            
            if (!response.ok) throw new Error(`HTTP error!`);
            const data = await response.json();
            addMessage(data.response, 'assistant');
            if (data.retrieved_documents) displaySources(data.retrieved_documents);
            conversationHistory = data.history;
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        } finally {
            userInput.disabled = false;
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
            userInput.focus();
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
    userInput.focus();
    addMessage('Hello! I am a RAG (Retrieval-Augmented Generation) Agent. I can answer questions based on documents in my knowledge base. Try asking about urban gardening - for example, "What are the health benefits?" or "How do I start an urban garden?"', 'assistant');
});