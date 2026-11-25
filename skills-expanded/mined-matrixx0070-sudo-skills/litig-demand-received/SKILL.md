---
name: litig-demand-received
version: 1.0.0
description: Handle a demand letter your client received by assessing exposure, deadlines, response strategy, and preservation duties.
author: matrixx0070
tags: [litigation, demand-letter, defense, exposure, preservation]
capabilities: []
---

## When to use
Use this the moment a client forwards a demand, cease-and-desist, or pre-suit notice they received. Your goals are to triage the deadline, size the exposure, trigger preservation duties, and set a response posture before the clock runs.

**Not for:** sending a demand on the client's behalf (see litig-demand-intake and litig-demand-draft).

## Method
1. Docket every deadline in the letter and any statutory response window (some notices demand action in days).
2. Trigger a litigation hold immediately — the demand is reasonable anticipation of litigation (see litig-legal-hold).
3. Assess exposure: is the claim plausible, what damages are realistically at stake, what defenses exist.
4. Check for insurance coverage and any duty to tender notice to a carrier promptly.
5. Identify counterclaims, offsets, or the sender's own weaknesses.
6. **Decision point:** if the claim is strong and cheap to resolve, recommend early settlement outreach; if weak or extortionate, recommend a firm rebuttal or silence per strategy.
7. **Decision point:** if a carrier may cover, tender notice before responding substantively — late notice can forfeit coverage.
8. Preserve, do not destroy — instruct the client to touch nothing referenced in the letter.
9. Route the exposure assessment and any response letter to a supervising attorney for review before sending.

## Example
> Client receives a cease-and-desist alleging trademark infringement, 14-day deadline. You docket the date, issue a hold on all product/marketing files, note possible IP-policy coverage to tender, and flag a fair-use / prior-use defense. Recommendation: tender to carrier, request a short extension, do not admit anything.

## Pitfalls
- **Ignoring the letter.** Silence can waive rights, trigger default timelines, or support a later willfulness finding — respond or decide strategically not to.
- **Spoliation.** Deleting emails or documents after a demand invites sanctions and adverse-inference instructions; preserve first.
- **Late tender.** Many policies require prompt notice; delay can void coverage the client needs.
- **Damaging admissions.** An off-the-cuff client email to the sender can become a party admission — route all communication through counsel.

## Output format
```
MATTER: <sender v. client>
DEADLINES: <letter deadline | statutory window | carrier notice>
CLAIM SUMMARY: <theory alleged>
EXPOSURE: likelihood <low/med/high> | realistic $ <range>
DEFENSES / COUNTERCLAIMS: <list>
INSURANCE: <carrier / tender status>
PRESERVATION: hold issued <Y/N + scope>
RECOMMENDED POSTURE: <settle / rebut / extension / silence>
ATTORNEY REVIEW: <pending / cleared>
```

## Reference
The duty to preserve evidence attaches when litigation is reasonably anticipated — receipt of a demand or C&D generally triggers it; failure can lead to spoliation sanctions under FRCP 37(e) (for ESI) or inherent authority, including adverse-inference instructions. Insurance policies commonly impose prompt-notice and cooperation conditions; late notice can forfeit coverage in many jurisdictions even without prejudice showings (varies by state). Watch for short statutory windows — anti-SLAPP, DMCA counter-notice (10-14 business days), and some administrative-claim deadlines. Nothing in a demand creates liability by itself; assess the merits independently. This is general information, not legal advice, and rules vary by jurisdiction — a licensed attorney must evaluate the specific matter.
