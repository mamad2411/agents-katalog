---
name: make-better
description: "One-command Make Better — auto-decides between bootstrap, refresh, or review-only based on registry state. Orchestrates /systems-discover and /systems-review. Flags: [count] [subsystem] [--no-discover|--rebuild|--discover-only] [--yes]"
disable-model-invocation: false
model: opus
---

You are running the `/make-better` orchestrator. Your job is to glue `/systems-discover` and `/systems-review` into a single user-facing flow, with smart defaults driven by registry state.

The user invocation is in `$ARGUMENTS`. Follow this procedure exactly.

## Step 1 — Parse $ARGUMENTS

Tokens may appear in any order. Process tokens left-to-right:

- `--no-discover` → set `skip_discover = true` (run review only)
- `--rebuild` → set `force_full_discover = true` (force a full re-discovery before review)
- `--discover-only` → set `skip_review = true` (run discovery only, no review)
- `--yes` / `-y` / `--auto` → set `non_interactive = true` (no prompts, no plan mode — agent runs to completion unattended)
- The first remaining numeric token → `count` (how many systems to review)
- All other remaining tokens, joined by space → `subsystem` filter

Defaults: `skip_discover=false`, `force_full_discover=false`, `skip_review=false`, `non_interactive=false`, `count=null`, `subsystem=null`.

If both `--no-discover` and `--discover-only` were passed, stop with: "These flags are mutually exclusive — pick one."

If both `--no-discover` and `--rebuild` were passed, stop with: "These flags are mutually exclusive — pick one."

## Step 2 — Load configuration

Run the systems-review loader (it exposes the same merged config keys we need):

```bash
bash ${CLAUDE_SKILL_DIR}/../systems-review/bin/load-config.sh
```

The output is a single merged JSON object. From it you need:
- `registry_path` (e.g. `docs/SYSTEMS.md`)
- `auto_discover_when_stale_days` (default `30`)
- `user_language` (for all messages you print)

Render every user-facing message you produce in `user_language`. Skill instructions, JSON shapes, branch names, commit messages stay English regardless.

### Model self-check

This skill is declared with `model: opus` in its frontmatter, but Claude Code versions that don't honor that field would silently fall back to the user's session model. Verify your own identity before continuing.

If your model is **not Opus** (any 4.x variant), surface a single one-line warning in `user_language`:

> "⚠ Make Better expects Opus for best results, but this turn is executing on `<your-model>`. Sub-skills are still pinned to Opus via their own frontmatter, so review/discover quality is preserved — only this orchestrator's planning is on a smaller model. Consider `/model opus` and re-running."

Then:
- If `non_interactive` is true: log the warning and continue.
- Otherwise: call `AskUserQuestion` with options `Continue anyway` (default) and `Abort — I'll switch to Opus and re-run`. Proceed based on choice.

If your model is Opus, say nothing.

## Step 3 — Inspect registry state

Read the file at `<registry_path>`:

- File does not exist → `state = "missing"`.
- File exists. Parse the YAML frontmatter (lines between two `---` at the top of the file). Look for `last_discovered_by_section`:
  - Missing, malformed, or empty `{}` → `state = "never_swept"`.
  - Otherwise find the **oldest** `<section>: <ISO date>` value. If `oldest_date < (today - auto_discover_when_stale_days)` → `state = "stale"`. Otherwise → `state = "fresh"`.

## Step 4 — Compute the plan

Pick `discover_phase` and `review_phase` from this matrix. Apply user flags AFTER state-based defaults.

State-based defaults:

| state | discover_phase | review_phase |
|---|---|---|
| missing | full discover | review |
| never_swept | full discover | review |
| stale | incremental discover | review |
| fresh | (none) | review |

Flag overrides:

- `--rebuild` → `discover_phase = "full discover"` regardless of state.
- `--no-discover` → `discover_phase = (none)`. If state is `missing`, stop with: "Registry doesn't exist at `<registry_path>`; cannot run review without discovering. Drop --no-discover, or run `/systems-discover` first."
- `--discover-only` → `review_phase = (none)`. (Discover phase still computed from state and `--rebuild`.)

Final values: `discover_phase ∈ {none, "incremental", "full"}`, `review_phase ∈ {none, "review"}`.

If both phases are `none` (e.g. `fresh` state + `--no-discover` + no `--discover-only` makes no sense, or some weird combo), stop with: "Nothing to do — both phases skipped. Check your flags."

## Step 5 — Announce

In `user_language`, print a short paragraph (3–5 lines max) explaining what you're about to do and why. Examples (English; translate as needed):

- *missing + no flags:* "No registry found at `docs/SYSTEMS.md` — bootstrapping. Phase 1: full discover (~2–5 min depending on repo size). Phase 2: review the resulting systems."
- *stale + no flags:* "Registry's oldest section was last discovered 47 days ago (threshold: 30). Phase 1: incremental discover. Phase 2: review of stale systems."
- *fresh + no flags:* "Registry is fresh (oldest section: 8 days). Skipping discover, going straight to review."
- *fresh + --rebuild:* "Forcing a full re-discovery, then review."
- *any + --discover-only:* "Discovery only — no review will run."

Do not ask for confirmation. Proceed directly.

## Step 6 — Execute discover phase (if any)

If `discover_phase` is not `none`, invoke the **systems-discover** skill via the `Skill` tool. Build its `args` by joining the relevant tokens with spaces:

- Add `--rebuild` if `discover_phase == "full"`
- Add `--yes` if `non_interactive`
- Add `subsystem` if it's set

Examples: `"--rebuild --yes flutter"`, `"--yes"`, `"flutter"`, `""`.

Wait for the skill to complete. If it errored, stop and report.

## Step 7 — Execute review phase (if any)

If `review_phase` is `review`, invoke the **systems-review** skill via the `Skill` tool. Build its `args` by joining the relevant tokens with spaces:

- Add `--yes` if `non_interactive`
- Add `count` if set
- Add `subsystem` if set

Examples: `"--yes 5 flutter"`, `"5"`, `"flutter"`, `""`.

Wait for the skill to complete.

## Step 8 — Final summary

In `user_language`, print one combined summary:
- Which phases ran.
- Discovery delta (if discover ran): how many systems added/removed/unchanged. Get this from the discover skill's own report.
- Review findings (if review ran): the per-topic counts and total. Get this from the review skill's own report.
- **If `non_interactive` was set:** explicitly list every system or proposal flagged as "skipped — human decision needed" by the sub-skills, so the user can address them on their next interactive run.
- Where to look next: relevant branches, PRs, the registry file.

Keep it tight — under 15 lines.
