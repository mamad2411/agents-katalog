---
name: laravel-architecture-review
description: Review a Laravel codebase's architecture and design, not just its types. Use when asked to audit a Laravel app, find architectural smells, decide where business logic belongs (controller vs Action vs Service), whether a Repository/DDD/TDD layer is justified, or how to apply SOLID/DRY to a Laravel project. Runs the real tools (Larastan, Rector, Pest) when present, then applies design heuristics the linters cannot see, and produces a prioritized report calibrated to the app's actual scale. Anti-dogma: it refuses to push Repository or DDD on apps that do not need them. Triggers: laravel architecture review, laravel code audit, refactor laravel, where should this logic go, service class vs controller, repository pattern laravel, DDD laravel, SOLID laravel, clean up laravel codebase, laravel best practices.
---

# Laravel: architecture review

Larastan finds type errors. Pint fixes formatting. Rector modernizes syntax. **None of them tell you the business logic is in the wrong place.** This skill is the layer above the linters: it reads design intent and flags where structure has drifted, then recommends the fix that fits the app's real scale, not a pattern from a blog post.

The single rule that makes this skill worth using: **recommend a pattern only when the code earns it.** Most "best practices" advice fails because it applies enterprise patterns to a CRUD app. A Repository layer to "abstract the ORM you will never swap" is ceremony Laravel's own team argues against. Match the recommendation to the evidence.

## Step 0 - Detect before you judge

Everything downstream depends on these. Never recommend a pattern without them.

```bash
php artisan --version                                  # Laravel version -> which idioms apply
composer show | grep -E 'pestphp/pest|phpunit|larastan|rector|pint'   # what tooling exists
php artisan route:list --json | jq length              # rough app size
ls app/Models | wc -l                                  # model count
find app/Http/Controllers -name '*.php' | wc -l        # controller count
```

**Scale sets the bar.** A 5-model app with 20 routes is a different conversation than a 60-model app with 400 routes. Small app: keep it flat, controllers + FormRequests + a few Actions. Large app with a genuinely complex domain: that is when Services, bounded contexts, and maybe DDD start paying rent. State the scale bracket at the top of every report so the reader sees the recommendations are sized, not generic.

## Step 1 - Run the tools that are already there

Do not hand-audit what a tool already checks. Run what exists, suggest installing what does not, never hard-require.

### Larastan (static analysis) - package is `larastan/larastan`
```bash
# if missing:  composer require --dev larastan/larastan
vendor/bin/phpstan analyse --memory-limit=2G
```
`phpstan.neon` includes `vendor/larastan/larastan/extension.neon`. Levels run 0-10 (`max` = 10). New audit target: level 5-6 with a baseline for legacy code, raise over time. Larastan's findings are type-level; fold them in but they are not the architecture story.

### Rector (automated refactoring) - use the maintained fork
```bash
# rector/rector-laravel is ABANDONED. use driftingly/rector-laravel
composer require rector/rector driftingly/rector-laravel --dev
vendor/bin/rector process --dry-run          # shows changes, writes nothing
```
Config uses `RectorLaravel\Set\LaravelSetList` and `LaravelLevelSetList` (higher version sets include lower ones). `--dry-run` output is a free list of mechanical wins you can offer to apply later.

### Pest (test coverage) - v5 is the current line
```bash
vendor/bin/pest --coverage --min=0           # where is the critical-path coverage?
```
Pest 5 (PHP 8.4, PHPUnit 13) ships **Tia** (test impact analysis, re-runs only affected tests), a first-party **PHPStan plugin** (types your `it()`/`expect()`), **Rector rules** that convert raw assertions to Pest matchers, and **Evals** for AI output. If the app is on Pest, mention Tia for CI speed and the PHPStan plugin for typed tests, but coverage on business-critical paths is the architecture signal you care about here.

## Step 2 - The design heuristics (what the linters miss)

For each, cite a concrete `file:line` as evidence. No evidence, no finding.

| Smell you detect | Recommend | Do NOT recommend when |
|---|---|---|
| Controller method with real logic (many lines, queries, branching) | Extract to a single-purpose **Action** (`app/Actions`) or a **Service** | It is thin CRUD delegating to Eloquent - leave it |
| Same complex query chain duplicated across many callers | A query **Scope**, or a **Repository** only if truly reused across sources | One or two callers - a local scope is enough, no repository |
| Business logic living in a Model (beyond relations/scopes/casts) | Move to an Action/Service; keep the model about data | Accessors, casts, scopes, relationships - those belong there |
| Inline `$request->validate([...])` with many rules | **FormRequest** | Trivial 1-2 rule cases - inline is fine |
| A block repeated N times across classes | Extract to a **trait** or a small **helper/service** | Coincidental similarity that will diverge - premature DRY is its own smell |
| Authorization checks scattered in controllers | **Policies** / Gates | One-off check with no reuse |
| God model / God service (hundreds of lines, many concerns) | Split by responsibility (SRP), pull cohesive groups into Actions | It is large but genuinely one cohesive concern |
| No test on a business-critical path (from Pest coverage) | Add a **feature test** for that path first | Framework glue, generated scaffolding |

## Step 3 - N+1 and eager loading (check the AppServiceProvider FIRST)

Do not sprinkle `with()` blindly. The right fix depends on what the app already declares globally. Check `app/Providers/AppServiceProvider.php` before writing a single N+1 finding:

- **`Model::automaticallyEagerLoadRelationships()` is set** (Laravel 12.8+): the framework auto-eager-loads accessed relationships app-wide. Do **not** recommend adding manual `with()` for accessed relations - that is redundant. Only flag spots the auto-loader cannot help (e.g. relationships loaded conditionally in ways that defeat it).
- **`Model::preventLazyLoading()` or `Model::shouldBeStrict()` is set**: the app already throws `LazyLoadingViolationException` in dev, so N+1 is caught by the test suite, not by manual review. Recommendation becomes "run the suite / exercise the pages", not a code audit.
- **None of these are set** (the common case): the systemic fix beats scattered `with()`. Recommend adding to `AppServiceProvider::boot()`:
  ```php
  use Illuminate\Database\Eloquent\Model;

  Model::automaticallyEagerLoadRelationships();          // Laravel 12.8+: auto eager load
  Model::preventLazyLoading(! $this->app->isProduction()); // throw on N+1 in dev only
  // or the full strict bundle:
  // Model::shouldBeStrict(! $this->app->isProduction());  // + discarded attrs + missing attrs
  ```
  This surfaces every N+1 as a hard error in dev instead of a silent slowdown in prod. It is one edit that fixes the whole class of bug, which is exactly the lazy-in-the-good-sense fix a per-query `with()` never is.

## Step 4 - The anti-dogma stance (the part that makes this credible)

Say these out loud in the report when relevant. This is the differentiator from every generic "best practices" skill.

- **Repository pattern**: Eloquent *is* your data-access layer. Wrapping it to "swap the database later" is abstracting against a change that almost never comes. Recommend a repository only for genuine query reuse of complex logic or a real second data source. Otherwise: query scopes and Actions.
- **DDD**: earns its keep in a genuinely complex domain with real invariants and ubiquitous language, not a CRUD app. For most apps the lighter ladder is enough: **Controller -> FormRequest -> Action/Service -> Eloquent**. Reach for bounded contexts only when the domain, not the developer, demands it.
- **SOLID**: a lens for spotting a class doing too much or a hard-wired dependency, not a checklist to satisfy. Prefer Laravel-native seams (container binding, events, policies) over hand-rolled interfaces with one implementation.
- **TDD**: recommend where the logic is worth protecting (money, permissions, domain rules). Do not demand 100% coverage of framework glue.
- **Prefer native over generic**: FormRequest over inline validation, Policy over inline checks, Scope over repository, Action over service-with-one-method, Event/Listener over manual wiring. The framework already gives you the seam.

## Step 5 - Output: a prioritized report, then offer to fix

Produce a report, never silently edit. Structure:

1. **App scale** (version, size bracket, tooling present) - so recommendations read as sized.
2. **Findings, ranked by severity**, each: `file:line`, the smell, the recommendation, and *why it fits this app*.
3. **Mechanical wins** - the `rector --dry-run` list and any obvious extract-to-trait / inline-validation-to-FormRequest, marked as auto-fixable.
4. **Close with the offer**: "Want me to apply the safe fixes? These are mechanical and reversible: [list]." Only refactor on an explicit yes, one finding at a time, tests green before and after.

## Guardrails

- **Evidence or it does not ship.** Every finding names a real `file:line`. No hypothetical smells.
- **Size the advice.** Never recommend Repository/DDD/CQRS without the scale and duplication to justify it. When unsure, recommend the lighter Laravel-native option.
- **Report first.** Default is read-only analysis. Apply fixes only when the user says yes, and only the mechanical ones unless they ask for more.
- **Verify version-specific claims.** Idioms move between Laravel versions (automatic eager loading is 12.8+, strict mode APIs evolved). Confirm against the detected version, not memory.
- **Do not fight the framework.** If the recommendation contradicts a documented Laravel idiom, the idiom wins.
