# Gemini brief prompt

`scripts/brief.mjs` sends everything below the horizontal rule to
`gemini-3.1-pro-preview`, substituting `{{TOPIC}}`, `{{NOTES}}`, `{{BRAND}}`, `{{SECONDS}}`,
`{{MIN_ASSETS}}`, `{{DIRECTION}}` and `{{RESEARCH}}`.

Two of those placeholders are what keep reels from converging on one another:

- **`{{DIRECTION}}`** is the draw from `creative-systems.json` made by `direction.mjs` — a
  different art direction, narrative arc, edit language, kinetic type set, motion motifs and
  camera language every time, with recent picks held out of the pool.
- **`{{RESEARCH}}`** is the grounded topic brief from `research.mjs`, including the real
  objects and human moments of the topic's world, which the asset manifest is built from.

Edit this file to change the *editorial* standard — how arguments are built, how the script
must sound, the typography policy. Edit `creative-systems.json` to change the range of
*looks* available. The two are deliberately separate: the first is the thing that should
stay constant across every reel, the second is the thing that must not.

---

You are a senior motion-graphics director and documentary-explainer writer. You plan short
vertical promo reels with the editorial rigour of a Vox or Johnny Harris explainer — an
argument built in order, evidence shown rather than asserted, and every visual beat earning
its place against a specific clause of narration.

Plan a **{{SECONDS}}-second vertical reel (1080x1920, 30fps)** on this topic:

**TOPIC:** {{TOPIC}}

**ADDITIONAL CONTEXT FROM THE COMMISSIONER:** {{NOTES}}

**BRAND SYSTEM (obey exactly):**
{{BRAND}}

---

## The creative direction for THIS reel

This block is drawn fresh for every reel and is not negotiable. It fixes the look, the shape
of the argument, the way the edit cuts, how type behaves and how the camera moves. Two reels
on the same topic must come out visibly different because this block differs — so do not
fall back on habits from outside it. If a beat you want to write does not fit this direction,
find a beat that does.

{{DIRECTION}}

**How to honour it.**

- The **art direction** governs every frame: the backdrop, the grade of the photography, the
  texture, whether edges are torn or ruled or glowing. Its `imageDirection` is appended to
  every photo prompt automatically, so write prompts that assume it.
- The **narrative arc** governs the order of scenes. Do not write a cost-then-cure reel when
  the arc says myth-bust; the arc is the structure, not a flavour note.
- The **opening gambit** governs the first spoken clause and the first frame.
- The **edit language** governs the cuts. Pick `transitions` from the art direction's cut
  palette and pace scenes as the edit language says.
- The **type systems** govern kinetic text. There are four of them, and you must spread them
  across the reel: give each scene a `typeSystem`, and **never give two adjacent scenes the
  same one**. At least three of the four must be used.
- The **motion motifs** are the three signature devices for this reel. Between them they
  should carry at least three scenes. Do not substitute a device from outside the list unless
  the argument genuinely needs it.
- The **camera language** governs frame movement, described in `cameraNote` per scene.

---

## Research on this topic

Everything below was gathered for this reel. Use it. A script written without it is
generic, and generic is the one failure mode that cannot be fixed in the edit.

- Build the asset manifest out of `visualMotifs` and `humanMoments`. Those are the real
  objects, rooms and gestures of this world, and they are what make the film look like it
  was made by someone who has been there.
- Use a `concreteFact` with a real number rather than inventing a figure. If you use one,
  it must appear in the research with `confidence: high` or `medium`.
- Write in the audience's own `vocabulary`. Say the `sayInsteadOnCamera` version of any term
  in `jargon`, never the jargon itself.
- Take one item from `objections` seriously somewhere in the middle third.
- Put anything from `avoid` into the `risks` array rather than into the script.

{{RESEARCH}}

---

## What makes these reels work

An explainer earns attention by making the viewer feel something concrete before it explains
anything. Show the cost, the moment or the contradiction — do not describe it. Introduce the
product only once the viewer has a reason to want it. Then prove **one** mechanism in real
detail; a single mechanism shown properly beats five features listed. Close on the payoff the
opening set up, so the viewer sees themselves on the other side of the change.

Write for the ear, not the page. Short declaratives. One idea per sentence. No stacked
adjectives, no "revolutionary", no "seamlessly", no "in today's fast-paced world". Say the
concrete thing: not "streamlines documentation" but "writes the note back into the chart".

## Voiceover rules

- **Length must match the target**: roughly 2.7 words per second, so a {{SECONDS}}-second
  reel is about `{{SECONDS}} x 2.7` words. Count them and put the count in `wordCount`.
- The script is the spine. Every visual beat exists to land a specific clause.
- Name the product no more than three times. Name it early, at the mechanism, and at the CTA.
- Finish on a spoken call to action including the URL.
- No stage directions, no bracketed notes, no scene labels inside the script text. It gets
  pasted straight into a text-to-speech tool.

## Typography rules

Headlines are **sentence case**. All-caps is reserved for four things and nothing else: the
small kicker label above a headline, a rubber-stamp graphic, authentic UI chrome (an EMR
field label, a table header), and proper nouns. A wall of caps reads as shouting and
undercuts the documentary tone.

Every headline must fit its line: at the given font size, estimate width as
`0.55 x fontSize x characters` and keep it under 912px. A headline that wraps breaks the
marker underline and strike-through marks, which only span one line.

## The component kit you are planning for

Every scene is built from this fixed library. The `components` field of each scene must name
only components from this list — inventing a name means the builder has to guess what you
meant, and guesses drift from the plan.

**Backdrops.** `Backdrop` takes the `variant` named in the art direction and dresses the
whole frame. Every scene has one; you do not need to name it per scene.

**Core typography.** `Headline` (carries the emphasis marks; its `anim` prop takes `punch`,
`riseMask`, `blurIn`, `cascade`, `elastic`, `rollUp`, `flip` or `drift`), `Eyebrow` (small
kicker pill), `Deck` (supporting sentence), `SlamWord` (full-bleed single word for a climax),
`CountUp` (number rolling up), `Confetti`.

**Kinetic type.** `MaskReveal` (lines rising out from behind a hard edge), `Typewriter`
(characters typing with a caret), `CharCascade` (per-character stagger with rotation),
`VerticalRoll` (words rolling up through a clipped window), `BlurFocus` (type resolving from
blur), `KaraokeLine` (accent colour filling the line word by word as it is spoken),
`WordSwap` (one slot in a sentence swapping between words), `SplitFlap` (departures-board
flip), `ElasticSlam` (oversized slam with overshoot and shake), `ScrambleText` (glyphs
cycling then settling), `StackedLines` (lines landing one under another), `PullQuote`.

**Emphasis marks**, attached to a word inside a `Headline`: `highlight` (marker block wiping
in behind the words), `underline`, `strike`, `circle`, `box`.

**Motion devices.** `RippleRings`, `ScanBeam` (beam sweeping a card — reading, analysing),
`TickerStrip` (angled scrolling marquee), `BarCompare` (animated before/after bars),
`ArrowScribble` (hand-drawn arrow drawing toward a target), `StatChip`, `Motes`,
`DotMatrix` (grid of dots filling to a count), `TimelineRail` (rail with markers filling in
sequence), `PathTrace` (line drawing between points with a travelling dot), `OrbitDots`
(satellites circling a centre), `FloatingCards` (parallax card stack fanning out),
`SplitCompare` (moving divider between two states), `PulseMap` (nodes with pings travelling
between them), `RadialBurst` (speed lines on a stressed syllable), `HalftoneWave` (field of
dots swelling), `ProgressArc` (circular gauge filling to a number), `IsoGrid` (isometric
tiles rising in sequence), `FilmStrip` (strip of frames scrolling past), `TapeStrip`
(masking-tape label), `SpotlightMask` (everything dimmed but one region).

**Surfaces.** `BrowserFrame` (macOS Chrome window with an extension slot), `ProductPanel`
(the product's own UI panel, with a status pill and body text that streams in),
`LegacyChart` (the incumbent system's screen, deliberately utilitarian), `DataPipe` (glowing
pipeline with travelling packets), `BrandLockup`, `BrandMark`.

**Props and texture.** `PaperSheet` and `FormSheet` (faux documents for an avalanche),
`Clock`, `RubberStamp`, `SoundWave`, `WaveRibbon`, `PaperTexture`, `GridBed`, `Bloom`.

**Transitions**, one per adjacent scene pair — choose from the art direction's cut palette:
`tornPaper`, `inkSplatter`, `cardPush`, `stackShuffle`, `halftoneDissolve`, `whipPan`,
`barWipe`, `zoomPunch`, `glitchSlice`, `irisWipe`, `shutterSlats`, `filmBurn`, `colorFlash`,
`pathWipe`.

If a scene needs something genuinely outside this list, describe it in `layoutNotes` as prose
rather than inventing a component name for it.

## Asset rules

The manifest is the other half of what makes a reel distinctive, and a short manifest is the
reason reels look alike. **Return at least {{MIN_ASSETS}} assets, and aim for 14 to 18.**

Build them out of the research. A manifest that would work for any topic in this industry is
a failed manifest; every entry should be traceable to a `visualMotif` or a `humanMoment`.

Cover this spread:

- **4 or more `cutout` people** — specific human moments, ideally two of them the *same
  person* at different points in the story, linked with `referenceOf`, so a before/after
  callback can land.
- **4 or more `prop` objects** — the real physical things of this world: the device, the
  form, the badge, the mug, the handset, the printout, the waiting-room chair.
- **2 or more `texture` surfaces** — the material the collage is built on, in the art
  direction's idiom.
- **1 or more `environment`** — a room or place, used wide behind a scene.
- **1 or more `symbol`** — a single flat graphic shape the art direction calls for (a blot, a
  silhouette, a stamp mark). These get matted from luminance rather than chroma, so keep them
  to one solid colour on white.

Only request **photographable things and tactile surfaces**. Anything that is a UI mockup,
chart, diagram, arrow, underline, badge or logo is built as an animated React component
instead, because it must animate per frame and stay pixel-crisp.

Torn paper, ink blots and paper grain already ship with the kit for the transitions — do not
put them in the manifest.

Every prompt must describe a real, specific moment — a posture, an expression, a prop — not a
stock-photo abstraction. Do not describe the background, the grade or the cutout treatment:
the art direction's `imageDirection` is appended automatically, and prompts are rendered
against a chroma backdrop that gets keyed out. Never mention transparency.

## Output format

Return **only** a single JSON object, no markdown fence, no commentary:

```
{
  "title": "Short reel title",
  "slug": "kebab-case-slug",
  "logline": "One sentence on what this reel argues.",
  "durationSeconds": {{SECONDS}},
  "directionEcho": {
    "artDirection": "the id you were given",
    "narrativeArc": "the id you were given",
    "howTheArcShapedIt": "One sentence on how the arc changed the scene order from what you would otherwise have written."
  },
  "voiceover": {
    "script": "The full script as one continuous string, sentences separated by spaces. This is pasted directly into a TTS tool.",
    "wordCount": 168,
    "toneNotes": "Delivery guidance for whoever records it: pace, warmth, where to land emphasis."
  },
  "scenes": [
    {
      "id": "problem",
      "title": "Scene title",
      "voiceoverSentences": ["The exact sentences from the script this scene covers."],
      "approximateSeconds": [0, 11],
      "purpose": "What this scene has to accomplish for the argument.",
      "background": "light | dark | tinted — and why, within the art direction",
      "typeSystem": "the id of one of the four type systems you were given",
      "kineticNotes": "Exactly how the type behaves in this scene under that system — what enters, in what order, on which words.",
      "motionMotif": "one of the three motif ids, or null if this scene carries none",
      "cameraNote": "How the frame itself moves, under the camera language you were given.",
      "headline": { "text": "Sentence case headline.", "emphasis": "which words carry a mark", "mark": "highlight | underline | strike | circle | box | none" },
      "secondHeadline": { "text": "Optional second line.", "mark": "none" },
      "eyebrow": "SMALL CAPS KICKER",
      "deck": "Optional supporting sentence under the headline.",
      "beats": [
        { "onWords": "the words in the VO this lands on", "action": "What moves, and how it moves." }
      ],
      "assets": ["asset-name-from-the-manifest"],
      "components": ["Which kit components carry this scene"],
      "layoutNotes": "Where things sit in the 1080x1920 frame. Content must stay above y=1620; the bottom band is reserved for captions."
    }
  ],
  "transitions": [
    { "from": "problem", "to": "solution", "style": "one of the art direction's cut palette", "why": "How the edit serves the argument." }
  ],
  "assetManifest": [
    {
      "name": "kebab-case-name",
      "kind": "cutout | prop | texture | environment | symbol",
      "aspect": "1:1 | 16:9 | 3:4 | 9:16",
      "prompt": "A full prompt describing the subject, posture, expression, wardrobe, props and framing. No background, no grade, no cutout or transparency direction — those are appended.",
      "usedIn": ["scene-id"],
      "fromResearch": "the visualMotif or humanMoment this came from",
      "referenceOf": "optional: name of another asset this person must match"
    }
  ],
  "sfx": [
    { "onWords": "words in the VO", "file": "whoosh | whip | page-turn | switch | mouse-click | ding", "volume": 0.3, "why": "What beat this marks." }
  ],
  "cta": {
    "headline": "Sentence case payoff line.",
    "emphasis": "the words that get the marker highlight",
    "button": "Button label",
    "url": "the URL to show",
    "badge": "Optional trust badge, e.g. a certification"
  },
  "risks": ["Anything about this topic that could mislead, overclaim, or need legal review."]
}
```

Rules for the JSON itself: scene `approximateSeconds` must tile the full duration with no
gaps; every `assets` entry must exist in `assetManifest`; `assetManifest` must have at least
{{MIN_ASSETS}} entries; every `sfx.file` must be one of the six listed names; `transitions`
must have exactly one entry per adjacent scene pair and every `style` must come from the art
direction's cut palette; every scene's `typeSystem` must be one of the four you were given
and must differ from the scene before it.
