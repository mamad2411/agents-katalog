---
name: toolchain-node
description: "Node.js/TypeScript project toolchain -- npm/pnpm/yarn, testing, linting, building, and debugging."
metadata: {"thinkfleetbot":{"emoji":"🟢","requires":{"bins":["node"]}}}
---

# Node.js / TypeScript Toolchain

Common commands for Node.js and TypeScript projects.

## Package managers

```bash
# Detect which package manager is used
[ -f pnpm-lock.yaml ] && echo "pnpm" || ([ -f yarn.lock ] && echo "yarn" || echo "npm")
```

```bash
npm install          # or: pnpm install / yarn
npm ci               # Clean install (CI)
npm install lodash   # Add dependency
npm install -D vitest # Add dev dependency
```

## Run scripts

```bash
npm run build
npm run dev
npm test
npm run lint
```

## Testing

```bash
# Jest
npx jest --coverage
npx jest --watch
npx jest path/to/test.ts

# Vitest
npx vitest run
npx vitest run --coverage
npx vitest path/to/test.ts

# Node test runner (built-in)
node --test src/**/*.test.ts
```

## Linting & formatting

```bash
npx eslint . --fix
npx prettier --write .
npx biome check --write .
```

## TypeScript

```bash
npx tsc --noEmit               # Type check only
npx tsc --noEmit --watch        # Watch mode
npx tsc --showConfig            # Show resolved config
npx tsx src/script.ts            # Run TS directly
```

## Debugging

```bash
node --inspect-brk dist/index.js   # Debug with breakpoint
node --enable-source-maps dist/index.js  # Enable source maps
```

## Dependencies

```bash
npm outdated                    # Check for updates
npm audit                       # Security audit
npm ls --depth=0                # List top-level deps
npx depcheck                    # Find unused deps
```

## Monorepo (Turborepo / Nx)

```bash
npx turbo run build
npx turbo run test --filter=my-package
npx nx run my-app:build
```

## Notes

- Check `package.json` scripts section for project-specific commands.
- Use `npx` to run locally-installed binaries without global install.
- Prefer `npm ci` over `npm install` in CI environments.
