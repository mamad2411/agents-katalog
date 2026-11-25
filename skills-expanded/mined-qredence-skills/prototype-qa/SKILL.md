---
name: prototype-qa
description: "Reviews a prototype plan or visible/provided prototype details for missing links, ambiguous destinations, dead ends, overlay risks, orphaned frames, and state-logic gaps. Use before sharing a prototype for testing, review, or demo. Treat results as evidence-based QA findings and a manual test plan, not as guaranteed automated traversal unless the current Figma Agent session explicitly supports prototype inspection."
---

# Prototype QA

## Purpose
Find prototype risks before a review, test, or demo by checking visible/provided prototype details and producing a practical manual QA plan.

## Operating Role
Act as a Figma prototype QA reviewer. Inspect visible frames, labels, annotations, comments, existing prototype details if available, and any supplied connection map. Report evidence-backed risks and manual tests. Do not claim exhaustive automated traversal unless the environment explicitly supports it.

## Capability Boundary
Current Figma documentation marks prototyping and interaction editing as coming soon for the Figma Agent. This skill may review visible/provided prototype information, but should not assume it can inspect every hidden connection, click through the prototype, or repair interactions automatically.

## Supported Context
- Start from the selected flow, starting frame, section, or supplied connection map.
- Use visible Figma context first: frames, labels, buttons, links, overlays, annotations, comments, and existing prototype settings if visible.
- Use connector or code context only when supplied. Mark missing context as unverified.
- Ask at most two targeted questions if the starting frame or intended flow is unclear.

## Activation Boundary
Use this skill when:
- A prototype is about to be shared for usability testing, stakeholder review, or demo.
- A flow has changed and prototype coverage may now be stale.
- A team has a prototype connection plan and wants risk review before wiring or testing.

Do not use this skill to build or edit interactions. Use `prototype-from-flow` for planning a new flow and `wire-up-interactions` for a specific interaction spec.

## Required Inputs
- Starting frame or flow scope.
- Intended user path or connection map, if available.
- Known branches or states that should be covered.

If the full interaction graph is not available, proceed with visible evidence and label the review as partial.

## Workflow
1. State the evidence level: visible frames only, supplied connection map, visible prototype settings, or confirmed executable prototype context.
2. Identify expected paths: happy path, back/cancel paths, error paths, overlays, state branches, and terminal success/failure states.
3. Check visible interactive-looking elements for missing or ambiguous destinations: buttons, links, list rows, tabs, icons, cards, and dismiss controls.
4. Check destinations for mismatch risk: label says one thing but likely target frame indicates another, destination frame is missing, or destination frame appears stale.
5. Check overlay behavior risks: missing close path, unsafe outside-click dismissal, unclear modal stacking, or overlay content that should be a full page.
6. Check orphan and dead-end risk: frames that appear part of the flow but are not referenced in the plan, or terminal screens with no obvious next step.
7. Check state-logic risk: branches that require variables, conditionals, or reset behavior but lack a clear state model.
8. Produce a manual test script that a designer can run in presentation/prototype mode.

## Severity Rules
- `Blocker`: would prevent a tester or stakeholder from completing the main path.
- `High`: breaks an important branch, state, overlay, or recovery path.
- `Medium`: creates confusion but has a visible workaround.
- `Low`: polish or documentation gap that will not block the demo/test.

## Guardrails
- Do not mark the prototype as fully passed unless all required paths were actually verifiable.
- Do not claim a link is broken if you can only infer it from missing visible evidence; label it as `Unverified risk`.
- Do not auto-resolve prototype issues or alter the file unless explicitly supported and requested.
- Report exact frame and element names wherever possible.

## Output Contract
Start with a status line: `Prototype QA partial` or `Prototype QA verified` depending on evidence.

Then return:
1. **Scope and evidence level** - what was reviewed and what could not be verified.
2. **Findings** - grouped as `Dead ends`, `Destination risks`, `Overlay risks`, `Orphaned frames`, `State-logic gaps`, and `Ambiguous interactions`.
3. **Manual test script** - ordered steps for happy path and branches.
4. **Unverified areas** - what needs manual presentation-mode testing or product confirmation.
5. **Fix/spec suggestions** - exact interaction specs to create next, without claiming they were applied.
