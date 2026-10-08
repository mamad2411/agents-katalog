# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**World Cup 104** — a match-prediction competition platform. Users predict all 104 World Cup matches plus season-long outcomes, results are imported from data providers, a scoring engine awards points, and users compete on multiple leaderboards (global, league, accuracy, perfect-104) with a heavy gamification layer (titles, streaks, trophies, Hall of Fame, share cards). See `PRD.md` for full feature scope.

**Stack source of truth is `composer.json`, not `PRD.md`.** The PRD lists an aspirational/outdated stack (Laravel 12, Livewire 3, Flowbite, MySQL+Redis+Horizon). What is actually installed: **PHP 8.3, Laravel 13, Livewire 4, Flux UI v2 (free), Filament v5, Fortify, spatie/laravel-permission v8, Pest 4, Larastan 3, Tailwind v4.** Redis/Horizon/Reverb are *not* installed yet — add them only when a task explicitly needs them. Treat the PRD as feature/scope guidance, build to the installed versions.

The codebase is built on the **Laravel Livewire starter kit**; most app code beyond auth/settings is still to be written.

## Commands

```bash
composer dev          # Run everything: serve + queue worker + pail logs + vite (concurrently)
composer test         # Full gate: config:clear, pint --test, phpstan, then artisan test
composer lint         # pint --parallel (auto-fix)
composer types:check  # phpstan analyse (larastan)
npm run dev           # Vite dev server only
npm run build         # Production asset build

php artisan test --compact --filter=testName   # Run a single test by name
php artisan test --compact tests/Feature/X.php # Run a single test file
vendor/bin/pint --dirty --format agent         # Format only changed files (run before finalizing PHP changes)

# Dev commands (knockout testing)
php artisan dev:seed-knockout-results --stage=round_of_32               # Seed random knockout results for a stage
php artisan dev:seed-knockout-results --stage=round_of_32 --dry-run     # Preview without persisting
php artisan dev:seed-knockout-results --stage=all                       # Seed all knockout stages in order
php artisan dev:seed-knockout-results --stage=round_of_32 --reset       # Clear results and reset to Scheduled
php artisan dev:seed-knockout-results --stage=all --reset               # Reset all knockout stages (reverse order)
```

There is no `npm test`; all tests are PHP/Pest. The DB is **MySQL** (`DB_CONNECTION=mysql` in `.env`) served via Laravel Herd at `https://worldcup-104-0-0.test`.

### Dev Knockout Results Seeder

**`dev:seed-knockout-results`** simulates knockout match results with a realistic distribution of outcome types and automatically advances winners to the next round. Use this during development to test the knockout prediction/scoring flow.

**Seed mode (default):**
- Randomly generates results for all fixtures in a stage, distributing equally across 6 outcome types: `HomeWin`, `AwayWin`, `HomeWinAet`, `AwayWinAet`, `HomeWinPens`, `AwayWinPens`.
- Fires `ResultImported` event synchronously, so points recalculate immediately.
- Automatically advances winners (and losers, for `third_place`) into downstream fixture team slots using the bracket placeholder strings (e.g. `"Winner Match 73"`).
- Use `--stage=all` to seed all knockouts in order (round_of_32 → round_of_16 → ... → final).
- Use `--dry-run` to preview changes without persisting to the database.

**Reset mode (`--reset`):**
- Clears all scores (home/away/AET/pens), nulls `points` on predictions, and reverts fixture status to `Scheduled`.
- **Also clears downstream fixtures** that reference the reset stage's match numbers — ensuring the bracket remains consistent.
- When resetting all stages with `--reset --stage=all`, processes in reverse order (final → ... → round_of_32) so downstream clears before upstream.

## Architecture

**Authentication is Fortify-backed, not Livewire-component-based.** `FortifyServiceProvider` is the wiring hub: it registers user-creation/password-reset actions (`app/Actions/Fortify/`), points Fortify's view callbacks at Blade files under `resources/views/livewire/auth/`, and defines `login`/`two-factor` rate limiters. Those auth "livewire" views are plain **Flux/Blade forms that POST to Fortify routes** — they are not Livewire class components. Don't look for `app/Livewire/Auth/`; it doesn't exist.

**Full-page Livewire (v4) components** are mounted with `Route::livewire(...)` (see `routes/settings.php`). Static pages use `Route::view`. `routes/web.php` requires `routes/settings.php`. Real Livewire class components live in `app/Livewire/` (currently only `Settings/` and `Actions/`).

**Filament v5 admin panel** is at `/admin` (`app/Providers/Filament/AdminPanelProvider.php`), primary color Amber. It auto-discovers Resources, Pages, and Widgets from `app/Filament/` — that directory doesn't exist yet, so admin CRUD for the domain models will go there via `php artisan make:filament-resource`.

**Authorization** uses `spatie/laravel-permission` v8 (roles/permissions tables migrated in `2026_06_10_...create_permission_tables.php`). The PRD also calls for Laravel Policies — combine spatie roles with policies as features land.

**API responses**: `bootstrap/app.php` renders JSON for any `api/*` path, and `f9webltd/laravel-api-response-helpers` is available for consistent API response envelopes. There are no API routes yet.

**Models use PHP 8 attribute config** (Laravel 13 style): `#[Fillable([...])]`, `#[Hidden([...])]`, and a `casts()` method rather than `$fillable`/`$hidden`/`$casts` properties — follow this pattern on `User` when creating new models.

**Identifiers — ULID primary keys (locked-in convention).** All new domain models use **ULID** primary keys so the database PK is never an enumerable integer. ULIDs are time-ordered (index-friendly, like UUIDv7) but narrower (`CHAR(26)` vs UUID's `CHAR(36)`), which keeps every secondary index and FK smaller on the high-row tables (`predictions`, `activity_events`).

- **Model:** add `use Illuminate\Database\Eloquent\Concerns\HasUlids;` — route-model binding then works automatically (the ULID *is* the route key; no `getRouteKeyName()` needed).
- **Migration PK:** `$table->ulid('id')->primary();` (force ascii to keep indexes compact: append `->charset('ascii')`).
- **Domain → domain FK:** `$table->foreignUlid('team_id')->constrained();`
- **Domain → framework FK:** the starter-kit tables (`users`, `cache`, `jobs`, spatie `permission` tables) keep their **BIGINT** keys — do **not** convert them. So a reference to a user is still `$table->foreignId('user_id')->constrained();`, not `foreignUlid`. Only domain-to-domain references use ULID FKs.
- **Never expose a sequential int** in URLs, API resources, share cards, or Filament — ULID PKs make this the default, keep it that way.
- **Exception — reference data:** `teams` and `players` are non-sensitive BBC-imported reference data and use plain **BIGINT** PKs (`$table->id()`). They are not user-generated and carry no enumeration risk. New *user-facing/sensitive* models still default to ULID.

**Tests**: Pest 4. `RefreshDatabase` is auto-applied to everything under `tests/Feature/` via `tests/Pest.php` (not to `tests/Unit/`). Most tests should be feature tests using model factories.

## Reference docs

**UI component policy: Flux first, Flowbite as fallback.** Build app UI with **Flux UI v2** (the installed kit) wherever a suitable component exists. Only reach for **Flowbite** when Flux has no equivalent or can't achieve the needed pattern (e.g. datatables, WYSIWYG, charts, complex marketing layouts). Flowbite is Tailwind + vanilla-JS data-attribute components, so when used it must be wired up manually (npm install + data attributes / init); it is not installed via npm yet.

- **Flowbite** full component reference: `.ai/flowbite-llms-full.txt` (2.7MB — read it on demand for fallback work, never inline it here). Covers Getting started/config, Components (Accordion, Modal, Drawer, Datepicker, Tables, Tabs, Toast, Carousel, Sidebar, etc.), Forms (inputs, select, file, toggle, range, floating label), Typography, and Plugins (Charts, Datatables, WYSIWYG).

## Data sources

- **OpenFootball 2026 World Cup JSON**: https://github.com/openfootball/worldcup.json/tree/master/2026 — open source JSON data for 2026 groups, tournament fixtures, qualification playoffs, stadiums, and teams. Use as a reference/import source for fixture and team data, but validate against official/provider data before treating it as canonical.
- **Local 2026 source file**: `world-cup_2026.json` at the repository root. Prefer this local file when building fixture importers or seed data so imports are reproducible.

<laravel-boost-guidelines>
=== foundation rules ===

# Laravel Boost Guidelines

The Laravel Boost guidelines are specifically curated by Laravel maintainers for this application. These guidelines should be followed closely to ensure the best experience when building Laravel applications.

## Foundational Context

This application is a Laravel application and its main Laravel ecosystems package & versions are below. You are an expert with them all. Ensure you abide by these specific packages & versions.

- php - 8.3
- filament/filament (FILAMENT) - v5
- laravel/fortify (FORTIFY) - v1
- laravel/framework (LARAVEL) - v13
- laravel/prompts (PROMPTS) - v0
- livewire/flux (FLUXUI_FREE) - v2
- livewire/livewire (LIVEWIRE) - v4
- larastan/larastan (LARASTAN) - v3
- laravel/boost (BOOST) - v2
- laravel/mcp (MCP) - v0
- laravel/pail (PAIL) - v1
- laravel/pint (PINT) - v1
- laravel/sail (SAIL) - v1
- pestphp/pest (PEST) - v4
- phpunit/phpunit (PHPUNIT) - v12
- tailwindcss (TAILWINDCSS) - v4

## Skills Activation

This project has domain-specific skills available in `**/skills/**`. You MUST activate the relevant skill whenever you work in that domain—don't wait until you're stuck.

## Conventions

- You must follow all existing code conventions used in this application. When creating or editing a file, check sibling files for the correct structure, approach, and naming.
- Use descriptive names for variables and methods. For example, `isRegisteredForDiscounts`, not `discount()`.
- Check for existing components to reuse before writing a new one.

## Verification Scripts

- Do not create verification scripts or tinker when tests cover that functionality and prove they work. Unit and feature tests are more important.

## Application Structure & Architecture

- Stick to existing directory structure; don't create new base folders without approval.
- Do not change the application's dependencies without approval.

## Frontend Bundling

- If the user doesn't see a frontend change reflected in the UI, it could mean they need to run `npm run build`, `npm run dev`, or `composer run dev`. Ask them.

## Documentation Files

- You must only create documentation files if explicitly requested by the user.

## Replies

- Be concise in your explanations - focus on what's important rather than explaining obvious details.

=== boost rules ===

# Laravel Boost

## Tools

- Laravel Boost is an MCP server with tools designed specifically for this application. Prefer Boost tools over manual alternatives like shell commands or file reads.
- Use `database-query` to run read-only queries against the database instead of writing raw SQL in tinker.
- Use `database-schema` to inspect table structure before writing migrations or models.
- Use `get-absolute-url` to resolve the correct scheme, domain, and port for project URLs. Always use this before sharing a URL with the user.
- Use `browser-logs` to read browser logs, errors, and exceptions. Only recent logs are useful, ignore old entries.

## Searching Documentation (IMPORTANT)

- Always use `search-docs` before making code changes. Do not skip this step. It returns version-specific docs based on installed packages automatically.
- Pass a `packages` array to scope results when you know which packages are relevant.
- Use multiple broad, topic-based queries: `['rate limiting', 'routing rate limiting', 'routing']`. Expect the most relevant results first.
- Do not add package names to queries because package info is already shared. Use `test resource table`, not `filament 4 test resource table`.

### Search Syntax

1. Use words for auto-stemmed AND logic: `rate limit` matches both "rate" AND "limit".
2. Use `"quoted phrases"` for exact position matching: `"infinite scroll"` requires adjacent words in order.
3. Combine words and phrases for mixed queries: `middleware "rate limit"`.
4. Use multiple queries for OR logic: `queries=["authentication", "middleware"]`.

## Artisan

- Run Artisan commands directly via the command line (e.g., `php artisan route:list`). Use `php artisan list` to discover available commands and `php artisan [command] --help` to check parameters.
- Inspect routes with `php artisan route:list`. Filter with: `--method=GET`, `--name=users`, `--path=api`, `--except-vendor`, `--only-vendor`.
- Read configuration values using dot notation: `php artisan config:show app.name`, `php artisan config:show database.default`. Or read config files directly from the `config/` directory.

## Tinker

- Execute PHP in app context for debugging and testing code. Do not create models without user approval, prefer tests with factories instead. Prefer existing Artisan commands over custom tinker code.
- Always use single quotes to prevent shell expansion: `php artisan tinker --execute 'Your::code();'`
  - Double quotes for PHP strings inside: `php artisan tinker --execute 'User::where("active", true)->count();'`

=== php rules ===

# PHP

- Always use curly braces for control structures, even for single-line bodies.
- Use PHP 8 constructor property promotion: `public function __construct(public GitHub $github) { }`. Do not leave empty zero-parameter `__construct()` methods unless the constructor is private.
- Use explicit return type declarations and type hints for all method parameters: `function isAccessible(User $user, ?string $path = null): bool`
- Use TitleCase for Enum keys: `FavoritePerson`, `BestLake`, `Monthly`.
- Prefer PHPDoc blocks over inline comments. Only add inline comments for exceptionally complex logic.
- Use array shape type definitions in PHPDoc blocks.

=== deployments rules ===

# Deployment

- Laravel can be deployed using [Laravel Cloud](https://cloud.laravel.com/), which is the fastest way to deploy and scale production Laravel applications.

=== herd rules ===

# Laravel Herd

- The application is served by Laravel Herd at `https?://[kebab-case-project-dir].test`. Use the `get-absolute-url` tool to generate valid URLs. Never run commands to serve the site. It is always available.
- Use the `herd` CLI to manage services, PHP versions, and sites (e.g. `herd sites`, `herd services:start <service>`, `herd php:list`). Run `herd list` to discover all available commands.

=== tests rules ===

# Test Enforcement

- Every change must be programmatically tested. Write a new test or update an existing test, then run the affected tests to make sure they pass.
- Run the minimum number of tests needed to ensure code quality and speed. Use `php artisan test --compact` with a specific filename or filter.

=== laravel/core rules ===

# Do Things the Laravel Way

- Use `php artisan make:` commands to create new files (i.e. migrations, controllers, models, etc.). You can list available Artisan commands using `php artisan list` and check their parameters with `php artisan [command] --help`.
- If you're creating a generic PHP class, use `php artisan make:class`.
- Pass `--no-interaction` to all Artisan commands to ensure they work without user input. You should also pass the correct `--options` to ensure correct behavior.

### Model Creation

- When creating new models, create useful factories and seeders for them too. Ask the user if they need any other things, using `php artisan make:model --help` to check the available options.

## APIs & Eloquent Resources

- For APIs, default to using Eloquent API Resources and API versioning unless existing API routes do not, then you should follow existing application convention.

## URL Generation

- When generating links to other pages, prefer named routes and the `route()` function.

## Testing

- When creating models for tests, use the factories for the models. Check if the factory has custom states that can be used before manually setting up the model.
- Faker: Use methods such as `$this->faker->word()` or `fake()->randomDigit()`. Follow existing conventions whether to use `$this->faker` or `fake()`.
- When creating tests, make use of `php artisan make:test [options] {name}` to create a feature test, and pass `--unit` to create a unit test. Most tests should be feature tests.

## Vite Error

- If you receive an "Illuminate\Foundation\ViteException: Unable to locate file in Vite manifest" error, you can run `npm run build` or ask the user to run `npm run dev` or `composer run dev`.

=== livewire/core rules ===

# Livewire

- Livewire allow to build dynamic, reactive interfaces in PHP without writing JavaScript.
- You can use Alpine.js for client-side interactions instead of JavaScript frameworks.
- Keep state server-side so the UI reflects it. Validate and authorize in actions as you would in HTTP requests.

=== pint/core rules ===

# Laravel Pint Code Formatter

- If you have modified any PHP files, you must run `vendor/bin/pint --dirty --format agent` before finalizing changes to ensure your code matches the project's expected style.
- Do not run `vendor/bin/pint --test --format agent`, simply run `vendor/bin/pint --format agent` to fix any formatting issues.

=== pest/core rules ===

## Pest

- This project uses Pest for testing. Create tests: `php artisan make:test --pest {name}`.
- The `{name}` argument should not include the test suite directory. Use `php artisan make:test --pest SomeFeatureTest` instead of `php artisan make:test --pest Feature/SomeFeatureTest`.
- Run tests: `php artisan test --compact` or filter: `php artisan test --compact --filter=testName`.
- Do NOT delete tests without approval.

</laravel-boost-guidelines>
