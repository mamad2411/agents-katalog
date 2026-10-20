---
name: dependabot-config-hardening
description: >
  Harden GitHub Dependabot: complete .github/dependabot.yml coverage, safe schedules and
  groups, open-pull-requests-limit, private registries, ignore rules with expiry, monorepo
  directories, github-actions and docker ecosystems, versioning-strategy, vendor allow,
  and review/CI gates without blind auto-merge. Use when dependabot.yml, Dependabot security
  updates, package-ecosystem entries, or hardening dependency bots on GitHub — hand pin/lock
  strategy to dependency-pinning-strategies and pure grouping noise control to
  dependabot-group-updates.
---

# Dependabot Config Hardening

## Scope And Authorization

- **In scope:** GitHub orgs/repos you own or administer; Dependabot config and related branch protection.
- **Out of scope:** Enabling bots on third-party repos without permission; storing registry tokens in plaintext in git.
- Prefer staging branch or canary repo before org-wide policy rollouts.
- Redact private registry credentials, PATs, and org secrets from tickets and screenshots.
- Pair with `code-quality-standards` for any workflow code; use `secrets-management-hygiene` for token lifecycle.

## When To Use

- Creating or reviewing `.github/dependabot.yml` for complete ecosystem coverage.
- Reducing risk from noisy, unreviewed, or over-privileged dependency PRs.
- Configuring private registries, monorepo directory entries, and Actions/Docker updates.
- Enforcing PR limits, cooldown, and ignore hygiene without silent permanent ignores.
- Blocking blind auto-merge of dependency PRs without CI and review.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Grouping patterns / fewer noisy PRs detail | `dependabot-group-updates` |
| Version pin vs range strategy | `dependency-pinning-strategies` |
| Dependency confusion / private vs public | `dependency-confusion` |
| Renovate-only presets | Renovate docs / dedicated Renovate skill if present |
| SBOM generation | SBOM skill in catalog |
| Org SSDLC process | `secure-sdlc-checklist` |
| Implementation baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Config file | `.github/dependabot.yml` (`version: 2`) |
| Ecosystems | npm, pip, bundler, maven, gradle, nuget, go_modules, cargo, composer, docker, github-actions, terraform, etc. |
| Security updates | GitHub Security advisory PRs — keep enabled; do not rely only on version updates |
| Controls | schedule, groups, limit, allow/ignore, registries, directories, labels, assignees, reviewers |
| Pitfalls | Missing directories; permanent ignores; registry secrets in YAML; auto-merge without checks |

## Workflow

### 1. Confirm scope and success criteria

1. List target repos (or org template), package managers, and monorepo paths.
2. Success: every package manifest path covered; Actions + Docker included if used; open PR count under control; no plaintext registry passwords; required checks on Dependabot PRs.
3. Note who reviews dependency PRs and whether security updates have a faster path.

### 2. Inventory current Dependabot state

1. Read `.github/dependabot.yml` if present; check repo Settings → Code security for Dependabot alerts/security updates.
2. List manifests: `package.json`, `requirements*.txt`/`pyproject.toml`, `go.mod`, `Dockerfile*`, `.github/workflows/*.yml`, etc.
3. Capture pain: ignored CVEs, 50 open Dependabot PRs, missing private module installs, Actions never updated.

### 3. Author hardened `dependabot.yml` skeleton

```yaml
# .github/dependabot.yml
version: 2
registries:
  npm-private:
    type: npm-registry
    url: https://npm.pkg.example.com
    token: ${{secrets.NPM_PRIVATE_TOKEN}}
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
      day: monday
      time: "09:00"
      timezone: UTC
    open-pull-requests-limit: 10
    versioning-strategy: increase-if-necessary
    labels: ["dependencies", "npm"]
    reviewers:
      - "my-org/security-deps"
    registries:
      - npm-private
    groups:
      production-patches:
        dependency-type: production
        update-types: ["patch"]
  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
  - package-ecosystem: docker
    directory: "/deploy"
    schedule:
      interval: weekly
```

1. One `updates` entry per ecosystem + directory pair in monorepos (`/`, `/frontend`, `/services/api`).
2. Always add `github-actions` when workflows exist; pin Actions SHAs in workflows separately as policy allows.
3. Use `open-pull-requests-limit` to avoid drowning CI (typical 5–15).

### 4. Private registries and allow rules

1. Define `registries:` with secret references only—never commit tokens.
2. Grant Dependabot access to secrets via repo/org Dependabot secrets (not only Actions secrets).
3. Use `allow` / `vendor` patterns carefully; document why public transitive deps are restricted.
4. For private modules (Go, npm scopes), confirm CI and Dependabot resolve the same registry order (see `dependency-confusion`).

### 5. Ignores, schedules, and grouping

1. Prefer temporary `ignore` with `versions` or linked issue; review quarterly—no eternal ignores for critical CVEs without compensating control.
2. Weekly schedule for most apps; daily only if you have review capacity.
3. Use groups for low-risk patch batches; keep major updates ungrouped or separately grouped for review (detail: `dependabot-group-updates`).
4. Labels + CODEOWNERS/reviewers so dependency PRs never sit unowned.

### 6. Branch protection and CI gates (no blind merge)

1. Require status checks (build, test, SCA) on default branch for Dependabot PRs.
2. Avoid org-wide auto-merge for majors; if auto-merge is used, limit to patch groups + green checks + short cooldown.
3. Enable Dependabot security updates; treat security PRs with higher priority labels/SLA.
4. Optionally assign `commit-message` prefixes for changelog tooling.

### 7. Verify and hand off

```bash
# Repo checks (owned clone)
test -f .github/dependabot.yml && yamllint .github/dependabot.yml
# List manifests vs directories in yml (manual matrix or script)
rg -n "package-ecosystem|directory:" .github/dependabot.yml
# Confirm workflows and Dockerfiles covered
find . -name Dockerfile -o -name package.json -o -name go.mod | head
```

1. Open a trivial Dependabot config PR; confirm GitHub accepts config (Dependabot logs / UI).
2. Document ignore review cadence and secret rotation for registry tokens.
3. Apply `code-quality-standards` if custom automation scripts ship.

## Ecosystem coverage checklist

| Ecosystem | Typical directory | Notes |
| --- | --- | --- |
| npm / yarn / pnpm | `/` or app path | Lockfile must exist for reproducible PRs |
| pip | `/` | Prefer single source of truth (pyproject vs requirements) |
| go_modules | module root | Private GOPROXY config |
| docker | dir with Dockerfile | Base image CVEs |
| github-actions | `/` | Workflow third-party actions |
| terraform | stack dirs | Provider pins |
| nuget / maven / gradle | project roots | Multi-module monorepo entries |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Coverage | All manifests + Actions + Docker | Only root npm |
| Secrets | Dependabot secrets + `${{secrets.*}}` | Token pasted in yml |
| Ignores | Ticketed, version-scoped, expiry | Ignore all majors forever |
| Merge | Required CI + review/auto patch only | Auto-merge everything |
| Limits | `open-pull-requests-limit` set | Unlimited PR flood |
| Monorepo | Per-directory entries | Single `/` missing apps |

## Output Checklist

- [ ] Owner/repo scope and success criteria recorded
- [ ] Inventory of manifests vs `dependabot.yml` entries complete
- [ ] `version: 2` config with schedules and PR limits
- [ ] Private registries use secrets only; Dependabot can read them
- [ ] github-actions and docker covered when applicable
- [ ] Groups/ignores documented; ignores not permanent without review date
- [ ] Branch protection/CI required on dependency PRs
- [ ] Security updates enabled and triaged with SLA
- [ ] Config validated in GitHub UI / Dependabot logs
- [ ] Hand-off: reviewers, ignore cadence, residual risk

## Rules

- Authorized org/repos only; no credential leakage in config.
- Dependabot is not a substitute for lockfiles, SCA policy, or human review of majors.
- Do not disable security updates to reduce noise—fix grouping and limits instead.
- Keep this skill on config hardening; deep grouping and pin strategy are neighbor skills.
- Evidence: accepted config, covered paths, and green CI on sample PRs.
