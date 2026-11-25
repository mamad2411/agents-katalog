---
name: oxygen-sequencer-enroll
description: Prepare a reviewed, verified cohort for a native OXYGEN Sequence and execute only the user's authorized enrollment and sending scope.
---

# Hand off to a native Sequence

Read [composition](../../../docs/composition.md), [runtime contract](../../../docs/runtime-contract.md) and the `prepare_sequence` definition. Discover the installed CLI's Sequence operations and schemas; older generic create/start examples are not authoritative.

Use [oxygen-sequencer](../oxygen-sequencer/SKILL.md) for native definition, lifecycle and dispatch controls. This skill is the kit-specific adapter from `prepare_sequence` into enrollment.

Inspect the exact Sequence, recipient cohort, sender identity, channel, steps, schedule/time zone, reply stops, suppression and current capacity. Use observed sender health and configured limits. Do not substitute a universal sends-per-day number.

Every row needs independent company/persona gates, current valid email verification, an explicitly reviewed message, clear suppression state and frozen experiment IDs. Run `prepare_sequence` for the selected rows; held rows keep their reasons.

Prepare native enrollment field mappings from real output columns. Render the actual subject/body against one real recipient and inspect unresolved variables and reply routing. Enrollment can itself trigger sending depending on Sequence state: verify that state before writing.

If the user authorized the exact send scope, proceed within it. If only a draft/setup was requested, finish the concrete preview and report the remaining authorization. Avoid duplicate enrollment after ambiguous results; query the recipient/Sequence state first.

Report enrolled/skipped/failed counts, actual Sequence state, limits and recipient scope. Preserve enrollment and experiment IDs for outcome normalization. Creating a Sequence, enrolling and starting delivery are distinct states; report only the one verified.
