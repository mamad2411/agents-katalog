# Development Guidelines

- Stack: React, Tailwind CSS, JavaScript/TypeScript
- Code Style: Clean, modular, and responsive UI components
- Version Control: Use Conventional Commits standard

# Project Rules & AI Guidelines (`CLAUDE.md`)

## 1. Form Validation Standard
- All interactive form components MUST use `react-hook-form` integrated with `@hookform/resolvers/zod`.
- Uncontrolled inputs, plain `useState` forms, or raw HTML5 validation without a Zod validation schema are strictly forbidden.

## 2. Mandatory Accessibility (a11y) Tags
- Every form control MUST feature an explicit `id` matching its corresponding `<label htmlFor="...">`.
- Invalid fields MUST programmatically set `aria-invalid="true"` when errors exist and bind to their error text container using `aria-describedby="{field}-error"`.

## 3. Asynchronous UI Boundaries
- All submit controls and input fields MUST set `disabled={isSubmitting}` during asynchronous processing to prevent duplicate request dispatches.
