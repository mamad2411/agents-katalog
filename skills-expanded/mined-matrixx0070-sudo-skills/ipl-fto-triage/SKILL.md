---
name: ipl-fto-triage
version: 1.0.0
description: Triage freedom-to-operate risk before a product or feature launches by charting live patent claims element-by-element and recommending proceed, design-around, license, or opinion.
author: matrixx0070
tags: [ip, patent, freedom-to-operate, infringement, claim-chart, risk, escalation]
capabilities: []
---

## When to use

Use this when a team is about to launch a product or feature and needs a fast read on patent-infringement exposure before shipping. It surfaces blocking claims early, while design choices are still cheap to change.

**Not for:** deciding whether your own invention is patentable (use `ipl-invention-intake`); responding to an accusation aimed at you (use `ipl-infringement-triage`); or drafting a demand letter (use `ipl-cease-desist`).

## Method

1. **Define the product.** List the concrete features, components, and processes you will ship. Vague descriptions produce useless searches.
2. **Find relevant patents.** Search by CPC/IPC classification, keywords, and competitor assignees. Capture number, assignee, and status.
3. **Read the independent claims.** These are broadest and define scope. Ignore abstracts and marketing — only claims matter.
4. **Chart element-by-element.** Map each claim element to your product. Under the all-elements rule, literal infringement needs *every* element present; one missing element defeats it (watch the doctrine of equivalents for near-misses).
5. **Check status and geography.** Confirm the patent is in force, unexpired, and granted where you will sell.
6. **Rate risk** (low / medium / high) per patent and overall.
7. **Decision point:** for a medium/high hit, choose **design-around** (change a claimed element) versus **license** (element is core) — weigh engineering cost against royalty.

**ATTORNEY-ESCALATION GATE:** Any live blocking claim you cannot cleanly design around, any willful-infringement exposure, or any need for a formal FTO or non-infringement opinion stops here and routes to a licensed patent attorney or agent. You assist; you do not give a legal opinion. This is not legal advice.

## Example

A wearable estimates hydration from skin impedance. A search finds an in-force US patent whose independent claim recites electrodes + impedance measurement + an ML hydration model. Charting shows all elements read on the design. Risk: high. Recommendation: design-around the ML-model element or license; escalate for a non-infringement opinion before launch.

## Pitfalls

- **Reading abstracts, not claims.** Only the claims define the monopoly; the abstract misleads.
- **Charting dependent claims first.** Independent claims are broadest — start there.
- **Ignoring expiry and geography.** An expired or foreign-only patent may not block you.
- **Treating one missing element as clearance.** The doctrine of equivalents can still reach substitutes.

## Output format

```
FTO TRIAGE — <product/feature> | markets: <countries>
Features assessed: <list>
Patents reviewed:
  | Patent | Assignee | Status/expiry | Indep. claim charted | Every element met? | Risk |
Overall risk: LOW | MEDIUM | HIGH
Decision: proceed | design-around (<element>) | license | opinion-of-counsel
Escalation: <live blocking claim? formal opinion needed? -> patent counsel>
```

## Reference

Patentability bars double as the invalidity arguments you can raise against a blocking patent:
- **§101 — eligible subject matter.** Abstract ideas, laws of nature, natural phenomena excluded (Alice/Mayo).
- **§102 — novelty.** Prior-art anticipation; AIA first-inventor-to-file; the 1-year on-sale and public-use grace/bar.
- **§103 — non-obviousness.** Graham factors.
- **§112 — written description, enablement, definiteness.**

Claims define scope; independent claims are broadest. Literal infringement requires every element (all-elements rule); the doctrine of equivalents reaches insubstantial substitutions. This is not legal advice.
