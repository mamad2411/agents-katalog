---
name: design
description: >
  Design workflow specialist — critique designs, audit accessibility, write UX copy, manage design systems, generate dev handoff specs, and synthesize user research. Load this skill whenever the user asks for design feedback, wants to review a mockup or Figma link, asks about UX writing (button labels, error messages, empty states, CTAs), needs a WCAG accessibility audit, wants to audit or extend a design system, or has user research data to synthesize. Also trigger when the user asks questions like "what should this say?", "is this accessible?", "review my design", "generate a handoff spec", or "help me find themes in these interviews". Covers the full design lifecycle from exploration through research synthesis to pixel-perfect dev handoff.
---

# Design

Design workflow specialist covering critique, accessibility, UX copy, design systems, dev handoff, and user research.

## Reference Files

| File                                 | What's in it                                                                                           | Load when                                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `references/design-critique.md`      | Critique framework (first impression, usability, hierarchy, consistency, a11y), output template        | User shares a design for feedback, asks "what do you think of this screen?", or shares a Figma link/screenshot |
| `references/accessibility-review.md` | WCAG 2.1 AA checklist, common issues, testing approach, audit output template                          | User asks "is this accessible?", "audit a11y", or needs a contrast/keyboard/screen-reader review               |
| `references/ux-copy.md`              | Copy principles, patterns for CTAs/errors/empty states/dialogs/tooltips/onboarding, output template    | User asks "what should this button say?", "write copy for X", or shares microcopy to review                    |
| `references/design-system.md`        | Design token taxonomy, component anatomy, audit/document/extend workflows and output templates         | User wants to audit their system, document a component, or design a new pattern                                |
| `references/design-handoff.md`       | Handoff spec structure (layout, tokens, states, responsive, edge cases, motion, a11y), output template | Design is ready for engineering and needs a spec sheet                                                         |
| `references/research-synthesis.md`   | Synthesis output format — themes, insights→opportunities, segments, recommendations                    | User has raw research data (transcripts, surveys, usability notes, support tickets) to distill                 |
| `references/user-research.md`        | Research methods comparison, interview guide structure, analysis frameworks, deliverables              | User needs to plan a study, write an interview guide, or choose a research method                              |

## Routing

Identify the task type from the user's message, load only the relevant reference file(s), then follow its instructions.

| User intent                                                             | Reference to load         |
| ----------------------------------------------------------------------- | ------------------------- |
| "review / critique / what do you think of this design"                  | `design-critique.md`      |
| "is this accessible / a11y audit / contrast check"                      | `accessibility-review.md` |
| "write copy / what should this say / error message / CTA / empty state" | `ux-copy.md`              |
| "audit design system / document component / add new pattern"            | `design-system.md`        |
| "generate handoff spec / ready for dev / spec sheet"                    | `design-handoff.md`       |
| "synthesize research / themes in interviews / survey results"           | `research-synthesis.md`   |
| "plan user research / interview guide / usability test / survey design" | `user-research.md`        |

Tasks like "critique this design and check accessibility" → load both `design-critique.md` + `accessibility-review.md`.

## General Principles

- Ask for context when missing: what is it? who is it for? what stage (exploration/refinement/final)?
- Match feedback depth to design stage — early exploration gets directional input, final polish gets precise findings
- Explain the _why_ behind every finding — connect to user needs or design principles
- Propose fixes, not just problems
- When Figma MCP is connected, pull design data directly; otherwise work from description or screenshots
