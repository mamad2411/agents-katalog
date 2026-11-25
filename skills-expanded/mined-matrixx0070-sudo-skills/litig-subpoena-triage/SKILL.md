---
name: litig-subpoena-triage
version: 1.0.0
description: Triage a subpoena your client received — check validity, scope, and deadlines, then plan objections, meet-and-confer, and compliance versus a motion to quash.
author: matrixx0070
tags: [litigation, subpoena, discovery, objections, motion-to-quash]
capabilities: []
---

## When to use
Use this the moment a client hands you a subpoena and asks what to do. It walks you through confirming the subpoena is valid, measuring its scope, calendaring the response deadline, and deciding whether to object, negotiate, comply, or move to quash. Applies to document, testimony, and deposition subpoenas.

**Not for:** preparing the resulting deposition (see litig-deposition-prep) or logging withheld documents (see litig-privilege-log-review).

## Method
1. Verify validity: issuing court, correct caption, proper service, and whether it issued from a court with authority over your client.
2. Calendar every deadline immediately, including the objection window, working backward from the compliance date.
3. Assess scope and burden: relevance, proportionality, geographic limits, and whether it demands privileged or trade-secret material.
4. **Decision point:** If the request is overbroad or unduly burdensome but curable, serve written objections and open a meet-and-confer; if it is facially defective or seeks privileged/protected material, prepare a motion to quash or for a protective order.
5. **Decision point:** If your client is a non-party, invoke the FRCP 45 protections against undue burden and cost-shifting; if a party, coordinate with the case's discovery obligations.
6. Preserve responsive material at once to avoid spoliation, even while objecting.
7. ATTORNEY-ESCALATION gate: Route objections, the meet-and-confer position, and any motion to a supervising attorney for review before serving or filing.

## Example
> A client receives a document subpoena from a distant federal court demanding five years of records in 10 days. You calendar the 14-day objection window, note the 100-mile limit and the short compliance date, and prepare timely written objections plus a meet-and-confer letter, routing both to the supervising attorney before service.

## Pitfalls
- **Missing the objection window:** Under FRCP 45 the objection deadline is often the earlier of 14 days after service or the compliance date; blowing it can waive objections.
- **Ignoring the geographic limit:** The 100-mile rule constrains where compliance can be commanded.
- **Spoliation while objecting:** Objecting does not suspend your preservation duty.
- **Overlooking privilege/trade-secret:** These require an express claim, not silent withholding.

## Output format
```
SUBPOENA TRIAGE
Issuing court / caption / service: [valid? notes]
Deadlines: objection [date] | compliance [date]
Scope/burden: [relevance | proportionality | 100-mile | privilege]
Recommendation: [comply | object + meet-confer | move to quash / protective order]
Preservation: [hold issued? date]
Attorney review: [name | date | status]
```

## Reference
FRCP 45 governs federal subpoenas. Objections to document subpoenas must be served before the earlier of the compliance time or 14 days after service (45(d)(2)(B)); a court must quash or modify a subpoena that fails to allow reasonable time, requires travel beyond the 100-mile limit (45(c)/45(d)(3)(A)), requires disclosure of privileged material, or subjects a person to undue burden. The issuing party must take reasonable steps to avoid imposing undue burden or expense on a non-party (45(d)(1)). A non-party can seek cost-shifting for significant compliance expense. State subpoena rules, deadlines, and mileage limits vary; verify the governing jurisdiction and any interstate-deposition act. General information, not legal advice.
