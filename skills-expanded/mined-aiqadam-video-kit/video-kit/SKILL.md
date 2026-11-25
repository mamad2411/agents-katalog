---
name: video-kit
description: Make or change a promo, pitch, product or explainer video with AI Qadam Video Kit (HTML scenes rendered by HyperFrames; licensed footage, photos and music fetched by reference; voice by ElevenLabs, OpenRouter or a free local engine, checked by transcription). Use for any request to make a video, a clip, a teaser, an ad or a screencast-style demo, and for edits to a video in videos/: new scene, new text, other language, vertical version, faster, re-voice.
---

# Making a video with the kit

A video here is code. Scenes are HTML; motion is a function of time, so every frame can be
rendered again exactly; text, timing and language change without re-shooting anything.
One file, `video.json`, holds all timing, and the kit derives everything else from it.

## The work, in order

1. **Brief** (`references/brief.md`). Find out what the video must say, to whom, in what
   shape and language. Ask only for what the request and the materials do not already
   answer; write it into `videos/<name>/brief.md` with a source for every fact.
   Start the folder with `node kit.mjs new <name> --format … --lang …`.
2. **Timeline** (`references/video-json.md`). Split the video into 4–12 scenes of
   4–12 s. Write the voice lines into `video.json` with their start inside the scene.
   Run `node kit.mjs plan <name>` and read it: lines must not overlap, gaps stay under
   `maxSilence`.
3. **Media** (`references/media.md`). Gather what the scenes show: the person's own
   materials first, then licensed footage, photos and music with `node kit.mjs media
   search` and `media add`, which record the license and make a preview to look at. For
   anything sensory (food, places, rituals) real footage beats drawings.
4. **Scenes** (`references/scenes.md`). One file per scene in `compositions/`. Read the
   example's scenes in `videos/tutun-lounge/compositions/` first: footage cut on the
   beat, kinetic type, captions per shot. For a software product, redraw its screens in
   HTML from its source or screenshots and act out taps and typing ("Product screens");
   `videos/kit-promo/compositions/` does this for a terminal, files and a player;
   `videos/qatnov/compositions/` for a mobile app in an iPhone (camera moves in on each
   tap, screens push in, notifications arrive), with footage in arch frames between;
   `videos/naryad/compositions/` for the same in portrait, with footage in rounded cards.
   For a vertical video told in captions without a voice, read
   `videos/ottoman-empire/compositions/`: archive images that pan and push in, a year
   that rolls forward, a timeline across the top.
   For a music video with no words, read `videos/dutar-protocol/compositions/`: one
   photographed stage, a camera and light per section of the track, threads drawn on a
   canvas that move with the music (`s.audio`).
5. **Look** (`references/review.md`). `node kit.mjs check <name>`, fix every error, then
   `node kit.mjs stills <name>` and read the PNGs. Repeat until the frames are right.
6. **Voice and sound** (`references/voice-and-sound.md`). The narration tells the story
   the pictures do not; it never reads the captions. Pick the provider and voice with
   the person: list two or three in `voiceSamples`, run `node kit.mjs voice <name>
   --samples`, and let them choose by ear.
   `node kit.mjs voice <name>` makes the lines that changed and checks each take by
   transcribing it back. The real lengths replace the estimates; run `plan` and `check`
   again and move lines that now collide.
   Music is a track the person gives, a licensed one (`media search --type audio`), or one
   generated from a description (`node kit.mjs music <name> --samples`, then `--use`);
   let the person choose it by ear too, and cut scenes to its bars.
7. **Render** with `node kit.mjs render <name>`. Report the file, its length and loudness,
   and say plainly that you have not watched or listened to it.

Before the person has approved the frames, show stills rather than rendering again and
again. Offer `node kit.mjs preview <name>` when they want to scrub through it themselves.

## Rules

- **Facts come from the brief.** No number, claim or feature that is not in `brief.md`.
  Captions never contradict the picture.
- **Readable on a phone.** Text that must be read is at least 28 px at 1080 px on the
  short side; keep it inside the central 90% of the frame.
- **Deterministic.** No `Date.now()`, `Math.random()`, timers, network calls or CSS
  transitions in scenes: everything visible is computed from `t` in `kit.scene`.
- **Unique ids.** Prefix every id in a scene with the scene id (`order-btn`, not `btn`).
- **Credits.** Every outside file is credited: `media add` writes it into
  `assets/sources.json`; a file you put under `assets/` yourself gets a line in
  `assets/CREDITS.md`. CC BY material is credited on screen or in the published
  description (`references/media.md`).
- **Silence is short.** Narrated videos keep gaps between lines under about 5 s.
- **Nothing harness-specific.** Use `node kit.mjs …` commands; they work the same for
  any agent and any operating system.

## References

| Read | When |
| ---- | ---- |
| `references/brief.md` | starting a video; what to ask; recording facts |
| `references/video-json.md` | scenes, lines, sounds, music, theme, fonts, languages, formats |
| `references/scenes.md` | writing a scene; the `kit` API; product screens; camera; vertical |
| `references/voice-and-sound.md` | voice providers, models per language, pronunciation, music, mix |
| `references/media.md` | finding footage, photos, music and fonts you may use; `media` commands; credits; logos |
| `references/review.md` | checks, stills, what to look for, delivery note |
| `references/pitfalls.md` | mistakes that already cost time |
