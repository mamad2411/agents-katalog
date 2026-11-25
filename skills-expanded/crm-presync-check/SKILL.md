---
name: crm-presync-check
description: Check an OXYGEN cohort against the connected CRM and produce existing, new, ambiguous or failed lookup decisions before a sync.
---

# Check the CRM before syncing

Read [the runtime contract](../../../docs/runtime-contract.md) and the actual CRM connection/schema. No CRM adapter or credentials are bundled. Establish company versus person identity with `oxygen-dedupe`.

Inspect the CRM's supported exact identity attributes and query operators. Do not assume one vendor's response path or LinkedIn slug format works elsewhere. Use a bounded read-only lookup, with any applicable provider cost visible.

Keep a decision for each row:
`source_id, identity_key, lookup_status, crm_id, matched_ids, checked_at, reason`.

- One confirmed identity match: `existing`.
- Successful lookup with no match: `new`.
- Multiple or conflicting matches: `ambiguous`.
- Timeout, error, incomplete pagination or unusable key: `failed`.

A null CRM ID does not prove the row is new. Separate an error from a genuine zero-result lookup. Resolve conflicts before proposing writes.

Deliver counts, matches and held rows with destination IDs. This skill prepares a sync plan; an actual CRM write uses the user's separately requested scope, field ownership rules and a re-check for concurrent changes.
