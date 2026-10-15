---
name: mount-operations
description: Framework mount development workflows for React, Vue, Angular, Svelte, and other frameworks. Use when creating framework-specific mount kits, integrating 3Lens with frameworks, or debugging mount kit issues.
---

# Mount Operations

Mount operations cover framework-specific integration patterns for 3Lens, enabling framework developers to integrate 3Lens into their applications.

## When to Use

- Creating a mount kit for a new framework
- Integrating 3Lens into a React/Vue/Angular/Svelte app
- Debugging mount kit issues
- Understanding framework integration patterns

## Framework Mount Kits

### React Mount Kit

```typescript
// packages/mounts/react/src/index.ts
import { createLensContext } from './provider';

export { createLensContext, useLens } from './provider';

// Usage in React app
import { LensProvider, useLens } from '@3lens/mount-react';

function App() {
  return (
    <LensProvider>
      <MyComponent />
    </LensProvider>
  );
}

function MyComponent() {
  const lens = useLens();
  // Use lens client
}
```

### Vue Mount Kit

```typescript
// packages/mounts/vue/src/index.ts
import { useThreeLens, provideThreeLens } from './composables';

export { useThreeLens, provideThreeLens };

// Usage in Vue app
import { provideThreeLens, useThreeLens } from '@3lens/mount-vue';

export default {
  setup() {
    provideThreeLens();
    const lens = useThreeLens();
    // Use lens client
  }
};
```

### Angular Mount Kit

```typescript
// packages/mounts/angular/src/index.ts
import { LensService } from './lens.service';
import { LensComponent } from './lens.component';

export { LensService, LensComponent };

// Usage in Angular app
import { LensService } from '@3lens/mount-angular';

@Component({ /* ... */ })
export class MyComponent {
  constructor(private lens: LensService) {}
}
```

### Svelte Mount Kit

```typescript
// packages/mounts/svelte/src/index.ts
import { lensStore } from './store';
import { useLens } from './actions';

export { lensStore, useLens };

// Usage in Svelte app
import { lensStore, useLens } from '@3lens/mount-svelte';

useLens();
$lensStore.client.query(/* ... */);
```

## Commands

### Scaffold a Mount Kit

```bash
# Create a new mount kit
3lens scaffold mount react
3lens scaffold mount vue
3lens scaffold mount angular
3lens scaffold mount svelte
```

Generates:
- Package structure
- Framework-specific provider/context
- Hooks/composables/components
- Type definitions
- README with examples

## Agent Use Cases

1. **New framework**: "Create a mount kit for Solid.js"
2. **Integration**: "How do I use 3Lens in my React app?"
3. **Debugging**: "My mount kit isn't working, help debug"
4. **Best practices**: "What's the best way to integrate 3Lens?"

## Mount Kit Requirements

Every mount kit MUST:

1. **Only depend on UI Core and Runtime**
   - Never import from kernel directly
   - Use public client API only

2. **Provide Framework-Specific APIs**
   - React: Hooks (`useLens`)
   - Vue: Composables (`useThreeLens`)
   - Angular: Services (`LensService`)
   - Svelte: Stores (`lensStore`)

3. **Integrate with UI Core**
   - Use `@3lens/ui-web` components
   - Support overlay/dock/panel modes

4. **Support Live and Offline Modes**
   ```typescript
   const data = client.isLive 
     ? await client.queryLive(query, params)
     : await client.queryTrace(query, params);
   ```

5. **Handle Errors Gracefully**
   ```typescript
   try {
     const lens = createLens();
   } catch (error) {
     if (error.code === 'CSP_BLOCKED') {
       // Handle CSP blocking
     }
   }
   ```

## Integration Patterns

### Provider Pattern (React/Angular)

```typescript
// Create provider/context at app root
<LensProvider>
  <App />
</LensProvider>

// Use hook/service in components
const lens = useLens();
```

### Composition Pattern (Vue)

```typescript
// Provide at app root
provideThreeLens();

// Use composable in components
const lens = useThreeLens();
```

### Store Pattern (Svelte)

```typescript
// Initialize store
useLens();

// Use store in components
$lensStore.client.query(/* ... */);
```

## Post-Scaffold Steps

After scaffolding, follow the playbook:
- [.cursor/playbooks/add-a-mount-kit.md](../../../.cursor/playbooks/add-a-mount-kit.md)

## Additional Resources

- Contract: [.cursor/contracts/runtime-boundaries.md](../../../.cursor/contracts/runtime-boundaries.md)
- Contract: [.cursor/contracts/ui-surfaces.md](../../../.cursor/contracts/ui-surfaces.md)
- Rule: [.cursor/rules/mount-standards.mdc](../../../rules/mount-standards.mdc)
- No scaffold command; follow [add-a-mount-kit playbook](../../../.cursor/playbooks/add-a-mount-kit.md) manually