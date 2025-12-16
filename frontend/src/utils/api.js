/**
 * API client for Physical AI Textbook Backend
 * Handles communication with FastAPI backend
 */

// Backend API URL - update this based on environment
// For Docusaurus, we need to check if process is defined (browser vs SSR)
const API_BASE_URL = typeof process !== 'undefined' && process.env?.REACT_APP_API_URL
  ? process.env.REACT_APP_API_URL
  : 'https://physical-ai-books.onrender.com';

/**
 * Query the RAG chatbot
 * @param {string} query - User question
 * @param {string} chapter - Optional chapter filter
 * @param {string} selectedText - Optional highlighted text
 * @returns {Promise<Object>} Response with answer and sources
 */
export async function queryChatbot(query, chapter = null, selectedText = null) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        chapter,
        selected_text: selectedText,
        stream: false
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to get response from chatbot');
    }

    return await response.json();
  } catch (error) {
    console.error('Chatbot query error:', error);
    throw error;
  }
}

/**
 * Submit feedback on a chatbot response
 * @param {string} messageId - UUID of the message
 * @param {string} feedback - Feedback type: 'helpful', 'not_helpful', 'incorrect'
 * @returns {Promise<Object>} Updated feedback status
 */
export async function submitFeedback(messageId, feedback) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/${messageId}/feedback`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ feedback })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to submit feedback');
    }

    return await response.json();
  } catch (error) {
    console.error('Feedback submission error:', error);
    throw error;
  }
}

/**
 * Check backend health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
}
