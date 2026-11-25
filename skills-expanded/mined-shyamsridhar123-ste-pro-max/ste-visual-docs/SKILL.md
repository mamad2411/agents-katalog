---
name: ste-visual-docs
description: "Author source-grounded diagrams, charts, and interactive technical explanations with native STE or host tools and standalone HTML/SVG templates. Preserve readable text/data equivalents; not for decorative artwork or a prose-only rewrite."
---

# STE visual documentation

Produce a focused explanation from reviewed facts. Use native STE authoring tools
for automatic checks or the host's normal tools. See
[native checks](../ste-promax/references/automatic-policy.md); this skill does not
restrict other tools or require a session switch.

## Choose and ground the visual

Identify the reader, the question, and what the source actually establishes.
Use a flow for relationships, a sequence for message order, and a bar/line chart
for quantities. Keep the user's requested format; do not build an application
where a diagram and short explanation suffice.

Read [the example guide](../../examples/showcase/README.md) for starters, and
[STE-ProMAX](../ste-promax/SKILL.md) for writing rules when revising prose.
For multiple evidence-linked beats, use
[ste-storytelling](../ste-storytelling/SKILL.md), not a second rendering engine.
For an original isometric figure, inspectable parts, or a paced interactive SVG
explanation, use [STE Line Studio](../ste-line-studio/SKILL.md). Its JavaScript
primitives are bundled locally; no additional plugin or package install is needed.

- Keep units, baselines, populations, dates, and uncertainty attached to the data.
  Label illustrative or simulated material. Never fill an evidence gap with an
  invented relationship, measurement, benefit, or causal arrow.
- Sequence spacing means order, not duration. Chart categories are equally
  spaced, not a continuous time scale. State these limits when timing matters.
- Represent missing values with `null`, not zero. Supply uncertainty bounds only
  from the source; explain what they measure. Do not compute an interval or
  confidence level merely because the renderer supports one.
- Label the visual meaningfully and inspect its complete text/data equivalent.
  Color or dashed styling alone must not carry a qualification.
- Review framing: selection, exclusions, ordering, axis limits, labels, and
  annotations can change the apparent conclusion. Disclose material choices.

## Author with the installed plugin

Resolve the plugin root from this loaded `SKILL.md`. Read the nearest
[showcase guide](../../examples/showcase/README.md) and the relevant standalone
HTML starter. Adapt its inline CSS/SVG/JavaScript using `ste_write_artifact` or
the host's ordinary authoring tools.
Write new output to a fresh directory in the user's workspace, never the plugin
cache. The starter is source code, not a command that installs dependencies.

Keep the visual and readable text/data equivalent together. Use SVG for labeled
relationships or quantities; make controls native buttons/inputs. Preserve
keyboard operation, reduced motion, no-JavaScript/print reading, and visible
scope. Use local assets and inline styles/scripts unless external assets are
explicitly requested. Escape source text; do not execute source-supplied HTML.

Follow [the shared low-friction workflow](../ste-promax/references/low-friction-workflow.md).
Choose the simplest faithful visual yourself. Do not ask the user to choose
internal schema names, file paths, themes, or renderer options. Preserve the
requested medium, and ask only when a missing fact or ambiguity affects meaning.

The native engine offers deterministic validated shapes for structured rendering.
Its commands and prerequisites are in [Authoring](../../docs/AUTHORING.md).
Native operations, including `ste_write_artifact`, run automatic checks. Other
tools do not gain those checks from skill loading. Do not silently run a bootstrap
when capability is missing or claim renderer schema validation for a document
that the renderer did not produce.

## Inspect before delivery

1. Preserve the supplied source next to the output. Inspect the actual rendered
   labels and text/data equivalent. If the optional engine was used, read its
   manifest, warnings, and hashes too; otherwise do not invent those checks.
2. Check every node, edge, message, category, value, interval, and qualification.
   A valid reference or number is not proof that the source supports the claim.
3. Exercise desktop and narrow-width output, keyboard access to scroll regions,
   noncolor distinctions, and readable long labels. Record browser or assistive
   technology checks not performed; do not infer them from static markup.
4. Return the artifact and material gaps. Separate successful rendering, design
   lint, factual review, accessibility checks, and any learning evaluation.

Stop when the requested visual is source-faithful and the checks are recorded,
or report the specific blocker. Do not install globally or publish by default.
