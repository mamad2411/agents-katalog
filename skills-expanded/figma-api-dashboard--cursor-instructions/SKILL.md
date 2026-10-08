# Cursor AI Instructions for Figma-Cursor Project

## Project Context

You are working on a Next.js 15 application with TypeScript, Tailwind CSS 4, and Figma integration. This project follows modern React patterns with App Router and server components.

## Technology Stack Understanding

- **Next.js 15.3.4** with App Router (not Pages Router)
- **React 19** with latest features and patterns
- **TypeScript 5+** with strict type checking
- **Tailwind CSS 4** with utility-first approach
- **Turbopack** for fast development builds

## Key Development Principles

### 1. Component Creation

When I ask you to create a component:

- Use Server Components by default
- Add "use client" only when necessary
- Use TypeScript interfaces for props
- Include JSDoc comments
- Implement responsive design with Tailwind
- Add proper accessibility attributes
- Use semantic HTML elements

### 2. API Development

When creating API routes:

- Use App Router conventions (route.ts files)
- Implement proper TypeScript types
- Include input validation with Zod
- Use structured error responses
- Add proper HTTP status codes

### 3. Styling Approach

- Use Tailwind CSS 4 utility classes exclusively
- No custom CSS or CSS-in-JS libraries
- Implement mobile-first responsive design
- Use CSS variables for theming
- Support dark mode with dark: variants

### 4. Data Fetching

- Use Server Components for initial data loading
- Implement Server Actions for mutations
- Use proper caching strategies
- Handle loading and error states
- Implement parallel data fetching

### 5. Performance Optimization

- Use Next.js Image component for images
- Implement code splitting with dynamic imports
- Use React.memo() for expensive components
- Optimize bundle size
- Cache data appropriately

### 6. Security Standards

- Never expose sensitive data to client
- Use environment variables properly
- Validate all user inputs
- Implement proper authentication
- Follow OWASP guidelines

### 7. Error Handling

- Use try-catch blocks for async operations
- Implement error boundaries
- Provide meaningful error messages
- Log errors appropriately
- Use Next.js error pages

### 8. Testing Requirements

- Write unit tests for components
- Use Jest and Testing Library
- Test accessibility features
- Mock external dependencies
- Follow AAA pattern

## File Organization Rules

- Use kebab-case for file and directory names
- Place components in `src/components/`
- Use PascalCase for component files (.tsx)
- Create index.ts files for component groups
- Group related components by feature

## Code Quality Standards

- Use TypeScript strict mode
- Follow ESLint configuration
- Format with Prettier
- Include proper JSDoc comments
- Use descriptive variable names
- Implement proper type safety

## Figma Integration Patterns

- Use proper authentication for Figma API
- Handle API rate limiting
- Cache Figma responses appropriately
- Implement error handling for API calls
- Use environment variables for tokens

## Common Commands

- Development: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`
- Test: `npm test`

## Questions to Ask

When requirements are unclear, ask about:

- Component functionality and props needed
- Whether client-side features are required
- Styling preferences and responsive behavior
- Data fetching requirements
- Error handling preferences
- Accessibility requirements

Remember to always follow the .cursorrules file and maintain consistency with the existing codebase.
