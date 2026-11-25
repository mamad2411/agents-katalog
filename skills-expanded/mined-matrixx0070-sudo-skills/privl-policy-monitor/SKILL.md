---
name: privl-policy-monitor
version: 1.0.0
description: Detect policy drift — compare a published privacy policy against actual data practices and regulatory changes, and flag the divergences that create exposure.
author: matrixx0070
tags: [privacy, legal, policy-drift, monitoring, privacy-notice, compliance]
capabilities: []
---

## When to use

Use this to catch the gap between what a privacy policy *says* and what the organization actually *does* — or what the law now requires. Drift is where enforcement lands: a policy promising practices you no longer follow, or silent on new data flows, is a misrepresentation and a compliance gap.

**Not for:** the full program audit (privl-reg-gap-analysis), assessing one new activity (privl-use-case-triage), or drafting the policy from scratch. Use this on an *existing* published policy against *current* reality.

## Method

1. Pull the current published privacy policy/notice and its last-updated date.
2. Reconstruct actual practice from the data map / RoPA: what is collected, purposes, sharing/selling, retention, transfers, cookies/trackers, and rights offered.
3. Diff the two directions:
   - **Policy says, practice differs:** promised deletion timelines, "we don't sell," security claims, categories omitted or overstated.
   - **Practice exists, policy silent:** new vendors, new pixels/SDKs, new purposes (e.g., AI training), new transfers.
4. Overlay regulatory drift: new/changed obligations since last update (e.g., new state laws, opt-out signal recognition like GPC, sensitive-PI disclosures).
5. Rate each divergence by exposure: misrepresentation risk, enforcement visibility, subject harm.
6. **Decision point:** stop-the-bleed items (an untrue "we don't sell" while pixels share data) get flagged for immediate correction, not the next review cycle.
7. **Attorney-escalation gate:** any active statement that is now false, undisclosed sensitive-data or AI-training use, or a new law's applicability → route to counsel; policy language is a legal representation.

## Example

> **Policy:** "We do not sell personal information"; last updated 14 months ago.
> **Practice:** Meta + TikTok pixels active (sharing under CPRA); a new data-enrichment vendor added; support transcripts now feed model training.
> **Drift:** false "no sale/share" statement (P1); enrichment + training undisclosed (P1).
> **Action:** flagged both to counsel; interim GPC honoring + notice update queued.

## Pitfalls

- Reviewing the policy in isolation without checking real data flows.
- Treating an out-of-date policy as harmless — a stale promise is still binding.
- Missing silent additions (a new SDK) because you only checked what the policy already lists.
- Not tracking new laws/opt-out signals that impose fresh disclosure duties.

## Output format

```
POLICY DRIFT — <org> | policy dated: <date> | reviewed: <date>
Divergence: <policy-says-X / practice-is-Y> | Type: <false-claim | undisclosed>
  Exposure: <misrep | enforcement | harm> | Priority: <P1-P3>
Regulatory drift: <new obligation not reflected>
Immediate fixes: <list>
For counsel: <false-statement / new-law items>
```

## Reference

- **GDPR Arts. 13-14** transparency/notice content; **Art. 5(1)(a)** fairness and transparency; updates must reach subjects.
- **CCPA/CPRA** notice-at-collection, "Do Not Sell/Share," sensitive-PI disclosures, GPC/opt-out preference signals.
- **FTC Act §5** unfair/deceptive practices — a policy statement contradicted by practice is actionable.
- Escalate any now-false statement, undisclosed AI-training/sensitive-data use, and new-law applicability to an attorney.
