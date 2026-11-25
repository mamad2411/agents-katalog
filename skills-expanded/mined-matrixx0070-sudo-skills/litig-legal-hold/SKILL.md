---
name: litig-legal-hold
version: 1.0.0
description: Issue and manage a litigation hold or preservation notice to prevent spoliation of relevant evidence.
author: matrixx0070
tags: [litigation, legal-hold, preservation, ediscovery, spoliation]
capabilities: []
---

## When to use
Use this the moment litigation is filed or reasonably anticipated — a demand, threat, dispute, or internal escalation can trigger the duty. The deliverable is a preservation notice to custodians plus a plan to suspend auto-deletion and track compliance.

**Not for:** substantive claim assessment (see litig-demand-received) or discovery collection and review, which follow after preservation is secured.

## Method
1. Determine the trigger date and scope: what claims, time period, and subject matter are in play.
2. Identify custodians (people) and data sources (email, chat, drives, phones, backups, third parties).
3. Suspend routine auto-deletion, retention purges, and litigation-relevant device recycling.
4. Draft a clear hold notice: what to preserve, why, and the consequences of deletion.
5. Distribute to custodians and obtain written acknowledgment of receipt and understanding.
6. **Decision point:** if custodians use personal devices or ephemeral/auto-deleting apps, expand the hold and disable disappearing-message settings; if purely corporate systems, coordinate with IT to snapshot.
7. **Decision point:** if a departing employee or a third-party vendor holds relevant data, secure it before access is lost.
8. Track acknowledgments, send periodic reminders, and re-scope as the matter evolves.
9. Release the hold only in writing when the matter and appeal/preservation obligations conclude.
10. Route the hold notice and scope decisions to a supervising attorney for review before distribution.

## Example
> A demand arrives alleging wrongful termination. Same day you issue a hold to HR, the manager, and IT; freeze the mailbox-deletion policy for those custodians; disable auto-purge on the HR system; and collect written acknowledgments. Scope: all communications about the employee from hire through termination plus 90 days.

## Pitfalls
- **Delayed trigger.** Waiting for a filed complaint when the duty arose at the demand risks sanctions for the gap.
- **Under-scoped custodians.** Missing a key player or a shadow data source (texts, personal email) leaves a spoliation hole.
- **No acknowledgment tracking.** A hold nobody confirmed reading is hard to defend; document receipt.
- **Set-and-forget.** Holds must be reissued and re-scoped; single notices go stale as facts and custodians change.

## Output format
```
LITIGATION HOLD NOTICE
TO: <custodians>          DATE: <trigger>
MATTER: <caption / dispute>
PRESERVE: <categories, time range, subject>
SOURCES: <email / chat / drives / devices / backups>
DO NOT: delete, alter, or auto-purge covered data
IT ACTIONS: <suspend retention / snapshot>
ACKNOWLEDGE BY: <date> — reply to confirm
CONTACT: <counsel>
ATTORNEY REVIEW: <pending / cleared>
```

## Reference
The duty to preserve arises when litigation is reasonably anticipated, not only when suit is filed (Zubulake v. UBS Warburg is the seminal line of authority). Under FRCP 37(e), a party that fails to take reasonable steps to preserve ESI faces measures up to adverse-inference instructions or case-dispositive sanctions where there was intent to deprive. Preservation must reach all relevant sources — including text messages, collaboration tools, and ephemeral/auto-deleting apps, which courts increasingly scrutinize. A defensible hold documents scope, distribution, custodian acknowledgment, and periodic reissuance. Coordinate with IT to suspend auto-deletion before it destroys data. This is general information, not legal advice; preservation standards vary by jurisdiction and forum, and a licensed attorney must tailor the hold to the specific matter.
