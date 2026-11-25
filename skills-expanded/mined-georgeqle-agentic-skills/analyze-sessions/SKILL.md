---
name: analyze-sessions
description: Analyze Claude Code and Codex session history for cross-session trends, recurring patterns, and automation opportunities
type: analysis
version: v0.7
required_conventions: [alignment-page]
argument-hint: "[history file, session directory, repo path, date range, or trend question]"
context_intake: artifact_only
visual_tier: visual
---

# Analyze Sessions

Invoke as `$analyze-sessions`.

Use this skill to answer questions against your local Claude Code and Codex history — both broad cross-session trends AND one-off lookups. That spans broad trend analysis, repeated prompt patterns, recurring frustrations, workflow evolution, automation opportunities, and skill performance over multiple sessions, as well as single informational questions such as finding a past conversation, explaining why a skill recommended a particular path, or checking one run's token spend.

Route to `$session-triage` only when the user needs a *verified fix for a live incident*: a correction to act on, a failed run to repair, a repo incident, or a suspected skill failure. Pure informational history questions stay here even when they are about one session.

## Inputs

- Default Claude history file: `~/.claude/history.jsonl`
- Default Codex prompt history file: `~/.codex/history.jsonl`
- Default Codex rich session root: `~/.codex/sessions/**/*.jsonl`
- Optional paths from the user. Accept history files, session directories, repository directories, or exported logs.
- Optional filters such as repo path, project name, date range, command/skill name, exact phrase, or trend question.
- Optional model pricing table or explicit request to verify current provider pricing. Use pricing only when it is supplied by the user, present in the logs, or verified from an authoritative provider source during the run.
- Persistent insights store (machine-local, gitignored): `.session-insights/insights.md` (accumulated findings) and `.session-insights/watermark.json` (last-processed timestamp per history source). These let the skill accumulate across runs instead of recomputing from raw history every time.

## Persistent Insights Memory

This skill maintains an accumulating memory so cross-session findings compound, mirroring the read-at-start discipline of `tasks/lessons.md` and the keyed Terms-table shape of the shared glossary. The store is **machine-local and gitignored** — it derives from this developer's private `~/.claude` / `~/.codex` history, so committing it would be noisy and a privacy leak.

- `.session-insights/insights.md`: a keyed table `| Insight | Category | First Seen | Last Seen | Occurrences | Status |`, plus a `## Recently Added` audit table for the most recent run's new/updated rows. Insights are deduped by semantic match (same discipline `tasks/lessons.md` uses), not exact string match.
- `.session-insights/watermark.json`: last-processed timestamp per history source — `~/.claude/history.jsonl`, `~/.codex/history.jsonl`, and `~/.codex/sessions/**`.

**Recall step (run first, before parsing history):**
- Read `.session-insights/insights.md` and `.session-insights/watermark.json` if they exist. Treat the recalled insights as established context for this run. If neither exists yet, this is a cold start — process the full history (per the existing "read the full available history" rule) and create the store at the write step.
- When the store exists, parse only history records *newer than* the per-source watermark, then layer the newly parsed activity on top of the recalled insights. Do not re-derive the recalled findings from scratch.
- For an explicit full-history request, or when the user passes a custom scope/date range that predates the watermark, ignore the watermark for that run (read the full requested scope) but still merge results into the store at the end.

**Write step (run last, after reporting):**
- Merge this run's findings into `.session-insights/insights.md`: for each finding that semantically matches an existing row, increment `Occurrences` and advance `Last Seen`; for genuinely new findings, append a row with `First Seen` = `Last Seen` = this run's date, `Occurrences` = the count observed, and `Status` = `proposed` (promote to `confirmed` once corroborated across runs or by `$session-triage`).
- Record the new/updated rows in the `## Recently Added` audit table.
- Advance `.session-insights/watermark.json` to the newest timestamp processed per source. Create the store (with the standard header) if it did not exist.
- Never commit `.session-insights/` — it is gitignored. If `git status` shows it tracked, stop and report instead of committing.

## Process

1. Confirm the request is an informational history question for this skill:
   - Continue for overall history, usage breakdowns, repeated prompts, recurring workflow issues, cross-tool changes, automation opportunities, or performance trends across multiple sessions — and for single informational lookups such as finding a past conversation, explaining why a skill recommended a path, or checking one run's token spend. Scale the read to the question.
   - Route to `$session-triage` only when the user needs a verified fix for a live incident: a correction to act on, a failed run to repair, a repo incident, or a suspected skill failure.
   - When a request contains both a live incident and recurrence questions, recommend `$session-triage` first for the incident and use this skill afterward for frequency or trend evidence.

2. Run the Recall step from Persistent Insights Memory first, then read history for the selected scope: the full available history on a cold start (no store) or an explicit full-history request, or only records newer than the per-source watermark when the insights store exists. Read the full selected scope, not a sample.

3. Use a scriptable approach for scale. Prefer streaming or line-by-line processing for large files.

4. Normalize records into one common shape:
   - `source`: `claude` or `codex`
   - `timestamp`
   - `session_id`
   - `project` or `cwd`
   - `text`
   - optional token usage such as input, cached input, output, reasoning output, and total tokens
   - optional cost metadata such as estimated USD cost, billed credits, pricing source, and price-table version
   - optional metadata such as git branch, repository URL, model, provider, and CLI version

5. Parse Claude history:
   - `~/.claude/history.jsonl` lines contain user messages with fields such as `display`, `timestamp` in milliseconds, `project`, `sessionId`, and `pastedContents`.

6. Parse Codex history:
   - `~/.codex/history.jsonl` lines contain compact user prompts with `text`, `ts` in seconds, and `session_id`.
   - `~/.codex/sessions/**/*.jsonl` lines contain richer rollout records. Use `session_meta.payload.id` to map session IDs to `cwd`, git metadata, CLI version, and model/provider.
   - Include user `response_item` records only when they represent user messages. Exclude developer/system/base instruction payloads from prompt-pattern counts.
   - Prefer compact Codex prompt history for user prompt counts, enriched with rollout metadata. Use rollout user records only for prompts missing from compact history or for metadata checks.
   - Parse Codex `event_msg` records with `payload.type == "token_count"`. Normalize `payload.info.total_token_usage` and `payload.info.last_token_usage` fields such as `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, and `total_tokens`.

7. Parse token spend and cost metadata:
   - For session-level token totals, use the final or highest cumulative `total_token_usage` snapshot per session instead of summing every cumulative snapshot.
   - For date or turn-level trends, sum deduplicated `last_token_usage` records and reconcile them against each session's final cumulative total when possible.
   - Attribute token usage by source, session, project, model, provider, and date when those fields are available; otherwise report the missing dimensions explicitly.
   - Use direct cost fields when logs include them, such as `cost`, `total_cost`, `totalCost`, `estimated_cost_usd`, or `estimatedCostUsd`, preserving their original source and units.
   - When costs are not logged, estimate USD cost only from a user-provided or freshly verified provider pricing table. Show the pricing source, retrieval date or table version, model mapping, formula, and assumptions.
   - Treat cached-input and reasoning-output tokens according to the pricing table. If the table is ambiguous, state the assumption, such as reasoning tokens billed as output tokens, and keep the estimate labeled as an estimate.
   - If no reliable cost basis is available, still report token totals and say cost is unavailable instead of guessing.

8. Extract and report:
   - Project breakdown: top projects by message volume with percentages.
   - Source breakdown: Claude vs. Codex message/session counts and date ranges.
   - Token spend breakdown: total tokens plus input, cached input, output, and reasoning output by source, project, model, and date where supported.
   - Cost breakdown: total estimated cost, cost by source/project/model/date, and top cost-driving sessions when supported by explicit cost fields or a verified/provided price table.
   - Activity categories and recurring workflow themes.
   - Exact and fuzzy repeated prompt patterns.
   - Common multi-step workflow sequences.
   - Cross-tool differences, including workflows that moved from Claude to Codex or still require different commands.
   - Skill performance patterns across multiple invocations, including recurring corrections or repeated bad recommendations when supported by scoped history evidence.

9. For each major pattern, recommend the best automation shape:
   - Skill: repeatable workflow with a stable sequence.
   - Agent: complex exploratory or autonomous work.
   - Plugin/integration: external-service or persistent-connection workflow.
   - Standing instruction/project convention: behavior that should always apply.
   - `$session-triage`: one concrete incident needs verification before a durable fix is designed.

10. Run the Write step from Persistent Insights Memory last: merge this run's findings into `.session-insights/insights.md` (dedup/increment Occurrences, advance Last Seen, append new rows), update the `## Recently Added` table, and advance the watermark. Do not commit the gitignored store.

## Comparison Mode

A recurring question shape is a **model/config A-B comparison**: compare two model or config regimes across sessions on cost and output quality — for example "Opus 4.6 vs 4.7 token usage and quality", "gpt 5.5 low vs xhigh reasoning effort", or "Claude vs Codex UI quality". When the request fits this shape:

- Identify the two regimes from the user's question (model, provider, reasoning effort, tool, or config) and the sessions that belong to each, stating how you attributed each session when the field is sparse.
- Compare on token/cost per the cost section above and on observable quality signals from the history — correction rate, retries, follow-up prompts, abandonment, or explicit user praise/complaints — not on assumed model capability.
- Report the comparison as a side-by-side: regime A vs regime B on tokens, estimated cost (or `cost unavailable`), and the quality signals, with sample sizes and the date range each regime covers.
- Label quality signals as observed evidence vs inference, and call out when one regime has too few sessions to compare fairly.

## Output

Produce a structured report with:

- Overview stats: total messages, sessions, date range, and top projects.
- Source comparison: Claude vs. Codex totals, top projects, command usage, and recent trend.
- Token and cost check: total tokens, token class breakdown, total estimated cost or explicit `cost unavailable`, pricing source/assumptions, and coverage gaps for sources without usage metadata.
- Categorized patterns with counts and real examples from history.
- Skill performance trends when requested or visible in the scoped data.
- Ranked recommendations table: pattern, frequency, recommendation type, suggested name/description.
- Highest-impact section: top 5 automations by avoided manual prompts.
- Recommended next skill: `$session-triage` for any concrete incident that needs verification, `$targeted-skill-builder` (skill-dev pack) `<concrete gap phrase>` for a broad verified workflow gap, or `none` when no follow-up is justified. When recommending `$targeted-skill-builder` (skill-dev pack), include the likely owner surface and validation expectation in the report.

## Constraints

- Process the entire available history for broad usage analysis on a cold start or full-history request; when the persistent insights store exists, process every record newer than the watermark layered on the recalled insights, never a sample of that window.
- Treat `.session-insights/` as machine-local and gitignored. Never commit it; if `git status` shows it tracked, stop and report.
- Use actual message examples from the history, not hypothetical ones.
- Be specific about frequencies; show exact counts where possible.
- Show exact token counts where available and clearly distinguish logged costs from estimated costs.
- Do not infer token counts from message length when usage metadata is missing.
- Do not estimate dollar cost from remembered or stale model pricing. Use explicit log cost fields, a user-provided price table, or a current provider source verified during the run; otherwise report cost as unavailable.
- Avoid double-counting cumulative token snapshots. For Codex `token_count` events, aggregate final session totals from `total_token_usage` and use `last_token_usage` only for deduplicated timeline or turn-level analysis.
- Group near-identical prompts together.
- Deduplicate Codex prompts that appear in both `~/.codex/history.jsonl` and rollout files by `(session_id, timestamp, normalized text)` where possible.
- Do not include system, developer, base instruction, or tool output text in repeated-prompt counts.
- Answer informational history questions here, single or trend; do not work up a verified fix for a live incident — route that to `$session-triage`.
- Do not create or modify GitHub Actions workflows.
- If one source is missing or unreadable, report that clearly and continue with the other source instead of guessing.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, prepend `npx skillpacks install <pack-name>` to the recommendation.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/analyze-sessions-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
