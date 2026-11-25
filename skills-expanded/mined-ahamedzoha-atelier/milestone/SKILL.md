---
name: milestone
description: Produce the next guided build doc (six-part - Concept, ADR, Guided build, Challenges, Verify, Stretch). Use when the user asks to start a phase, begin a milestone, or wants the next build step.
---

Run the workflow in [`docs/playbooks/milestone.md`](../../../docs/playbooks/milestone.md).

Read the active mode and current phase from `PROJECT.md` first, find the next
milestone in `docs/progress.md`, then write
`docs/milestones/<phase>.<n>-<slug>.md` from the six-part template. Respect the
mode (in `guided`, deliver annotated snippets only — never edit app code).
