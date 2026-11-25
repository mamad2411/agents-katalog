# Strudel Sequencer - Cursor AI Rules

## Project Overview

A fully-featured React step sequencer built on top of Strudel (TidalCycles for the web).

## Architecture

### Folder Structure

- `src/app/` - Main application component
- `src/audio/` - Audio engine modules (engine, scheduler, helpers)
- `src/components/` - Atomic design components (atoms, molecules, organisms, pages)
- `src/hooks/` - Custom React hooks for state management
- `src/styles/` - TailwindCSS 4 styles with @apply patterns
- `src/utils/` - Utility functions
- `src/types/` - Constants and type definitions

### Design Patterns

- **Atomic Design**: Components organized by complexity (atoms → molecules → organisms → pages)
- **Custom Hooks**: State management and side effects encapsulated in reusable hooks
- **Separation of Concerns**: Audio logic, UI logic, and state management are clearly separated
- **No State Library**: Uses only React hooks and local component state

## Code Quality Standards

### Components

- All components must have PropTypes validation
- All components must have JSDoc comments
- No component should exceed ~300 lines
- Use semantic class names from `components.css` instead of inline Tailwind utilities
- Follow atomic design principles strictly

### Styling

- Use TailwindCSS 4 with `@apply` patterns in `components.css`
- Do NOT use custom classes in `@apply` directives (TailwindCSS 4 limitation)
- Use SCSS-style nesting in CSS files
- Extract frequently reused styles into component classes
- Match the POC's visual style (dark UI, translucent panels, outlines, gradients, shadows)

### Hooks

- All hooks must have JSDoc comments
- Hooks should be single-purpose and reusable
- Use `useCallback` and `useMemo` appropriately for performance

### Audio Engine

- Audio logic must be in `src/audio/` modules
- All audio functions must have JSDoc comments
- Use npm imports for Strudel packages (no CDN)

## Technical Stack

- **Vite 7** - Build tool
- **React 19** - UI framework
- **TailwindCSS 4** - Styling with @tailwindcss/vite
- **ESLint 9** - Code linting (flat config format)
- **Prettier** - Code formatting
- **PropTypes** - Runtime type checking
- **Strudel** - Audio engine (@strudel/core, @strudel/mini, @strudel/webaudio)

## Important Constraints

### TailwindCSS 4 Limitations

- Cannot use custom classes in `@apply` directives
- Cannot use `group` variant in `@apply` (add `group` class directly to JSX)
- Custom utilities must be defined as direct CSS properties, not in `@apply`
- Animation utilities like `slide-in-from-bottom-4` don't exist - use custom keyframes

### File Naming

- Components: PascalCase (e.g., `ControlBar.jsx`)
- Hooks: camelCase with `use` prefix (e.g., `useSequencerState.js`)
- Utilities: camelCase (e.g., `gridUtils.js`)
- Constants: camelCase (e.g., `constants.js`)

### Import Conventions

- Use explicit `.js` or `.jsx` extensions
- Group imports: React, third-party, local components, hooks, utils, types, styles

## Common Patterns

### Component Structure

```jsx
/**
 * Component description
 * @module path/to/Component
 */

import PropTypes from 'prop-types';
// ... other imports

/**
 * Component JSDoc
 * @param {Object} props - Component props
 * @returns {JSX.Element} Component element
 */
export function ComponentName({ prop1, prop2 }) {
  // Component logic
  return <div className="semantic-class-name">{/* JSX */}</div>;
}

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number,
};
```

### Hook Structure

```javascript
/**
 * Hook description
 * @module hooks/useHookName
 */

import { useState, useEffect } from 'react';

/**
 * Hook JSDoc
 * @param {Type} param - Parameter description
 * @returns {Object} Return value description
 */
export function useHookName(param) {
  // Hook logic
  return { value, setValue };
}
```

## When Making Changes

1. **Always** add PropTypes to new components
2. **Always** add JSDoc comments to new functions/components/hooks
3. **Never** use inline Tailwind classes - use semantic classes from `components.css`
4. **Never** exceed 300 lines per component - split if needed
5. **Always** test that `npm run build` works after CSS changes
6. **Always** follow the atomic design hierarchy

## Testing

- Run `npm run lint` before committing
- Run `npm run build` to verify production build works
- Ensure all PropTypes are correct

## Audio Engine Notes

- Strudel scheduler must be initialized before use
- Sample library loads from remote URL
- Patterns are generated dynamically from grid state
- CPS (cycles per second) is calculated from BPM and beats per bar
