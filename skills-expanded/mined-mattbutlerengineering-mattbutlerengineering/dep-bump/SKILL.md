---
name: dep-bump
description: Batch-apply pnpm.overrides for CVE fixes in a single PR. Use when multiple Dependabot/security alerts need dependency overrides — collapses N identical workflows into one operation.
---

# Dependency Bump (CVE Override Batch)

Apply one or more pnpm.overrides entries to fix CVEs in transitive dependencies, verify the audit passes, and open a single PR.

## When to use

- Multiple Dependabot alerts for transitive dependency CVEs
- `pnpm audit --audit-level=high` failing in CI Build job
- Security issues labeled `ready` with `fix(deps): bump` titles

## Input

Either:

- A list of overrides to apply (e.g., from issue bodies)
- Or no args — the skill scans `pnpm audit --audit-level=high` and proposes overrides automatically

## Workflow

### 1. Scan for vulnerabilities

```bash
pnpm audit --audit-level=high 2>&1
```

If no high-severity vulnerabilities, report clean and stop.

### 2. Build override entries

For each vulnerability, construct the scoped override per gotchas:

```
"pkg@<patched": "^patched"
```

**NOT** the open-range form `"pkg": ">=patched"` — that can pull major bumps.

### 3. Apply overrides

Edit the `pnpm.overrides` block in the root `package.json`. Add new entries; update existing entries if the patched version is higher.

### 4. Install and verify

```bash
pnpm install --lockfile-only
pnpm audit --audit-level=high
```

If high-severity vulnerabilities remain, iterate — some CVEs chain (e.g., `form-data` fixed but `tmp` still vulnerable).

### 5. Update antipattern baseline

```bash
node scripts/check-ai-antipatterns.mjs
```

If the ratchet shows pre-existing regressions (not from your changes), update the baseline:

```bash
node scripts/check-ai-antipatterns.mjs --update
```

### 6. Regenerate artifacts

```bash
pnpm regen
```

### 7. Commit and PR

Stage `package.json`, `pnpm-lock.yaml`, any updated baselines, and regenerated artifacts. Commit with:

```
fix(deps): patch <list of CVEs>

Override <pkg1>@<range> → ^<patched>, <pkg2>@<range> → ^<patched>.
All transitive — no code changes.
```

Push and open a PR with `Closes #<issue1>, Closes #<issue2>, ...` for all addressed issues.

## Gotchas

- Use scoped pattern `"pkg@<patched": "^patched"` — open ranges pull major bumps
- Run `pnpm audit --audit-level=high` (not `--audit-level=moderate`) — Build job gates on high only
- Regenerate artifacts after lockfile changes — CI "Verify generated artifacts" step will fail otherwise
- Check antipattern baseline — lockfile changes can shift counts
