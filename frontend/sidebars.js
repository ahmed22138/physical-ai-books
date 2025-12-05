/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a set of docs in the sidebar
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 NOTE: Phase 1 implementation uses simplified sidebar with only intro.
 Full 4-module structure will be added in Phase 3 (content creation).
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: Embodied AI Fundamentals',
      collapsed: false,
      items: [
        'introduction/week-1-embodied-ai',
        'introduction/week-2-robot-anatomy',
        'introduction/week-3-control-systems',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Perception & Computer Vision',
      collapsed: false,
      items: [
        'perception/week-4-computer-vision',
        'perception/week-5-3d-perception',
        'perception/week-6-slam',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Motion Planning & Navigation',
      collapsed: false,
      items: [
        'control/week-7-path-planning',
        'control/week-8-trajectory-planning',
        'control/week-9-mobile-navigation',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Integration & Advanced Topics',
      collapsed: false,
      items: [
        'integration/week-10-learning',
        'integration/week-11-deployment',
        'integration/week-12-capstone',
      ],
    },
  ],
};

module.exports = sidebars;
