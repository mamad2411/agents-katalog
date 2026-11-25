---
name: component-gen
description: Generates a React/Vue/Svelte component with props, types, tests, and stories
argument-hint: <ComponentName> [description]
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## Generate Component

Component name: **$1**
Description: **$2**

1. Detect stack:
```bash
cat package.json | grep -E '"react"|"vue"|"svelte"|"next"|"nuxt"'
ls src/components/ 2>/dev/null | head -5
```

2. Read 2 existing components to match:
   - File structure and naming
   - Import style
   - CSS approach (Tailwind, CSS modules, styled-components)
   - Export style (default vs named)

3. Generate the component:
   - TypeScript props interface
   - Component with proper typing
   - Default prop values where sensible
   - Accessibility attributes (aria-*, role, etc.)

4. Generate test file matching project test style.

5. If Storybook is present (`ls .storybook/`), generate a story too.

6. Place files in the correct directory following project conventions.

Summary: list all created files.
