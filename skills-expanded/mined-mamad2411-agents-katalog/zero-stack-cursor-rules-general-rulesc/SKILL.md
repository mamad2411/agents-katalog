---
description: 
globs: 
alwaysApply: false
---
# General Project Rules

## Version Control
- Commit messages should follow Conventional Commits format (e.g., feat: add user login page).
- Branch names: feature/[ticket-id]-short-description (e.g., feature/FE-101-user-profile-display).

## Coding Style
- Adhere to the project's Prettier configuration for automated code formatting.
- Follow ESLint rules defined in .eslintrc.js.
- Code should be self-documenting where possible; add JSDoc/TSDoc comments for complex functions and public APIs.

## Security
- Sanitize all user inputs on backend.
- Use parameterized queries or ORM methods to prevent SQL injection.
- Implement CSRF protection for web applications.
- Be mindful of OWASP Top 10 vulnerabilities during development.

- Store secrets and API keys securely, never in version control.