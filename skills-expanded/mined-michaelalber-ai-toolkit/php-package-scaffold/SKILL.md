---
name: php-package-scaffold
audience: team
description: >
  Scaffolds production-ready Composer packages for Packagist with a complete composer.json,
  PSR-4 autoloading, a Pest/PHPUnit test harness, GitHub Actions CI (PHP version matrix,
  PHPStan, PHP-CS-Fixer), and a semver tag-based publish workflow. PHP analog of
  nuget-package-scaffold, pypi-package-scaffold, and cargo-package-scaffold. Use when creating a
  reusable PHP library, configuring composer.json metadata, setting up Composer/Packagist
  publishing, or building a PHP package CI pipeline.
---

# PHP Package Scaffold (Composer / Packagist)

> "A library is a contract. Once published, every breaking change is someone else's incident."

> "Make it work, make it right, make it releasable."

## Core Philosophy

This skill produces a **publishable Composer library** — not an application. The deliverable is a package
that a stranger can `composer require vendor/package`, that installs cleanly across a matrix of supported
PHP versions, that passes static analysis and style checks in CI, and that publishes to Packagist
automatically on a semver git tag. Packagist serves whatever a tag points at, so the **tag is the
release** — discipline lives in the tag and in CI, not in a manual upload step.

A library is a long-lived contract. Semantic versioning is mandatory: `MAJOR.MINOR.PATCH`, where a MAJOR
bump is the only place a breaking change is allowed. The public API surface is everything not marked
`@internal`; treat it as frozen within a major version.

**Non-Negotiable Constraints:**
1. **Valid `composer.json`** — `composer validate --strict` passes
2. **PSR-4 autoloading** — `src/` mapped to a vendor namespace; tests in a separate `autoload-dev`
3. **`declare(strict_types=1)`** in every `src/` file
4. **Semver discipline** — tags are `vX.Y.Z`; breaking changes only on MAJOR
5. **CI gate before publish** — tests + PHPStan + style must pass on the tag
6. **Declared, bounded dependency constraints** — caret ranges, no `dev-master`, no unbounded `*`

The full domain principles, AI discipline rules, anti-pattern catalog, and error-recovery
procedures live in `references/conventions.md`.

## Workflow

### Phase 1: PLAN

Decide the package identity and surface before writing files.

```bash
php -v | head -1
# Pick: vendor/name (lowercase, hyphenated), namespace (StudlyCase), license, PHP range
# Confirm the name is free on packagist.org
```

Record: `vendor/package`, root namespace, license (SPDX id), supported PHP range, runtime deps.

### Phase 2: SCAFFOLD

See `references/composer-json-template.md` for the full manifest and `references/ci-publish-workflow.md`
for the GitHub Actions and Packagist setup.

```
composer.json
src/                       # PSR-4 root; @internal on non-public classes
tests/                     # Pest or PHPUnit; autoload-dev
.github/workflows/ci.yml   # matrix: tests + phpstan + cs-fixer
phpstan.neon.dist          # level 8
.php-cs-fixer.dist.php      # PSR-12 ruleset
CHANGELOG.md               # Keep a Changelog
README.md  LICENSE  .gitignore  .gitattributes
```

### Phase 3: VERIFY LOCALLY

```bash
composer validate --strict
composer install
vendor/bin/phpstan analyse src --level=8
vendor/bin/php-cs-fixer fix --dry-run --diff
vendor/bin/pest            # or vendor/bin/phpunit
```

### Phase 4: PUBLISH

```bash
# After CI is green on main:
# 1. Update CHANGELOG.md with the new version
# 2. Tag with semver and push
git tag v1.0.0
git push origin v1.0.0
# Packagist auto-updates via the GitHub webhook (or `composer` API hook).
```

First-time only: submit the repo URL once at packagist.org and enable the GitHub service hook so future
tags publish automatically.

**Load on demand — `references/conventions.md`:** Knowledge Base Lookups (`collection="php"`; run them before the first phase).

## State Block

```xml
<php-package-scaffold-state>
  phase: PLAN | SCAFFOLD | VERIFY | PUBLISH | COMPLETE
  package: vendor/name
  namespace: [root namespace]
  php_range: [e.g. ^8.2]
  license: [SPDX id]
  test_runner: pest | phpunit
  phpstan_level: [n]
  ci_created: true | false
  validate_passes: true | false
  packagist_registered: true | false
  last_action: [description]
</php-package-scaffold-state>
```

## Output Template

Emit a `## PHP Package Scaffold: vendor/name` report with Identity, Files Created, Gates, and Publish
checklists. The full report markdown lives in `references/conventions.md` (Output Report Template).

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `php-architecture-checklist` | Run before the first tag to verify the package's internal structure and boundaries. |
| `php-security-review` | Audit the package (and its dependencies) for OWASP and supply-chain risks before publishing. |
| `supply-chain-audit` | Review the dependency tree for known-vulnerable or unmaintained packages. |
| `php-feature-slice` | When the package provides Laravel integration, ship a service provider following slice conventions. |
| `tdd-loop` | Drive the public API test-first so the released contract is the tested contract. |
