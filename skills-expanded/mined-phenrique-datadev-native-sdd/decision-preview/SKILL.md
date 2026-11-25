---
name: decision-preview
description: Generate a single self-contained Artifact that compares 2-4 variants of an as-yet-undecided design choice side by side, grounded in real project data, and closes with an explicit choice question. Use when a decision has multiple viable options and getting it wrong after implementing would be costly to redo — a UI copy choice, a terminal/CLI output design, a schema layout, a component variant, an architecture option. Not for explaining or reviewing something already decided (use visual-explainer for that) or for a single mockup with no comparison (use artifact-design directly).
argument-hint: "<a decisão + as variantes a comparar>"
metadata:
  maintained_by: native-sdd (internal — not a third-party marketplace skill)
  version: "1.0.0"
---

# Decision Preview

Generate **one** Artifact that lets someone **choose before building**, instead of implementing
the first option that comes to mind. The output is always the same shape regardless of domain:
**N variants side by side, each grounded in real project data, each annotated, closing with an
explicit choice.**

**Explicit trigger:** `/decision-preview <a decisão + as variantes>` runs this skill directly (a skill wins over a same-name command, so there is no `commands/decision-preview.md`). The decision and variants come from the arguments; **if fewer than 2 variants come in, ask before generating.**

## When to use

Use this skill when:
- The decision has **2–4 viable options**, none obviously correct.
- Getting it wrong is **expensive to redo** after implementation (not a one-line revert).
- The difference between options is **easier to show than to describe**.

Don't use this skill for:
- Explaining or reviewing something **already decided** (a diff, a finished plan, an existing
  architecture) — that's `visual-explainer`, if installed.
- A **single** mockup with nothing to compare — that's `artifact-design` directly.
- More than ~4 options — narrow it down first; a wall of variants defeats the point.

[`../../rules/artifact-first.md`](../../rules/artifact-first.md) is the always-on predicate that
decides *when* to reach for this skill; everything else about the posture lives here.

## Routing — which tool fits

| Situation | Use | Why |
|-----------|-----|-----|
| Compare **N undecided variants** and have the user pick one | **this skill** | the gap no other skill covers: compare + choose before building |
| Explain/review something **already decided** (diff, plan, finished architecture) | `visual-explainer` (if installed) | already solved — don't duplicate it |
| **One** mockup, nothing to compare | `artifact-design` directly | design guidance for an Artifact; no "variants + choice" layer needed |
| Chart or data table | `dataviz` (if installed) | its own domain, outside this posture |

## Workflow

1. **Load `artifact-design`** first — it carries the design calibration (aesthetic direction,
   anti-slop rules, accessibility) this skill builds on. Don't re-derive that guidance here.
2. **Name the variants** — 2 to 4, each a genuinely distinct answer to the same question (not
   minor tweaks of one idea, unless the tweak *is* the decision).
3. **Ground every variant in real data.** Read the actual theme tokens / copy / schema / code the
   project already has. **Never** fabricate placeholder content (no lorem ipsum, no invented
   colors, no hypothetical data) — if the real input is missing, ask for it before generating.
   Anything unavoidably hypothetical must be labeled `[hipotético]` inline.
4. **Read `./templates/base.html`** before writing — don't reimplement its layout from memory each
   time. Adapt the variant-card structure and the closing choice section to the content at hand;
   the example content in it is illustrative only, replace it.
5. **Annotate each variant** — a short line on what it optimizes for / trades off, not just the
   raw rendering. The annotation is what turns "here are 3 things" into "here's how to decide".
6. **Close with an explicit choice**, not a vague "let me know what you think":
   - Interactive session → publish the Artifact, then ask via `AskUserQuestion` referencing it.
   - Non-interactive (background agent/workflow) → the HTML's own "Escolha" section must stand on
     its own for async review — don't rely solely on the chat-turn question.
7. **Publish via the `Artifact` tool** when the session has it (see below when it doesn't). One
   artifact, all variants — not one artifact per variant. Follow the tool's own constraints: no
   `<!DOCTYPE>`/`<html>`/`<head>`/`<body>` tags (the wrapper adds those), self-contained CSS/JS,
   theme-aware for both light and dark.
8. **The chosen variant becomes the spec** — only then implement.

## Without the `Artifact` tool

Check your tool list before step 7. The tool is not always there: in headless runs (`claude -p`) it
does not exist even in the main session (measured in v0.11.10), and an account or a subagent may
lack it too. Then don't pretend it published:

1. Wrap the same page in `<!doctype html><meta charset="utf-8"><meta name="viewport"
   content="width=device-width,initial-scale=1">` (the Artifact wrapper used to add that) and save it
   as `.claude/sdd/features/DECISION_<slug>.html`.
2. Say that the Artifact was **not** published, give the file path, and ask for the choice
   (`AskUserQuestion` when interactive; the page's own "Escolha" section otherwise).

## Red flags

| Red flag | What it means |
|----------|---------------|
| Offered the comparison for renaming a variable or fixing a typo | Needless friction — the decision was trivial |
| Used this skill to review a finished diff | Should have routed to `visual-explainer` — redundancy |
| Implemented the "obvious" variant without showing the others when ≥ 2 were viable | Lost the point: the difference shows when looking, not when deciding alone |
| Filled a variant with invented or placeholder data | Breaks the "never invent data" rule — ask for the real grounding first |
| Said "published" in a session without the `Artifact` tool | False report — save the local file and say so |

## Anti-patterns (explicitly forbidden)

- Filling a variant with generic/placeholder content because the real grounding wasn't at hand.
- More than ~4 variants in one page — split the decision instead.
- Rendering variants without an annotation (just N boxes, no "why").
- Ending without a concrete choice mechanism (no question, no "Escolha" section).
- Rebuilding what `visual-explainer` already does (diff review, plan review, slide decks,
  architecture explainers) — if the task is "explain/review something decided", route there
  instead.
- Reusing this skill for a single mockup — if there's nothing to compare, `artifact-design` alone
  is enough.

## Template

`./templates/base.html` is a self-contained, theme-aware (light/dark) skeleton with:
- A header slot for the decision being made (1 sentence — what's being decided and why).
- A responsive variant grid (2–4 cards), each with a content slot + an annotation slot. The
  content slot comes in two shapes: `.dp-content` for text/code/schema and `.dp-shots` for UI
  variants, one `<figure>` per width with the calibrated PNG from the `visual-check` skill as a
  `data:` URI.
- A `<title>` and the theme/gutter rules the `Artifact` tool requires today (tokens on `:root`,
  explicit `body` background, safe-area side padding). Replace the title with the decision's name.
- A closing "Escolha" section with the explicit question and the options to pick from.

It has no external dependencies (inline CSS only, CSP-safe) — read it, then adapt the slots to the
actual content; don't ship it unmodified, and don't carry its example content into the real output.
