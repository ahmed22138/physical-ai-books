/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a set of docs in the sidebar
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // But you can create a sidebar manually
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'intro',
        'why-embodied-ai',
        'learning-path',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: Introduction to Embodied AI',
      items: [
        {
          type: 'category',
          label: 'Week 1: Embodied AI Fundamentals',
          items: ['01-introduction/week-1-embodied-ai'],
        },
        {
          type: 'category',
          label: 'Week 2: Robot Anatomy & Sensors',
          items: ['01-introduction/week-2-robot-anatomy'],
        },
        {
          type: 'category',
          label: 'Week 3: Control Systems Basics',
          items: ['01-introduction/week-3-control-systems'],
        },
        '01-introduction/learning-outcomes',
        '01-introduction/formative-assessments',
        '01-introduction/summative-assessment',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Perception & Sensing',
      items: [
        {
          type: 'category',
          label: 'Week 4: Computer Vision Fundamentals',
          items: ['02-perception/week-4-vision-fundamentals'],
        },
        {
          type: 'category',
          label: 'Week 5: LiDAR & Depth Sensing',
          items: ['02-perception/week-5-lidar-sensing'],
        },
        {
          type: 'category',
          label: 'Week 6: Sensor Fusion',
          items: ['02-perception/week-6-sensor-fusion'],
        },
        '02-perception/learning-outcomes',
        '02-perception/formative-assessments',
        '02-perception/summative-assessment',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Control & Actuation',
      items: [
        {
          type: 'category',
          label: 'Week 7: Kinematics',
          items: ['03-control/week-7-kinematics'],
        },
        {
          type: 'category',
          label: 'Week 8: Motion Planning',
          items: ['03-control/week-8-motion-planning'],
        },
        {
          type: 'category',
          label: 'Week 9: Real-Time Control',
          items: ['03-control/week-9-real-time-control'],
        },
        '03-control/learning-outcomes',
        '03-control/formative-assessments',
        '03-control/summative-assessment',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Multi-Robot Integration',
      items: [
        {
          type: 'category',
          label: 'Week 10: Multi-Robot Systems',
          items: ['04-integration/week-10-multi-robot'],
        },
        {
          type: 'category',
          label: 'Week 11: Human-Robot Collaboration',
          items: ['04-integration/week-11-human-robot-collab'],
        },
        {
          type: 'category',
          label: 'Week 12: Deployment & Scaling',
          items: ['04-integration/week-12-deployment'],
        },
        '04-integration/learning-outcomes',
        '04-integration/formative-assessments',
        '04-integration/summative-assessment',
      ],
    },
    {
      type: 'category',
      label: 'Capstone & Assessment',
      items: [
        'capstone-project',
        'assessment-rubrics',
      ],
    },
    {
      type: 'category',
      label: 'Resources',
      items: [
        'hardware-requirements',
        'glossary',
        'tools-and-setup',
      ],
    },
  ],
};

module.exports = sidebars;
