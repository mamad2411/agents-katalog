---
name: vibe-breakpoint
description: Find how many users a web app can handle at the same time before it slows down or fails, and which database queries get slower as data grows (N+1 queries, missing indexes, unbounded fetches). Runs on an isolated copy of the app with a throwaway database; never changes the project. Use when the user asks whether their app will scale, how many users it can handle, or why it is slow.
---

# /vibe-breakpoint

Define once: `VB` = `node "${CLAUDE_SKILL_DIR}/scripts/vibe-breakpoint.mjs"`. If the path above still contains the literal `${`, stop and tell the user the skill path was not resolved.
`PROJECT` = absolute path of the git root (`git rev-parse --show-toplevel`), or the current directory if there is none.
Run every command non-interactively.

## Never
- Open, read or print a real env file (`.env`, `.env.local`, `.env.production`, ...). `.env.example`, `.env.sample`, `.env.template` are fine. Env names come from `inspect.json`.
- Connect to any database, URL or host from the user's config (no psql, curl, fetch against them).
- Modify anything outside `PROJECT/.vibe-breakpoint/`.
- Invent numbers. Every number comes from `result.json` or the CLI output.
- Put env values or secrets in any file or reply.

## Step 1: Inspect
Run `VB inspect PROJECT` and read the JSON it prints.
- `supported` is false: tell the user the `unsupported_reason` in plain words, then stop.
- `docker.available` is false: follow **No-Docker path**, then stop.

## Step 2: Read the code, write the inputs
Use `${CLAUDE_SKILL_DIR}/references/framework-notes.md` to find routes, auth and schema. Write `PROJECT/.vibe-breakpoint/scenario.json` and `seed.json` following `${CLAUDE_SKILL_DIR}/references/inputs.md`.
If `has_scenario` / `has_seed` is true, reuse the existing file, say so, and do not overwrite it.

## Step 3: One message (questions and consent)
Ask only what the code cannot show (for example which flow matters most); skip the questions if there are none. In the same message give this consent text:

> vibe-breakpoint will: copy this project to a temporary folder (your files are not changed; results go to `.vibe-breakpoint/`); build the app image and start containers on an offline Docker network: your app, a throwaway Postgres in memory, a mock for outside services, and k6 for load (image `grafana/k6`); download images: `<missing_images from inspect.json, or "none, all are local">`; take roughly 10-15 minutes (build 2-5 min, data seeding and query probe 2-5 min, load test up to 6 stages x 60 s, stops early when the app breaks); remove all containers and temp files at the end. OK to go ahead?

Without a clear yes, stop.

## Step 4: Run
After the yes, run `VB run PROJECT --pull` with the Bash tool's `run_in_background`, and wait for it to exit. `--pull` only after consent.
- Exit 0: continue.
- Exit 2: unsupported; explain the reason in plain words.
- Exit 1 with `scenario.json:` or `seed.json:` in the output: that file is invalid (this fails before Docker). Fix it and run once more without asking again.
- Any other exit 1: explain the last lines in plain words. Do not retry.
- Exit 129, 130 or 143, or the user stopped it: run `VB cleanup` and say the run was interrupted.
Never run `render` after a failed run.

## Step 5: Code locations
Read `PROJECT/.vibe-breakpoint/out/result.json`, key `flags`. For each flag find the handler using `${CLAUDE_SKILL_DIR}/references/query-patterns.md`. Write `PROJECT/.vibe-breakpoint/code-locations.md` (overwrite every run):

```
### <flag> - <endpoint>
- <file>:<line> - <what the code does>
- Fix: <one line>
```
No secrets or env values. If the cause is not found, say so.

## Step 6: Render and reply
Run `VB render PROJECT`. Reply in under 8 lines:
- the breaking point ("handles about N users" or "no breaking point up to N") and the limiting resource,
- the top data-growth issue with `file:line`,
- limits that matter (for example OAuth-only login so only public endpoints were tested, SDKs that cannot reach the mock),
- paths: `.vibe-breakpoint/out/report.md` and `.vibe-breakpoint/out/chart.png`.

## No-Docker path
Read the code with `${CLAUDE_SKILL_DIR}/references/query-patterns.md` and write `PROJECT/.vibe-breakpoint/static-report.md`, starting exactly with:

```
# vibe-breakpoint static report (no load test): <project name>

**No load test ran** because <docker.reason from inspect.json>. Nothing was measured; the findings below come from reading the code for known slow-query patterns. Start Docker and run /vibe-breakpoint again for real numbers.
```
Then, per finding: pattern name, `file:line`, why it grows, suggested fix. No measured-looking numbers (no users, ms or row counts). Reply in under 8 lines with the reason and the file path.

## Cleanup
`VB cleanup` is always safe to run. Mention it whenever a run was interrupted.
