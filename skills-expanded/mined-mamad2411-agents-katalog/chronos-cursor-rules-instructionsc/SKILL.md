---
description: This rules file provides comprehensive coding standards and guidelines for the project. The Cursor editor should apply these rules when:- Analyzing code for potential improvements - Suggesting refactoring options - Reviewing pull requests - Providing code completions - Offering real-time coding suggestions - Generating new code blocks or components - Implementing debugging solutions - Managing state and side effects - Organizing project structure
globs: *
---
# Project Standards and Guidelines
# CHRONOS: REMIX PROJECT

> **IMPORTANT NOTE:** This is a Remix application, NOT a Next.js application. All code generation, suggestions, and optimizations should follow Remix patterns and conventions.

## Code Simplicity and Clarity

### Core Principles
1. Prefer simple code over complex solutions - cleverness should never be chosen
2. Reduce cognitive complexity by breaking down complex operations
3. Use meaningful and descriptive names for variables, functions, and components
4. Keep functions and components focused on a single responsibility
5. Keep components under 150 lines as a general guideline

## React and TypeScript Best Practices

### Components
1. Prefer function components over class components
2. Use TypeScript interfaces/types for component props
3. Prefer inline functions for simple event handlers:
```tsx
// ✅ Good
function Component() {
  return <Button onClick={() => console.log('clicked')} />
}

// ❌ Avoid when handler is simple
function Component() {
  const handleClick = () => console.log('clicked')
  return <Button onClick={handleClick} />
}
```

### State Management
1. Minimize useState usage - only use when necessary
2. Prefer local component state over global state when possible
3. Use controlled components for form state
4. Consider reducers for complex state logic

### Side Effects
1. Minimize useEffect usage - only use when necessary
2. Always specify dependency arrays in useEffect
3. Keep effects focused on a single concern
4. Clean up side effects when component unmounts

### Code Organization
1. Group related files together in feature-based directories
2. Keep utility functions in dedicated files under `lib/` or `utils/`
3. Maintain clear separation between UI components and business logic

### Comments and Documentation
1. Don't add unnecessary UI section comments
2. Document complex business logic or non-obvious solutions
3. Use JSDoc comments for public APIs and important functions

## Debugging Process

### Problem Definition
1. Before making changes, clearly define:
   - Current behavior
   - Desired behavior
   - Specific conditions that trigger the issue

### State Management Issues
1. Document the current state flow
2. Identify all state updates and their triggers
3. Track state changes through component lifecycle
4. Consider state management alternatives if current approach is too complex

### Debugging Steps
1. Start with a clean state
2. Make one change at a time
3. Document the effect of each change
4. If a change doesn't work, revert before trying next approach
5. Keep track of attempted solutions and their outcomes

## Refactoring Guidelines

### Core Principles
1. Maintain Functionality
   - Preserve existing behavior and outputs
   - Verify through testing
2. Improve Readability
   - Use clear, descriptive names
   - Simplify complex logic
   - Follow language idioms
3. Enhance Maintainability
   - Reduce code duplication
   - Follow SOLID principles
   - Apply appropriate design patterns
4. Optimize Performance
   - Only optimize identified bottlenecks
   - Balance with readability

### Refactoring Strategies
1. Code Simplification
   - Eliminate redundant code
   - Replace complex conditionals
   - Optimize loops and iterations
2. Modularization
   - Extract to smaller functions
   - Group related functionality
3. Clean Code
   - Use descriptive names
   - Document complex logic
   - Remove dead code
   - Replace magic numbers

## Architecture and Build

### Stack Requirements
1. Build with idiomatic Remix
2. Use actions and loaders properly
3. Deploy to Vercel
4. Use pnpm as package manager

### UI and Design
1. Use Tailwind for styling
2. Implement minimalistic UI approach
3. Support dark theme with light mode option
4. Use shadcn/UI library components
   ```zsh
   pnpm dlx shadcn@latest add [component-name]
   ```

### Package Management
1. Use Remix-compatible packages
2. Prefer TypeScript-supported packages
3. Use pnpm instead of npm for package management

## Performance and Testing
1. Memoize expensive calculations with useMemo when necessary (don't preoptimize)
2. Use useCallback for function props passed to memoized child components
3. Implement virtualization for long lists
4. Write tests for critical business logic
5. Focus on user behavior in component tests
6. Use meaningful test descriptions
7. Follow Arrange-Act-Assert pattern