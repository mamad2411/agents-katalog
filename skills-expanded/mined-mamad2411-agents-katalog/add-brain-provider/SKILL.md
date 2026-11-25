---
name: add-brain-provider
description: Add a BYOK or local brain to ZeroAgent Studio. Use when integrating a new AI API or local inference engine.
paths:
  - src/engines/**/*
  - src/lib/brainResolver.ts
  - src/lib/brainLabels.ts
  - src/types/**/*
  - src/components/settings/**/*
  - src/components/inspector/**/*
  - tests/**/*
---

# Add Brain Provider

## Files (in order)

1. `src/engines/<provider>.ts` — `BrainEngine`: `name`, `isAvailable`, `chat`
2. `src/engines/index.ts` — `getEngine()` switch
3. `src/types/index.ts` — `BrainType`, `ApiKeys` if BYOK
5. `src/lib/brainResolver.ts` — `isBrainConfigured()`, `getBrainCostLabel()`; fallback copy if BYOK
6. `src/lib/brainLabels.ts` — `getBrainDisplayName()`
7. `src/components/settings/SettingsPanel.tsx` — key + models (free options first)
8. `src/components/inspector/NodeInspector.tsx` — brain + model dropdown
9. `tests/engines/<provider>.test.ts` — positive, negative, edge (see test-engineer rule)

## BYOK pattern

```typescript
export function createProviderEngine(apiKey: string): BrainEngine {
  return {
    name: 'Provider',
    isAvailable: () => !!apiKey,
    async chat(messages, options) { /* fetch provider */ },
  }
}
```

## Local engine pattern

- Dynamic `import()` for heavy deps
- `createModelLoadCallback()` for download UI
- `isAvailable()` checks WebGPU / browser support
- Prefer smallest default model

## Prometheus

- Register in free-brain selection if usable without key
- Missing key → `brainResolver` fallback, not crash
- Settings: label cost clearly (`Free (local)`, `Free tier`, etc.)

## Validate

```bash
npm run ci
```

Manual: Demo workflow + agent node on new brain; verify activity log on fallback.

**Rules:** `.cursor/rules/zeroagent-engineer.mdc` · `.cursor/rules/zeroagent-test-engineer.mdc`
