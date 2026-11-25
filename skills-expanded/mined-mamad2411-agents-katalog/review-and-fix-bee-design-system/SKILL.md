---
name: review-and-fix-bee-design-system
description: "Use when reviewing a Figma screen or component for Bee-DS integration drift, then fixing one approved Bee-backed finding in a narrow follow-up pass. Trigger for requests such as 'review this for Bee-DS and fix it', 'audit this screen against Bee and repair the top issue', or 'use Bee-DS to review then fix this Figma link'."
---

# Review And Fix Bee-DS Drift

Use this skill when the user wants a Bee-DS-specific review-and-repair loop on a Figma screen, frame, or component.

This is a Bee-DS-specific specialization of [review-and-fix-design-system](../review-and-fix-design-system/SKILL.md).

Follow the full workflow in [review-and-fix-design-system](../review-and-fix-design-system/SKILL.md) for scope control, one-finding selection, and narrow fix validation. This skill adds only Bee-specific defaults, lookup rules, and routing guidance.

## Use This Skill For

- requests such as `review this for Bee-DS and fix it`, `audit this against Bee and repair the top issue`, or `use Bee-DS to review then fix this screen`
- starting from a Figma URL when the exact Bee finding is not known yet
- keeping the write scope narrow while still grounding the review and repair in Bee-DS families, variants, tokens, and icons

## Load First

- [review-and-fix-design-system](../review-and-fix-design-system/SKILL.md)
- [bee-ds-live-lookup](../bee-ds-live-lookup/SKILL.md) when the exact Bee family, variant, token, or icon still needs verification
- [bee-ds-design-guide](../bee-ds-design-guide/SKILL.md) when Bee pattern choice, spacing, or screen structure is ambiguous
- `figma-use` before any `use_figma` write call

## Skill Boundary

This skill is for Bee-specific review plus one narrow Bee-backed repair.

Use:
- [review-and-fix-design-system](../review-and-fix-design-system/SKILL.md) for the base workflow
- [bee-ds-live-lookup](../bee-ds-live-lookup/SKILL.md) to verify the exact current Bee family, variant, token, or icon in Figma
- [bee-ds-design-guide](../bee-ds-design-guide/SKILL.md) to choose the right Bee pattern when the design intent is not obvious

Do not use this skill for:
- broad Bee-DS migration across multiple coupled sections
- general Bee screen redesign
- creating new Bee-DS components or inventing local Bee-like approximations

Route broader migration work to [apply-bee-ds-toolkit](../apply-bee-ds-toolkit/SKILL.md).

## Bee-Specific Overrides To The Base Workflow

Apply these rules while following the base review-and-fix workflow.

### Review Defaults

- bias the review toward concrete Bee-DS integration drift, not general design taste
- prefer findings that map cleanly to a published Bee primitive, family, token, or icon
- when several findings exist, prioritize the highest-signal issue that can plausibly be repaired with one Bee-backed change

### Lookup Before Fix When Bee Choice Is Ambiguous

Before the fix phase, use [bee-ds-live-lookup](../bee-ds-live-lookup/SKILL.md) when:
- more than one Bee family looks plausible
- the Bee variant names are unclear
- the node may depend on a Bee icon or token that needs exact verification
- the fix will fail if the wrong Bee family is chosen

Do not guess Bee names from memory when live lookup can confirm them.

### Design Judgment Before Fix When Pattern Choice Is Ambiguous

Before the fix phase, use [bee-ds-design-guide](../bee-ds-design-guide/SKILL.md) when:
- the screen could reasonably use more than one Bee pattern
- spacing or section structure is part of the compatibility question
- the review finding is clear, but the Bee-compliant repair shape is not

### Fix Scope Rules

The write phase must still stay narrow:
- one approved finding at a time
- one offending node or local cluster at a time
- minimal read scope
- minimal write scope

Bee specificity does not justify widening into a screen-wide cleanup pass.

## Bee Review Heuristics

- Prefer findings where the offending node is a plain frame, detached text cluster, local wrapper, or raw-value element that should likely map to a Bee family.
- Prefer findings with a credible Bee replacement path over speculative Bee taste feedback.
- If the highest-priority issue would require coordinated changes across several sibling sections, stop and route to [apply-bee-ds-toolkit](../apply-bee-ds-toolkit/SKILL.md) instead.

## Bee Fix Heuristics

- If a Bee primitive already exists for the node's role, bias toward a true Bee-backed swap.
- If the Bee component renders the needed title or label internally, remove detached sibling text only after confirming the Bee instance itself renders the copy.
- If a Bee family change crosses component families, inspect the real published properties and descendants before declaring the fix complete.
- If Bee does not publish a safe replacement, report `blocked` instead of fabricating a Bee-like local rebuild.

## Prompt Shapes

- `Review this Figma link for Bee-DS drift and fix the top approved issue: <FIGMA_URL>`
- `Use [review-and-fix-bee-design-system] on this Figma screen: <FIGMA_URL>`
- `Audit this against Bee-DS and repair one approved finding: <FIGMA_URL>`

## Deliverable Format

When closing the task, report in this order:

1. `Bee review summary`: the highest-signal Bee-DS findings and which one was selected
2. `Bee finding fixed`: what changed and which Bee family, variant, token, or icon was used
3. `Validation`: how the original Bee-DS issue was confirmed resolved
4. `Follow-up`: only when additional Bee findings remain or the task should widen into [apply-bee-ds-toolkit](../apply-bee-ds-toolkit/SKILL.md)