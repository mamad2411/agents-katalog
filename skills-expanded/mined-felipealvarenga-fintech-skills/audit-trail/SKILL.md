---
name: audit-trail
description: >-
  Use when code changes money, limits, permissions, customer data or configuration in a financial
  product, or when an agent acts on behalf of a user. Covers append-only event records with actor,
  action, before and after, time, reason and request context; corrections as new events; tamper
  evidence; UTC time with per-object sequence; links to idempotency keys and external references;
  dual identity for agents and approvers; retention by regulation; queries and exports for
  auditors; and a test per mutation. Triggers on a new mutation endpoint, an admin or back-office
  action, an approval flow, an automated or AI-driven decision, an auditor or regulator request.
  Not for application debug logs, which have different retention and content.
  Use it also when an auditor asks who changed what and why, or when support asks to see full customer data.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Audit trail

When an auditor, a regulator, a customer or your own incident review asks "who changed this,
when, and why", the answer must come from a record that nobody could edit. An audit trail is
that record. It is separate from debug logs, written by the same transaction as the change,
and complete enough to replay the story without the people who were there.

## When to use

- A new or changed endpoint, job or tool that mutates money, balances, limits, fees, rates,
  permissions, customer data, KYC status or configuration.
- Admin, back-office or support actions, especially reveals of sensitive data.
- Approval flows: payouts, refunds above a threshold, limit changes.
- Actions taken by automations or AI agents on behalf of users.
- A request from an auditor, a regulator or a dispute process.

## Rules

1. **Every mutation writes an event in the same transaction.** `event_id, object_type,
   object_id, sequence, action, actor, before, after, reason, request_id, occurred_at,
   recorded_at, source`. If the event write fails, the mutation fails. No "best effort" audit.
2. **Append only.** No update or delete on the audit table, enforced by database privileges for
   the application role. A wrong event is corrected by a new event that references it.
3. **Actor is who, and as whom.** `actor_type` (user, service, agent, system), `actor_id`,
   and `on_behalf_of` when an agent or support person acts for a customer. Approvals record the
   approver as a separate event from the execution.
4. **Before and after, or the command.** Store the changed fields' previous and new values
   (masked per `pii-and-card-data`), or the full command for creates. The reader must be able
   to see the delta without joining other tables that may have changed since.
5. **Reason is required for human actions.** A reason code from a fixed list plus free text
   or a ticket reference. Support tools do not submit without it.
6. **Time is UTC with a per-object sequence.** `occurred_at` from the business event,
   `recorded_at` from the database clock, and a monotonic `sequence` per object so order is
   never inferred from timestamps. Display timezone is a presentation concern.
7. **Link everything.** The event carries the idempotency key, the external reference
   (processor id, bank reference), the ledger entry id and the request id. From any one of them
   a reader reaches the rest.
8. **Tamper evidence proportional to the risk.** Minimum: separate credentials, append-only
   privileges, backups. Better: a hash chain per object or a daily digest written to a
   write-once store. Best: a replicated, append-only sink outside the application's blast
   radius.
9. **Retention follows regulation, not disk size.** Financial records commonly require five
   or more years; the exact period per jurisdiction and record type comes from compliance.
   Personal data inside events follows the field map's masking so retention does not conflict
   with deletion rights.
10. **Queryable by object, actor and time, exportable in a stable format.** Auditors get a
    documented export (CSV or JSON lines with a schema version). Reports derived from the
    trail: limit changes, payout approvals, sensitive data reveals, agent actions per customer.

## How to apply

1. List the mutations in the change. For each, name the object, the action and the actor types
   that can trigger it.
2. Add the event write inside the service layer method that performs the mutation, in the same
   transaction. Not in the controller, not in a middleware, not after commit.
3. Define the reason codes for human actions and make the UI require one.
4. For agent or automation actions, pass `on_behalf_of` and the policy or run id that
   authorized the action.
5. Write the tests in the **Tests** section: one per mutation.
6. Add the query endpoint or admin view by object and by actor, and the export.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Each mutation endpoint: after a successful call, exactly one event exists with the required
  fields, correct `before` and `after`, and the request id.
- A failed mutation writes no event; a failed event write rolls back the mutation.
- The application role cannot update or delete an event (a test that tries and fails).
- Sequence numbers per object are gapless and ordered for concurrent writers.
- Masking: an event for a CPF change stores masked values.
- Agent action: `actor_type = agent` and `on_behalf_of` set; approver event separate from
  execution event.
- Export: a fixture object produces the documented schema.
- Reference vectors: `skills/audit-trail/evals/vectors/test_audit.py` with `AUDIT_SOLUTION`
  pointing at your module (same-transaction events, sequences, masking, agents, hash chain).

## Review checklist

- Is the event write in the same transaction as the change? Show the code.
- Which role writes the table, and does it have update or delete rights?
- What is the reason code list, and can the UI bypass it?
- How is order determined for two changes in the same second?
- Which values are masked in `before` and `after`?
- How does an auditor get the trail for customer X between two dates?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Audit via application logs | Rotated, unstructured, editable | Dedicated append-only table or sink |
| Event written after commit by a hook | Lost on crash, out of transaction | Same transaction |
| `updated_by` and `updated_at` columns only | History overwritten on the next change | One event per change |
| Timestamps as order | Clock skew reorders events | Per-object sequence |
| Agent actions recorded as the user | Nobody can tell what the agent did | `actor_type = agent`, `on_behalf_of` |
| Free-text reason only | Not queryable, often empty | Reason code plus text |

## References

- SOX and similar internal-control regimes on change management evidence; PCI DSS requirements on audit logs and their protection.
- Event sourcing literature (Fowler, Young) on append-only records and derived state.
