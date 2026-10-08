---
description: This is for the general structure of the web app and programming rules
globs: 
alwaysApply: false
---

# Web App Structure & Programming Rules - Mehmet Semih Babacan

## Core Principles

1. **Elegance in Simplicity**: Code should be clear, concise, and easy to understand.
2. **Performance First**: Always optimize for speed and efficiency.
3. **Mobile-First Approach**: Design for mobile devices first, then scale up.
4. **Accessibility Matters**: Ensure the web app is accessible to all users.
5. **Modular Architecture**: Build components that can be reused across the application.
6. **Understanding Technology**: Prioritize solutions that adapt to human needs rather than forcing humans to adapt to technology.

## File Structure

- `/app`: Core application code
- `/components`: Reusable UI components
- `/public`: Static assets
- `/fonts`: Custom typography
- `/styles`: Global styles and theme configurations
- `/content`: Blog posts and technical articles
- `/projects`: Showcases of Solace and other technical projects

## Coding Standards

### JavaScript/TypeScript
- Use TypeScript for all new code
- Follow ES6+ standards
- Utilize functional programming principles where applicable
- Keep functions pure and focused on a single responsibility
- Document complex AI-related algorithms thoroughly

### CSS/Styling
- Use Tailwind CSS for styling
- Maintain a consistent color palette that reflects the Solace brand identity
- Follow the design system and component library
- Ensure responsive design for all device types

### Component Design
- Each component should be self-contained
- Follow the Single Responsibility Principle
- Use React hooks for state management
- Document component props with TypeScript interfaces
- Create specialized components for displaying smart home technology concepts

## Performance Guidelines

- Optimize images before adding them to the project
- Lazy load components and images when appropriate
- Minimize JavaScript bundle size
- Utilize code splitting for larger applications
- Implement efficient rendering for real-time data displays (important for smart home dashboards)

## Testing Strategy

- Write unit tests for all business logic
- Create integration tests for critical user flows
- Implement end-to-end tests for key user journeys
- Aim for high test coverage on core functionality
- Test thoroughly on multiple devices to ensure cross-platform compatibility

## Deployment Workflow

- Use Vercel for deployments
- Set up preview deployments for all PRs
- Ensure all tests pass before merging to main
- Follow semantic versioning for releases
- Maintain separate staging environments for testing Solace integrations

## Content Guidelines

- Keep blog posts focused and concise
- Use high-quality images that align with the brand
- Maintain a consistent tone of voice that reflects technical expertise and innovation
- Optimize content for SEO when appropriate
- Include detailed technical explanations for smart home and AI concepts
- Balance technical depth with accessibility for non-technical readers
- Showcase Solace projects with both technical details and real-world benefits

## Project Documentation

- Document all APIs thoroughly
- Create clear user guides for any interactive demos
- Maintain up-to-date diagrams for system architecture
- Include detailed explanations of AI and smart home technologies
- Document research findings and technological innovations

This document serves as the foundation for all development work on Mehmet Semih Babacan's personal blog and associated projects, including showcases of Solace's "Anlayan Ev" (Understanding Home) initiative.
