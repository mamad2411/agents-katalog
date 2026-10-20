---
description: Run Dependency Management and Supply Chain Security Checks
globs: ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']
---

# Infrastructure: Dependency & Supply Chain Hygiene

<audit_rules>

- You MUST verify that a lockfile (`package-lock.json`, `yarn.lock`, etc.) is present and its integrity matches the package manager specified in the project.
- You MUST flag any unused dependencies or dependencies that are duplicated across sub-workspaces.
- You MUST ensure strict separation of `dependencies` (production) and `devDependencies` (build/test tools).
- You MUST flag any dependency that has known critical or high security vulnerabilities (e.g., requiring an `npm audit` check).
- You MUST be highly suspicious of packages with post-install scripts or unexpected version bumps to prevent supply chain attacks.
- You MUST recommend version pinning (removing `^` or `~`) for critical security or infrastructure packages.
  </audit_rules>

<example_good>

```json
{
  "dependencies": {
    "next": "15.0.0",
    "react": "19.0.0"
  },
  "devDependencies": {
    "typescript": "5.5.4",
    "vitest": "2.1.0"
  }
}
```

</example_good>

<example_bad>

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "vitest": "2.1.0" // BAD: Test framework in production dependencies
  }
}
```

</example_bad>
