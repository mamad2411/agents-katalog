# Genex models at play time in AI Game Studio: the first step

You are building inside AI Game Studio. Below the upstream marker is Genex's card on the play-time
model lane, with the passages of advice Studio does not ship taken out. Where it disagrees with
this preface, this preface wins.

- `npx genex llm models`: `genex__cli {"command":"llm models"}`. `npx genex doctor`:
  `genex__cli {"command":"doctor"}`, or `genex__asset` with operation `status`.
- `npx genex init --convert` does not apply in Studio. A game becomes a hosted Genex game when you
  publish its first draft with `genex__publish {"operation":"draft"}` (the user approves it).
- Then read the full procedure with `genex__skill {"name":"genex-llm-in-games"}`.
- Other commands map onto Studio tools as the `genex` skill describes
  (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-tool-llm/SKILL.md v1.40.0 sha256 aea8c0be5ca9c270a47d59b132c1774f9ae30e8f0d3df5abca832f3abcf55ae7 -->
---
name: genex-tool-llm
description: A language model running while somebody PLAYS the finished game — an NPC that answers in its own words, a quest written from what the player typed, a prompt box in the game. On Genex the player pays and approves it, so this is a platform feature, never a key on the author's meter.
---

# Genex Tools · Models at play time

This card is about a model that runs **while somebody plays the finished game**
— not about generating art while you build it. "Make me a picture, a model, a
voice line" is the asset belt: use the lane card for it and stay here only if a
model has to run for the player.

## What the platform does

A game hosted on Genex can call a language model from inside the running game
and get back text or JSON. **The player pays and the player approves**: credits
from their Genex account, billed as each call is used and never past the
per-call ceiling the game declares, or their own Claude / ChatGPT subscription,
chosen on an approval sheet Genex draws that the game cannot render, skin or
bypass. Either one call at a time, or one standing budget the player approves
once and the game then spends against without another popup. The game holds no provider
key, sees no credential, and never talks to a model vendor.

That is the whole reason this is a platform feature and not something you wire
up here: an unhosted folder has nowhere to put a key that is not the author's
own.

## Recognise the request

Any of these means a model at PLAY time, however it is phrased:

- NPCs that talk, answer, argue, or decide in their own words
- anything written from what the player types — a name, a wish, a command, a question
- a prompt box, a chat panel, an "ask the oracle" widget inside the game
- quests, items, dialogue, or levels generated per save or per run
- "let the player choose a model", "use my API key in the game", "hook a chatbot into it"
- a judge, a grader, or a referee that reads free-form player input

## Building it

1. `npx genex llm models` — whether this stand serves the lane at all, and
   which models. It answers in this folder as it is, before anything is
   converted, so it comes first: if it says the lane is off, in-game calls
   answer 404 here. It prints
   the FEATURED models; `--all` lists the whole catalog. Whatever model is picked, the picker in the game
   shows the server's own label for it — a name you invent is a name that
   differs from the model they are billed for.
2. `npx genex init --convert` — it connects this folder to a hosted Genex game
   in place. The code, the files and this toolkit stay exactly as they are, and
   generations still land in `./assets`. It is the user's yes that runs it, so
   ask before you do if you have not already.
3. Load `$genex-llm-in-games` — it arrives with the conversion and owns the
   build: the SDK surface, one-time calls versus a standing budget, measuring
   the per-call ceiling before the game declares it, and honest handling of
   every refusal.

**The game has to be a static browser build.** A hosted game is files served
from the edge; there is no server of yours inside it. So the familiar pattern —
a small local Express/Flask app that holds a key and proxies the model — works
on your machine and can never ship. Calling `generate()` from the browser is
the shipping shape of that idea.

## No author key

A shipped game never calls a model on its author's credential: not a key in `.env`, not a
local proxy, not the author's own account behind a fetch. A shipped game
carrying the author's credential means every visitor spends the author's money,
with nobody approving anything and no limit on it — and the credential is
readable in the bundle.

## The honest boundary — text and JSON only

Player-funded generation returns **text or JSON**. Nothing else.

- **"The player types anything and gets a 3D model, paid by them"** is not a
  thing on this platform.
- 3D models, images, textures, video, music, voice and characters are the ASSET
  lanes of this toolkit: you generate them while you build, on the user's own
  meter, and they download into `./assets` and ship inside the game. What is
  live and what it costs: `npx genex doctor`.
