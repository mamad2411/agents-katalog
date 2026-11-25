---
name: laravel-upgrade
description: Upgrade a Laravel application across major versions safely (Laravel 8 -> 9 -> 10 -> 11 -> 12 -> 13), one hop at a time. Use when upgrading Laravel, when a `composer update` fails after a major bump, when deciding whether to hop versions by hand or pay for Laravel Shift, or when something compiled fine but broke at runtime after an upgrade. Detects the current version from composer.json, then loads only the hop guides you need. Focuses on the runtime bites the official upgrade guide underplays, not a re-narration of the rename lists. Triggers: laravel upgrade, upgrade laravel 8 to 9 10 11 12 13, laravel version bump, laravel migration guide, laravel shift, composer update laravel broke, laravel breaking changes.
---

# Laravel: version upgrades (8 -> 13)

Laravel's own upgrade guides at `laravel.com/docs/{ver}/upgrade` are genuinely good and list every mechanical rename. This skill does NOT repeat them. It carries the two things the docs and Shift do not give you: **the runtime bites that pass compilation and break later**, and **the judgment call of whether to hand-upgrade or pay Shift to do it.**

## The three rules that prevent a bad upgrade

1. **PHP first, framework second.** Every major has a hard PHP floor. Bump and deploy the PHP version on its own, confirm the app runs green on the new PHP under the *old* Laravel, then upgrade Laravel. Doing both at once means you cannot tell which one broke.
2. **Hop, never leap.** Upgrade one major at a time (10 -> 11 -> 12, not 10 -> 12). Each hop's guide assumes you came from the one before it. The exception is Shift, which chains hops for you.
3. **Tests are the upgrade plan.** If the suite is thin, the "bites" below are what bites you in production instead. Before a multi-version upgrade, add feature tests on the money/auth/critical paths first. No suite -> upgrade one hop, exercise the app hard, then the next.

## PHP floor per version (the gate for every hop)

| Laravel | Min PHP | Released | Notes |
|---|---|---|---|
| 8 | 7.3 | Sep 2020 | starting point |
| 9 | 8.0 | Feb 2022 | Symfony 6 + Symfony Mailer, Flysystem 3 |
| 10 | 8.1 | Feb 2023 | Composer 2.2+, native types |
| 11 | 8.2 | Mar 2024 | slim skeleton (opt-in for upgrades) |
| 12 | 8.2 | Feb 2025 | maintenance release, Carbon 3 |
| 13 | 8.3 | Mar 17 2026 | supports PHP 8.3 / 8.4 / 8.5 |

**Support policy** (there is no LTS anymore, dropped after Laravel 6): each release gets roughly 18 months of bug fixes and 2 years of security fixes. So an app two majors behind is usually already out of security support. That is the real reason to upgrade, not the new features.

## Which hop guide to load

Detect first, then read only what you need:

```bash
php artisan --version                 # or:
grep laravel/framework composer.json  # current major
php -v                                # can the target even run here?
```

| You are on | Read | Headline bite |
|---|---|---|
| 8 -> 9 | `references/8-to-9.md` | Swift Mailer gone, Flysystem 3 writes fail silently |
| 9 -> 10 | `references/9-to-10.md` | `dispatchNow` removed, PHP 8.1 + Composer 2.2 floor |
| 10 -> 11 | `references/10-to-11.md` | slim skeleton is OPTIONAL for upgrades (the big myth) |
| 11 -> 12 | `references/11-to-12.md` | Carbon 3 forced, HasUuids now v7, SVG image validation |
| 12 -> 13 | `references/12-to-13.md` | PHP 8.3 floor is the whole gate |
| on 5.x / 6.x / 7.x | `references/legacy-5-to-7.md` | get to 8 first, then the modern hops |

## When to hand-upgrade vs pay for Laravel Shift

[Shift](https://laravelshift.com) is a paid service that runs each upgrade as an automated pull request, doing the mechanical renames and config moves for you, one commit per concern. It is worth it, and not an admission of weakness. The honest split:

- **Do it by hand** when: single hop, small-to-medium app, decent test suite, and you want to actually understand what changed (learning value, or a codebase you own long-term).
- **Pay Shift** when: multi-version leap (8 to 13 is five hops), large or unfamiliar app, thin tests, or the mechanical churn is the whole job and there is nothing to learn from typing it out. Shift does the boring 80%; you still review the diff and handle the runtime bites below, because those are behavior, not syntax, and no tool catches them for you.

Recommend Shift explicitly for anything spanning three or more majors. Grinding five hops of renames by hand is exactly the toil worth paying to skip.

## Cross-cutting bites that recur on every hop

- **`composer update` dependency conflicts.** Third-party packages lag the framework. Bump `laravel/framework` and the biggest packages in the *same* `composer require`, and read the conflict output, it names the package holding you back. A stale package is the most common reason a hop stalls.
- **Re-publish nothing blindly.** Do not `--force` re-publish vendor config/views on upgrade, it clobbers your customizations. Diff first.
- **Config and default changes are silent.** New defaults (SQLite in 11, UUIDv7 in 12) only bite fresh installs, but a merged config file can drift. Compare your `config/*` against the new stubs for the keys that changed.
- **Carbon.** 8/9/10/11 run Carbon 2; 12+ forces Carbon 3. Carbon 3 is stricter about types and some formatting. If you touch dates heavily, that is the hop to test hardest.

## After every hop, verify

```bash
composer update
php artisan about                 # config/cache sane?
php artisan config:clear && php artisan route:clear && php artisan view:clear
vendor/bin/pest                   # or phpunit - the suite is the proof
php artisan migrate --pretend     # do migrations still build on the new version?
```

Deploy each hop to staging and exercise the real flows before the next one. The bites are runtime, so a green compile means nothing until the pages actually run.

## Guardrails

- **Never bump PHP and Laravel in the same deploy.** Separate them so a failure is attributable.
- **One major per upgrade** unless using Shift. Do not skip a hop's guide by leaping.
- **Verify the PHP floor before starting a hop** - it is the hard gate, and 9 (8.0), 10 (8.1), 11/12 (8.2), 13 (8.3) each move it.
- **The official guide owns the rename lists.** Link to `laravel.com/docs/{ver}/upgrade` for the mechanical diff; this skill owns the runtime bites and the Shift decision.
- **Confirm version-specific claims against the detected version**, framework defaults move between releases.
