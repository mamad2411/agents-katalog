---
name: accessibility-audit
description: "Reviews accessibility and applies requested fixes with precise evidence. Use for a WCAG-oriented report or a bounded frontend accessibility repair."
---

# Accessibility audit

Read AGENTS.md and the repository's frontend docs. Use
[accessibility-scan](../accessibility-scan/SKILL.md) for the actual page scan and
source locations. Select report or fix mode from the user request.

1. Record pages, states, viewports, authentication and engine/manual coverage.
   Capture before evidence before any fix. Inspect keyboard access, focus,
   semantics, labels, errors, contrast and motion where relevant to the flow.
2. Prioritize by user impact and reproducible failure. Separate violations,
   incomplete/manual checks and suggestions; cite the applicable rule when known.
3. In report mode, return findings and verification gaps. In authorized fix mode,
   repair the source owner with local design-system primitives and preserve
   existing behavior. Avoid broad component rewrites outside the requested flow.
4. Re-run the affected scan and relevant local checks. Verify keyboard/focus
   behavior on the changed state. Compare before and after and report unresolved
   coverage. Do not suppress a baseline or weaken a rule to claim a pass.
