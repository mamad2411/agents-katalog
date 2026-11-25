---
name: adam-self-improvement
description: Runs the ADAM /reflect review loop. Use when the user types /reflect or /reflect --explain, asks "what has adam learned", asks to "review proposals" or "review the queue", or acts on a SessionStart nudge about pending proposals. Pre-filters and scores the observation journal, dispatches the adam subagent in two stages, auto-applies verified high-confidence proposals, and walks the rest of the queue for approve, reject or edit.
---

# adam-self-improvement

## When to invoke

- User types `/reflect`
- User types `/reflect --explain` (same flow, but the analyst's clustering trace is shown to the user — see §2b)
- User asks: "what has adam learned", "any proposals", "review the queue"
- SessionStart nudge said proposals are pending and user wants to act on it

## Supporting file

- [apply-by-type.md](apply-by-type.md): the Karpathy constraints and the per-type apply, move, A/B-tracking, archive, reject and edit procedures. **Read it before any apply in §3a or §4.** Its checks are mandatory. If no proposal reaches §3a or §4, you do not need it.

## Protocol

### 0. Parse flags

Check the slash-command argument string for the literal token `--explain`. Set `explain=true` when present, otherwise `explain=false`. Unknown flags: print a one-line warning, continue with `explain=false`. `--explain` is the only argument `/reflect` accepts.

### 1. Pre-filter the journal (window + exclusion) + score

Run these steps in order before dispatching the analyst. Each step writes stdout to the output file and stderr to the log file. On failure, show the stderr log to the user and apply the fallback. No failure stops the run.

| # | Step | Command | Fallback on non-zero exit |
|---|------|---------|---------------------------|
| 1 | Window filter | `node ~/.claude/adam/scripts/adam-window.mjs --home ~/.claude > /tmp/adam-windowed-journal.jsonl 2> /tmp/adam-windowed-journal.log` | Pass the raw `~/.claude/adam/journal.jsonl` path to the agent. Its manual excluded-timestamps logic still filters actioned entries. Only the freshness window is lost. |
| 2 | Score | `node ~/.claude/adam/scripts/adam-score.mjs --input /tmp/adam-windowed-journal.jsonl > /tmp/adam-scores.json 2> /tmp/adam-scores.log` | Pass `{"sessions":[],"reinforcement_candidates":[]}` (dampener defaults to 1.0). |
| 3 | A/B measure | `node ~/.claude/adam/scripts/adam-ab-measure.mjs --home ~/.claude --format json > /tmp/adam-ab-regressions.json 2> /tmp/adam-ab-regressions.log` | Pass `[]`. |
| 4 | Auto-rollback (only if step 3 found `regressed`) | `node ~/.claude/adam/scripts/adam-rollback.mjs --auto --home ~/.claude > /tmp/adam-rollback-results.json 2> /tmp/adam-rollback.log` | Continue (best-effort). |
| 5 | Evidence batching | `node ~/.claude/adam/scripts/adam-batch.mjs --input /tmp/adam-windowed-journal.jsonl > /tmp/adam-batches.json 2> /tmp/adam-batch.log` | Pass `null`. The analyst falls back to raw journal clustering. |
| 6 | Skill utility | `node ~/.claude/adam/scripts/adam-skill-utility.mjs --input /tmp/adam-windowed-journal.jsonl --json > /tmp/adam-skill-utility.json 2> /tmp/adam-skill-utility.log` | Skip (best-effort). |

What each step does and how to use its output:

1. **Window filter.** Reads the active journal and all rotated journals (weekly `journal/YYYY-Www.jsonl` and legacy size-rotated `journal/YYYY-MM-DD-<ts>.jsonl`). Applies per-signal-type sliding windows (`SIGNAL_WINDOWS_DAYS` in `adam-window.mjs`). Drops entries already actioned through the `source_entries` frontmatter of `applied/*.md` and `rejected/*.md`.
2. **Score.** Produces a per-session `dampener` (0.5 / 0.75 / 1.0, from `task_completed_count`) and a `reinforcement_candidates` list (skills cited by ≥3 clean `task_completed` events). The analyst uses both (`agents/adam.md` §"Scoring: task_completed dampener").
3. **A/B measure.** Runs on previously auto-applied proposals (see the A/B tracking append in apply-by-type.md). Output is an array of delta objects (`pre_count`, `post_count`, `delta_pct`, `status` ∈ {`improved`,`neutral`,`regressed`,`no_baseline`,`pending`}). Filter to `status == "regressed"` and pass that as `ab_regressions`. When the list is non-empty, the analyst must put a `## Regressions` section at the top of its output (`agents/adam.md` §"A/B effectiveness").
4. **Auto-rollback** (MOSS §3.5). Reverts regressed proposals before analyst dispatch. The script moves each one from `applied/` back to `proposals/` with `rolled_back: true` and creates a regression nudge. For each one, print: `adam: rolled back "<proposal_id>" — regression detected (delta: <delta_pct>%)`.
5. **Evidence batching** (MOSS §3.1). Groups entries by (signal_type, cluster_key) into coherent failure batches, with per-batch metadata such as `has_context_window` (transcript evidence attached).
6. **Skill utility** (execution-grounded selection signal, after SkillsInjector arXiv 2605.29794: utility Δ(s), not surface match). Surfaces advisory candidates for description disambiguation or archival. Ranks skills by co-occurrence with positive (`task_completed`, `clean_recovery`, `correction_free_streak`) vs negative outcome events. **CO-OCCURRENCE, NOT CAUSATION.** Show the worst 3 below-baseline skills (`lift < 0`, not low-sample) to the *user* as a one-line advisory before listing proposals (e.g. `skill-utility: chezmoi 9% pos n=85, ghostty-config 14% pos n=50, …`). Do NOT feed this into the analyst's proposal machinery or auto-draft skill archival from it. The human decides.

### 2. Dispatch the analyst (two-stage pipeline)

MOSS §3.3: "A single prompt asked to diagnose, plan, implement, verify, and decide overloads context and produces lower-quality output than a sequenced flow." Dispatch the analyst in two stages with a validation gate between them.

**Stage 1 — Diagnose + Plan**: Use the Agent tool with `subagent_type: "adam"` and prompt:

```
stage=diagnose

Read the batched journal entries, cluster by signal type, diagnose root causes,
plan fix types, and score the keypoint matrix. Write diagnoses to /tmp/adam-diagnoses.json.
Do NOT draft proposal files.

Inputs:
- windowed_journal_path: /tmp/adam-windowed-journal.jsonl
- batches_path: /tmp/adam-batches.json                     # pre-clustered evidence batches
- scores_path: /tmp/adam-scores.json
- ab_regressions_path: /tmp/adam-ab-regressions.json
- skill_utility_path: /tmp/adam-skill-utility.json         # per-skill utility Δ (worst-first); already computed in pre-analysis
- journal_path: ~/.claude/adam/journal.jsonl               # raw — fallback only
- state_path: ~/.claude/adam/state.json
- usage_path: ~/.claude/adam/usage.json
- applied_dir: ~/.claude/adam/applied/
- rejected_dir: ~/.claude/adam/rejected/
- transcripts_root: ~/.claude/projects/
- skills_root: ~/.claude/skills/

Use batches_path for pre-clustered evidence when available. Prefer context_window
fields in journal entries over transcript file lookups. Write /tmp/adam-diagnoses.json
per the "Diagnose-stage output format" in your system prompt.
```

Wait for return.

**Inter-stage validation** (§2a): after stage 1 returns, read `/tmp/adam-diagnoses.json` and validate each diagnosis:

1. Every `source_entries` timestamp exists in the windowed journal (read `/tmp/adam-windowed-journal.jsonl`, check timestamps match).
2. Every diagnosis has all four fields (`trigger`, `action`, `mismatch`, `outcome`).
3. The planned `type` is a valid proposal type.
4. Remove diagnoses that fail validation — log a one-line warning per removal.

If all diagnoses are removed or the file is missing/empty, print "adam: no valid diagnoses — nothing to implement" and skip to §6.

**Adaptive re-diagnose** (ReContext P5 — spend depth only where it is needed): after validation, collect validated diagnoses whose `mismatch` is `unclear` OR whose cluster severity-sum is top-tier (≥32, per `scores_path`); take at most the top 3 by severity. If any exist, re-dispatch **one** more `stage=diagnose` pass carrying `redigest: <their cluster_ids>` and `prior_diagnoses_path: /tmp/adam-diagnoses.json` (the analyst refines only those clusters in place), then re-run the inter-stage validation above on the refreshed file. Do this at most once per `/reflect`; clear clusters are never re-diagnosed. If none qualify, go straight to Stage 2.

**Stage 2 — Implement**: Use the Agent tool with `subagent_type: "adam"` and prompt:

```
stage=implement

Read the validated diagnoses and draft full proposal files.

Inputs:
- diagnoses_path: /tmp/adam-diagnoses.json                 # validated stage-1 output
- windowed_journal_path: /tmp/adam-windowed-journal.jsonl
- scores_path: /tmp/adam-scores.json
- ab_regressions_path: /tmp/adam-ab-regressions.json
- skill_utility_path: /tmp/adam-skill-utility.json         # per-skill utility Δ — drives the utility-lift rubric penalty
- state_path: ~/.claude/adam/state.json
- usage_path: ~/.claude/adam/usage.json
- proposals_dir: ~/.claude/adam/proposals/
- applied_dir: ~/.claude/adam/applied/
- rejected_dir: ~/.claude/adam/rejected/
- transcripts_root: ~/.claude/projects/
- skills_root: ~/.claude/skills/

Draft proposal files to proposals_dir/ for each diagnosis. Score against the
confidence rubric. Emit the clustering trace and punch list as your final message.
```

Wait for return.

### 2b. Persist and render the clustering trace

The analyst's final message always contains a fenced ` ```trace ` block (`agents/adam.md` §"Clustering trace (always emit)") immediately before its punch-list JSON line.

1. Extract the trace block. If it is missing, print `adam: trace block missing from agent output — proceeding without observability` and continue. Do not block on this.
2. ALWAYS write the trace verbatim (without the fences) to `~/.claude/adam/last-trace.txt`, overwriting each run.
3. ALWAYS show the trace's `SUMMARY:` line as a one-line status BEFORE the proposals are listed, e.g. `clustering: <SUMMARY line>`, in both modes.
4. If `explain=true`: ALSO render the full trace as a fenced ` ```text ` block under the header `Clustering trace:`. If `explain=false`: SUPPRESS the cluster-line body (step 3 already showed the SUMMARY line).

The user can re-render any past trace:

```bash
node ~/.claude/adam/scripts/adam-explain.mjs --mode summary    # SUMMARY + per-decision counts
node ~/.claude/adam/scripts/adam-explain.mjs --mode full       # verbatim trace + rejection histogram
node ~/.claude/adam/scripts/adam-explain.mjs --mode json       # machine-readable
```

### 3. Pre-apply verification gate (MOSS §3.4)

MOSS §3.4: "Verification must therefore be runtime, on a production-equivalent environment, and against the same prompts that produced the failure evidence."

For each id in `high_confidence`, read `~/.claude/adam/proposals/<id>-*.md` and run these checks. All four must pass for auto-apply. Any failure demotes the id to `queued` for manual review.

1. **Source entries exist**: every timestamp in `source_entries` frontmatter appears in `/tmp/adam-windowed-journal.jsonl`. A missing one means the evidence is stale or already actioned.
2. **Diagnosis grounded**: the `# Diagnosis` section has all four fields (Trigger, Action, Mismatch, Outcome) with ≥1 backtick-wrapped quote.
3. **Type-evidence match**: the proposal `type` matches what the evidence supports:
   - `correction` signals → `memory`, `skill_new`, `skill_edit` (not `nudge`)
   - `dead_end` signals → `nudge`, `skill_new`, `skill_edit` (not `memory`)
   - `tool_error_loop` signals → `memory`, `skill_new`, `skill_edit`
   - `harness_edit` → must cite harness-level evidence (false negative, scoring bias, window miscalibration)
4. **No conflicting applied proposal**: grep `~/.claude/adam/applied/` for a proposal with the same `target` applied in the last 7 days. This prevents stacking rapid edits.

Print `verified: <id> (4/4 checks passed)` or `demoted: <id> (failed: <check_name>)`.

### 3a. Apply verified high-confidence items

Read [apply-by-type.md](apply-by-type.md). Enforce its Karpathy constraints, then follow its §3a sections for each verified id: the per-type apply, then move, A/B tracking append and archive. Print `auto-applied N proposals: [ids]`.

### 4. Walk the queue

For each id in `queued`:

a. Read and display the proposal in full (frontmatter + body).
b. Ask the user: **approve** / **reject** / **edit**.
c. On **approve**: enforce the Karpathy constraints, apply per the apply-by-type.md §4 approve section, move the proposal to `~/.claude/adam/applied/<ts>-<id>.md`, and archive it.
d. On **reject**: follow apply-by-type.md §4 reject (reason, `auto_apply_blacklist` for `skill_edit`, move to `rejected/`, archive).
e. On **edit**: ask the user for the change, edit the proposal in place, then loop back to step a for that same id.

### 5. Handle failures

If apply fails (file write error, target missing): leave the proposal in `proposals/`, append `# Apply error\n<error>` to its body, and tell the user. Do not move it.

### 6. Summary

End with one block:

```
adam reflect summary:
  observations processed: <new>
  batches formed: <N>
  diagnoses validated: <N>/<total>
  rolled back (regression): <N>
  verification passed: <N>/<total high_confidence>
  auto-applied: <N>
  approved: <N>
  rejected: <N>
  edited+approved: <N>
  failed: <N>
```

**Keypoint history**: after all proposals are processed, append one JSON line to `~/.claude/adam/keypoint-history.jsonl` with the aggregate keypoint scores from the diagnose stage. This is the longitudinal record of which capabilities improve across `/reflect` runs.

```json
{"ts":"<iso>","session":"<session_id>","keypoints":{"tool_selection":N,"scope_discipline":N,"error_recovery":N,"first_attempt":N,"build_reliability":N},"proposals_emitted":N,"proposals_applied":N}
```

## Things you MUST NOT do

- Do not auto-apply anything not in `high_confidence`.
- Do not apply any proposal before you read apply-by-type.md and enforce its Karpathy constraints.
- Do not invoke other skills during a `/reflect` run.
- Do not modify `settings.json` without explicit user yes.
- Do not hard-delete anything. Use `mv` to `~/.claude/adam/trash/<ts>/`.
- Do not bypass the rubric (`auto_apply_eligible: false` means queue, full stop).
