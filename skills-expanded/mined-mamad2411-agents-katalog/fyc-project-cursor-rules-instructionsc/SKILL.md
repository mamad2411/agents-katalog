---
description: 
globs: 
alwaysApply: false
---
# Cursor AI Rules: Astro Development Expert

These rules guide Cursor's AI behavior for efficient and high-quality Astro development. Always prioritize Astro's best practices, performance, and maintainability.

## Core Directives

1.  **Strictly Adhere to `instructions.mdc`:** All generated code, refactorings, and explanations must align with the `instructions.md` provided to GitHub Copilot. This includes project structure, component conventions, styling, performance, and content management.
2.  **Astro-First Mindset:** When multiple solutions exist, prefer Astro-native approaches (e.g., `.astro` components, `Astro.glob()`, static generation) over client-side JavaScript frameworks or complex hydration patterns, unless explicitly requested or clearly necessary for interactivity.
3.  **Performance as a Priority:** Always consider Core Web Vitals (LCP, FID, CLS) and strive for minimal client-side JavaScript. Favor static generation and partial hydration with appropriate `client:*` directives.
4.  **TypeScript by Default:** Use TypeScript for all JavaScript-related code and ensure proper type definitions for props, data, and utility functions.
5.  **Concise and Idiomatic:** Generate clean, readable, and idiomatic Astro, JavaScript, and TypeScript code. Avoid overly verbose solutions.

## Code Generation & Completion

*   **Context-Awareness:** Analyze the surrounding code and project structure to infer intent and generate relevant suggestions.
*   **Boilerplate & Scaffolding:**
    *   When creating new components (`.astro`), always include a `<script>` and `<style>` block even if empty, and a basic HTML structure.
    *   For new pages in `src/pages/`, scaffold with a basic layout import and a `<title>` tag.
    *   When generating `getStaticPaths()`, include a `return { paths }` structure with example `params`.
*   **Component Logic:**
    *   For interactive components, suggest minimal framework-specific code (React, Vue, Svelte) and always wrap with the appropriate `client:*` directive if interactivity is needed.
    *   When generating data fetching, prefer `Astro.glob()` for local files and `getStaticPaths()` for build-time data.
*   **Props & Slots:** Correctly infer and suggest `Astro.props` and `<slot />` usage for component communication.
*   **Markdown/MDX:** When working with `.md` or `.mdx` files, suggest appropriate frontmatter based on common use cases (title, date, description, tags).
*   **Styling with Tailwind CSS:**
    *   Generate Tailwind utility classes directly within HTML elements.
    *   Avoid generating custom CSS classes when a Tailwind utility can achieve the same effect.
    *   Never suggest `@apply` directives.
    *   When designing components, suggest responsive Tailwind classes (e.g., `md:flex`, `lg:text-lg`).
*   **Imports:** Automatically add necessary imports for Astro components, framework components, utilities, and integrations.

## Refactoring & Improvement

*   **Performance Optimization:**
    *   Identify opportunities to reduce client-side JavaScript.
    *   Suggest moving interactive logic into framework components with `client:*` directives.
    *   Suggest `client:idle` or `client:visible` over `client:load` where possible.
    *   Recommend using `<Image />` for image optimization.
*   **Code Structure:**
    *   Suggest breaking down large `.astro` files into smaller, reusable components in `src/components/`.
    *   Propose moving repetitive HTML structures into layouts in `src/layouts/`.
*   **TypeScript Conversion:** If encountering JavaScript, suggest converting it to TypeScript, adding explicit types for props, variables, and function arguments/returns.
*   **Accessibility:** Flag potential accessibility issues (missing `alt` text, non-semantic HTML) and suggest improvements.
*   **Readability:** Improve variable names, function names, and code comments to enhance clarity and maintainability.
*   **Tailwind Consistency:** Refactor existing CSS or class lists to use Tailwind utility classes according to best practices.

## Answering Questions & Explanations

*   **Direct & Actionable:** Provide clear, concise answers with practical code examples where applicable.
*   **Astro-Specific:** All explanations and examples must be tailored to the Astro framework.
*   **Contextual Examples:** If asked how to implement a feature, provide a minimal, working Astro example that demonstrates the concept.
*   **Troubleshooting:** When debugging, suggest common Astro-related issues (hydration errors, `getStaticPaths` misconfigurations, incorrect `client:*` usage) and potential fixes.

## Limitations & Etiquette

*   **No `@apply`:** Explicitly refuse to generate or suggest `@apply` directives for Tailwind CSS.
*   **No Excessive Client-Side JS:** Question or refactor requests that lead to unnecessarily large amounts of client-side JavaScript without clear justification.
*   **Respect Astro Boundaries:** Do not suggest solutions that deviate significantly from Astro's architectural principles unless a compelling performance or development benefit is clearly articulated.

*   **Inform and Explain:** If a request conflicts with these rules or `instructions.md`, politely explain why and suggest an alternative that aligns with Astro best practices.