---
name: php-composer
description: Use when managing PHP dependencies with Composer — version constraints, PSR-4 autoload, scripts, path/vcs repositories, minimum-stability, allow-plugins.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: language
  languages: [php]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [php-essentials, php-symfony, security]
---

# Composer

**Iron Law: commit `composer.lock` and deploy with `composer install` (never `update`). `install` resolves the EXACT versions in the lockfile; `update` re-resolves against constraints and silently bumps transitive deps. `update` is a developer action that produces a reviewable lockfile diff — it is NOT a deploy step.**

**Version:** Composer `2.8.x` · — _2.x is the only supported line; `composer audit` ships built-in, parallel downloads are default, and the resolver is orders of magnitude faster than 1.x. Run `composer self-update` to stay current._

## require vs require-dev

```json
{
  "require": {
    "php": ">=8.5",
    "ext-ctype": "*",
    "symfony/console": "*"
  },
  "require-dev": {
    "phpunit/phpunit": "*",
    "phpstan/phpstan": "*",
    "roave/security-advisories": "dev-latest"
  }
}
```

`require` = runtime deps shipped to production. `require-dev` = test/lint/dev tooling, excluded by `composer install --no-dev`. Declare PHP version and `ext-*` requirements in `require` so the resolver and `composer check-platform-reqs` enforce them. `composer require symfony/console` adds to `require`; add `--dev` for the dev section.

## Semver constraints

| Constraint   | Matches                         | Use                                                      |
| ------------ | ------------------------------- | -------------------------------------------------------- |
| `^3.4`       | `>=3.4.0 <4.0.0`                | **default** — allows compatible (minor/patch) updates    |
| `~3.4`       | `>=3.4.0 <3.5.0`                | patch-only; tighter than `^` at the last specified digit |
| `~3.4.2`     | `>=3.4.2 <3.5.0`                | pin minor, allow patch                                   |
| `3.4.*`      | `>=3.4.0 <3.5.0`                | wildcard — same as `~3.4` in practice                    |
| `*`          | any stable                      | lets a meta-package / monorepo dictate the version       |
| `8.1.*`      | the `8.1` series                | pin a framework train (Symfony LTS-style)                |
| `dev-main`   | the `main` branch tip           | track a branch; needs `minimum-stability` to allow it    |
| `4.18.x-dev` | dev builds of the `4.18` branch | branch-alias dev versions                                |
| `dev-latest` | the `latest` branch             | rolling deps like `roave/security-advisories`            |

Prefer `^` for libraries. `*` and `dev-*` are deliberate choices (meta-packages, vendored branches) that the lockfile pins to a concrete commit anyway — the looseness lives in `composer.json`, the determinism in `composer.lock`.

## PSR-4 autoload

```json
{
  "autoload": {
    "psr-4": {
      "App\\": "src/",
      "Acme\\": "packages/acme/src/"
    },
    "files": ["src/bootstrap.php"],
    "exclude-from-classmap": ["packages/acme/src/Bundle/recipe"]
  },
  "autoload-dev": {
    "psr-4": { "App\\Tests\\": "tests/" }
  }
}
```

`psr-4` maps a namespace prefix to a directory — `App\Order\Money` → `src/Order/Money.php`. `files` is eager-loaded on every request (use sparingly — helpers, polyfill shims, global functions that can't be autoloaded). `autoload-dev` keeps test namespaces out of the production classmap. After editing autoload config run `composer dump-autoload`.

## Scripts, auto-scripts, @-references

```json
{
  "scripts": {
    "auto-scripts": {
      "cache:clear": "symfony-cmd",
      "assets:install %PUBLIC_DIR%": "symfony-cmd"
    },
    "lint": ["vendor/bin/php-cs-fixer fix --using-cache=no"],
    "post-install-cmd": ["@auto-scripts", "@my-build"],
    "post-update-cmd": ["@auto-scripts"],
    "my-build": "php bin/console app:build"
  }
}
```

`@name` references another script (composes pipelines: `post-install-cmd` runs `@auto-scripts` then `@my-build`). `symfony-cmd` is a Symfony Flex handler that runs the key as a console command. Lifecycle hooks (`post-install-cmd`, `post-update-cmd`, `pre-autoload-dump`) fire automatically. Run a named script with `composer lint`; pass args via `composer lint -- --dry-run`.

## path & vcs repositories

```json
{
  "repositories": [
    {
      "type": "path",
      "url": "./acme-plugin",
      "options": { "symlink": true }
    },
    {
      "type": "vcs",
      "url": "https://github.com/your-fork/SncRedisBundle",
      "no-api": true
    }
  ]
}
```

**`path`** — install a sibling package from a local directory; `symlink: true` makes edits live (changes in `./acme-plugin` appear instantly, no re-install). The backbone of monorepo/multi-app development. **`vcs`** — install from a git fork/branch by URL; `no-api: true` clones over git instead of hitting the GitHub API (avoids rate limits, works for forks where releases aren't tagged). Both let you depend on `dev-main` of a fork before it's on Packagist.

## minimum-stability & prefer-stable

```json
{
  "minimum-stability": "dev",
  "prefer-stable": false
}
```

`minimum-stability` is the floor (`stable` > `RC` > `beta` > `alpha` > `dev`). Default is `stable`, which rejects any `dev-*` or branch constraint. A project tracking forks and branch tips sets it to `dev`. `prefer-stable: true` then prefers a stable release where one satisfies the constraint, falling back to dev — the safe pairing. Setting `prefer-stable: false` (as the source project does) means dev versions win whenever allowed: maximum freshness, you own the breakage. Treat project-wide `dev` as a supply-chain exposure — a compromised upstream `dev-main` ships arbitrary code on the next `composer update`, so pin forks to reviewed commits and run `composer audit` against the committed lockfile in CI (it works under `--no-dev`, unlike `roave/security-advisories`). Per-package `@dev` stability flags (`"foo/bar": "*@dev"`) scope looseness to one dep instead of the whole project.

## replace & conflict

```json
{
  "replace": {
    "symfony/polyfill-mbstring": "*",
    "symfony/polyfill-php84": "*"
  },
  "conflict": {
    "symfony/symfony": "*"
  }
}
```

`replace` declares "this package provides X, don't install X separately" — on PHP 8.4+ the polyfills are dead weight (the functions are native), so replacing them with `*` strips them from the tree. `conflict` forbids a package from co-existing: `symfony/symfony` is the monolithic meta-package; conflicting it forces the resolver to use the individual `symfony/*` components and fails loudly if anything drags the monolith back in.

## config.allow-plugins

```json
{
  "config": {
    "allow-plugins": {
      "symfony/flex": true,
      "symfony/runtime": true,
      "php-http/discovery": true
    },
    "sort-packages": true,
    "optimize-autoloader": false,
    "apcu-autoloader": true,
    "classmap-authoritative": false
  }
}
```

Since Composer 2.2, plugins run code at install time and must be explicitly allowed — an unlisted plugin is blocked with a prompt (CI hangs without it). Never set `"allow-plugins": true` (allows arbitrary install-time code from any dep — a supply-chain hole); enumerate the exact plugins. See `Skill(devkit:security)`.

## Autoloader optimization

| Flag                     | Effect                                                                            |
| ------------------------ | --------------------------------------------------------------------------------- |
| `optimize-autoloader`    | builds a classmap from PSR-4 rules — skips filesystem `stat` per class            |
| `classmap-authoritative` | classmap is the ONLY source; unmapped class = not found (fastest, no FS fallback) |
| `apcu-autoloader`        | caches class→file lookups in APCu across requests                                 |

Production deploy: `composer install --no-dev --optimize-autoloader --classmap-authoritative`. Dev leaves `optimize-autoloader: false` so newly-added classes resolve without a re-dump. `classmap-authoritative` is unforgiving — only enable it on an immutable build artifact.

## roave/security-advisories

```bash
composer require --dev roave/security-advisories:dev-latest
```

A `conflict`-only meta-package: it has no code, it declares conflicts against every package version with a known CVE. The resolver then REFUSES to install a vulnerable version — security as a constraint, enforced at `composer update` time, not as a separate audit step. Complements (doesn't replace) `composer audit`, which reports advisories for what's already locked.

## Anti-patterns

- `composer update` on a production deploy — re-resolves and silently bumps transitive deps; use `install`
- Not committing `composer.lock` — every environment resolves different versions; non-reproducible builds
- `"allow-plugins": true` — runs arbitrary install-time code from any dependency; enumerate plugins
- `minimum-stability: dev` without `prefer-stable: true` (unless intentional) — pulls dev builds where a stable release exists
- Everything in `require`, nothing in `require-dev` — ships phpunit/phpstan to production
- Editing `vendor/` directly — wiped on next install; fork + `vcs` repository instead
- `classmap-authoritative` in dev — new classes 404 until you re-dump; it's a build-artifact flag
- Loose `*` constraints across the board without a lockfile review discipline — surprise major bumps
- `files` autoload for things that could be classes — eager-loaded on every request

## Red flags

| Thought                                           | Reality                                                                         |
| ------------------------------------------------- | ------------------------------------------------------------------------------- |
| "I'll run `composer update` on the server"        | that re-resolves constraints; deploy is `composer install`, full stop           |
| "lockfile conflict — I'll just delete it"         | the lockfile IS the dependency decision; resolve the merge, don't discard it    |
| "set allow-plugins to true so CI stops prompting" | you just allowed arbitrary code from every dep; list the four plugins you trust |
| "I need a patched fork — I'll edit vendor/"       | add a `vcs` repo pointing at the fork; `vendor/` is disposable                  |
| "`*` everywhere is simpler"                       | the lockfile pins it anyway, but a `^` floor documents intent and blocks majors |

## Hand-off

For PHP language rules the dependencies are written against: `Skill(devkit:php-essentials)`. For Symfony Flex recipes, bundle configuration, and the `extra.symfony` block: `Skill(devkit:php-symfony)`. For supply-chain trust, `allow-plugins` review, and CVE handling: `Skill(devkit:security)`.
