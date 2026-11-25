---
name: react-component-scaffold
description: |
  Scaffold a React component with co-located tests, stories, and CSS module.
  Triggers on "create component", "scaffold component", "new component", "generate component".
metadata:
  type: tool
  version: "1.0.0"
  author: community
  tags: [react, component, scaffolding, typescript]
triggers:
  - "create component"
  - "scaffold component"
  - "new component"
  - "generate component"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# React Component Scaffold

Scaffold React components with tests, stories, and styles in one shot.

## When to Use
- Creating a new React component from scratch
- User says "create a component", "scaffold a component"
- Need consistent component file structure across a project

## When NOT to Use
- Modifying existing components
- Non-React component files
- The project has a code generator already (e.g., Plop, Hygen)

## Workflow
1. Ask user: component name, props (if known), and which optional files to generate
2. Detect or ask: JavaScript or TypeScript, CSS Modules or styled-components
3. Generate files:

```
ComponentName/
├── ComponentName.tsx          # Component with typed props
├── ComponentName.test.tsx     # Basic render + interaction tests
├── ComponentName.stories.tsx  # Storybook story (if project uses Storybook)
├── ComponentName.module.css   # CSS Module (if using CSS Modules)
└── index.ts                   # Barrel export
```

4. Write the component with:
   - Typed props interface
   - Default exports
   - Accessibility attributes (aria-label, role)
   - Loading/empty/error states if data-dependent

## Component Template
```tsx
import { type FC } from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  /** Button label text */
  children: string;
  /** Visual variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Disabled state */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
}

export const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      disabled={disabled}
      onClick={onClick}
      type="button"
    >
      {children}
    </button>
  );
};
```

## Key Principles
- One component per folder — co-locate all related files
- Always include a barrel export (`index.ts`)
- Props interface should be exported (for consumers)
- Add JSDoc comments for each prop
- Use `type="button"` on buttons to prevent form submission

## Notes
- Follow the project's existing patterns — don't introduce new conventions
- If Storybook isn't used, skip the stories file
- Run `npm run lint` after generating to ensure compliance
