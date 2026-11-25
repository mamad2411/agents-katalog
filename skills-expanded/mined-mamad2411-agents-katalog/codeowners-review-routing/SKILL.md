---
name: codeowners-review-routing
description: >
  Design and maintain CODEOWNERS path ownership, required review rules, and monorepo
  routing that avoids single-owner bottlenecks. Use when CODEOWNERS syntax, path owners,
  required reviewers, branch protection review counts, monorepo package ownership, or
  fixing slow PR queues caused by overly broad owner teams.
---

# CODEOWNERS Review Routing

## Scope And Authorization

- **In scope:** git hosting configs (GitHub/GitLab/Bitbucket) for repos you administer.
- **Out of scope:** forcing ownership of third-party projects; using CODEOWNERS to block competitors.
- Changes to required reviewers can freeze delivery — stage carefully.
- Pair with `code-review-comments-style` for human review quality and `code-quality-standards` for code bars.

## When To Use

- Introducing or refactoring `CODEOWNERS` / `CODEOWNERS` equivalents.
- Monorepo package ownership and path-based routing.
- PR latency caused by `@whole-company` as owner.
- Tokens: CODEOWNERS, required review, branch protection, monorepo owners, review routing.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Comment tone/severity | `code-review-comments-style` |
| Implementation quality | `code-quality-standards` |
| Security scan automation | CodeQL / SAST skills |
| Git commit messages | `commit-message-conventions` |

## Syntax Essentials (GitHub-style)

```text
# .github/CODEOWNERS (order: last match wins)
*                           @org/default-reviewers
/docs/                      @org/tech-writers
/services/payments/         @org/payments-team
/services/payments/infra/   @org/payments-team @org/sre
*.tf                        @org/sre
/CODEOWNERS                 @org/platform
```

| Rule | Detail |
| --- | --- |
| Last match wins | Put specific paths below broad ones |
| Teams vs users | Prefer teams for bus-factor |
| Optional owners | GitHub: rulesets can require code owner review |
| Escape paths | Spaces and special chars need care |

## Workflow

### 1. Confirm goals

1. Protect critical paths without serializing all PRs through one person.
2. Success: correct teams auto-requested; median time-to-first-review improves; critical dirs still gated.
3. Map org teams to systems (payments, iam, platform).

### 2. Inventory

```bash
# Find current owners file
ls -a CODEOWNERS .github/CODEOWNERS docs/CODEOWNERS 2>/dev/null
# Branch protection / rulesets in hosting UI or API
# PR metrics: time to approve, re-request rate
```

1. List top directories by change frequency and risk.
2. Identify single-human owners (risk).

### 3. Design ownership model

| Path class | Owner pattern |
| --- | --- |
| Product service | Team that on-calls it |
| Shared lib | Platform + 1 consumer rep |
| Infra/TF | SRE + service team |
| Security-sensitive | Seceng **and** service team |
| Docs | Writers optional; not blocking unless policy |

1. Keep default `*` team small and generalist, not “everyone”.
2. Avoid requiring 5 teams on leaf packages.
3. Use hierarchical paths; don’t list every file.

### 4. Wire enforcement

1. Enable “require review from Code Owners” on protected branches (or rulesets).
2. Align required **count** (e.g. 1) with owner team size.
3. CODEOWNERS changes themselves owned by platform + security.
4. Document emergency bypass (admin) with audit.

### 5. Monorepo tactics

| Problem | Tactic |
| --- | --- |
| Huge CODEOWNERS | Generate from package metadata (owners.yaml per package) |
| Cross-cutting PR | Multiple teams OK; keep PR small |
| Hot folder | Split packages; ownership follows code |
| Vacation coverage | Team membership not individuals |

### 6. Verify

1. Open test PR touching only `/docs` → only docs owners.
2. Touch payments + TF → both teams, not entire monorepo.
3. Invalid user/team in CODEOWNERS → fix CI check if available.
4. Measure: % PRs with correct auto-request; median wait.

### 7. Maintain

1. Quarterly prune dead teams/users.
2. When team renames, update CODEOWNERS in same PR as team migration.
3. Alert on CODEOWNERS PRs that broaden `*` to huge teams.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default owner | Small platform/triage team | `@org/all-engineers` |
| Specificity | Service directory teams | One person owns `/` |
| Enforcement | Ruleset + owners | Owners file ignored |
| Changes | Reviewed by platform | Anyone silent edit owners |
| Metrics | TTFR by path | No measurement |

## Output Checklist

- [ ] Teams mapped to systems
- [ ] CODEOWNERS paths ordered correctly (last match)
- [ ] No single-human critical bottlenecks (or accepted risk)
- [ ] Branch protection requires owner review where intended
- [ ] Test PRs prove routing
- [ ] Bypass process documented
- [ ] Maintenance cadence set
- [ ] Residual broad paths listed

## Rules

- Prefer teams over individuals for resilience.
- Optimize for safe velocity, not maximum friction.
- Focus on **ownership routing**; review tone and code quality are sibling skills.
- Keep secrets out of owners files (they are only paths and teams).
