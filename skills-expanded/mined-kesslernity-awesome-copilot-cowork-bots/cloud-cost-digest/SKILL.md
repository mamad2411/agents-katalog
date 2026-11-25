---
name: cloud-cost-digest
description: Turns cloud billing exports and provider alert emails into a short digest of what moved, what is anomalous and what to ask an owner about. Use when the user asks about cloud spend, what changed on the bill, why costs went up, to prepare a FinOps review, or to explain a cost spike.
---

# Cloud Cost Digest

Explains what moved on the bill, with the question to ask each owner.

## Inputs
- A billing export the user supplies, through **Excel**
- Provider alert and budget emails, through **Email**
- `references/config.md` for the materiality floor, owner mapping and the comparison period

## Procedure
1. **Load the export.** Without it, say so and stop. Alert emails alone cannot produce a digest;
   they can produce an alert summary, which is a different and lesser thing.
2. **Compare** the current period against the comparison period in config, by service and by the
   tag or account that config names as the ownership dimension.
3. **Surface only movement above the materiality floor**, in absolute and percentage terms both.
   A 400% rise on 12 units of currency is noise and must not lead the digest.
4. **For each movement, state** the service, the owner from the mapping, the absolute change, the
   percentage, and whether anything in the mailbox explains it: a deployment notice, a budget
   alert, a migration thread.
5. **Separate facts from inference explicitly.** "Spend rose 38%" is a fact from the export.
   "Likely the new environment stood up on the 14th" is an inference and must be labelled.
6. **Write** the digest and attach the per-service table.

## Output
Digest, in this order: total for the period against comparison; the three largest movements with
owner and probable cause; anomalies with no explanation found; then the full table.

| Service | Owner | This period | Comparison | Change | Change % | Explanation | Evidence |

## Definition of done
Every movement above the floor appears, every one names an owner or says OWNER UNKNOWN, and every
explanation is labelled fact or inference.

**A flat month is a result.** Say "no movement above the floor" and stop.

## When there is no data
- No export: stop, say what is needed.
- Tags missing so ownership cannot be derived: produce the digest with OWNER UNKNOWN and say how
  many rows that affects. Do not guess an owner from a service name.
- Comparison period incomplete: state the actual dates compared.

## Boundaries
- Never state a forecast as a commitment.
- Never recommend terminating, resizing or deleting a resource. Surface the movement and the
  question; the owner decides.
- The provider's own billing console is the source of truth. This reads an export.
- Never share account identifiers outside the organization.
- **Read only, and draft only.** This skill reads an export and writes a digest for the user. It
  never opens a ticket, never emails an owner, and never changes a budget or an alert. Sending
  the digest to anyone is the user's action, behind the normal approval prompt.

## Self-check
- Is every percentage paired with an absolute, so small numbers cannot lead?
- Is every explanation labelled fact or inference?
- Did I avoid recommending any change to a resource?
