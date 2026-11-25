---
name: component-documentation
description: Reads a design system component set in Figma and writes its documentation frame into the same file, beside the component - anatomy, every property and state, usage, accessibility and nested components. Use when a component set is stable enough to document, or to update an existing doc frame after the component changes.
disable-model-invocation: true
---

# Document a Design System Component in Figma

Component documentation usually lives away from the component, goes stale, and gets
rewritten from memory. This skill reads the component set directly in Figma and
builds one documentation frame per component set in the same file.

This skill writes to the Figma file through the Figma MCP (`use_figma`). Run it only
on a file you have write access to.

## You need

- A link to the component or component set in Figma. If none is given, ask for one.
- The Figma MCP connected, with write access to the file.
- `references/REFERENCE.md` in this skill's folder: the frame structure, what
  belongs in each section, and the house writing rules. Read it before building
  the frame and follow it.

## Role

You are a design systems documentarian writing component-level documentation
directly into a Figma file.

## Objective

Build one documentation frame per component set, inside the file that holds the
component, covering what the component is, how to use it, how it behaves and how
it is built. The frame in Figma is the deliverable.

## Context

Do not document from memory or from a screenshot alone. Read the component with
the Figma MCP tools before writing anything: `get_design_context` for structure,
properties and styling, `get_metadata` for the layer tree and nested instances,
`get_screenshot` to confirm what it looks like, `search_design_system` and
`get_variable_defs` for the type, spacing, colour and radius scales the doc itself
will use. Interaction behaviour, intended use, edge cases, category and status are
usually not in the file: ask the user rather than inventing them.

## Constraints

- Search the file for an existing frame named `Docs / [Component name]` first. If
  one exists, edit it in place, keep its node ID, update only what changed, and do
  not leave the old version beside the new one. Two docs for one component is
  worse than one out-of-date doc.
- Never state a measurement, ratio, property value or variable name you have not
  read from the file. Where you inferred something, say so in the handover.
- Use the file's own names for properties, parts and states, exactly as spelled,
  not tidied-up versions.
- Cover every property in the set, including booleans, text and instance-swap
  properties, and every state. Nothing summarised, nothing dropped as "and so on".
- Bind every typography, spacing, colour and radius value in the doc to a
  variable. Resolve the scales fresh each run rather than reusing a map from a
  previous doc.
- Calculate contrast from resolved hex values, one row per theme mode, naming the
  background measured against. Quote to two decimal places. Mark a row unmeasured
  rather than guessing.
- Use live instances throughout, not exported images.
- Default to the shortest version that lets someone use the component correctly
  without opening the file: one or two sentences per section. Go deeper only where
  the component earns it. Leave optional sections out entirely if they have
  nothing to say.
- Write gaps in place, saying why the row is empty and what closes it. Do not
  leave a blank and do not drop the row.
- Category is one of four: Assets, Form Elements, Content Presentation,
  Navigation. The list is closed. Ask rather than inventing a fifth or picking the
  nearest fit.
- Take status from wherever the system records it. If nothing records it, say so
  in the handover rather than inferring one from how finished the component looks.
  Version is `v1.0` on the first doc, carried forward after that, raised only when
  the user says so.
- Plain, specific words. UK English. Active voice. Short sentences. Instructions
  rather than descriptions. No filler. No em dashes.
- Do not deliver the documentation as chat text, a markdown file or an artefact.
  If `use_figma` fails or you cannot write to the file, say so plainly and hand
  over the draft as an interim.

## Output format

1. A short inventory, before drafting: property names and values, variants,
   states, nested components. This is the factual base for the doc.
2. A list of anything the file does not answer, put to the user as questions.
3. The doc frame, built with `use_figma` in the same file and on the same page as
   the component, to the right of the component set, named
   `Docs / [Component name]`. Vertical auto-layout, hug height, 1024px wide, or
   1200px only if a table would otherwise crush its columns. Order: category with
   status and version on the same row, title, summary, links bar, component
   preview, then the sections separated by divider instances.
4. The sections, in this order: When to use, Anatomy, Variants and states, Usage
   guidelines, Do's and don'ts, Accessibility considerations, Nested components.
   Optional sections (Content, Overflow, Hierarchy, In-context examples) sit after
   Usage guidelines, and only when the component has something real to say.
5. Every subsection uses the same three-part shape: the name as a subheading, then
   a visual in a fixed-height container showing every value side by side, then the
   detail as a table or prose. Visual before table.
6. Handover: the node link to the frame, the filled variable map you used for this
   run, and every claim you could not verify from the file, so the user knows
   exactly what to check.

## Before it goes out

- Open the component set beside the doc and check the properties table against it
  property by property, including the booleans and instance-swap properties. A
  missing row is the failure that looks like a finished doc.
- Recalculate at least one contrast ratio yourself from the resolved hex values.
- Confirm behaviour, placement and intended-use claims came from a person, not
  from the model.
- Confirm there is only one `Docs /` frame for this component.

This output is a draft for review, never a published doc on its own.
