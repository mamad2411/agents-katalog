---
name: dependabot-group-updates
description: >
  Configure Dependabot (and analogous Renovate) dependency grouping to cut noisy PRs,
  preserve security-first paths, and control CI cost: groups by dependency-type,
  update-types (patch/minor/major), patterns, exclude-patterns, and per-ecosystem strategy.
  Use when dependabot groups, grouped version updates, too many dependency PRs, batching
  npm/pip/Actions updates, or CI minutes burned by Dependabot — hand full yml hardening to
  dependabot-config-hardening and pin/range policy to dependency-pinning-strategies.
---

# Dependabot Group Updates

## Scope And Authorization

- **In scope:** Owned GitHub repos/orgs; Dependabot or Renovate grouping configuration.
- **Out of scope:** Forcing updates on third-party projects; hiding critical CVE fixes inside giant unreviewed groups.
- Prefer canary on one service repo before monorepo-wide groups.
- Redact registry tokens and internal package names that are sensitive in public forks.
- Pair with `dependabot-config-hardening` for base yml and `code-quality-standards` for scripts.

## When To Use

- Dozens of single-dep PRs overwhelm review and CI.
- You want patch production deps batched weekly but majors isolated.
- Monorepos need per-directory group strategies.
- Security updates should stay visible and not buried in a 40-package group.
- Migrating from ungrouped Dependabot to pattern-based groups.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full dependabot.yml hardening (registries, limits, Actions) | `dependabot-config-hardening` |
| Pin vs caret/range policy | `dependency-pinning-strategies` |
| Dependency confusion controls | `dependency-confusion` |
| SCA / advisory triage process | secure-sdlc / vuln management skills |
| Renovate-only advanced presets | Renovate documentation |
| Code quality baseline | `code-quality-standards` |

## Domain Concepts

| Concept | Meaning |
| --- | --- |
| Group | Single PR containing multiple dependency bumps matching rules |
| `dependency-type` | production vs development (ecosystem-dependent) |
| `update-types` | `patch`, `minor`, `major` version bumps |
| `patterns` / `exclude-patterns` | Name globs (e.g. `@types/*`, `eslint*`) |
| Security updates | Advisory-driven PRs; may ignore grouping depending on product behavior—verify |
| CI cost | One grouped PR ≈ one pipeline vs N pipelines |

## Workflow

### 1. Confirm scope and success criteria

1. Measure baseline: open Dependabot PRs/week, CI minutes/week, median time-to-merge, skipped security PRs.
2. Success examples: ≤ N open dep PRs; patch groups merge within 7 days; majors always solo; no critical CVE left ungrouped into noise.
3. Agree reviewer capacity and freeze windows (release week = pause groups).

### 2. Inventory dependency noise

1. Export recent Dependabot PRs by ecosystem and directory.
2. Cluster by: lint/tooling, types, AWS SDK family, Spring Boot BOM, Actions `actions/*`, etc.
3. Flag high-risk packages that must never batch (auth, crypto, ORMs, payment SDKs)—keep ungrouped or “majors only alone”.

### 3. Design group matrix

| Group name | Match | Rationale |
| --- | --- | --- |
| `prod-patches` | production + patch | Low risk, high volume |
| `dev-lint` | eslint*, prettier, @types/* | Dev-only noise |
| `aws-sdk` | `@aws-sdk/*` patterns | Coordinated minors |
| *(none)* | majors / security-critical names | Force human focus |

Rules of thumb:

1. Batch patches liberally; minors carefully; majors rarely (or never) in multi-package groups.
2. One failing member fails the group—keep groups cohesive (same test surface).
3. Separate ecosystems and directories (frontend npm ≠ backend npm).

### 4. Implement Dependabot groups

```yaml
# Excerpt — .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/web"
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
    groups:
      production-patches:
        dependency-type: "production"
        update-types:
          - "patch"
      development-non-major:
        dependency-type: "development"
        update-types:
          - "patch"
          - "minor"
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier*"
        exclude-patterns:
          - "typescript"   # majors/minors of tsc reviewed separately if desired
      aws-sdk-minor-patch:
        patterns:
          - "@aws-sdk/*"
        update-types:
          - "minor"
          - "patch"
    # majors intentionally ungrouped for individual PRs
```

1. Keep `open-pull-requests-limit` so groups cannot explode unbounded.
2. Labels: `dependencies`, `grouped`, ecosystem name for filtering.
3. Document that a broken group may need temporary ignore or split—do not force-merge red CI.

### 5. Security-first policy

1. Confirm how GitHub handles security updates vs groups for your ecosystem (behavior evolves—verify in docs/UI).
2. SLA: critical/high security PRs reviewed outside weekly batch cadence.
3. Never `ignore` a CVE solely because it “conflicts with a group.”
4. If a group PR mixes a security bump with unrelated minors, split before merge when review quality suffers.

### 6. Renovate parity (if dual-running)

```json5
// renovate.json excerpt — analogous packaging
{
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "matchDepTypes": ["dependencies"],
      "groupName": "production patches"
    },
    {
      "matchPackagePatterns": ["^eslint"],
      "groupName": "eslint"
    },
    {
      "matchUpdateTypes": ["major"],
      "groupName": null
    }
  ]
}
```

1. Do not run uncoordinated Dependabot + Renovate on the same manifests without partition rules.
2. Prefer one bot per ecosystem to avoid duplicate PRs.

### 7. Verify, measure, hand off

```bash
# After config merge (owned repo)
rg -n "groups:|patterns:|update-types:" .github/dependabot.yml
# Track outcomes over 2-4 weeks
# - count of dep PRs opened
# - CI minutes for dependency branch prefix
# - security PR age
```

1. First grouped PR: ensure CI runs once, tests cover all bumped packages, rollback is revert PR.
2. Tune: if groups always fail, split by package family; if still too many PRs, widen patch groups only.
3. Write team norm: “grouped patch OK to auto-merge with green CI; majors need owner.”

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Patches | Grouped prod patches weekly | 30 single patch PRs/day |
| Majors | Solo PR + changelog read | 12 majors in one PR |
| Security | Fast path, visible SLA | Buried in lint group |
| Cohesion | `@aws-sdk/*` together | random unrelated packages |
| Failure | Split group / fix tests | `--force` green ignore |
| Bots | One bot per manifest set | Dependabot + Renovate fight |

## Output Checklist

- [ ] Baseline PR/CI metrics captured
- [ ] High-risk packages excluded from large groups
- [ ] Group matrix documented (name, match, update-types)
- [ ] `dependabot.yml` groups implemented per directory/ecosystem
- [ ] Security update handling verified and SLA set
- [ ] PR limits and labels applied
- [ ] No dual-bot conflict
- [ ] First grouped PRs validated in CI
- [ ] Review/auto-merge norms written
- [ ] Follow-up tune date scheduled

## Rules

- Authorized repos only; grouping is for manageability, not to sneak majors past review.
- Prefer smaller cohesive groups over one mega-group.
- Do not permanently ignore failures inside groups—fix the package set.
- Hand full config hardening and pinning policy to neighbor skills.
- Measure after change; revert groups that increase mean time to merge security fixes.
