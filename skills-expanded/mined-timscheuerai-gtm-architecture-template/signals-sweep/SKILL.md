---
name: signals-sweep
description: Collect a bounded batch of hiring, engagement or other account signals with source dates, deduplication and explicit qualification rules.
---

# Collect useful signals

Read the active ICP, exclusions and [runtime contract](../../../docs/runtime-contract.md). Define the business event, why it could matter, date window, source, buyer hypothesis and maximum batch size.

Inspect the provider's current filter semantics: HQ geography differs from job or person geography; event time differs from indexing time. Use the timestamp the hypothesis actually needs. Unknown dates remain unknown rather than becoming fresh.

Keep stable event ID, company identity, source URL, event type, occurred/observed/indexed dates where available, query term and collection batch. Convert a known timestamp to Unix milliseconds only at the function boundary. Do not silently invent the missing event date.

Preview scope and current cost; count-only calls can also be billable. Follow pagination and persist resumable state in OXYGEN. Deduplicate on provider/event ID and preserve multiple genuine signals per company.

Run independent fit checks before contact enrichment. Exclusions come from the current company brief; substring matches are review hints, not definitive identity matches. Use `prioritise_accounts` and `prioritise_contacts` with an explicit evaluation time and signal lifetime.

Report fresh/duplicate/unknown/held counts and incomplete pages. Engagement does not establish buyer intent. For comment-to-resource requests, deliver only the requested resource through the authorized channel; use `oxygen-sequencer-enroll` for a separately authorized outreach motion.
