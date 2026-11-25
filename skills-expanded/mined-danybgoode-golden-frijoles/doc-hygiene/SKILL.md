---
name: doc-hygiene
summary: "Measures the always-read session-start docs and writes a dated report of bloat and duplication."
description: >
  Keeps the always-read session-start docs (this project's AGENTS.md, Roadmap/WAYS-OF-WORKING.md,
  Roadmap/LEARNINGS.md, Roadmap/README.md poster) from re-bloating after the one-time de-noise sweep.
  Use when the product owner asks to "check doc hygiene", "measure LEARNINGS size", "is LEARNINGS
  bloated again", "run the doc hygiene report", or as the weekly Routine C hygiene pass. Runs
  scripts/doc-hygiene.mjs, reviews its flagged candidates against the source docs, and emits a dated
  advisory report. Never edits Roadmap docs — proposals only, the product owner or the builder
  hand-merges.
# Repo-local scripts this skill wraps — its FULL closure: the entry script, everything it imports,
# scripts it runs as subprocesses, and data files it reads by path. Paths are relative to the
# CONSUMING project's scripts/ dir; they deliberately do NOT ship inside this plugin. CI
# (scripts/check-skill-scripts.mjs) walks the import graph and fails if this list understates it.
requires_scripts:
  - doc-hygiene.mjs
  - roadmap-extract.mjs
  - doc-format.mjs
  - doc-format.enforced.json
  - lib/roadmap-contract.mjs
  - lib/result-dates.mjs
  - lib/project-root.mjs
  - lib/epic-kickoff.mjs
  - lib/stage-facts.mjs
  - lib/stage.mjs
  - lib/work-branch.mjs
  - lib/board-text.mjs
  - lib/config-registry.mjs
  - lib/config.mjs
  - roadmap-push.mjs
---

# Doc hygiene — rolling maintenance for the always-read set (Cowork or Claude Code)

<!-- kit block: frozen at the move out of the plugin (plugin-1-0 S3.3); nothing renders it now, and in this repo
     the local scripts/ copy always wins, so the pinned version below is only the fallback. -->
> **Running this skill's scripts.** Each `node scripts/<name>.mjs <args>` below means, from the project root:
> `if [ -f scripts/<name>.mjs ]; then node scripts/<name>.mjs <args>; else npx -y @golden-frijoles/kit@0.45.0 <name> <args>; fi`
> The project's own copy always wins. The kit needs no install and copies nothing into the repo. If npx fails on
> the network or the registry (ENOTFOUND, ECONNREFUSED, ETIMEDOUT, E404, a proxy error), report **could not
> look: the kit is unreachable**, not a broken project, and offer to retry online or to copy the script into
> `scripts/`. This covers the scripts the kit carries (`frijoles-kit --list`). Any other `scripts/` command here is
> project tooling: if the project lacks it, say so and stop. Never re-implement a script's logic inline.
> If a script prints `GF-NEEDS-SETTING {"key",…}`, ask the user that question once, save the answer with
> `npx -y @golden-frijoles/kit@0.45.0 config set <key> <value>` (always the kit, never local-wins: a project
> may own an unrelated `scripts/config.mjs`), tell them they can change it later the same way, and run the
> script again if it exited 7.
<!-- kit:end -->

> **This skill never writes to `Roadmap/LEARNINGS.md` or `Roadmap/README.md`.** It measures, flags
> candidates, and writes ONE new dated report file (`Roadmap/00-ideas/DOC-HYGIENE-REPORT-<date>.md`).
> Any actual edit to the source docs is a separate, human-reviewed change — same discipline as the
> standing `HYGIENE-REPORT-*.md` convention from Routine C.

## When to run me
The product owner asks to check doc hygiene, measure the always-read set, or investigate whether `LEARNINGS.md`/
the poster are bloating again — or the weekly **Routine C** roadmap-hygiene pass invokes me as its
fourth step (`scripts/routines/roadmap-hygiene.prompt.md`).

## What already exists (reuse, don't rebuild)
- **`scripts/doc-hygiene.mjs`** — the mechanical part. Run it first, always:
  `node scripts/doc-hygiene.mjs` (writes the dated report) or `node scripts/doc-hygiene.mjs --check`
  (prints only, writes nothing — use this for a quick look or when just verifying the script itself).
- **`scripts/doc-format.mjs`** — the FORMAT half of doc hygiene (this script is the content half):
  epic README / sprint / retrospective shape against the refine templates. `node scripts/doc-format.mjs`
  reports every finding; `--check` fails only on the paths in `scripts/doc-format.enforced.json`;
  `--fix` rewrites only the mechanical ones. Include its report summary in yours.
- **`scripts/roadmap-extract.mjs`** — the epic-status SSOT the script's "archived epic mention" check
  reads. Don't re-parse frontmatter yourself. (A project scaffolded before the extractor was split out
  of `roadmap-to-notion.mjs` has the same rows behind `roadmap-to-notion.mjs --extract`.)
- **`Roadmap/00-ideas/HYGIENE-REPORT-*.md`** — the sibling dated-advisory-report format from Routine C
  (funnel/status drift). This skill's report is a **different concern** (doc size/dedupe, not
  funnel/epic status), hence the distinct `DOC-HYGIENE-REPORT-` filename — don't conflate the two.
- **The `doc-hygiene-learnings-sweep` epic** (`Roadmap/09-platform-infra/doc-hygiene-learnings-sweep/`)
  — the one-time sweep this skill exists to keep from being needed again. Its `RETROSPECTIVE.md` has
  the original before/after numbers if you need a size baseline.

## Stage 1 — Run the script
`node scripts/doc-hygiene.mjs` (or `--check` for a dry look). It prints:
- the always-read set's line/KB sizes (a table), so you can compare against the last known-good
  baseline (the sweep's before/after, or the previous `DOC-HYGIENE-REPORT-*.md`);
- **flagged candidates** in `LEARNINGS.md` and the `README.md` poster: possible near-duplicate bullets
  (same section, high word overlap), referenced file paths not found in any known app root, and
  bullets mentioning an epic whose README frontmatter is now `Archived`.

## Stage 2 — Verify every flagged candidate before reporting it as real (the script is deliberately dumb)
The script's heuristics are cheap word-overlap and path-existence checks — they exist to **narrow
where to look**, not to assert staleness. For each flagged item:
- **Near-duplicate bullets**: read both bullets in context. A shared topic with different why/date/
  source is *not* a duplicate — the LEARNINGS discipline (below) explicitly wants related lessons kept
  as separate bullets when they're separate incidents.
- **Dead path reference**: check **every** app root the project has before concluding a path is gone —
  in a multi-app setup this checkout may not be authoritative for each app's own `main` (they can be
  separate, gitignored repos here). A bullet describing a **swap** (e.g. "converted `app/robots.ts` →
  `app/robots.txt/route.ts`") will *always* flag the old path — that's the bullet correctly documenting
  history, not staleness.
- **Archived-epic mention**: read the bullet. Mentioning an archived epic isn't wrong by itself (a
  bullet can legitimately reference the epic that *caused* an archival, e.g. "supersedes the
  neon-egress spike's call") — only flag it onward if the *lesson itself*, not just the epic name, is
  now incorrect.

## Stage 3 — Emit the report, propose, don't touch
Write the dated report (the script does this automatically unless `--check`). If Stage 2 turned up a
genuine candidate worth acting on, **propose it in the report** (or, if invoked ad hoc, describe
the specific edit you'd make) — do not edit `LEARNINGS.md`/`README.md` yourself as part of this skill.
An actual edit is a separate, explicit, human-reviewed change (same as the original sweep: reviewed diff
+ a "removed & why" note + before/after counts, no silent deletions).

## Stage 4 — Wire-in: weekly Routine C
`scripts/routines/roadmap-hygiene.prompt.md`'s step 4 runs this skill and folds its findings into the
same weekly `claude/` docs PR Routine C already opens — a fourth report section alongside funnel
refining / status drift / board regeneration, not a second PR.

---

## Gotchas
- **The LEARNINGS discipline is the thing this skill exists to protect — internalize it before
  proposing any edit.** Every retained line keeps its **why + date/source**; dedupe by **sharpening the
  existing line**, never appending a near-duplicate; **no silent deletions** — anything removed is named
  in a "removed & why" note; a human confirms before merge. Over-pruning to hit a size target is exactly
  the failure mode the epic warns against — bias toward merging/tightening over deleting.
- **A word-overlap "near-duplicate" flag is not proof.** Two bullets about the same tool/file from two
  different incidents are supposed to stay separate if they have different why/date/source — the
  script cannot tell "same topic" from "same lesson," only a human/model read can.
  **A dead-path flag says nothing about "was this ever true"** — it only means the path isn't in this
  checkout right now, which can be because the app moved on (real staleness) or because this monorepo
  checkout of `apps/*` is stale relative to the app's own `main` (not staleness at all). Confirm against
  the app repo before concluding anything.
  **An archived-epic mention is often the DESIRED reference**, not staleness — several LEARNINGS bullets
  explicitly cite an archived epic as the thing they superseded. Read the bullet before flagging it as
  wrong.
- **Never auto-edit.** This skill's only write output is a new dated report file. If you find yourself
  about to run an `Edit` against `LEARNINGS.md` or `README.md` while "running doc-hygiene," stop — that's
  a separate, explicitly-requested sweep, not this skill's job.
- **Don't let the report collide with Routine C's own `HYGIENE-REPORT-*.md`.** This skill's output is
  `DOC-HYGIENE-REPORT-<date>.md` (doc size/dedupe) — a distinct file from Routine C's funnel/status-drift
  report, even though both land in `Roadmap/00-ideas/` on the same day.
