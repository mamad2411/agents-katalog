---
name: modellix-comic
description: Plan prompts for a knowledge comic, educational comic, biography comic, tutorial comic, concept story, or four-panel strip. Use this skill whenever the user asks for 知识漫画, 教育漫画, 传记漫画, 四格漫画, or a comic that explains an idea — even if they only say "turn this into a comic." Recommend art, tone, and layout or a preset, confirm page count, aspect, language, and text level, lock the cast, then hand each page to modellix-design. Skip infographics, article covers, in-article illustration sets, casting boards, social cards, posters, and requests that only need an already finished prompt executed.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: comic,knowledge,storyboard,prompt-engineering,modellix
---

# Modellix Comic

Turn a source into a storyboard and one prompt per page. This skill plans the
comic. `modellix-design` generates each image.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the pages made, finish the brief first and then hand the prompts to
`modellix-design` in order.

A structured infographic belongs to `modellix-infographic`. An article cover with
no named network belongs to `modellix-cover-image`. A set of illustrations placed
through an article belongs to `modellix-article-illustrator`. A casting board
belongs to `modellix-casting`. A card for a named
network belongs to `modellix-social-card`. A poster, product shot, or single
illustration belongs to `modellix-image-prompt-engineering`. A commerce UGC video
belongs to `modellix-ecomm-ugc-video`. Files already on disk belong to
`modellix-ffmpeg` or `modellix-moviepy`.

## Route the request

Use this skill when the user wants a new comic that explains something: a
tutorial, a technical idea, a biography, a concept story, or a four-panel strip.

Ask once for the source when the user names the format but not the subject. Do
not invent a title, a date, a quotation, or a statistic to fill an empty request.

Skip or keep the pass short when:

- The user already supplied finished page prompts and asked only to run them.
  Pass those prompts to `modellix-design` in the order given.
- The request is one comparison, sequence, or metric board with no story. Use
  `modellix-infographic`.
- The request is one article, blog, or newsletter cover. Use `modellix-cover-image`.
- The request is a set of illustrations placed through an article, with no comic
  pages. Use `modellix-article-illustrator`.
- The request is a casting board or turnaround lookbook, with no comic pages.
  Use `modellix-casting`.
- The request names a network and a card, cover, thumbnail, or carousel. Use
  `modellix-social-card`.
- The request is a poster, product shot, or single illustration. Use
  `modellix-image-prompt-engineering`.
- The request is a commerce UGC video that still needs a shot plan. Use
  `modellix-ecomm-ugc-video`.
- The request is video editing, credentials, task status, or a download.

## Plan the comic

Read `references/selection.md` to recommend the style. Read `references/styles.md`
for what those names look like, and `references/presets.md` when a preset is
chosen. Read `references/storyboard.md` before writing a prompt.

1. Copy the facts that must survive. Keep names, dates, and quotations the source
   actually contains. Drop credentials, tokens, and secrets. Do not add a claim
   the source does not contain.
2. State the core message in one sentence. Decide what to keep, simplify, and
   leave out. A concept becomes a prop, an action, or a place, not a lecture.
3. Recommend one preset, or one art style, tone, and layout. Give a one-line
   reason from the source. Also recommend the page count, aspect, on-image
   language, and text level. Language follows the source unless the user names
   another. A four-panel strip is one page at 3:4. A webtoon is 9:16. Other
   comics default to 3:4. Recommend a cover plus at most six story pages unless
   the user already named a count. Do not plan a long serial by default.
4. A choice the user already named is the confirmation. If any of preset or
   art/tone/layout, page count, aspect, language, or text level is still open,
   ask once for the open set and wait. "Use the recommendation" is a confirmation.
   Do not write prompts before that.
5. Define the cast in words: role, age range, face, hair, build, costume, and
   two or three color names. Repeat that same lock in every page prompt. Use
   original characters. Do not borrow a named copyrighted mascot. A historical
   person is described by era, role, and costume in the chosen art style, not as
   a photographic portrait.
6. When more than one page shares recurring characters, write a character-sheet
   prompt first: front view, three-quarter view, and a few expressions on a plain
   background. A four-panel strip and any other single page skip the sheet. The
   brief tells `modellix-design` to generate the sheet first and pass that saved
   image as a reference on every later page. This skill does not upload files.
7. Write one prompt per page, in reading order. Describe the panel grid, the
   action, and the cast lock. `bubbles` quotes only short lines from the source
   or the user, and tells the model to copy them and add no title, logo,
   watermark, or extra claim. `silent` puts no words in the image and lists the
   lines beside that page. Do not hand those lines to `modellix-ffmpeg` or
   `modellix-moviepy`.

When the user supplies reference images, name each path and one usage: direct,
style, or palette. Describe the concrete elements to keep.

Until the open choices are confirmed, return the recommendation and the facts
you will keep, and leave every prompt empty.

## Brief

Return this brief:

```text
Comic brief
- Title / core message:
- Preset or art / tone / layout:
- Pages / aspect:
- On-image language / text level:
- Cast:
- References: none | path / usage
- Character sheet prompt: omitted | prompt
- Pages: N. role / exact text / prompt
- Next step: stop after prompts | pass prompts to modellix-design in order
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for prompts, stop after the brief. If the original request
asked for the comic, pass the prompts to `modellix-design` in this order:
character sheet when present, then the cover, then the story pages. That skill
asks for a model and owns schema validation, credentials, paid submission,
waiting, and download. Each page is a separate image.

## Revision

When a generated page misses, change the prompt and return a new brief:

- Garbled or invented words: shorten the quoted line, or switch that page to
  `silent`. Do not paint text over the bitmap.
- A character changed face or costume: restate the cast lock and require the
  character-sheet image as a reference.
- A talking-heads page in a preset that forbids them: replace the panel with a
  prop, an action, or a place.
- A photographic portrait of a historical person: restate the chosen art style
  and the era costume.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate.
