---
name: php-monorepo-builder
description: Use `symplify/monorepo-builder` to manage PHP monorepos with `vendor/bin/monorepo-builder` and `monorepo-builder.php`. Trigger this skill when the user mentions monorepo-builder, merging package `composer.json` files into a root `composer.json`, validating inter-package versions, configuring package directories, propagating dependencies, or automating monorepo releases and release workers.
version: 1.0.0
source: https://github.com/symplify/monorepo-builder
license: MIT
doc_version: 12.5.2
---

# monorepo-builder

A set of tools for managing PHP monorepos: merging `composer.json` files, validating package versions, releasing with automation, and more.

**Repository:** [symplify/monorepo-builder](https://github.com/symplify/monorepo-builder)
**Package:** `monorepo-php/monorepo` (via Packagist)
**Language:** PHP 8.2+
**License:** MIT License
**Latest Release:** 12.5.2 (2026-03-26)

---

## When to Use This Skill

Use this skill when you need to:

- **Set up a new PHP monorepo** — scaffolding directory structure, initial `monorepo-builder.php` config
- **Merge `composer.json` files** — aggregate dependencies from all packages into the root `composer.json`
- **Validate version consistency** — ensure all inter-package dependencies use matching version constraints
- **Automate releases** — bump versions, tag releases, push tags across all packages in one command
- **Manage package discovery** — configure which directories are scanned for packages, and which to exclude
- **Append or remove data after merge** — add shared dev dependencies, remove per-package-only entries
- **Troubleshoot merge issues** — composer section ordering, dropped custom keys, `readme` property loss (fixed in 12.5.0)
- **Configure release workers** — customize the sequence of steps that run during a release

---

## Quick Reference

### Installation

```bash
composer require monorepo-php/monorepo --dev
```

Requires **PHP 8.2+**. For PHP 8.1, use `symplify/monorepo-builder:^11.2` (no longer maintained).

### Initialize a New Monorepo

```bash
vendor/bin/monorepo-builder init
```

Generates a basic monorepo structure and a starter `monorepo-builder.php` config at your project root.

---

### Core Commands

| Command | Description |
|---|---|
| `vendor/bin/monorepo-builder merge` | Merge all package `composer.json` into root |
| `vendor/bin/monorepo-builder validate` | Check that inter-package versions are consistent |
| `vendor/bin/monorepo-builder propagate` | Push root dependency versions back into package `composer.json` files |
| `vendor/bin/monorepo-builder bump-interdependency <version>` | Update mutual package constraints to one target version |
| `vendor/bin/monorepo-builder package-alias` | Update `branch-alias` across package `composer.json` files |
| `vendor/bin/monorepo-builder localize-composer-paths` | Swap mutual package paths to local paths for pre-split testing |
| `vendor/bin/monorepo-builder release <version>` | Tag and release a new version across all packages |
| `vendor/bin/monorepo-builder init` | Scaffold a new monorepo structure |

---

### Configuration: Package Directories

All configuration lives in `monorepo-builder.php` at the project root.

```php
use Symplify\MonorepoBuilder\Config\MBConfig;

return static function (MBConfig $mbConfig): void {
    // Scan multiple directories for packages
    $mbConfig->packageDirectories([
        __DIR__ . '/packages',
        __DIR__ . '/projects',
    ]);

    // Exclude specific packages from discovery
    $mbConfig->packageDirectoriesExcludes([
        __DIR__ . '/packages/secret-package',
    ]);
};
```

---

### Configuration: Merge — Append and Remove Data

```php
use Symplify\MonorepoBuilder\ComposerJsonManipulator\ValueObject\ComposerJsonSection;
use Symplify\MonorepoBuilder\Config\MBConfig;
use Symplify\MonorepoBuilder\ValueObject\Option;

return static function (MBConfig $mbConfig): void {
    // Add data to root composer.json after merge
    $mbConfig->dataToAppend([
        ComposerJsonSection::AUTOLOAD_DEV => [
            'psr-4' => [
                'Symplify\Tests\\' => 'tests',
            ],
        ],
        ComposerJsonSection::REQUIRE_DEV => [
            'phpstan/phpstan' => '^2.1',
        ],
    ]);

    // Remove data from root composer.json after merge
    $mbConfig->dataToRemove([
        ComposerJsonSection::REQUIRE => [
            // Version is irrelevant — removed by key
            'phpunit/phpunit' => '*',
        ],
        ComposerJsonSection::REPOSITORIES => [
            Option::REMOVE_COMPLETELY,
        ],
    ]);
};
```

> **Note (12.5.0+):** `dataToAppend` now supports arbitrary composer.json keys — no longer limited to 24 hardcoded sections.

---

### Run a Merge

```bash
vendor/bin/monorepo-builder merge
```

Reads all `composer.json` files in discovered package directories and merges their dependencies into the root `composer.json`.

---

### Release a New Version

```bash
vendor/bin/monorepo-builder release 1.2.0
```

Runs all configured release workers in sequence (bump versions, create tags, push, etc.).

### Split Packages to Separate Repositories

Monorepo Builder does not handle package splitting itself. For split repos, pair it with `symplify/github-action-monorepo-split` in GitHub Actions.

---

## Key Concepts

### Package Discovery

By default, monorepo-builder scans `./packages` for subdirectories containing a `composer.json`. You configure additional or alternative directories with `packageDirectories()`. Packages whose directory names contain `tests` may be excluded — see issue #59.

### Merge Behaviour

The `merge` command aggregates `require`, `require-dev`, `autoload`, `autoload-dev`, and other sections from all discovered packages into the root `composer.json`. Since **12.5.0**, custom/non-standard keys (e.g. `scripts-aliases`, `abandoned`, `readme`) are preserved during merge.

### Release Workers

Release workers are discrete steps executed in sequence during a release. They can be customized or reordered. A known issue (#77) exists where `SetNextMutualDependenciesReleaseWorker` always increments the minor version — review worker ordering carefully.

### Version Validation

The `validate` command checks that when package A depends on package B (both in the monorepo), the version constraint in A's `composer.json` matches the actual version of B. This prevents inter-package version drift.

---

## Known Issues

### Open Issues

| # | Summary |
|---|---|
| #90 | [Feature] Conventional Commit release support |
| #77 | `SetNextMutualDependenciesReleaseWorker` always updates minor version |
| #76 | No helper to import autoloader regardless of monorepo depth |
| #72 | Incompatible declaration in `EventDispatcher.php` |
| #69 | Composer install behaviour question |
| #59 | Packages with `tests` in name are always ignored |
| #25 | Interdependency version update fails for pre-release versions |

### Recently Fixed (12.5.0 — 2026-02-13)

- **Merge now preserves unknown/custom composer.json sections** — `scripts-aliases`, `abandoned`, `readme`, and any non-standard keys are no longer dropped (#105, #106, #71, #107)
- **`dataToAppend` supports arbitrary composer.json keys** — no longer limited to 24 hardcoded sections (#105)

### Recent Releases

| Version | Date | Highlights |
|---|---|---|
| **12.5.2** | 2026-03-26 | Allow `sebastian/diff ^8` (#110) |
| **12.5.0** | 2026-02-13 | Preserve custom composer.json sections; arbitrary `dataToAppend` keys |

*See `references/releases.md` for full release notes.*

---

## Reference Files

| File | Contents | Confidence |
|---|---|---|
| `references/README.md` | Full README: install, commands, configuration options, usage examples | Medium |
| `references/releases.md` | Release notes for all tagged versions (2 releases) | Medium |
| `references/issues.md` | All 34 GitHub issues — 7 open, 27 closed — with labels and dates | Medium |
| `references/file_structure.md` | Repository directory tree (813 items) | Medium |

---

## Working with This Skill

### Beginner

1. Run `vendor/bin/monorepo-builder init` to scaffold your monorepo.
2. Add packages under `packages/` (each with its own `composer.json`).
3. Run `vendor/bin/monorepo-builder merge` to sync dependencies into root.
4. Check `references/README.md` for full configuration options.

### Intermediate

- Customize `monorepo-builder.php` to add multiple package directories and exclusions.
- Use `dataToAppend` to inject shared dev tooling (PHPStan, PHPUnit) into root `composer.json`.
- Use `dataToRemove` to strip per-package-only entries (e.g. local repositories) from the merged root.
- Run `validate` in CI to catch inter-package version drift early.
- Use `propagate` or `bump-interdependency` when root and package version constraints need to move together.

### Advanced

- Configure and reorder release workers for custom release pipelines.
- Use `Option::REMOVE_COMPLETELY` to drop entire sections (e.g. `repositories`) after merge.
- Be aware of issue #77 when using `SetNextMutualDependenciesReleaseWorker` — it may bump the minor version unexpectedly.
- For pre-release versions (alpha/beta/RC), see issue #25 before relying on automatic interdependency updates.
- Use branch-aware tag validation if you maintain multiple active major version lines.

---

**Source:** GitHub repository `symplify/monorepo-builder` | Last updated: 2026-04-11
