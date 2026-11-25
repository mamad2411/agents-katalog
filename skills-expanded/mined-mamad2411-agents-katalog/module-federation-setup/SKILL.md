# Module Federation Setup

## Purpose
Configures Module Federation for MFE remote and host applications.

## Role
Frontend Developer

## Phase
Development

## Triggered By
Architect decides MFE pattern during planning.

## Inputs
- Architect's MFE decision and remote/host designation

## Rule
Only implement when Architect explicitly decides MFE during planning.

## Process

### Remote App Configuration (`apps/mfe/{name}/rsbuild.config.ts`)
```typescript
export default defineConfig({
  moduleFederation: {
    options: {
      name: '{remote-name}',
      exposes: {
        './{Module}': './src/modules/{feature}/index.ts',
      },
      shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
    },
  },
})
```

### Host App Configuration
```typescript
export default defineConfig({
  moduleFederation: {
    options: {
      name: 'host',
      remotes: {
        '{remote-name}': '{remote-name}@{remote-url}/remoteEntry.js',
      },
    },
  },
})
```

### bootstrap.tsx (handles async module loading)
```typescript
// Async import to support Module Federation
import('./App').then(({ App }) => {
  ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
})
```

## Outputs
Configured Module Federation remote or host.

## Quality Gates
- [ ] Only configured when Architect decides MFE
- [ ] Remote exposes only the modules explicitly needed
- [ ] Shared singletons configured (react, react-dom)
- [ ] bootstrap.tsx uses async import pattern

## References
- `.claude/skills/frontend-developer/webapp-scaffolding/SKILL.md`
