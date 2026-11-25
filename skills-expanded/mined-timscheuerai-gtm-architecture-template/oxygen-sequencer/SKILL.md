---
name: oxygen-sequencer
description: Operate native OXYGEN Sequences for new conversations and outreach cadence: readiness, drafts, previews and rendered copy, send ceilings, enrollment, do-not-contact policy, monitoring and recovery.
---

# Operate the Sequence

Read [the runtime contract](../../../docs/runtime-contract.md). The kit-specific [enrollment skill](../oxygen-sequencer-enroll/SKILL.md) maps `prepare_sequence` outputs into the native surface; this skill owns Sequence setup and lifecycle.

New LinkedIn conversations belong to Sequences even for one recipient. Multistep email, LinkedIn, WhatsApp, call or CRM-task outreach uses Sequences. Existing-thread replies and direct email without cadence use [Messages](../oxygen-unibox/SKILL.md). A Workflow can enroll leads; the Sequence sends.

## Launch ladder

1. Readiness: `oxygen sequences get <sequence> --readiness --json` lists blockers and changes nothing.
2. Draft: `sequences create` from a steps file, then `sequences update` while draft. A step for a channel the lead cannot be reached on is skipped, so one Sequence can cover leads with and without an email.
3. Preview and render: `oxygen sequences preview <sequence> --json` (who sends each step, scope, capacity, suppressions) and `oxygen sequences render <sequence> --json` (every step and variant for real rows).
4. Ceilings: `--max-live-sends` is the hard ceiling on real sends and CRM writes, required for email, WhatsApp and CRM-task journeys; `--max-credits` is optional.
5. Explicit approval for the external write and the ceilings, then `sequences enroll` and `sequences start --approved`.
6. Monitor with `sequences stats`, `sequences events --kind skipped,sent` and sender health.

## Do not contact

Entries block before every send. Read `suppressions policy show` before the first live start: by default a LinkedIn reply suppresses that person in every future campaign, and bounces, unsubscribes and complaints stay suppressed for compliance.

## Recovery

Every recovery path previews first and applies only to a paused Sequence: reconcile an ambiguous LinkedIn action before resending, retry stale deferrals, recover capacity denials. Enrollment and dispatch are separate actions; a cap is not authorization.
