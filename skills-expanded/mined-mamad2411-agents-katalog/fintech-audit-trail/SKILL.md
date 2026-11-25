---
name: fintech-audit-trail
description: Audit-trail specialist. Owns immutable event log, who/what/when capture, tamper evidence, retention, and audit export. Auto-invoked when adding audit logging to a new domain or responding to an audit request.
---

# Fintech Audit Trail

If it's not in the audit trail, it didn't happen; if the trail can be edited,
it's worthless to a regulator. The trail must prove not just *what* happened
but that nothing was altered after the fact.

## When to reach for this

- Adding audit logging to a new domain (postings, compliance decisions, admin actions)
- Designing the event schema, storage, or retention for an audit log
- Preparing an audit export or responding to a regulator/auditor request
- Reviewing whether an existing log would survive a tamper-evidence challenge

## Principles

1. **Append-only enforced at the storage layer.** Object-lock/WORM storage or a
   database trigger that raises on UPDATE/DELETE — application-level discipline
   is not evidence.
2. **Capture context, not just the action.** Actor (human or service), session,
   source IP, request ID, the policy/rule version in force, and before/after
   state. "Status changed to rejected" without *which rule version* is
   unanswerable in an audit.
3. **Hash-chain for tamper evidence.** Each event embeds the previous event's
   hash; periodically anchor the chain head externally (a different account,
   provider, or timestamping service) so an insider can't rewrite and re-chain.
4. **Separate store, separate access.** Different database/bucket and different
   credentials from operational data — the people who can change the system
   must not be able to change its history.
5. **Retention is per event class, with legal hold.** Map each class to its
   regime (US AML/BSA records: 5 years; SEC 17a-4 broker-dealer records:
   6 years on WORM media) and make legal hold override expiry — automated
   deletion during an investigation is itself a finding.
6. **Test the export, not the backup.** Quarterly, actually run: "all events
   for customer X / case Y, with integrity proof, as CSV/JSONL" — and verify
   the chain over the exported range.

## Event schema checklist

Every audit event carries:

- [ ] `event_id` (unique, ordered) and `occurred_at` (UTC, from a trusted clock)
- [ ] `actor` — principal ID + type (user / service / system job), plus session and source IP for humans
- [ ] `action` + `object` — verb, object type, object ID
- [ ] `before` / `after` state (or a diff) for mutations
- [ ] `reason` / `policy_version` — why the system or reviewer did this
- [ ] `request_id` — correlates to application traces
- [ ] `prev_hash` + `hash` — the chain link
- [ ] `retention_class` — drives expiry and legal-hold logic

## Pitfalls

- Audit events written in the same transaction-optional path as the action (action succeeds, audit write silently dropped — write both or neither)
- Logging the action but not the policy/rule version that produced the decision
- Hash chain verified at write time but never re-verified (a chain nobody checks deters nobody)
- PII in audit events with no deletion story — audit immutability vs. erasure requests must be designed, not discovered (pull `common-privacy`)
- Operational admins holding delete rights on the audit store
- Export tested for the first time during the audit

---
*Related: `fintech-compliance` (the decisions being evidenced), `fintech-ledger`
(postings are business records, not a substitute for the trail),
`common-privacy` (erasure vs. immutability) · domain agent: `fintech-architect`
(storage topology) · output/ADR format: `playbook-conventions`*
