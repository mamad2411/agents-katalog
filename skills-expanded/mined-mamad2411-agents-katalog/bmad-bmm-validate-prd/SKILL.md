---
name: bmad-bmm-validate-prd
description: >-
  Use this skill to run a comprehensive automated validation of a PRD against
  BMAD standards across 12 quality dimensions, producing a detailed validation
  report with actionable improvement recommendations. Invoke when the user says
  "validate this PRD" or "run PRD validation", or after creating or editing a
  PRD and wanting a quality gate before moving to architecture. The skill
  detects the PRD format, then autonomously checks information density,
  Product Brief coverage, requirement measurability, traceability chains,
  implementation leakage, domain compliance, project-type sections, SMART
  scoring of each requirement, holistic quality, and completeness — then
  presents an interactive report with options to fix issues using bmad-bmm-edit-
  prd. Input is a PRD file path. Output is a validation report with scores and
  prioritized findings. Unlike bmad-bmm-check-implementation-readiness (which
  validates the whole planning suite), this skill validates one PRD document
  only. Do not invoke on an empty or non-existent PRD.
argument-hint: "Provide the path to the PRD file to validate. Optionally mention input documents (product brief, research)."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Validate PRD

Validate a PRD against BMAD standards through comprehensive automated checks.

## Outcome

A comprehensive validation report assessing PRD quality across 12 validation dimensions, with actionable findings and improvement recommendations.

## Your Role

Validation Architect and Quality Assurance Specialist. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- Steps 3–12 auto-proceed without user interaction (autonomous validation sequence).
- Steps 1, 2, and 13 are interactive — halt at menus and wait for user input.
- Track progress via `validationStepsCompleted` array in the validation report frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `user_skill_level`, etc.).
2. Announce: **"Validate Mode: Validating an existing PRD against BMAD standards."**

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

### Interactive Setup
1. [Discover Document](./steps/discover-document.md) — Confirm PRD path, load input documents, initialize validation report
2. [Detect Format](./steps/detect-format.md) — Classify PRD format (BMAD Standard/Variant/Non-Standard), optional parity check

### Autonomous Validation Sequence (Steps 3–12 auto-proceed)
3. [Validate Density](./steps/validate-density.md) — Scan for information density anti-patterns
4. [Validate Brief Coverage](./steps/validate-brief-coverage.md) — Map Product Brief content to PRD (skip if no brief)
5. [Validate Measurability](./steps/validate-measurability.md) — Check FR/NFR measurability and format
6. [Validate Traceability](./steps/validate-traceability.md) — Validate vision → success → journeys → FRs chain
7. [Validate Implementation Leakage](./steps/validate-implementation-leakage.md) — Detect technology/implementation terms in requirements
8. [Validate Domain Compliance](./steps/validate-domain-compliance.md) — Check domain-specific regulatory requirements (skip for low complexity)
9. [Validate Project Type](./steps/validate-project-type.md) — Validate project-type required/excluded sections
10. [Validate SMART](./steps/validate-smart.md) — Score each FR on SMART criteria (1–5)
11. [Validate Holistic Quality](./steps/validate-holistic-quality.md) — Multi-perspective document quality assessment (1–5 rating)
12. [Validate Completeness](./steps/validate-completeness.md) — Final gate: template variables, section completeness, frontmatter

### Interactive Report
13. [Finalize Report](./steps/finalize-report.md) — Summarize all findings, present results, offer next steps

## Menu Pattern

Steps 1 and 2 share this menu after setup is complete:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current context, then return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current context, then return to menu.
- **[C] Continue** — Proceed to next step.

Step 13 has its own action menu (review findings, edit PRD, quick fixes, exit).

## Halt Conditions

- HALT if no PRD file path is provided and none can be found in `{planning_artifacts}` after prompting
- HALT if the PRD file is found but is empty or unreadable
- HALT if `./data/prd-purpose.md` is unreadable — validation criteria cannot be loaded
- HALT if the validation report cannot be written to `{planning_artifacts}` due to a path resolution failure

## Data Files

- [./data/project-types.csv](./data/project-types.csv) — Project type detection signals, required/skip sections
- [./data/domain-complexity.csv](./data/domain-complexity.csv) — Domain complexity levels, key concerns, compliance requirements
- [./data/prd-purpose.md](./data/prd-purpose.md) — BMAD PRD philosophy, standards, and validation criteria

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis (used in holistic quality step)
- `bmad-core-party-mode` — Collaborative brainstorming
- `bmad-bmm-edit-prd` — Edit workflow (offered at completion for fixing issues)

## When to Use

Use this skill when:
- The user says "validate this PRD" or "run PRD validation"
- A PRD needs comprehensive automated validation against BMAD standards across 12 validation dimensions
- The user wants a validation report with actionable findings and improvement recommendations before proceeding to architecture

