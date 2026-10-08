---
name: project-maintainer
description: Maintain an llmwiki-style open-source project across the full framework pipeline. Use when the user says "maintain the project", "check my tasks", "update progress", "run phase gate", "do a monthly verify", "lint my wiki", "check stale entries", or invokes any form of ongoing project-keeping chore. Reads _progress.md, tasks.md, docs/roadmap.md, and .github issues to figure out what's next and what's drifted.
---

# project-maintainer

## What this skill does

The **Maintainer** owns the full Open Source Framework v4.1 pipeline on a project. Given the current repo state, it:

1. **Audits phase gates** — are we in the right phase? Are the deliverables for the current phase complete?
2. **Reconciles task tracking** — keeps `tasks.md`, `_progress.md`, and GitHub issues in sync (the framework's "dual-tracking" rule).
3. **Runs stale checks** — flags content, links, and claims older than the stale threshold.
4. **Triggers CI** — re-runs the privacy grep, performance budget check, and link checker.
5. **Reports next action** — tells the user exactly what to do next and why.

It works for any project that follows the framework — not just llmwiki.

## When to invoke

- "Maintain the project" / "maintenance check" / "do a health check"
- "Update progress" / "reconcile tasks" / "sync tasks"
- "Check phase gate" / "can I move to the next phase"
- "Lint the wiki" / "check for stale entries"
- "Monthly verify" / "quarterly review"
- Any time the user is unsure what to work on next

## Framework phase awareness

| Phase | The Maintainer's job in this phase |
|---|---|
| **0 Capture** | Verify `idea-brief.md` exists and names target users + the 10x mechanism |
| **1 Validate** | Verify scorecard /25 is in `_progress.md` and ≥20 |
| **1.25 Research** | Verify `.temp/` has at least 10 cloned reference repos and `docs/research.md` exists with a gap matrix |
| **1.5 Steering** | Verify `_progress.md` has "Key Decisions" table filled in |
| **1.75 Agent Survey** | For agent-native tools — verify adapter compatibility matrix exists |
| **2 Brand** | Verify `README.md`, `LICENSE`, and badges are in place |
| **3 Structure** | Verify folder layout matches `docs/architecture.md` |
| **4 Content** | Track which `M` items in `docs/roadmap.md` are ✅ vs `[ ]` |
| **5 Contribution** | Verify `CONTRIBUTING.md`, PR template, issue templates, CI workflow |
| **5.25 Adapter Flow** | For agent-native tools — verify adapter contract doc + at least one community contribution example |
| **5.5 Pre-Launch QA** | Run the full QA checklist from `docs/framework.md` |
| **6 Launch** | Verify git tag + GitHub Release + social posts drafted |
| **6.5 Self-Demo** | Verify GitHub Pages workflow triggered and live URL returns 200 |
| **7 Grow** | Track stars / forks / downloads week-over-week |
| **7.5 Living Knowledge** | Verify public wiki is updating on release |
| **8 Maintain** | Run monthly verification, merge PRs, update stale entries |

## Workflow

1. **Locate the project root.** Look for `_progress.md` in the current dir or its parents. If missing, tell the user this skill needs a project that follows the framework.

2. **Read the state files:**
   - `_progress.md` — current phase + phase status table
   - `tasks.md` — Kiro-style tasks with `[ ]`/`[/]`/`[x]`/`[-]` markers
   - `docs/roadmap.md` — if present, the master MoSCoW table
   - `CHANGELOG.md` — latest release

3. **Audit each phase gate up to the current phase.** For each phase marked done, verify the deliverable file exists and is non-empty. Report any gaps.

4. **Reconcile task tracking:**
   - Are there items in `tasks.md` marked `[x]` but not in `CHANGELOG.md`?
   - Are there open GitHub issues with no matching task in `tasks.md`?
   - Are there tasks in `tasks.md` with no corresponding GitHub issue?
   - If any drift — propose fixes before making any changes.

5. **Run stale checks:**
   - Any `last_updated` in wiki frontmatter older than 30 days? Flag.
   - Any `source_file` reference in wiki pointing to a file that no longer exists? Flag.
   - Any entity page mentioned in 3+ sources but with its own `last_updated` older than the newest source? Flag.
   - Any `[[wikilink]]` pointing to a non-existent page? Flag.

6. **Run CI gates locally** (if configured):
   - Privacy grep: `grep -r "<real_username>" site/ wiki/` must be empty
   - Link check: `python3 -m llmwiki lint-docs` (when implemented)
   - Performance budget: build time `<15s`, HTML `<50MB`

7. **Write the report.** Structure:
   ```
   ## Health report: <project> — <date>

   **Phase:** <current phase> (<status>)

   ### ✅ Green
   - <things that are fine>

   ### ⚠️ Yellow
   - <minor drift that should be fixed soon>

   ### ❌ Red
   - <broken gates that block progress>

   ### Next action
   1. <specific thing the user should do next>
   2. <second thing if any>
   ```

8. **Offer to fix green issues automatically.** For yellow/red, ask before touching anything.

## Hard rules

1. **Never silently update `_progress.md`.** Always explain what changed and why.
2. **Never close a GitHub issue** without the user saying so.
3. **Never overwrite `tasks.md`** without showing the diff first.
4. **Respect the framework's "one PR per concern" rule** — if a fix spans multiple files, surface it as multiple suggestions, not one big patch.
5. **Never auto-bump versions.** Version bumps are a launch activity, not maintenance.

## Related skills

- `self-learn` — when a new pattern emerges during maintenance, pipe it to `self-learn` to potentially add it to the framework.
- `llmwiki-query` — when you need context from past sessions on why a decision was made.
- `llmwiki-lint` — for wiki-specific lint work (overlaps with step 5).
