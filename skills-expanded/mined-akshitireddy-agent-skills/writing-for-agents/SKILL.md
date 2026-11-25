---
name: writing-for-agents
description: Write or revise skills and agent instruction files with precise scope, useful references, and clear completion criteria.
---

# Write useful agent instructions

Include guidance that changes a decision: project constraints, fragile steps,
domain knowledge, useful references, and observable completion criteria.
Respect the user's task, existing authorization, and the host's instruction
priority. Prefer clear desired behavior over generic encouragement or fixed
rituals. Match procedural detail to the actual risk.

For skill structure and invocation policy, read
[skill mechanics](SKILL-MECHANICS.md). For a substantial instruction redesign,
read [instruction design](references/instruction-design.md). A wording correction
does not require both references.

Keep discovery descriptions short and specific. Separate workflows only when
their triggers or resources differ. Keep each rule in one authoritative place;
load supporting detail only for the branch that needs it.

Define what completes the requested outcome, what requires input, and what
side effects are authorized. Verification should establish the relevant claim
without expanding a small change into a full audit. Preserve explicit user
preferences while removing duplicated or stale scaffolding.

Validate naming, frontmatter, links, and any changed helper behavior. For complex
changes, test realistic decisions independently when available and authorized.
Structural validation alone does not establish behavioral quality.
