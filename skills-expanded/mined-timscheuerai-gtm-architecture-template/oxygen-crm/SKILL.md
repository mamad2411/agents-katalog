---
name: oxygen-crm
description: Work with OXYGEN Records, the canonical CRM: objects, fields and identities, notes and tasks, HubSpot or Attio imports and syncs with do-not-contact first, and binding and promoting Table rows into records.
---

# Keep canonical records

Read [the runtime contract](../../../docs/runtime-contract.md). Records hold canonical truth: companies, people, deals and custom objects, with identities, relationships, activities, notes, tasks and files. Tables hold working rows; a row becomes a record only at a deliberate bind-and-promote gate.

| Need | Start with |
|---|---|
| See the model | `oxygen crm objects --projection compact --json`, `oxygen crm describe <object> --json` |
| Find or open a record | `oxygen crm search "<fragment>" --suggest --json`, `crm get <object> <id>` |
| One HubSpot list or Pipedrive filter as a working table | `tables hubspot import`, `tables pipedrive import` (do-not-contact syncs first) |
| A whole CRM object into Records | `crm sync import <provider> --object <object>` |
| HubSpot or Attio kept in sync | `crm sync configure`, then `crm sync run --dry-run`, then `crm sync enable` |
| Table rows as native contacts | a bind column, then `tables promote` |

## Gates

- Check the connection first (`oxygen integrations list --json`); a broken connection stops the work.
- Every import, sync, object change and promotion previews or dry-runs first; the live call needs `--approved` and a spend ceiling.
- Do-not-contact syncs first and is additive; skipping it is an explicit choice.
- Imports are last-write-wins on the fields the CRM supplies; edits in the CRM do not flow back on their own.
- New workspaces start with sample records marked `_sample: true`; never count or work them.
- Binding and promoting are truth writes; identity fields are never overwritten from a table.

Writing a score, tier and why-now line to the CRM is its own approved step; confirm which portal it writes to before the first write.
