---
name: motion-match
description: "Copy, clone or match how something moves: measure timing and easing, write a spec, build, film ours the same way and compare until the numbers pass; third-party references stay at motion level. Use orbyn-ui-design to design motion, technical-illustration for films, product-illustration for faux UI."
---

# Motion match

Use this when the user points at something that moves and wants ours to move the same way, or wants proof that it does. The result is code plus numbers and sheets, never "it looks about right".

## Rights come first

Decide who owns the reference before capturing anything, and state it in your first message.

| Reference | What you may do |
| --- | --- |
| Our own work, or one the user owns or has licensed | Any fidelity, including pixel-level |
| Anyone else's site or video | Measure timing, easing, order and distance only, as a written spec, and build with our own design |

For anyone else's work:

- Never copy their code, shaders, assets, fonts, brand, layout or copy. Never recreate a real product as if it were ours.
- A pixel-faithful match is off the table, whatever the wording of the request. Offer motion-level instead and say why: "I can match how it moves with your design. Copying their look would take their design work, so I won't do that."
- Login walls, paywalls, bot checks and DRM stay closed. Respect the site's terms and capture only what a normal visitor sees. When a page can't be reached, ask for a screen recording. Never download someone else's video.
- Raw captures stay in an ignored local folder. They are never committed, published or used in a deliverable, and they are deleted when the user chooses. Only the written numbers carry forward. Tell the user where they are.

If the user says they own a reference and nothing contradicts it, take their word and record it in the spec. "Make it identical to that company's site" is not a licence. Use `--rights third-party` whenever ownership is unclear.

## Fidelity

State the level in your first message; it decides what you verify.

| Level | Must match | May differ |
| --- | --- | --- |
| Motion (default) | Trigger, order, stagger, timing of every step within 80 ms, easing, direction and distance | Copy, colours, fonts, images, layout, brand |
| Pixel, own or licensed only | All of the above, plus fonts, sizes, colours, spacing and assets; mean mismatch at most 2% | Nothing the user did not ask to change |
| Mixed | The matched part, at one of the levels above | The additions, which must not break the matched motion |

Match only what the user named: one section, one widget, or a time range.

## Method

Work in `output/motion-match/<name>/`, or another folder Git ignores. Keep every round. Node 22, an existing browser driver and an existing browser are required; `ffmpeg` is needed for video. Nothing is installed ([requirements](references/capture.md#requirements)).

1. **Scope.** Write the target, the destination in the project, the rights and the fidelity.
2. **Capture the reference** with `scripts/capture.mjs`, or `scripts/frames.mjs` for a supplied video. Give it the rights you decided with `--rights` ([capture](references/capture.md) has the command).
3. **Read every sheet.** Run `scripts/sheet.mjs filmstrip`, then open each sheet. The easing lives in the middle frames.
4. **Write the spec.** Run `scripts/spec.mjs draft`: one row per element per property. A `?` means you have not finished reading the frames, and the check refuses to run until each is replaced.
5. **Build** in the project's own stack, with its own design for a third-party reference.
6. **Film ours the same way.** Reuse the reference command, changing only `--url`, `--out` and `--rights`. Different settings measure your setup, and `compare.mjs` fails them.
7. **Compare.** Run `scripts/spec.mjs check`, `scripts/compare.mjs` and `scripts/sheet.mjs compare`. Read every sheet.
8. **Change the smallest thing the numbers point at**, one cause per round, then go back to step 6.
9. **Stop after 5 rounds** if a row still fails, and report it with its numbers and the reason. Keep the thresholds where they are.
10. **Report** so the message stands alone ([report block](references/verify.md#report-block)): rights and fidelity, what was matched and added, files and trigger, the last round's table, sheet paths, each residual with a number and a reason, and where any raw third-party capture sits.

### Worked failure

Round 1 of three cards fails: every row is late by +300 ms, while the easing curve and the gaps are right. The only cause is the base delay, so change that one number and re-film. Aligning the frames would pass the row and ship a 300 ms late animation, which is why `compare.mjs` refuses `--auto-align` between two captures. Full numbers: [verify](references/verify.md#worked-failure). Pitfalls (viewport, fonts, scroll, springs, canvas, recordings, CSS easing) are in the same file.

## Boundaries

Use [orbyn-ui-design](../orbyn-ui-design/SKILL.md) to decide what motion a product should have, [technical-illustration](../technical-illustration/SKILL.md) for films, and [product-illustration](../product-illustration/SKILL.md) for faux UI. A video follows the [code-only rule](../technical-illustration/references/code-only.md): study a reference for technique, and never copy its frames.

## Read when needed

- For capture recipes, triggers and output files, read [capture](references/capture.md).
- For the spec format and how to read frames, read [analysis](references/analysis.md).
- For easing, springs and building patterns, read [implementation](references/implementation.md).
- For pass criteria, what each failure means, the worked failure and pitfalls, read [verify](references/verify.md).
