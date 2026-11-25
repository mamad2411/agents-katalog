---
name: prove-every-number
description: "Use when code or docs contain a numeric constant, threshold, default, rate, or tolerance — especially one just introduced. Every number is derived from real data or cited to a source; an assumption is labeled as one. Use when a value was picked to look reasonable, a test went green by adjusting a constant, or a doc quotes a figure nobody re-measured."
---

# Prove Every Number

## The failure mode this fixes

An agent needs a value — a timeout, an efficiency factor, a retry limit, a price, a physical constant — and it *makes one up that looks plausible*. `0.95`. `30`. `1.2x`. The code runs, the demo works, and the number sits there radiating false authority. Months later someone builds a real decision on output that was quietly resting on a guess.

The malignant variant: a test fails, and instead of finding out why, the agent *adjusts the constant until it passes*. Now the codebase contains a number whose only provenance is "this made the assertion green" — a lie sticker over a defect.

This skill enforces a simple provenance rule: **every number is derived or cited.** Derived means computed from real inputs or first principles, and the derivation is traceable. Cited means it points at something outside the code's own wishes — a spec, a datasheet, a standard, an RFC, a measured benchmark, a documented product decision. A number that is neither is a finding.

## When to Use This Skill

- You (or the agent) are about to introduce a numeric literal that isn't 0, 1, or a structural index
- Reviewing AI-generated code for magic numbers and invented defaults
- A failing test was fixed by changing a constant, tolerance, or threshold
- Output feeds a real decision — money, capacity, safety, compliance, anything a customer reads
- Real input data exists but the code uses a hardcoded stand-in "for now"
- A README, doc, or UI string quotes a figure about the system's own behavior

**Don't use when:** the number is structurally meaningless (array index, test fixture ID, placeholder in a sketch you've labeled as a sketch). Don't demand a citation for `MAX_RETRIES = 3` in a script nobody's life depends on — scale provenance rigor to how much the output gets trusted.

## Instructions

### 1. Inventory the numbers

In the diff (or file), list every numeric literal and ask of each: *where did this come from?* Three acceptable answers: derived (show the derivation), cited (show the source), or explicitly-labeled assumption (see step 3). "It seemed reasonable" is the finding.

### 2. Prefer the real data over the stand-in

If a real input exists — a config the user provides, a measured value, an API that reports the actual number — use it, and let the constant die. The hierarchy is strict:

1. **Real data** from the actual system/site/user — the truth
2. **Derived** from real data or first principles — the calculation
3. **Cited assumption** — industry standard, spec default, published typical value, *with the source named*
4. **Invented number** — not on the list

A hardcoded value where real data was available isn't a shortcut, it's a fork from reality that every downstream result inherits.

### 3. Make assumptions loud, not embedded

When a value genuinely can't be derived or sourced yet, don't bury it in an expression. Surface it: a named constant with a comment carrying the source or the honest label (`# ASSUMED: no vendor data; typical per <source>; revisit`), or better, a declared default in config/schema where it's visible and overridable. The reader must be able to tell, at a glance, which numbers are load-bearing facts and which are scaffolding.

### 4. Never tune a number to pass a test

If a test fails and the fix on the table is "adjust the constant / widen the tolerance," stop. Either the code is wrong (fix the code), the test's expectation is wrong (fix it *with a justification that references reality*, not the test run), or the constant truly was wrong (then its replacement needs the same derivation-or-citation as any other number). The test result itself is never evidence for a value.

### 5. Numbers in prose are numbers too

A figure quoted in a README, a doc, or the product's own copy ("handles 10k rps", "error under 2%") is a claim with the same provenance rule. Measure it before writing it, re-measure after any change that could move it, and grep the docs for quoted figures when the code behind them changes. When one turns out wrong, correct it visibly rather than silently — the reader who trusted the old value needs to know.

### 6. Audit sibling numbers

A made-up number rarely travels alone. When you find one, sweep the module for its siblings — the same hand that invented one default invented the others.

## Output format

```
Number provenance audit: <scope>
Derived: <n> (derivations traceable)
Cited: <n> (sources named)
Declared assumptions: <list — value, label, source-or-gap, where surfaced>
Findings: <list — invented values, tuned-to-pass constants, hardcoded stand-ins for available data>
Fixes: <each finding → derived / cited / surfaced as assumption / replaced with real data>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Plausible-looking invention | `efficiency = 0.92` because 0.92 sounds like an efficiency. |
| Tuned to green | the constant's git history is "make test pass." |
| Buried assumption | a guess inlined into a formula, indistinguishable from a fact. |
| Stale citation | a comment citing a source the value no longer matches. A wrong citation is worse than none. |
| The doc figure from memory | a number written into the README from recollection, never measured, drifting further with every change. |
| Citation theater | citing a source that doesn't actually contain the number. The skill is provenance, not decoration. |

## Mental Model

> Every number in the code will eventually be believed by someone who can't see where it came from. Derived or cited means they inherit evidence; invented means they inherit your guess wearing evidence's clothes.
