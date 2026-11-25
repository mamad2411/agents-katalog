---
name: modellix-social-card
description: Plan prompts for social cards, covers, and carousels on mainstream networks. Use this skill whenever the user wants a Xiaohongshu, WeChat Official Account, Weibo, Douyin, Bilibili, X, Twitter, Instagram, Facebook, LinkedIn, YouTube thumbnail, TikTok, Threads, Pinterest, Snapchat, Bluesky, Reddit, WhatsApp Status, or Telegram card, cover, or carousel — even if they only say "social post image", "thumbnail", or "carousel". Turn the source into one image prompt per placement, with exact on-image text and aspect ratio, then hand generation to modellix-design. Skip article covers with no named network, in-article illustration sets, casting boards, knowledge comics, generic posters, video edits, and requests that only need execution of an already finished prompt.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: social-card,thumbnail,carousel,prompt-engineering,modellix
---

# Modellix Social Card

Turn a note, article, or announcement into prompts for social cards. This skill
plans the cards. `modellix-design` generates them.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. Catalogs
change quickly, and choosing a model is outside this skill. When the user wants
the images made, finish the brief first and then hand each prompt to
`modellix-design`.

A cover, thumbnail, or carousel for a named network stays here. A set of
illustrations placed through an article, with no named network, belongs to
`modellix-article-illustrator`. A casting board with no named network belongs
to `modellix-casting`. A structured infographic belongs to
`modellix-infographic`. A poster, product shot, or illustration that is not an
information diagram belongs to `modellix-image-prompt-engineering`. Files already
on disk belong to `modellix-ffmpeg` or `modellix-moviepy`.

## Route the request

Use this skill when the user wants a card, cover, thumbnail, or carousel for a
specific network, or when the wording is "social post image" even if they have
not named the network yet.

Skip or keep the pass short when:

- The user already supplied a finished prompt and asked only to run it. Pass that
  prompt to `modellix-design`.
- The request is an article, blog, or newsletter cover and does not name a
  network placement. Use `modellix-cover-image`.
- The request is a set of illustrations placed through an article and does not
  name a network placement. Use `modellix-article-illustrator`.
- The request is a casting board or turnaround lookbook and does not name a
  network placement. Use `modellix-casting`.
- The request is a knowledge comic, educational comic, biography comic, or
  four-panel strip, and does not name a network placement. Use `modellix-comic`.
- The request is a poster or illustration with no platform. Use
  `modellix-image-prompt-engineering`.
- The request is a structured infographic. Use `modellix-infographic`.
- The request is a commerce UGC video that still needs a shot plan. Use
  `modellix-ecomm-ugc-video`.
- The request is video editing, subtitles, credentials, task status, or a download.
- The user wants an avatar or a profile banner. Say those placements are outside
  this skill and ask which content card they want instead.

If the platform is missing, ask once which network and placement they mean, then
continue. Do not invent a platform.

## Plan the cards

Read `references/platforms.md` for the aspect and safe area. Read
`references/card-planning.md` when the source is long or the post needs more than
one card.

1. Name the placement. One placement gets its own prompt. A second network gets a
   second prompt with its own crop and line breaks. Do not tell the user to crop
   a landscape card into a portrait.
2. Compress the source into one claim, then one idea per card. The image carries
   the hook. The caption keeps the nuance.
3. Pick one visual stance for the set: editorial, systematic, photographic, or
   poster. Describe it in ordinary design language. Keep that stance on every card.
4. Write the exact words that will appear on the image. Quote them. Name the
   language. The prompt must tell the image model to copy those words and not add
   captions, logos, watermarks, or extra claims.
5. Use only facts from the source. Leave out prices, dates, and percentages the
   user did not supply.

A carousel should change jobs from card to card: hook, problem, contrast,
checklist, evidence, quote, close. Repeating the same title-and-bullets layout
makes the set feel like unfinished slides.

On-image language follows the audience. This skill's own brief stays in English.
A Chinese Xiaohongshu card still quotes Chinese text inside the prompt.

## Safe type

Image models can render short, exact text when the prompt is strict. They still
fail when the card is crowded. Keep on-image copy short, put the largest line
first, and keep words inside the safe area from `references/platforms.md`.

- A 9:16 story, reel, or short-video cover keeps type in the middle. The top,
  bottom, and right edge belong to the app interface.
- A YouTube thumbnail keeps the lower-right corner clear for the duration badge.
- A WeChat headline cover is a thin band. Use one short line, and compose the
  square secondary cover as its own image.
- An Instagram, TikTok, or Shorts grid crops toward the center. Put the claim in
  that center band.

If the user has no photo, ask once whether the card should be type-led or include
a generated scene. Accept the answer. A generated scene stays free of extra text
so the quoted words are the only words in the image.

## Brief

Return this brief:

```text
Social card brief
- Platform / placement:
- Aspect:
- Audience language:
- Visual stance:
- Cards:
  1. Role / exact on-image text / prompt
- Next step: stop after prompts | pass each prompt to modellix-design
- Model: <only a slug the user already named | omitted>
```

Each card prompt is one finished flat image. Include the aspect, the stance, the
subject, the quoted text, which line is largest, and the safe area. Mark pixel
sizes as unverified unless a current platform page was checked.

Leave `Model` blank unless the user already named a slug. Do not browse the
catalog from this skill.

If the user asked only for prompts, stop after the brief. If the original request
asked for the images, pass each finished prompt to `modellix-design` and let that
skill ask for a model, then own schema validation, credentials, paid submission,
waiting, and download.

## Revision

When a generated card misses, change the layer that failed and return a new brief:

- Wrong claim: rewrite the hook.
- Extra or garbled words: shorten the quoted text and repeat the copy instruction.
- Type in the chrome: move the words into the safe area.
- Inconsistent set: restate the same stance on every card.
- Wrong crop: write a new prompt for that placement instead of cropping the file.

`modellix-design` decides whether an existing task can be recovered or a new
submission is appropriate.
