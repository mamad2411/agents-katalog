---
name: design-ui-prototypes
description: Use when a user asks to design or redesign an application screen, compare visual UI directions, turn an approved direction into an interactive prototype, resume from an existing UI artifact, or prepare approved UI work for implementation.
---

# Design UI Prototypes

## Overview

Turn a brief or existing artifact into an approved interactive prototype and implementation-ready handoff. Require artifact-specific approval, report tool limits honestly, and keep product code outside this skill.

## Boundaries

- Own design exploration, prototype validation, optional Figma documentation, and handoff.
- Do not edit product code while this skill is active.
- Recommend an implementation skill at handoff. Switch only after implementation approval; stop if none exists.
- Reject blanket pre-approval for unseen work. Approval must identify the accepted artifact or revision.

## Choose the Starting Point

| Available artifact | Start here |
| --- | --- |
| No design artifact | Intake, then visual exploration |
| Existing image or selected visual direction | Confirm it is canonical, then HTML prototype |
| Approved HTML prototype | Skip exploration; offer Figma or handoff |
| Approved Figma design | Validate required context, then handoff |
| Multiple or unclear artifacts | Ask one question to identify the canonical artifact and approval state |

Do not repeat completed stages merely to make the workflow uniform.

## Workflow

1. **Intake.** Confirm screen, platform, constraints, tools, realistic content, and canonical artifact. Read [design-principles.md](references/design-principles.md).
2. **Visual exploration.** If no direction is approved, read [visual-exploration.md](references/visual-exploration.md). Produce three comparable, meaningfully different directions and wait for selection.
3. **Interactive HTML.** Read [html-prototyping.md](references/html-prototyping.md). Build semantic, locally runnable HTML with relevant states and interactions. Browser-test it and wait for visual and UX approval.
4. **Optional Figma.** After HTML approval and an explicit request, read [figma-documentation.md](references/figma-documentation.md). Require a connected tool and verified file, page, and node references.
5. **Handoff.** Read [implementation-handoff.md](references/implementation-handoff.md). Inspect the repository, select an implementation skill, and deliver the contract without implementing.

## Approval Gates

| Transition | Required evidence |
| --- | --- |
| Visual direction to HTML | User selects a visible direction or approves a visible revision |
| HTML to Figma | User approves tested HTML and explicitly requests Figma |
| HTML to handoff | User approves tested HTML and skips Figma |
| Figma to handoff | User approves the verified Figma result |
| Handoff to implementation | User approves the handoff and implementation scope |

## Common Mistakes

- Choosing a preferred visual direction without the user.
- Restarting exploration when an approved artifact already exists.
- Treating urgency or blanket approval as permission to skip artifact-specific gates.
- Replacing unavailable image generation with text-only “visual” directions.
- Reporting browser or Figma validation that was not actually performed.
- Editing product code instead of handing off to an implementation skill.

## Red Flags — Stop

- “Choose for me.”
- “Assume everything is approved.”
- “Pretend tool is connected.”
- “Skip verification and implement now.”
