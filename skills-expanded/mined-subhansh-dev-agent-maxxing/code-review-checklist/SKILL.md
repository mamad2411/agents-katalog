---
name: code-review-checklist
description: Ship-ready code review checklist covering correctness, readability, security, performance, and frontend/backend specifics.
---

# Code Review Checklist

Before shipping any code, run through this.

## Does It Work?

- Runs without errors
- Handles the happy path
- Handles edge cases (null, empty, 0, negative, very large)
- Handles errors gracefully (try/catch, validation)
- No console.logs or debug code left in

## Is It Readable?

- Variable names are descriptive (not `x`, `temp`, `data2`)
- Functions do one thing
- No magic numbers (use constants)
- Comments explain "why", not "what"
- Consistent style with existing codebase

## Is It Safe?

- No SQL injection / XSS / path traversal
- No hardcoded credentials
- No secrets in logs or error messages
- Input validation on user-facing endpoints
- Rate limiting on public APIs

## Is It Performant?

- No N+1 queries
- No unnecessary re-renders (React)
- No blocking operations on main thread
- Lazy loading for heavy resources
- Pagination for large datasets

## Is It Maintainable?

- No code duplication (DRY)
- Clear separation of concerns
- Error messages are helpful
- Configuration is externalized
- Dependencies are pinned

## Frontend-Specific

- Accessible (ARIA labels, keyboard nav, contrast)
- Responsive (mobile, tablet, desktop)
- Loading states for async operations
- Error states with recovery paths
- Empty states that guide the user
- No layout shift (CLS)
- 60fps animations (transform + opacity only)

## Backend-Specific

- Database migrations are reversible
- API responses are consistent
- Rate limiting is in place
- Logging is sufficient for debugging
- Health check endpoint exists
- Graceful shutdown handling
