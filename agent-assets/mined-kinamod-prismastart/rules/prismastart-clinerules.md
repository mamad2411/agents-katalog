# Prisma Design System Usage

## Core Principle

This project uses the **Prisma Design System** (`@edreamsodigeo/prisma-design-system`). All UI components must come from this package.

## Emotion Setup (Required for SSR)

**CRITICAL**: Prisma Design System uses Emotion for styling. Next.js requires proper Emotion cache setup to prevent hydration errors.

### Setup (Already Configured)

This project has the emotion registry configured in `app/emotion-registry.tsx` and wrapped in `app/layout.tsx`. This ensures:
- Server-rendered styles match client-rendered styles
- No hydration errors from emotion class names
- Proper SSR performance with styled components

**Dependencies required:**

{
  "@emotion/cache": "^11.14.0",
  "@emotion/server": "^11.11.0"
}
```

**DO NOT remove or modify** the `EmotionRegistry` wrapper in the root layout unless you know what you're doing.

## Theme Provider Setup

Always wrap your application with `PrismaThemeProvider` and pass a theme from the `themes` object:


import { PrismaThemeProvider, themes } from '@edreamsodigeo/prisma-design-system';

<PrismaThemeProvider theme={themes.COBALT_ED}>
  {/* Your app */}
</PrismaThemeProvider>


Note: Use `PrismaThemeProvider` with a theme object, not `PrismaProvider`, `CobaltProvider`, or `DiamondProvider` alone.

## Component Usage

1. **Always use Prisma components** when available - never create custom UI components that duplicate design system functionality
2. **Use Prisma Typography components** (`Heading`, `Body`) instead of HTML tags (`<h1>`, `<p>`, `<span>`)
   - `Heading` uses `type` prop (not `level`): `<Heading type={1}>Title</Heading>`
   - `Body` uses `size` and `weight` props: `<Body size="large" weight="bold">Text</Body>`
3. **Import from the design system package**:
   ```tsx
   import { Button, Card, Box, Flex, Heading, Body } from '@edreamsodigeo/prisma-design-system';
   ```

## Styling

- Use the `sx` prop for component styling (Emotion/styled-system)
- Prefer Prisma's layout components (`Box`, `Flex`) over custom CSS
- Only write custom CSS for application-specific needs not covered by the design system

## Avoiding Hydration Errors (Next.js)

**CRITICAL**: Prevent hydration mismatches between server and client rendering.

### Common Causes & Solutions

1. **State Initialization**
   - ❌ WRONG: `const [value, setValue] = useState(Math.random())`
   - ✅ CORRECT: Initialize state consistently or use `useEffect` for client-only values

2. **Component Libraries with State**
   - ❌ WRONG: `<Modal isOpen={isOpen} />` (custom prop names)
   - ✅ CORRECT: Use library's hooks (e.g., `useModal()`) that handle SSR properly
   - Example: Prisma Modal uses `useModal()` hook and spreads `modalProps`

3. **Conditional Rendering**
   - ❌ WRONG: `{typeof window !== 'undefined' && <Component />}`
   - ✅ CORRECT: Use `useEffect` or `'use client'` with proper state initialization

4. **Date/Time Formatting**
   - ❌ WRONG: `{new Date().toLocaleString()}` (varies by timezone)
   - ✅ CORRECT: Format dates in `useEffect` or pass from server as props

5. **Random Values**
   - ❌ WRONG: `{Math.random()}` or `{Date.now()}` in render
   - ✅ CORRECT: Generate in `useEffect` or use stable IDs from props

6. **Browser-Only APIs**
   - ❌ WRONG: `const width = window.innerWidth`
   - ✅ CORRECT: Access in `useEffect` with proper state updates

### Best Practices

- **Use library hooks properly**: Don't create custom prop names for state (like `isOpen`) when the library provides hooks
- **Client-only state**: Initialize client-specific state in `useEffect`, not during render
- **Test SSR**: Ensure components render identically on server and client
- **Check props**: Ensure all props passed to components are serializable and consistent

### Example: Proper Modal Usage


// ✅ CORRECT - Using Prisma's useModal hook
const modal = useModal();

<Modal {...modal.modalProps}>
  <ModalHeader onClose={modal.close}>Title</ModalHeader>
  <ModalContent>Content</ModalContent>
</Modal>

// ❌ WRONG - Custom state management
const [isOpen, setIsOpen] = useState(false);
<Modal isOpen={isOpen} onClose={() => setIsOpen(false)} />
```

## When in Doubt

- Check what components are available in `@edreamsodigeo/prisma-design-system`
- Prefer composition over creation
- Ask if unsure which Prisma component to use
- Always use design system hooks (like `useModal`) instead of custom state management
