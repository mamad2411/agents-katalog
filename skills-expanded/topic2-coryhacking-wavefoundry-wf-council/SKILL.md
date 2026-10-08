---
name: wf-council
description: Convene an on-demand review on one artifact, choosing among the role-based Wave Council, the stance-based Archetype Council, and standalone Red-team review. Not the open wave's required lanes (Review wave) and not Review plan, the optional change-doc or current-wave stress test whose aliases are Interrogate this plan and Stress-test this plan.
---

# Convene a review council (Wavefoundry skill)

This skill is a router: pick the review form that fits the artifact, then read and follow that form's prompt doc. The full chooser table lives in `docs/prompts/archetype-council.prompt.md`.

- Code, architecture, or trust-boundary artifact: **Council review**, `docs/prompts/council-review.prompt.md`.
- Prose, naming, AC formulation, or decision narrative: **Archetype review**, `docs/prompts/archetype-council.prompt.md`.
- One sharp adversarial challenge on a single artifact: **Red-team review**, `docs/prompts/red-team-review.prompt.md`.
- These on-demand reviews record no lifecycle signoffs and satisfy no gate; when a prompt directs recording against a wave, use the `wf_review_event` MCP tool.
- Boundary: the open wave's REQUIRED review lanes run under Review wave (`wf-review-wave`), and a change doc or current wave record gets Review plan (`wf-review-plan`; aliases: Interrogate this plan, Stress-test this plan) before implementation; this router is for on-demand reviews outside both.
