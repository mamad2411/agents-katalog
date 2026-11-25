---
name: ste-line-studio
description: "Create original line-art SVG figures and reader-controlled HTML explanations from source material. Use for interactive isometric figures, mechanism walkthroughs, or custom visual intuition; preserve the requested medium rather than turning prose into a demo."
---

# STE Line Studio

Make a mechanism understandable through original figures, not decorative motion.
This fourth native STE skill is included in **v0.5.0**.
The published skill targets host-native authoring in Copilot CLI, Claude Code,
and Codex. Native STE tool adapters target Copilot CLI and OpenCode; see
[their checks](../ste-promax/references/automatic-policy.md). They do not restrict
ordinary host tools.
This file is not evidence of installation or runtime verification.

## Start with the explanation

Identify the reader's question, the source-supported relationship, and one
misunderstanding the figure should resolve. Preserve facts, attribution, units,
uncertainty, and assumptions. Label illustrative models visibly.

Honor the requested medium. Keep a prose answer as prose, a still as SVG, and an
interactive explanation as HTML. Do not add video, an application, or a catalogue
of patterns merely because they are possible.

For intuition-led work, establish one concrete case, show the meaningful
intermediate states, then generalize. Let readers predict, inspect, and compare.
Use motion only to connect those states; every resting state must explain
something without playback. Quality comes from the explanation, not resemblance
to another creator's artwork.

## Author locally

Read [the authoring reference](references/authoring.md) before adapting a figure.
Resolve the plugin root from this skill's location, not the working directory.
Read the selected template and its source before editing:

- [Retry Observatory](../../examples/showcase/retry-observatory.html) is the
  flagship explanation; [its source](../../examples/showcase/sources/retry-storm.json)
  defines the arithmetic and limits.
- [Line Studio](../../examples/showcase/line-studio.html) demonstrates six
  reusable patterns, not six limits on what can be explained.
- [Token bucket mechanism](../../examples/showcase/token-bucket-mechanism.html)
  builds a concept as a small working object. Read
  [mechanism figures](references/mechanism-figures.md) before adapting it.

Use `ste_write_artifact` or ordinary authoring tools to adapt HTML/SVG into a
fresh `artifacts/` subdirectory in the user's workspace. Preserve the supplied
source and a normalized source copy beside the result. Never edit the plugin
cache, overwrite source files, or execute source-provided HTML/scripts.

The standalone output requires no npm, React, server, or provider key. Native STE
checks require the configured SkillC runtime; ordinary host-tool authoring does not.
Use inline/local assets with no external traffic.
Do not install missing tooling or publish output as a workaround. If a bundled
asset is absent, report that specific gap rather than inventing a shipped feature.

Adapt primitives and templates into custom original figures when the explanation
needs them. The six patterns are starting points, not a mandatory toy demo.
There is no Hairline API or React parity promise.

## Check and deliver

- Verify the source-to-figure mapping, arithmetic, labels, and visible limits.
  For the retry model, total attempts include the initial attempt: nested
  budgets give `A^L`; one owner gives `A`, not `A*L`.
- Exercise stable hit targets, visible keyboard focus, keyboard/touch-equivalent
  controls, narrow layouts, light/dark themes, and reduced motion. Provide pause
  and scrubbing for authored playback; keep a static/no-JS and print reading path.
- Inspect the actual artifact in the available browser. Static SVG export captures
  the current state; it is not an animation or video export.
- Return the artifact and material limits. Separate source review, structural
  validation, browser checks, and untested behavior; never imply they ran merely
  because a template or skill describes them.

See [the feature guide](../../docs/LINE_STUDIO.md) for scope and examples.
Stop when the requested explanation is delivered with evidence-backed checks,
or state the precise remaining blocker.
