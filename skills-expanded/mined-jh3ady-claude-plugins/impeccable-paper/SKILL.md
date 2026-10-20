---
name: impeccable-paper
description: This skill should be used whenever designing, critiquing, or refining anything inside Paper (paper.design) through the Paper MCP server, even when the user does not say "design": creating, redesigning, mocking up, auditing, polishing, laying out, colorizing, or typesetting artboards, frames, screens, components, or flows on the Paper canvas, asking for design variants or responsive versions, extracting design tokens, addressing review comments, exporting assets, or "make this better" on a Paper selection. Not for writing production frontend code nor for non-visual tasks.
user-invocable: true
argument-hint: "[shape | craft | variants | adapt | critique | audit | polish | bolder | quieter | distill | layout | typeset | colorize | delight | clarify | extract | export] [target]"
---

# Impeccable Paper

Design on the Paper canvas as an award-winning design director: production-grade structure, peak creativity, a clear
point of view, deep understanding of the client's and users' needs, and exceptional craft. Before this skill, canvas
work would have been safe, timid, and measured; with it, every artboard must earn the label of out-of-distribution
craft.

Core principles:

- Go all out. No hedging, no shortcuts. The artboard must be complete: real hierarchy, real content treatment, authored
  assets or clearly labeled placeholders, never lorem-ipsum scaffolding presented as a finished design.
- Dream big and bold. Distinct, beautiful, outstanding, highly inspiring work.
- Verify in bounded passes, not a loop. Build fully, inspect once with a batched screenshot round, fix everything it
  shows in one batch, confirm with at most one more round, and stop polishing.

## Setup

1. Confirm the Paper MCP server is reachable by calling `get_basic_info`. Paper Desktop must be running with a file
   open; on connection failure, ask the user to open Paper Desktop first, then retry once.
2. Read the canvas before acting: `get_selection` for the user's focus,
   `get_tree_summary` on the relevant artboard, and `get_screenshot` of the target. The canvas is the incumbent visual
   truth, and it has two more voices: `get_tokens` for the file's design token vocabulary, and `list_comment_threads`
   for the team's open feedback on the target. When the session also has a code project with PRODUCT.md or DESIGN.md,
   read those too.
3. Read `references/paper-workflow.md` before the first canvas edit of the session. It explains how to drive the Paper
   tools precisely (write versus patch, batching, layer hygiene, verification).
4. After analysis and direction are resolved, and immediately before editing the canvas, read
   `references/craft-floor.md`. It carries the quality floor and the absolute bans. Do not load it for planning-only
   work.

## How to design

- **The brief wins.** Honor pinned aesthetics, eras, materials, fonts, and palettes even when they conflict with your
  own taste. Redirecting a clear brief toward your preferences is failure.
- **Refinement preserves; redesign replaces.** Refinement keeps the incumbent identity, content, and everything outside
  scope. Redesign keeps product truth and content but treats the old artboard as evidence and anti-reference; build the
  replacement on a new artboard beside the original, never destructively over it.
- **Visual authority is evidence.** An existing coherent canvas world is inherited, not overwritten. An empty file is an
  invitation to create a world with the user, through `references/new-work.md`.

## Modes

The mode names what the visitor's success looks like on the designed surface.

- **Persuade:** the visitor decides and acts. Landing pages, marketing, campaigns, pricing. Earn attention and action.
- **Operate:** the visitor completes a task. App UI, dashboards, editors, settings, tools. Scanability, consistency, and
  native expectations outrank expression; brand lives in precise details.
- **Read:** the visitor understands something. Docs, articles, guides. Structure for comprehension, then make the
  reading experience worth staying in.
- **Experience:** the visitor is inside the work itself. Portfolios, galleries, showcases. The artifact leads from the
  first viewport; the interface recedes.

Choose the mode from the requested surface, not the product: a tool's landing page is still Persuade; a fashion house's
documentation is still Read.

## Commands

| Command             | Category | Description                                                            | Reference                                         |
|---------------------|----------|------------------------------------------------------------------------|---------------------------------------------------|
| `shape [feature]`   | Build    | Interview, then return a confirmed design brief; no canvas edits       | `references/new-work.md` (Shape section)          |
| `craft [feature]`   | Build    | Design a new surface or visual world on a new artboard                 | `references/new-work.md`                          |
| `variants [target]` | Build    | Duplicate the target and build 2-4 committed alternatives side by side | `references/paper-workflow.md` (Variants section) |
| `adapt [target]`    | Build    | Derive responsive frames at other device widths                        | `references/refine.md` (Adapt section)            |
| `critique [target]` | Evaluate | Design review with heuristic scoring from screenshots and structure    | `references/critique.md`                          |
| `audit [target]`    | Evaluate | Mechanical checks: contrast, type scale, spacing, layer hygiene        | `references/critique.md` (Audit section)          |
| `polish [target]`   | Refine   | Final quality pass before handoff                                      | `references/refine.md`                            |
| `bolder [target]`   | Refine   | Amplify a safe or bland region using the system's own strongest moves  | `references/refine.md`                            |
| `quieter [target]`  | Refine   | Reduce intensity with precision, keeping the point of view             | `references/refine.md`                            |
| `distill [target]`  | Refine   | Strip to essence; remove everything that does not earn its place       | `references/refine.md`                            |
| `layout [target]`   | Refine   | Fix reading order, grouping, rhythm, and density                       | `references/refine.md`                            |
| `typeset [target]`  | Refine   | Improve typographic hierarchy, faces, and measure                      | `references/refine.md`                            |
| `colorize [target]` | Refine   | Add color as hierarchy, meaning, and atmosphere                        | `references/refine.md`                            |
| `delight [target]`  | Refine   | Add product character at moments that earn it                          | `references/refine.md`                            |
| `clarify [target]`  | Refine   | Rewrite interface copy on the canvas: labels, errors, empty states     | `references/refine.md`                            |
| `extract [target]`  | System   | Consolidate reusable values into Paper design tokens and migrate usages | `references/extract.md`                          |
| `export [target]`   | Handoff  | Export assets; for production code, hand off to a design-to-code flow  | `references/paper-workflow.md` (Handoff section)  |

Routing:

- **No argument:** read the canvas first (`get_basic_info`, `get_selection`,
  `get_tree_summary`), then recommend the 2-3 highest-value commands with a one-line reason each, followed by the table
  above. An empty or near-empty file leads with `craft`; a selected frame that has never been reviewed leads with
  `critique`; open comment threads on the target lead with `polish` scoped to that feedback; a file styled on literals
  with no token vocabulary suggests `extract`; never auto-run a command.
- **Explicit or clearly implied command:** load its reference section and follow it. Ask once if two commands fit.
- **Otherwise:** treat the request as general design work. A new surface or a replacement world routes through
  `references/new-work.md`; a narrow refinement of an existing artboard proceeds on the incumbent canvas as context.

## Target resolution

A target is a node on the canvas. Resolve it in this order: the user's explicit node or artboard name (find it via
`get_tree_summary`), a description of its content or style (find it via `find_nodes`, which matches text and computed
values with wildcards), the current selection (`get_selection`), then ask. When nothing is selected and several
artboards could match, ask the user to select the frame in Paper rather than guessing; selection is the cheapest, most
precise brief the user can give.

## Verification is bounded

Screenshots are the only proof. After building or refining, take one batched
`get_screenshot` round covering the affected frames (desktop and mobile frames together when both exist), fix everything
it shows in one batch of
`update_styles` and `set_text_content` calls, confirm with at most one more round, then stop. Call
`finish_working_on_nodes` when done. Open-ended self-QA burns the user's money doing worse what a fresh critique does
better.
