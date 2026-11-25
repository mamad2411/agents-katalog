---
name: optimize-slide-diagram
description: "Optimize an existing PowerPoint slide diagram around its intended message, using the slide text and supplied evidence while preserving the deck design. Use to clarify a diagram, adapt it to a topic, or choose a better visual structure. 既存の記述と伝えたい結論に合わせた図解の最適化、別トピックへの更新に使用。"
license: MIT
---

# Optimize Slide Diagram

## Scope and inputs

Default to the selected slide only. Ask which slide if selection is unavailable;
edit multiple slides only when explicitly requested. Preserve the deck's language.
This skill changes the explanation's structure, not the presentation theme.
It must work independently of other skills, local scripts, and specific tool names.

Use the existing slide text and user-supplied materials as the primary evidence.
Identify the topic, a one-sentence takeaway, supporting facts, and intended audience.
Infer an unambiguous topic from the existing content rather than asking needlessly.
If the topic or meaning is unclear, ask. If the takeaway is not explicit, propose
one based on the content; obtain confirmation before adopting an interpretation
that changes its meaning, implies agreement, or adds a new conclusion.
Follow an indicated audience; otherwise assume an executive-level summary and
disclose that assumption without deleting necessary technical qualifications.

Do not search internal systems or the web by default. Ask for missing evidence;
search externally only when requested and use only authorized sources.
Do not invent numbers, proper names, causal links, priorities, or next actions.
Use hypothetical examples only when requested and label them clearly in the slide.
Preserve required citations, units, caveats, and the distinction between fact and inference.

## Procedure

1. Inspect the target slide's text, notes relevant to meaning, object bounds,
   styles, grouping, and available preview. Identify the title, lead, actors,
   relationships, key decision, and any action block. Inspect dependencies such
   as links, animation, and connectors before modifying shapes. Keep a recoverable
   version. If editing or inspection is unavailable, state the limitation and
   provide a proposed layout instead of claiming the slide was changed.
2. Establish the takeaway and map every retained fact to its role in the explanation.
   Keep the title and lead aligned with that takeaway. Preserve disagreements and
   uncertainty; do not make a topic look like consensus merely to simplify a diagram.
3. Choose a structure for the meaning, not for superficial symmetry:

   | Content relationship | Starting structure |
   |---|---|
   | Different positions leading to a shared question or agreement | Converging lanes: positions, common issue, decision |
   | Steps or change over time | Flow or timeline |
   | Current versus future, or alternatives | Side-by-side comparison or before/after |
   | Roles, reporting lines, or levels | Hierarchy or organization diagram |
   | Relationships between elements | Matrix, set diagram, or cycle, only when those relationships are supported |
   | Measured trends, distributions, or proportions | Editable native chart with source values |

   These are starting points, not a closed list. Keep the existing type when it
   already explains the message well. Use overlap only for genuine shared membership,
   cycles only for recurrence, and arrows only for actual flow or convergence.
   Use an editable table for exact lookup/comparison data when it is clearer.
4. Organize the slide into takeaway, main diagram, and next action when the content
   supports all three. Do not invent an action to fill a third tier. Highlight the
   key point with existing contrast, a short label, or a deck-compatible card/band;
   do not add decorative rules or arbitrary "most important" labels.
5. Preserve the actual deck's fonts, palette, background, corners, and arrow motifs.
   Do not force a particular font or blue palette onto another template.
   Use existing muted/strong accents for current/future states where appropriate,
   with explicit labels so color is not the only signal.
6. Choose the smallest suitable edit:
   - Same elements and relationships: update text and preserve run formatting.
   - Different element count: reuse suitable shapes, adjust spacing, and reconnect
     relationships; remove only elements made obsolete by the approved redesign.
   - Unsuitable structure: rebuild only the diagram block, keeping other content.
   Keep shapes, connectors, tables, and charts editable; do not rasterize the diagram.
   Ask before changes that would discard interactions, timing, or unsupported features.
   Do not clear the slide, replace its identity, or add another slide without permission.
7. Keep one message per box. For Japanese, aim for about 100-200 visible characters
   in the main explanation; for English, use a similarly concise, readable summary
   rather than enforcing a Japanese character count. Never remove evidence or
   change meaning just to hit a length target.
   Aim for headings at least 16 pt, body text at least 14 pt, and notes at least
   12 pt; do not newly shrink text below 10.5 pt to force a fit.
   Preserve compatible template sizing. If content cannot fit, propose shortening
   or splitting and ask before expanding beyond the selected slide.
8. Use consistent card widths and gaps, align edges, and keep about 0.5 inch
   outer margins unless the template intentionally uses a different safe area.
   Add numbering only when it represents a reading order. Keep citations readable
   and all shapes within the slide. Do not draw measured charts by hand with shapes.
9. Inspect duplicate candidates before and after the edit. Matching coordinates
   and text alone do not prove equivalence. Report suspicious pairs and leave
   them untouched; do not delete pre-existing duplicates as part of this skill.
   If cleanup is requested, obtain approval for a separate, content-aware deletion
   preview; `remove-duplicate-shapes` is an optional companion, not a prerequisite.
   Update existing objects rather than stacking a second generated diagram on them.
10. Preview the result, collect issues, fix them together, and inspect again.
    Repeat if necessary; one repair pass is not a reason to stop with known issues.
    Check takeaway fidelity, all relevant facts, no stale topic labels in the edited
    block, no overflow/overlap, readable type/contrast, correct connectors, no newly
    introduced duplicates, and no changes outside the requested scope.
    If rendering is unavailable, report the visual checks as unverified.

## Report

Update the selected slide in place when supported. In two or three sentences,
explain the chosen structure and why it fits the message, any confirmed assumptions
or explicitly requested hypothetical content, and unresolved duplicate candidates
or checks that could not be completed. Do not claim to have inspected an example
deck, slide number, or object ID that the user has not actually supplied.
