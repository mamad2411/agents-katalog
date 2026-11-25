---
name: grill-visual-hierarchy
description: Stress-test and redesign a flat, same-color, hard-to-scan UI through visual hierarchy, information priority, depth, semantic color, and glanceability. Use when a screen, table, dashboard, list, or workflow makes everything compete equally, hides urgent actions, or needs UX direction before implementation.
---

# Grill visual hierarchy

Turn a visually flat interface into a decision hierarchy. The user owns product choices. The codebase, screenshots, and design system supply facts.

## 1. Inspect the real interface

Invoke `grilling` and `domain-modeling`. Read the applicable project instructions, glossary, ADRs, and design references. Inspect the rendered interface when browser access exists; otherwise inspect the components, data, tokens, interactions, responsive rules, accessibility behavior, and tests.

Read [HIERARCHY-LENSES.md](HIERARCHY-LENSES.md) before mapping the design tree.

Done when every visible region has a known purpose, current emphasis, available data, interaction, and governing project constraint. Keep unresolved facts out of the interview and investigate them yourself.

## 2. Name the glance question

Start the design tree with the decision the screen must help its user make at a glance. Separate primary operational information from supporting detail and archival context. Sharpen vague words such as "important," "highlight," "beginning," and "depth" into observable choices.

Done when the user has chosen one plain-language glance question and the actor who asks it.

## 3. Grill the hierarchy

Run the `grilling` workflow in rounds. Ask the whole current frontier and recommend an answer for every question. Cover only branches that affect this interface:

- priority and exception precedence
- ordering and placement
- typography, spacing, grouping, and density
- semantic color and non-color cues
- depth and clickability
- active, completed, blocked, empty, loading, and error states
- filtering, sorting, and persistence
- keyboard, screen-reader, contrast, and supported viewport behavior
- proof through user-visible tests

Use concrete collisions to force precision. Ask what wins when one item is both urgent and blocked, when color is unavailable, when two rows have equal priority, and when a completed item contains an exception.

Done when the frontier is empty, every competing signal has a winner or coexistence rule, and no visual treatment invents a domain state.

## 4. Keep the model honest

Apply `domain-modeling` throughout the rounds. Use the project's canonical terms. Cross-check claims against code and existing decisions. Update the glossary immediately when the team resolves a real domain term. Offer an ADR only when the decision is costly to reverse, surprising without context, and the result of a genuine trade-off.

Done when interface labels respect the domain model, presentation concepts remain presentation concepts, and every discovered contradiction is resolved or called out.

## 5. Confirm the design contract

Summarize the agreed hierarchy as a compact contract:

- the glance question
- priority and tie-break rules
- leading information and supporting information
- semantic color meanings
- depth and interaction rules
- accessibility and viewport commitments
- the highest user-visible test seam
- explicit exclusions

Ask the user to confirm shared understanding. Begin implementation or specification work only after confirmation.

Done when the user confirms the contract without an open design-tree branch.
