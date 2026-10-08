# Project Rules and Guidelines

This document outlines the rules, standards, and best practices to follow when developing new features or making changes to this project.

## Table of Contents

1. [Code Style and Standards](#code-style-and-standards)
2. [Git Workflow](#git-workflow)
3. [Component Structure](#component-structure)
4. [State Management](#state-management)
5. [Testing Guidelines](#testing-guidelines)
6. [Performance Considerations](#performance-considerations)
7. [Accessibility](#accessibility)
8. [Documentation](#documentation)

## Code Style and Standards

### General

- Use consistent indentation (2 spaces)
- Use meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Avoid excessive nesting
- Use ES6+ features when appropriate
- Use TypeScript for type safety when possible

### React Specific

- Use functional components with hooks instead of class components
- Use destructuring for props
- Use the React 19 features appropriately
- Avoid inline styles; use Tailwind CSS classes
- Keep components small and reusable
- Use proper prop validation

### CSS/Tailwind

- Follow Tailwind CSS v4 best practices
- Use utility classes instead of custom CSS when possible
- Group related Tailwind classes logically
- For complex components, consider using Tailwind's composition pattern

## Git Workflow

- Create feature branches from `main` using the format: `feature/feature-name`
- Create bug fix branches using the format: `fix/bug-description`
- Write clear, concise commit messages that explain the "why" not just the "what"
- Keep commits focused on a single change
- Rebase feature branches on `main` before creating pull requests
- Squash commits before merging to maintain a clean history
- Delete branches after merging

## Component Structure

- Organize components by feature or domain
- Follow a consistent file structure:
  ```
  /component
    /feature-name
      FeatureName.jsx
      FeatureName.test.jsx
      useFeatureNameLogic.js (if needed)
      index.js (for exports)
  ```
- Use index files for cleaner imports
- Keep presentation and logic separate (consider custom hooks for complex logic)

## State Management

- Use React's built-in state management (useState, useReducer) for component-level state
- Consider context API for shared state across multiple components
- For complex applications, consider using a state management library
- Avoid prop drilling by using context or composition
- Keep state as local as possible

## Testing Guidelines

- Write tests for all new features
- Aim for high test coverage, especially for critical paths
- Use React Testing Library for component tests
- Write both unit and integration tests
- Test edge cases and error scenarios
- Mock external dependencies appropriately

## Performance Considerations

- Use React.memo for expensive components
- Optimize re-renders by using callback functions appropriately
- Use virtualization for long lists
- Lazy load components and routes when appropriate
- Use code splitting to reduce initial bundle size
- Optimize images and assets
- Monitor and analyze bundle size regularly

## Accessibility

- Ensure all components are accessible
- Use semantic HTML elements
- Include proper ARIA attributes when necessary
- Ensure keyboard navigation works properly
- Maintain sufficient color contrast
- Test with screen readers
- Follow WCAG 2.1 AA standards

## Documentation

- Document complex logic with comments
- Use JSDoc for function documentation
- Keep the README updated with new features and changes
- Document API endpoints and data structures
- Include setup instructions for new dependencies
- Document known issues and workarounds

## Deployment

- Test thoroughly before deployment
- Use the deployment script provided in package.json
- Verify the deployed application works as expected
- Monitor for errors after deployment
- Document any deployment-specific considerations
