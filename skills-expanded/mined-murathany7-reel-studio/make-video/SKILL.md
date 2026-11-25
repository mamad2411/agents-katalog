---
name: make-video
description: Make a marketing video, reel, ad, post or carousel for any brand in brands/. Starts as a conversation with the person (who it's for, the idea, voice, face, look), checks the idea against what makes reels work (hook in the first second, a voice, a face, the real product, a change every second, worth sending), then storyboard, approval, production, frame-by-frame QA and delivery. Use for any "make a reel / ad / post / video for <brand>" request.
---

# Making a marketing video

## How to talk (read this first)

The person is usually a **marketer, founder or creator, not a developer**. Act like a good producer sitting next
to them: curious, quick, opinionated, plain-spoken.

- **Talk about the video, not the machinery.** What people see, hear and feel; who it's for; what they do after.
  No file paths, commands, engine names, fps, codecs or "section 4 of the README" unless they ask. Do the technical
  work quietly and report the outcome: "Here's the first frame of each idea", "The video's ready: 18 s, 12 MB".
- **Ask back, a little at a time.** Never more than 2–3 questions in one message. Each comes with options and your
  pick: "Voice: your own (best), an AI voice, or music only? I'd go with your own." If they say "you decide", decide
  and say what you chose.
- **Show, don't describe.** A still of the idea beats a paragraph about it. Send pictures of the options, then ask.
- **Have opinions.** If an idea won't work on Instagram (see *What makes a reel work*), say so kindly and offer a
  better one. Never just do what was asked when you can see it will flop. Say why in one line.
- **Translate vague notes into a choice.** "Make it pop" → "More pop could mean faster cuts, a bigger first line, or
  brighter colour. Which one? (I'd do faster cuts.)"
- **Keep the person's words.** Their product names, their customer's words, their jokes.

## 1. The conversation (before anything is made)

First, silently: no `core/render.mjs` → run `setup`. Read `STATUS.md`. Find the brand in `brands/<slug>/` (README,
`compliance.md`); no brand yet → `new-brand` (also a conversation). Create the production folder from
`productions/_TEMPLATE/` (`REEL-###`, `POST-###`, never reused) and write what you learn into its README as you go.

Then talk, in this order. Skip what the request or the brand folder already answers, and say what you assumed.

1. **What and who.** What is this one for (a launch, a feature, awareness, an offer)? Who should stop scrolling
   for it? Where does it go (Instagram or TikTok, a post or a paid ad)? What should a viewer do after (follow, visit,
   buy, sign up)?
2. **The idea.** Pitch **2–3 ideas** in one line each, and recommend one. An idea is a moment, not a style: a
   relatable problem, a surprising demo, a satisfying build, a before/after, a joke, a myth busted. Each must pass
   "would someone send this to a friend?" Say which one you'd pick and why.
3. **Voice and face.** These matter most for reach (see below), so always ask:
   - "Should someone talk? Your own voice recorded on a phone works best. I can also do an AI voice (a free one
     right away, or ElevenLabs for a more natural one), or music only."
   - "Can you or someone be on camera for the first second or two, even a selfie? Or is there a mascot or
     character?" No to both: the product has to be the face.
4. **The look.** Show 2–3 style frames (pictures) that differ from each other and from the brand's last pieces
   (`node scripts/looks.mjs <brand>`, `looks/README.md`), with the real first line on them. Ask which feels right.
   A look is a *treatment* on the real product, never a template to fill in.
5. **The script.** A short plain table: time, what you see, what you hear, the words on screen. Then the 3 hook
   variants for the first second. Ask: "Shall I make it?"

**No production before a clear yes** to the idea, look and script. The first time in a project, offer the desk in
one line: "Prefer to review on a page? I can open one." (`review-desk`). Never tick approval yourself.

## 2. What makes a reel work (check every idea and script against this)

From what Instagram says it ranks (watch time, likes per reach, **sends per reach**) and published retention
studies (STATUS.md, 2026-11-04 research). Use it to push back, in plain words, when an idea misses these.

| | Rule | Why |
|---|---|---|
| 1 | **The hook is the first second.** Open on the outcome, the problem or the surprise, never on a logo, a title card or an empty frame. Cut any slow start | Viewers decide in about 1.5 s; Instagram reports a skip rate for the first 3 s |
| 2 | **A voice from the first second** when the piece allows it (own voice > AI voice > none) | Speech in the first 3 s: about 25% better 10 s retention than music-only openings |
| 3 | **A face or character on screen early**: the person, a mascot, a hand building it | About 10% better 10 s retention |
| 4 | **The real product, doing its thing**: screen recording, real CAD, real photo, real footage. Never placeholder shapes | Demos are what app and product reels that work have in common |
| 5 | **Something changes every 0.5–1.5 s**: a cut, a new angle, a word, a punch-in, on the beat. Each second gives something new | Retention drops when the rhythm gets predictable |
| 6 | **Worth sending**: useful, funny, relatable or surprising. A feature list is not | Sends are the strongest signal for reaching non-followers |
| 7 | **Captions as the headline** when there is a voice: big, few words, said words lit. Don't add a second headline on top | Text helps a little; too much text on a voiced piece distracts |
| 8 | **Ends so it loops**: the last frame leads back into the first | Rewatches count as watch time |
| 9 | **Clean, bold images**: little grain, no fine noise, text 40 px+. Instagram re-encodes at about 3.5 Mbit/s | Grain and thin detail turn to mush after upload |
| 10 | **Original**: no watermarks, no reposts, no other brands' clips | Unoriginal content isn't recommended |

Length: 15–20 s for most pieces, up to ~40 s when it teaches something with a clear payoff.

## 3. Produce (quiet work; tell the person only what they'd care about)

| Step | How |
|---|---|
| Plates | 3D: `scene-3d` skill (Three.js live, or Blender → MP4). Live site or app: `capture-site` skill. Footage: `Studio.video` |
| Character | `character-2d` skill (SVG rig, Lottie, Rive, lip sync) |
| Voice | The person's recording → `audio/vo.wav`. AI, free and local: `audio/script.json` (lines with start times) → `python3 scripts/voice.py audio/script.json audio/vo` → `vo.wav` + `vo.json` (word times for captions; it warns when a line runs into the next). AI, better: ElevenLabs MCP (`.mcp.json`). Disclose AI voices where the platform asks |
| Audio | Music and SFX → `audio/`. Cue sheet `audio/cues.json` → `python3 scripts/mix_audio.py audio/cues.json audio/mix.wav` (ducks music under the voice). Word timings from a recording: `scripts/transcribe.sh`. Mouth shapes: `scripts/lipsync.sh` |
| Beat grid | `node scripts/beats.mjs audio/music.mp3 audio/beats.json`; in the composition `await Studio.beats(...)`, cut on `Studio.bar(n)` / `Studio.beat(n)` |
| Captions | `Studio.captions(el, "../audio/vo.json", { style: "karaoke" \| "pop" \| "highlight", upper, maxChars, lines, gap })`. One spoken phrase per caption page: check the stills for a sentence split across pages |
| Composition | `composition/index.html`. Start from the chosen look's starter (or blank), not an earlier production, unless the piece is a deliberate variant of one (say so). The starters are 5 s sketches: the product, the voice and the pacing come from this piece's script. Load `/core/lib/base.css`, `/brands/<slug>/tokens.css`, `/looks/<look>/look.css` (+ `/looks/fx.js`). Patterns: `examples/engines-demo/`, `examples/reel-layer/`. Text inside `.safe` (paid) or `.safe-organic` |
| Formats | `Studio.setup({ …, formats: ["4x5", "1x1", "16x9"] })`; per-format CSS under `.fmt-4x5`; `Studio.pick({...})` |
| Render | `node core/render.mjs video <comp> export/<ID>-<lang>.mp4 --audio audio/mix.wav` (posts: `still`; other formats `--formats all`). 30 fps. Bitrate is capped at 12 Mbit/s |
| Motion blur | For fast moves: `Studio.setup({ …, motionBlur: true })`; `--motion-blur 1` for quick checks |

Send the person something to look at along the way when it helps them steer (a few frames, a rough cut), with one
question at most.

## 4. QA (never skip; the person only hears the result)

1. `scripts/qa-video.sh export/<ID>.mp4 qa` → `qa/report.md`. Every ❌ fixed. Every jump an intended cut or fixed.
2. `node core/render.mjs text-qa <comp> qa` → `qa/text.md`: hook readable at once, text ≥ 28 px (aim 40+),
   contrast, nothing under the Reels UI. Every ❌ fixed or explained. Look at `qa/flagged/text_*.jpg`.
   `node core/render.mjs layout-qa <comp> qa` → `qa/layout.md`: text cut off by its box or the stage, words split
   across lines, text over text or over the logo, things outside `.safe`, broken images. Every ❌ fixed; mark an
   intended case on the element (`data-qa-lines="2"`, `data-qa-ignore="overlap"`) and say why in the README.
3. `node core/render.mjs stills <comp> qa/beats --at <beats> --safe`, and **look at each one**: safe zone, nothing
   cut off, no half-loaded asset, no overlap, spelling, captions whole, the look held throughout.
4. Determinism spot check with WebGL or plates: one frame twice, same md5.
5. Listen once: voice in sync with captions (and mouth), music under the voice, −14 LUFS.
6. Fact check: every claim has a source in the brand README. `compliance.md` passes.
7. **The hit check**: go down *What makes a reel work* and note in the README which rules the piece meets and which
   it can't (e.g. "no face: the person declined"). Tell the person the one thing that would make it stronger.

## 5. Deliver

To the person, in plain words: the video (and other formats), its length and size, a suggested post caption and
first comment, and **one thing to test next** (usually a second hook: "Post this one, then try the version that opens
on the replay; whichever holds people longer wins").

Quietly: README sections 5–7 (log, fact check, rebuild commands), status `delivered`, `STATUS.md` row and anything
learned in *Learnings*.

## Defaults

| | |
|---|---|
| Reel / video ad / Story | 1080×1920, 9:16, 30 fps CFR, H.264 ≤ 12 Mbit/s, −14 LUFS. Paid 9–20 s, organic 15–45 s |
| Post / carousel | 1080×1350, 4:5 |
| Safe zone, paid Reels | top 14%, bottom 35%, sides 6% (`.safe`) |
| Safe zone, organic Reels | top 11.5%, bottom 22%, left 6%, right 11% (`.safe-organic`) |
| Voiced pieces | Burned-in captions: many people watch with the sound off |
| Silent pieces | Only when the person chooses it. All meaning on screen; captions ≥ 42 px; each line held ≥ 1.5 s |
| Other formats | 4:5 1080×1350, 1:1 1080×1080, 16:9 1920×1080 |
