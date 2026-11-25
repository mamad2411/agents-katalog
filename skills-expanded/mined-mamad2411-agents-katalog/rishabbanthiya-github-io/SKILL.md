# Cursor Rules for Rishab Banthiya Website

You are an expert in TypeScript, React, Vite, and modern web development with Bootstrap.

## Code Style and Structure

- Write concise, technical TypeScript code with accurate examples
- Use functional and declarative programming patterns; avoid classes
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Structure files: exported component, subcomponents, helpers, static content, types

## TypeScript Best Practices

- Use TypeScript for all code; prefer interfaces over types
- Avoid enums; use maps instead
- Use functional components with TypeScript interfaces
- Enable strict mode in TypeScript for better type safety
- Avoid using `any`; use `unknown` if type is truly unknown
- Use proper type inference where possible

## React Best Practices

- Use functional components and React hooks
- Prefer named exports for components
- Use React.memo() for expensive computations
- Implement proper error boundaries
- Use custom hooks to encapsulate reusable logic
- Keep components small and focused on a single responsibility
- Use composition over inheritance

## State Management

- Use React hooks (useState, useEffect, useContext) for state management
- Minimize use of useEffect; prefer derived state
- Use useCallback and useMemo for performance optimization
- Implement proper cleanup in useEffect hooks

## Performance Optimization

- Minimize 'use client', 'useEffect', and 'setState'; favor React Server Components (RSC)
- Wrap client components in Suspense with fallback
- Use dynamic loading for non-critical components
- Optimize images: use WebP format, include size data, implement lazy loading
- Implement code splitting and lazy loading where appropriate

## Bootstrap Integration

- Follow Bootstrap 5.3 conventions and best practices
- Use Bootstrap utility classes appropriately
- Maintain responsive design principles
- Ensure proper Bootstrap component integration with React
- Avoid inline styles; use Bootstrap classes or CSS modules

## Vite Configuration

- Leverage Vite's fast HMR for development
- Configure proper build optimizations
- Use environment variables appropriately
- Implement proper asset handling

## Error Handling and Validation

- Implement proper error boundaries
- Use try-catch blocks for async operations
- Provide meaningful error messages
- Handle loading and error states in components

## Testing

- Write unit tests for utilities and helpers
- Test component behavior, not implementation details
- Use meaningful test descriptions

## Accessibility (a11y)

- Use semantic HTML elements
- Implement proper ARIA labels
- Ensure keyboard navigation support
- Maintain proper color contrast ratios
- Provide alt text for images

## Git and Code Quality

- Write clear, descriptive commit messages
- Follow conventional commits specification
- Keep commits atomic and focused
- Run linting and type-checking before commits

## Project-Specific Guidelines

- This is a personal website
- Maintain a clean, professional design aesthetic
- Ensure fast load times and optimal performance
- Keep the codebase maintainable and well-documented
- Focus on responsive design for all screen sizes

## Code Review Checklist

- TypeScript strict mode enabled with no type errors
- ESLint rules followed with no warnings
- Components are properly typed
- No console.logs in production code
- Proper error handling implemented
- Responsive design verified
- Accessibility standards met
- Performance optimized

