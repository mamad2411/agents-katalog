# Monorepo Setup with Turborepo

## Summary

**One-sentence:** Wires a pnpm + Turborepo monorepo: apps/ + packages/ workspaces, shared tsconfig + eslint, turbo.json task graph with remote cache, CI matrix per package.

**One-paragraph:** Wires a pnpm + Turborepo monorepo: apps/ + packages/ workspaces, shared tsconfig + eslint, turbo.json task graph with remote cache, CI matrix per package. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- ≥2 deployable surfaces (web + mobile, web + admin, app + marketing) sharing types or UI.
- Team needs incremental build + remote cache to keep CI under 10 minutes.
- Single language family (TypeScript) across packages.
- Output produces `config` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- ≥2 deployable surfaces (web + mobile, web + admin, app + marketing) sharing types or UI.
- Team needs incremental build + remote cache to keep CI under 10 minutes.
- Single language family (TypeScript) across packages.

## Skip If (ANY kills it)

- Single deployable surface — monorepo adds tooling cost with no payoff.
- Polyglot monorepo (TS + Python + Go) — use Nx or Bazel, not Turborepo.
- Team has zero ops bandwidth to operate remote cache + per-package CI.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| pnpm 9+ | package manager | team |
| TypeScript 5+ | shared baseline | team |
| Turborepo CLI | turbo binary or npx | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[best-practices-2026]] | ts-strict baseline applies inside every package |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-workspace` | sonnet | Create apps/ + packages/ + pnpm-workspace.yaml + turbo.json. |
| `shared-config` | sonnet | Extract tsconfig.base.json + eslint preset. |
| `ci-matrix` | haiku | Matrix generation per package. |

## Templates

| File | Purpose |
|------|---------|
| `templates/turbo.json` | Turborepo task graph: build / lint / test with cache |
| `templates/pnpm-workspace.yaml` | pnpm workspace declaration |
| `templates/tsconfig.base.json` | Shared TypeScript base config (strict) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monorepo-turborepo.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[best-practices-2026]]
- [[practices-js-ts-stack]]
- [[practices-frontend-components]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are there ≥2 deployable surfaces AND is the stack TypeScript-only AND has ops bandwidth?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/turbo.json`

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [
    "**/.env.*local"
  ],
  "tasks": {
    "build": {
      "dependsOn": [
        "^build"
      ],
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**"
      ],
      "inputs": [
        "src/**",
        "tsconfig.json",
        "package.json"
      ]
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "dependsOn": [
        "^build"
      ],
      "outputs": [
        "coverage/**"
      ]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### `templates/pnpm-workspace.yaml`

```yaml
# faion_header_json: {"__faion_header__":{"purpose":"pnpm workspace declaration","consumes":"see content/02-output-contract.xml","produces":"config","depends_on":"content/01-core-rules.xml#two-tier-workspaces","token_budget_impact":"~150 tokens when loaded"}}
packages:
  - apps/*
  - packages/*
```

### `templates/tsconfig.base.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```
