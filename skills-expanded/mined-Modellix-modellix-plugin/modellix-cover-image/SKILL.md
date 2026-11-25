---
name: modellix-cover-image
description: Plan one prompt for an article, blog, or newsletter cover. Use this skill whenever the user asks for an article cover, blog cover, 文章封面, or 封面图 that is not tied to a named social network — even if they only say "make a cover for this post." Recommend a type, palette, rendering, text level, mood, and font, confirm them, quote the source title, then hand generation to modellix-design. Skip platform cards, in-article illustration sets, casting boards, infographics, knowledge comics, photographic posters, and requests that only need an already finished prompt executed.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: cover,article,prompt-engineering,modellix
---

# Modellix Cover Image

Turn an article into one prompt for one cover. This skill plans the image.
`modellix-design` generates it.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the image made, finish the brief first and then hand the prompt to
`modellix-design`.

A cover, thumbnail, or carousel for a named network belongs to
`modellix-social-card`. A set of illustrations placed through an article belongs
to `modellix-article-illustrator`. A casting board belongs to
`modellix-casting`. A structured infographic belongs to
`modellix-infographic`. A photographic poster, product shot, or packaging concept
belongs to `modellix-image-prompt-engineering`. Files already on disk belong to
`modellix-ffmpeg` or `modellix-moviepy`.

## Route the request

Use this skill when the user wants one illustrated cover for an article, blog
post, essay, or newsletter, and has not named a social-network placement.

Ask once for the source when the user names the format but not the article. Do
not invent a title or a claim to fill an empty request.

Skip or keep the pass short when:

- The user already supplied a finished prompt and asked only to run it. Pass that
  prompt to `modellix-design`.
- The request names a network and a card, cover, thumbnail, or carousel. Use
  `modellix-social-card`.
- The request is a set of illustrations placed through the article, not one
  cover. Use `modellix-article-illustrator`.
- The request is a casting board or turnaround lookbook. Use `modellix-casting`.
- The request is a structured infographic, or the picture has to carry a
  comparison, sequence, or metric board. Use `modellix-infographic`.
- The request is a knowledge comic, educational comic, biography comic, or
  four-panel strip. Use `modellix-comic`.
- The request is a photographic poster, product shot, or packaging concept. Use
  `modellix-image-prompt-engineering`.
- The request is a commerce UGC video that still needs a shot plan. Use
  `modellix-ecomm-ugc-video`.
- The request is video editing, credentials, task status, or a download.

## Plan the cover

Read `references/selection.md` to recommend the dimensions. Read
`references/types.md`, `references/palettes.md`, and `references/renderings.md`
for the words those names mean. Read `references/prompt-shape.md` before writing
the prompt.

1. Copy the title from the source. Keep product names in their original spelling.
   Drop credentials, tokens, and secrets. Do not invent a second title, a price,
   or a statistic the source does not contain.
2. Recommend one type, palette, rendering, text level, mood, and font. Give each
   a one-line reason from the source. Also name the aspect and the on-image
   language. Language follows the source unless the user names another. Aspect
   defaults to 16:9. The other choices are 2.35:1, 1:1, and 3:4.
3. A dimension the user already named is the confirmation. If any recommended
   dimension is still open, ask once for the open set and wait. "Use the
   recommendation" is a confirmation. Do not write the prompt before that.
4. Quote only the words the confirmed text level allows. `title-only` is the
   title. `title-subtitle` adds one short line from the source. `text-rich` adds
   at most two short labels. A cover that needs a diagram belongs to
   `modellix-infographic`. `none` puts no words in the image.
5. Write one prompt for one flat image. Describe the type, palette, rendering,
   mood, and font in ordinary visual language. Tell the model to copy the quoted
   text and not add captions, logos, watermarks, or extra claims. People, when
   the type needs them, are simplified figures in that rendering, not photographs.

When the user supplies reference images, name each path and one usage: direct,
style, or palette. Describe the concrete elements to keep. This skill does not
upload the files. `modellix-design` decides which schema field receives them.

## Brief

Return this brief:

```text
Cover brief
- Title:
- Type / palette / rendering:
- Text / mood / font:
- Aspect:
- On-image language:
- Exact text:
- References: none | path / usage
- Prompt:
- Next step: stop after prompt | pass the prompt to modellix-design
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

Until the dimensions are confirmed, return the recommendation and the title you
will keep, and leave the prompt empty.

If the user asked only for a prompt, stop after the brief. If the original
request asked for the image, pass the prompt to `modellix-design` and let that
skill ask for a model, then own schema validation, credentials, paid submission,
waiting, and download.

## Revision

When a generated cover misses, change the prompt and return a new brief:

- Wrong or invented title: quote the source title again.
- Garbled words: shorten the quoted text, or drop to a lower text level.
- Wrong reading of the article: restate the confirmed type and the metaphor.
- Too little air: restate the whitespace for that type.
- A photographic face: restate simplified figures in the confirmed rendering.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate. This skill does not cover the bitmap with corrected type.
