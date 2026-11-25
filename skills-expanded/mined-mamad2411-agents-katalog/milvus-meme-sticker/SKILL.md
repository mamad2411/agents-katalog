---
name: milvus-meme-sticker
description: Create tiny no-text Milvus-style sticker memes for technical marketing, WeChat-style article moments, community posts, and developer-group reactions. Use when the user wants an original meme/sticker with an abstract Milvus bird/eagle mascot, strong exaggerated emotion, internet-native sticker energy, light-blue accents without making the whole character blue, and deterministic small-size exports such as 512, 240, 120, or 50 px.
---

# Milvus Meme Sticker

Create original sticker-style memes for technical marketing moments. The output should feel like something people would send in a developer WeChat group: compact, expressive, funny, emotionally resonant, and safe to publish because it does not reuse existing meme templates, celebrities, screenshots, anime, or other IP.

Read `references/style-guide.md` before generating the first sticker in a session.

## Workflow

1. Identify the emotion from the source paragraph or user request: overwhelmed, confused, relieved, proud, shocked, exhausted, or "why is this so hard?".
2. Generate three square variants first unless the user asks for one exact direction.
3. Use an abstract Milvus bird/eagle mascot as the recurring character, not a logo copy.
4. Keep the image text-free. No captions, labels, letters, UI words, fake code snippets, or speech bubbles with text.
5. Prefer a compact sticker composition with a clear silhouette and large readable facial expression.
6. Save the best or selected source image at high resolution, then run `scripts/resize_sticker.py` to export true sticker sizes.
7. Insert or deliver the small exported image, not only the large generation.

## Prompt Rules

Use prompts like this, adapting only the emotion and scene:

```text
Square 1:1 sticker-style meme illustration, no text, no letters, no captions.
Original abstract mascot inspired by a Milvus-like bird/eagle, simplified and
not copying any exact logo. The character has a light body with only partial
soft blue accents, a non-blue beak and mouth, oversized expressive eyes, and a
funny exaggerated [EMOTION] expression.

Scene: [SCENE]. Developer-group chat sticker vibe, hand-drawn, thick clean
outline, white sticker border, compact composition readable at small size.
Use a light-blue accent palette with colorful secondary accents; do not make
the whole character blue. No real brands, no existing meme templates, no
celebrities, no screenshots, no IP characters, no text anywhere.
```

## Style Guardrails

- Keep the mascot abstract: bird/eagle-inspired, rounded and sticker-like, not a realistic animal and not a copy of any official mark.
- Use light blue as an accent, not as a full-body flood. Avoid blue teeth, blue mouth interiors, or an all-blue face that loses expression.
- Make the beak, mouth, eyes, sweat, and emotion marks clearly separated in color and value.
- Favor expressive face and body posture over detailed props.
- Use props only when they explain the pain point: documents, connector plugs, database cylinders, cloud buckets, chat bubbles, tickets, code brackets.
- Avoid text because this sticker must travel across languages and stay legible at tiny sizes.
- Avoid photorealism, 3D toy rendering, glossy mascot branding, and polished corporate illustration. It should feel like a hand-drawn sticker meme.

## Small-Size Export

Generated images are usually too large to feel like real stickers. Always create small derivatives after generation:

```bash
python3 scripts/resize_sticker.py path/to/source.png --out-dir path/to/output-dir
```

Defaults create:

- `512x512` for article insertion when some detail should remain visible.
- `240x240` for WeChat-style sticker main image scale.
- `120x120` for thumbnail checks.
- `50x50` for tiny panel legibility checks.

Use the smallest version that still reads in context. For Markdown articles, prefer `240x240` or `512x512` plus explicit display sizing if needed.

## Quality Check

Before showing the final result, inspect the image and verify:

- No visible text or pseudo-text.
- The mascot is not entirely blue.
- The mouth, beak, eyes, and expression are readable.
- The emotion is obvious even at `240x240`.
- The sticker silhouette is compact and not too busy.
- The image does not resemble a known meme template, celebrity, anime, or existing IP character.
