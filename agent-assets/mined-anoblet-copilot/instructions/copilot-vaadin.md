# Vaadin Instructions

This document outlines the standards for using Vaadin components and routing within the workspace.

## Routing

Use `@vaadin/router` for client-side routing in Single Page Applications (SPAs).

### Standard Pattern

Define routes in a dedicated file (e.g., `routes.ts`) or within the main application shell component.

```typescript
import { Router } from '@vaadin/router';

const router = new Router(document.getElementById('outlet'));
router.setRoutes([
  { path: '/', component: 'home-view' },
  { path: '/users', component: 'user-list-view' },
  { path: '(.*)', component: 'not-found-view' },
]);
```

## Components

Use standard Vaadin components to ensure UI consistency across applications.

### Recommended Components

- **Layout**: `vaadin-app-layout`, `vaadin-scroller`, `vaadin-split-layout`
- **Data Display**: `vaadin-grid` (for tabular data)
- **Input**: `vaadin-text-field`, `vaadin-text-area`, `vaadin-checkbox`, `vaadin-select`
- **Action**: `vaadin-button`
- **Feedback**: `vaadin-notification`, `vaadin-progress-bar`

### Usage Guidelines

- Import components individually to minimize bundle size.
- Use TypeScript for all component implementations.
- Avoid using legacy Polymer-based syntax if encountered in older documentation.

## TypeScript Enforcement

All Vaadin-related code must be written in **TypeScript**.
While legacy examples or existing codebases might use JavaScript, new implementations must strictly adhere to the workspace's TypeScript standards.

## Troubleshooting

### CSS Property Registration Error

**Error**: `Uncaught InvalidModificationError: Failed to execute 'registerProperty' on 'CSS': The name provided has already been registered.`

**Cause**: This error typically occurs when there is a mismatch in Vaadin web component versions (e.g., mixing v24 and v25 components), causing conflicting property registrations.

**Resolution**: Ensure all `@vaadin/*` dependencies in `package.json` are aligned to the same patch version using pinned versions (e.g., all `24.6.11`). Run `pnpm install` to deduplicate. Avoid caret ranges (`^`) for Vaadin component packages to prevent transitive dependency drift.
