/**
 * RAG Chatbot Component for Physical AI Textbook
 * Provides intelligent Q&A over textbook content
 */

import React, { useState, useRef, useEffect } from 'react';
import { queryChatbot, submitFeedback } from '../utils/api';
import styles from './Chatbot.module.css';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: 'Hi! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. Ask me anything about the course content!',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chatbot opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const query = inputValue.trim();
    if (!query || isLoading) return;

    // Add user message
    const userMessage = {
      type: 'user',
      content: query,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setError(null);
    setIsLoading(true);

    try {
      // Query the RAG chatbot
      const response = await queryChatbot(query);

      // Add bot response
      const botMessage = {
        type: 'bot',
        content: response.response,
        sources: response.sources,
        confidence: response.confidence,
        messageId: response.id,
        timestamp: new Date(response.created_at)
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.message || 'Failed to get response. Please try again.');

      // Add error message
      const errorMessage = {
        type: 'error',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running and try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (messageId, feedbackType) => {
    try {
      await submitFeedback(messageId, feedbackType);

      // Update message to show feedback was submitted
      setMessages(prev => prev.map(msg =>
        msg.messageId === messageId
          ? { ...msg, feedback: feedbackType }
          : msg
      ));
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <>
      {/* Floating toggle button */}
      <button
        className={`${styles.toggleButton} ${isOpen ? styles.open : ''}`}
        onClick={toggleChatbot}
        aria-label="Toggle chatbot"
        title="AI Assistant"
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        )}
      </button>

      {/* Chatbot panel */}
      {isOpen && (
        <div className={styles.chatbotPanel}>
          {/* Header */}
          <div className={styles.header}>
            <div className={styles.headerContent}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <div>
                <h3 className={styles.headerTitle}>AI Assistant</h3>
                <p className={styles.headerSubtitle}>Ask about textbook content</p>
              </div>
            </div>
            <button
              onClick={toggleChatbot}
              className={styles.closeButton}
              aria-label="Close chatbot"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div className={styles.messagesContainer}>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`${styles.message} ${styles[message.type]}`}
              >
                <div className={styles.messageContent}>
                  {message.content}

                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <p className={styles.sourcesTitle}>📚 Sources:</p>
                      {message.sources.map((source, idx) => (
                        <div key={idx} className={styles.source}>
                          <strong>{source.chapter}</strong> - {source.section}
                          <p className={styles.sourceQuote}>"{source.quote.substring(0, 100)}..."</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Confidence score */}
                  {message.confidence !== undefined && (
                    <div className={styles.confidence}>
                      Confidence: {(message.confidence * 100).toFixed(0)}%
                    </div>
                  )}

                  {/* Feedback buttons */}
                  {message.type === 'bot' && message.messageId && !message.feedback && (
                    <div className={styles.feedbackButtons}>
                      <button
                        onClick={() => handleFeedback(message.messageId, 'helpful')}
                        className={styles.feedbackButton}
                        title="Helpful"
                      >
                        👍
                      </button>
                      <button
                        onClick={() => handleFeedback(message.messageId, 'not_helpful')}
                        className={styles.feedbackButton}
                        title="Not helpful"
                      >
                        👎
                      </button>
                    </div>
                  )}

                  {/* Feedback confirmation */}
                  {message.feedback && (
                    <div className={styles.feedbackConfirm}>
                      Thanks for your feedback!
                    </div>
                  )}
                </div>

                <div className={styles.messageTimestamp}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.messageContent}>
                  <div className={styles.loadingDots}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Error message */}
          {error && (
            <div className={styles.errorBanner}>
              ⚠️ {error}
            </div>
          )}

          {/* Input form */}
          <form onSubmit={handleSubmit} className={styles.inputForm}>
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about the textbook..."
              className={styles.input}
              disabled={isLoading}
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={isLoading || !inputValue.trim()}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}