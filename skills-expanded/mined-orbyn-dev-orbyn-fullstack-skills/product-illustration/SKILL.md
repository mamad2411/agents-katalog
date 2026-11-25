---
name: product-illustration
description: "Build faux product UI as stills or animated cursor demos: heroes, feature cards, bento grids, cursor walkthroughs. Use orbyn-ui-design for real product screens, technical-illustration for films and model-driven figures, social-preview for posters."
---

# Product illustration

Use this for miniature product UI: a believable interface, framed in its space, as one still or a short animation in which one thing happens. These are authored illustrations, not browser automation: `a.click()` draws the cursor pressing, `a.set()` changes the scene. The React kit derives from Stageshow.

The kit root is `references/upstream/stageshow/`. In the references, `kit/`, `examples/`, `teaching/` and `scripts/` mean folders there.

## The one idea

**It reads as a real product, simplified to what the viewer needs, framed with intent, and every motion has a cause.**

Five ways it fails:

- **Too much.** Real text in every row, numbers everywhere.
- **Wireframe.** Two gray blobs and a button: built too small, or stripped of what made it recognizable.
- **Boxed.** A whole window shrunk into a card with even margins: a screenshot pasted in.
- **Flat.** Every object the same weight in the same bordered card.
- **Bland.** A gray window with a cursor, whatever the brief said; the brief's look and energy are the point.

The fix: a full, structured screen in quiet grays, real words only on what the story is about, placeholder lines elsewhere, room to breathe, and a crop that puts the eye on the story. Simplify the words, not the context.

## Method

1. **Plan first.** Write where it sits, the focal object, the action, the payoff and what can be left out. Choose still or animation. Design at shown size; any demo that can sit in a phone column ships a `compact` redesign at 358. For a grid, plan the set with [bento](references/bento.md). Sizes: [build method](references/build-method.md#plan-sizes).
2. **Set up a working copy** outside the library, or copy `kit/` into the project's React app; install only there with `npm install --ignore-scripts`, so the library stays free of `node_modules` and lockfiles ([setup](references/build-method.md#working-copy)).
3. **Choose the look.** Map the user's product tokens to the kit's ([looks](references/looks.md)), or pick a theme, palette and fidelity. Default to light, accent, standard. Give a brief with a style that style in full. Name the product: the user's own, or a fictional one.
4. **Write the story.** Three to five beats and a payoff, 10 to 16 seconds, with no cursor move you can't explain. Choose a calmer frame over a richer story ([motion](references/motion.md)).
5. **Start from the closest gold** in [gold examples](references/gold-examples.md): film it and copy its folder to `examples/<yours>/`. Keep its stage size, crop, spacing, beats and kit parts. Read [craft](references/craft.md) in full. Replace look and content; a renamed copy is unfinished. Then frame it ([framing](references/framing.md)) and film one still beside the gold's at both widths. If yours is emptier, flatter or more boxed, fix the frame first.
6. **Build the screen.** Spend 3 to 7 real strings. Build with kit tokens, `Bar`, `Text`, `Row`, `Card`, `Button` and `Kbd`; never hand-build a lookalike of a kit part. Mark what the cursor touches with `data-target` and `data-cursor`; measure with `rect()`, never hard-code ([kit](references/kit.md)).
7. **Choreograph.** Keep what appears mounted and toggle it so exits animate. Animate the relationship: a new row carries the rows below it. Beats overlap, the payoff holds, the loop ends where it began or resets with a visible cause.
8. **Rehearse for real.** Set `poster` first: the beat that tells the story alone, with the result on screen. Film the loop, not just a still, at shown width, again at `--width 390`, and with `--states`, always with `--gate` ([film command](references/build-method.md#film-command)): it exits 1 on any fault, and you do not hand over until it ends `rehearsal passed`. That is necessary, not sufficient. Read every frame; fix the largest fault first (framing, hierarchy, motion, polish) and re-film. Finish with [rehearse](references/rehearse.md) (commands), [verify](references/verify.md) and `REHEARSAL.md` beside the component, naming the gold, what changed and what you did not check.

### Worked failure

A hero for invoice approval is built as a complete 480-wide window on a tinted plate with real names in all twelve rows. The gate passes, but beside `static-card` it reads as a screenshot. Fix the largest fault first: drop the plate, run the window off the bottom edge at 720 wide, keep real words only on the selected row and its total, and let the approval move that total. Full version: [build method](references/build-method.md#worked-failure).

## Check these before handing over

Each comes back every round. The gold examples are the bar ([how hard to press](references/build-method.md#how-hard-to-press)).

- Content that swaps instead of moving.
- Gray bars where the eye lands; filler belongs at the edges.
- A plate behind the window, or a window floating with air on four sides.
- Empty bands, cut controls and cut shadows.
- Stock AI and made-up logos: sparkles, purple, a letter in a colored square.
- Busy rows and uneven insets.
- Long holds and a reset with no cause.
- A selection that isn't under the I-beam.
- A status bar or home indicator drawn by hand; the `Phone` draws both.
- A centered amount centered with its sign.

## Boundaries

- Show the user's own product or a fictional one. A request to recreate a real company's app gets a generic product with the same interaction; never that company's name, logo, look or UI ([interaction lessons](references/interaction-lessons.md)).
- Logos come from the user ([logos](references/logos.md)). The kit bundles none.
- Web illustrations use React as their host runtime. A video that uses the kit follows the [code-only rule](../technical-illustration/references/code-only.md).
- A fresh-eye review is a [separate reader](references/review.md) when the host offers one. Report your own pass as a self-check.

## Read when needed

- Step detail, bar, full worked failure: [build method](references/build-method.md).
- Example to copy: [gold examples](references/gold-examples.md); props: [kit](references/kit.md).
- Still frame: [craft](references/craft.md), [framing](references/framing.md); grid: [bento](references/bento.md); grounds: [backgrounds](references/backgrounds.md); leaders and dimensions: [annotations](references/annotations.md).
- Story, loops, cursors: [motion](references/motion.md); overlapping changes: [choreography](references/choreography.md).
- User's product tokens: [looks](references/looks.md); a logo: [logos](references/logos.md); a familiar product category: [interaction lessons](references/interaction-lessons.md).
- Filming: [rehearse](references/rehearse.md); last checklist: [verify](references/verify.md); fresh-eye brief: [review](references/review.md); diagnosing a fault: [teaching](references/teaching.md).
