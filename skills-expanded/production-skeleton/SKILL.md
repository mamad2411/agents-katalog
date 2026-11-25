---
name: production-skeleton
description: The foundation to lay before the first feature, not an audit — 13 gates (CI, dependency updates, env example, human-gates register, error tracking, /health, backup drill, rollback runbook, timeouts, CSRF, security headers, limits + retention, privacy page). Use before the first feature of a new project, even in an empty folder; /skeleton shows which gates exist (read-only scorecard), /skeleton fix writes the missing files (dry-run by default); on a grown app it checks the foundation is still there. Also read HUMAN-GATES.md aloud at session start when it has open lines.
---

# production-skeleton

**Skeleton, not audit. Probes, not prose. 13 gates, not 90.**

A skeleton is the floor you build before the first feature. Run this skill
first, in an empty folder if need be: it says which of the 13 gates exist,
generates the missing files for known stacks, and keeps a register of the
things only a human can do. On a grown app the same probe checks the floor is
still there.
`skeptic-review` (same repo) is the audit that proves the floor holds.

**Contents:** Commands · Session start · Statuses · Stages · HUMAN-GATES.md ·
Evidence paths · What the probe does not do · After the scorecard

## Commands

| Say | Runs | Changes files? |
|---|---|---|
| `/skeleton` | `node <skill>/scripts/probe.mjs .` | No |
| `/skeleton --url https://app.example` | probe + 2 live checks (health, headers), GET requests only | No |
| `/skeleton --url https://app.example --csrf-post` | the same + 1 cross-origin POST to `/api/health` | No files; it sends a write request to that server |
| `/skeleton --no-audit` | probe without the `npm audit` call (offline, or a slow registry) | No |
| `/skeleton fix` | `node <skill>/scripts/fix.mjs .` — plan only | No |
| `/skeleton fix --write` | generates missing files, appends human gates | Yes, never overwrites |

`<skill>` is this skill's directory. Show the scorecard verbatim; do not
paraphrase the statuses.

Gate 2 runs `npm audit --json` against `package-lock.json` when one exists, or `pip-audit` for a Python project (`requirements.txt`, or `uv.lock` exported with `uv export` to a temp file) (network, ~3 s); any high or critical finding turns the gate FAIL with the count. A missing lockfile, unsupported input, skipped package or offline registry is UNKNOWN and not verified. Python input must be exact pinned requirements; --no-deps --disable-pip prevents resolving or building it. Supply a complete resolved export for transitive dependencies.

What --url sends: `GET /api/health` (falling back to `GET /health`) and `GET /` (following redirects, headers only). Nothing else. `--csrf-post` adds `POST /api/health` with a foreign `Origin` header and an empty JSON body; the response is diagnostic only and gate 10 remains UNKNOWN because health cannot prove mutation-route protection. The POST is a write request and the probe cannot know what it does on a server, so never add `--csrf-post` on your own: use it only when the user asks for the live CSRF check on an app they own. "Read-only" describes the repo, not what a remote server does with a request.

`fix` writes only what can work in the project it finds, and says why it skipped the rest (`skip-requires`, `manual`). The one adapter is Next.js (15 or newer for the health route) + Supabase + Vercel: routes go under `src/app` when the app lives there; a Pages Router project, or one where `src/app/` sits next to a root `app/` or `pages/` (Next.js ignores `src/` then), gets a manual step instead of a route file; the CI workflow is an npm + TypeScript template that needs `package-lock.json`, `typescript` and both a `test` and a `build` script (with pnpm, yarn or bun the user writes it by hand); the `.ts` helpers need `typescript`. Read the plan's Action column to the user instead of promising that everything was generated.

The backup workflow it generates dumps the Postgres schema `public` only (no auth users, no Storage files), keeps each encrypted dump as a 90-day artifact, refuses to run in a public repository, and commits nothing to the repo unless the owner opts in. The restore drill ships without a date: gate 7 stays FAIL until a human has restored into a throwaway database. Never write a drill date for a restore that did not happen.

## Session start (gate 4)

If `HUMAN-GATES.md` exists and has open `- [ ]` lines, list them before any
feature work — the created date, the text, the due date. Stop listing when the
file is empty. A line past `stale_days` (default 7) or past its `due:` turns
the gate STALE; say so.

## Statuses

- **PASS** — evidence found. Notes marked `static:` were checked in the repo only; pass `--url` to check them live.
  PASS means the probe found the pattern, not that it works end to end. Comments are never
  evidence — whole-line, trailing or block: `# npm test` is not a CI step, `// TODO timeout` is
  not a timeout. A gate 10/11 helper counts only when the framework loads it (middleware, proxy,
  next.config, settings.py, …) or another source file imports it — after `fix --write`, wire the
  helpers in before those gates turn green. Gates 7, 9 and 12 are heuristics (a backup job name,
  a timeout near a call, a cleanup job); the live checks and the audit skill are the stronger proof.
  Gate 5 is always `static:`: a tracker init with its DSN key, or a hand-rolled reporter that has a
  body, is called, and whose alert address is named in config and read in a file that defines or
  calls a reporter. An empty `recordError() {}` plus a key name does not pass. The probe cannot
  tell a reporter that sends from one that only logs, and it cannot see an alert arrive, so never
  say "errors reach a human" as a tested fact: say the path is wired and delivery is untested.
- **FAIL** — evidence missing. The note says what was looked for and where.
- **STALE** — evidence exists but is too old (restore drill > `drill_max_days`, human gate past due).
- **UNKNOWN** — the probe tried to verify and could not: gate 2's audit did not run (offline, tool
  missing, no lockfile), or `--url` was given and the live request for gate 6, 10 or 11 failed. Counts
  as not passed. `--no-audit` is a deliberate opt-out: gate 2 then passes on its config and says so.
- **N/A** — not applicable: stage 0 (no deploy target) makes gates 5–13 N/A; any gate can be declared N/A in `HUMAN-GATES.md` frontmatter with a reason. No reason → FAIL. Gate 2 is N/A when the repo has no dependency manifest. `fix` never
  writes files or adds human gates for an N/A gate.

Score: `x/y required · x/13 total, n n/a`. Required = gates at or below the
detected stage. The badge counts total.

## Stages

Detected from the code and shown with the reason:

- **0 library** — no server framework, no deploy file, no bundled single-page app (Vite config, CRA, Angular). Gates 1–4 only.
- **1 tool** — deploys somewhere. Gates 1–4 required.
- **2 product** — personal data: an auth library or an `email|phone|name|address` column in a migration. Gates 1–9 required.
- **3 service** — payments (`stripe`, `paddle`, …). All 13 required.

Override in `HUMAN-GATES.md` frontmatter: `stage: 2`.

## HUMAN-GATES.md

```markdown
---
stage: 2
stale_days: 7
drill_max_days: 90
privacy: app/legal/page.tsx
na:
  7: managed database with provider snapshots, restore tested 2026-09-01
---
- [ ] 2026-09-12 Add SENTRY_DSN to the hosting env (due: 2026-09-19)
- [x] 2026-09-01 Commit the backup public key
```

Every frontmatter key is optional; `na` is a map of gate number → reason, and an entry without a reason counts as FAIL.

The date is the day the line was written. `fix --write` appends lines for the
things it cannot do itself (secrets, DNS, vendor accounts).

## Evidence paths (fixed, convention over configuration)

- `.env.example` (or `.env.sample` / `.env.template`) — every env var read in
  source needs a key there; and no `.env*` other than those may be tracked in
  git. A tracked one FAILs gate 3 with its first-commit date, because adding it
  to `.gitignore` later removes nothing from history: rotate first, then purge.
- `docs/ops/restore-drill.md` — the drill date is the first `YYYY-MM-DD` right after a label (`Date:`, `Last drill:`, `Viimane proov:`, any language). A label that names a plan (`Next`, `Planned`, `Due`) does not count.
- `docs/ops/rollback.md` — must mention code/deploy, schema/migration, and data.
- a file or route named `privacy` (English, eight other languages —
  privacidad, datenschutz, andmekaitse, confidentialité, integritetspolicy,
  tietosuoja, personvern, privatlivspolitik — or `gdpr`), or the file
  named by the `privacy:` key in `HUMAN-GATES.md` frontmatter; it must be
  linked as a route from a source file (a `/stem` reference), not just
  mentioned in a README.

## What the probe does not do

No performance, SEO, accessibility, code quality, or deep OWASP. Those are
other tools' jobs. Security depth: run `/cso` or a proper pentest.

## After the scorecard

End with **I can do this now:** — 1–3 numbered lines, only actions the agent
can take in this environment (write a file, run `fix --write`, add a test),
ordered by risk, not ease. Do not run them; wait for a number.

When gate 5 passes and `HUMAN-GATES.md` has no line about it, offer to add one:
"Throw one test error in production and confirm the alert reaches you". Do not
send test alerts yourself.

## Coverage limits

Read JSON coverage before interpreting a score: `audit` lists manifest results,
`manifestsNotRead` includes unsupported manifests and partially parsed TOML, and `notScanned`
counts unsupported extensions, including Vue/Svelte/Astro. Probe nested applications in their
own directory. Do not call uncovered projects clean or ready.
Generated registers leave stage automatic; deliberate lower overrides remain with a warning.
Record only completed restore drills in a Date/Last drill/Last run/Completed field.
Static import chains and CI checks are heuristics; verify execution separately.
