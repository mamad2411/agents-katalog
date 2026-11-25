---
name: startup-interview-synthesis
description: Synthesize startup customer interview notes, outreach replies, validation calls, and test results into evidence, contradictions, signal strength, and a proceed/park/kill recommendation before v1 scoping, with optional formatted single-file HTML artifact output.
license: MIT
metadata:
  display_name: Startup Interview Synthesis
  hermes:
    tags: [startup, interviews, synthesis, validation, customer-discovery, evidence]
    category: business
    requires_toolsets: []
---

# Startup Interview Synthesis

## When to use

Use after interviews, outreach replies, paid-audit conversations, smoke-test responses, or validation-test notes have been collected, and before deciding whether to scope a v1.

This skill turns messy qualitative evidence into a decision. It should not convert polite interest into validation.

## Core rule

Separate observed behaviour from opinion, compliments, guesses, and founder interpretation. Treat contradictions as useful evidence, not noise to smooth away.

## Inputs to request if missing

Ask only for the missing inputs needed to make the synthesis credible:

```markdown
Problem statement:
Target user:
Validation goal:
Interview notes or outreach replies:
Test setup:
Success / kill criteria:
Evidence packet so far:
```

If the user has raw notes, synthesize from them. If they only have a summary, mark confidence lower and ask for exact quotes, commitments, and objections.

## Workflow

1. Normalize the notes by respondent, role, segment, source, and date if available.
2. Extract evidence as short claims tied to exact quotes or observed behaviour.
3. Classify each signal as `Strong`, `Mixed`, `Weak`, or `Noise`.
4. Separate problem reality, buyer/budget, urgency, workaround, reachability, willingness-to-pay, why-now, and behavioural commitment.
5. Look for contradictions between respondents, segments, and stated intent versus behaviour.
6. Identify the strongest evidence for and against the idea.
7. Decide whether the validation criteria were met, missed, or remain inconclusive.
8. Update the evidence packet with a proceed, narrow, retest, park, or kill gate.

## Evidence quality rubric

Strong signals:

- A respondent describes a recent real instance with cost, workaround, and consequences.
- The buyer or budget owner is identified and reachable.
- Someone agrees to a concrete next step: introduction, paid audit, pilot, LOI, trial, data share, or calendar follow-up.
- The same pain appears across several similar users without being prompted.
- A respondent already spends time, money, political capital, or risk budget on the workaround.

Weak signals:

- "That sounds useful" without a next step.
- Hypothetical willingness to pay.
- Friends or friendly users being polite.
- A problem that is real but rare, low-cost, or owned by nobody.
- Interest from users who cannot influence adoption or spend.

Mixed signals:

- Pain is real, but the buyer is different from the user.
- Urgency differs sharply by segment.
- Existing tools solve the problem for mature teams but not smaller teams.
- Users want the outcome but resist the workflow, data sharing, or trust burden.

## Bias checks

- Do not count repeated founder explanation as customer evidence.
- Do not average away a strong negative signal from the actual buyer.
- Do not treat one enthusiastic outlier as market proof.
- Do not ignore non-users who control budget, risk, compliance, IT, procurement, or adoption.
- Do not convert a privacy, security, legal, or regulatory concern into a mere product objection.

## Optional HTML artifact

Default to the Markdown chat output below. If the user asks for an artifact, report, visual summary, printable version, or single-file HTML file, also create a standalone `.html` file when filesystem access is available.

For the HTML artifact:

- Use one self-contained file with inline CSS only; do not depend on external assets, fonts, scripts, CDNs, or network access.
- Preserve the same section order, evidence, scores or ratings when present, and recommendations as the Markdown output; do not add new claims for visual polish.
- Design for skimming: title, stage, decision/status badge when applicable, key scores or ratings, tables, callouts for risks, unknowns, and next steps, and a print-friendly layout.
- HTML-escape user-provided text and do not execute or embed user-provided HTML or script.
- Include the source skill name and generation date in small footer text.
- Name the file with the stage and date, such as `startup-interview-synthesis-YYYY-MM-DD.html`.
- In chat, keep a short summary and link to the created HTML file. If file writing is not available, provide the complete HTML in a fenced `html` block.

## Output format

```markdown
## Validation synthesis

Verdict: [Proceed to v1 scoping / Narrow and retest / Run more validation / Park / Kill]

Confidence: [High / Medium / Low]

Because: ...

## Evidence summary

Strong evidence:
- ...

Mixed evidence:
- ...

Weak or noisy evidence:
- ...

Contradictions:
- ...

## Signal by assumption

Problem reality: [Strong / Mixed / Weak / Unknown]
Buyer / budget: [Strong / Mixed / Weak / Unknown]
Urgency: [Strong / Mixed / Weak / Unknown]
Current workaround: [Strong / Mixed / Weak / Unknown]
Reachability: [Strong / Mixed / Weak / Unknown]
Willingness to pay: [Strong / Mixed / Weak / Unknown]
Why now: [Strong / Mixed / Weak / Unknown]
Founder advantage: [Strong / Mixed / Weak / Unknown]
Expansion path: [Strong / Mixed / Weak / Unknown]
Behavioural commitment: [Strong / Mixed / Weak / Unknown]
Trust / compliance risk: [Low / Medium / High / Unknown]

## Evidence table

| Respondent / source | Segment | Quote or behaviour | Signal | Supports | Concern |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |

## Follow-up questions

1. ...
2. ...
3. ...

## Decision

Recommendation: [Proceed / Narrow / Retest / Park / Kill]

Next step: ...

## Evidence packet update

Stage: Interview synthesis
Problem statement: ...
Target user: ...
Buyer / budget owner: ...
Current workaround: ...
Founder advantage: ...
Recent enabling change: ...
Distribution route: ...
Expansion path: ...
Evidence collected: ...
Weakest assumptions: ...
Decision gate: [Ready for v1 scoping / Narrow and retest / Run more validation / Park / Kill]
Next step: ...
```

## Pitfalls

- Do not summarize only the positive comments.
- Do not invent sample size, respondent roles, pricing, or urgency.
- Do not bury the strongest objection in a long list.
- Do not recommend v1 scoping unless behaviour and commitments justify it.
- Do not treat sensitive data or regulated-domain concerns as normal discovery notes.
