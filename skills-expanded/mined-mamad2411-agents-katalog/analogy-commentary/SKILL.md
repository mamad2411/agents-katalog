---
name: analogy-commentary
description: Turn source content into a familiar analogy framework, then produce concise commentary angles and a short take. Use when the user asks whether a post, article, speech, or idea is “like” a known story, theory, faction, historical pattern, or strategic lens.
---

# Analogy Commentary

## Overview

Use this skill to explain content through a familiar frame, then turn that interpretation into concise commentary. It works best for social posts, essays, speeches, interviews, and summaries where the user wants a sharper lens rather than a factual report.

Default output is lightweight:

- 1 line on the source content's core claim
- 1 selected analogy framework
- 3-7 mapping bullets
- "similar" vs "not the same" boundaries
- 1-3 commentary angles
- 1 short takeaway paragraph

## When To Use

Use this skill when the user asks for any of the following:

- "Does this sound like `<story / faction / theory / historical pattern>`?"
- "Use `<framework>` to interpret this content."
- "Give me a commentary angle on this post."
- "Map this article to a familiar lens."
- "What's the closest analogy, and where does the analogy break?"

Common source inputs:

- social media long posts and threads
- articles, blogs, essays, speeches, interviews
- user-provided summaries or notes

Do not use this skill when the user primarily needs fact-checking, source verification, legal/medical/financial guidance, or exhaustive research synthesis.

## Workflow

### 1. Extract the real claim first

Before making any analogy, identify:

- what the content is actually arguing
- what tension drives it
- what emotional posture it takes

Useful tension types:

- efficiency vs coordination
- abundance vs scarcity
- order vs disruption
- agency vs submission
- adaptation vs inertia
- signal vs hype

If the source is long, summarize it in 1-3 lines before proceeding.

### 2. Choose one primary lens

Pick the closest framework, not the most stylish one.

Good framework families:

- fiction or literature
- political factions or ideological camps
- business and strategy models
- historical transitions
- organizational behavior

Use `references/frameworks.md` for quick options and trigger examples.

Avoid stacking multiple frameworks unless the user explicitly asks. Default to one main lens and mention one secondary lens only if it materially improves clarity.

### 3. Map structure, not surface details

Explain both:

- what feels similar
- what is importantly different

Prioritize structural similarity:

- role similarity
- incentive similarity
- power relationship similarity
- system dynamic similarity

Deprioritize shallow similarity:

- tone
- aesthetics
- buzzwords
- isolated slogans

### 4. Keep boundaries explicit

Every analogy should include a boundary line such as:

- "It resembles X in posture, but not in end-state."
- "It uses X's emotional register, but the incentives are different."
- "It is closer to X as a strategy than X as a worldview."

This prevents overclaiming and makes the commentary more reusable.

### 5. Produce concise commentary

Default output shape:

```text
Core claim:
Primary lens:
Mappings:
- ...
- ...

Where it fits:
- ...

Where it breaks:
- ...

Commentary angles:
- ...
- ...

Short take:
...
```

Keep the short take crisp and publishable. It should sound like an informed interpretation, not a final truth claim.

## Output Modes

### Default: Lightweight

Use this unless the user asks for more:

- 3-7 mappings
- 1-3 commentary angles
- 100-200 word short take

### Optional: Expanded

If requested, add:

- competing analogies
- audience-specific rewrites
- stronger disagreement / critique
- a social-post-ready version and a memo-style version

See `references/output-patterns.md` for example shapes.

## Quality Bar

The output should:

- name the analogy clearly
- explain why it fits
- explain where it fails
- avoid pretending the analogy is exact
- preserve the user's original topic instead of replacing it with the metaphor

Bad pattern:

- forcing every topic into the same favorite reference
- writing only vibes with no structural reason
- mistaking rhetoric for substance

Good pattern:

- identify the real tension
- choose the nearest framework
- mark the boundary
- turn that into commentary

## Resources

- `references/frameworks.md`: quick analogy families and selection hints
- `references/output-patterns.md`: compact output templates for common requests
