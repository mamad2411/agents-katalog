---
name: composer-security-audit
description: >
  Run and gate PHP Composer dependency vulnerability checks with composer audit
  locally and in CI: Packagist/GitHub advisories, composer.lock scans, JSON output,
  abandoned packages, ignore policy, and upgrade paths for owned PHP apps. Use when
  composer audit, Composer CVE scanning, PHP lockfile SCA gates, or wiring audit into
  GitHub Actions/GitLab CI.
---

# Composer Security Audit

## Scope And Authorization

- **In scope:** PHP projects and private packages you own or are allowed to scan.
- **Out of scope:** scraping others’ private composer repos without access; ignoring critical vulns in prod without risk acceptance.
- Commit `composer.lock` for applications; audit the lockfile that deploys.
- Pair upgrades with `code-quality-standards` and test suites.

## When To Use

- Adding SCA gate for PHP (`composer audit`).
- Responding to advisory on a locked package.
- Tokens: composer audit, composer.lock, Packagist advisories, abandoned packages.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| npm/pip/cargo audit | respective ecosystem skills |
| Full SBOM program | SBOM skills |
| Fixing app CMDi/XSS | domain security skills |
| Secrets in repo | `secrets-management-hygiene` |

## Commands

```bash
composer --version
composer install --no-interaction
composer audit
composer audit --format=json
composer audit --locked
# Abandoned packages often listed; treat as maintenance risk
```

Exit code non-zero when advisories found (version-dependent) — use in CI.

## Workflow

### 1. Confirm scope and success

1. App repos, PHP/Composer versions, whether monorepo packages.
2. Success: CI fails on high/critical (per policy); upgrade path known; ignores time-boxed.
3. Inventory private satis/packagist mirrors.

### 2. Baseline audit

```bash
composer audit --format=json > /tmp/composer-audit.json
composer show --tree | head
```

1. List direct vs transitive vulns.
2. Note abandoned packages in use.

### 3. Triage

| Factor | Action |
| --- | --- |
| Fixed version available | Upgrade within constraints; run tests |
| No fix yet | Mitigate (WAF, disable feature), monitor, ticket |
| Dev-only package | Still triage if used in CI/prod build |
| False positive | Document; narrow ignore with expiry |

### 4. Remediate

```bash
composer update vendor/package --with-dependencies
composer update  # only if intentional full bump
composer audit
phpunit  # or project test command
```

1. Prefer minimal version bumps that clear advisories.
2. For major bumps: changelog review + regression tests.
3. Remove abandoned packages when replacements exist.

### 5. CI gate

```yaml
# GitHub Actions sketch
- name: Composer audit
  run: |
    composer install --no-interaction --prefer-dist
    composer audit --locked --no-interaction
```

1. Cache Composer downloads carefully; still re-run audit every build.
2. Optional: fail only on severity threshold if tool supports filters; else fail-all + ignore list.

### 6. Ignore policy

```json
// composer.json config.audit.ignore — use sparingly; example conceptual
```

1. Every ignore: CVE/advisory ID, reason, owner, expiry date.
2. Review ignores quarterly.
3. Never permanent ignore of actively exploited RCE without exec approval.

### 7. Hand off

1. Dashboard or CI badge for audit status.
2. Runbook: emergency upgrade + deploy.
3. SBOM export if org requires (separate skill).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Lockfile | Committed + audited | Deploy without lock |
| CI | Blocks known vulns | Audit only on laptop yearly |
| Upgrade | Tested minimal bump | Blind `composer update` on Friday prod |
| Ignore | Expiry + owner | `--ignore` forever |
| Abandoned | Plan replace | Depend forever |

## Output Checklist

- [ ] `composer audit` baseline captured
- [ ] Findings triaged (direct/transitive)
- [ ] Upgrades tested and merged
- [ ] CI gate enabled on lockfile
- [ ] Ignores documented with expiry
- [ ] Abandoned packages planned
- [ ] Residual risk accepted formally if any
- [ ] Owners for PHP deps clear

## Rules

- Owned PHP apps only for enforcement changes.
- Evidence is audit JSON + green tests after upgrade.
- Prefer fix over ignore.
- Focus on **Composer audit**; other ecosystems have their own skills.
