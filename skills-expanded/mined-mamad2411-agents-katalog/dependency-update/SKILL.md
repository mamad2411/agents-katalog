---
name: dependency-update
description: Safely update project dependencies - assess risk, batch by risk level, verify with tests, and produce a clean changelog. Use when the user asks to update dependencies, bump packages, audit outdated deps, or handle a security advisory.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, edit, grep
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [dependencies, maintenance, security]
---

# Dependency Update

Updating dependencies is mostly safe — until it isn't. The discipline: **know what you're changing, change it in reviewable chunks, verify each chunk.**

## When to use

- "Update dependencies"
- "What's outdated?"
- "Bump <package>"
- "Address this security advisory"
- "Renovate / Dependabot PR needs review"

## Procedure

### 1. Detect the ecosystem

```bash
ls package.json composer.json pyproject.toml Cargo.toml go.mod Gemfile 2>/dev/null
```

| Ecosystem | List outdated | Audit | Lockfile |
|---|---|---|---|
| npm | `npm outdated` | `npm audit` | `package-lock.json` |
| pnpm | `pnpm outdated` | `pnpm audit` | `pnpm-lock.yaml` |
| yarn | `yarn outdated` | `yarn audit` | `yarn.lock` |
| composer | `composer outdated` | `composer audit` | `composer.lock` |
| pip | `pip list --outdated` | `pip-audit` | `requirements.txt` / `poetry.lock` |
| cargo | `cargo outdated` (plugin) | `cargo audit` | `Cargo.lock` |
| go | `go list -u -m all` | `govulncheck ./...` | `go.sum` |
| bundler | `bundle outdated` | `bundle audit` | `Gemfile.lock` |

Lockfile must be committed. If it isn't, fix that first.

### 2. Classify each update by risk

| Risk | Includes | Strategy |
|---|---|---|
| 🟢 **Low** | Patch bumps (`1.2.3 → 1.2.4`), dev-only deps, well-maintained libs | Batch many in one PR |
| 🟡 **Medium** | Minor bumps (`1.2.x → 1.3.0`), runtime deps | Small batches, one ecosystem area at a time |
| 🔴 **High** | Major bumps (`1.x → 2.0`), core framework, deps with sprawling APIs | One per PR, read the changelog first |
| 🚨 **Security** | CVE / advisory | Prioritize, but still verify — don't break prod to fix theoretical risk |

**Always read the changelog/release notes** for medium and high risk. "Just bump it" is how prod goes down on a Friday.

### 3. Choose a batching strategy

| Strategy | When |
|---|---|
| **Patch sweep** | All patches at once. Quick PR, full test run. |
| **Minor by area** | Group related minors (all React-ecosystem packages together, all build tools together). |
| **One major per PR** | Always. Even when "small". |
| **Security first** | Address advisories before voluntary updates. |

### 4. Apply

```bash
# npm — interactive
npx npm-check-updates -i

# pnpm — interactive
pnpm update -i

# Targeted bump
npm install lodash@^4.17.21
composer require vendor/pkg:^2.0
pip install --upgrade somepkg
cargo update -p somecrate
```

### 5. Verify

For each batch:

1. **Install** clean: delete `node_modules`/etc, reinstall from lockfile
2. **Build** passes
3. **Type-check** / lint passes
4. **Test suite** passes (full, not just affected)
5. **Manually smoke-test** the affected areas (especially for medium+ risk)
6. **Run the audit** again to confirm advisories are resolved

```bash
# npm example
rm -rf node_modules
npm ci
npm run build
npm run test
npm audit
```

### 6. Commit & PR

One commit per logical batch:

```text
chore(deps): patch sweep — 12 packages

Patches only, no API changes. Full test suite passes.

- lodash 4.17.20 → 4.17.21
- @types/node 20.10.0 → 20.10.5
- … (see lockfile diff)
```

For majors, link the relevant changelog:

```text
chore(deps): upgrade react-router 6.x → 7.0 (BREAKING)

Migration notes: https://reactrouter.com/upgrading/v7

Changes required:
- `<Routes>` API split — see commit 1
- Loader signature change — see commit 2
```

## Handling a security advisory

1. **Read the advisory** — what's the actual vulnerable code path?
2. **Check reachability** — is the vulnerable code actually called from your app? `npm audit` often flags transitive deps in build tools that never run in prod
3. **Prefer the minimal fix** — patch bump > minor > major
4. **If no fix is published**:
   - Override the transitive dep (`overrides`/`resolutions` in package.json, `replace` in go.mod, etc.)
   - Pin to a known-safe version
   - Mitigate at the app level (input validation, disabling the affected feature)
5. **Document what you decided and why** — silence on a known CVE looks bad in a future audit

```bash
# npm — force a resolution
# package.json
{
  "overrides": {
    "vulnerable-pkg": "1.2.3-patched"
  }
}

# pnpm
# package.json
{
  "pnpm": {
    "overrides": {
      "vulnerable-pkg": "1.2.3-patched"
    }
  }
}
```

## Reading a changelog/diff before bumping

For medium/high-risk updates, skim:

- **Breaking changes** section — non-negotiable
- **Migration guide** if one exists
- **Default behavior changes** — these are the silent killers
- **Dropped support** (Node version, browser, runtime)
- **Removed/renamed APIs** — `grep` your codebase for them

```bash
# Quick: what changed since current version?
# (npm)
npm view <pkg> versions --json
# Browse changelog:
npm view <pkg> repository.url
```

## When NOT to update

- **Right before a release** — wait until after
- **On Friday afternoon** — wait until Monday
- **Without a working test suite** — the suite is the safety net; fix that first
- **If you don't have time to read the changelog** for a major
- **For a "newer is better" reason** with no actual benefit

## Output format

```markdown
## Dependency update report

**Ecosystem:** <npm / pnpm / composer / …>
**Lockfile diff:** +<n> -<m> entries
**Audit status:** <n> advisories before → <m> after

### Updated (batched by risk)
- 🟢 Patches (n packages): lodash, @types/node, …
- 🟡 Minors (n packages): vite 5.0 → 5.4, …
- 🔴 Majors: react-router 6 → 7 (separate PR)

### Skipped (with reason)
- pkg-x — major bump deferred: depends on N codepaths, needs migration plan
- pkg-y — advisory not reachable in our usage (build-time only)

### Verification
- ✅ Clean install
- ✅ Build
- ✅ Type-check
- ✅ Test suite (n passed, 0 failed)
- ✅ Smoke-tested: <areas>
- ✅ Audit: <result>

### Follow-ups
- …
```

## Anti-patterns

- ❌ `npm audit fix --force` without understanding what it changes
- ❌ Bumping a major across the codebase in one commit
- ❌ "Updated deps" PR with 50 packages and no notes
- ❌ Ignoring lockfile changes ("they're auto-generated") — they're the contract
- ❌ Updating during a release freeze
- ❌ Adding `overrides`/`resolutions` without a comment explaining why
- ❌ Bumping a dep purely because it's red on `npm outdated`

## Tips

- Set up **Renovate** or **Dependabot** to surface updates as PRs continuously — much easier than batched manual audits
- Configure auto-merge for patches with passing CI, manual review for minor/major
- Track **license changes** when bumping majors (`license-checker --summary`)
- Keep a `dependency-policy.md` if your team has rules (no GPL, no abandoned, etc.)
