---
name: emplaw-handbook-updates
version: 1.0.0
description: Review an existing employee handbook for legal compliance and drift, flagging gaps against current federal and state requirements.
author: matrixx0070
tags: [handbook, compliance-review, drift, audit, employment-law]
capabilities: []
---

## When to use
Use this when an organization has an existing handbook and needs a compliance sweep — annually, after a legal change, or after crossing a headcount threshold. You are auditing what exists and identifying additions, deletions, and rewrites, not writing a single new policy from scratch. **Not for:** drafting one standalone policy (that is emplaw-policy-drafting); gathering org facts (emplaw-cold-start-interview); setting house style (emplaw-customize); managing a live dispute (emplaw-matter-workspace).

## Method
1. Load the current handbook and the org profile (headcount, states, triggered laws).
2. Build the required-policy checklist for the org's triggered laws and states. Decision point: if headcount recently crossed a threshold (e.g., to 50+), add newly-required sections (FMLA); if it dropped, flag but do not auto-remove.
3. Compare handbook sections against the checklist; mark each Present / Missing / Outdated.
4. Scan for drift: at-will disclaimer, NLRA-safe language, anti-retaliation, updated protected classes, and any clauses that conflict with current law. Decision point: if a clause could chill protected concerted activity, flag for rewrite.
5. Check jurisdiction-specific mandates for every operating state (leave laws, harassment policy, pay transparency).
6. Produce a prioritized findings list: Critical (legal exposure), Recommended, Optional.
7. Route Critical and advice-adjacent findings to counsel before adopting changes.

## Example
A handbook last updated in 2022 for a company now at 55 employees across CA and TX. Review flags: FMLA section Missing (now 50+), CA harassment-prevention language Outdated, an overbroad confidentiality clause that risks chilling NLRA-protected wage discussion (rewrite), and no pay-transparency statement for CA postings. Findings sorted Critical (FMLA, NLRA clause), Recommended (CA harassment), Optional (formatting).

## Pitfalls
- **Copying a template without jurisdiction fit.** A generic handbook can omit state-mandated leave or harassment language; check every operating state.
- **Overbroad confidentiality/social-media clauses.** These frequently violate the NLRA by chilling protected concerted activity; flag for rewrite, not deletion-only.
- **Weakening the at-will disclaimer.** Careless edits can create implied-contract exposure; preserve clear at-will and disclaimer language.
- **Auto-removing sections on a headcount drop.** Coverage can persist across a calendar-week test; flag for counsel rather than silently deleting.

## Output format
```
EMPLAW HANDBOOK REVIEW — <org>   Handbook date: <d>
Headcount/states: <n / states>   Triggered laws: <list>
FINDINGS
  [CRITICAL] <section> — <Missing/Outdated/Conflict> — <statute> — <fix>
  [RECOMMENDED] <section> — <issue> — <fix>
  [OPTIONAL] <section> — <note>
Counsel review required: <sections>
Next review date: <d>
```

## Reference
Common required/expected handbook policies keyed to thresholds (general reference, not tailored legal advice): EEO/anti-harassment and ADA reasonable-accommodation (15+), ADEA age language (20+), FMLA leave policy (50+/75-mi), FLSA wage-and-hour and overtime, COBRA notice (20+), and at-will disclaimer. State mandates vary: CA (FEHA 5+, harassment-prevention policy and training, pay transparency), NY/NYC (sexual-harassment policy, 4+), plus state paid-sick-leave and pregnancy-accommodation laws. NLRA constrains confidentiality, social-media, and no-disparagement clauses for all covered employers. Escalate every Critical finding and any advice-adjacent rewrite to licensed counsel before adoption — this review flags issues, it does not constitute legal advice.
