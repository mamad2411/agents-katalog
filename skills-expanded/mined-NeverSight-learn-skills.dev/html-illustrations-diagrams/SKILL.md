---
name: html-illustrations-diagrams
description: "Use when the output is primarily a self-contained HTML figure sheet, inline SVG illustration set, annotated flowchart, process map, or lightweight diagram."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [html, artifacts, visualization]
    related_skills: [html-artifact-foundation, architecture-diagram, excalidraw, baoyu-infographic]
---

# HTML Illustrations and Diagrams

## Overview

This skill creates self-contained HTML artifacts for figure sheets and lightweight diagrams inside HTML. It builds on `html-artifact-foundation`: keep the shared single-file, accessibility, responsive, print, attribution, and verification rules centralized there, and use this skill for the category-specific structure.

For diagrams and diagram-like visualizations, inherit the foundation default: Catppuccin Mocha dark theme unless the user asks otherwise.

Local examples: `examples/10-svg-illustrations.html`, `examples/13-flowchart-diagram.html`. The guidance below distills reusable patterns; copied examples preserve the upstream Apache-2.0 notice.

## When to Use

Use this skill when:
- the deliverable is a figure sheet, concept illustration, process map, or annotated flowchart
- inline SVG plus explanatory text is more useful than a standalone image
- diagram elements need legends, annotations, or copyable SVG snippets
- a lightweight HTML diagram is preferable to `.excalidraw`, `.pptx`, or a production asset

Do not use this skill when a plain markdown answer is enough, when the requested deliverable is a production app implementation, or when a more specialized peer skill is a better fit.

## Inputs to Gather

Use the foundation input checklist first. Additionally gather:

- subject, diagram scope, entities, relationships, sequence, and terminology
- required legend semantics: colors, line styles, shapes, annotations
- whether individual SVG figures need copy/export buttons
- any source architecture/process evidence the diagram must faithfully represent

Evidence gate: do not render factual claims until you have the underlying source, or label the panel as an assumption/draft.

## Relationship to Other Skills

Use `architecture-diagram` for dark themed software/cloud architecture diagrams and `excalidraw` for hand-drawn editable `.excalidraw` files. Use this skill for HTML-native figure sheets, inline SVG illustration sets, annotated flowcharts, legends, and copyable SVG regions.

## Artifact Anatomy

- Figure sheet with repeated SVG specimens, captions, and usage notes.
- Annotated flowchart with step details next to or below the graphic.
- Legend mapping colors, line styles, node shapes, and severity/status labels.
- Copyable SVG regions when users may reuse individual figures.
- Textual summary of the diagram for accessibility and narrow screens.
- Source/evidence panel if the diagram represents real architecture or process data.

## Implementation Workflow

1. Apply `html-artifact-foundation` for document skeleton, accessibility, responsive, print, attribution, and verification rules.
2. Gather the category-specific inputs above and write a short evidence list before composing the page.
3. Choose one primary artifact type from this skill; avoid mixing every pattern into one page.
4. Build the category-specific anatomy below with semantic sections and CSS variables.
5. Add JavaScript only for the category-specific interaction/export/navigation behavior described here.
6. Verify using the foundation checklist plus the category-specific checklist below.

## Prompt Template

```text
Create a self-contained HTML artifact for: [goal].
Audience: [reader/operator].
Source evidence to use: [files, diffs, notes, data, screenshots].
Artifact type: [choose one from this skill].
Must show: [required sections or states].
Interaction/export needs: [tabs, filters, copy JSON, keyboard deck, none].
Constraints: single local HTML file; embedded CSS/JS only; semantic HTML; accessible controls; responsive layout; no unsupported claims.
Verification: save to [path], run static checks, and if interactive open locally and check console errors.
```

## HTML/CSS/JS Patterns

Inline SVG should use a `viewBox`, descriptive `<title>`, consistent coordinate system, and CSS variables for colors. Draw connectors behind nodes. Use markers for arrowheads and keep labels large enough to read. For copyable SVG, place the source in a `<textarea>` or generate it from a known string and provide a copy button.

## Verification Checklist

- [ ] Foundation checklist passed: complete HTML document, accessibility basics, responsive behavior, and appropriate print/export behavior.
- [ ] Category trigger fits this skill and the relationship notes above rule out a better peer skill.
- [ ] Category-specific source evidence was gathered before rendering factual content.
- [ ] Artifact anatomy includes the required category sections and omits irrelevant decorative panels.
- [ ] Any category-specific JavaScript interaction/export/navigation works and has no console errors.
- [ ] Factual claims are tied to source notes or labeled assumptions.

## Common Pitfalls

- Duplicating the foundation skill instead of keeping this category focused.
- Creating an attractive but unsupported artifact with invented data.
- Adding controls that do not change anything meaningful.
- Letting dense layouts become unreadable on narrow screens.
- Recreating what `architecture-diagram` or `excalidraw` already does better. Use this for HTML-native annotated figure sheets and lightweight flowcharts.
- Tiny SVG labels that look fine in source but fail visually.
- Omitting a legend for color/shape semantics.
