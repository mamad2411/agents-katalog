---
name: routing-frontend
description: Design and implement frontend routing. Use when planning routes,
  guards, and navigation in SPAs.
metadata:
  tags: routing, frontend
---

# Frontend Routing

## Use this skill when
- Structuring routes, layouts, and nested routes
- Adding auth/authorization guards and lazy loading
- Handling 404s, redirects, and search-state in the URL

## Do not use this skill when
- Server routing (use nextjs-development or backend skills)

## Instructions
1. Model routes after the information architecture, not the components.
2. Make the URL the source of truth for page state (query params).
3. Add route-level guards for authentication and permissions.
4. Lazy-load route chunks.
5. Handle 404 and error routes explicitly.
6. Support deep links and back/forward reliably.
7. Define breadcrumbs and page titles from route metadata.

## Output Format
- Route map | guard matrix | param schema | chunking plan

## Common Mistakes
- Hardcoding navigation instead of using the router
- Guards that depend on client-only state
- State that does not survive a refresh
