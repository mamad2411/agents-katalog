# React Assessment Guidelines

## Code Quality Standards

- Write clean, maintainable React code with proper component structure
- Use modern React patterns (hooks, functional components)
- Follow consistent naming conventions (PascalCase for components, camelCase for functions/variables)
- Add PropTypes or TypeScript types when applicable
- Keep components focused and single-responsibility

## Problem-Solving Approach

- Read requirements carefully before coding
- Break down complex problems into smaller steps
- Test edge cases and handle errors gracefully
- Consider performance implications (unnecessary re-renders, memoization)
- Write self-documenting code with clear variable names
- **Be Mindful of Usage Limits:** For minor, operational code changes, provide the full suggested code or a clear prompt for manual application (to save on usage). For larger code transformations, provide a usage warning and offer to walk through each change step-by-step.

## React-Specific Best Practices

- Avoid prop drilling - consider context or state management when needed
- Use appropriate hooks (useState, useEffect, useMemo, useCallback)
- Clean up side effects in useEffect return functions
- Keep state as local as possible
- Use keys properly in lists (avoid index as key when order changes)

## When Helping Me

- Explain your reasoning briefly
- Point out potential bugs or improvements
- Suggest alternative approaches if relevant
- Help me understand WHY, not just WHAT
- Flag any anti-patterns I should avoid

## Speed & Efficiency

- Provide complete, working code solutions
- Minimize back-and-forth by anticipating common needs
- Include necessary imports
- Consider both the happy path and edge cases

## Common Assessment Patterns to Watch For

- Form handling and validation
- API calls and async data fetching
- Conditional rendering
- List rendering and filtering
- State management across components
- Event handling
- Styling approaches (CSS modules, styled-components, Tailwind, etc.)

## Quick Reference Reminders

- useEffect dependencies: include all values used inside the effect
- Event handlers: use arrow functions or bind to avoid losing context
- Controlled vs uncontrolled components: prefer controlled for forms
- When to lift state up: when multiple components need the same state
