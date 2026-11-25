---
name: sec-access-review
version: 1.0.0
description: Run a periodic least-privilege access review that finds stale accounts, over-provisioning, and role drift, with owner attestation.
author: matrixx0070
tags: [security, iam, access-review, least-privilege, governance, defensive]
capabilities: []
---

## When to use

Use this on a recurring cadence (quarterly is common), during audits, or after reorgs and offboarding waves. It enforces least privilege and removes access that is no longer justified.

**Not for:** using discovered credentials to access systems; privilege escalation testing; or bulk-revoking without owner sign-off. Review and recommend — revocation follows attestation, not a hunch.

## Method

1. **Gather inventory.** Collect all identities (users, service accounts, API keys) and their granted roles/permissions across systems. Include group and inherited access.
2. **Establish expected access.** For each identity, determine the role its job actually requires. Note owners and last-login/last-used timestamps.
3. **Find stale accounts.** Flag disabled-but-not-removed users, accounts with no activity past a threshold, orphaned service accounts, and unused API keys.
4. **Detect over-provisioning.** Compare granted vs. required permissions. *Decision point:* standing admin or wildcard grants used rarely are candidates for just-in-time access rather than permanent rights.
5. **Detect role drift.** Identify permissions accumulated across role changes that were never revoked, and separation-of-duties conflicts (e.g., the same identity approves and executes payments).
6. **Remediate.** *Decision point:* recommend revoke, downgrade, or convert-to-JIT for each finding — and require owner attestation for any access retained.

## Example

Identity `svc-reporting` holds `db:admin` but its job is read-only exports. Last used for a write: never (90-day window). Justified: no. Recommended action: downgrade to `db:readonly`; if occasional schema tasks arise, grant `db:admin` just-in-time. Owner @data-eng must attest to the downgrade before it is applied.

## Pitfalls

- **Reviewing users but skipping service accounts and API keys.** Non-human identities accumulate the most unnoticed standing privilege.
- **Missing inherited access.** A user may look minimal directly but hold admin via a group; expand group and role inheritance.
- **Revoking without attestation.** Silent removal breaks jobs and erodes trust; require the owner to confirm each retained or removed grant.
- **Treating the report as the outcome.** Findings without tracked remediation recur every quarter; assign owners and due dates.

## Output format

```
## Review scope
Systems: <>. Identities reviewed: <count>.

## Findings
| Identity | System | Current access | Justified? | Last used | Recommended action |
|----------|--------|----------------|------------|-----------|--------------------|

## Remediation list
| Identity | Action (revoke/downgrade/JIT/attest) | Owner | Due |
|----------|--------------------------------------|-------|-----|

## Trends
- <recurring drift or offboarding-process gaps>
```
