# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Antrenman Log" — a single-user personal weight & strength-training tracker. Plain PHP 8.1+ with PDO/MySQL, no framework, no build step, no dependencies (Chart.js is pulled from a CDN at runtime). UI text and code comments are in **Turkish** — keep new strings and comments in Turkish to match.

The actual application lives in [antrenman-log/](antrenman-log/). The repo root only holds duplicate copies of `README.md` and `schema.sql`.

## Running / setup

There is no build, lint, or test tooling. To run locally it must be served by PHP+MySQL (this checkout sits under XAMPP's `htdocs`).

1. Create the DB: `mysql -u root -p < antrenman-log/schema.sql` (or import via phpMyAdmin). The script creates the `gymtrack` database itself.
2. Edit the 4 DB constants at the top of [antrenman-log/config.php](antrenman-log/config.php).
3. Open the directory in a browser. Default login: user `zeyt`, password `antrenman` (seeded by `schema.sql`).

## Architecture

Classic page-per-file PHP. Every page follows the same top-of-file contract:

```php
require __DIR__ . '/config.php';   // PDO ($pdo), helpers, session
require_login();                   // redirects to login.php if not authed
$me = current_user($pdo);          // the single user row (cached static)
// ... handle POST (with check_csrf()), run queries ...
$title = '...'; $nav = '...';      // then:
require __DIR__ . '/header.php';   // opens <html>, topbar nav, flash msg
// ... HTML body ...
require __DIR__ . '/footer.php';   // closes the document
```

[config.php](antrenman-log/config.php) is the shared core — DB connection, session bootstrap, and all helper functions. Read it before touching any page. Key helpers:
- `h($s)` — HTML-escape; wrap **all** output of user/DB data with it.
- `require_login()`, `current_user($pdo)` — auth gate and the single-user record.
- `csrf_token()` / `csrf_field()` / `check_csrf()` — every `<form method="post">` must emit `csrf_field()`, and every POST handler must call `check_csrf()` first.
- `flash($msg)` / `take_flash()` — one-shot messages; `header.php` renders them.
- `redirect($to)` — Location header + exit.

Pages handle their own POST at the top, then **redirect after a successful POST** (Post/Redirect/Get) rather than rendering. Forms use a hidden `action` field to multiplex multiple operations (e.g. `add`, `delset`, `note` in [log.php](antrenman-log/log.php)) through one endpoint.

### Pages
- [index.php](antrenman-log/index.php) — dashboard: weight stats, goal progress bar, bodyweight chart, recent workouts.
- [workout.php](antrenman-log/workout.php) — list workouts; start a new one (creates row → redirects to `log.php`).
- [log.php](antrenman-log/log.php) — the core set-entry screen for one workout. Notable: the `last_time()` function fetches the previous session's sets for each exercise ("geçen sefer" / progressive-overload reference).
- [weight.php](antrenman-log/weight.php), [history.php](antrenman-log/history.php), [exercises.php](antrenman-log/exercises.php), [settings.php](antrenman-log/settings.php), [login.php](antrenman-log/login.php), [logout.php](antrenman-log/logout.php).

### Data model ([schema.sql](antrenman-log/schema.sql))
`users` (one row) → `workouts` (a session on a date, labeled A/B/Serbest) → `workout_sets` (exercise + reps + weight per set). `exercises` is a reusable library categorized by `session` (A/B/both/none). `bodyweight` holds daily weigh-ins (unique per user+date). All child tables cascade-delete and scope queries by `user_id = $me['id']`.

## Conventions

- **Always parameterize** SQL via PDO prepared statements — never interpolate input. Emulated prepares are off (`ATTR_EMULATE_PREPARES => false`).
- Weight inputs accept comma decimals — normalize with `str_replace(',', '.', ...)` before casting (see `log.php`).
- A NULL `weight` means a bodyweight exercise, displayed as "VA".
- Styling is one hand-written file, [style.css](antrenman-log/style.css) (dark theme); reuse existing classes (`card`, `btn`, `stat`, `pill`, `muted`, `row`) rather than adding inline styles where a class exists.
- When editing `schema.sql`, remember both root and `antrenman-log/` copies exist; keep them in sync.
