---
description:
globs:
alwaysApply: true
---
# Cursor AI State Management Rules: 3D Chess Web Platform

These rules define the standards and best practices for all client-side state management on the 3D Chess Web Platform.

---

## Primary State Management

- Use **Solid Store** for all client-side state management.
- Scope stores by feature or domain to maintain modularity and prevent unnecessary coupling.
- Avoid global singleton stores unless absolutely necessary for cross-cutting concerns.
- Use derived stores for computed or memoized state to optimize performance and maintain clarity.