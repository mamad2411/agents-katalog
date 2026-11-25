---
name: product-motion-ads
description: "Style for edit-video: a vertical motion-graphics ad built in code from the product itself (its app, site, screenshots, product photos, packaging or renders), with an optional voiceover and every sound on its frame. No camera footage needed. Use when a creator wants to promote a product, physical or digital (a gadget, a bottle, an app, a SaaS tool, a template or free resource), a comment-to-DM giveaway, or asks for a motion-graphics or launch video for Reels, TikTok or Shorts, or a 16:9 launch film for a landing page or YouTube."
---

# Product motion ads

A style on top of `edit-video`, which owns the voice, captions, sound mix and
review. The whole reel is motion graphics made from the real product: its
interface or its photos and packaging, its copy and its flow, animated as one
continuous piece where each scene turns into the next, with sound locked to the
picture. This skill is a method, not a template: the product decides what appears,
and you design every scene for it.

Fits a reel that sells or explains one product: a physical one (a gadget, a
bottle, a bag), an app or SaaS tool, a template, a free resource behind a comment
keyword. Skip it when the creator's face carries the story (use a footage style)
or the product has nothing to show yet.

The same method makes a 16:9 launch film for a landing page or YouTube. Build the
scenes once and cut the vertical reel from them, re-laid for 1080×1920, rather than
starting over.

## Creative laws

- **The first second decides.** Frame 0 must look finished and already say what
  the reel is about: the hook in large type over the product's world, the product
  visible. Never an empty canvas, a logo sting or raw code/markdown, which reads as
  broken formatting. Then keep the opening moving: in the first ~10 s, keep the
  pauses between voice lines under about 0.9 s. A 1.5 s silence there reads as the
  place to leave. Close a gap by trimming the scene's tail, not by re-timing its
  animation.
- **Show the product in use.** Entry → key action → result beats a page
  describing it: open the app → the key action → the result, or pick the bottle
  up → use it → what it gives you. Reuse the real interface or product photos,
  copy, colors and assets; rebuild only what you can't reuse. No abstract filler.
- **Show where it lives as itself.** When the product works inside another app (an
  AI assistant, a terminal agent, a chat tool) or a real setting (a kitchen
  counter, a desk, a gym bag), make that place recognizable at a glance. For an
  app: its official mark, from files the creator supplies and never altered, and
  its real interface language, such as a terminal agent's transcript or a chat
  app's own window and controls. For a physical product: true proportions,
  materials and scale next to familiar objects. A neutral stand-in reads as
  generic.
- **Every claim is grounded.** Names, numbers, features and quotes must exist in
  the product, its README or UI, its packaging and spec sheet, or the creator's
  brief. So must every detail: use the exact labels, states, colors and finishes,
  and never show a screen, feature, flavor or size the product doesn't have.
  Hooks, jokes and connective lines are free to invent; claims are not. Label a
  mockup or a staged demo as an example on screen.
- **One object carries the story.** Each scene turns into the next through
  something the viewer is already watching: a file falls into a screen and becomes
  a chip, an input grows into the prompt card, a card flips into a DM. A cut to an
  unrelated layout restarts attention. See [motion](references/motion.md).
- **Readable at speed.** Pace comes from motion, not from pulling text early: a
  short label holds ~0.8 s settled, a sentence ~0.3 s per word.
- **Sound on the frame.** Every hit plays on the first frame that shows its event.
- **One look.** The product's palette and type (or the creator's brand), one
  accent, consistent motion. Keep critical text inside `edit-video`'s safe area.
- **An honest ending.** The call to action matches what the creator actually
  offers: a comment keyword that really sends the thing, a link that works, a
  limit or price they will honor.

## The creator's direction comes first

The laws above are defaults for when nobody has said otherwise. A creator's brand
guide, style notes, reference reel or approved script overrides them: their fonts,
colors, pacing, transitions and wording win, even where they differ from these
defaults (hard cuts instead of handovers, a logo first, a longer read). Only the
truth rules don't bend: grounded claims, labelled examples, an honest call to
action. When their direction would hurt the ad, build it their way and say why
in one line.

- **Guides.** Read the whole guide or reference before planning, write the rules
  you'll follow into the plan, and check the render against that list.
- **Feedback.** Turn each comment into a concrete change in the plan, revise the
  next numbered version, and leave everything they didn't mention alone (copy,
  timing, sound). Re-check the scenes you touched and the handovers next to them,
  then report what changed for each comment. If a comment is unclear, make your
  best reading and say which one you chose. For "a bit faster" overall, change the
  tempo (step 7) instead of re-timing every scene.

## Workflow

Use the run folder `edit-video` creates (`scripts/new-edit.mjs`, or the existing
one when revising): the plan goes in `analysis/`, product material in `assets/`,
the composition, voice and mixes in `work/`, renders in `previews/`, finished
videos in `exports/` and reviews and sync strips in `reports/`. Number every
revision (`ad-v01`, `ad-v02`, …) and keep the earlier ones.

1. **Inspect the product** and the creator's brief.
   - **Software:** read its code (main page, styles, routes, key components) or
     capture its site, plus any screenshots and demo clips. Read the code on the
     default or deployed branch after a fetch, not whatever the local checkout
     holds; one was 172 commits behind.
   - **A physical product:** photos from several angles (or renders), packaging and
     label art, the spec sheet and the brand's site.

   Note the exact colors and fonts, the strongest visual, the copy you may quote
   and the 2–3 beats of the product in use. Never carry secrets, tokens, internal
   URLs or real customer data into the ad; swap in plausible stand-ins and say so.
   - **Facts before story.** List the exact labels, states, screens or variants
     the story touches, and what doesn't exist. They change the plan: a consent
     button that says "Allow access", not "Approve"; a bottle that comes in two
     sizes, not three.
   - **A kit from the real thing.** For software, rebuild the components the story
     needs from their real markup and CSS into a small kit in `assets/kit/`: live
     markup with editable text, plus a 2x still that stays sharp through a
     punch-in. For a physical product, cut each photo out of its background at 2x
     and keep parts and labels on separate layers, so a scene can turn, open or
     take it apart. Scenes reuse the kit instead of redrawing the product.
   - **Assets stay local and owned.** Use images, clips and fonts that are in the
     project or that the creator supplies. Don't download stock photos or fonts a
     page merely links to; ask for the files, or redraw the idea in code (shapes,
     silhouettes, the UI itself) and note the swap. Prefer the product's own font
     files or an installed font (`@font-face { src: local(...) }`); a web font URL
     makes the renderer fetch it at build time.
2. **Plan** in `analysis/ad-plan.md` with the [story guide](references/story.md):
   study strong references first when polish matters, then write the angle, hook,
   beats, the handover between every pair of scenes, on-screen text, voiceover
   lines, the call to action and the sound events. Get the creator's OK on the plan
   when they are present.
3. **Voiceover first, when there is one.** The creator's own recording is best.
   Otherwise add one with ElevenLabs if needed, or HyperFrames' local
   text-to-speech (`hyperframes tts`; it downloads a voice model once, then runs
   offline). Get word timings from a transcription or the service's alignment,
   and take every beat's frame from them: the click lands on "send", the reveal on
   its word. Cut and place whole lines on the audio's real silences instead
   (`ffmpeg -i voice.wav -af silencedetect=n=-40dB:d=0.12 -f null -`): alignment
   timestamps drifted up to ~0.4 s from the audio, and cutting a line on them
   clipped its first word. Use word timings only for offsets inside a line.
   Without a voiceover, pace the beats by reading time and, if there is music, its
   strong hits. Music is the creator's licensed track, one they own, a bed you make
   in code or generate for this piece, or none; the SFX pack has no music.
4. **Build** a HyperFrames composition in `work/ad-vNN/` (Node 22+ and the
   workspace runtime from `edit-video`'s `init-workspace.mjs --install`). If
   HyperFrames' own skills are installed (`hyperframes-core`,
   `hyperframes-animation`, `hyperframes-keyframes`), read them for the composition
   contract and animation mechanics; they track the current renderer. Their
   `product-launch-video` workflow can build from your plan when the creator wants
   its presets and has signed in to its services; keep your plan as the brief and
   the reel at 1080×1920 (1920×1080 for a 16:9 film). Otherwise write the
   composition yourself following [motion](references/motion.md). Either way, write
   `cues.json` beside it: one sound cue per visible event (format in `edit-video`'s
   sound-sync reference).
   - **Longer pieces.** For a launch film with many scenes, put one scene per
     sub-composition file, each with a fixed duration taken from the voice. Split
     the build across parallel agents only past about six scenes; give each
     builder its scene's plan block (handovers included), the design tokens and
     the kit. Then assemble, run step 5 on the whole piece and snapshot every
     scene, not just the handovers.
5. **Check and look before rendering.** Run, from the workspace:

   ```bash
   .favstash-studio/runtime/node_modules/.bin/hyperframes check work/ad-vNN --at-transitions \
     --caption-zone "x0=0;y0=.65;x1=1;y1=1"
   ```

   - **Errors** fail the build. **Layout warnings** on visible text (overlap,
     overflow, text in the bottom app-UI band set by `--caption-zone`) are defects
     unless the layering is deliberate and marked on that element. Lint notes about
     file size can stay for one continuous composition.
   - If the contrast pass reports **0 text checks**, it didn't measure anything:
     judge contrast on the snapshots.
   - Snapshot frame 0 and every handover at its start, middle and end with
     `hyperframes snapshot work/ad-vNN --describe false --at …` (times in seconds:
     frame ÷ 30, rounded down to 4 decimals). `--describe false` keeps frames off
     outside vision services. Look at every PNG, fix and repeat. Keep critical text
     inside `edit-video`'s safe area (x 72–900, y 269–1248 at 1080×1920) and measure
     the widest line, not just its anchor. The caption zone and safe area are the
     vertical reel's; for a 16:9 film, set them from where it will play.
6. **Render** with `hyperframes render work/ad-vNN --fps 30 --quality high --output
   previews/ad-vNN.mp4`, then scan it for black frames and dead holds:

   ```bash
   ffmpeg -i previews/ad-vNN.mp4 -vf "blackdetect=d=0.03,freezedetect=n=0.003:d=1.5" -an -f null - 2>&1 | grep -E "black_|freeze_"
   ```

   A hold longer than ~1.5 s with nothing moving reads as a stall; give it motion
   or cut it.
7. **Sound.** Pick each cue's sound from the sound map below. Mix the voice and
   `cues.json` onto the render with `edit-video`'s
   `scripts/sfx-sync.mjs mix work/ad-vNN/cues.json --out work/mix-vNN.wav
   [--voice …] --video previews/ad-vNN.mp4 --mux exports/ad-vNN.mp4`, then
   `sfx-sync.mjs check exports/ad-vNN.mp4 --mix work/mix-vNN.wav --cues … --strips
   reports/sync-vNN` and look at the strips: each red frame should be the first
   that shows its event. Use `--crop x,y,w,h` to zoom on small events.
   - **Faster overall without re-authoring.** Render again at a whole frame rate
     near 30 ÷ k, play it back at 30 fps and tempo-shift the finished mix by k with
     pitch preserved. Every frame is still a real frame and every cue stays in
     sync. k ≈ 1.1 reads as "a bit faster": render with `--fps 27` (k = 30/27) to
     `previews/ad-vNN-27fps.mp4`, check sync on the normal-speed export above, then:

     ```bash
     ffmpeg -i previews/ad-vNN-27fps.mp4 -i work/mix-vNN.wav -filter_complex \
       "[0:v]setpts=PTS*27/30[v];[1:a]atempo=1.111111,loudnorm=I=-14:TP=-2.5,aresample=48000[a]" \
       -map "[v]" -map "[a]" -r 30 -c:v libx264 -crf 16 -c:a aac -b:a 192k \
       exports/ad-vNN-fast.mp4
     ```

     The stretch shifts loudness, so re-normalize after it (−14 LUFS matches the
     mix; −16 also suits social).
8. **Review and deliver** with `edit-video`: the encoded export, frame 0 and the
   first 3 seconds, every handover at phone size, safe areas, a full decode, and the
   claims against the source. Say what you measured and what you could not judge
   (a listening pass). Keep numbered versions; never publish without the creator's
   approval of the exact post, and confirm the call to action really delivers.
   - **YouTube.** Render the 16:9 film natively at 4K (`hyperframes render
     --resolution landscape-4k`, same frames at twice the pixel density) and upload
     that: YouTube's re-encode keeps small text far sharper from a 4K upload, even
     for viewers watching in 1080p. Keep the file under the upload tool's size limit
     by capping the bitrate (about 25 Mbps fits a one-minute film in 200 MB).
   - **Thumbnail or cover.** A frame from the film rarely reads at feed size. Build
     one from the kit: a short two-line headline and one big piece of the product,
     then check it at about 250 px wide.

## Sound map

Start from these, all in `edit-video`'s SFX pack. Keep every sound short, dry and
under the voice; ordinary text changes stay silent and cues closer than about 6
frames merge.

| Visible event | Sound | Note |
|---|---|---|
| Frame 1 of the hook | `curated/hook-impact.wav` | On the opening frame |
| Product, card or panel arrives | `curated/ui-pop.wav` | Quieter for small chips |
| Product or block settles into place | `thock.wav` | On the frame it lands |
| Step, row or spec callout appears | `tick.wav` | One per step |
| Dial, mechanism or progress moves | `ratchet.wav` | Trim it with `dur` for a short move |
| Lid closes, clasp locks, account connects | `latch.wav` | Its main click lands on the event |
| Highlight or sheen passes over the product | `shimmer.wav` | Peaks on the brightest frame |
| Visible click or button press | `curated/ui-click.wav` | On the click |
| Camera move, push-in or handover | `curated/zoom-swish.wav` | Peaks on the move's fastest moment |
| Build into the reveal | `curated/metallic-riser.wav` | Resolve it on the reveal |
| Earned completion | `clean-ding.wav` | Once |

A creator's own library comes first when they have one; trim each file to just
before its hit (`edit-video`'s sound-sync reference).

## Pitfalls already paid for

- A later element that isn't hidden at frame 0 shows before its cue. Set the
  starting state of everything explicitly.
- Frame times rounded up (29.0667 s for frame 872) fire a hard switch one frame
  late and put its sound a frame early. Compute times from frame numbers and round
  down.
- A fade-in's first visible frame is the one after it starts; a hard switch shows
  on its own frame. Cue each accordingly.
- Font stacks with quotes break an inline `style` attribute and silently fall back
  to Times. Put design tokens in a stylesheet.
- Symbols such as ✻ ⏺ ⎿ ✓ › were missing from the shipped font files and rendered
  as boxes or in a fallback face. Draw such symbols as inline SVG, or confirm the
  font file covers them.
- A big move into a new world (rising into space, diving into a screen) goes black
  for a frame if the old layer leaves before the new one arrives. Bring the new
  layer in first.
- Tilted or layered text trips the layout checker. Mark only the specific
  deliberate blocks with `data-layout-allow-overlap`; anything else is a real
  collision.
- Text over a busy crossfade turns to mud. Stagger it: old out, new in, or carry
  one object across instead.

The inspect → plan → build method and the grounding and reading-time rules are
informed by [brag](https://github.com/latent-spaces/brag) (MIT); no third-party text
or code is included.
