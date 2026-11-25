---
name: modellix-article-illustrator
description: Plan prompts for a set of illustrations placed through an article. Use this skill whenever the user asks to illustrate an article, add images to a post, 为文章配图, or 文章配图 — even if they only say "add pictures to this article." Recommend a preset or a type, style, and palette, confirm density, aspect, and language, then write one prompt per illustration and hand each to modellix-design. Skip a single article cover, a single infographic, a casting board, a knowledge comic, a named social card, and requests that only need an already finished prompt executed.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: article,illustration,prompt-engineering,modellix
---

# Modellix Article Illustrator

Turn an article into one prompt per illustration. This skill plans the set.
`modellix-design` generates each image.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the images made, finish the brief first and then hand the prompts to
`modellix-design` in order.

One article cover with no named network belongs to `modellix-cover-image`. One
standalone infographic belongs to `modellix-infographic`. A knowledge comic
belongs to `modellix-comic`. A casting board belongs to `modellix-casting`. A
card for a named network belongs to
`modellix-social-card`. A poster, product shot, or single illustration belongs
to `modellix-image-prompt-engineering`. A commerce UGC video belongs to
`modellix-ecomm-ugc-video`. Files already on disk belong to `modellix-ffmpeg` or
`modellix-moviepy`.

## Route the request

Use this skill when the user wants several pictures placed through an article,
blog post, essay, or newsletter: 为文章配图, illustrate this article, or add
images to this post.

One picture inside that set may be an infographic, a scene, or a diagram. The
set stays here. Send the request away only when the whole deliverable is a
single cover, a single infographic, or a comic.

Ask once for the article when the user names the format but not the source. Do
not invent a title, a section, a quotation, or a statistic to fill an empty
request.

Skip or keep the pass short when:

- The user already supplied finished illustration prompts and asked only to run
  them. Pass those prompts to `modellix-design` in the order given.
- The request is one article, blog, or newsletter cover. Use `modellix-cover-image`.
- The request is one comparison, sequence, or metric board and nothing else. Use
  `modellix-infographic`.
- The request is a knowledge comic, educational comic, biography comic, or
  four-panel strip. Use `modellix-comic`.
- The request is a casting board or turnaround lookbook. Use `modellix-casting`.
- The request names a network and a card, cover, thumbnail, or carousel. Use
  `modellix-social-card`.
- The request is a poster, product shot, or single illustration. Use
  `modellix-image-prompt-engineering`.
- The request is a commerce UGC video that still needs a shot plan. Use
  `modellix-ecomm-ugc-video`.
- The request is video editing, credentials, task status, or a download.

## Plan the illustrations

Read `references/selection.md` to recommend the set. Read `references/styles.md`
for what the style and palette names look like, and `references/presets.md` when
a preset is chosen. Read `references/prompt-shape.md` before writing a prompt.

1. Copy the facts that must survive. Keep names, numbers, and quotations the
   article actually contains. Drop credentials, tokens, and secrets. Do not add
   a claim the article does not contain.
2. State two to five core points. Mark the sections where a picture adds
   something the paragraph does not already say. Skip transitions and repeated
   points. A metaphor becomes the underlying idea: a bottleneck is a narrow
   gate, not a glass bottle, unless the article is about bottles.
3. Recommend one preset, or one type, style, and optional palette. Give a
   one-line reason from the article. Also recommend density, aspect, and
   on-image language. Language follows the article unless the user names
   another. Aspect defaults to 16:9. The other choices are 1:1 and 4:3. Density
   defaults to `per-section`, one picture per major section, and at most six
   pictures. Go past six only when the user names a higher count, and say that
   each picture is a separate generation later.
4. A choice the user already named is the confirmation. If any of preset or
   type/style/palette, density, aspect, or language is still open, ask once for
   the open set and wait. "Use the recommendation" is a confirmation. Do not
   write prompts before that.
5. When `mixed` is confirmed, each illustration keeps its own type. The style,
   palette, and aspect stay the same across the set.
6. When the same figure appears in more than one illustration, write one
   appearance lock: role, age range, face, hair, costume, and two or three
   color names. Repeat that lock in every prompt that includes the figure. Do
   not add a character sheet unless the user asks for one. A comic that needs a
   sheet belongs to `modellix-comic`.
7. Write one prompt per illustration, in article order. Name the section it
   follows. Quote only the labels that illustration needs. Tell the model to
   copy those words and add no caption, logo, watermark, or extra claim.

When the user supplies reference images, name each path and one usage: direct,
style, or palette. Describe the concrete elements to keep. This skill does not
upload the files. `modellix-design` decides which schema field receives them.

Do not rewrite the article. The brief lists the section each picture follows.
Insert Markdown image links only when the user asks for that edit, and only
after the images exist.

Until the open choices are confirmed, return the recommendation, the core
points, and the section anchors, and leave every prompt empty.

## Brief

Return this brief:

```text
Article illustration brief
- Article / core points:
- Preset or type / style / palette:
- Density / count:
- Aspect:
- On-image language:
- Style lock:
- Figure lock: none | description
- References: none | path / usage
- Illustrations: N. section / purpose / exact labels / prompt
- Next step: stop after prompts | pass prompts to modellix-design in order
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for prompts, stop after the brief. If the original
request asked for the images, pass the prompts to `modellix-design` in article
order. That skill asks for a model and owns schema validation, credentials,
paid submission, waiting, and download. Each illustration is a separate image.

## Revision

When a generated illustration misses, change that prompt and return a new brief:

- Garbled or invented words: shorten the quoted labels. Do not paint text over
  the bitmap.
- A literal reading of a metaphor: restate the underlying idea.
- A number or quotation the article does not contain: delete it.
- Style drift across the set: restate the same style lock.
- A figure that changed face or costume: restate the figure lock.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate.
