
import React from "react";
import Layout from "@theme/Layout";
import Head from "@docusaurus/Head";

export default function Home() {
  return (
    <Layout>
      <Head>
        <style>
          {`
            *, *::before, *::after {
              margin: 0;
              padding: 0;
              box-sizing: border-box;
            }

            body {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
              background: linear-gradient(135deg, #0a0a0a, #1f1f1f, #151515);
              color: white;
              overflow-x: hidden;
            }

            [data-theme='light'] body {
              background: linear-gradient(135deg, #ffffff, #f3f4f6, #e5e7eb);
              color: #1f2937;
            }

            .stars {
              position: fixed;
              top: 0;
              left: 0;
              width: 100%;
              height: 100%;
              pointer-events: none;
              z-index: 0;
            }

            .container {
              position: relative;
              z-index: 1;
              min-height: 100vh;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              padding: 40px 20px;
              text-align: center;
            }

            h1 {
              font-size: 3.5rem;
              font-weight: 700;
              letter-spacing: -0.5px;
              line-height: 1.2;
              background: linear-gradient(135deg, #00d4ff, #7c3aed, #00d4ff);
              background-size: 200% 200%;
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
              animation: gradientShift 6s ease infinite;
            }

            [data-theme='light'] h1 {
              background: linear-gradient(135deg, #0284c7, #7c3aed, #0284c7);
              background-size: 200% 200%;
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
            }

            @keyframes gradientShift {
              0% { background-position: 0% 50%; }
              50% { background-position: 100% 50%; }
              100% { background-position: 0% 50%; }
            }

            .tagline {
              font-size: 1rem;
              color: #00d4ff;
              margin-top: 8px;
              text-transform: uppercase;
              letter-spacing: 1.5px;
              font-weight: 500;
            }

            [data-theme='light'] .tagline {
              color: #0284c7;
            }

            .subtitle {
              font-size: 1.1rem;
              color: #c0c0d0;
              max-width: 750px;
              margin: 16px auto 0;
              line-height: 1.8;
              font-weight: 400;
              letter-spacing: 0.3px;
            }

            [data-theme='light'] .subtitle {
              color: #555555;
            }

            .stats {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
              gap: 20px;
              max-width: 900px;
              margin: 40px auto;
            }

            .stat-card {
              padding: 20px;
              background: rgba(255,255,255,0.05);
              border-radius: 12px;
              border: 1px solid rgba(0,212,255,0.3);
            }

            [data-theme='light'] .stat-card {
              background: rgba(255,255,255,0.6);
              border: 1px solid rgba(2,132,199,0.3);
            }

            .stat-number {
              font-size: 3rem;
              font-weight: 700;
              background: linear-gradient(135deg,#00d4ff,#7c3aed);
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
            }

            [data-theme='light'] .stat-number {
              background: linear-gradient(135deg,#0284c7,#7c3aed);
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
            }

            .stat-label {
              color: #b0b0d0;
              font-size: 0.8rem;
              letter-spacing: 1px;
            }

            [data-theme='light'] .stat-label {
              color: #4b5563;
            }

            .cta-container {
              margin-top: 40px;
              display: flex;
              gap: 20px;
              flex-wrap: wrap;
              justify-content: center;
            }

            .btn {
              padding: 15px 40px;
              border-radius: 10px;
              cursor: pointer;
              border: none;
              font-size: 1rem;
              font-weight: 700;
              text-decoration: none;
            }

            .btn-primary {
              background: linear-gradient(135deg,#00d4ff,#7c3aed);
              color: #0f0f1e;
            }

            [data-theme='light'] .btn-primary {
              background: linear-gradient(135deg,#0284c7,#7c3aed);
              color: white;
            }

            .btn-secondary {
              background: transparent;
              border: 2px solid #00d4ff;
              color: #00d4ff;
            }

            [data-theme='light'] .btn-secondary {
              border: 2px solid #0284c7;
              color: #0284c7;
            }

            footer {
              margin-top: 40px;
              padding: 30px 20px 25px;
              background: linear-gradient(180deg, rgba(15,15,30,0) 0%, rgba(0,212,255,0.05) 100%);
              border-top: 1px solid rgba(0,212,255,0.2);
              position: relative;
              z-index: 1;
            }

            [data-theme='light'] footer {
              background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(2,132,199,0.03) 100%);
              border-top: 1px solid rgba(2,132,199,0.2);
            }

            .footer-content {
              max-width: 1200px;
              margin: 0 auto;
            }

            .footer-grid {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
              gap: 25px;
              margin-bottom: 25px;
            }

            .footer-section h3 {
              font-size: 0.95rem;
              color: #00d4ff;
              margin-bottom: 12px;
              text-transform: uppercase;
              letter-spacing: 1px;
            }

            [data-theme='light'] .footer-section h3 {
              color: #0284c7;
            }

            .footer-section ul {
              list-style: none;
              padding: 0;
              margin: 0;
            }

            .footer-section li {
              margin-bottom: 8px;
            }

            .footer-section a {
              color: #b0b0d0;
              text-decoration: none;
              transition: color 0.3s ease;
              font-size: 0.9rem;
            }

            .footer-section a:hover {
              color: #00d4ff;
            }

            [data-theme='light'] .footer-section a {
              color: #4b5563;
            }

            [data-theme='light'] .footer-section a:hover {
              color: #0284c7;
            }

            .footer-divider {
              height: 1px;
              background: linear-gradient(90deg, rgba(0,212,255,0) 0%, rgba(0,212,255,0.3) 50%, rgba(0,212,255,0) 100%);
              margin: 20px 0;
            }

            [data-theme='light'] .footer-divider {
              background: linear-gradient(90deg, rgba(2,132,199,0) 0%, rgba(2,132,199,0.3) 50%, rgba(2,132,199,0) 100%);
            }

            .footer-bottom {
              text-align: center;
              color: #777;
            }

            [data-theme='light'] .footer-bottom {
              color: #6b7280;
            }

            .footer-bottom p {
              margin: 6px 0;
              font-size: 0.85rem;
            }

            .social-links {
              display: flex;
              gap: 12px;
              margin-top: 12px;
            }

            .social-links a {
              display: inline-flex;
              align-items: center;
              justify-content: center;
              width: 36px;
              height: 36px;
              border-radius: 50%;
              background: rgba(0,212,255,0.1);
              color: #00d4ff;
              text-decoration: none;
              transition: all 0.3s ease;
              font-size: 1rem;
            }

            .social-links a:hover {
              background: rgba(0,212,255,0.3);
              transform: translateY(-3px);
            }

            [data-theme='light'] .social-links a {
              background: rgba(2,132,199,0.1);
              color: #0284c7;
            }

            [data-theme='light'] .social-links a:hover {
              background: rgba(2,132,199,0.3);
            }

            .footer-logo {
              font-size: 1.8rem;
              margin-bottom: 12px;
            }

            .copyright {
              color: #555;
              font-size: 0.8rem;
              margin-top: 12px;
            }

            /* Responsive Design - Mobile First */

            /* Mobile devices (< 480px) */
            @media (max-width: 480px) {
              h1 {
                font-size: 2rem;
                padding: 0 10px;
              }

              .tagline {
                font-size: 0.85rem;
              }

              .subtitle {
                font-size: 0.95rem;
                padding: 0 10px;
              }

              .stats {
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
                margin: 30px 10px;
                padding: 0 5px;
              }

              .stat-card {
                padding: 16px 12px;
              }

              .stat-number {
                font-size: 2rem;
              }

              .stat-label {
                font-size: 0.75rem;
              }

              .cta-container {
                flex-direction: column;
                gap: 12px;
                padding: 0 20px;
              }

              .btn {
                width: 100%;
                padding: 14px 30px;
                font-size: 0.95rem;
              }

              .footer-grid {
                grid-template-columns: 1fr;
                gap: 20px;
                text-align: center;
              }

              .social-links {
                justify-content: center;
              }

              .container {
                padding: 30px 15px;
              }

              .logo {
                font-size: 60px !important;
              }
            }

            /* Small tablets (481px - 768px) */
            @media (min-width: 481px) and (max-width: 768px) {
              h1 {
                font-size: 2.5rem;
              }

              .stats {
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin: 35px 15px;
              }

              .stat-card {
                padding: 18px;
              }

              .stat-number {
                font-size: 2.5rem;
              }

              .footer-grid {
                grid-template-columns: repeat(2, 1fr);
              }
            }

            /* Tablets (769px - 1024px) */
            @media (min-width: 769px) and (max-width: 1024px) {
              h1 {
                font-size: 3rem;
              }

              .stats {
                grid-template-columns: repeat(4, 1fr);
                gap: 18px;
              }
            }

            /* Landscape phones */
            @media (max-height: 600px) and (orientation: landscape) {
              h1 {
                font-size: 2rem;
              }

              .container {
                padding: 20px 15px;
              }

              .stats {
                margin: 20px auto;
                gap: 10px;
              }

              .stat-card {
                padding: 12px;
              }

              .stat-number {
                font-size: 1.8rem;
              }
            }
          `}
        </style>
      </Head>

      <div className="container">
        <div className="logo" style={{ fontSize: "80px", marginBottom: "20px" }}>
          🤖
        </div>

        <h1>Physical AI & Humanoid Robotics</h1>
        <p className="tagline">Master Embodied Intelligence</p>

        <p className="subtitle">
          A comprehensive AI-native interactive textbook with semantic search,
          real-world robotics examples, and hands-on learning.
        </p>

        <div className="stats">
          <div className="stat-card">
            <div className="stat-number">12</div>
            <div className="stat-label">Weeks</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">4</div>
            <div className="stat-label">Modules</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">100+</div>
            <div className="stat-label">Examples</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">48</div>
            <div className="stat-label">Outcomes</div>
          </div>
        </div>

        <div className="cta-container">
          <a className="btn btn-primary" href="/docs/intro">
            📖 Start Learning Now
          </a>

          <a className="btn btn-secondary" href="/docs/introduction/week-1-embodied-ai">
            ▶ Week 1: Embodied AI
          </a>
        </div>
      </div>

      <footer>
        <div className="footer-content">
          <div className="footer-grid">
            <div className="footer-section">
              <div className="footer-logo">🤖</div>
              <h3>AI Textbook</h3>
              <p style={{ color: "#b0b0d0", marginBottom: "12px", fontSize: "0.85rem", lineHeight: "1.5" }}>
                Master embodied intelligence through interactive, hands-on learning.
              </p>
              <div className="social-links">
                <a href="https://github.com/your-username" title="GitHub">
                  🔗
                </a>
                <a href="https://twitter.com" title="Twitter">
                  𝕏
                </a>
                <a href="https://linkedin.com" title="LinkedIn">
                  💼
                </a>
              </div>
            </div>

            <div className="footer-section">
              <h3>Course</h3>
              <ul>
                <li><a href="/docs/intro">Introduction</a></li>
                <li><a href="/docs/introduction/week-1-embodied-ai">Week 1: Embodied AI</a></li>
                <li><a href="/docs">All Modules</a></li>
              </ul>
            </div>

            <div className="footer-section">
              <h3>Resources</h3>
              <ul>
                <li><a href="https://github.com/your-username/">GitHub Repository</a></li>
                <li><a href="/docs">Setup Guide</a></li>
              </ul>
            </div>

            <div className="footer-section">
              <h3>About</h3>
              <ul>
                <li><a href="/docs/intro">Documentation</a></li>
                <li><a href="https://github.com/your-username/issues">Contact</a></li>
              </ul>
            </div>
          </div>

          <div className="footer-divider"></div>

          <div className="footer-bottom">
            <p>✨ Built with Claude Code | Spec-Kit Plus | AI-Native Textbook</p>
            <p>🟢 PRODUCTION READY</p>
            <p className="copyright">
              Copyright © {new Date().getFullYear()} Physical AI & Humanoid Robotics.
            </p>
          </div>
        </div>
      </footer>

    </Layout>
  );
}
