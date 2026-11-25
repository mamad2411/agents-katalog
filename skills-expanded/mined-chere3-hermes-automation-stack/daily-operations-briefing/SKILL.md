---
name: daily-operations-briefing
description: Build source-grounded daily executive briefings from autonomous-agent journals, state snapshots, logs, and artifacts, delivered on a durable schedule.
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [automation, cron, daily-brief, operations, audit-trail, reporting]
    related_skills: [hermes-agent, claude-code]
created_by: agent
---

# Daily Operations Briefing

Use this skill when a user wants a recurring daily summary of what an autonomous agent, browser operator, background service, or operational workflow actually did that day.

The goal is not a generic activity digest. It is a compact, source-grounded executive brief that distinguishes actions, observed results, intentional non-actions, and operational health.

## Core Pattern

Separate collection from reasoning:

1. **Identify authoritative sources.** Prefer an append-only session journal for actions and decisions, a generated state snapshot for current metrics, and artifact metadata for cross-checking outbound work.
2. **Build a deterministic collector.** A small script should select only the target timezone's current-day records and print bounded context. Do not make the script write the narrative.
3. **Schedule an LLM-driven cron job.** Inject collector stdout into a self-contained prompt that defines the report format and anti-fabrication rules.
4. **Choose delivery time from the user's routine.** Prefer after the operating window closes when practical, but if the user sleeps before that window ends, deliver shortly before bedtime and explicitly state that the brief covers activity only through the delivery cutoff.
5. **Verify immediately without violating side-effect boundaries.** Run the collector and every dry-run/validation path now. Trigger a full cron run only when its delivery is safe and authorized; for audible, destructive, broadcast, or quiet-hours-sensitive jobs, verify the scheduler's `next_run_at` and let the first authorized window exercise the live side effect.

## Source Hierarchy

Use sources according to what they can prove. Conversation/session continuity is never a source of truth: do not pin the brief to one session ID, name, “latest session,” or assumed long-lived process. Transcript *content* may be useful supplementary evidence when every project transcript matching the target date is discovered dynamically and aggregated. Aggregate every durable record for the target date even when the operator closes one Claude Code/Chrome/Hermes session and opens another. Do not report a session switch as downtime, restart, context loss, or an operational event.

- **Append-only journal:** authoritative for actions, rationale, holds, skips, errors, and per-run decisions across any number of operator sessions.
- **Generated state file:** authoritative for the latest current-state numbers, but not automatically evidence that a cumulative value changed today.
- **Artifact metadata:** cross-check for comments, posts, invitations, deployments, or other outbound objects created today.
- **Service logs:** use only for operational failures, restarts, and gaps not already captured in the journal.
- **Agent transcripts (optional, supplementary):** dynamically discover every root transcript associated with the project and reporting date. Aggregate across sessions without pinning or exposing a session ID. Use transcript text for context, reasoning, decisions, and details, but do not treat a planned, requested, or attempted action as completed unless the journal, state, or artifacts corroborate it. Exclude subagent copies and command-expansion boilerplate when they duplicate the root transcript, and bound excerpts to protect the cron context window.

Never infer an outbound action merely because a file's modification time changed. Metric refreshes and normalization pipelines often touch old artifacts. When transcripts conflict with persistent operational records, the journal/state/artifacts hierarchy wins.

## Collector Requirements

A good collector must:

- Compute the date in the workflow's explicit IANA timezone.
- Extract every journal block whose heading belongs to that date, even if newest-first.
- Include the generated state snapshot with its generation timestamp.
- List today's artifacts using semantic timestamps such as `published_at`, `sent_at`, or `created_at`.
- Print separate clear sentinels when no durable journal records exist and when no matching transcripts exist; neither absence alone proves there was no activity.
- Tolerate missing files and malformed optional artifacts without crashing the whole brief.
- Remain read-only.
- For calendar sources, fetch every calendar in the exact half-open local-day window, paginate fully, exclude cancelled and self-declined events, preserve all-day/timed/tentative semantics, and precompute overlaps plus tight transitions without inventing travel time. See `references/google-calendar-spoken-briefing.md`.
- For personal health sources, read a normalized local snapshot rather than refreshing OAuth inside the collector. Keep API synchronization in a separate silent job shortly before delivery, fetch both today and yesterday to absorb delayed wearable sync, and expose source freshness plus a `day_complete` flag.
- For personal-finance sources, prefer the application's authenticated read-only API or MCP connector over raw database access. Use a dedicated read-only credential, a fixed tool allowlist, bounded date ranges, and a deterministic collector that emits normalized KPI JSON without account identifiers or transaction narratives.
- Treat financial totals as sensitive. Include only material signals—cashflow, savings, net-worth direction, category changes, and budget exceptions—and omit exact balances or merchant details unless the user explicitly wants them spoken.
- Preserve missing-data semantics: `null` means “no data,” never zero. Precompute comparisons only when both periods contain values, and label imported or asynchronously synchronized financial data with source freshness rather than presenting it as real-time.

Prefer Python's `zoneinfo.ZoneInfo` over shell-local date assumptions. Keep the output bounded enough for a scheduled model run.

## Brief Prompt Contract

The scheduled prompt must be self-contained because cron runs in a fresh session. Require:

- The exact reporting timezone and the meaning of “today.”
- Source-of-truth precedence.
- No invented actions, metrics, or causality.
- Consolidation of repetitive ticks and snapshots rather than a long chronology.
- Clear separation of today's deltas from cumulative state.
- Explicit reporting when there were no outbound actions.
- A compact mobile-friendly format with no tables when delivery is through WhatsApp.

### Adaptive editorial structure

Do not default to a fixed template, mandatory sections, a constant order, or prefilled phrases. Decide the structure fresh on every run from that day's evidence:

- Combine related signals when that creates a clearer executive narrative.
- Give a material topic its own emphasis only when warranted; omit empty categories entirely.
- Use headings or bullets only when they improve comprehension for that specific day, not because a template requires them.
- Scale length and detail to the density of material events: a quiet day should produce a short brief; a complex day may need more structure.
- Keep all sources inside one coherent operational brief rather than producing source-by-source mini-briefs.
- Treat channel syntax, speech duration, privacy rules, and required opening phrases as technical constraints—not editorial templates.

Possible content dimensions—not required sections—include outcomes, actions, observed signals, intentional holds, operational health, risks, and grounded next steps.

### WhatsApp formatting for the user

Generate the final brief directly in WhatsApp-native formatting rather than relying on a Markdown conversion layer, while preserving adaptive structure:

- Use one asterisk per side for bold when useful: `*texto*`; never `**texto**`.
- Use `_text_` for optional italics.
- Simple `- ` bullets and blank lines are available when they improve readability, but they are not mandatory and must not become a recurring template.
- Do not use `#` headings, tables, fenced code blocks, horizontal rules, or embedded-link syntax.
- Keep the message mobile-readable and avoid showing implementation paths unless an operational error requires them.
- When setup or integration work is performed through WhatsApp, keep intermediate progress non-actionable; place all instructions the user must follow, copy, open, or decide in the final response so they are not buried mid-process.

## Hermes Cron Setup

For reasoning-based summaries, use an agent cron job with a pre-run collector script rather than `no_agent=True`.

Important setup rules:

- Place scripts under `~/.hermes/scripts/`.
- Pass the cron `script` field as a path **relative to that directory** (for example, `daily_context.py`), not an absolute path.
- Set `workdir` to the operation's project root so its context file is available.
- Use `deliver='origin'` unless the user explicitly requests another destination.
- When the user changes a brief to device-only delivery, pause the separate written-delivery job rather than rerouting it. Keep silent collectors, device preflights, delivery-receipt watchdogs, and true failure alerts active unless the user also opts out of alerts; alerts are not duplicate briefs.
- Use `attach_to_session=True` when the user is likely to reply to the daily brief.
- Restrict toolsets to what the scheduled run needs, commonly `file` and `terminal`.
- Choose the schedule in the operation's timezone and align it with the user's actual routine. If delivery must occur before the operation ends, encode and disclose the cutoff instead of implying a complete day.

## Verification Checklist

Before reporting success:

1. Run the collector manually and inspect its date, journal extraction, state timestamp, and artifact list.
2. Test semantic timestamp fields on at least one known artifact type; invitations may use `sent_at` while comments use `published_at`.
3. Create the cron job and verify its returned `next_run_at` has the expected UTC offset.
4. Trigger a manual cron run only if the live delivery is non-disruptive and authorized at the current time. For audible or quiet-hours-sensitive delivery, run the collector and renderer in dry-run mode instead.
5. For an immediate live run, confirm `last_status: ok`, `execution_success: true`, and no delivery error. If the brief invokes a nested side-effect helper (speaker, sender, publisher), also inspect that helper's exit code and durable ledger/receipt; outer agent success can coexist with nested delivery failure. For a deferred live run, confirm the job is enabled, its next run is correct, and the side-effect helper has passed dry-run validation.
6. Tell the user the schedule, timezone, sources, delivery destination, host/network availability dependency, and how to request a timing change.

## Pitfalls

- **Summarizing cumulative metrics as today's gains:** label cumulative state explicitly; only journaled or timestamped deltas belong under today's results.
- **Using file mtime as proof:** data-refresh pipelines touch historical files.
- **Chronology dump:** consolidate repeated no-op ticks and snapshots into decisions and net outcomes.
- **Fixed-template drift:** recommended content dimensions can silently become mandatory headings and a constant order. Re-evaluate structure from the day's evidence every run; omit empty categories and keep all sources in one coherent brief.
- **Source-silo brief:** integrating a new source such as health data does not justify a permanent new section or mini-brief. Blend it into the operational narrative unless its materiality that day warrants distinct emphasis.
- **No-activity ambiguity:** distinguish “no sessions were recorded” from “sessions ran but intentionally held all outbound actions.”
- **Cron script path rejection:** Hermes resolves cron scripts under `~/.hermes/scripts/`; use only the relative filename/path in the job.
- **Premature brief time:** a pre-close brief omits later actions. Prefer post-close delivery, but when the user's bedtime comes first, deliver before bedtime and label the coverage cutoff clearly.
- **Document-style Markdown on WhatsApp:** write native WhatsApp formatting directly (single asterisks, simple bullets, no headings/tables) rather than assuming conversion will match the user's preference.
- **Unverified delivery:** a created job is not enough; run it once and inspect execution and delivery status.
- **Nested side-effect hidden by outer success:** an LLM cron can return a normal final response after its speaker/sender command failed, leaving the cron itself marked `ok`. Require a machine-readable receipt or durable per-run ledger from the side-effect helper and alert from that evidence; do not equate narrative completion, renderer dry-run success, or outer cron status with delivery.
- **Authorized health scope treated as available data:** OAuth consent proves read permission, not that a wearable supplied records for the day. Keep missing values as `null`, label incomplete-day totals as partial, and never turn absence into zero, diagnosis, or medical advice.

## Supporting Material

- See `references/linkedin-claude-browser.md` for a concrete autonomous social-operations example using Claude Code, browser automation, an append-only session journal, generated state, and artifact cross-checks.
- See `references/alexa-spoken-delivery.md` for targeted Echo playback, privacy filtering, fresh morning source windows, audit files, dry-run/live safety, and device-specific scheduling guardrails.
- See `references/google-health-fitbit-briefing.md` for OAuth-safe synchronization, normalized SQLite snapshots, missing-data semantics, wearable-delay handling, and written/spoken health briefing verification.
- See `references/comprehensive-wearable-coaching.md` for full Google Health/Fitbit stream discovery, endpoint selection, non-finite-value handling, observation-counted personal baselines, and actionable non-clinical coaching beyond steps and distance.
- See `references/financial-kpi-briefing.md` for read-only MCP access, financial KPI normalization, privacy-aware spoken selection, and end-to-end verification.
- See `references/google-calendar-spoken-briefing.md` for least-privilege Calendar OAuth, deterministic multi-calendar collection, spoken privacy, schedule-issue detection, and dry-run verification.
- For Alexa authentication, exact-device API calls, appliance discovery, power/state control, and private-API payloads, load the class-level `alexa-smart-home-automation` skill.
