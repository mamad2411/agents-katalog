---
name: modellix-ecomm-ugc-video
description: Plan shot prompts for a vertical ecommerce UGC video. Use this skill whenever the user wants a creator-style product video, 带货口播, unboxing, try-on, haul, listicle, or a TikTok, Reels, or Shorts shop ad — even if they only say "UGC", "口播视频", or "make it look like a real person reviewing this". Confirm the pattern, spoken language, and length, quote only the product facts they supplied, then hand each shot to modellix-design. Skip cinematic product commercials, still images, and edits of files already on disk.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for video execution. After those files exist, modellix-ffmpeg concatenates shots and burns the caption list.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: ugc,ecommerce,video,prompt-engineering,modellix
---

# Modellix Ecomm UGC Video

Turn a product and a selling point into shot prompts for one vertical creator-style
video. This skill plans the video. `modellix-design` generates each shot.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. When the
user wants the video made, finish the brief first and then hand each shot prompt
to `modellix-design`.

A cover or thumbnail belongs to `modellix-social-card`. A cinematic product
commercial, TVC, or brand film belongs to `modellix-tvc`. A still product shot or
poster belongs to `modellix-image-prompt-engineering`. A structured infographic
belongs to `modellix-infographic`. Files already on disk belong to
`modellix-ffmpeg` or `modellix-moviepy`.

## Route the request

Use this skill when the user wants a new ecommerce video that should feel like a
person filmed it on a phone: a talking-head review, an unboxing, a try-on, a
short list of variants, or a casual product clip with someone speaking.

Ask once for the product when the user names the format but not the item. Do not
invent a product, a price, a review count, or a performance claim to fill an
empty request.

Skip or keep the pass short when:

- The user already supplied a finished video prompt and asked only to run it.
  Pass that prompt to `modellix-design`.
- The request is a still image, a poster, or a product photo with no video. Use
  `modellix-image-prompt-engineering`.
- The request is a cinematic product commercial, TVC, or brand film. Use
  `modellix-tvc`.
- The request is a social card, cover, or thumbnail. Use `modellix-social-card`.
- The request is a structured infographic. Use `modellix-infographic`.
- The request is concatenation, trimming, a subtitle burn, or a title on files
  that already exist. Use `modellix-ffmpeg` or `modellix-moviepy`.

## Plan the video

Read `references/patterns.md` to choose the pattern. Read
`references/shot-prompts.md` before writing a prompt.

1. Copy the product facts that must appear. Keep every name, material, color, and
   claim the user supplied. Drop credentials, tokens, and secrets. Do not add a
   price, a star rating, a wear-time, or a medical claim the user did not supply.
2. If the pattern, spoken language, length, or cast is missing, ask once for the
   missing pieces together. A choice the user already named is the confirmation.
   Spoken language follows the audience. The brief itself stays in English.
3. Ask once whether a product still exists. When it does, name that file in the
   brief and tell `modellix-design` that every shot takes it as an input image.
   This skill does not upload the file.
4. Use 9:16 unless the user names another aspect. A 15-second video is four
   shots. A 30-second video is six shots. A listicle uses one shot per item the
   user named, plus a hook and a close, and the length has to fit that count.
5. Write one prompt per shot. Repeat the same cast lock in every prompt. Quote
   one spoken line per shot. Tell the model to leave captions, logos,
   watermarks, and writing on the package out of the frame.
6. List on-screen captions separately. They are burned by `modellix-ffmpeg`
   after the shots exist. Keep each caption to one or two short lines.

Until the pattern, spoken language, and length are confirmed, return the choices
and the facts you will keep, and leave the shot prompts empty.

## Brief

Return this brief:

```text
Ecomm UGC brief
- Market / spoken language:
- Placement / aspect:
- Length:
- Pattern:
- Cast lock:
- Product facts:
- Reference images: none | paths the user supplied
- Shots:
  1. Role / duration / spoken line / prompt
- On-screen captions: exact lines, for modellix-ffmpeg after download
- Next step: stop after brief | pass each shot prompt to modellix-design
- Model: <only a slug the user already named | omitted>
```

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for prompts, stop after the brief. If the original
request asked for the video, pass each finished shot prompt to `modellix-design`
and let that skill ask for a model, then own schema validation, credentials,
paid submission, waiting, and download. One shot is one generation. After those
files exist, concatenation and the caption burn belong to `modellix-ffmpeg`.

## Revision

When a generated shot misses, change that shot's prompt and return a new brief:

- Wrong claim: quote the user's fact again and drop the invented one.
- Words on the package or a misspelled caption inside the frame: repeat the
  instruction to leave writing out of the frame, and keep the caption in the
  `modellix-ffmpeg` list.
- A different person or room: paste the same cast lock again and regenerate
  that shot.
- Too many beats in one clip: split the action into the next shot.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate. This skill does not edit the downloaded file.
