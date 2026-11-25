---
name: oxygen-deliverability
description: Diagnose OXYGEN sender health from bounce, authentication, warmup and run evidence, then apply only the requested bounded remediation.
---

# Investigate sender health

Read [the runtime contract](../../../docs/runtime-contract.md). Discover `oxygen capabilities search "deliverability sender health" --json` and hydrate the selected mailbox, deliverability, Sequence or egress command.

Start with a read-only fleet summary ordered by operational impact: paused/blocked senders, bounce evidence, authentication faults, warmup state, recent volume, provider errors and affected Sequences. Inspect the relevant mailbox and event/run timeline before assigning a cause.

Distinguish sender health from recipient verification. The kit's `enrich_contact_details` and `prepare_sequence` cover contact verification and freshness; they do not certify inbox placement or repair sender authentication.

Use a directional placement test only if it will change a decision. Preview the current scope, price and provider effects before an authorized test. A seed-test result is advisory; it cannot override an authoritative bounce pause or prove production placement.

Recommend the smallest supported action: repair auth/DNS, reduce caps, pause/rotate a sender or observe longer. Apply within the user's authorized remediation scope and current native gates. Never resume a bounce-paused sender simply because one outside test looks healthy.

Return evidence, time window, affected identities, proposed/applied actions and deep-links. Use [email infrastructure](../oxygen-email-infra/SKILL.md) for setup changes and [Sequences](../oxygen-sequencer/SKILL.md) for pacing/binding controls.
