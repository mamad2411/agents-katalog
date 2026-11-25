---
name: biome-lint-format
description: >
  Biome unified lint and format pipeline for owned JS/TS repos: install/pin, biome.json
  rules, organizeImports, CI check vs write, ignore files, migrate from ESLint/Prettier,
  and enforce format-on-save without dual formatters fighting. Use when biome check,
  biome format, biome ci, lint-staged Biome, or replacing ESLint+Prettier with Biome.
---

# Biome Lint Format

## Scope And Authorization

- **In scope:** Repositories and CI you own or are authorized to change.
- **Out of scope:** Force-pushing format-only mass rewrites onto protected branches without review; scanning third-party codebases without permission.
- Prefer a dedicated PR for pure format adoption so functional diffs stay reviewable.
- Redact tokens in CI logs; do not commit machine-local Biome paths or secrets.
- Pair code fixes with `code-quality-standards` and language packs (`typescript-style-and-eslint` when residual ESLint remains).

## When To Use

- Adopting Biome as the sole formatter + linter for JS/TS (and supported JSON/CSS).
- CI must fail on lint errors and unformatted files (`biome ci` / `biome check --error-on-warnings`).
- Migrating away from Prettier + ESLint dual config drift.
- Tuning rule severity, ignore globs, VCS integration, or monorepo root configs.
- Editor format-on-save alignment with CI so “works on my machine” format fails stop.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ESLint-only / Prettier dual pipeline keep | `prettier-eslint-editorconfig` or `typescript-style-and-eslint` |
| General TypeScript typing / architecture | `typescript-style-and-eslint`, `code-quality-standards` |
| Dependency / supply-chain audit | `npm-supply-chain-hygiene` or lockfile skills |
| Security SAST beyond style rules | language SAST / `secure-sdlc-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Binary | `@biomejs/biome` CLI; pin exact version in package.json + lockfile |
| Config | `biome.json` / `biome.jsonc` at repo or package roots; `extends` for monorepos |
| Modes | `check` (lint+format diagnose), `format`, `lint`, `ci` (no writes, CI-friendly) |
| Writes | `biome check --write` or `--fix` for safe autofix; avoid silent mass rewrite on main |
| Ignore | `files.ignore`, `files.include`; respect `.gitignore` via VCS settings when enabled |
| Conflict | Disable Prettier + eslint-plugin-prettier once Biome owns format; one formatter only |

## Workflow

### 1. Confirm scope and success criteria

1. Record package manager (npm/pnpm/yarn/bun), monorepo layout, current ESLint/Prettier usage, CI provider.
2. Success: `biome ci .` green in CI; editors use Biome; no Prettier/ESLint format overlap; rule baseline documented.
3. Decide: big-bang format PR vs gradual package rollout.

### 2. Inventory current tooling

```bash
# Detect existing format/lint
ls package.json biome.json biome.jsonc .eslintrc* eslint.config.* .prettierrc* 2>/dev/null
jq '.devDependencies, .dependencies, .scripts' package.json
# If Biome already present:
npx @biomejs/biome --version
npx @biomejs/biome rage 2>/dev/null || true
```

1. List paths that must stay Prettier-owned (e.g. Markdown-only pipelines) and exclude them explicitly.
2. Note generated dirs (`dist/`, `coverage/`, `.next/`) for ignore.
3. Capture current CI lint job names for replacement.

### 3. Baseline before change

1. On a clean branch, record `git status` and optionally snapshot a format report.
2. Run existing lint once and archive exit code/count for comparison.
3. Agree with the team: format-only commits allowed as single-purpose PRs.

### 4. Install, configure, and adopt

```bash
# Install (example npm)
npm install --save-dev --save-exact @biomejs/biome
npx @biomejs/biome init
```

**Minimal `biome.json` sketch:**

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "files": {
    "ignore": ["dist/**", "coverage/**", "**/*.min.js"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": { "noExplicitAny": "warn" },
      "correctness": { "noUnusedImports": "error" }
    }
  },
  "javascript": {
    "formatter": { "quoteStyle": "double", "semicolons": "always" }
  }
}
```

```bash
# Diagnose without write
npx @biomejs/biome check .
# Apply safe fixes + format
npx @biomejs/biome check --write .
# CI-oriented (no filesystem writes)
npx @biomejs/biome ci .
```

**package.json scripts (example):**

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "ci:biome": "biome ci ."
  }
}
```

1. Remove or narrow Prettier/ESLint format rules that duplicate Biome; keep ESLint only if you still need rules Biome lacks — document the split.
2. Editor: enable Biome LSP/extension; disable “Format with Prettier” as default for JS/TS.
3. Optional husky + lint-staged: run `biome check --write --files-ignore-unknown=true --no-errors-on-unmatched` on staged files only.
4. Monorepo: root config + per-package overrides via nested `biome.json` where needed.

### 5. Verify with evidence

```bash
npx @biomejs/biome ci .
npx @biomejs/biome check --error-on-warnings .   # if policy requires zero warnings
# Ensure generated paths are ignored (should not flood)
npx @biomejs/biome check dist 2>&1 | head
git diff --stat   # review format blast radius
```

1. CI job uses the **same** Biome version as lockfile (no floating `@latest` in CI only).
2. Confirm a deliberately bad file fails CI (unused import / format break).
3. Confirm intentional rule disables use `biome-ignore` with justification comments, not global off.

### 6. Observe and harden

1. Track CI duration; if slow, narrow `files.include` or split jobs by package.
2. Version-bump Biome deliberately; re-run full check after major upgrades (rule renames happen).
3. Forbid committing `biome-ignore` without owner + ticket for security-adjacent rules.

### 7. Hand off

1. Document “one formatter” policy in CONTRIBUTING / README.
2. Link PR of initial format adoption; freeze dual-formatter period with end date.
3. Apply `code-quality-standards` for any non-format logic changes bundled by mistake (split them out).

## CI Snippet (GitHub Actions)

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: npm
- run: npm ci
- run: npx @biomejs/biome ci .
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Version pin | Exact `@biomejs/biome` in lockfile | CI uses `npx @biomejs/biome@latest` only |
| Format ownership | Biome only for JS/TS | Prettier + Biome both format on save |
| Adoption | Dedicated format PR | Mix 5k format lines with feature logic |
| Ignores | Generated + vendor ignored | Linting `node_modules` or build output |
| Suppressions | Line-level `biome-ignore` + reason | `"recommended": false` forever |
| CI mode | `biome ci` / check without write | CI runs `--write` and commits back unchecked |

## Output Checklist

- [ ] Scope, package manager, monorepo layout recorded
- [ ] Baseline existing ESLint/Prettier inventory done
- [ ] Biome installed and version-pinned
- [ ] `biome.json` covers formatter, linter, ignore, VCS
- [ ] Scripts and CI use `check`/`ci` consistently
- [ ] Prettier/ESLint format conflict removed or documented
- [ ] Editor + optional pre-commit aligned
- [ ] Verification: failing case + green `biome ci` evidence
- [ ] `code-quality-standards` applied for non-format code changes

## Rules

- One primary formatter for a given file type; do not dual-run Prettier and Biome on the same paths.
- Prefer reversible adoption via branch/PR; never force-push format rewrites onto shared main without policy.
- Keep `biome-ignore` rare and justified.
- Do not weaken security-relevant lint rules to silence debt without a tracked exception.
- Focus this skill on Biome pipeline setup; route deep TS architecture and supply-chain work elsewhere.
