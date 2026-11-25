---
name: copy-editing
description: "Editing and refreshing existing marketing copy. Use when the user already has copy to proofread, tighten or improve, not write from scratch."
metadata:
  version: 2.0.0
---

# Copy Editing

Improve existing copy through focused passes and keep the author's message and voice. Each edit gets a stated reason. Present findings with proposed rewrites and let the author decide.

Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`, or legacy `product-marketing-context.md`) first when it exists, and edit toward its brand voice and customer language.

Ask only what is missing: the goal (awareness, conversion, retention), the action readers should take, known concerns, available proof, new copy or refresh.

## Seven sweeps

One dimension per pass, in this order. After each sweep, re-check the earlier ones, since a fix in one often breaks another. Finish when a full round finds nothing new.

1. **Clarity**: one main idea per section, copy addresses the reader. Look for sentences carrying too much, unclear pronouns, jargon, abstractions, qualifications burying the point.
2. **Voice and tone**: one register throughout. Read aloud. Look for formal/casual drift, "we" vs "the company", unintended humor or technical bursts.
3. **So what**: ask "so what?" of every claim and add the "which means..." bridge from feature to outcome.
4. **Prove it**: every claim needs nearby evidence (named testimonial, number, case study, third-party validation, guarantee, logos, review score). "Trusted by thousands" and "industry-leading" need a source, or get softened.
5. **Specificity**: swap vague verbs and adjectives for numbers, timeframes and examples ("Save time" becomes the real hours per week).
6. **Heightened emotion**: paint the before state, use sensory detail, one micro-story, a shared experience. Keep it authentic and in service of the message.
7. **Zero risk**: around each CTA, list the reasons to hesitate and check each is answered: guarantee, trial, "cancel anytime", social proof, what happens next, privacy, hidden costs. Replace "Contact us" with a concrete next step.

Detailed checks, tests and fixes per sweep: [references/sweeps.md](references/sweeps.md).

## Quick pass

For small edits skip the sweeps and apply: cut intensifiers and filler (very, really, just, actually, basically, "in order to"), prefer plain words (use, set up, help, new), convert passive voice and nominalizations ("make a decision" to "decide"), one idea per sentence, important information first, paragraphs of 2 to 4 sentences. Word lists and symptom/fix pairs (wall of features, corporate speak, buried CTA, mixed audiences): [references/quick-checks.md](references/quick-checks.md). Larger plain-English word map: [references/plain-english-alternatives.md](references/plain-english-alternatives.md).

## Quality gates

- **Final QA** before delivering edits: [references/checklist.md](references/checklist.md).
- **Expert panel** (3 to 5 personas scoring 1 to 10, revise until every score is 7+ and the average 8+) for launch copy, pricing pages and high-traffic landing pages; skip for minor edits. Personas and rubric: [references/expert-panel.md](references/expert-panel.md).

## Refreshing existing pages

Pages decay: stale stats, outdated examples, drifted voice, a changed product. For traffic decline or stale data, use the refresh checklist and the refresh-vs-rewrite matrix in [references/content-refresh.md](references/content-refresh.md).

## Working with the author

1. Run a sweep, show what you found and why it matters.
2. Propose a specific edit for each finding.
3. Let the author take the final decision, then re-check earlier sweeps on the updated copy.

New copy from scratch goes to `copywriting`; structural or page-level changes go to `cro`.
