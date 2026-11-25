---
name: matchcut
description: Use when making any short video for a software product or project - a launch film, hackathon entry, demo reel, product walkthrough, feature clip, trailer or social teaser - especially one that should look made by a studio rather than screen-recorded. Covers films built only from the real product, films that open on AI-generated cinematic shots and match-cut into the real product, and generated story shorts. Start here; it routes to keyframes, clip-prompts, ui-reel and score.
---

# matchcut

A matchcut film earns attention with a picture, then proves itself with the real thing. The signature move: one
object from a generated story (a card, a key, a message, a badge) lands flat to camera, and the next frame is
the same object alive in the real product. Everything after is real footage, recorded so every frame is smooth,
cut like a trailer, with its own music.

| Part | Skill |
|---|---|
| Stills: style, cast, shots, the hero object (any image model) | `keyframes` |
| Animating stills into clips (MiniMax, Grok, Seedance, Veo, Kling, Wan, Runway, Luma, LTX) | `clip-prompts` |
| Recording the real product at 60 fps and cutting it with a virtual camera | `ui-reel` |
| An original soundtrack, recorded effects, a voiceover | `score` |

## Pick the film

| Film | Length | Made from | Skills |
|---|---|---|---|
| **Product reel** | 15 to 45 s | a title intro made in code, then the real product (the demo film) | `ui-reel`, `score` |
| **Matchcut film** | 45 to 90 s | a generated cold open, the match cut, the real product | all four |
| **Story short** | 10 to 30 s | generated shots only (a teaser, a mascot moment) | `keyframes`, `clip-prompts`, `score` |

Ask at most three questions, and only if the product, the film or the length is missing: what it is, where it will
be posted, and whether there is a cast or a mascot.

## The run

1. **Find the hero object.** One thing that exists in the product and could exist in a story. Render or screenshot
   the real one at full size, front and back if it has two. The film is built around this object.
2. **Write the beats** in one short message and get a yes. Offer a move for each beat from `references/moves.md`,
   name the 3 to 5 **heroes** (the moments that land exactly on the music with the biggest sounds: usually the match
   cut, the payoff and the end card), and answer its five questions in a line each before sending. For a matchcut
   film:

   | Time | Beat |
   |---|---|
   | 0 to 18 s | Cold open, 3 to 6 clips, letterboxed 2.39:1: the world, the detail, the subject growing until it fills the frame the product will match |
   | 18 s | The match cut: the object flat to camera, a bloom, the same object in the real UI |
   | 18 to 55 s | The real product in 3 to 5 shots, one caption each |
   | 55 to 65 s | A payoff on the beat (all the tiers, all the results, the before and after) |
   | 65 to 74 s | End card: the name, the install line or URL, one true fact |

   A product reel has no generated pictures: it opens on a title intro made in code (`intro` in `tl.json`): dots
   land as the product's wordmark, a cut line splits it, and the dots swirl into the product's first shape as its own
   entrance takes over. Then its best moment.
3. **Stills** (`keyframes`): the style approved on the first image (and a line-up first if people appear), then one shot
   per message.
4. **Record the product** (`ui-reel`) while stills generate. The first take opens on the hero object at the size
   and place the last generated frame leaves it.
5. **Clips** (`clip-prompts`): one self-contained prompt per clip, generated at the model's shortest useful length
   and trimmed in the edit.
6. **Score** (`score`): written to the same timeline, a stop before the match cut, effects on clicks and cuts, the
   heroes on the beat with a hit and a tail each, everything else free to breathe.
7. **Cut** in Remotion with the reel template (the cold open goes in `tl.json` `opening`, the bars in `bars`), or render the product section on its own and let the person join it
   to their cold open in their editor (ask which before the last render).
8. **Check**: a storyboard of every take, `npm run check`, a contact sheet of the render, the five questions in
   `references/moves.md` asked again of what was rendered, the render measured with `measure.py` (in `score`: every
   hero lands its hit, 12 to 16 dB of peak-to-loudness, a pace that suits the film), then deliver.

## Deliver

- The master, 1920 x 1080 at 60 fps, and a 720p30 preview under 30 MB for phones and chat apps.
- Square and vertical cuts for socials from the same timeline (move the camera targets; never squash).
- A poster still and a short GIF for READMEs.
- For a person finishing in their own editor: the letterbox spec. Canvas 1920 x 1080; a 2.39:1 picture is
  1920 x 804 with 138 px bars top (y 0 to 138) and bottom (y 942 to 1080). Keep the bars through the cold open
  and open them on the match cut; the reel template retracts its own bars from `tl.json` `bars`.
- If they post it: a short post in their own voice, the film attached, the link last.

## Rules

- **The product is real.** Every product frame is a recording of the real code. Never a mock-up, a redrawn UI or
  someone's private account. Demo data comes from a throwaway profile the film seeds itself.
- **People and characters.** A real person becomes a character only with their consent, from their own public
  avatar. A licensed character (a famous mascot) becomes an original lookalike; say why.
- **Every film gets its own music.** New key, tempo and instruments each time.
- **Test browsers are isolated.** Headless, muted, a throwaway profile, never the person's own browser.
- **Nothing goes public without a yes.** Posts, repos, uploads and forms are the person's call.
- **Exists early, then improves.** The whole film renders end to end before any one shot is polished. When a
  generated clip will not behave, hold its still with a slow push-in and move on.
