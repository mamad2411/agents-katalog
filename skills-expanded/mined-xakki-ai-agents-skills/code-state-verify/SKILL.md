---
name: code-state-verify
description: 'Validate persisted and in-memory state transitions, schemas, counters and authorization snapshots. Use when untrusted or stored state governs transitions or ownership. RU: проверка состояния.'
license: MIT
disable-model-invocation: true
---

# State and transition validation

Use when untrusted or previously persisted state governs transitions, ownership, leases, counters or public status. Define the actual schema, versions, bounded types, identity and cross-record invariants before implementation or read-only review. Validate at each public construction, read and transition boundary; earlier successful validation does not prove a mutable value remains safe.

Reject malformed or ambiguous state according to the real contract before comparison, arithmetic, dispatch or mutation. Keep typed error, absent state, unknown state and valid empty data distinct. Do not impose exact unknown-field rejection where the contract intentionally supports forward-compatible extensions. For sensitive or mutable authorization across an external exchange, compare the full validated authorization snapshot at the final acceptance boundary, not merely the pathname or object identity.

Use [validation and projection tests](references/validation-and-projection.md) for adversarial fixtures and evidence. Review mode remains read-only; a proposed repair, production action or independent acceptance requires the task's actual authorization.
