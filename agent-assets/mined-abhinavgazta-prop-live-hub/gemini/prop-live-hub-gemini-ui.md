# UI Components

This directory contains reusable UI components built on top of [Radix UI](https://www.radix-ui.com/) and styled with [Tailwind CSS](https://tailwindcss.com/). We follow the [Shadcn UI](https://ui.shadcn.com/) pattern.

## Guidelines

- **Atomic Components:** Keep components focused and reusable. Use `class-variance-authority` (CVA) for managing component variants.
- **Composition:** Prefer composition over large, complex components with many props. Use the `Slot` component from `@radix-ui/react-slot` when a component needs to be "polymorphic" (e.g., a button that can also be a link).
- **Styling:** Use Tailwind CSS utility classes. Avoid hardcoded colors or spacing; instead, use the theme variables defined in `src/styles.css`.
- **Accessibility:** Ensure all components are accessible. Since we use Radix UI, many accessibility features are built-in, but always verify ARIA attributes and keyboard navigation.
- **Utils:** Use the `cn` utility from `@/lib/utils` for merging Tailwind classes safely.

## Adding New Components

When adding a new Shadcn UI component, use the CLI or copy the implementation from the Shadcn UI documentation. Ensure it follows the existing patterns in this directory.

```bash
# Example (if shadcn-ui CLI is configured)
npx shadcn-ui@latest add [component-name]
```

## Naming Convention

- Use PascalCase for component names (e.g., `Button.tsx`, `Dialog.tsx`).
- Sub-components should be exported as properties of the main component when appropriate (e.g., `Dialog.Title`, `Dialog.Content`).
