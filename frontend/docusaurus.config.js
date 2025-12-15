// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Embodied Intelligence in the Real World',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-username', // Usually your GitHub org/user name.
  projectName: 'ai-textbook', // Usually your repo name.

  onBrokenLinks: 'ignore', // Phase 1: content still being created
  onBrokenMarkdownLinks: 'ignore',

  // Custom fields for backend API
  customFields: {
    backendApiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000/chat',
  },

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-username/tree/main/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-username//tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'image/imag.jpg',
      navbar: {
        title: '🤖 Physical AI & Humanoid Robotics',
        // logo: {
        //   alt: 'AI Robotics Logo',
        //   src: 'images/imag.jpg',
        // },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/your-username',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      // footer: {
      //   style: 'dark',
      //   links: [
      //     {
      //       title: 'Course',
      //       items: [
      //         {
      //           label: 'Introduction',
      //           to: '/ai-textbook/docs/intro',
      //         },
      //         {
      //           label: 'Week 1: Embodied AI',
      //           to: '/ai-textbook/docs/introduction/week-1-embodied-ai',
      //         },
      //         {
      //           label: 'All Modules',
      //           to: '/ai-textbook/docs',
      //         },
      //       ],
      //     },
      //     {
      //       title: 'Resources',
      //       items: [
      //         {
      //           label: 'GitHub Repository',
      //           href: 'https://github.com/your-username/ai-textbook',
      //         },
      //         {
      //           label: 'Docusaurus',
      //           href: 'https://docusaurus.io',
      //         },
      //       ],
      //     },
      //     {
      //       title: 'About',
      //       items: [
      //         {
      //           label: 'Documentation',
      //           to: '/ai-textbook/docs/intro',
      //         },
      //         {
      //           label: 'Contact',
      //           href: 'https://github.com/your-username/ai-textbook/issues',
      //         },
      //       ],
      //     },
      //   ],
      //   copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      // },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      // AI-native color scheme
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),
};

export default config;
