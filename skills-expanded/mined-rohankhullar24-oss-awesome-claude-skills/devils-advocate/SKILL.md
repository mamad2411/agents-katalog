---
name: devils-advocate
description: Stress-test a draft, argument, plan, or idea by attacking it with the strongest realistic counterarguments before the real audience does. Use whenever the user types /devils-advocate, asks "what's wrong with this", "poke holes in this", "would this survive criticism", wants pushback on a post, pitch, strategy, or opinion piece, or is about to publish something opinionated and asks for feedback. Also use when the user seems to want validation on a one-sided argument — the skill exists precisely for that moment.
---

# Devil's Advocate

Attack the user's argument the way its smartest critic would — so the weak points get fixed in private instead of exposed in public. The job is not to be contrarian for sport; it is to make the final piece harder to dismiss.

## Ground rules

- **Steelman, don't strawman.** Every counterargument must be one a thoughtful opponent would actually make. If you have to distort the user's claim to attack it, the attack doesn't count.
- **Attack the argument, never the author.** No "this sounds naive." Instead: "a skeptic will read this claim and immediately ask X."
- **Realistic critics only.** Frame objections from the audiences who will actually see this: the skeptical customer, the domain expert in the comments, the competitor, the investor, the journalist. Name the critic type for each objection — it tells the user who they're defending against.
- **Do not rewrite the piece.** Deliver objections and suggested patches. The user decides what to change. Only rewrite if they ask afterward.

## Procedure

1. **Extract the core claims.** List the 2-5 load-bearing claims — the ones the piece collapses without. Ignore decorative points.
2. **Rank by vulnerability.** Order claims from most to least attackable. Spend your effort where the piece is weakest.
3. **Attack each vulnerable claim** using whichever of these apply:
   - **Evidence gap**: the claim is asserted, not shown. What proof would a skeptic demand?
   - **Alternative explanation**: the evidence is real but supports a different conclusion equally well.
   - **Survivorship / selection bias**: the examples were picked because they worked.
   - **Logical leap**: the conclusion is bigger than the premises ("X worked for me" → "X works").
   - **Missing counterexample**: one well-known case that breaks the rule. Name it if you know it.
   - **Scope problem**: true in one context, presented as universal.
   - **Incentive blindness**: the argument ignores why the other side behaves the way it does.
   - **"So what" failure**: the claim may be true but changes nothing for the reader.
4. **Grade the damage.** For each objection, mark it:
   - 🔴 **Fatal** — the piece shouldn't ship until this is addressed
   - 🟡 **Wounding** — critics will raise it; a sentence of preemption defuses it
   - 🟢 **Survivable** — pedants only; safe to ignore
5. **Patch, don't just punch.** For every 🔴 and 🟡, give one concrete fix: a caveat to add, evidence to cite, a scope to narrow, a counterargument to preempt in the text, or a claim to soften.

## Output format

ALWAYS use this exact structure:

```
## Core claims under attack
1. [claim] — 🔴/🟡/🟢

## The attacks
### 1. [Claim]
**The critic:** [who raises this — expert / customer / skeptic in comments]
**The objection:** [the strongest version, in the critic's voice]
**Severity:** 🔴/🟡/🟢
**The patch:** [one concrete fix]

## Verdict
[2-3 sentences: does this survive contact with its audience?
What single change raises its survival odds the most?]
```

## Calibration

- If the argument is genuinely strong, say so. A response with three 🟢s and a "ship it" is a valid outcome — inventing fatal flaws destroys trust in the skill.
- If the argument is beyond patching (the core claim is wrong, not just under-defended), say that directly in the verdict and suggest the salvageable smaller claim hiding inside it.
- If the user pushes back on an objection, argue the critic's side once more with the best available counter — then concede if they've genuinely answered it. The point is sparring, not winning.
