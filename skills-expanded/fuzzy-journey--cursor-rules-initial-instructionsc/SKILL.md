---
description: 
globs: 
alwaysApply: true
---
# Tiger.Chat Codebase Rules

## Tech Stack
**Description:** This is a Next.js 15 application using TypeScript, React, and Tailwind CSS. The project uses PNPM as the package manager and includes various modern React libraries like Radix UI for components.

- Next.js 15 (Canary) with App Router
- TypeScript for type safety
- React 19 (Release Candidate)
- Tailwind CSS for styling
- Shadcn for pre-build component
- PNPM for package management
- Drizzle ORM for database operations
- Vercel deployment and analytics

## Code Style
**Description:** The project uses Biome for linting and formatting with specific configuration rules.

- Use single quotes for strings
- 2 spaces for indentation
- Maximum line width of 80 characters
- Trailing commas required in multi-line structures
- Double quotes for JSX attributes
- Semicolons are required
- Arrow functions always use parentheses

## Project Structure
**Description:** The project follows Next.js App Router conventions with specific directory organization.

- app/ - Contains all Next.js pages and layouts
- components/ - Reusable React components
- lib/ - Utility functions and core logic
- public/ - Static assets
- hooks/ - Custom React hooks
- tests/ - Playwright test files

## Database
**Description:** The project uses Drizzle ORM with Vercel Postgres.

- Database migrations in lib/db/migrations
- Use drizzle-orm for database operations
- Database schema should be defined using Drizzle's schema builder
- Run migrations before builds

## Testing
**Description:** The project uses Playwright for end-to-end testing.

- Tests are located in the tests/ directory
- Run tests using 'pnpm test'
- Playwright configuration in playwright.config.ts

## Accessibility
**Description:** The project emphasizes accessibility with specific Biome rules.

- Use semantic HTML elements
- Ensure proper ARIA attributes
- Include lang attribute in HTML
- Provide proper heading structure

## Performance
**Description:** Performance optimization guidelines for the application.

- Use Next.js built-in performance features
- Optimize images using Next.js Image component
- Implement proper code splitting
- Use React Server Components where appropriate

## Security
**Description:** Security guidelines and practices for the application.

- Use Next-Auth for authentication
- Implement proper input validation
- Follow security best practices for API routes
- Use environment variables for sensitive data
