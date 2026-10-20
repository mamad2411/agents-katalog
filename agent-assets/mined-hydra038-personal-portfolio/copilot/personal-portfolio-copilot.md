# Victor Kipkirui Portfolio - GitHub Copilot Instructions

This is a personal portfolio website built with Next.js, React, TypeScript, and Tailwind CSS for Victor Kipkirui, a Computer Science student and aspiring software developer.

## Project Overview

- **Technology Stack**: Next.js 15, React 19, TypeScript, Tailwind CSS, Framer Motion
- **Features**: Responsive design, dark mode, animations, GitHub integration, contact form
- **Structure**: Modern Next.js app router structure with component-based architecture

## Key Components

- **Hero Section**: Introduction with name, tagline, and call-to-action
- **Navigation**: Sticky navigation with smooth scrolling and theme toggle
- **Projects**: Automatically fetches GitHub repositories via REST API
- **Skills**: Displays programming languages and frameworks as animated badges
- **Resume**: Timeline-style education and experience cards
- **Contact**: Working contact form with Nodemailer integration
- **Theme Provider**: Dark/light mode with localStorage persistence

## Development Guidelines

- Use functional React components with TypeScript
- Follow Next.js 15 app router conventions
- Implement responsive design with Tailwind CSS
- Add smooth animations with Framer Motion
- Maintain accessibility standards
- Optimize for SEO and performance

## Customization Areas

- Replace placeholder content with actual personal information
- Update GitHub username in Projects component
- Configure email settings for contact form
- Customize color scheme in Tailwind config
- Add or modify skills, education, and experience data

## Environment Variables

Required for full functionality:
- EMAIL_USER: Gmail address for contact form
- EMAIL_PASSWORD: App password for Gmail
- GITHUB_USERNAME: GitHub username for repository fetching

The project is deploy-ready for Vercel and includes comprehensive documentation in README.md.