---
name: react-forge
description: Generate production-ready React components with React Query, design tokens, and enterprise standards
category: software-development
triggers:
  - "create a react component"
  - "build react screen"
  - "generate react"
---

# React Component Generation

Generate complete React features following enterprise patterns.

## Instructions

1. Read `agents/react-forge.md` for the full React code generation workflow
2. Read `react/REACT_QUERY_RULES.md` — React Query is MANDATORY for all GET requests
3. Read `react/COMPONENT_ARCHITECTURE.md` for component patterns
4. Data fetching at the leaf level — each component fetches its own data via React Query
5. Reuse existing components — search codebase first, refactor god components
6. Always include: Component + Hooks + QueryOptions + Service + Tests (8 files)
7. Handle loading, error, empty states on every component
8. Financial formatting: currency symbol symbol, locale-specifics (currency symbol1,23,456.78)
