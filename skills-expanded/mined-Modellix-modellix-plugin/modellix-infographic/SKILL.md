---
name: modellix-infographic
description: Plan one prompt for a single infographic, visual summary, or information diagram. Use this skill whenever the user asks for an infographic, 信息图, 可视化总结, visual summary, or a diagram that packs a source into one comparison, sequence, funnel, cycle, dashboard, or module overview — even if they only say "turn this into a picture of the facts." Confirm the structure, aspect, and on-image language, quote the source facts, then hand generation to modellix-design. Skip social-network cards, in-article illustration sets, knowledge comics, ordinary posters, and requests that only need an already finished prompt executed.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: infographic,information-design,prompt-engineering,modellix
---

# Modellix Infographic

Turn a source into one prompt for one infographic. This skill plans the image.
`modellix-design` generates it.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the image made, finish the brief first and then hand the prompt to
`modellix-design`.

A cover, thumbnail, or carousel for a named network belongs to
`modellix-social-card`. A poster, product shot, or illustration that is not an
information diagram belongs to `modellix-image-prompt-engineering`. Files already
on disk belong to `modellix-ffmpeg` or `modellix-moviepy`.

## Route the request

Use this skill when the user wants one image that explains a source: a
comparison, a sequence, a funnel, a cycle, a stack of layers, a hub, a metric
board, or a set of peer modules.

Ask once for the source when the user names the format but not the content. Do
not invent facts to fill an empty request.

Skip or keep the pass short when:

- The user already supplied a finished prompt and asked only to run it. Pass that
  prompt to `modellix-design`.
- The request is a social card for a specific network. Use `modellix-social-card`.
- The request is an article, blog, or newsletter cover. Use `modellix-cover-image`.
- The request is a set of illustrations placed through an article. Use `modellix-article-illustrator`.
- The request is a knowledge comic, educational comic, biography comic, or four-panel strip. Use `modellix-comic`.
- The request is a poster or product image with no structured facts. Use
  `modellix-image-prompt-engineering`.
- The request is a commerce UGC video that still needs a shot plan. Use
  `modellix-ecomm-ugc-video`.
- The request is video editing, credentials, task status, or a download.

## Plan the image

Read `references/structures.md` to choose the structure. Read
`references/prompt-shape.md` before writing the prompt.

1. Copy the facts that must appear. Keep every number, name, and quotation. Drop
   credentials, tokens, and secrets. Do not add a statistic the source does not
   contain.
2. State one purpose: what the viewer should understand in a glance.
3. Split the source into sections. Each section has a short headline, the exact
   text, and a visual role such as a bar, a step, or a spoke.
4. Offer two or three structures that fit, each with a one-line reason. A
   structure the user already named is the confirmation. Otherwise wait. Also
   confirm the aspect and the on-image language. Language follows the source
   unless the user names another.
5. Write one prompt for one flat image. Quote the exact words, say which line is
   largest, and describe where each section sits. Tell the model to copy the
   quoted text and not add labels of its own.

Do not ask for SVG, HTML, or a second pass that paints text onto the bitmap.
Crowded copy is fixed by shortening the quoted labels, then regenerating.

## Brief

Return this brief:

```text
Infographic brief
- Purpose:
- Structure:
- Aspect:
- On-image language:
- Sections:
  1. Role / exact text / visual role
- Prompt:
- Next step: stop after prompt | pass the prompt to modellix-design
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for a prompt, stop after the brief. If the original
request asked for the image, pass the prompt to `modellix-design` and let that
skill ask for a model, then own schema validation, credentials, paid submission,
waiting, and download.

## Revision

When a generated infographic misses, change the prompt and return a new brief:

- Wrong or extra number: quote the source figure again and say not to invent one.
- Garbled label: shorten the quoted text and repeat the copy instruction.
- Wrong reading order: restate the confirmed structure and where each section sits.
- Too much text: move nuance out of the image and keep the labels.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate. This skill does not cover the bitmap with corrected type.
