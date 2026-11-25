---
name: litig-claim-chart
version: 1.0.0
description: Build an element-by-element proof matrix mapping each cause-of-action element to supporting facts and evidence.
author: matrixx0070
tags: [litigation, evidence, claims, proof, discovery]
capabilities: []
---

## When to use
Use this when you need to test whether a claim or defense is actually provable before drafting a complaint, opposing summary judgment, or preparing for trial. It forces you to break each cause of action into its legal elements and pin every element to specific evidence. Reach for it whenever someone asks "can we prove this?" or "what are our holes?"

**Not for:** damages modeling (use a damages worksheet) or deposition planning (use litig-oc-status for adversary tracking).

## Method
1. Identify each cause of action and pull its elements from the governing jurisdiction's pattern jury instructions or controlling case law.
2. For every element, list the facts that satisfy it and the evidence that proves each fact (document, testimony, admission, stipulation).
3. Grade each element: PROVEN, WEAK, or GAP. Note the source and whether it is admissible.
4. **Decision point:** if any element is a GAP, decide whether targeted discovery can close it or whether the claim should be dropped or repleaded.
5. **Decision point:** if evidence is WEAK due to admissibility (hearsay, authentication, privilege), flag it for a motion in limine or a foundation witness.
6. Cross-check the opponent's likely affirmative defenses and map your rebuttal evidence the same way.
7. ATTORNEY-ESCALATION gate: route the completed chart and any pleading strategy to a supervising attorney for review before sending or filing.

## Example
> Claim: Breach of contract (CA). Element 2 — Plaintiff's performance.
> Fact: Plaintiff delivered all 12 shipments. Evidence: signed BOLs (Ex. 4), Rodriguez decl. ¶6.
> Grade: PROVEN. Element 4 — Damages: only an unsigned invoice exists → GAP; open discovery for payment records.

## Pitfalls
- **Conflating facts with evidence.** A fact is what happened; evidence is the admissible thing that proves it. List both.
- **Ignoring admissibility.** An element backed only by inadmissible hearsay is a GAP, not PROVEN.
- **Skipping affirmative defenses.** A fully proven claim still fails if you cannot rebut a statute-of-limitations defense.
- **Static charts.** Update after every deposition and production; grades shift as the record develops.

## Output format
```
CLAIM: <cause of action> (<jurisdiction>)
| # | Element | Supporting Facts | Evidence (Ex./Witness) | Admissible? | Grade |
|---|---------|------------------|------------------------|-------------|-------|
DEFENSES: <defense> -> Rebuttal evidence -> Grade
OPEN ITEMS: <discovery needed to close GAPs>
```

## Reference
Elements come from controlling substantive law; pattern jury instructions (CACI, NY PJI, federal circuit models) are the cleanest source. On summary judgment (Fed. R. Civ. P. 56), the movant must show no genuine dispute of material fact on each element; a single unsupported element defeats the claim (Celotex, 477 U.S. 317). Evidence must be reducible to admissible form. Note that element sets and burdens vary by jurisdiction and claim type — always confirm against current controlling authority. General guidance, not legal advice.
