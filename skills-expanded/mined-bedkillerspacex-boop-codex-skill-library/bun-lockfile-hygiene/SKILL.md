---
name: bun-lockfile-hygiene
description: >
  Bun lockfile hygiene for owned JS/TS projects: commit bun.lock, reproducible installs
  (bun install --frozen-lockfile), trust/lifecycle script policy, registry config, and
  CI verification. Use when bun.lock drift, bunfig.toml, private registries with Bun,
  or supply-chain hygiene for Bun-based apps — not for tampering with others' packages.
---

# Bun Lockfile Hygiene

## Scope And Authorization

- **In scope:** Repositories and registries you control using the Bun toolkit.
- **Out of scope:** Publishing malware packages; violating registry terms.
- Prefer CI frozen installs for releases.
- Redact registry tokens in `bunfig` and logs.
- Pair with `code-quality-standards` and broader npm supply-chain practices.

## When To Use

- Adopting Bun for installs/runtime and need deterministic dependencies.
- Fixing “works on my machine” due to missing or uncommitted lockfiles.
- Hardening CI: fail on lockfile drift; control `postinstall` scripts.
- Migrating from npm/pnpm/yarn lockfiles to Bun carefully.
- Private registry / workspace monorepo installs with Bun.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| npm/pnpm lockfile only | npm/pnpm hygiene skills |
| Runtime security of Node APIs | Node/TS security skills |
| General secrets in env | `secrets-management-hygiene` |
| Biome/format pipeline | `biome-lint-format` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Artifact | Role |
| --- | --- |
| `bun.lock` | Binary/text lock (version-dependent format) — **commit it** |
| `package.json` | Declared ranges |
| `bunfig.toml` | Registry, install behavior, trust |
| `node_modules` | Install output — usually gitignored |
| Workspaces | Monorepo package graph |

## Workflow

### 1. Confirm scope and success criteria

1. Bun version policy (pin in CI and engines field if used).
2. Success: clean CI install with frozen lockfile; no uncommitted lock drift; scripts policy documented.
3. Note dual package managers — avoid mixing npm/bun installs ad hoc.

### 2. Inventory

```bash
bun --version
ls package.json bun.lock bun.lockb yarn.lock package-lock.json pnpm-lock.yaml bunfig.toml 2>/dev/null
# Show outdated / why (commands evolve — check bun --help)
bun pm ls 2>/dev/null || true
```

1. If multiple lockfiles exist, pick **one** package manager as source of truth.
2. Check `.gitignore` does not ignore `bun.lock` / `bun.lockb`.
3. List private scopes needing registry auth.

### 3. Baseline install

```bash
rm -rf node_modules
bun install
git status  # lockfile should not thrash randomly after second install
```

1. Re-run install twice; lockfile should be stable.
2. Record package count and any `postinstall` executions.

### 4. Commit and freeze

```bash
git add bun.lock package.json bunfig.toml
# CI
bun install --frozen-lockfile
# or: bun install --lockfile-only  (when updating intentionally)
```

**CI sketch:**

```yaml
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: "1.1.34"  # pin
- run: bun install --frozen-lockfile
- run: bun test
```

1. Dependabot/Renovate: configure for Bun lockfile support if used.
2. PR rule: changes to lockfile require review for unexpected packages.

### 5. bunfig and script trust

**Example `bunfig.toml` ideas:**

```toml
[install]
# exact version policy preferences per team
peer = true

[install.scopes]
"@myorg" = { url = "https://npm.pkg.github.com/", token = "$BUN_AUTH_TOKEN" }
```

1. Pass tokens via env — never commit tokens.
2. Review lifecycle scripts: prefer `bun install --ignore-scripts` in untrusted contexts, then enable intentionally.
3. For production image builds, install with frozen lockfile and disable unnecessary scripts.

### 6. Verify supply-chain basics

```bash
bun install --frozen-lockfile
# Audit: use available Bun/npm audit path for your version
bun pm untrusted 2>/dev/null || true
# Compare unexpected new deps in PR diff of bun.lock
git diff main -- bun.lock | head
```

1. Flag new deps with `postinstall`, native bindings, or unexpected maintainers.
2. Ensure `NODE_ENV=production` installs omit devDeps when intended for runtime images.
3. Pin Bun version — lockfile interpretation can differ across majors.

### 7. Hand off

1. README: “use Bun X; never commit `node_modules`; always commit lockfile”.
2. Remove stale npm/yarn lockfiles if fully migrated.
3. Apply `code-quality-standards` for app code; keep package PRs small.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Lockfile | Committed + frozen CI | gitignored lockfile |
| Version | Bun pinned in CI | Latest Bun every build |
| Tokens | Env in bunfig | Token in committed bunfig |
| Managers | One tool per repo | bun + npm install mixed weekly |
| Scripts | Policy for lifecycle | Blind scripts on untrusted PR forks |
| Reviews | Lockfile diff reviewed | “lockfile noise” auto-merge |

## Output Checklist

- [ ] Bun version policy set
- [ ] Single package manager decided
- [ ] `bun.lock` committed and stable
- [ ] CI `bun install --frozen-lockfile` green
- [ ] Registry auth via env secrets
- [ ] Lifecycle script policy documented
- [ ] Lockfile review expectations in CONTRIBUTING
- [ ] Migration leftover lockfiles removed if applicable
- [ ] `code-quality-standards` noted for code changes

## Rules

- Deterministic installs require a committed lockfile and frozen CI installs.
- Treat lockfile diffs as security-sensitive.
- Never commit registry tokens.
- Prefer one package manager per repository.
- Authorized packages only; do not sabotage public registries.
