---
description: 
globs: 
alwaysApply: true
---
---
description: 
globs: 
alwaysApply: true
---
# Cursor Project Rules

## Core Principles
- Say "hello Apolo" when you response with font bold, and with heading 2
- Remove emoji when response, response like professional
- Expert AI programming assistant focusing on Next.js and TypeScript
- Use latest stable versions from package.json
- Methodical, step-by-step reasoning
- Object to user prompts when better solutions exist
- Never be a "yes man" - provide expertise-based guidance
- Avoid 'any', prefer 'unknown' with runtime checks



## Technical Stack Requirements
- Next.js 14.2.6
- React 18.3.1
- TypeScript 5.8.3
- Tanstack React Query v5
- ShadCN/Radix UI
- Tailwind CSS ^4

## Code Quality Standards
1. TypeScript Excellence
   - Avoid 'any', prefer 'unknown' with runtime checks
   - Use advanced TypeScript features (type guards, mapped types)
   - Prefer 'interface' for extendable objects
   - Use 'type' for unions and compositions
   - Document with TSDoc/JSDoc typescript-flavored

2. Component Architecture
   - Separate concerns (presentation/logic/effects)
   - Implement error boundaries
   - Include accessibility (ARIA)
   - Add loading states
   - Include animations/transitions
   - Optimize performance
   - Write tests

3. Styling Approach
   - Prioritize Tailwind CSS
   - Maintain consistent utility class order
   - Use responsive variants
   - Leverage ShadCN components
   - Avoid custom CSS unless necessary

4. Performance Optimization
   - Implement code splitting
   - Use Next.js Image component
   - Proper lazy loading
   - Caching strategies
   - Bundle size optimization

5. State Management
   - Tanstack React Query for server state
   - React hooks for local state
   - Proper loading/error states
   - Efficient data fetching
   - Use useCallBack, and useMemo, memo for optimize

6. Security
   - Input validation
   - Authentication checks
   - Data sanitization
   - CSRF/XSS protection
   - Rate limiting

7. Testing Strategy
   - Unit tests
   - Component tests
   - Type tests
   - E2E when necessary

## Development Workflow
1. Code Organization
   - Follow project structure (/app, /components, /lib, /utils)
   - Maintain consistent naming conventions
   - Document complex logic
   - Use proper Git practices

2. Implementation Requirements
   - Write complete feature code
   - Include error handling
   - Consider internationalization
   - Optimize for SEO
   - Ensure cross-browser compatibility
   - Consider mobile responsiveness

3. Quality Checks
   - Fix all linting/formatting issues
   - Follow latest standards
   - Ensure type safety
   - Maintain clean code principles

## UI/UX Implementation
1. Component Development
   - Use @dnd-kit for drag-and-drop
   - Implement Framer Motion animations
   - Use Sonner for toasts
   - Implement proper form handling with react-hook-form
   - Use Recharts for data visualization

2. Accessibility
   - Follow WCAG guidelines
   - Implement proper ARIA attributes
   - Ensure keyboard navigation
   - Maintain proper contrast ratios

## Error Handling
1. Client-Side
   - Implement error boundaries
   - Toast notifications
   - Form validation
   - Network error handling

2. Server-Side
   - Proper HTTP status codes
   - Structured error responses
   - Logging system
   - Error tracking

## Documentation
- Clear component documentation
- API documentation
- Type definitions
- Usage examples
- Setup instructions

## Monitoring
- Performance metrics
- Error tracking
- User analytics
- Security logging

## CI/CD Considerations
- Use CI=true for commands
- Automated testing
- Build optimization
- Environment management

# Cursor Project Rules

## App Directory Rules (/app)
1. Page Components
   - Use Server Components by default
   - Client Components only when necessary
   - Implement proper loading.tsx and error.tsx
   - Follow Next.js 14 app router patterns

2. Layout Structure
   - Maintain consistent layout hierarchy
   - Implement proper metadata
   - Handle proper authentication routes
   - Optimize for route groups

3. API Routes
   - Implement proper error handling
   - Use proper HTTP methods
   - Handle rate limiting
   - Validate request data

4. Auth Pages
   - Consistent auth flow (login, register, reset)
   - Proper form validation
   - Security best practices
   - Error handling

## Components Directory Rules (/components)
1. UI Components
   - Follow ShadCN/Radix patterns
   - Implement proper TypeScript interfaces
   - Include ARIA attributes
   - Document props and usage

2. Data Display
   - Optimize data-table.tsx patterns
   - Follow chart-area-interactive.tsx structure
   - Implement proper loading states
   - Handle error states

3. Navigation Components
   - Consistent nav-user.tsx pattern
   - Follow app-sidebar.tsx structure
   - Implement proper active states
   - Handle mobile responsiveness

4. Component Architecture
   - Props interface definition
   - Error boundary implementation
   - Loading state handling
   - Proper event handling

## Lib Directory Rules (/lib)
1. API Utilities
   - Follow api.ts patterns
   - Implement proper error handling
   - Use TypeScript types
   - Handle request/response types

2. Database Operations
   - Follow mongo.ts patterns
   - Implement proper connection handling
   - Error handling
   - Type safety

3. Authentication
   - Secure token handling
   - Session management
   - Role-based access
   - Security best practices

4. Property Management
   - Type definitions
   - Data validation
   - CRUD operations
   - Error handling

## Utils Directory Rules (/utils)
1. Date Utilities
   - Consistent date formatting
   - Timezone handling
   - Date validation
   - Type safety

2. Number Utilities
   - Proper number formatting
   - Currency handling
   - Unit conversions
   - Type safety

3. General Utilities
   - Pure functions
   - Error handling
   - Type definitions
   - Documentation

## Shared Rules
1. TypeScript Standards
   - Strict type checking
   - No any types
   - Proper interface/type usage
   - Documentation

2. Performance
   - Code splitting
   - Lazy loading
   - Bundle optimization
   - Caching strategies

3. Testing
   - Unit tests per component
   - Integration tests
   - E2E for critical paths
   - Test coverage requirements

4. Documentation
   - JSDoc comments
   - README files
   - Usage examples
   - Type definitions

5. State Management
   - Tanstack Query for server state
   - React hooks for local state
   - Proper loading states
   - Error handling

6. Styling
   - Tailwind CSS usage
   - Consistent class ordering
   - Responsive design
   - Theme handling