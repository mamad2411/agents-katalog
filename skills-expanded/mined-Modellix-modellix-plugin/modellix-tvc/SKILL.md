---
name: modellix-tvc
description: Plan shot prompts for a product TVC, brand film, or cinematic commercial. Use this skill whenever the user wants a 商品广告片, TVC, brand film, or a polished product film — even if they only say "make a commercial for this product." The product can be anything they name. Confirm the structure, length, aspect, and whether a person appears, lock only the facts they supplied, then hand each shot to modellix-design. Skip creator talking-head ads, still images, and edits of files already on disk.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for video execution. After those files exist, modellix-ffmpeg concatenates the shots.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: tvc,commercial,product-film,prompt-engineering,modellix
---

# Modellix TVC

Turn any product into one prompt per shot for a cinematic commercial. This skill
plans the film. `modellix-design` generates each shot.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the film made, finish the brief first and then hand the shot prompts
to `modellix-design` in order.

A creator-style review, unboxing, try-on, haul, or talking-head shop ad belongs
to `modellix-ecomm-ugc-video`. A still product photo or poster belongs to
`modellix-image-prompt-engineering`. Files already on disk belong to
`modellix-ffmpeg` or `modellix-moviepy`.

## Route the request

Use this skill when the user wants a finished-looking product commercial: a TVC,
a brand film, a 15-second or 30-second spot, or 商品广告片. The product category
does not matter. A shoe, a snack, a tool, a bottle, a machine, or a packaged
good all use the same brief. The user's facts fill the product lock.

Ask once for the product when the user names the format but not the item. Do
not invent a product, a price, a slogan, or a performance claim to fill an
empty request.

Skip or keep the pass short when:

- The user already supplied finished shot prompts and asked only to run them.
  Pass those prompts to `modellix-design` in the order given.
- The request is a phone-style review, 口播, unboxing, try-on, or haul. Use
  `modellix-ecomm-ugc-video`.
- The request is a still image, a poster, or a product photo with no film. Use
  `modellix-image-prompt-engineering`.
- The request is concatenation, trimming, a subtitle burn, or a title on files
  that already exist. Use `modellix-ffmpeg` or `modellix-moviepy`.

## Plan the film

Read `references/selection.md` to choose the structure, length, aspect, and
whether a person appears. Read `references/patterns.md` for what the chosen
structure does. Read `references/shot-shape.md` before writing a prompt.

1. Copy the product facts that must survive. Keep the category, shape, material,
   color, and any claim the user actually supplied. Drop credentials, tokens,
   and secrets. Do not add a price, a rating, an efficacy, or a slogan.
2. Recommend one structure, a length, an aspect, and whether a person is in the
   film. Give a one-line reason from the job of the spot, not from a fixed
   catalog of product types. Length defaults to 15 seconds. Aspect defaults to
   16:9. Use 9:16 when the user asks for a vertical or social cut.
3. A choice the user already named is the confirmation. If structure, length,
   aspect, or the presence of a person is still open, ask once for the open set
   and wait. "Use the recommendation" is a confirmation. Do not write prompts
   before that.
4. Write one product lock: category, shape, material, and color, in the user's
   words. When a person appears, add one person lock: age range, face, hair,
   clothes, and two color names. Repeat both locks in every shot that contains
   them. Use an original person. Do not name a celebrity or a copyrighted
   character.
5. Write one prompt per shot, in film order. A 15-second film is five shots.
   The last shot is a slow product hold, unless the confirmed structure ends on
   the person with the product. Each shot is one action and one camera move.
   Tell the model to leave captions, logos, watermarks, and writing on the
   package out of the frame.
6. If the user supplied an exact end line, list it beside the last shot for
   `modellix-moviepy` after the files exist. Do not put that line inside a
   generation prompt.
7. Name a music mood in the brief when it helps the cut. Leave it out of the
   picture prompts. Pass a separate audio description to `modellix-design` only
   when the user asked for a soundtrack.

When the user supplies a product still, name that path with usage `direct` on
every shot that shows the product. This skill does not upload the file.
`modellix-design` decides which schema field receives it.

Until the open choices are confirmed, return the recommendation and the facts
you will keep, and leave every shot prompt empty.

## Brief

Return this brief:

```text
TVC brief
- Product facts:
- Structure:
- Length / shots / aspect:
- Person: none | lock
- Product lock:
- Reference images: none | path / direct
- Music mood: omitted | words, not a picture prompt
- Shots: N. role / duration / prompt
- End line: none | exact words, for modellix-moviepy after download
- Next step: stop after prompts | pass shot prompts to modellix-design in order, then concatenate with modellix-ffmpeg
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for prompts, stop after the brief. If the original
request asked for the film, pass the shot prompts to `modellix-design` in
order. That skill asks for a model and owns schema validation, credentials,
paid submission, waiting, and download. Each shot is a separate video. After
those files exist, concatenation belongs to `modellix-ffmpeg`. An end line, if
the user supplied one, belongs to `modellix-moviepy`.

## Revision

When a generated shot misses, change that prompt and return a new brief:

- An invented claim or slogan: delete it and restate the user's facts.
- Letters on the package or in the frame: say again that the image contains no
  writing. Do not paint type onto the file.
- The product changed shape or color: restate the product lock. If a still was
  supplied, require it as `direct`.
- The person changed: restate the person lock.
- Too many actions in one shot: move the extra action to the next shot.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate.
