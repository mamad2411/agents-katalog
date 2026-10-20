---
name: Node.js Standards
description: Essential Node.js development standards and best practices
alwaysApply: false
globs: "**/*.{js,ts,mjs,cjs,json}"
---

# Node.js Standards

## Code Quality
- Use modern ES6+ syntax (const/let, async/await, destructuring)
- Handle errors explicitly with try/catch blocks
- Use meaningful names for variables and functions
- Keep functions small and focused

## Security & Performance  
- Never commit secrets - use environment variables
- Validate all inputs and sanitize user data
- Use async operations to avoid blocking the event loop
- Clean up resources (connections, listeners, timers)

## Dependencies
- Keep dependencies updated and minimal
- Separate dev and production dependencies
- Use exact versions for critical dependencies