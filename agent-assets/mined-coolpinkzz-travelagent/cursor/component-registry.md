---
description: Controlled UI registry — no arbitrary generated UI
globs: src/agent/**/*.ts,src/agent/**/*.tsx,src/components/travel/**/*.tsx
alwaysApply: false
---

# Component registry

Add a new agent-facing UI capability in this order:

1. Add a props type and component name in `src/agent/types.ts`
2. Build a presentational component in `src/components/travel`
3. Register it in `src/agent/registry.ts`
4. Emit a `ui` event from the demo script, tool mapper, or the Zod-validated `emit_ui` tool

```ts
// ❌ BAD — model returns markup
{ type: 'html', content: '<div>Flights</div>' }

// ✅ GOOD — model selects a capability
{ type: 'ui', component: 'transport', props: { options } }
```
