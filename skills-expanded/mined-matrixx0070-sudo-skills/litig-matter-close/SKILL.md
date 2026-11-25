---
name: litig-matter-close
version: 1.0.0
description: Close out a concluded litigation matter — final disposition, file retention, client wrap-up, and litigation-hold release.
author: matrixx0070
tags: [litigation, closeout, retention, litigation-hold, case-management]
capabilities: []
---

## When to use
Use this when a matter has reached final disposition — judgment, dismissal, settlement, or withdrawal — and you need to wind it down cleanly. Use it to confirm nothing is left undone before the file goes to storage. A disciplined close protects the client and the firm long after the matter ends.

**Not for:** interim status logging (see litig-matter-update) or pausing an active matter.

## Method
1. Record the final disposition: judgment, settlement terms, dismissal (with or without prejudice), or withdrawal, with dates.
2. Confirm all post-disposition obligations are satisfied. **Decision point:** if an appeal window is still open, do NOT close — set a tickler for the deadline and keep the matter active.
3. Verify settlement performance: payments made, releases exchanged, dismissals filed.
4. Reconcile billing and issue the final invoice; return unearned retainer funds.
5. Send the client closing letter confirming the outcome and the end of representation. ATTORNEY-ESCALATION gate: route the closing letter to the supervising attorney for review and signature before it is sent.
6. Release the litigation hold once no preservation duty remains. **Decision point:** if related or anticipated litigation exists, keep the hold in place and document why.
7. Set the retention/destruction date and move the file to archive.

## Example
> A breach case settles; the client is paid and a stipulation of dismissal with prejudice is filed. You confirm no appeal applies, reconcile billing and refund the retainer balance, route the closing letter for signature, release the hold after confirming no related claims, and set a seven-year retention date.

## Pitfalls
- **Premature close:** an open appeal or unpaid settlement means the matter is not concluded.
- **Early hold release:** releasing preservation while related litigation is foreseeable risks spoliation sanctions.
- **Forgotten trust funds:** unearned retainer must be returned, not swept.
- **No end-of-representation notice:** without a closing letter the duty to the client may be treated as ongoing.

## Output format
```
MATTER: <name> | No: <matter#>
DISPOSITION: <type — date; terms>
POST-DISPOSITION OBLIGATIONS: <satisfied? / appeal window>
BILLING: <final invoice; retainer returned>
CLOSING LETTER: <sent / pending attorney signature>
LITIGATION HOLD: <released / retained — reason>
RETENTION: <archive date; destroy-by date>
```

## Reference
A hold cannot be released while litigation is pending or reasonably anticipated; the duty to preserve is ongoing and spoliation may trigger FRCP 37(e) sanctions for lost ESI. Appeal windows are jurisdictional: FRAP 4 generally gives 30 days from entry of judgment (60 when the United States is a party); state deadlines vary. Dismissal "with prejudice" bars refiling; "without prejudice" does not. File-retention periods are set by jurisdiction, ethics rules, and engagement terms — commonly 5–10 years, longer for minors, wills, or matters with continuing obligations. Unearned fees held in trust must be returned (ABA Model Rule 1.15). Confirm all deadlines and retention rules with the supervising attorney.
