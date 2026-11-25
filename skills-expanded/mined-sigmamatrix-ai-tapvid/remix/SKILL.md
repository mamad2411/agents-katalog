---
name: remix
description: Clone a reference video into a reusable template (React boards, transition table, narrative structure, reference clips per media slot, sound effects) and replicate it on the user's own topic — rewrite the copy, generate or find new footage that follows the original shots with the user's people and products swapped in, voice it at the original's pace, score it and render tapvid.mp4, all locally, at a 1:1 `high` tier (default) or a fast `low` tier. Use when the user asks (in any language) to clone, replicate or remake a reference video (a local file, a link, or keywords to search for one), or to reuse a template made earlier on a new topic.
allowed-tools: Read, Write, Edit, Bash, Agent, Task, WebSearch, WebFetch
metadata:
  version: "1.0.1"
---

# Remix a video

Invocation: `remix <video path | url | keywords | clone dir> [topic] [low | high] [auto]`.

Arguments: `$ARGUMENTS` — the reference (a video file, a link, search keywords, or an existing `clone-<id>`
directory or its `template/`), optionally the new topic, optionally the tier `low` or `high`, and optionally
`auto`. Resolve `~` and relative
paths. Where the client does not fill `$ARGUMENTS` in, take them from the user's request.

`SKILL_ROOT` is the absolute path to the directory containing this SKILL.md. Resolve it from the installed skill location, never from the working directory. Run every script as
`node "$SKILL_ROOT/scripts/<name>.mjs" …`. `PROJECT` is the clone directory (default `./clone-<id>/`, `<id>` =
`<topic>-<kind>` such as `saas-launch-explainer`); `REPLICA` is `$PROJECT/replicas/<slug>` (slug = short
English name of the new topic). References live in `$SKILL_ROOT/references/`; read each one at the step that
names it, not up front.

## Two tiers

The tier decides how faithfully step 3 rebuilds the original.

| Tier | When | What changes |
|---|---|---|
| **low** | `low` in the arguments, or the user wants it quick or rough (in any language) | step 3 is the quick template (one generated board per scene: the original's layout as avatar / pixel / screen / code layers plus its on-screen texts); talking-to-camera regions become digital humans, filmed regions AI video that follows the original region, code regions elements written per replica; no stop 1, so plan mode has one stop; about 25 minutes |
| **high** (default) | no tier in the arguments, `high`, or the user asks for an exact, faithful, 1:1 copy | the full 1:1 clone below: hand-built boards, measured elements, fonts and sound effects, two stops; about 80 minutes |

A reused clone directory keeps its template's tier (`tier` in `analysis/brief.json`); `high` on a `low`
template rebuilds step 3 at `high`. Record the tier in `brief.json` in step 2. Tell the user the tier in
the first progress line, and at `high` that `low` exists for a quicker, rougher copy.

## Sub-agents

You do the work yourself by default. A sub-agent starts with its own system prompt, tools and skill list
(50–150k tokens before its first step) and has to rebuild what you already know, so it pays only where
several of them run at once on work that needs no judgment from the whole film. Use one, when the harness
has a sub-agent tool, exactly where a step says so:

- step 3 (high), boards: a template with **4 or more layouts** — one sub-agent per layout, all in one message;
- step 5, sketches; step 7, checking each generated clip as it lands; step 9, checking final frames per
  scene group.

The split, the decomposition, element measurement, fonts, transitions, the structure and acceptance stay
with you: they need the whole film, and handing them over returns work you then redo.

| Tier | Tasks | Claude Code | Codex |
|---|---|---|---|
| **strong** | a board the fast tier failed | `model: "opus"` | spawn with the strongest model, `reasoning_effort: "high"` |
| **fast** | writing and fixing a layout's boards; sketches; checking generated clips and final frames | `model: "sonnet"` | spawn with a smaller model or `reasoning_effort: "low"` |

- Split by unit of work, never by board when boards repeat: one sub-agent per **layout** (it writes every board
  of that layout), per generated clip, per scene group. Launch independent ones in the same message so they
  run at once; at most 8.
- Every brief names: the files to read (only the sections the task needs, not whole references), the files
  it may write, the command that accepts the result, the round limit, and what to return — a short text
  result, never images or file dumps.
- A fast-tier task that fails its acceptance command twice goes to the strong tier with the files as they
  are; the acceptance bar never changes.
- Codex: spawn with `fork_turns: "none"` (a full-history fork rejects model overrides); where the session
  does not expose `model` / `reasoning_effort`, the sub-agent inherits yours.

## Two modes

The goal is one pass to a finished film. In both modes the work is the same and every check below runs; the
modes differ only in where the user is asked.

| Mode | When | The user |
|---|---|---|
| **plan** (default) | always, unless the user asks for auto | confirms the 1:1 clone (stop 1, after step 3; `high` only), then the replica with its cost (stop 2, step 6). Then production runs to delivery |
| **auto** | `auto` in the arguments, or the user says "just make it", "fully automatic", "don't ask me" (in any language) | is asked nothing after the topic; you make every content and production choice and deliver the film |

**A stop is a confirmation, not a review session.** Before each stop, every self-check of that stage has
passed and its fixes are done — the user should only need to say yes. What a check cannot reach (a font with
no open look-alike, a moving original shot the replica must regenerate) is stated as a known limit with its
reason, never handed to the user as a question. If the user still asks for a change, make it, rerun the checks
of that stage, and stop again.

**auto mode.** Needs the topic; ask for it if it is missing — the only question. Research the topic on the
web (step 4) and use the user's materials if they gave any. Choose like a careful producer: replacements AI-generated from the brief (people as plausible
new people, never a real person's likeness), copy written by you within the copy budget, the first recommended
voice, the template's audio mode, free music, Giphy for reaction GIFs when its key is set, the economy tier
for small pop-ups. A budget the user named ("under 200 credits", "under $5") is a hard cap: downgrade models, then
move slots to code until the estimate fits; if it cannot fit, stop and say so. Without a budget, spend what the
plan needs at economy-first defaults. Paid work runs without a stop, so state the estimate in one line when
generation starts. Deliver with the same report, and say which choices you made.

## How to talk to the user

- **Speak the user's language for the whole run** (the docs and files stay English). A film in another
  language does not change the language you talk in: show its copy with the meaning in the user's language.
  Plain words, one short progress line per step while scripts and generations run.
- **Every example message, table and phrase in this skill and its references is a pattern, not text to
  paste.** Write it in the user's language — an English-speaking user never sees Chinese, a Chinese-speaking
  user never sees English labels. Quoted trigger phrases (e.g. "just make it", "you pick") are things a user
  may say, in any language.
- Never show file names, field names, model codes, JSON or script output. Picture sources are AI video, AI
  image, GIF, animation, your material, digital human — in the user's language. Name providers by vendor: "MiniMax", "fal", "TapVid", "ElevenLabs", "GIPHY";
  models by their product names ("Nano Banana", "Seedance 2.0 Fast").
- **Show, don't open.** Everything the user looks at lives in the review page: the original beside the
  template, the replica preview, the cost, the finished film beside the original, every version and every
  generated clip. After a change, rebuild it (`review.mjs`) and name the tab; never open loose video, audio or
  image files in an external player. The page opens in English with a Chinese switch in its header. Its tabs:
  Clone comparison, Replica preview, Storyboard & cost, Final cut, Assets. Name a tab in the user's language
  (as the page's Chinese view labels it for a Chinese-speaking user, and tell them the switch is top right).
- **The user decides the content** (plan mode). The new topic, which people / products / logos get replaced
  and with what, and the user's own materials come from the user. Never invent defaults. Only when the user
  hands the choice over ("you pick", "choose for me") offer 2–3 options, or pick one and say why. Production
  choices — language, audio mode, voice, music, GIFs vs AI pictures — you recommend and the user confirms.
- **Look it up before asking.** When the user's materials leave gaps — what the product does, its features,
  pricing, audience, real names, its logo, how its screens look, facts the copy needs — research it yourself
  with the client's web tools (web search, page fetch, the browser tool): the official site, docs, changelog,
  press kit, app-store page. Searching is a first try, not a replacement for asking: what you cannot find,
  or find only unreliably (a product with no web presence, an unreleased feature, the user's own photos),
  you ask the user for, together with what the user alone decides. Say in one line what you found and where;
  never present a guess as a fact.
- **Infrastructure is not a question.** Local, free tools (ffmpeg, the runtime, Whisper, yt-dlp) are installed
  without asking — say so in one line. Ask only what the user alone can decide, or what costs money.
- **Clone first, then ask.** Steps 1–3 rebuild the original and need none of the user's content decisions:
  do not ask about the replica before the template exists (stop 1 at `high`). Step 4 opens with all the questions in one message,
  when you can show what the original actually contains.
- **Nothing is spent before stop 2** (plan mode). Steps 0–5 cost only time and tokens. Commands that call a
  paid API for a test (`media.mjs check --live`) need `--spend` and the user's yes; prices come from
  `media.mjs prices <provider>`, which spends nothing.
- **Keys never enter the chat.** If the user pastes one, tell them it is now exposed, ask them to revoke it,
  and use the password box (`set-key.mjs`) for the new one.

## Step 0 — environment (every run)

1. `node "$SKILL_ROOT/scripts/ensure-runtime.mjs"` installs whatever is missing (Homebrew on macOS, winget on
   Windows) and the runtime; the first run downloads Chromium and can take minutes — say so. Only a
   `missing: …` last line (no package manager, or a manual step) needs the user: show what it printed.
2. `node "$SKILL_ROOT/scripts/media.mjs" providers --json` — read it with `references/providers.md`, quietly. `whisper-local`
   not ready → `node "$SKILL_ROOT/scripts/ensure-runtime.mjs" --tool whisper-cli` (local, free, first in the
   transcription order even when another vendor has a key; the model download falls back to a mirror on a slow
   network by itself).
   Keys and generation providers are not raised now; they come up in step 4, where they matter.

## Step 1 — inputs

**Reference video.**

| The user gives | Do |
|---|---|
| A local video | Step 2 |
| A link | `node "$SKILL_ROOT/scripts/ensure-runtime.mjs" --tool yt-dlp`, then write `$PROJECT/requests/download.json` = `{"id":"download-1","capability":"video.download","params":{"url":"<link>"},"out":"../source/download"}`, run `node "$SKILL_ROOT/scripts/media.mjs" run "$PROJECT/requests/download.json"`, use the file it reports |
| Keywords ("find a trending SaaS launch video") | Write `$PROJECT/requests/search.json` = `{"id":"search-1","capability":"video.search","params":{"query":"<English or platform-language query>","sort":"views","limit":10}}` (add `duration`, `orientation`, `published_after` from the request), run it, read the items from `$PROJECT/requests/tasks.json` (`tasks["search-1"].result.items`). Show a table: title, length, views, date, link. Download the one the user picks (auto: the most viewed that fits) |
| An existing clone directory or its `template/` | Reuse the template: skip to step 4 |

Search or download failed (no provider for that platform, login wall, refused): follow the fallback in
`references/providers.md` — first, with the user's consent, browser automation in the user's own browser
(they log in themselves; no paywall, DRM or captcha bypass; only the video they picked); else ask them to
download it and give you the file. A Douyin / TikTok search the user wants regularly is a reason to offer a
written provider (`references/provider-authoring.md`).

Keep the topic if the user gave one; ask nothing else yet (the search pick above is the exception — only the
user can choose the video).

## Step 2 — read the original, frame by frame

`node "$SKILL_ROOT/scripts/intake.mjs" "$PROJECT" <video>` — add `--understand` when a video-understanding
provider is ready. Transcription runs through a ready provider or local Whisper (step 0). Besides the shots,
strips and words, intake lists the original's sound effects (`source/sfx.json`, a clip per event).

Then read `references/analysis.md` and write `$PROJECT/analysis/brief.json` from the shot strips, overview,
transcript and (when present) the understanding file. Times always come from `source/timeline.json`.

## Step 3 (low) — the quick template

1. Write `$PROJECT/analysis/shots.json` following `assets/schemas/shots.json`, from the shot strips,
   the overview and the transcript: consecutive shots grouped into scenes that tile the film (a scene with a
   pixel or screen layer at most 15 s — split a longer shot with `start` / `end`), each with a one-line
   English `role`.
   The heart of the step is each scene's `layers`: look at the frame and decide which source builds each
   region — `avatar` (someone talking to camera), `pixel` (filmed picture), `screen` (a phone or desktop
   screen) or `code` (graphics the board draws: panels, charts, lists, cards) — with its box (read off
   `measure.mjs grid`; a split screen is two layers, a picture-in-picture a full-frame layer then a small
   `circle` / `round` one, a keyed presenter a backdrop then an avatar with `cutout`), a `describe`, and the
   people, products and screens the replica may replace (`subjects`, boxes in the layer). A new layout
   inside a scene starts a new scene. Order layers back to front; boxes are `[x, y, width, height]` in
   0–1 of the frame (subjects use the layer's coordinates). Give layers unique keys: `presenter` for
   the single avatar layer, other names excluding `texts` and `say` for the rest.
   Then every designed on-screen text with its box (read off `measure.mjs grid`), in / out in source seconds, entrance, colour and plate.
   Burned-in captions of the narration are not texts: their look goes into `captions` (`references/captions.md`
   tokens). One open `font` that looks like the original's text, picked by eye; a palette from the frames.
2. `node "$SKILL_ROOT/scripts/quick.mjs" "$PROJECT"` writes the template (boards, transitions, design, narrative
   structure, element inventory), installs the font, extracts the reference clips and builds the previews.
3. `node "$SKILL_ROOT/scripts/validate.mjs" template "$PROJECT/template"` — fix `shots.json` and rerun
   `quick.mjs --force` until clean. Look at each board's preview frame against the original at a moment its
   texts show — `template/boards/<Name>.png` is taken there — beside the same moment of the original:
   every region in its place (code regions stay empty until the replica), text in its place, no overflow.
4. Write `$PROJECT/report.md` in a few lines: scenes and their layouts, what the quick template does not
   rebuild (measured element motion, sound effects, designed transitions), and that `high` rebuilds them.

No stop: go on to step 4.

## Step 3 (high) — build the template (1:1)

Follow `references/analysis.md` → `boards.md` → `transitions.md` → `structure.md` → `acceptance.md`, each
artifact on disk before the next. Read each reference once, when its step starts; the scripts' usage lines
and these references cover what you need, so do not read plugin sources.

1. Split into boards (one per layout system, not per shot) and write the reasons into `$PROJECT/report.md`.
2. Decompose: structure vs topic, region roles, lists, layering; write `analysis/boards.json` with windows
   from `timeline.json` and per-slot `crop` / `subjects`.
3. **Inventory every element** (`references/analysis.md` §9) into `analysis/elements.json`: each instance's
   measured box (`measure.mjs grid`), in / out, entrance, idle motion, content motion, font role, sound
   effect, and `behind` for an element the person in a footage slot covers (`references/boards.md` §8). Then `node "$SKILL_ROOT/scripts/measure.mjs" motion "$PROJECT"` — it tells stills from GIF-like loops,
   screen recordings and stop-motion "boil", which decide the field types (a moving original picture is a
   video slot) and the boards' idle motion.
4. Transition table into `template/template.json`, measured from the soft windows.
5. `template/design.js` with the measured captions style (`Design.captions`, `references/captions.md`), then
   fonts: for every text role, `measure.mjs fonts` against a crop of the original with 6–12 open candidates,
   pick by eye, then `node "$SKILL_ROOT/scripts/fonts.mjs" "$PROJECT" --family "<Family>" --weights 400,700`
   (`--substitute` for a non-open font; record the swap).
6. **Boards**, layout by layout. Write `template/boards/<Name>.jsx` / `.json` from its elements (measured
   boxes replayed per instance, idle motion, `data-sfx` on the elements that sound, whether and where
   captions show on this layout in `meta.captions`, the cutout layer for elements behind the person), run
   `refs.mjs "$PROJECT" --only <Name>`, `build-boards.mjs "$PROJECT" --only <Name>`,
   `compare.mjs "$PROJECT" --only <Name>`, read the rows and fix by element until the board passes, at most
   5 rounds; open a compare image only for a row under 0.95. With 4 or more layouts and a sub-agent tool,
   give each layout to a fast sub-agent instead (brief in `references/boards.md` §7), all in one message: 2
   rounds, then the strong tier takes over for up to 3 more.
7. `node "$SKILL_ROOT/scripts/refs.mjs" "$PROJECT"` for all slots; write one English `describe` per slot in
   `template/refs/refs.json`.
8. Narrative structure `template/skill/SKILL.md` and the rest of `template.json` (`references/structure.md`).
9. Swap test (second topic, min / max list counts, Chinese and 1.5× English text, every line half its length).
10. Acceptance (`references/acceptance.md`): full `build-boards.mjs`, then in one command (they are
    independent, run them in the background together) `clock.mjs "$PROJECT"`,
    `compare.mjs "$PROJECT" --fail-under 0.95 --timing` (sound effects included) and
    `validate.mjs template "$PROJECT/template"`; then the element checklist (acceptance §7). Every failure
    is fixed or proven a known limit before going on; after a fix rerun only what it touches (compare
    reuses unchanged boards).
11. Finish `$PROJECT/report.md`.

**Stop 1 — the clone** (plan mode; auto goes straight on). `node "$SKILL_ROOT/scripts/review.mjs" "$PROJECT"`
builds and opens the clone review: the template plays beside the original, in sync, with component frames
and the template's sound effects. Tell the user in a few lines: how close it is (samples ≥ 0.95, timing
within one frame), what was measured and rebuilt (fonts, element boxes, idle motion, captions, sound
effects), and the known limits with reasons. Ask for a yes; then step 4.

## Step 4 — write the replica

Read `references/replica.md`.

**Research first**. Before the questions, look up the topic and the user's product on the web (see "How to
talk": official site, docs, press kit, app-store page) and write what you learn to `$PROJECT/research.md` —
what it is, key features and numbers, audience, tone, brand colours, the official logo's URL, links to real
screenshots or demo videos, each with its source, and what you could not find. The questions propose concrete
answers where research found them and ask the user for the rest; step 4.4 writes the copy from it. An official logo or press-kit picture of the user's own
product goes to `assets/user/` as their material once the user confirms it is theirs (auto: when the topic
names the product).

**Now ask — one message, in plain words** (auto: decide each point yourself as in "Two modes"). Start from
what the original contains (from `brief.json` and the template): its structure in a line (e.g. "a presenter
talks to camera; above her a title, four numbered steps, app screenshots and reaction GIFs; word-by-word
captions"), then:

- the topic, if not given yet;
- for each person, product, logo or sticker in the original: replace with what, or drop. Ask for the user's
  own pictures (copied into `$REPLICA/assets/user/` once step 1 below creates it); without one, AI can generate
  it from a description or a slot can be drawn as animation;
- the original's product screens (screenshots, screen recordings): offer three ways and recommend the first —
  you record their product (they log in once in a window you open, you do the rest; `references/capture.md`),
  they give you recordings or screenshots they have, or the screens are drawn as animation. Their choice
  stands: a "no" to recording means their files or animation, without asking again. Open nothing before they
  agree. In auto mode record only public pages or a product with a saved session; otherwise animation;
- the original's moving pictures (reaction GIFs, loops): real GIFs from GIPHY (free; needs a free GIPHY key)
  or AI pictures brought to life (paid per clip) — recommend GIFs for meme-style originals;
- the content of repeated parts in the new topic (e.g. the four steps), or whether you should draft it;
- production choices with your recommendation: language; audio mode (`narration` when the original has a
  voice-over, `music-only` when it only has music); in narration mode the voice — write
  `$PROJECT/requests/voices.json` = `{"id":"voices-<lang>","capability":"speech.voices","params":{"language":"<lang>"}}`,
  run it, propose 2–3 recommended voices close to the original's register and energy (one voice serves the
  whole film and every digital human);
- what generation can do right now (from step 0's providers list): what is ready, what is missing and its
  effect (`references/providers.md` degradation table), and the cheapest fix — one TapVid key covers most of
  it: they create one at https://tapvid.ai/developer/apikey, then `node "$SKILL_ROOT/scripts/set-key.mjs" tapvid`
  pops up a password box for it; a key they already have for another vendor: `set-key.mjs <provider>`; a
  service that is not built in: ask for its API docs and follow `references/provider-authoring.md`.
  `set-key.mjs` prints `saved`, `cancelled` or `invalid-key` (rejected three times — ask for a new key). With
  no generation provider at all the flow still works: every slot becomes animation.

Then:

1. `node "$SKILL_ROOT/scripts/replica-init.mjs" "$PROJECT" <slug> --topic "<topic>" --language <lang>`.
2. Replacement table (`replace`): every subject the user named. Ask now about any subject in the original the
   user has not decided on — unless they handed the choice to you. A presenter portrait whose head sits higher
   or lower than the original host's (more than 5 % of the height) is reframed for free with `reframe.mjs`
   (`references/replica.md` §2) — the template's pop-ups must not cover the face.
3. Invented product (only with the user's agreement): write `$REPLICA/product.md` first.
4. Rewrite every scene's narration and data from the user's brief and `research.md` (real features and
   numbers, nothing invented about a real product) within the field limits and **within the copy budget**: the
   original's pace in syllables per second × the scene's window (`references/replica.md` §4). Copy that is too
   long makes the film slow or long; `validate.mjs replica` warns per scene. List counts follow the topic.
5. Media plan per slot: source `ai` (mode `reference` / `keyframe` / `text`), `code`, `user`; product screens
   the way the user chose: a capture of their product (`references/capture.md`: log in once, storyboard,
   `capture.mjs record`, `index`, `clip` per slot — moving slots get the recorded span, still slots the 2×
   shot), their own files (indexed and cut the same way), or code; moving original
   pictures as GIFs (`gif.mjs search` / `pick`, `references/replica.md` §5) or AI clips; elements as code in
   `$REPLICA/elements/`; presenter slots as digital human (narration mode only).
   **At `low`** each layer is one slot: `presenter` stays a digital human; a pixel layer stays `ai` /
   `reference` with `provider: "tapvid"`, `model: "minimax-h3"` when TapVid is ready (else leave both
   `null`), the replacements in `replace` and the prompt from `references/replica.md` §6 Low tier, and goes to
   keyframe when the identity gate in step 7 fails; a screen
   layer becomes `user` (their recording or screenshot) when it must be readable, otherwise it is treated
   like a pixel layer; a code layer is an element — write `$REPLICA/elements/<Board>.<key>.jsx` for the new
   topic inside the region its field's `desc` names. The `texts` items are the new copy, one per original
   text, in its place.
6. `node "$SKILL_ROOT/scripts/validate.mjs" replica "$REPLICA/replica.json"`, then
   `node "$SKILL_ROOT/scripts/media.mjs" plan "$REPLICA/replica.json"` (read its warnings: a reference falling
   back to keyframe changes what the user sees) and
   `node "$SKILL_ROOT/scripts/media.mjs" estimate "$REPLICA/plan.json" --json` (per model: unit price, count,
   subtotal). Small, short pop-up pictures take the cheapest fitting model by themselves (economy tier); a
   model the user picks pins its slots.

## Step 5 — preview material

At `low` there are no sketches or GIFs: only the code layers' elements, the music candidates and the
self-check below apply.

Slots that need a sketch (an `ai` slot without a reference clip, every `code` slot): read
`references/sketches.md`. One sub-agent per board writes all of that board's sketches
(`$REPLICA/sketches/<Board>.<path>.jsx`) and checks each with
`node "$SKILL_ROOT/scripts/frames.mjs" "$REPLICA" --sketch <file> --duration <s>` — rewrite if it fails the bar,
at most 2 rounds. Without sub-agents, write them yourself.

GIF slots: search and pick now (free) — look at each contact sheet and take the candidate that says the line
best; avoid the very GIF the original used.

Background music candidates now, free ones only (`references/audio.md`): the user's file, two composed
scores, or a royalty-free search hit. A paid AI-music candidate is a cost row, made after stop 2.

Self-check before stop 2: `validate.mjs replica` clean (copy-budget warnings fixed), every moving original
picture has a moving source, every product screen has its chosen source (a capture or the user's files,
checked frame by frame, nothing private; or code), presenter headroom checked, the plan's warnings understood.

## Step 6 — stop 2: the replica and its cost

`node "$SKILL_ROOT/scripts/review.mjs" "$PROJECT" <slug>` builds and opens the review page (auto: build it, do not
stop). Then give the table, filled from the replica and the estimate — this pattern, written in the user's
language:

> Here is the replica. Generation starts (and costs money) once you confirm:
>
> | # | Role | On screen | Narration / copy | Source | Made by | Length | Est. cost |
> |---|---|---|---|---|---|---|---|
> | 1 | Opening | The original's push-in on shot 1, with your photo as the person | How many hours does your team spend in meetings each week? | AI video (from the original) | MiniMax | 2.1s | $0.28 |
> | 2 | Pain point | Three data cards popping in one by one | — | Animation | — | 4s | 0 |
>
> Cost by model:
>
> | Use | Model | Unit price | Count | Subtotal |
> |---|---|---|---|---|
> | Pop-up pictures | Nano Banana (small pictures use the cheaper model) | 6 credits / image | 12 | 72 credits |
>
> Audio: narration (paced like the original, about 6.4 syllables a second) + music (2 options) + sound effects
> where the original has them; captions: same style as the original
> Total about **$1.52**. The review page is open; in Replica preview, tick "Compare with original" to play both

TapVid costs read as credits, every other vendor in dollars, totals per vendor. Name low-resolution and
fallback rows plainly ("not sharp enough", "made from a new first frame").

Changes to copy, counts, replacements, a slot's source or vendor, voice, music: update `replica.json` and the
sketches → plan → estimate → rebuild the review → ask again. Template faults: back to step 3 for that board,
rebuild, ask again. Wait for an explicit yes.

## Step 7 — generate the pictures

1. Narration mode, voice first so clip lengths fit:
   - a digital human that speaks the script itself (the plan then writes no separate narration take) is
     generated first: `media.mjs run "$REPLICA/plan.json" --only <avatar ids>,<image ids>` — the replacement
     images and keyframes go in the same run, since no length depends on them (one run at a time: the runner
     owns `tasks.json`). Check each clip as it
     finishes against the original's presenter footage of that slot (`inspect.mjs`, below): framing, the
     person, and nothing in the picture the original's footage does not have — text the original's footage
     shows is fine, text it lacks (garbled subtitles, a drawn caption) is not. Regenerate only the failing
     clip; when the same line fails twice, rephrase that line (words such as "subtitles", "captions" or "text"
     can make the model draw them) and keep its meaning;
   - otherwise the narration takes: `--only <speech ids>`;
   - then `node "$SKILL_ROOT/scripts/timing.mjs" "$REPLICA"`: it transcribes self-voiced avatar clips and lays the
     lines on their real words, measures the pace against the original and applies one uniform tempo for the
     whole film when the voice is slower (capped so a presenter never looks fast-forwarded), and prints both
     rates. Then `media.mjs plan` again (video lengths now follow the resolved scenes, transition overlaps
     included). Any change in total cost above 10 % is told to the user before going on (auto: noted).
2. `node "$SKILL_ROOT/scripts/media.mjs" run "$REPLICA/plan.json"`. The runner orders replacement images →
   keyframes → videos, keeps ≤ 10 in flight and resumes from `tasks.json`; rerunning never pays twice.
3. Check before anything depends on it (`references/replica.md` §Checks): generated replacement images and
   the first invented-product screen, then every keyframe (subject swapped, hands, product shape) — a bad one
   is regenerated once (`--only <id>` after fixing its prompt) before its video runs.
4. Every finished clip, as soon as it lands (do not wait for the rest): a fast sub-agent runs
   `node "$SKILL_ROOT/scripts/inspect.mjs" "$REPLICA" <request-id>` and looks at each frame it lists at full size,
   returning pass, or the problem and a clean span: extra hands, wrong fingers, a morphing product, garbled text, clipping, the subject
   drifting back to the original, a digital human's pace drifting within its clip. Trim to a clean span that
   covers the slot; otherwise state the cost and regenerate once with the prompt fixed.
   **Identity gate, on every clip that shows a person** (`references/replica.md` §9): the original's person must
   not appear in any frame. `inspect.mjs "$REPLICA" <request-id> --identity`, look at every frame, then
   `identity.mjs pass|fail "$REPLICA" <request-id> --saw "<whose face, where>"`; `render.mjs` refuses the film
   until `identity.mjs status "$REPLICA"` is clear. A clip that fails is never trimmed or kept: it goes to keyframe,
   and the other reference clips of the film lose their verdict and are read again. Do not route a generated clip
   through `source: user`: that slot leaves the gate. Contact sheets and overviews do not count as this check.

| Failure | Do |
|---|---|
| Network / 5xx | The runner already retried once; rerun `run` later |
| Moderation | Rewrite the prompt without brands, celebrities, copyrighted elements; retry once; a refused reference video switches that slot to keyframe |
| A first frame with a realistic face flagged as sensitive (Seedance) | Move that slot to another first-frame model (`veo-3.1-fast`); rewording does not help |
| The same error returns seconds after a rerun, with no new vendor job | The rerun returned the earlier result of an identical request: change the model or the prompt, then run it |
| A reference picture refused by the vendor | Retry that request without the reference (prompt only); a portrait reframe falls back to `reframe.mjs` |
| Unsupported / invalid | The runner moved to the next model or vendor; nothing to do unless all failed |
| Bad key / no balance | That vendor is off for this run; tell the user (new key via `set-key.mjs`, or top up) |
| Every vendor failed | The slot falls back to its sketch (`source: code`); list it in the delivery report |

## Step 8 — voice, music, timing

Read `references/audio.md` and, in narration mode, `references/captions.md`.

- Digital human slots were generated in step 7 with the same voice.
- Music: render or fetch the chosen candidate at the final length (`music-compose.mjs`, or a one-off
  `music.generate` request), beat grid with `beats.mjs`; music-only cuts land on the original's beats.
- `node "$SKILL_ROOT/scripts/timing.mjs" "$REPLICA"` writes `resolved` (and the tempo). A narration that pushes a
  scene past its board's `maxDuration` is shortened and re-voiced.
- Sound effects need nothing: the template's elements carry them, so they follow the new timing.

## Step 9 — render and deliver

1. `node "$SKILL_ROOT/scripts/project.mjs" "$REPLICA" --final`.
2. `node "$SKILL_ROOT/scripts/validate.mjs" project "$REPLICA/project"` — fix every error.
3. `node "$SKILL_ROOT/scripts/frames.mjs" "$REPLICA"`, then fast sub-agents (one per group of scenes) look at
   every scene midpoint, the frames around every line boundary, every transition's start / middle / end and the contact sheet — text overflow, two texts overlapping (captions included; `frames.mjs` also scans the film for this and exits 1 listing each pair), captions covered, a pop-up over a face, jumps at
   boundaries, sound vs picture. Fix and repeat, at most 3 rounds.
4. `node "$SKILL_ROOT/scripts/render.mjs" "$REPLICA"` → `$REPLICA/out/tapvid.mp4` (1080p). Check the render: its
   length against the original's, the pace line `timing.mjs` printed, and frames sampled across the film,
   including the first second of every scene that shows a person, frame by frame at full width: a midpoint never
   sees an original person who is only in a scene's opening frames. A slot that went back to generation
   counts as done only when its request completed: a failed request leaves the old clip under the same file name.
   Alternative versions the user asks for go to `out/tapvid-<what>.mp4`; `tapvid.mp4` is always the current one.
5. `node "$SKILL_ROOT/scripts/review.mjs" "$PROJECT" <slug>` again: the Final cut tab plays the film beside
   the original with a version picker, the Assets tab every generated clip with its vendor and cost.
6. Write `$REPLICA/report.md` (actual cost per vendor and model from `media.mjs spend "$REPLICA"`, slots that
   fell back to animation, each asset's vendor, licenses and credits of stock footage, GIFs and music). Tell
   the user: the film is in the review page's Final cut tab (and where the file is), its length, what it actually
   cost per vendor, what became animation and why, and that the template folder can be reused next time —
   give them the `template` path to pass in for a new topic.

Later edits stay in the same replica: copy or code changes rerun only the affected part of steps 8–9; new
paid media needs the cost stated and the user's yes first (auto: within the budget).
