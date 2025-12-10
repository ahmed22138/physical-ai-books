/**
 * Root wrapper component for Docusaurus
 * Adds global components like the chatbot to all pages
 */

import React, { useState, useEffect } from 'react';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

export default function Root({ children }) {
  const [ChatbotComponent, setChatbotComponent] = useState(null);

  useEffect(() => {
    if (ExecutionEnvironment.canUseDOM) {
      import('../components/Chatbot').then((module) => {
        setChatbotComponent(() => module.default);
      });
    }
  }, []);

  return (
    <>
      {children}
      {ChatbotComponent && <ChatbotComponent />}
    </>
  );
}
