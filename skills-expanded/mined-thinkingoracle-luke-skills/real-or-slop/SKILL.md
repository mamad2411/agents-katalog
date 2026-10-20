---
name: real-or-slop
skill_id: browser-skill:real-or-slop
description: Whether that clip is real, generated, or old news in a new caption
when_to_use:
  - intent_keywords: [is this real, ai generated, fake, slop, did this happen, verify, real footage]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: whether it actually happened and who first reported
    capability_target: web_search
    mutation_boundary: read_only
  - caption: fact checks, original uploads and debunks of
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_clip
    current_value: how to tell if a video is AI generated
    fill_rule: describe or paste what you were sent and Luke goes looking
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [verify, ai, misinformation, group chat, culture]
    related_skills: [browser-skill:trace-the-screenshot]
platforms: [macos]
---

# Real or slop

## Purpose
On demand, in the ten seconds before you hit send. There are two ways to look
silly in a group chat this year: forwarding a generated clip as news, and
loudly calling a real thing AI. This checks which one you are about to do.

## Reads
- Search results for whether it actually happened and who first reported how to tell if a video is AI generated.
- Search results for fact checks, original uploads and debunks of how to tell if a video is AI generated.

## Lands in
- Separates the four failure modes. Short enough to act on straight away.

## Steps
1. Look up whether it actually happened and who first reported how to tell if a video is AI generated.
2. Look up fact checks, original uploads and debunks of how to tell if a video is AI generated.
3. Separates the four failure modes. Real footage with a lying caption is now the most common one, and it survives every AI detector because it is real.

## Success criteria
- Separates the four failure modes. Real footage with a lying caption is now
  the most common one, and it survives every AI detector because it is real.
- Refuses to treat "it looks off" as evidence. People confidently called an
  actual Monet an AI fake in front of seven million viewers, so vibes lose.
- Names what would settle it when the answer is not there, instead of picking
  a side to sound decisive.
- Gives the user a line they can send with the verdict, so the correction lands
  as friendly rather than smug.

## Failure behavior
- If it genuinely cannot be settled, say unresolved and say what is missing.
- If a source will not load, skip it and keep going.

## Never
- Never sign in, post, reply, report or share anything. The user sends it.
- Never invent a source, a debunk, a date or a confidence level.
- Never punch down, and never turn a wrong forward into a case against a person.

## Redaction
Omit query strings, account details, handles the user has not mentioned, and
anything shown after a page unexpectedly asks for a login.
