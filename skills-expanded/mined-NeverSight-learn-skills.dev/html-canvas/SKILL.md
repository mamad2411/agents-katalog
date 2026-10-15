---
name: html-canvas
description: Generate a rich, self-contained HTML artifact for specs, code reviews, designs, reports, or custom editors. Use when the user asks for an "HTML file/artifact/explainer/report/playground", wants a shareable visual deliverable instead of markdown, or asks to "make a canvas/dashboard/diagram-heavy doc". Trigger phrases include "make an HTML", "html artifact", "html canvas", "html report", "html explainer", "html playground", "visual spec", "html mockup".
arguments: [mode, topic, output_path, language]
argument-hint: "[spec|code-review|design|report|editor] [topic] [output_path] [language]"
---

# html-canvas

Produce a single, self-contained HTML artifact tailored to one of five archetype use-cases. Inspired by Thariq's "Unreasonable Effectiveness of HTML" — HTML is denser, more readable, more shareable, and supports two-way interaction in a way markdown cannot.

## When to use

| Mode | Use when the user wants… |
|---|---|
| `spec` | Brainstorming, comparing approaches, or an implementation plan with mockups. |
| `code-review` | A PR walkthrough, annotated diff, or focused review of a code area. |
| `design` | Visual designs, component prototypes, animation tuning, or design-system artifacts. |
| `report` | An explainer, research summary, status report, or technical deep-dive. |
| `editor` | A throwaway purpose-built UI to triage/edit/tune data, ending with an export. |

If the user asks for something HTML-shaped that doesn't clearly map to one of these, ask which mode fits or pick the closest and tell them.

## Parameters

### Positional (declared in `arguments`)

These can be passed as slash-command args (`/html-canvas $mode $topic $output_path $language`) or extracted from natural language. They map to `$mode`, `$topic`, `$output_path`, and `$language` in this skill's logic, with `$ARGUMENTS` holding the full raw string.

- `$mode` (required) — one of `spec` | `code-review` | `design` | `report` | `editor`.
- `$topic` (required) — what the artifact is about (free text). Quote it if it contains spaces: `/html-canvas report "rate limiter explainer"`.
- `$output_path` (optional) — absolute path to write the HTML file. Default `./<slug>.html` derived from `$topic` if omitted. If the third positional value looks like a language name or locale tag rather than a path, treat it as `$language` and derive the output path.
- `$language` (optional) — output language for human-readable artifact text such as headings, labels, annotations, explanations, and export copy. Accept plain names or locale tags (`English`, `Chinese`, `zh-CN`). Default to the user's requested language, or preserve the existing artifact language when revising. Do not translate code identifiers, diffs, API names, file paths, logs, or literal source excerpts unless the user explicitly asks.

### Additional (free-form, ask if missing)

These aren't positional — extract them from the user's message or ask:

- `sources` — list of files, directories, URLs, browser context, or MCP queries to ingest as context. Start here, then follow the mode-specific source discovery rules below.
- `design_reference` — path to an existing HTML file whose visual style should be matched.
- `interaction_level` — one of `auto` | `none` | `light` | `full`. Defaults to `auto`; see `references/modes.md` for per-mode defaults. `light` means navigation/filtering/copy affordances. `full` means direct manipulation, forms, sliders, live previews, or other stateful controls.
- `open_after` — boolean. When true, run `open <output_path>` after writing.

### Source discovery by mode

Use the user's named sources first, then expand just enough to make the artifact truthful:

| Mode | Gather before writing |
|---|---|
| `spec` | Related code paths, product docs, prior implementations, relevant design references, and any tests that reveal current behavior. |
| `code-review` | `git diff`, recent `git log`, touched-file context, nearby tests, and any named focus area. Render the actual diff, not a paraphrase. |
| `design` | Existing design tokens, component implementations, CSS/theme files, screenshots or HTML references, and nearby interaction patterns. |
| `report` | Relevant code, docs, git history, URLs, cited source files, and MCP/browser context when provided. Include a short source brief or citations when possible. |
| `editor` | The real data/config/transcript/diff first. Parse it, infer constraints and dependencies, and preserve the export shape the user needs back. |

### Revising existing artifacts

If the user asks to edit/update/revise an artifact, or if `$output_path` already exists, read the existing HTML before changing it. Preserve the visual system, CSS variables, anchors, working JavaScript, copy/export buttons, and user-facing interaction model. Patch the targeted sections instead of regenerating from scratch unless the user explicitly asks for a rewrite or the current file is too broken to repair.

### Invocation examples

Good invocations describe the artifact shape, source context, interaction model, and export affordance:

```
/html-canvas spec "onboarding screen: 6 distinct approaches in one comparison grid, varying layout/tone/density and labeling each tradeoff" ./onboarding-variants.html
/html-canvas spec "implementation plan for the checkout rewrite with mockups, data-flow diagram, and key code snippets to review" ./checkout-plan.html
/html-canvas code-review "PR review focused on streaming/backpressure: render the actual diff with inline margin annotations and severity-colored findings" ./streaming-review.html
/html-canvas design "checkout button animation playground with sliders/options, live preview, quick purple transition, and copy-parameters button" ./checkout-button-playground.html
/html-canvas report "rate limiter explainer from the relevant code: token-bucket diagram, 3-4 annotated snippets, and gotchas optimized for one read" ./rate-limiter.html zh-CN
/html-canvas editor "30 Linear tickets as draggable Now/Next/Later/Cut cards, pre-sorted with rationale and copy-as-markdown export" ./linear-prioritizer.html
/html-canvas editor "feature flag config editor grouped by area, showing dependencies, prerequisite warnings, and copy-diff for changed keys" ./feature-flags.html
/html-canvas editor "system prompt tuner with editable template, highlighted variables, 3 live sample renders, token counter, and copy button" ./prompt-tuner.html
```

Natural-language form also works — the skill is triggered by the description's phrases and the parameters are inferred from the message:

```
Make a single HTML explainer for our rate limiter. Read the relevant code, show the token-bucket flow, annotate the key snippets, and add gotchas at the bottom.
Create an HTML artifact for this PR review. I am unfamiliar with streaming/backpressure, so render the actual diff with margin notes and severity-coded findings.
Build an HTML editor for these feature flags. Group by area, warn on broken prerequisites, add a copy-diff button for changed keys, and write the artifact in Chinese.
```

## Workflow

1. **Resolve `$mode`.** If missing or not one of the five values, ask the user before doing anything else. (Slash invocation: `$0` / `$mode`.)
2. **Resolve `$topic`.** If missing, ask. (Slash invocation: `$1` / `$topic`.)
3. **Resolve `$output_path`.** If missing, derive a slug from `$topic` and write to `./<slug>.html`. If `$2` looks like a language name or locale tag rather than a path, treat it as `$language` and derive the path. (Slash invocation: `$2` / `$output_path`.)
4. **Resolve `$language`.** If missing, infer it from the user's request; when revising an existing artifact, preserve the artifact's current language unless the user requests a change. (Slash invocation: `$3` / `$language`, or `$2` when output path is omitted.)
5. **Check for revision.** If the request is an edit/revision or `$output_path` exists, read the current artifact and plan a targeted patch that preserves working behavior.
6. **Ingest sources.** Read files, fetch URLs (WebFetch), run MCP queries, and inspect browser context as specified. Follow the source discovery table above for the chosen mode.
7. **Load design.** If `design_reference` is given, read it and extract palette, typography, spacing, component styles. Otherwise use `references/design-defaults.md` (the warm earth-tone editorial style).
8. **Load mode checklist.** Read `references/modes.md` for the chosen mode and follow its must-haves, interaction default, and visual patterns.
9. **Read canonical example(s).** From `references/examples/`, read at least one example file matching the chosen mode (each mode in `modes.md` lists 3–7 examples). These are ground-truth for layout, class names, SVG patterns, and JS idioms — match them before improvising.
10. **Generate or revise.** Write a single self-contained HTML file to `$output_path` using `$language` for human-readable artifact text. Inline all CSS and JS; no build step. CDN libs (D3, Mermaid, Highlight.js) are allowed when they meaningfully improve the result, but the file must still degrade gracefully offline.
11. **Verify.** Open/render the HTML with browser tooling when available. Check desktop and mobile widths, console errors, horizontal overflow, diagram scaling, and core interactions such as tabs, filters, sliders, drag, and copy/export buttons. If browser tooling is unavailable, do a static QA pass and tell the user verification was limited.
12. **Open.** If `open_after` and the file is not already open from verification, run `open $output_path`.

## Constraints

- **Single file.** Inline CSS and JS. No bundlers. No external local assets.
- **Offline-friendly.** If you use a CDN lib, the document's primary content must still be readable without it.
- **Mobile-responsive.** Use sensible breakpoints; avoid fixed widths.
- **Interactive exports.** Whenever the artifact accepts user input or supports a meaningful selection/filter state, include a button that copies the resulting state as prompt/JSON/markdown so the user can paste it back into Claude Code.
- **Verified output.** Treat visual QA as part of the artifact, not an optional polish pass. Prefer real browser checks; fall back to static inspection only when tooling is unavailable.
- **Don't pad.** Match length to content. A 200-line report is fine; a 2000-line report nobody reads is not.
- **Taste over templates.** Don't ship boilerplate sections that aren't earned by the content.

## References

- `references/modes.md` — per-mode must-haves, visual patterns, example prompts, and pointers to canonical example files.
- `references/design-defaults.md` — default visual identity (warm earth-tone editorial style: clay/olive/slate/oat palette, serif headings + system sans, 1.5px borders, 12–14px radius, soft hover shadows). Used unless `design_reference` overrides.
- `references/examples/*.html` — 20 canonical example artifacts covering all 5 modes. Read the matching mode's examples before generating.
