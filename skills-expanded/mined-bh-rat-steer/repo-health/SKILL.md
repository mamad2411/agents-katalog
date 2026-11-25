---
name: repo-health
description: "Generates a repository health report: commit activity, code inventory, TODO debt, test presence. Use when the user asks for a repo health check, codebase overview, or tech-debt snapshot."
metadata:
  version: 0.1.0
---

# repo-health
Produce a one-page health report for the repository in the current
workspace: recent commit activity, what the codebase is made of, how much
marked debt (TODO/FIXME) it carries, and whether tests exist. The result
the user gets is `out/health/REPORT.md`, with trends against the previous
run.

This skill bundles its own steer runtime at `scripts/steer.py`; the
commands below invoke it with `python3` and need nothing installed.
Paths are relative to this skill's directory: when your working
directory is elsewhere (it usually is), use the skill's full path
(`python3 <path-to-this-skill>/scripts/steer.py ...`).

## Before you start

1. **Ground yourself.** Run `python3 scripts/steer.py context` and read
   the snapshot before doing anything else; it tells you the platform,
   project type, git state, and which tools exist here.
2. **Apply past lessons.** Run `python3 scripts/steer.py learn show` and
   follow what it says; those lessons came from real previous runs.
3. **Check credentials**, only when the user wants the summary posted to
   their webhook (`scripts/share.py`). Run `python3 scripts/steer.py
   secrets check REPO_HEALTH_WEBHOOK`. If it is missing, ask the user to
   run `python3 scripts/steer.py secrets set REPO_HEALTH_WEBHOOK` (never
   ask them to paste the value into the chat), then re-check.

## Process

This skill has an enforced flow: steps verify themselves against
reality, and you cannot skip ahead.

1. Announce: "Working through the repo-health flow."
2. Run `python3 scripts/steer.py flow status` (in the workspace) to see
   progress and the current step.
3. Do what the directive says. Steps with a verify condition complete
   automatically once reality matches; for mandate steps, mark completion
   with `python3 scripts/steer.py flow done <step-id>`.
4. Run `python3 scripts/steer.py flow next` and repeat until it reports
   all steps complete.

Do NOT claim the work is done while `python3 scripts/steer.py flow
status` shows incomplete steps. The flow is defined in `flow.toml`.

## Memory

This skill persists data between runs with the bundled `store` command
(per-skill SQLite). `scripts/report.py` records this run's totals at
workspace scope to power the report's Trend section; if the user asks
"compared to what?":

    python3 scripts/steer.py store get last_totals --scope workspace

Use `--scope workspace` for state that belongs to this project rather
than the user.

## Background processes

Start helpers through the bundled runtime so nothing leaks or zombies.
If the user wants to browse the report:

    python3 scripts/steer.py proc start health-preview --ready-port 8642 -- python3 -m http.server 8642 --directory out/health
    python3 scripts/steer.py proc status health-preview
    python3 scripts/steer.py proc stop health-preview      # always stop what you started

## Learning

This skill improves with use. As you work:

- The moment the user corrects you, or something fails and then works a
  different way, capture it:
  `python3 scripts/steer.py learn note "<one imperative rule>" --kind correction`
  Lessons are atomic rules ("Use X not Y when Z"), never secrets.
- When a lesson from `python3 scripts/steer.py learn show` helped, run
  `python3 scripts/steer.py learn confirm <id>`; when one was wrong,
  `python3 scripts/steer.py learn dispute <id>`.
- Before finishing, record the outcome:
  `python3 scripts/steer.py learn run ok` (or `failed` with `--note`).

If a `learnings.md` exists in this skill, read it too; those are
promoted lessons that shipped with the skill.

## Output

Scripts print a single JSON result envelope to stdout
(`{"status", "summary", "data", "artifacts"}`); read `status` instead of
parsing prose. Diagnostics go to stderr.

## Gotchas

- Not a git repository → `collect` still works; the Activity section says
  so instead of failing.
- The scripts skip `.git`, virtualenvs, `node_modules`, build output, and
  `out/` itself; binary and >1MB files are excluded from line counts.
- The report is a snapshot, not a judgment: present findings, let the
  user decide what matters.
