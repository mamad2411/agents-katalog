---
name: github-codeowners-enforcement
description: >
  CODEOWNERS design and enforcement on GitHub: syntax, ownership coverage,
  required reviews via branch protection/rulesets, owners-file validity checks,
  and bypass governance. Use on owned repositories to ensure path-based review.
---

# GitHub CODEOWNERS Enforcement

## Scope And Authorization

- **In scope:** Repos you administer; configuring review requirements.
- **Out of scope:** Removing others’ ownership protections without authority; social-engineering
  review bypasses.
- CODEOWNERS without branch protection is advisory only — **enforce** with rules.
- Keep owners teams current with HR offboarding.
- Pair with `git-workflow-conventions` and `code-review-comments-style`.

## When To Use

- Introducing path-based required reviewers (app vs infra vs `.github`).
- Fixing invalid CODEOWNERS entries that silently fail.
- Migrating from ad-hoc reviewer pings to teams.
- Auditing who can approve production-critical paths.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Branching/PR process | `git-workflow-conventions` |
| CI gates | GitHub Actions skills |
| Deploy approvals | `github-actions-environment-gates` |
| Review comment tone | `code-review-comments-style` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| `CODEOWNERS` file | Path → owner users/teams |
| Locations | `.github/CODEOWNERS`, root, or `docs/` |
| Last match wins | Order matters |
| Team availability | Teams must be visible; members with repo access |
| Rulesets / branch protection | “Require review from Code Owners” |
| Bypass actors | Admins/roles that can skip — minimize |

## Workflow

### 1. Map ownership domains

| Path | Owner team |
| --- | --- |
| `/` default | `@org/platform` |
| `/apps/web` | `@org/web` |
| `/apps/api` | `@org/api` |
| `/infra` `/terraform` | `@org/sre` |
| `/.github` | `@org/security` + platform |
| `/docs` | `@org/tech-writers` optional |

### 2. Write CODEOWNERS

```text
# .github/CODEOWNERS
# Default
*       @org/platform

# Apps
/apps/web/   @org/web
/apps/api/   @org/api

# Infra highly sensitive
/infra/      @org/sre @org/security
/.github/    @org/platform @org/security

# Personal user example (prefer teams)
# /legacy/   @alice
```

Syntax tips:

- Patterns similar to gitignore; trailing slash for dirs.
- Teams need write access or explicit permission to be review-requestable.
- Use `@org/team` not display names.

### 3. Validate file

```bash
# On PR, GitHub shows errors; also use tools:
# - GitHub UI "Code owners" errors on the file
# - npx codeowners-validator / third-party validators in CI
```

Common failures: unknown team, team not synced, typos, unreachable users.

### 4. Enforce with ruleset

Repository Settings → Rules → Rulesets (or classic branch protection):

1. Target `main` (and release branches).
2. Require pull request before merging.
3. Require review from Code Owners.
4. Require status checks.
5. Restrict who can dismiss reviews / force push.
6. Limit bypass list to break-glass role with audit.

### 5. CI optional check

```yaml
# Fail if CODEOWNERS invalid (tool-dependent)
jobs:
  codeowners:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate CODEOWNERS
        run: |
          # install validator of choice; exit non-zero on error
          echo "run validator"
```

### 6. Verify end-to-end

| Change path | Expect |
| --- | --- |
| `/apps/web/...` | Web team required |
| `/.github/workflows/...` | Platform+security required |
| Admin bypass | Audited only |

Open test PR and confirm review requests.

### 7. Operate

- Quarterly: remove former employees; sync IdP groups → GitHub teams.
- Avoid single-human owners for critical paths.
- Document how to request ownership changes.
- Do not use CODEOWNERS as only access control — IAM separate.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Owners | Teams | Only one person for whole monorepo |
| Enforcement | Ruleset requires code owners | File present, protection off |
| Sensitive paths | Dual team for `.github`/infra | Anyone merges workflow changes |
| Order | Specific paths after default `*` | Unreachable rules shadowed wrong |
| Bypass | Rare break-glass | All admins always bypass quietly |

## Output Checklist

- [ ] Ownership map agreed
- [ ] CODEOWNERS committed validly
- [ ] Teams exist with repo access
- [ ] Branch ruleset requires code owners
- [ ] Test PR demonstrates requests
- [ ] Bypass process documented
- [ ] CI validation optional but preferred
- [ ] Offboarding updates owners

## Rules

- Enforcement requires branch rules, not just a file.
- Prefer teams; keep membership automated.
- Dual-control sensitive automation paths.
- Minimize permanent bypass actors.
- Focus on CODEOWNERS; deploy environments are separate gates.
