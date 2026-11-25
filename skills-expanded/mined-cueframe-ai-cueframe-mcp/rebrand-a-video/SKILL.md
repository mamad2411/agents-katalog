---
name: rebrand-a-video
description: Swaps the brand kit under an existing video and re-renders — tokens, bumpers, logo, captions, and motion re-theme automatically; hardcoded card values get surgical edits. Triggers on "rebrand this video", "swap the brand", "we changed our colors", "new logo, same video", "make this video match the new brand", "re-theme our launch video", "white-label this for a client".
---

# Rebrand a video

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

You bring a finished video and a new brand (a kit, a website, or new colors/fonts/logo); you get
the same video back wearing the new identity — everything bound to brand tokens re-themes at
render, and the few graphics that hardcoded the old brand get found and fixed. Change one line,
not the whole video.

## Before you start

Collect the new brand's facts first — the swap itself is fast. When the first tool call
approaches and CueFrame isn't connected, load **`cueframe-connect`** and follow it once.

Then back to the brand — most of this job is a kit definition and an audit.

## Inputs

- **The video** (required): the composition (via `list_compositions`) and which project it lives
  in.
- **The new brand** (required): an existing kit id, a website to `extract_brand_kit` from
  (colors/fonts only — ask for logo, tagline, voice), or explicit values for `create_brand_kit`.
- **Scope:** a title/color/logo correction edits only affected clip values or bindings. Do not upsert a shared kit for one local correction. A project-wide brand change must be explicit: a same-kit upsert affects every referencing composition. For a new identity, use a new kit when supported. Styling preserves layout; a full redesign requires explicit scope.
- **Tone shift**: does the new brand change the music mood too? Check the kit's `musicMood`
  intent.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
for affected graphics and saved-composition checks. Inspect motion if the kit changes timing;
keep the final re-render separate from previews used to resolve individual styling corrections.

1. **For an explicit project-wide brand change, pin the new brand as a kit.** `extract_brand_kit` or `create_brand_kit`; show the kit and
   get sign-off — it is the contract. Then bind it: upsert in place (same kit id) to restyle,
   or point the project at the new kit for a white-label. The kit lives on the PROJECT, not on
   a composition op.
2. **Know what re-themes for free.** Everything resolved at render: `$brand:` color/font/motion
   tokens on overlays and cards, the kit's intro/outro bumpers, the logo corner mark, the
   caption profile, the motion identity. Edit the kit, re-render, these all follow — that is
   the whole "one line" story.
3. **Hunt what does NOT re-theme.** Anything that hardcoded the old brand: literal hexes or
   font names inside `kind:"card"` HTML, an old wordmark imported as media, footage graded
   toward the old palette, baked stock choices that lived in the old world. Walk the
   composition's overlay and card clips and list every literal value — this audit is the real
   work.
4. **Verify with pixels, not the kit.** Kit contents aren't inspectable over MCP after
   creation, so the truth is the frame: `preview_frame` at t=0, each card, the bumpers, and the
   end card. Describe each still — is any old color, font, or mark visible? A `$brand:` token
   that fails to resolve is loud in render logs and falls to a legible neutral; a hardcoded old
   hex is silent, which is why you hunt it by eye.
5. **Fix the holdouts surgically.** `apply_composition` edits per offending clip: rebind card
   fields to `$brand:` tokens (so the NEXT rebrand really is one line), swap the old-wordmark
   media, re-grade footage toward the new palette. A replaced card gets its
   `clip.setKeyframes` re-applied in a FOLLOWING call. If the requested scope is styling, retain its layout; rebuild only for an explicitly requested redesign.
6. **Review audio only when in scope.** A styling correction preserves existing audio and timing; for a broader brand change: check the bed against the
   new kit's `musicMood`. Wrong mood → `search_resources` a replacement (license recorded),
   same role and ducking, `materializeGrid` re-run if cut timing shifts. Still right → say so
   in the delivery note. If the piece was intentionally silent, confirm that decision still
   fits the new brand and restate it.
7. **Preview the affected styling.** Check the changed color/logo/text and relevant regressions against the requested values. For broader brand review, use `score_composition` only when useful and within budget. Export with `create_render` only for requested final delivery.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. The bespoke test in section 3 of the [format standards](../video-craft-standards/references/format-standards.md) applies to every card in any class.

## Delivering

The last message closes the loop, never "done":

- The re-rendered link and where it lives (project + composition id), plus the kit id now bound
  — and the one-line promise made true: next time, edit the kit and re-render.
- What re-themed automatically vs what you hand-edited (the audit list from step 3) — the user
  should know which parts of their video are now token-bound.
- Attribution for any newly licensed bed or asset (provider, id, author).
- The audio decision: bed kept / bed swapped and why / intentional silence restated.
