---
name: oxygen-sequencer
description: Operate native OXYGEN Sequences for new conversations and outreach cadence, including sender readiness, previews, enrollment, dispatch and recovery.
---

# Operate the Sequence

Read [the runtime contract](../../../docs/runtime-contract.md). The kit-specific [enrollment skill](../oxygen-sequencer-enroll/SKILL.md) maps `prepare_sequence` outputs into the native surface; this skill owns Sequence setup and lifecycle.

New LinkedIn conversations belong to Sequences even for one recipient. Cadenced or multi-recipient outreach uses Sequences. Existing-thread replies and direct email without cadence use [Messages](../oxygen-unibox/SKILL.md).

Discover exact commands with `oxygen capabilities search "preview outreach sequence" --json`, then `commands get` for the selected operation.

Inspect these together:
- Sender profiles, exact accounts/mailboxes, health, channel limits and stable recipient-to-sender binding.
- Definition/version, ordered steps, delays, variants, send windows/time zone and any channel fallback.
- Recipient identity, mapped variables, exclusions, suppression, prior-contact rules and tags.
- Dispatch limits, lifetime budget, live-run cap, reply stops and bounce behavior.

Preview the actual recipient scope and render messages with their real variables. Report unresolved identities individually. A connected mailbox is not proof of readiness. Use [email infrastructure](../oxygen-email-infra/SKILL.md) for sender setup and [deliverability](../oxygen-deliverability/SKILL.md) for health issues.

Enrollment and dispatch are separate actions. Inspect the selected Sequence's current state: draft or paused enrollments may remain pending, while an active Sequence may deliver after enrollment. Execute only the user's authorized send scope and current platform gates; a cap is not authorization.

Record enrollment, variant and run IDs. For results, inspect campaign events/analytics and preserve actual mailbox/domain attribution; missing identity stays unattributed. Normalize events into `analyse_results` without claiming that the kit automatically wires telemetry.

For recovery, preview the narrow failed/deferred scope and reconcile provider outcomes before retrying. Pause/resume, retirement and capacity recovery have distinct semantics; discover them before acting. Return counts, held reasons, actual state, budget and deep-links.
