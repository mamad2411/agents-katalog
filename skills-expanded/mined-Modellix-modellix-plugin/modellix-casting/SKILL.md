---
name: modellix-casting
description: Plan one casting-board prompt per character. Use this skill whenever the user asks for a casting sheet, talent board, 选角图, 定妆照, or a turnaround lookbook — even if they only say "show this character from every angle on one board." Recommend a rendering, lock the identity, confirm the aspect, then hand the prompt to modellix-design. Skip comic model sheets, posters, article covers, and requests that only need an already finished prompt executed.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: casting,character,turnaround,prompt-engineering,modellix
---

# Modellix Casting

Turn a character into one prompt for one casting board. This skill plans the
image. `modellix-design` generates it.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the board made, finish the brief first and then hand the prompt to
`modellix-design`.

A knowledge comic, including the plain character sheet a comic uses between
pages, belongs to `modellix-comic`. A poster, product shot, or single portrait
belongs to `modellix-image-prompt-engineering`. An article cover belongs to
`modellix-cover-image`. A set of illustrations placed through an article belongs
to `modellix-article-illustrator`. A card for a named network belongs to
`modellix-social-card`. A commerce UGC video belongs to
`modellix-ecomm-ugc-video`. Files already on disk belong to `modellix-ffmpeg` or
`modellix-moviepy`.

## Route the request

Use this skill when the user wants one board that shows the same character as a
hero portrait, an expression grid, and a full-body turnaround. Wording includes
casting sheet, talent board, 选角图, 定妆照, and turnaround lookbook.

Ask once for the character when the user names the format but not the person.
Do not invent a name, an age, or a costume to fill an empty request.

Skip or keep the pass short when:

- The user already supplied a finished casting prompt and asked only to run it.
  Pass that prompt to `modellix-design`.
- The request is a knowledge comic, educational comic, biography comic, or
  four-panel strip, including the plain sheet that keeps a comic cast
  consistent. Use `modellix-comic`.
- The request is one poster, product shot, or single portrait. Use
  `modellix-image-prompt-engineering`.
- The request is one article, blog, or newsletter cover. Use `modellix-cover-image`.
- The request is a set of illustrations placed through an article. Use
  `modellix-article-illustrator`.
- The request names a network and a card, cover, thumbnail, or carousel. Use
  `modellix-social-card`.
- The request is a commerce UGC video that still needs a shot plan. Use
  `modellix-ecomm-ugc-video`.
- The request is video editing, credentials, task status, or a download.

## Plan the board

Read `references/layout.md` before describing the frame. Read
`references/selection.md` to choose the rendering and the layout example. Read
`references/prompt-shape.md` before writing the prompt.

1. Copy only the identity the user gave. Keep age range, face, hair, build, and
   costume in their words. Drop credentials, tokens, and secrets. Use an
   original character. Do not name a real celebrity or a copyrighted character.
   A historical person is described by era, role, and costume, not by a claim
   that the picture is a photograph of that person.
2. Write one identity lock: age range, face, hair, build, costume, and two or
   three color names. The same sentences appear in the hero, the expression
   grid, and the turnaround.
3. Recommend one rendering and the aspect. Give a one-line reason. `studio` is
   the usual recommendation: a photographic studio, an ivory ground, and even
   soft light. `illustrated` keeps the same board in a drawing style the user
   named. `period` keeps the same board and takes the costume from the era the
   user named. Aspect defaults to 16:9. If the user named no costume, recommend
   one plain studio outfit and the closest layout example. Do not invent a
   costume they already contradicted.
4. A choice the user already named is the confirmation. If rendering, aspect, or
   a missing costume is still open, ask once for the open set and wait. "Use
   the recommendation" is a confirmation. Do not write the prompt before that.
5. Write one prompt for one board. The image contains no letters, numbers,
   logos, or watermarks. Describe the left 3×3 headshots, the center portrait,
   and the right full-body front, three-quarter, and back views.
6. When the user asks for a separate front, side, or back file, add one prompt
   per named view and keep the board. Do not split the board unless they ask.
   Each extra view is a separate generation later.
7. One character is one board. Plan at most four boards unless the user names a
   higher count.

When the user supplies a picture of the person, name that path with usage
`direct`. For `studio`, also name one layout example from
`references/examples/` with usage `layout`. Pick the example whose costume is
closest; otherwise use `references/examples/studio-board-suit.webp`. The prompt
says the layout example controls the board and the studio light, and does not
control face, hair, age, build, or costume. For `illustrated` and `period`, do
not attach a photographic example. This skill does not upload files.
`modellix-design` decides which schema field receives each path.

Until the open choices are confirmed, return the recommendation and the
identity you will keep, and leave the prompt empty.

## Brief

Return this brief:

```text
Casting brief
- Character:
- Rendering:
- Aspect:
- Identity lock:
- References: none | path / direct or layout
- Board prompt:
- Extra views: none | view / prompt
- Next step: stop after prompt | pass the prompt to modellix-design
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for a prompt, stop after the brief. If the original
request asked for the image, pass the board prompt to `modellix-design`, then
any extra views. That skill asks for a model and owns schema validation,
credentials, paid submission, waiting, and download. Each file is a separate
image.

## Revision

When a generated board misses, change the prompt and return a new brief:

- The face or costume drifted: restate the identity lock in every zone.
- The layout example's person leaked in: say again that the example controls
  only the board and the light.
- An extra person, a label, or a number appeared: restate the 3×3 grid, the
  three full-body views, and that the image contains no text.
- Do not paint corrected type onto the bitmap.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate.
