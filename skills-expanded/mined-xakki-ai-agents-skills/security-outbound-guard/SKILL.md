---
name: security-outbound-guard
description: 'Bound external attempts and validate outbound work across retries and background paths. Use when a canary, job, retry loop or sender must obey an explicit external-attempt or emergency-stop policy. RU: внешние запросы, аварийная остановка.'
license: MIT
disable-model-invocation: true
---

# External attempt controls

Use when a canary, job, retry loop, timer or outbound sender must obey an explicit external-attempt or emergency-stop policy. Trace configuration through the actual runner and every independent retry, manual and background entrypoint. Distinguish selected items from physical external attempts and specify unset, zero, invalid and valid limits according to the product contract.

Validate outbound event identity, type, required fields and bounds at the consumer before transport configuration, request rendering or dispatch; do not assume only a trusted producer can invoke it. A disabled or invalid path must produce the documented safe result without acquiring unrelated locks, changing cadence or sending traffic. A shared resource needs the same verified single-flight boundary for all paths that may conflict.

Check and account for each actual dispatch immediately before it occurs, including retries and fallback. A counted attempt does not prove the target received or did not receive it. An ambiguous timeout requires an explicit supported reconciliation or delivery-evidence protocol before retrying where duplicates are harmful. Test invalid policy, valid operation, lock failure, retries, parallel calls and forbidden effects using synthetic fakes; a local test does not authorize or prove a live canary.

If the safety claim depends on proving that dispatch never occurred, qualify an authoritative lifetime record across all dispatchers and versions. A missing attempt row or response alone is not that proof: a crash can occur after dispatch was permitted but before a row was recorded. Where a durable pre-dispatch intent is used, serialize it with terminal-state fencing and fail closed on an uncertain write; historical or mixed-version records remain unknown until qualified.

For durable sender outcomes and retries, read [delivery outcomes](references/delivery-outcomes.md).
