---
name: project-adr
description: Use to capture or resume durable design discussions, maintain decision records as implementation changes, or establish project decision maintenance.
---

# Project ADR

Preserve decision topics so another agent can recover the choice, reasons, evaluated alternatives, and open questions without the original conversation.

## Decide whether a record is useful

Follow project creation criteria. Otherwise, record a topic when future maintainers could reasonably reopen it, its reasons cannot be recovered from code or current documentation, or forgetting them could reintroduce a tempting mistake. Apply this test to lasting engineering choices, including architecture, data, security, tooling, and process.

Capture meaningful constraints, real tradeoffs, and substantial unresolved proposals as discussion progresses. Ordinary local fixes, wording, and unevaluated suggestions usually need no record. Maintain affected active records when implementation facts change, even without a new decision. Read-only reviews report gaps; writes and lifecycle actions stay within task authorization.

## Locate rules and records

Read applicable instructions and decision entry points. Resolve creation criteria, location, naming, format, lifecycle, and checks from the current request and project rules, then stable conventions among comparable records. Use defaults only for unresolved aspects.

Search active records by topic, capabilities, constraints, paths, and rejected alternatives. Read matching proposals, choices, rejection reasons, and open questions. Reuse this context while it remains valid; refresh discovery when scope, search terms, evidence, or records change. State changed conditions before reopening a choice. Use archives for historical evidence.

Preserve uncommitted work before editing. Reuse one project convention and topic owner across engineering and discussion workflows; external skills remain unchanged. Prefer directory/search discovery over a new manually maintained central index; follow existing index policy.

Read [project integration](references/PROJECT-INTEGRATION.md) for requested ongoing maintenance, or when the first decision's existing instruction entry point lacks maintenance rules.

## Capture discussion progress

For a design discussion or its resumption, read [discussion capture](references/DISCUSSIONS.md). Preserve meaningful progress before pausing, with selected conclusions, recommendations, open questions, and implementation evidence distinguishable.

## Maintain current facts and decisions

Before adding or updating a record, read [record maintenance](references/RECORDS.md#maintain-a-record) and compare active same-topic records with current implementation and inbound links.

Reuse the topic owner for evolving candidates and selection of a pending choice. For a replaced selected choice, follow project replacement rules; the default creates a linked successor, even if the predecessor was unimplemented. Preserve unique reasons during partial or full replacement. Every new record needs a same-topic review conclusion; extend review beyond affected topics only when requested.

Before archive or deletion, read [the retirement protocol](references/LIFECYCLE.md#archive-or-delete). Keep archived bodies frozen and preserve pending actions when lifecycle work exceeds authorization.

## Write a complete decision

Before drafting, read [record writing](references/RECORDS.md#write-a-record). Preserve valid project templates and existing representations. Without conventions, use one `docs/adr/YYYY-MM-DD-kebab-title.md` per topic, the project's language, and the default four-section format.

When the project lacks a lifecycle convention and uses the default format, read [default states](references/LIFECYCLE.md#default-states) before assigning one. Determine state from selection, implementation evidence, and replacement relationships. A recommendation remains a proposal; acceptance alone grants no execution permission.

## Validate and report

Review every affected active record for required content, accurate state, preserved reasons, replacement direction and scope, and resolvable links. Synchronize implementation facts in the same change as related implementation work.

Run project checks. For the default English or Chinese structure without a matching checker, run [check_adr.py](scripts/check_adr.py) on affected files or the decision directory. Other valid formats use project-specific checks or individual review; preserve their format.

Complete when meaningful progress is persisted, affected records and replacement links are synchronized, authorized lifecycle work is finished, and required checks pass. Report changed records, actual check results, and evidence or integration gaps. Mechanical checks cover structure, state values, and local link paths; review establishes truthful reasons and a usable handoff.
