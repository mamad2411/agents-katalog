---
description: General development rules for The Yard Thai website project
globs:
alwaysApply: true
---

# The Yard Thai Website - Development Rules

## Tech Stack

### Framework

- **Next.js 15** with App Router
- Use `src/` directory structure
- All routing must follow App Router conventions

### Language

- **TypeScript** for all code
- All generated code must be type-safe
- Use proper TypeScript interfaces and types
- Avoid `any` types unless absolutely necessary

### Package Manager

- Use **pnpm** for all package management
- Always use `pnpm` commands instead of npm or yarn

## Styling and UI

### Styling Engine

- **Tailwind CSS ONLY** for all styling
- **FORBIDDEN**: Separate CSS files, CSS Modules, or inline style objects
- Use Tailwind utility classes exclusively
- Leverage Tailwind's design system and spacing scale

### Component Library

- Use **shadcn/ui** for all standard UI components
- **First step**: Always provide the correct CLI command to add components:
  ```bash
  pnpm dlx shadcn-ui@latest add [component-name]
  ```
- Examples: `pnpm dlx shadcn@latest add button`, `pnpm dlx shadcn@latest add card`
- Import and use shadcn/ui components in generated code
- Customize shadcn/ui components using Tailwind classes

### Icons

- **lucide-react** for all icons
- Import icons from `lucide-react`
- Use semantic icon names that clearly represent their purpose

### Color Palette

- **MANDATORY**: Use the Thai-inspired color palette for all components
- **Primary (Golden Yellow)**: `#F4D03F` 🟨 — Use for primary buttons, links, and important headings (bright golden turmeric, Thai curry)
- **Secondary (Warm Amber)**: `#F39C12` 🟡 — Use for secondary buttons or highlight backgrounds (vibrant saffron, golden spices)
- **Accent (Terracotta)**: `#E67E22` 🟤 — Use sparingly for special tags, icons, or decorative elements (warm golden earth, clay pottery)
- **Neutral (Light Cream)**: `#FEFBF6` ⬜️ — Use for backgrounds (easier on eyes than pure white)
- **Text (Charcoal)**: `#8B4513` ⬛️ — Use for all text content (rich golden brown, dark earth)

#### Color Usage Guidelines

- **CSS Custom Properties**: Use `var(--golden-yellow)`, `var(--warm-amber)`, etc. in Tailwind classes
- **Semantic Mapping**: Leverage the semantic color variables (`--primary`, `--secondary`, etc.)
- **Hover States**: Use warm amber and terracotta for interactive hover effects
- **Accessibility**: Ensure sufficient contrast ratios for all color combinations
- **Consistency**: Never use arbitrary colors outside this palette without approval

## Code Style and Principles

### File Naming

- **kebab-case** for all file and folder names
- Examples: `user-profile.tsx`, `contact-form.tsx`, `api-routes/`
- No camelCase or PascalCase for file names

### Component Structure

- **Functional components** using React Hooks
- Break down complex components into smaller, reusable pieces
- Use custom hooks for complex logic
- Prefer composition over inheritance

### Design Philosophy

- **Mobile-first approach** for all components and layouts
- Code must work perfectly on small screens first
- Use Tailwind responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- Progressive enhancement for larger screens

### Accessibility

- Use **semantic HTML5** tags: `<nav>`, `<main>`, `<footer>`, `<section>`, `<article>`, etc.
- Include appropriate `aria-` attributes where necessary
- Ensure proper heading hierarchy (h1, h2, h3, etc.)
- Provide alt text for images

## Next.js Best Practices

### Server vs Client Components

- **Default to Server Components**: Use server components by default for better performance, SEO, and reduced bundle size
- **Use Client Components Only When Needed**: Only add "use client" when you need:
  - Event handlers (onClick, onSubmit, etc.)
  - State management (useState, useEffect, etc.)
  - Browser APIs or third-party libraries requiring client-side execution
  - Interactive UI components (forms, modals, dropdowns)

### Image Optimization

- **Always use Next.js Image component** instead of regular `<img>` tags or CSS background images
- **Include proper alt text** for accessibility and SEO
- **Use appropriate props**:
  - `priority` for above-the-fold images
  - `fill` with `object-cover` for background-style images
  - `sizes` for responsive images
  - `placeholder="blur"` for loading states when appropriate

### Performance Optimization

- **Leverage Server-Side Rendering**: Render static content on the server for better initial load times
- **Use Static Generation**: Pre-render pages at build time when possible
- **Optimize Bundle Size**: Minimize client-side JavaScript by using server components
- **Implement Proper Caching**: Use Next.js caching strategies for API routes and data fetching

### SEO and Accessibility

- **Server Components for SEO**: Server-rendered content is immediately available to search engines
- **Semantic HTML**: Use proper HTML5 semantic elements
- **Meta Tags**: Implement proper metadata in layout.tsx and page.tsx files
- **Structured Data**: Add JSON-LD structured data when appropriate

## Git Commit Messages

### Conventional Commits Specification

Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for all commit messages.

### Commit Message Structure

Every commit message must have:

1. **Subject line (title)**:

   - Start with a type: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`
   - Maximum 50 characters
   - Use imperative mood ("add feature" not "added feature")
   - No period at the end

2. **Single blank line** separating subject from body

3. **Optional body (description)**:
   - Explain the "what" and "why" of the change
   - Wrap at 72 characters
   - Use bullet points for multiple changes

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

### Examples

```
feat: add user authentication system

Implement login and registration functionality with JWT tokens.
Includes form validation and error handling.

fix: resolve mobile navigation menu overlap

The mobile menu was overlapping with page content on small screens.
Added proper z-index and positioning to fix the issue.

chore: update dependencies

Update Next.js to version 15.1.0 and Tailwind CSS to 3.4.0.
```

### Breaking Changes

- Use `!` after type/scope for breaking changes: `feat!: remove deprecated API`
- Or use `BREAKING CHANGE:` in the footer
- Explain what breaks and how to migrate

## General Guidelines

- Write clean, readable, and maintainable code
- Add comments for complex business logic
- Use meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Test components thoroughly before committing
- Follow React best practices and patterns
