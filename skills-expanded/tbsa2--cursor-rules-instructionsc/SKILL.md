---
description: 
globs: 
alwaysApply: true
---
# Expert Guidelines

You are an expert in TypeScript, Node.js, Next.js App Router, React, Shadcn UI, Radix UI and Tailwind.

Code Style and Structure

- Write concise, technical TypeScript code with accurate examples.
- Use functional and declarative programming patterns; avoid classes.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).
- Structure files: exported component, subcomponents, helpers, static content, types.
- Use console.log({value}) instead of console.log(value)
- Use onCallback instead of handleCallback

Naming Conventions

- Use lowercase with dashes for directories (e.g., components/auth-wizard).
- Favor named exports for components.

TypeScript Usage

- Use TypeScript for all code; prefer types over interfaces.
- Avoid maps; use enums instead.
- Use functional components with TypeScript types.
- When creating functionality for backend, create services that incapsulate the logic and are easier to test
- Prefer using Prisma types over recreating them from scrach 
- Prisma type are now imported from  "@prisma/client/wasm" 
- Writing tests it's like your second nature, each time you create a new functionality you will write at least 2-3 tesets, and will look into edge cases to cover them as well 
- When writing tests create mocks for services in separate files so we can import them, also for objects, for objects create them using faker 
- Use constants instead of magic numbers, and the constants live in their own files in a separate folder

Syntax and Formatting

- Use the "function" keyword for pure functions.
- Avoid unnecessary curly braces in conditionals; use concise syntax for simple statements.
- Use declarative JSX.

UI and Styling

- Use Shadcn UI, Radix, and Tailwind for components and styling.
- Implement responsive design with Tailwind CSS; use a mobile-first approach.

Performance Optimization

- Minimize 'use client', 'useEffect', and 'setState'; favor React Server Components (RSC).
- Wrap client components in Suspense with fallback.
- Use dynamic loading for non-critical components.
- Optimize images: use WebP format, include size data, implement lazy loading.

Key Conventions

- Optimize Web Vitals (LCP, CLS, FID).
- Limit 'use client':
  - Favor server components and Next.js SSR.
  - Use only for Web API access in small components.
  - Avoid for data fetching or state management.

Follow Next.js docs for Data Fetching, Rendering, and Routing.

---