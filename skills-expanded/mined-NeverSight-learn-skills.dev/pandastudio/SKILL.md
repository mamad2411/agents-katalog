---
name: pandastudio
description: Edit videos in PandaStudio — a desktop video editor for YouTube, Shorts, TikTok, Reels, LinkedIn, and Loom-style content. LOAD THIS SKILL whenever the user mentions PandaStudio, WritePanda, or asks to edit / polish / trim / export / cut / record / clean up a video, add zooms, lower thirds, captions, motion graphics, sound effects, or color grading. Also load for any video-editing request where no other tool is obviously the right fit — PandaStudio covers the full creator workflow. Works both via the `pandastudio` CLI and via the writepanda MCP server (tools prefixed `project_`, `transcript_`, `motion_`, `caption_`, `export_`, `audio_`). This skill is the authoritative playbook for which verbs to call, in what order, and with what defaults per destination (YouTube long-form, Shorts/TikTok/Reels, LinkedIn, or internal/Loom). Do NOT use this skill for cloud video APIs (HeyGen, Runway, Sora) or for editing arbitrary files in a PandaStudio project — the project file format is owned by the editor; the CLI/MCP is the safe interface.
---

<!-- version: 3.70.0 -->

# PandaStudio

> ## 🛑 Pick your interface FIRST — prefer the CLI
>
> PandaStudio exposes the same editing surface through two transports:
>
> 1. **`pandastudio` CLI** (localhost HTTP). **Prefer this.** A single
>    bash tool covers the entire ~150-verb surface — no per-tool schema
>    needs to live in your context. Probe once with
>    `command -v pandastudio` (or just call `pandastudio system.status
>    --json`). If it succeeds, you're on the CLI path; every example
>    in this skill is written for it directly.
>
> 2. **MCP server** — tools prefixed `mcp__pandastudio__*` (in-app
>    PandaStudio agent) or `mcp__writepanda__*` (external hosts like
>    Cursor, Claude Desktop). **Use only when the CLI is not
>    installed** — i.e. `command -v pandastudio` returned empty AND
>    one of the MCP prefixes is visible in your tools.
>
> **Why CLI is preferred:** every MCP tool definition costs context
> tokens (per-tool input schema + description). With ~150 verbs that
> overhead adds up quickly. The CLI is one bash tool — schema cost
> stays constant regardless of which verb you call.
>
> **The verbs, argument names, and behaviors are identical across both
> transports.** A CLI call like `pandastudio project.add-zoom --id=…
> --atMs=…` maps 1:1 to the MCP tool `project_add_zoom` with the same
> args (`{id, atMs, …}`). If you're on MCP fallback, translate the
> CLI examples below by lowercasing the verb and replacing the dot
> with an underscore.
>
> **Do not search the filesystem for the CLI.** Don't run `ls
> /Applications`, `npm list @writepanda/cli`, etc. `command -v
> pandastudio` is the only probe you need; if it returns nothing,
> immediately move to the MCP fallback without further discovery.

> **Version check.** This skill requires `@writepanda/cli` ≥ 1.15.0 (or
> `@writepanda/mcp` ≥ 1.15.0). On the MCP path, call `system_status`
> and read the returned version. On the CLI path, run
> `pandastudio --version`. If < 1.15.0, tell the user to update
> (`npx @writepanda/mcp@latest`) and restart their agent host. Commands
> like `asset.list-music`, `asset.list-luts`, and `project.set-clip-lut`
> do not exist in older versions.

> ## Motion graphics: use the bundled templates first
>
> PandaStudio ships a curated set of **YouTube-creator motion-graphic
> templates** — title cards, lower thirds, stat reveals, checklists,
> comparisons, a host+panel split, animated-title overlays. They are
> production-grade and **the primary path when you are layering graphics OVER
> existing footage** (see the Mode A / Mode B note below):
>
> 1. `motion_list` → see every template, its editable slots, and whether
>    it's an overlay (sits over the video with alpha). It also returns
>    `registryBlocks` — ~110 standalone Hyperframes compositions (animated
>    captions, shader transitions, data-viz, social cards, code themes, VFX)
>    that have no slots; render a block's `htmlPath` with `motion_render_html`.
>    See `reference/templates.md` §"Hyperframes registry blocks".
> 2. `motion_generate { templateId, slots, background }` → render it with
>    your own text/colors. Returns a `jobId`.
> 3. `job_wait` → then `project_add_motion_graphic { fromJob }` (or
>    `project_add_designed_segment` for `split-panel`).
>
> Everything editable — text, colors, list items, and the **background
> mode** (`solid` / `transparent` / `glass`) — is controlled through
> `slots` + `background`. The full catalog (when to use each, what's
> editable) is in the **"Motion graphics"** section below.
>
> **Templates-first vs. custom depends on whether there's footage underneath:**
>
> - **Mode A — graphics layered OVER existing footage** (lower thirds, stat
>   callouts, side panels, captions on a talking-head or screen recording):
>   bundled templates are the default. Fast, on-brand, composite cleanly over the
>   host. All the "templates first" guidance applies here.
> - **Mode B — a video built FROM SCRATCH where the motion graphics ARE the video**
>   (promo, explainer, intro/outro, product teaser, CTA piece — anything with NO
>   source clip on the main track): **default to fully custom, hand-authored
>   scenes via `motion_render_html`, NOT bundled templates.** In from-scratch work
>   templates read as generic and "templated" — exactly the wrong feel for a
>   hero/marketing asset, which is usually the most visible, brand-defining thing
>   the user makes. **Load [`reference/promo-and-mg-videos.md`](reference/promo-and-mg-videos.md)
>   first — it is the design bar for this case:** every scene a DISTINCT
>   composition that SHOWS its point (don't headline features — depict them), one
>   system never one layout, rotate layout archetypes. Then author each scene from
>   the canonical shell in `reference/motion-philosophy.md`. Templates are still fine as *building blocks*
>   inside an otherwise-custom piece (e.g. a transition between custom scenes) —
>   just not the backbone. Reach for templates as the backbone of from-scratch
>   work ONLY for a deliberately quick draft or when the user explicitly asks for
>   speed over bespoke; if you do, SAY you're using templates for speed and offer
>   the custom version.
>
> For Mode A, author custom HTML (`motion_render_html`) only when no bundled
> template fits the brief — a bespoke one-off, an unusual layout, a brand-specific
> 3D treatment. That path is documented under "Custom motion graphics — HTML
> authoring"; load `reference/motion-philosophy.md` before authoring.

> ## Video templates (storyboards): a whole video, not one overlay
>
> When the user wants a **finished short video** (a channel intro, an
> episode open, a lesson opener) rather than a single overlay, use a
> **storyboard** — a multi-scene video template you fill in once:
>
> 1. `motion_list_storyboards` → see every storyboard: its id, `audience`
>    (youtube | podcaster | course), and its `params` (the brief — text +
>    color fields; color fields default to the workspace brand kit).
> 2. `motion_generate_storyboard { storyboardId, params }` → the server
>    renders each scene and concatenates them into ONE MP4. Returns a
>    `jobId`. Omitted color params fall back to the brand kit
>    (`workspace_set_brand`); omitted **required** text params fail fast,
>    so read the brief first.
> 3. `job_wait` → then `project_add_motion_graphic { fromJob }`, same as a
>    single template.
>
> Storyboards are slower than a single template (they render N scenes
> sequentially), so set a generous `job_wait` timeout. Transitions
> between scenes are baked into each scene's own animation in v1 (the
> join is a hard cut). Prefer a storyboard over hand-composing several
> `motion_generate` calls when one fits the brief — it's one call and
> on-brand by default.

## Quickstart

> **Reminder:** examples below are the CLI path (preferred). If
> `command -v pandastudio` returned empty, mentally translate each
> verb — e.g. `pandastudio system.status --json` →
> `system_status` MCP tool, `pandastudio project.add-zoom --id=… …` →
> `project_add_zoom` with the same args.

```bash
# 1. Confirm the server is reachable AND the user has a license.
#    MCP equivalent: call `system_status` with no args.
pandastudio system.status --json

# 2. Discover what's available — never guess command names.
#    MCP equivalent: call `system_list_commands`.
pandastudio commands

# 3. Render a motion graphic from a bundled template (the primary path).
#    See the "Motion graphics" section for the full catalog.
JOB=$(pandastudio motion.generate \
  --templateId=creator-card \
  --slots='{"headline":"live demo","eyebrow":"now","brandColor":"#2563EB"}' \
  --aspectRatio=16:9 \
  --json | jq -r '.data.jobId')

pandastudio job.wait --id="$JOB" --json | jq '.data.job.result'

# 4. Add the rendered clip to the timeline at the playhead / a given time.
pandastudio project.add-motion-graphic --id="$PROJECT" --fromJob="$JOB" --durationMs=4500
```

That's the whole loop: probe → discover → call → (if async) wait. Every richer workflow is a composition of those four steps.

> **`job.wait` timeouts are not failures.** Default 5 min, hard cap 30 min. If the wait returns `{ job, timedOut: true }`, the job is **still running** — call `job.wait` again with the same id to keep polling. NEVER treat `timedOut: true` as a render failure; the underlying render keeps going regardless of whether anyone's waiting on it. For heavy 30s @ 1080p motion-graphic renders, expect 8–15 minutes — pass `--timeoutMs=600000` or higher up front, or re-poll until the result lands.

## Before any tool call: license check

Always run `pandastudio system.status --json` first. Read the `license` block:

| Field                          | What it means                                                  |
|--------------------------------|----------------------------------------------------------------|
| `licensed: true`               | Full surface available.                                        |
| `licensed: false` + `trialUsesRemaining > 0` | Active trial. Full surface available.            |
| `automationGated: true`        | Trial expired, no license. Only `system.*` and `window.focus` work. **Stop and tell the user to activate a license in Settings → License.** |

If the call fails with a connection error, the CLI auto-launches PandaStudio and waits up to 60 s. If it fails with `invalid or missing bearer token`, the on-disk credentials at `~/.config/pandastudio/{token,port}` rotated mid-flight — wait 2 s and retry once.

## Workspaces (v1.19+)

PandaStudio is multi-workspace as of v1.19. Every `project.*` / `export.*` / `motion.*` / `caption.*` / `audio.*` query operates inside the **active workspace** — the one listed in `workspace.current`. Users (typically agencies) separate clients into their own workspaces so credentials, exports, and YouTube connections never cross-contaminate.

**Right after `system.status`, check the workspace context:**

```bash
pandastudio workspace.list --json | jq '.data | { current: .currentWorkspaceId, count: (.workspaces | length), cap: .limit }'
```

The returned `limit.max` is:
- `1` — Starter plan or Trial
- `3` — Creator plan
- `null` — Team plan (unlimited)

**Switching workspaces:**

```bash
# Get the id of a specific client's workspace
WS=$(pandastudio workspace.list --json | jq -r '.data.workspaces[] | select(.name == "ACME Agency — Client A") | .id')
pandastudio workspace.switch --id=$WS --json
# Every subsequent query now operates inside that workspace.
```

**Creating a workspace:**

```bash
# Agencies: one workspace per client.
pandastudio workspace.create --name="ACME Agency — Client A" --switchTo=true --json

# If the plan cap is hit, the response looks like:
# { "ok": false, "error": "Your Starter plan allows 1 workspace. Upgrade to Creator to create more.",
#   "details": { "code": "workspace_limit_reached", "upgradeTo": "Creator" } }
# Tell the user to upgrade at writepanda.ai/#pricing; do NOT retry.
```

**Deleting (destructive):** call `workspace.contents` first so you can show the user what will be lost, then `workspace.delete`. Projects' on-disk `.pandastudio` files stay — only the library rows disappear. YouTube-published videos stay on YouTube (we can't delete those); we only drop the local connection + cache.

```bash
pandastudio workspace.contents --id=$WS --json | jq '.data.counts'
# { "projectCount": 12, "exportCount": 4, "publishedVideoCount": 3 }
# Confirm with user before:
pandastudio workspace.delete --id=$WS --json
```

**Don't quietly switch workspaces mid-task.** If you need to operate in a different workspace than the one the user opened, confirm with them first. Crossing client boundaries silently is how agency relationships break.

### ⚠ When given a project id with no other context

If the user hands you a project id (in chat, in a CSV, in a webhook payload) and you don't know which workspace it belongs to, **always run `project.locate` FIRST**, before any read/edit/export/publish:

```bash
RES=$(pandastudio project.locate --id=$PID --json)
# { "data": { "id": ..., "filePath": ..., "workspaceId": ..., "workspaceName": "Client A",
#             "isInActiveWorkspace": false } }
IN_ACTIVE=$(echo "$RES" | jq -r '.data.isInActiveWorkspace')
WS_NAME=$(echo "$RES" | jq -r '.data.workspaceName')

if [ "$IN_ACTIVE" != "true" ]; then
  # STOP. Do not silently switch. Ask the user.
  # "This project lives in workspace '$WS_NAME', current is '<X>' — switch?"
fi
```

**Why this matters:** `project.read` happily resolves a project from any workspace, but `export.publish-youtube`, `media.generate-image`, `export.generate-thumbnail`, and `youtube.list-accounts` all use the **active workspace's** credentials. Editing project A while workspace B is active and then publishing → the video lands on Client B's YouTube channel. **The worst kind of mistake.**

**Every `project.read` response now also carries the workspace fields** (`workspaceId`, `workspaceName`, `isInActiveWorkspace`) — so even if you skipped `project.locate`, you can still detect the mismatch from the read response and bail before mutating anything. But `project.locate` is cheaper (no project body) and clearer in intent — call it first when working from a bare id.

**Hard rule: never call `export.publish-youtube` without confirming `isInActiveWorkspace === true` for the project being published.** If the user asks you to publish a project in a different workspace, walk them through the explicit switch:

```bash
pandastudio workspace.switch --id=$TARGET_WS --json
# Then re-run any pre-flight that depends on workspace state
# (license check, youtube account list, replicate key check)
```

### Project-look defaults (v1.49.1+)

Save a workspace's preferred **look** once so every NEW project and fresh recording starts from it — the user doesn't re-pick a background / caption style each time. Per-workspace. Covers background (`wallpaper`), `captionSettings`, and editor `editorDefaults` (padding, shadow, corner radius, blur). The editor also exposes this as a "Save as default for new projects" button.

```bash
# Read the current defaults (null = none set)
pandastudio workspace.get-project-defaults --json

# Set them — pass any subset; unknown fields are dropped.
pandastudio workspace.set-project-defaults \
  --defaults='{"wallpaper":"/wallpapers/wallpaper5.jpg","captionSettings":{"enabled":true,"templateId":"editorial"},"editorDefaults":{"padding":18,"borderRadius":8}}' \
  --json

# Clear them
pandastudio workspace.set-project-defaults --defaults=null --json
```

Use when the user says things like "use this background for all my videos" or "always start new projects with these captions". Applies to projects/recordings created AFTER it's set — it doesn't retro-edit existing projects.

## Organising projects, renaming, transcription languages

Folders, `project.rename`, project-look defaults, transcription-language switching (Parakeet/Whisper), and transcribing a standalone file → text/SRT/VTT. Full detail: [`reference/projects-and-transcription.md`](reference/projects-and-transcription.md).
## Shorts: turning an exported video into vertical clips

Discover shots (`export.find-shots`), fork the source project per shot (`project.fork-from-shot`), the 9:16 vertical playbook, drift detection, and batch N shorts. Full detail: [`reference/shorts.md`](reference/shorts.md). To make a short actually RETAIN — "make it engaging/viral", "edit like Hormozi / Ali Abdaal / a podcast clip" — load [`reference/shorts-styles.md`](reference/shorts-styles.md): four evidence-based recipes with the seven retention laws, quantified caption/zoom/overlay parameters, and a render-frame verification pass. Load [`reference/shorts-cheatsheet.md`](reference/shorts-cheatsheet.md) alongside it — exact command shapes plus a hyperframes starter shell, so you never grep schemas or other reference files mid-edit. For `youtube-long` edits that should RETAIN (not just play clean), load [`reference/longform-styles.md`](reference/longform-styles.md) — quantified from a 9-video measured study (Ali Abdaal / MKBHD / Fireship, July 2026): three recipes (educator-pip, product-review, dev-explainer), the two-level rhythm, keyword pops instead of burned captions, in-edit segmentation, and ending liturgy.
## Publishing (YouTube + Instagram)

**Hard rules:** YouTube `privacyStatus` defaults to `unlisted` — never public without explicit user say; Instagram needs a Business/Creator account; never publish in the wrong workspace (confirm `isInActiveWorkspace`). Flows: connect → publish an export. Full detail: [`reference/publishing.md`](reference/publishing.md).
## Editorial decisions — what to ask, what to assume, what NEVER to ask

Video editing is a creative task with hundreds of small decisions. Asking the user about all of them kills the magic — they came to you because they wanted to type "edit this" and see something happen. Asking about none of them produces wrong-shape output. The rule:

**Ask only when the answer is genuinely user-specific AND can't be inferred AND is hard to reverse.** Default everything else, narrate what you did, and iterate via preview.

### The default edit pipeline (vague "edit my video", no specifics)

When the user asks to **edit / polish / clean up** a video without naming a
specific operation, this is the intended end-to-end pipeline, in order:

1. **Transcribe** any clip where `clipStates[i].transcribed === false` (`transcript.transcribe`).
2. **Remove filler words + immediate repeats** (`transcript.remove-fillers`).
3. **Fix transcript spelling / STT errors.** Read the transcript and correct
   obvious misspellings — *especially* product, brand, person, and technical
   names the speech-to-text got wrong (e.g. "Right Panda" → "WritePanda") —
   with `transcript.find-replace` (patches the word text in place, keeps
   timing). Do this BEFORE captions, motion graphics, or title generation —
   they all derive their text from the transcript, so a typo propagates.
4. **Cut bad takes.** Run `transcript.find-issues` (read-only — it never
   edits). For each `duplicate-take` / `false-start`, the **default is to keep
   the most recent (last, cleaner) take and delete the earlier attempt** —
   feed the candidate's `wordIds` (which point at the discarded attempt) into
   `transcript.delete-words`. **EXCEPT `severity: "low"` candidates — those
   are REVIEW-class: KEEP them by default.** A low-severity `false-start`
   means the restart diverges from the fragment, which is often deliberate
   parallel structure ("one for transcription, one for outreach"), not a flub
   — deleting it destroys the sentence. Only delete a low candidate when the
   surrounding context clearly shows an abandoned take. If a candidate is
   genuinely ambiguous (the repeat might be intentional emphasis, or you
   can't tell which take is better), **ask the user which take to keep**
   rather than guessing.
5. **Remove silences** (`transcript.remove-silences`, 500ms default — same as
   the UI Remove Silences button) — after
   content cleanup so it tightens the final timing. The verb returns
   `removedCount` + the new `revision` (synchronous — you'll know immediately
   how many it cut). **Every transcript cleanup step (2, 4, 5) ADDS trims and
   shifts the edited timeline**, so always finish cleanup BEFORE placing
   graphics/zooms/lower-thirds (steps 8–9). If you ever place a region from a
   transcript word *before* cleanup is done, pass `--anchorSourceMs` so it
   re-anchors when the timeline shifts. (If the user already removed silences in
   the UI, a fresh `project.read` shows the new `trimCount` / `editedDurationMs`
   / `totalTrimmedMs` — treat that as "silences already done".)
6. **Clean audio** (`audio.clean`) on clips where `audioCleaned === false`.
7. **Add captions** — `caption.toggle` + `caption.set-template` (default `bold`
   per profile; see the caption styles in "DO BY DEFAULT").
8. **Add motion graphics** — follow the Motion-graphics **Rules** + selection
   guide: `motion_list` first, vary templates by beat, prefer the **featured
   (premium) templates** (`paper-panel` / `vox-side-panel` / the Vox family),
   and for **camera-only / imported footage lead with `paper-panel` or
   `vox-side-panel` designed segments** (not the plainer `split-panel`). **On any
   talking-head (`kind === "camera"`), open with a `caption-editorial-emphasis`
   TOPIC card in the first 10–30s** that names what the video is about (from the
   speaker's opening lines) — the default hook for talking-heads. **For explainer
   content, author custom animated diagrams / flowcharts / charts** when the
   speaker explains how something works or connects and no template captures it
   (see "Authored graphics") — don't flatten a real explanation into a bullet
   list.
9. **Add emphasis zooms** — punch in on the key beats for a dynamic, edited
   feel (see "Emphasis zooms" just below).
10. **(Only when the brief is "make it engaging / cinematic / dynamic / give it
   energy", NOT a plain "clean it up")** — add **scene transitions** at the
   real section boundaries (`project.add-transition`, ~1 per major section, one
   consistent style). See the "Effects (FX) & transitions" section — restraint
   is the rule: a transition belongs at a section change, never on every cut.
   **Do NOT add FX overlays here** — FX is explicit-request-only (see the
   "NOT part of the default pipeline" list below); "make it engaging" does
   not authorize adding effects.
11. **Generate** title / description / timestamps, then **preview**.

**Do not skip steps, and report what actually ran.** Every step the user
confirmed for the full polish must be an ACTUAL verb call this session. Three
steps are skipped far too often — **none of them is optional in a full polish**:

- **`transcript.remove-fillers`** — vocalised pauses (um, uh, uhm, umm, hmm, hm) AND immediate repeated words. **Default behavior is the SAFE tier only** — the words above are sounds, never lexical, so removing every match is unambiguously correct. Pass `--aggressive` to additionally remove `like / you know / i mean / sort of / kind of`; these are real English words too, so the aggressive mode will sometimes cut legitimate uses ("I like this template" loses "like"). Only opt in when the user explicitly asks for a thorough cleanup AND is willing to skim the result for false positives.
- **`transcript.find-issues` → `transcript.delete-words`** — **bad takes and
  repeated phrases.** `find-issues` is read-only; you MUST then actually delete
  the discarded `wordIds` (keep the most recent take). Running `find-issues` and
  *not* deleting is the same as doing nothing — the bad take stays in the video.
  (`severity: "low"` false-starts are the exception — REVIEW-class, keep by
  default; see the transcript verbs table.)
- **`transcript.remove-silences`** — the single most-skipped step; silence
  removal is what makes a talking-head edit feel tight.

After the pass, your summary MUST quote the real result each verb returned
(e.g. *"removed 14 fillers, cut 2 bad takes + 3 repeated phrases, removed 67
silences, captions on, 4 graphics, 6 zooms"*). **Never claim a step happened
unless the verb actually ran and you saw its result** — "edited everything" with
bad takes, repeats, or silences still in the cut is a failure the user notices
immediately. If a step legitimately returned 0, say so explicitly rather than
omitting it. Treat the numbered pipeline as a checklist: before reporting done,
confirm each item was run (with its count) or consciously skipped for a reason.

**Ask-first — exactly once, for scope.** Because this is a large, visible
transformation, when the request is a vague "edit my video", confirm scope in
ONE message before running it: list the pipeline above and ask *"Want me to do
the full polish — remove fillers/repeats/silences, fix transcript typos, cut
bad takes (keeping the latest), clean audio, add captions, motion graphics, and
emphasis zooms? Or just some of it?"* Combine this with the destination-profile
question if that's also unknown — one message, not two.
- On **yes** (or if they said "just go" / "do everything" / "use defaults") →
  run the whole pipeline without further per-step asking, then narrate.
- If they **named a specific operation** ("just add captions", "only remove
  silences", "add a lower third") → do exactly that and nothing else.

**NOT part of the default pipeline — add ONLY on explicit request:**
- **Background music.** Never add a music track to "edit my video" / "do the
  full polish". Add it only when the user explicitly asks ("add background
  music", "put a track under it"). "Full polish" does NOT include music.
- **Intro / outro cards.** Never open with a title card or append an outro/CTA
  card unless the user explicitly asks for one ("add an intro", "add an outro").
  A plain edit keeps the user's footage as the first and last frame.
- **FX overlays (`project.add-fx`).** Never add an FX overlay (film burn, light
  leak, grain, VHS, embers, film-flash, etc.) on your own — NOT on a plain
  edit, and NOT even for "make it engaging / cinematic". FX is a deliberate
  creative choice the user makes; add one only when they explicitly ask for an
  effect ("add a film burn between these clips", "put some grain on it", "add a
  light leak"). When they do, follow the restraint rules in the "Effects (FX) &
  transitions" section. (Transitions are different — those ARE part of the
  engaging-tier flourish; see step 10.)

If you think music, an intro/outro, or an effect would help, you may *suggest*
it in your narration ("want me to add a music bed, an intro card, or a film
burn?") — but do not add it until they say yes.

### Emphasis zooms — punch in on the key beats

A perfectly static frame reads as unedited. Adding `project.add-zoom` pushes on
the moments the speaker emphasizes — the payoff word, a "look at this", a key
number, a name reveal — gives the cut a dynamic, professionally-edited feel,
and is part of the default polish. Find the beats from the transcript
(emphatic phrasing, the point of a sentence, a stated result) and place a
~1.5–2.5s zoom on each. Depth: modest (2–3) for talking-head emphasis; punchier
(3–5) for a UI/detail reveal. **For `kind === "screen"` recordings, prefer
cursor-telemetry-driven zooms; for `camera`/`upload`, place them on verbal
emphasis.** Don't over-zoom — aim for a real beat roughly every 10–20s, not a
constant push. (Don't pre-ask about zoom positions; infer and let the user
redirect via preview.)

### MUST ASK (3 things, only when context is missing)

<HARD-GATE>
Before issuing `project.new`, `project.add-*`, `motion.generate`, or `motion.render-html` calls that depend on user-specific information, you MUST have:

**1. Destination profile.** This single answer drives aspect ratio, pacing, zoom cadence, caption template, and whether to add lower-thirds. (Background music and intro/outro cards are NOT profile defaults — add them ONLY when the user explicitly asks; see the default edit pipeline.) Try to infer first, then fall back to asking:

Inference rules (in order — first match wins). Everything below the user's
own words comes from ONE `project.read --includeTranscript=false` you're
running in pre-flight anyway — this costs zero extra calls:
   - User mentioned "Shorts" / "TikTok" / "Reels" / "Instagram story" / "vertical" / "phone"? → **`shorts`** profile (9:16, punchy)
   - User mentioned "LinkedIn" / "client pitch" / "professional" / "corporate"? → **`linkedin`** profile (16:9 or 1:1, restrained)
   - User mentioned "Loom" / "internal" / "async update" / "for the team" / "quick video"? → **`loom`** profile (minimal editing)
   - User mentioned "YouTube" / "long-form" / "tutorial" / "vlog" / "channel"? → **`youtube-long`** profile (16:9, full pipeline)
   - Project was created by `project.fork-from-shot`? → **`shorts`** (it exists to BE a short)
   - Project aspect ratio is already 9:16 or 1:1 (project setting, not just source orientation — the user chose that canvas)? → **`shorts`**
   - Workspace project defaults name a destination (`workspace.get-project-defaults`)? → use it
   - **Duration bands** (total source duration):
       · ≤ 90s → **`shorts`** — regardless of orientation; nobody publishes a 45s "long-form video", and a landscape short gets auto-reframed to 9:16
       · > 8 min → **`youtube-long`** (or `loom` if it's a screen recording with cursor telemetry and no user framing — internal walkthroughs look exactly like this)
       · 90s–8 min → genuinely ambiguous: could be a long-form video OR source to cut a short from. Use content type as tiebreaker (screen recording → youtube-long/loom; phone-framed talking head → shorts), else ASK.
   - Source clip is portrait (height > width), no other signal? → **`shorts`**
   - Source clip is landscape, no other signal? → **`youtube-long`** (safe default — most common)
   - **Ambiguous or no clips yet?** → ASK ONE QUESTION:
     > "Where is this going — YouTube long-form, Shorts/TikTok/Reels, LinkedIn, or internal/async (Loom-style)?"

When the user says "just go" / "use defaults" / "I don't care" → `youtube-long`
**unless the duration band says shorts** (a 60s clip with "just go" is a short).

Special case — LONG recording + short-form ask ("make a short from this",
"clip this for TikTok"): that's not one profile, it's the fork-from-shot
pipeline (reference/shorts.md) — discover shots in the long source, fork a
9:16 project per shot, then apply the `shorts` profile to the fork.

The profile is the source of truth for every default below. See the [Video editing playbook](#video-editing-playbook--end-to-end-recipe-per-destination) section for the full profile table.

**2. Lower-third content.** If the user said "add a name plate" / "introduce me" / "add a lower-third" but didn't give the actual text, ASK both fields in one message:
   > "What's the name and the subtitle (e.g. role / company)?"

   Don't fabricate a name. Don't invent a job title. Skip this question entirely for the `shorts` and `loom` profiles — they don't use lower thirds.

**3. Brand / style direction.** If the user named a style ("MrBeast" / "MKBHD" / "Vox" / "Kurzgesagt" / "Veritasium" / "Linear" / "Infinite"), first see whether a bundled template fits and set its colors via `slots` (most accept brand / ink / accent colors). Only when no template matches the named look, author custom HTML — translate their palette, typography, and motion vocabulary into a composition built against [`reference/motion-philosophy.md`](reference/motion-philosophy.md) §1. If they gave no style reference AND there are multiple source clips that suggest a brand context, ASK ONE QUESTION:
   > "Any brand colors, fonts, or visual references — or default look?"

**4. Templated vs. custom for a from-scratch video.** When the brief is a video
built FROM SCRATCH where the motion graphics ARE the whole video (promo,
explainer, intro/outro, product teaser, CTA piece — no source clip on the main
track), do NOT silently reach for bundled templates: they read as generic for a
hero/marketing asset. Ask once up front:
   > "Templated quick version, or fully custom? For a promo I'd default to fully custom scenes — they look bespoke, not templated."

   If they don't care, **default to fully custom** (`motion.render-html`, scenes
   authored from `reference/motion-philosophy.md`). Only use templates as the
   backbone here if they explicitly choose speed — and say so. (This question does
   NOT apply to Mode A — graphics layered over existing footage — where templates
   stay the default and you should not ask.)

**5. Voiceover & music for a from-scratch promo.** Narration and a music bed are
first-class capabilities (`media.generate-narration` — 3 TTS models;
`media.generate-music` / bundled `asset.list-music`). For a Mode-B piece (promo,
explainer, intro/outro, teaser), if the brief doesn't already specify, **ASK up
front** whether to add them:
   > "Want a voiceover and/or a music bed? Both shape the timing, so I'll lock them in before building the scenes."

   They materially change the build — **if there's narration, generate the VO
   FIRST and time each scene to its line length** (TTS runs longer than you'd
   guess; visuals-first forces a re-time pass). See "Audio: decide voiceover &
   music FIRST" in [`reference/promo-and-mg-videos.md`](reference/promo-and-mg-videos.md).
   Don't silently ship a silent promo when audio was available.

If these are clear (or already specified), proceed without asking. Combine multiple asks into a single message when possible.
</HARD-GATE>

### DO BY DEFAULT, narrate transparently

For these operations, run them without asking and tell the user what you did in the same message. Every one is reversible (trims are spans, cleaned audio is a sibling file, generated text is just text — nothing is destructive).

**Before running `transcript.transcribe` or `audio.clean`, always call `project.read` and inspect the `clipStates` array in the response.** Each entry looks like:

```json
{ "clipId": "clip-1", "mediaPath": "...", "durationMs": 62400,
  "transcribed": true, "wordCount": 312,
  "audioCleaned": false, "kind": "camera" }
```

- `transcribed: true` → skip `transcript.transcribe` for that clip — it already has a transcript. Running it again would overwrite any manual word edits the user made in the app.
- `audioCleaned: true` → skip `audio.clean` for that clip — the `.cleaned.wav` already exists.
- `kind` → how the clip was captured: `"camera"` (talking-head — a PandaStudio camera-only recording), `"screen"` (screen recording, maybe with a webcam PiP), or `"upload"` (external import). **This is the authoritative signal for your visual strategy — use it, don't guess from aspect ratio:** `kind === "camera"` (talking-head) OR `kind === "upload"` (imported video) → there's no screen to zoom into, so **lead with a premium designed segment — `paper-panel` or `vox-side-panel`** (`project.add-designed-segment`) as the default for explainer beats; it's the highest-leverage way to make static footage look produced (`split-panel` is the plainer fallback — see the Motion-graphics "Rules" §5). `kind === "screen"` → use cursor-telemetry zooms, never clip-transform splits. On v1.28+ recordings this is stamped at capture; older projects don't have it, so `project.read` **infers** it (paired webcam track or cursor telemetry → `screen`; managed-dir media → `camera`; else `upload`) and sets `kindInferred: true`.

**When `kind` is inferred or absent, NEVER assume `screen`.** `screen` is the costly wrong guess — it suppresses the camera enhancements (designed segments, emphasis zooms) and a talking-head ends up flat. So:
- A clip flagged `kindInferred: true` is a hint, not gospel. If it reads `screen` but you have any doubt (the footage is a person talking, not a UI; no cursor), **treat it as `camera`** — the default when unsure is always `camera`, never `screen`.
- If it genuinely matters and you can't tell, **ask the user** ("Is this clip a screen recording, or you on camera?") rather than guessing `screen`.
- Once known, **lock it**: `project.set-clip-kind --clipId=… --kind=camera|screen|upload|podcast` stamps an authoritative value so no future agent has to re-guess (ideal for pre-v1.28 projects — stamp each clip once). `podcast` = a two-speaker composite (host=mediaPath, guest=webcamPath) recorded via Record Podcast; it's set automatically at ingest and edits as one clip with the `podcast` webcam layout.
- `contentIssues` (top-level on the `project.read` result, not per-clip) → a count summary `{ total, duplicateTakes, falseStarts, adjacentRepeats }`, present only when something is transcribed. If `total > 0`, run `transcript.find-issues` during the polish pass to see the actual candidates.

Only pass un-processed clips to each operation. If every clip is already transcribed, go straight to `transcript.get`.

| Operation | Default behaviour |
|---|---|
| `transcript.transcribe` | Run only on clips where `clipStates[i].transcribed === false`. Skip the rest. |
| `transcript.remove-fillers` | Default: auto-remove vocalised pauses (um/uh/uhm/umm/hmm/hm) + immediately-repeated words. Trim regions; fully reversible. Pass `aggressive=true` to ALSO catch lexical-word fillers (like, you know, i mean, sort of, kind of) — these can wrongly cut legitimate uses ("I like this template" loses "like"), so opt in only when the user wants a thorough cleanup. |
| `transcript.find-issues` | Run after remove-fillers. Surfaces re-takes (`duplicate-take`), abandoned restarts (`false-start`), and stutters (`adjacent-repeat`) as candidates — each with the `wordIds` of the discarded attempt. **Read-only — it never edits.** **Default: keep the most recent (last) take and delete the earlier attempt** by feeding the candidate's `wordIds` into `transcript.delete-words` — **but `severity: "low"` candidates are REVIEW-class: keep them by default** (a low `false-start` = the restart diverges from the fragment, often intentional parallel structure like "one for transcription, one for outreach"). The detector already skips comma-terminated parallel list items and lone stopword "repeats" across pause tokens. Review against context first — if a repeat looks intentional (emphasis) or you can't tell which take is cleaner, ask the user which to keep rather than blind-applying. |
| `transcript.remove-silences` | Run after the content cleanup. Runs the SAME two passes as the UI Remove Silences button and unions them: (1) transcript word-gaps (leading, between-word, trailing) and (2) ffmpeg audio-level `silencedetect` on each clip's media — pass 2 catches real dead air the transcript misses when speech-to-text invents phantom words over quiet stretches, which is why this now removes the same sections a manual click would (it previously did pass 1 only and left audio-only silence behind). Default threshold 500ms; don't hand-pick a higher value "to be safe" — that leaves dead air the user expects gone. |
| `audio.clean` | Denoise only clips where `clipStates[i].audioCleaned === false`. Writes a sibling `.cleaned.wav`; original audio untouched. |
| `caption.set-template` (when user said "add captions" without naming a style) | Default to `bold`. Tell user other templates exist (`classic, modern, minimal, spotlight, boxed, neon, colored, editorial`). `editorial` is magazine-style emphasis — the currently-spoken word renders big + accent while the rest of the line shrinks, so emphasis sweeps the line. |
| `llm.generate-title` / `llm.generate-description` / `llm.generate-timestamps` | Generate after the edit pass. Show the user; let them say "regenerate" or "use this exact title" or edit inline. |
| Specific zoom moments | Heuristically pick from the transcript ("you said 'click here' at 12.4s — adding a zoom"). Don't pre-ask. Iterate via preview. |
| FX overlays (`project.add-fx`) | **NOT do-by-default.** Never add an effect on your own — not on a plain edit, not for "make it engaging". Only when the user explicitly asks for one ("add a film burn", "put grain on it"). When they ask, place it where they said and follow the restraint rules. |

**Example of good narration after an edit pass:**

> "Edited.
> • Transcribed both clips (136 words).
> • Removed 14 fillers + 3 repeats. Trim regions are reversible — say 'undo fillers' if you want any back.
> • Cut 2 bad takes (kept the cleaner second attempt each time).
> • Removed 67 silences (>500ms), tightening ~48s of dead air.
> • Cleaned audio with DeepFilter on both clips.
> • Added a zoom at 12.4s where you said 'click here'.
> • Captions enabled with the bold template (8 other styles available).
> • Generated a title: *'How I Built This in 24 Hours'* — say if you want a different angle.
>
> Opening preview now."

Note how the summary names the **actual count for every step that ran** —
including silences. That's the bar: a summary line backed by a real verb call
and its returned result, never a vague "cleaned it up".

### NEVER ASK about

These produce friction with no upside. Just decide.

- Whether to remove filler words (it's reversible — do it)
- Whether to remove repeated words (same)
- Whether to clean audio (sibling file, original untouched)
- Specific zoom positions or focus points (infer; user redirects via preview)
- Specific caption colors / font sizes (template defaults are good)
- Whether to generate a title / description / timestamps (cheap, useful)
- Whether to enable captions when user said "add captions" (yes — they said yes)
- Specific lower-third design/colour (use defaults; user can swap)

### Preview, then export. Never export, then preview.

After a meaningful edit pass:

1. Call `preview.show --id=<uuid>` (opens the editor focused on the project — same single-step UX, ~2-3s).
2. Tell the user what you did (the narration block above).
3. Ask: *"Does this look right? Anything to tweak before I export?"*
4. **Only after explicit user confirmation** call `export.start`.

Export is 30-90s and produces a multi-MB MP4. Wasting an export because you skipped the preview is the worst UX failure in this surface. The editor's preview pane shows every effect / caption / FX / lower-third / motion graphic / zoom region exactly as the export will render them.

## Output modes

- **Default**: pretty one-line summaries to stdout. Show these to the user.
- **`--json`**: raw `{ ok, data, error }` envelope. **Always use `--json` when you intend to parse the response or chain commands** — pipe through `jq`.

## Discovery (the most important habit)

Don't memorise the command surface — the registry is the source of truth and it grows. Every PandaStudio launch self-describes:

```bash
pandastudio commands --json   # full schema with arg hints per command
```

Pattern-match `summary` against the user's intent. If you can't find a verb that fits, **say so** rather than fabricating one.

## Async jobs

`motion.generate` and any future `export.start` return a `jobId` immediately — the `data` block does **not** carry the result. Wait server-side:

```bash
pandastudio job.wait --id="$JOB" --timeoutMs=120000 --json
```

Terminal `job.status` is `succeeded | failed | canceled`. Read `result.outputPath` for the rendered MP4.

## Argument shape

Flags are either **scalars** (`--name=value`) or **JSON** (`--slots='{"title":"x"}'`). Anything starting with `{` or `[` is parsed as JSON. Strings stay strings; `true` / `false` / numbers auto-coerce.

## Error model

Every response: `{ ok: boolean, data?: ..., error?: string, details?: ... }`.

- HTTP 4xx/5xx → transport problem. CLI exits ≥ 1 to stderr.
- HTTP 200 + `ok: false` → handler-level error. CLI exits 1 with `error: <msg>` to stderr. The most useful machine-readable codes:
  - `license_required` / `trial_expired` — show the user the license activation flow
  - `unknown command` — typo; run `pandastudio commands` to recover
  - `invalid or out-of-tree project path` — project paths must live under the user's recordings dir; never pass arbitrary absolute paths

## Composing a real edit

> **HARD INVARIANT — every video the agent creates lives in a project.**
>
> Whatever the brief — promo, explainer, transcript-driven edit, PDF-to-video,
> a single motion graphic, B-roll over a recording, a one-shot title card —
> the **editor project is the deliverable**, not the raw MP4. Loose files in
> `~/Library/Application Support/pandastudio/recordings/` are *intermediates*
> the editor consumes; they are never the agent's hand-off.
>
> The two valid starting states:
>
> 1. A project is **already open** in the editor (`project.current` returns
>    a non-null id) → use it. Add your work to that timeline. Save. Preview.
> 2. No project is open (`project.current` returns null, or the chat opened
>    from the home screen) → **`project.new` is your FIRST tool call**, before
>    any motion render / transcription / b-roll generation. Name the project
>    something the user will recognise ("PandaScribe Promo", "Q4 Recap",
>    "How to install — explainer"). Pick the aspect ratio from the destination
>    profile (16:9 YouTube, 9:16 Shorts, 1:1 LinkedIn square).
>
> After the work lands in the project, `preview.show --id=<project-id>` to
> open it in the editor for the user. THAT is the hand-off. The chat message
> reports the project name/id, not a file path on disk.
>
> Exceptions are vanishingly rare — only when the user explicitly says
> "just give me the MP4, no project" (e.g. they want to upload it elsewhere
> right away). When in doubt, default to project.

Flow is always: **create or open a project → add things → save (conflict-safe)
→ preview.** Every verb's arg schema is discoverable at runtime — call
`system_list_commands` (MCP) or `pandastudio commands` (CLI), or see
`reference/commands.md`. So this section is the *judgment* the schema can't give
you: which verb, in what order, and the non-obvious gotchas.

### Target the right project

- **`project.new --withMedia='["/a.mp4","/b.mp4"]'`** — create pre-loaded; clip
  durations are FFmpeg-probed automatically.
- **`project.current`** → the open editor project (`{id,path,name,revision,clipCount}`
  or `null`). Use it when the user says "this one" / "what's open" — don't ask
  for an id. `null` ≠ "no projects exist"; fall back to `project.list`.
- **`project.read --id`** → full state. Key fields the schema won't spell out:
  - **clips** at `mainTrack.clips[]` — each carries `sourceDurationMs` (the
    clip's own length); there is **no per-clip `durationMs`** on the raw clip.
    For a normalized per-clip view use the top-level `clipStates[]`, where each
    entry has `clipId`, `durationMs` (= sourceDurationMs), `kind`, `transcribed`.
  - **motion-graphic / transition overlays** at `editor.mediaOverlayRegions[]`.
  - **audio overlays** (voiceover, music) at **top-level `project.audioOverlays[]`**
    — NOT under `editor`. Different array from the visual overlays.
  - **top-level read summary fields**: `aspectRatio`, `editedDurationMs`
    (post-trim — use for cadence planning), `sourceDurationMs`, `totalTrimmedMs`,
    `trimCount`, and per-clip `clipStates[].kind` (`camera`/`screen`/`upload`,
    your visual-strategy signal).
  Pass `--includeTranscript=false` after the first read.

### Adding things — the gotchas (call discovery for the arg schemas)

- **Clips:** `add-clip` (`--atIndex=0` prepends), `move-clip`, `split-clip`,
  `remove-clip`. **`project.delete` is permanent — no trash.** By default it only
  removes the project file and KEEPS the original source recording. Pass
  `--deleteRecording=true` to ALSO delete the original recording file(s) from disk
  (irreversible — only do this when the user explicitly asks to delete the source
  footage, not just the project). Returns `deletedRecordings` (count removed).
- **Motion graphics — use `--fromJob`, NOT `--file`, for render outputs.** Pass
  the render `jobId` (after `job.wait`); the server resolves the path itself:
  ```bash
  JOB=$(pandastudio motion.render-html --htmlPath=/tmp/card.html --durationMs=4000 --json | jq -r '.data.jobId')
  pandastudio job.wait --id="$JOB" --json
  pandastudio project.add-motion-graphic --id=$ID --fromJob="$JOB" --durationMs=4000
  ```
  `--file` is only for external uploads and **must be quoted** — render outputs
  live under `…/Application Support/…` (a space); an unquoted path truncates and
  silently produces a dead overlay (shows on the timeline, never renders).
- **Placing on a spoken word in a trimmed timeline:** trims make source-time ≠
  output-time. From `transcript.get`, each word has `startMs` (source) and
  `editedStartMs` (output; `null` = inside a trim → skip it). Pass the **source**
  `startMs` as the position **and** `--anchorSourceMs=<same>` so the region
  re-anchors when later cleanup trims shift the timeline. `timeline.source-to-edited
  --sourceMs=N` returns the output time (or `null` if trimmed).
- **Mid-video graphic on camera / upload footage:** don't cover the host — use
  **`project.add-designed-segment`** (the split-panel beat; see Motion-graphics
  Rules §5). Screen recordings use `project.add-zoom` instead, never a split.
  **Never place a zoom inside a designed-segment / split window** — the camera is
  already cropped to a half-frame band, so zooming it looks wrong. Zoom the
  full-frame stretches, split the rest.
- **Zoom depth → scale factor.** `depth` (1–6) maps to a fixed zoom multiplier.
  When the user asks for "a 1.5x zoom," translate it with this table — there is
  no separate scale arg:

  | depth | scale | feel |
  |---|---|---|
  | 1 | 1.25× | barely-there nudge |
  | 2 | 1.5× | **soft, modern default** (talking-head, tutorials) |
  | 3 | 1.8× | clear emphasis (UI clicks, callouts) |
  | 4 | 2.2× | strong punch-in |
  | 5 | 3.5× | dramatic detail |
  | 6 | 5.0× | extreme macro |
- **Zoom / fx / SFX:** `add-zoom` (default depth 2 = 1.5× + swoosh SFX;
  `--soundUrl=none` to silence), `add-motion-graphic` (default mouse-click SFX
  as of v1.36.0), `add-fx` (13 bundled FX overlays — film-burn, light-leak, light-flare, lens-flare-sweep, light-streaks, bokeh-drift, prism-leak, dust-scratches, film-grain, vhs-static, embers, snow-drift, film-flash; `--speed=0.25–4` adjusts loop speed, default 1; see the "Effects (FX) & transitions" section for when to reach for each), `set-region-sound` (retune/clear a placed region's
  SFX). Arg values: discovery (`asset.list-fx`).
- **Spotlight / blur (v1.50.0):** `add-spotlight --atMs=<ms> --durationMs=<ms>
  [--kind=spotlight|blur]` — a focus rect over the video. `kind=spotlight`
  (default) DIMS everything outside the rect (draw the eye to one spot);
  `kind=blur` BLURS everything inside it (hide an email, username, or other
  sensitive detail in a screen recording). Rect placement is `--x --y --width
  --height` as 0..1 fractions of the video (default a centred half-size box,
  `x=y=0.25 width=height=0.5`). `--roundness` (px corner radius, default 16),
  `--feathering` (px soft edge, default 12). Spotlight: `--maskOpacity` 0..1
  (surround darkness, default 0.6). Blur: `--blurAmount` px (default 12). The
  rect tracks content through zooms. `atMs` is EDITED time (no anchor arg).
  Edit or delete after placing (v1.85.0): `update-spotlight --regionId=<id>
  [--startMs --endMs --kind --x --y --width --height --roundness --feathering
  --maskOpacity --blurAmount]` patches only the fields you pass (move/resize,
  retime, restyle, or flip spotlight<->blur); `remove-spotlight --regionId=<id>`
  deletes it. Get ids from `project.read` under `editor.spotlightRegions[].id`.
- **Background blur / removal (v3.69.0):** `add-background-effect
  --mode=blur|remove [--atMs=<ms>] [--durationMs=<ms> | --endMs=<ms>]
  [--strength=<px>] [--anchorSourceMs=<srcMs>]` — AI PERSON SEGMENTATION on
  the camera video for the region's span, exactly like a zoom region on the
  timeline (draggable, trimmable, source-anchored, rebases on trims/speeds).
  `mode=blur` keeps the speaker sharp and gaussian-blurs everything behind
  them (video-call style; `--strength` is px sigma at 1080p, default 18).
  `mode=remove` cuts the background away entirely so the project
  wallpaper/background shows through behind the person — pair it with
  `set-wallpaper` for a branded backdrop. Duration defaults to 5000ms.
  CAMERA / TALKING-HEAD footage only — pointless on screen recordings.
  Runs on a bundled on-device model (no network); preview and export render
  it identically. Regions live under `editor.backgroundEffectRegions[]`;
  retime/restyle with `update-region --regionType=background-effect
  [--startMs --endMs --mode --strength]`, delete with `remove-region
  --regionType=background-effect`. Also batchable inside `apply-edit-plan`
  as `{op:'add-background-effect',atMs,durationMs,mode,strength?}`.
- **See a frame to place it (v1.85.0):** `render-frame --atMs=<ms> [--outPath=<png>]`
  composites the preview frame at that edited-time to a PNG and returns
  `{ path, width, height, timeMs, maskRect }`. A vision model should `read` the
  returned `path` to LOCATE on-screen text/UI (e.g. the email to blur), then place
  a focus region. `maskRect` is the video content rect as 0..1 fractions of the
  image — the SAME space as spotlight/blur x/y/width/height. Convert an image-space
  box (ix,iy,iw,ih) to region coords: `x=(ix-maskRect.x)/maskRect.width`,
  `y=(iy-maskRect.y)/maskRect.height`, `width=iw/maskRect.width`,
  `height=ih/maskRect.height`. Typical privacy-blur flow: `render-frame` →
  read PNG → locate text → `add-spotlight --kind=blur` with converted coords →
  `render-frame` again to verify → `export.start`. Caveats: existing focus
  regions are NOT drawn (you see content clearly); the frame reflects any active
  zoom at that time, so prefer an un-zoomed moment for placement.
- **Transitions (v2.98.0):** `add-transition --transitionId=<id> --atMs=<cutMs>` —
  places a scene-change overlay CENTERED on a cut (the opaque peak masks the
  join). Pass `atMs` = the cut time between two clips (from `project.read` clip
  boundaries). **`atMs` here is EDITED (output) time, and add-transition has NO
  `anchorSourceMs`** — unlike add-zoom / add-motion-graphic. If you only have a
  source-time value (a transcript word's `startMs`), convert it first with
  `timeline.source-to-edited --sourceMs=N` and pass the result. Ids
  (`asset.list-transitions`): fade-black, fade-white, flash, light-sweep,
  film-burn, glitch. `--durationMs` defaults to 1000.
  > **Time domains at a glance.** `atMs`/`startMs`/`endMs` are ALWAYS edited
  > (output) time. `anchorSourceMs` (source/raw-recording time) is an *extra*
  > drift-proofing arg on **add-zoom, add-motion-graphic, add-designed-segment,
  > add-lower-third** — pass it alongside `atMs` when `atMs` came from a
  > transcript word so the region re-anchors across later trims. Verbs WITHOUT
  > an anchor (**add-transition**, region edits) need a pre-converted edited time.
- **Lower thirds (v2.96.0):** `project.add-lower-third --name="…" --title="…"
  --atMs=<ms> [--templateId=lt-*]` — ONE async call that renders the nameplate
  template (default `lt-vox-marker`) AND places it as a transparent overlay.
  Returns `{ jobId }`; `job.wait` resolves once the region is placed. Pass
  `--anchorSourceMs` when atMs comes from a transcript word. The 10 `lt-*`
  designs are in the template catalog; they also live in the editor's
  **Lower 3rds** tab. (The pre-2.95 CSS designs + `--designType` are gone;
  the verb now drives the motion-template pipeline.)
- **Reset:** **`project.clear-edits`** — one atomic call wipes every region +
  audio overlays + turns captions off (keeps clips, transcript, aspect ratio;
  `--full=true` also resets LUT/crop/webcam/wallpaper). Use it for "start over";
  do NOT loop `project.remove-region` (that's for removing ONE region by
  `--regionType` + `--regionId`).

### Conflict-safe save

The editor autosaves, so two writers (you + the editor, or two agents) overwrite
each other silently unless you pass **`--expectedRevision`** (from
`project.read`'s `revision`). On conflict you get
`{ code:"revision_conflict", expected, actual, onDiskProject }` — re-read,
re-apply your change, retry. All `project.add-*` verbs accept it too.

### Preview without exporting

`preview.show --id` pops the live WYSIWYG overlay (~1–2s boot; `--atMs`,
`--autoplay`). `preview.seek --atMs` moves the playhead; `preview.hide` closes;
`preview.list` inspects it. **Call `preview.show` after every significant edit**
so the user sees the change live without leaving the chat. (`project.open` opens
the full editor — heavy, for handing off to the user.)

## Motion graphics

PandaStudio ships a curated set of **YouTube-creator templates**. They are
the primary way to add motion graphics — production-grade, editable, and
faster than authoring HTML. Custom HTML (`motion_render_html`) is the
fallback for briefs no template fits (see the next section).

### Rules — recommendations, not rigid law (bias toward DOING)

These are strong defaults, not handcuffs — use your judgment. The worst outcome
is a near-empty timeline because you were being cautious. **A video full of
points should be full of graphics.**

1. **`motion_list` FIRST, every time.** Discover the catalog + each template's
   editable slots at runtime; don't generate from memory or copy a templateId
   out of an example.
2. **Add a graphic on most meaningful beats — don't be shy.** Name-drops,
   claims, numbers, lists, comparisons, tool/product mentions, section changes
   — each is a candidate. If a 5-minute video has ten clear points, ~ten
   graphics is reasonable. **Under-graphicking is as much a failure as the
   wrong graphic** — when a beat clearly wants a visual, add one.
3. **Vary every scene — consistency comes from a shared SYSTEM, not a repeated
   layout.** Hold ONE design system across the video (same palette, type family,
   motion vocabulary) so it feels cohesive — but give every scene a **distinct
   composition**. Reusing one layout (or one template) beat after beat with only
   the text swapped is the #1 way a video reads as a flat, templated slideshow —
   and it is fatal for a from-scratch / promo video where the graphics ARE the
   video (see [`reference/promo-and-mg-videos.md`](reference/promo-and-mg-videos.md)).
   The ONLY repetition that belongs is a recurring *functional overlay* on real
   footage — e.g. the same lower-third name-plate style each time a person is
   introduced — which is a consistent repeated ELEMENT, not a repeated SCENE.
   (This replaces the earlier "repetition is good, reuse freely" guidance, which
   produced templated, monotonous output.)
4. **The ONE hard line: never misuse a purpose-specific template.** A few
   templates *mean* something — use them only when the content matches:
   `stat-reveal` → a real number (never a generic title) · `comparison` →
   exactly two things contrasted · `flowchart` → an actual sequence of steps ·
   `key-takeaways` → a list of points · `yt-lower-third` → introducing a
   person/channel. Everything else (the title family, `split-panel`, the
   parallax reveals) is **generic** — usable on any beat — but still vary the
   composition beat to beat; don't lean on one look for the whole video (Rule §3).
5. **Camera-only / imported footage → lead with a PREMIUM designed segment.**
   When the clip's `kind` is `"camera"` (talking-head) or `"upload"` (imported),
   there's no screen to zoom into, so a static frame is what makes it look flat.
   A designed segment (host one half, a panel the other, via
   `project.add-designed-segment`) is the highest-leverage fix and your
   **default workhorse** for explainer beats on this footage. **Default to
   `paper-panel` or `vox-side-panel`** — those are the featured, high-production
   panels that instantly level a video up. Use `split-panel` only as a plainer
   fallback or for variety, NOT as the go-to. Use the panels liberally (alternate
   side + content). For `kind === "screen"`, prefer cursor-telemetry zooms;
   don't split the frame.
6. **Reach for the FEATURED (premium) templates first.** Six templates are
   flagged top-tier in `motion_list` (`featured: true`) — they're the most
   produced looks we ship, and on an "engaging / cinematic / level it up" brief
   you should prefer them over the plainer templates (`split-panel`, the basic
   title cards):
   - **Strong workhorses:** `paper-panel`, `vox-side-panel` (side panels) and
     `vox-marker` (the highlighter headline reveal) — reach for these on
     explainer beats over real footage, but vary the side, content, and which
     one you use; don't repeat a single panel across the whole video (Rule §3).
   - **Reach for the moment the content gives you the hook:** `vox-stat` (a real
     number / metric), `vox-quote` (a quote or testimonial), `vox-annotation`
     (circle/callout a specific subject word).
   Don't force a purpose template where the content doesn't fit — Rule §4 still
   holds; a stat card with no number looks worse, not better. But when the hook
   IS there, take it: these elevate the video far more than a generic title card.
7. **Text isn't your only option.** When a beat wants a *visual* — logos for the
   tools being named, a product screenshot, an animated diagram — author a
   custom graphic (see "Authored graphics" below). Don't force every beat into a
   text template.

### Selection guide (beat → template)

"Class" tells you when a template fits: **Generic** = usable on any beat ·
**Purpose** = only when the content matches · **Semi-generic** = usable, has a
natural fit. **Across a video, vary your compositions — don't repeat one look
(Rule §3).** "Generic" means it has no content prerequisite, NOT "repeat it
every scene."

| What's happening in the video | Reach for | Class |
|---|---|---|
| Open / chapter / section title | `creator-card`, `transitions-3d`, `grain-overlay`, `transitions-destruction`, `caption-parallax-layers` — vary the look across sections | **Generic** |
| Explainer beat, host on camera/imported footage | **`paper-panel`** (torn-paper sheet + two-line title) or **`vox-side-panel`** (graph-paper/specimen look) — the premium designed segments that level the video up. `split-panel` (clean brand panel + bullets) is the plainer fallback. Alternate side, content, and panel across beats. | **Generic workhorse** |
| Hero reveal / intro / "ways to use it" recap | `parallax-zoom`, `parallax-unzoom` | Semi-generic |
| Introduce a person / channel / "subscribe" | `yt-lower-third` | Purpose |
| A real number / metric / result | `stat-reveal` | **Purpose — numbers only** |
| "Here are the N things…" / key points / recap | `key-takeaways` | Purpose |
| This vs that / before vs after / old vs new | `comparison` | Purpose |
| A simple linear process / N steps | `flowchart` | Purpose |
| **How something WORKS / connects / flows** — architecture, pipeline, request lifecycle, hierarchy, branching, a loop (richer than a flat step list) | **Author a custom animated diagram** — see "Authored graphics" below | Authored — the explainer workhorse |
| A trend / chart / data viz (bars, a line, a metric building over time) | **Author a custom chart** — see "Authored graphics" | Authored |
| Talking-head OPENER — name the topic in the first 10–30s (default on every camera edit) | `caption-editorial-emphasis` | **Default for `kind === "camera"`** |
| ONE thesis sentence / pull-quote / "money line" (hook or climax) | `caption-editorial-emphasis` | **Purpose — at most 2–3 per video** |
| Logos / tools / partners · a screenshot (a VISUAL, not text) | **Author a custom graphic** — see "Authored graphics" below | Authored (not a UI template) |

### Authored graphics — your repertoire is bigger than the gallery

The 13 templates above are the **UI gallery**: fixed-structure, slot-fill. But
your repertoire is larger — you can also **author content-specific graphics**
that *can't* be slot-templated because what they show depends on what's being
discussed. **This is a first-class capability, not a last resort** — when a beat
needs a *visual* that no template captures, authoring one is the right move, not
a fallback you apologize for. Build these as transparent overlays with
`motion.render-html`; they composite over the host exactly like an overlay
template.

**Explainer videos are the prime case.** The moment the speaker explains *how
something works, connects, or flows* — an architecture, a pipeline, a request
lifecycle, a hierarchy, a before→after, a trend over time — a custom **animated
diagram, flowchart, or chart** communicates it far better than a bullet list or
a title card. The built-in `flowchart` template handles a simple linear sequence
of steps; **anything richer you author yourself.** Don't flatten a real
explanation into text because the gallery has no template for it — draw it.

- **Animated diagram / flowchart** — a data-driven SVG that builds as the
  speaker talks: boxes + connecting arrows that draw on in sequence, a
  branching tree, a request flowing through services, a layered architecture
  stack, a cyclic loop. For ANY "here's how it works / how the pieces fit"
  explainer beat that's more than a flat list of steps. Reveal each node/edge in
  time with the narration so the diagram assembles, not just appears.
- **Chart / data viz** — bars growing, a line plotting, a metric counting, a
  donut filling — when the point is a trend or a structural comparison, not a
  single headline number (use `stat-reveal`/`vox-stat` for one number).
- **Logo / brand-card row** — N rounded white cards, each a logo, popped in over
  the lower third. For "we use X, Y, Z", tool / partner / integration mentions
  (e.g. HeyGen · Claude Code · Hyperframes).
- **Image / screenshot showcase** — real images via `--assets` (product shots,
  UI grabs) in a framed or tilted card.
- **Icon / emoji concept callout** — a glyph + short label punched on a concept.
- **Reuse a template's shell, swap text → graphics** — take the *look* of an
  overlay template (the lower-band card, the side panel, the depth stack) and
  put logos / images / animated SVG / a diagram where the text would go.

These never appear in the UI gallery (they're not in the manifest) — they're
yours to consider whenever a slot-fill template doesn't capture the beat.
Copy-able recipes (logo-card row, etc.) live in
[`reference/examples.md`](reference/examples.md); the authoring contract (page
shell, deterministic seek, transparent overlays) is in
[`reference/motion-philosophy.md`](reference/motion-philosophy.md).

### The workflow

```bash
# 1. ALWAYS discover first — templates + editable slots (runtime source of truth).
pandastudio motion.list --json          # MCP: motion_list

# 2. Pick the template that fits THIS beat (see the selection guide), then
#    render it with your own text/colors + a background mode.
#    Replace <TEMPLATE_ID> + slots with the chosen template's — do NOT
#    hardcode one template for every insert.
JOB=$(pandastudio motion.generate \
  --templateId=<TEMPLATE_ID> \
  --slots='{ ...the chosen template's slots from motion.list... }' \
  --aspectRatio=16:9 \
  --json | jq -r '.data.jobId')          # MCP: motion_generate
pandastudio job.wait --id="$JOB" --json

# 3. Add the rendered clip to the timeline (at the playhead by default).
pandastudio project.add-motion-graphic --id="$PROJECT" --fromJob="$JOB" --durationMs=4000
```

- **Editable everything** — every template's text, colors, list items, and
  images are `slots`; pass only the ones you want to change, the rest use
  defaults. `motion.list` returns each template's slot keys, types (`string` /
  `color` / `list` / `image`), and defaults.
- **Image slots** — a slot of type `image` takes an **absolute file path** to an
  image; the renderer stages the file into the render. Pass a project-media path
  or a generated image (e.g. from `media.generate-image`). Two templates take an
  image: **`image-showcase`** (the dedicated one — a screenshot/photo on a
  3D-tilted card; the go-to for highlighting a product page or app screen in a
  demo, 16:9 + 9:16) and `vox-side-panel` (a small photo in its specimen card).
  Example: `--slots='{"image":"/abs/screenshot.png","headline":"Ship faster.","eyebrow":"SEE IT IN ACTION"}'`
  on `image-showcase`.
- **`--fromJob` not `--file`** — pass the render `jobId` to the add tool; it
  resolves the path internally (hand-built paths truncate at the space in
  "Application Support" and silently fail).
- **Placement** — `add-motion-graphic` drops it at the playhead/end as an
  overlay. To re-time, pass `atMs`. Anchor to a transcript word with
  `anchorSourceMs` so it survives later transcript edits.
- **Default SFX** — every primitive that places an animated callout on the
  timeline now attaches a stinger by default so the agent's output sounds
  the way a hand-edited timeline does. Don't pass `soundUrl` to "set the
  default" — omit it. Override only when the user asks for a different
  sound, or pass `null` (MCP) to make the callout silent.

  | Verb | Default | Notes |
  |---|---|---|
  | `project.add-motion-graphic` | `bundled:sound/mouse-click` | New in v1.36.0; previously silent. Applies to every motion graphic — generated templates, custom MP4/WebM, designed-segment panels. |
  | `project.add-designed-segment` | `bundled:sound/mouse-click` | Inherits from add-motion-graphic. |
  | `project.add-zoom` | `bundled:sound/swoosh-fast` | Pre-existing. |
  | `project.add-lower-third` | `bundled:sound/mouse-click` | v2.96.0 — inherits the motion-graphic default. |
  | `project.add-fx` | none | FX overlays often have their own audio; left to the caller. |

  Use `asset.list-sounds` to discover other bundled sound ids when swapping.

### Background modes, designed segments, and the template catalog

`--background` modes, the host-on-one-half designed-segment pattern, and the full bundled-template catalog (incl. podcast layouts). Full detail: [`reference/motion-templates.md`](reference/motion-templates.md).
## Custom motion graphics — HTML authoring

When no template fits, author HTML against the HyperFrames contract. Render verbs (`motion.screenshot`/`render-html`/`concat`), transparent overlays + frosted glass, add-by-jobId. Read [`reference/motion-philosophy.md`](reference/motion-philosophy.md) + [`reference/motion-recipes.md`](reference/motion-recipes.md) before authoring; verbs in [`reference/custom-html.md`](reference/custom-html.md).
## Effects (FX) & transitions

**Golden rule: restraint.** Scene transitions (`project.add-transition`) and FX overlays (`project.add-fx`). Full detail: [`reference/fx-transitions.md`](reference/fx-transitions.md).
## Narration (voiceover) + B-roll generation

Replicate TTS narration and gpt-image B-roll (always Ken-Burns + vignette a still, never drop a flat photo). Requires the user's Replicate key. Full detail: [`reference/media-generation.md`](reference/media-generation.md).
## Transcript-based editing — PandaStudio's signature feature

The reason humans pick PandaStudio over Premiere is that you edit by **deleting words from the transcript**, not by scrubbing the timeline. The CLI exposes the same model.

### The full edit loop

```bash
# 0. Check which clips still need processing (avoids clobbering in-app edits)
STATE=$(pandastudio project.read --id=$ID --json | jq '.data.clipStates')
# clipStates: [{ clipId, transcribed, wordCount, audioCleaned }, ...]

# 1. Transcribe only clips that don't already have a transcript
#    (if all are transcribed, skip this step entirely)
JOB=$(pandastudio transcript.transcribe --id=$ID --json | jq -r '.data.jobId')
pandastudio job.wait --id=$JOB --timeoutMs=300000 --json

# 2. Pull the merged transcript — every word with edited-time start/end
pandastudio transcript.get --id=$ID --json | jq '.data.words[0:20]'

# 3a. AUTO: drop every "um" / "uh" / "you know" + immediate repeats
pandastudio transcript.remove-fillers --id=$ID --json
# → returns { removedCount, fillersRemoved, repeatsRemoved, trimsAdded }

# 3b. Remove silences (default ≥500ms = the UI button; covers leading/trailing/between-word)
#     Omit --thresholdMs to use the 500ms default; only pass it to override.
pandastudio transcript.remove-silences --id=$ID --json
# → returns { removedCount, totalTrimmedMs }

# 3c. Fix STT errors — NEVER use project.read → JSON mutation → project.save for this.
#     find-replace patches the word text in-place and preserves timing.
pandastudio transcript.find-replace --id=$ID --find="RightPanda" --replace="WritePanda" --json
# → returns { replacedCount, wordsPatched }
#  Matcher caveats:
#  - Matching is case-insensitive; punctuation is ignored on both sides
#    (`--find="graph, crew"` matches "graph crew").
#  - DIGITS are significant when the find phrase contains them:
#    `--find="try30"` matches only the merged STT token "try30", never a plain
#    "try". A letters-only find still ignores transcript-side digits
#    (`--find="than"` also matches "than60").
#  - A multi-word find ALSO matches a single merged STT token: `--find="Wispr
#    Flow"` hits the one token "Wispr Flow" (STT often emits multi-word brand
#    names as one token), and `--find="of $499"` hits the merged "of$499".
#  - A find that exactly equals a token's raw text always matches, so
#    space/digit/punctuation-bearing tokens — even pure numbers like "30%" —
#    are all targetable verbatim.
#  - A multi-word `--find` collapses to the FIRST word's slot: that word's text
#    becomes `--replace`, the other matched words are blanked. The replacement is
#    the literal `--replace` string, so include any punctuation you want kept
#    (the original word's trailing comma/period is not auto-preserved).

# 3d. SURGICAL: delete specific words by ID
pandastudio transcript.delete-words --id=$ID --wordIds='["clip-1:w-42","clip-1:w-43"]' --json

# 3e. PHRASE search → bulk delete
WORDS=$(pandastudio transcript.search --id=$ID --query="this is a test" --json \
  | jq -c '[.data.matches[].wordIds | .[]]')
pandastudio transcript.delete-words --id=$ID --wordIds="$WORDS" --json

# 3f. RESTORE previously deleted words (undo a delete / filler / repeat removal).
#     Removes the trim region(s) covering those words; silence trims are left
#     untouched. Mirrors the editor's right-click → Restore on struck-through words.
pandastudio transcript.restore-words --id=$ID --wordIds='["clip-1:w-42","clip-1:w-43"]' --json
```

Every deletion translates internally into a **trim region** the export pipeline skips. It's identical to clicking the word in the editor's transcript pane and hitting delete.

**`transcript.get` shows ALL words, including ones you've deleted.** Deleted words become trim regions — they're gone from the audio export — but they still appear in the raw word list. If you need to verify a deletion happened, check `trimsAdded` in the response rather than calling `transcript.get` afterwards and looking for missing words.

**STT coherence with motion graphics**: Fix all transcript errors with `transcript.find-replace` BEFORE calling `motion.generate` or `llm.generate-title`. The local LLM and motion-graphic slot values are derived from the transcript text — a "RightPanda" in the transcript will propagate into the title card if you generate it first.

### Audio cleanup, background audio, music, and color grading

`audio.clean` (DeepFilter), background-audio regions, bundled + Lyria-generated music, and LUT color presets. Full detail: [`reference/audio-color-music.md`](reference/audio-color-music.md).
## Visual edits — zooms, trims, speed, crop, layouts

Zoom (incl. follow-cursor + `--anchorSourceMs`), cut/speed, crop/reframe, face centering, webcam + per-section podcast layouts, speaker-driven editing, export defaults. Full detail: [`reference/visual-edits.md`](reference/visual-edits.md).
## Captions, AI metadata, thumbnails

Caption toggle/style/font, AI title/description/timestamps (local LLM), and YouTube thumbnail generation. Full detail: [`reference/captions-metadata.md`](reference/captions-metadata.md).
## Export — produce the final MP4

The centerpiece. Routes through the same Tier-3 PixiJS renderer the editor's Export Video button uses (v1.24+ — was a separate Skia native pipeline before that, see release notes for the convergence). When an editor window is already open on the project you're exporting, the agent reuses it. Otherwise the agent spawns a hidden editor window for the duration of the render and closes it after. **Async; poll `job.wait`.**

```bash
JOB=$(pandastudio export.start --id=$ID --quality=high --json \
  | jq -r '.data.jobId')

# Watch progress (server-side block; returns when done or 5min timeout)
pandastudio job.wait --id=$JOB --timeoutMs=600000 --json | jq '.data.job'
# → status: "succeeded", result: { outputPath, durationMs, width, height, frameRate }
```

Quality presets: `draft` (1280×720), `standard` / `high` (1920×1080), `ultra` (3840×2160). Aspect ratio comes from the project (`set-aspect-ratio`). Output lands in the recordings dir by default; pass `--outputPath=/somewhere/file.mp4` to override.

The export honours **everything** in the project: clips, trims (incl. those from transcript word deletes), speed regions, zooms, captions, FX, lower-thirds with sound, motion graphics, annotations, cleaned audio, wallpaper, padding/shadow/radius/blur. One verb, full pipeline.

**Video overlays (motion graphics) are fully composited in the export** — both opaque MP4 (`motion.generate`, `motion.render-html`) and transparent WebM (`motion.render-html --transparent`) are composited inline by the Tier-3 pipeline. Alpha channels from VP9/WebM sources are preserved exactly. There is nothing extra you need to call — `export.start` handles it automatically once overlays are on the timeline via `project.add-motion-graphic`.

## Video editing playbook — end-to-end recipe (per destination)

When the user says *"edit this"* / *"polish this"* / *"make this ready for <X>"* / *"YouTube-ready"*, follow this runbook. It turns a raw recording into a polished, destination-appropriate video using the foundational verbs above. Different destinations (YouTube long-form, Shorts/TikTok, LinkedIn, Loom) need different defaults — the table below is the source of truth.

**Philosophy:** good video editing is a series of pattern interrupts that match the platform's viewing context. A YouTube long-form viewer has settled in — cuts every 5–8s and a cinematic LUT feel right. A TikTok viewer is scrolling — you have 3 seconds to hook them and every second after needs a visible change. A LinkedIn viewer is at work — an aggressive soundscape is wrong. A Loom viewer doesn't want any editing at all beyond "cut the fluff". Same tools, very different dials.

### Destination profiles (the source of truth)

Resolve the destination first (see [HARD-GATE](#editorial-decisions--what-to-ask-what-to-assume-what-never-to-ask) step 1). Then apply every default below from the matching row — don't mix.

| Parameter | `youtube-long` | `shorts` (Shorts/TikTok/Reels) | `linkedin` | `loom` (internal/async) |
|---|---|---|---|---|
| Aspect | 16:9 | **9:16** | 16:9 or 1:1 | 16:9 |
| Hook deadline | 10 s | **3 s** | 10 s | — (none) |
| Intro / outro card | **only if the user asks** (then 2–4 s) | **only if the user asks** | **only if the user asks** (then 2–3 s) | none |
| Lower thirds | yes, at first mentions | **no** (too small vertically) | yes | no |
| Zoom cadence | 3–6 / min | **6–12 / min** | 1–2 / min | 0–1 / min |
| Default emphasis zoom duration | **7 s** | 3 s | 4 s | 2 s |
| Sustained held-zoom duration (section reframe) | **15 s** | — | 8 s | — |
| Agent zooms on screen-share clips | **NEVER** (telemetry handles it) | **NEVER** | **NEVER** | **NEVER** |
| Zoom SFX volume | 1.0 (swoosh-fast) | **1.0 (swoosh-fast)** | 0.5 (or `none`) | `none` |
| Filler/silence removal | yes | yes | yes | **yes (aggressive — minSilenceMs 300)** |
| Speed regions (B-roll) | 1.5–2× | **2–3×** or cut entirely | 1.25–1.5× | none |
| LUT preset | by content type @ 0.5–0.8 | **`modernVibrant` @ 1.0** | `naturalEnhanced` @ 0.3 | none |
| Background music | **only if the user asks** (then vol 0.15) | **only if the user asks** (then vol 0.30) | none | none |
| Captions enabled | **no burn-in** — keyword pops instead (measured: 0/9 studied long-form videos burn speech captions; see longform-styles.md LF4) | **yes (required)** | yes | optional |
| Caption template | — (keyword-pop overlays, not caption templates; if the user INSISTS on captions: `minimal`) | **`neon`** + positionY 0.65 | `minimal` | `minimal` (if any) |
| Export quality | `high` | `high` | `high` | `standard` (faster) |

**LUT by content type** (only for `youtube-long` — other profiles use their fixed preset above):

| Content type | Preset | Intensity |
|---|---|---|
| Tech tutorial / SaaS demo | `modernVibrant` | 0.7 |
| Cinematic vlog | `cinematicTealOrange` | 0.9 |
| Educational / neutral | `naturalEnhanced` | 0.5 |
| Moody storytelling | `moodyDark` | 0.7 |
| Travel / lifestyle | `warmSunset` | 0.7 |

### Creator-style overrides (when the user names a style)

When the user says *"like Ali Abdaal's videos"* / *"MKBHD style"* /
*"MrBeast-style"* / etc., start from the matching base profile, then
apply the overrides below. These are on top of the profile defaults,
not instead of them. Unlisted styles → fall back to base profile.

| Style | Base profile | Pacing | LUT | Music | Caption template | Motion-graphic cadence + notes |
|---|---|---|---|---|---|---|
| **Ali Abdaal** (productivity / book reviews / tutorial long-form) | `youtube-long` | 1 visual change every **3–5s**; aggressive filler + silence removal | `modernVibrant` @ 0.5 | warm ambient / lofi @ 0.15–0.20 | `bold`, positionY 0.85 (below lower-third zone) | Intro title card (3s held) · host lower-third at 0:04–0:09 · 3–4 right-rail concept callouts at emphasis claims · 1 stat-reveal full-frame takeover if the video cites a number · outro card 4–6s hold with "Like & Subscribe" + shimmer on handle |
| **MKBHD** (tech reviews / product-focused long-form) | `youtube-long` | 1 change every **4–6s** — contemplative, product breathes on screen | `modernVibrant` @ 0.6 OR `cinematicTealOrange` @ 0.5 | upbeat tech-review bed @ 0.20 | `minimal` @ positionY 0.82 | Clean intro wordmark (2s) · minimal lower-thirds (1 total, on first product mention) · stat-reveals over product shots use chrome-gradient numbers on dark · outro: product recap card + subscribe |
| **MrBeast** (stunts / challenges / max-retention) | `youtube-long` | 1 change every **2–3s** — very fast, shorts-like cadence | `warmSunset` @ 0.8 (saturated, warm) | dramatic orchestral bed @ 0.30 | `neon`, **huge** (fontSize ~4.5rem, near the 5.0rem max), color-coded by topic, positionY 0.8 | Big chrome-gradient kinetic-type every ~5s · frequent full-frame stat takeovers with counter tweens · countdown overlays if the video has stakes · outro: "what's next" teaser card, **hold full 6s** |
| **Veritasium / Kurzgesagt-live** (science / education long-form) | `youtube-long` | 1 change every **5–7s** — contemplative, give diagrams time to read | `naturalEnhanced` @ 0.4 | ambient / orchestral @ 0.12 | `minimal` @ positionY 0.85 | Explanatory diagrams as motion graphics (labeled SVGs with `power2.inOut` reveals, `stagger: 0.15` on labels) · chapter dividers with chrome-gradient section titles · one or two hero stat-reveals with counter tweens · outro: citations card + subscribe |
| **Vox / Johnny Harris** (explainer / essay long-form) | `youtube-long` | 1 change every **4–6s** — narrative-driven | `cinematicTealOrange` @ 0.7 | cinematic bed @ 0.18 | `minimal` @ positionY 0.85 | Chapter cards at every act break (bold chrome-gradient section titles) · map / timeline / chart motion graphics · pull-quote callouts in right rail · outro: credits card + next video teaser |

**Rule:** an agent authoring any "style X" edit MUST still follow the 11
Laws from `reference/motion-philosophy.md`. The style overrides change
palette, cadence, and the *suggested* music/intro/outro — they do NOT let
you ship flat-white text on a flat-black background. Grid + vignette + grain
+ chrome gradient are mandatory regardless of named style.

**Music + intro/outro stay opt-in even in style mode.** The Music and
motion-graphic-cadence columns above describe what the style *would* include
— but background music and intro/outro cards are still added ONLY when the
user asked for them (see the default edit pipeline). If the user named a style
without mentioning music or an intro/outro, apply the style's palette /
pacing / captions / mid-roll motion graphics, and *offer* the music bed +
intro/outro rather than adding them unprompted.

### Anchoring — every transcript-derived region MUST be anchored

This rule applies to FIVE region types: zoom, motion-graphic, lower-third,
annotation, and audio-overlay (when used as SFX, not background music).

**The problem.** Region positions are stored in **edited time** —
post-trim playback time. When the user (or you) runs `transcript.remove-fillers`,
`transcript.remove-silences`, `transcript.delete-words`, or `transcript.find-replace`,
new trim regions get added, the edited-time map shifts, and any region whose
`startMs`/`endMs` was authored against the previous edited time **drifts off
the moment it was placed on**. A "Like and Subscribe" lower third you placed
on the word "subscribe" silently moves 800ms early because there used to be
800ms of "um"s before it that got trimmed.

**The fix is the `--anchorSourceMs` argument.** When you derive `atMs` /
`startMs` from a transcript word's source time, pass that same value as
`--anchorSourceMs`. The region records its anchor moment in raw recording
time. Every subsequent trim/speed edit auto-rebases the region's edited
positions back onto the anchor — the lower third stays glued to "subscribe"
no matter how much you trim.

> **v1.35.0+: every region is auto-anchored on creation, even without `--anchorSourceMs`.**
> The primitive now back-computes a source-time anchor from the resolved
> edited `atMs` (via `editedToSource`) whenever the caller doesn't supply
> one explicitly. Regions placed by direct atMs survive subsequent silence
> removal, filler removal, and word deletion just like transcript-anchored
> ones. **Still pass `--anchorSourceMs` when you have a transcript word in
> hand** — it makes the agent's intent self-documenting and avoids a
> two-step round trip through edited time. But the days of "I placed an
> overlay, then trimmed silences, now it's playing at the wrong moment"
> are over for any project saved by v1.35.0 or later. Legacy projects
> (schemaVersion < 4) are auto-migrated on the first mutation: every
> anchorless region gets a source anchor back-filled at its current
> position. `type: "free"` anchors are preserved as opt-outs.

**Verbs that accept anchors (use them ALWAYS when picking from transcript):**

| Verb | Anchor args | When required |
|---|---|---|
| `project.add-zoom` | `--anchorSourceMs`, `--anchorSourceEndMs` | Always when atMs comes from a transcript word |
| `project.add-motion-graphic` | `--anchorSourceMs`, `--anchorSourceEndMs` | Always when atMs comes from a transcript word |
| `project.add-lower-third` | `--anchorSourceMs`, `--anchorSourceEndMs` | Always when atMs comes from a transcript word |
| `project.add-annotation` | `--anchorSourceMs`, `--anchorSourceEndMs` | Always when startMs comes from a transcript word |
| `project.add-audio` | `--anchorSourceMs`, `--anchorSourceEndMs` | When the overlay is an SFX pinned to a word. **NEVER for background music** — those should stay free-floating (a fixed slot of the edited timeline, not anchored to content). |

**Free-floating is OK** — when the user explicitly placed a region by edited
time (e.g. an outro card at "the last 5 seconds of the timeline"), omit the
anchor. The region stays where you put it regardless of subsequent edits.

**anchorSourceMs is global source-time (ms from recording start).** In
multi-clip projects, sum the preceding clips' `sourceDurationMs` to convert
an in-clip offset to global source time before passing as `--anchorSourceMs`.
Use `timeline.source-to-edited` to verify where a source-time position falls
on the edited timeline.

**The runbook below already orders pacing FIRST, then regions.** That's safe
even without anchors — regions land on the post-trim timeline. But: any
mid-flow re-edit ("actually, remove the part about X" after you've placed
motion graphics) drifts unanchored regions silently. Always anchor when the
position came from a transcript word, even if the runbook order is followed.
The cost is one extra arg per call; the benefit is correctness under iteration.

### The runbook (ordered — do not rearrange)

```bash
# 0. Resolve the project + destination profile
ID=$(pandastudio project.current --json | jq -r '.data.project.id // empty')
[ -z "$ID" ] && ID=$(pandastudio project.list --json | jq -r '.data.projects[0].id')

# $PROFILE is set from HARD-GATE step 1: youtube-long | shorts | linkedin | loom
# $ASPECT is derived from the profile:
#   youtube-long | linkedin | loom → 16:9
#   shorts                         → 9:16
pandastudio project.set-aspect-ratio --id=$ID --aspect=$ASPECT

# 1. PACING — the default cleanup pipeline (see "default edit pipeline" in
#    Editorial decisions for the mandatory steps + report-counts rule). Run it
#    in full — none of these is optional. audio.clean fires async; wait on it
#    before export (step 5). First read pulls the transcript (needed for step 2);
#    later reads pass --includeTranscript=false.
pandastudio project.read --id=$ID --json
pandastudio transcript.transcribe --id=$ID               # skip if transcribed
AUDIO_CLEAN_JOB=$(pandastudio audio.clean --id=$ID --json | jq -r '.data.jobId // empty')  # async
pandastudio transcript.remove-fillers --id=$ID           # fillers + immediate repeats
# Bad takes + repeated phrases: find-issues is READ-ONLY — you MUST then delete
# the discarded wordIds (keep the most recent take). Skipping the delete cuts nothing.
ISSUES=$(pandastudio transcript.find-issues --id=$ID --json | jq -c '.data.issues')
DROP=$(echo "$ISSUES" | jq -c '[.[] | select(.type=="duplicate-take" or .type=="adjacent-repeat") | .wordIds[]]')
[ "$DROP" != "[]" ] && pandastudio transcript.delete-words --id=$ID --wordIds="$DROP"
SILENCE_MS=$([ "$PROFILE" = "loom" ] && echo 300 || echo 500)
pandastudio transcript.remove-silences --id=$ID --thresholdMs=$SILENCE_MS   # NEVER skip; arg is thresholdMs (500ms = UI default)

# 2. EMPHASIS — zooms (skip for `loom`). Cadence comes from the profile table.
#
#    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    HARD RULE #1 — DO NOT add zooms to screen-share clips.
#    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PandaStudio auto-adds zooms to screen-share clips based on cursor
#    telemetry captured during recording. Adding more on top = stacked
#    zooms on the same moments, visual chaos.
#
#    For each clip returned by project.read:
#      - If clip.webcamPath is present  → "both" mode (screen + PiP
#        webcam). Telemetry zooms ALREADY exist on this clip. **SKIP.**
#      - If the clip is pure camera (no webcamPath AND mediaPath is a
#        camera recording) → safe to add zooms on emphasis.
#      - If screen-only (no webcamPath, mediaPath is screen) → telemetry
#        still exists, zooms are auto-added. **SKIP.**
#
#    Heuristic: if project.read returns existing zoomRegions for a clip
#    whose webcamPath is set, those are telemetry-based — stay OUT of
#    that clip's zoom space entirely. Only author zooms on pure-camera
#    clips (webcamPath absent, no pre-existing zoom regions).
#
#    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    HARD RULE #2 — Zoom duration floor is 6 seconds, NOT 1.5–3 seconds.
#    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    Premium YouTube zooms ride through a complete thought or cut. A 1.5s
#    or 3s zoom reads as a twitch. Defaults:
#      - Emphasis punch-in zoom (camera pulls in on a word/claim):
#        durationMs=6000 to 8000  (was 1500 — that was wrong)
#      - Sustained / held zoom (camera pulls in on a subject and
#        stays for the whole sub-topic):
#        durationMs=10000 to 20000
#      - Reveal moment (dramatic, loud SFX): durationMs=6000 minimum
#    Depth 3 (modest) for talking-head emphasis; depth 5 only for
#    dramatic reveal beats. Don't stack multiple zooms inside 5s of each
#    other — leaves no time to settle.
#
#    Shot selection: scan the transcript for punchy claims, specific
#    numbers, opinionated statements ("the best", "this changed
#    everything", "most people don't know"), moments of pivot ("and
#    now", "finally", "but here's the thing"). Aim for the user's
#    eyes to want to lean in. NOT every UI-verb word ("click", "select")
#    — that was the old rule, it's wrong for engagement-style edits.
#
#    CRITICAL: ALWAYS pass --anchorSourceMs when atMs comes from a transcript
#    word. Without it, the zoom drifts off the moment as soon as ANY trim is
#    added — and step 1 always adds trims (remove-fillers, remove-silences).
#    The anchor binds the zoom to the source recording moment so it
#    re-anchors automatically on every trim/speed change.

# Emphasis punch-in — modest scale, held through the thought
pandastudio project.add-zoom --id=$ID --clipId=$CLIP_ID \
  --atMs=<wordStartMs> --anchorSourceMs=<wordStartMs> \
  --durationMs=7000 --depth=3

# Sustained held zoom — reframe on a topic and stay for the full section
pandastudio project.add-zoom --id=$ID --clipId=$CLIP_ID \
  --atMs=<sectionStartMs> --anchorSourceMs=<sectionStartMs> \
  --durationMs=15000 --depth=3

# Reveal moment (dramatic, with SFX). Use SPARINGLY — 1-2 per video max.
pandastudio project.add-zoom --id=$ID --clipId=$CLIP_ID \
  --atMs=<ms> --anchorSourceMs=<ms> \
  --durationMs=6000 --depth=5 \
  --soundUrl=bundled:sound/dramatic-whoosh --soundVolume=0.7

# 3. POLISH — skip sections by profile:
#    - `shorts`: no lower thirds (tight vertical frame)
#    - `loom`:   skip 3b, 3c entirely
#    NOTE: 3a (intro/outro) and 3d (background music) are OPT-IN — run them
#    ONLY when the user explicitly asked for an intro/outro or music. They are
#    NOT part of the default "edit my video" pass for ANY profile.

# 3a. Intro / outro card — ONLY IF THE USER EXPLICITLY ASKED for one
# ("add an intro", "add an outro card", "open with a title"). Do NOT add
# one on a plain "edit this" request. When asked: fastest is the
# `creator-card` template via motion.generate; author custom HTML
# (reference/motion-philosophy.md §7) only for a bespoke intro.
if [ "$USER_ASKED_FOR_INTRO" = "1" ]; then
  JOB=$(pandastudio motion.render-html \
    --htmlPath=/tmp/intro-title.html \
    --durationMs=3000 --json | jq -r '.data.jobId')
  FILE=$(pandastudio job.wait --id=$JOB --json | jq -r '.data.job.result.outputPath')
  pandastudio project.add-motion-graphic --id=$ID --file=$FILE --durationMs=3000 --atMs=0
fi

# 3b. Lower third at first mention of a person/product (NOT shorts/loom)
#     One call renders the lt-* nameplate AND places it (async job).
if [ "$PROFILE" = "youtube-long" ] || [ "$PROFILE" = "linkedin" ]; then
  JOB=$(pandastudio project.add-lower-third --id=$ID \
    --name="<name>" --title="<role>" --atMs=<ms> --anchorSourceMs=<ms> \
    --json | jq -r '.data.jobId')
  pandastudio job.wait --id=$JOB
fi

# 3c. LUT (use the profile table. For youtube-long, use content-type sub-table.)
#     Apply to every clip via project.set-clip-lut.
#     Skip entirely for `loom`.

# 3d. Background music — ONLY IF THE USER EXPLICITLY ASKED for music
# ("add background music", "put a track under it"). Do NOT add music on a
# plain "edit this" request. When asked, use the profile volume (youtube-long
# 0.15, shorts 0.30) and let the user pick / swap the track.
if [ "$USER_ASKED_FOR_MUSIC" = "1" ]; then
  VOL=$([ "$PROFILE" = "shorts" ] && echo 0.30 || echo 0.15)
  pandastudio project.add-audio --id=$ID \
    --path=bundled:music/corporate-underscore --volume=$VOL --fadeIn=1000 --fadeOut=2000
fi

# 4. ACCESSIBILITY — captions per profile
if [ "$PROFILE" != "loom" ]; then
  pandastudio caption.toggle --id=$ID --enabled=true
  TEMPLATE=$(case "$PROFILE" in
    shorts)       echo "neon";;
    linkedin)     echo "minimal";;
    youtube-long) echo "bold";;
  esac)
  pandastudio caption.set-template --id=$ID --templateId=$TEMPLATE
fi

# 4.5. VERIFY FRAMES — MANDATORY. Never export without looking.
# Run motion.verify-frames on every rendered motion-graphic MP4 AND on
# a draft pass of the full composition (preview.show, then extract
# frames at hero timestamps). READ each PNG as a multimodal image and
# confirm against the motion-philosophy §4 pre-flight checklist:
# - no cropped faces / text overflow / blank frames
# - captions on the right word
# - no MG covers host face (Mode C) or screen zone (Mode B)
# - chrome-gradient text is actually rendering (not flat white)
# - grid + vignette + grain visible on every hero beat
# If any frame fails, iterate and re-verify. Do NOT skip this step
# even when "it's just a quick edit" — this is what separates
# ships-it-works-ish from ships-it-looks-good.
pandastudio preview.show --id=$ID   # let the project render a full draft
# Then verify each generated motion-graphic MP4 at its hero timestamps:
# pandastudio motion.verify-frames --videoPath=/tmp/motion-intro.mp4 \
#   --timestamps='[0.3,1.0,1.8,2.7]' --json
# Read every returned frame. If any fail, fix + re-render + re-verify.

# 5. EXPORT — quality per profile. Only run AFTER verify-frames passes.
# First: block on the audio.clean job that's been running in the
# background since step 1. By now it's almost certainly done (30-60s
# vs the ~90s+ the rest of the work took), so this resolves instantly.
[ -n "$AUDIO_CLEAN_JOB" ] && pandastudio job.wait --id="$AUDIO_CLEAN_JOB"
QUALITY=$([ "$PROFILE" = "loom" ] && echo "standard" || echo "high")
pandastudio export.start --id=$ID --quality=$QUALITY --json | jq -r '.data.jobId' | \
  xargs -I {} pandastudio job.wait --id={}
```

### Performance — keep wall-clock minimal

Motion-graphic renders dominate (each scene ~20–45s); everything else is
rounding error. The levers:
- **`motion.render-html` renders are SERIAL — fire ONE, `job.wait` it, then the
  next.** A single-render mutex serializes them; a second concurrent render
  returns `{ ok:false, error:"RENDER_BUSY" }` (parallel renders share GPU /
  scratch / headless-shell state and wedge). Do NOT fire all renders at once.
- **Run `audio.clean` in the background** (capture its jobId right after
  transcribe; `job.wait` only before `export.start`). This IS safe to overlap
  with a render — the serial limit is render-to-render only.
- **Pre-flight HTML with `motion.screenshot`** before a full render — a ~2s
  screenshot at `--atMs=<mid-scene>` beats a 20–45s wasted render. It inlines
  GSAP and seeks the paused timeline, so it previews the animated frame (not
  the static pre-JS DOM).
- **Re-read sparingly**: pass `--includeTranscript=false` after the first
  `project.read`, and reuse the `{ project }` each mutation returns instead of
  re-reading.

### Anti-patterns (do NOT do these — all profiles)

- **3 effects on the same moment** (zoom + lower-third + motion graphic at same t) — visual noise
- **Multiple LUTs per project** — pick one from the profile table
- **SFX on every cut** — cap at 1 meaningful SFX per 15–30s (except `shorts`, where 1 per 5–10s is fine)
- **Speed regions over voice** — always for setup / B-roll / scrolling only
- **Logo intro >5s** (any profile) — retention cliff
- **Asking the user which filler words to remove** — always-safe op, just do it
- **Applying `youtube-long` defaults to a `shorts` project** — wrong aspect, music too quiet, captions too subtle, pacing too slow
- **Motion graphics in `loom`** — kills the "this is a quick update" vibe

### Entry triggers — phrases that start the playbook

These phrases all route to the edit runbook above. Don't ask the user
to expand any of them — resolve the profile + style, announce the plan,
execute.

| User says | Resolve to |
|---|---|
| "edit this" / "polish this" / "make it engaging" / "make it ready" | `youtube-long`, no style override |
| "YouTube-ready" / "make a YouTube video" / "edit for YouTube" | `youtube-long`, no style override |
| "make it a Short" / "TikTok" / "Reel" / "vertical" / "9:16" | `shorts`, no style override |
| "for LinkedIn" | `linkedin`, no style override |
| "Loom" / "internal update" / "just cut the fluff" | `loom`, no style override |
| "edit like Ali Abdaal" / "Ali Abdaal style" / "tutorial style" / "productivity video" | `youtube-long` + **Ali Abdaal** override |
| "MKBHD style" / "tech review style" / "product review" | `youtube-long` + **MKBHD** override |
| "MrBeast style" / "high-retention" / "challenge video" / "maximum engagement" | `youtube-long` + **MrBeast** override |
| "Veritasium style" / "educational" / "Kurzgesagt vibe" / "explainer" | `youtube-long` + **Veritasium** override |
| "Vox style" / "essay" / "narrative" / "Johnny Harris style" | `youtube-long` + **Vox** override |

If the user doesn't name a style and doesn't specify a destination, the
safe default is `youtube-long` with no style override — the most common
case by far.

### Pattern: one-shot execution

After entry trigger + profile/style resolution, announce the plan in
one sentence and execute. Load `reference/motion-philosophy.md`
automatically before the motion-graphics steps. Run the full runbook
including the mandatory frame-verification gate. Do NOT ask the user
to approve individual steps.

> I'll edit this as a **YouTube long-form in Ali Abdaal style** — aggressive
> filler + silence removal, 3–5s pacing, 4 right-rail concept callouts at
> emphasis claims, 1 stat-reveal takeover, `modernVibrant` LUT at 0.5,
> warm ambient music at 0.15, `bold` captions at y=0.85, and a 5s
> outro CTA card. Motion graphics authored against motion-philosophy
> (chrome-gradient, grid + vignette + grain). Frame-verify before export.
> ~5 minutes.

> I'll edit this as a **Short** — aggressive pacing (hook in 3s, 6–12
> zooms/min), `modernVibrant` LUT at full intensity, `neon`
> captions positioned higher, music at 30%. No intro card or lower
> thirds — they don't fit the vertical frame. Frame-verify before
> export. ~2 minutes.

> I'll edit this as a **MrBeast-style YouTube video** — 2–3s pacing
> (very fast), `warmSunset` LUT at 0.8, dramatic orchestral bed at 0.30,
> huge color-coded `neon` captions, chrome kinetic-type every 5s,
> full-frame stat takeovers, 6s outro teaser card. Motion graphics
> authored against motion-philosophy. Frame-verify before export.
> ~6 minutes.

Don't ask the user to micro-manage step choices. The profile table +
creator overrides + motion-philosophy are the answer. If something
genuinely needs user input (missing brand reference for a named style
that has none obvious, missing subject name for the lower third),
collect ALL such questions in a single message — never one-at-a-time.

## In-app agent sessions — observe and stop

The desktop app embeds its own chat agent. Two verbs (app >= 1.60) let an
external agent see and control those sessions: `agent.session-list` (id,
title, timestamps; returns `running:false` when the embedded agent server
is down — it never starts it) and `agent.session-stop --sessionId=<id>`
(or `--all=true`) to abort execution while keeping the transcript. Use
when the user reports the in-app agent doing something unattended.

## What this skill is NOT for

- **Cloud video APIs** (HeyGen, Runway, Sora). PandaStudio is local-only.
- **Direct edits to `.pandastudio` project JSON.** The format is owned by the editor and changes between versions. Use `project.read` / `project.save` and treat the JSON as opaque between reads.
- **Cloud video APIs** — PandaStudio is local-only; `export.start` renders on the user's machine.

## Reference files

- [`reference/commands.md`](reference/commands.md) — every verb.noun with arg schema and a one-line example.
- [`reference/examples.md`](reference/examples.md) — multi-step recipes + the long-form **motion-graphics authoring recipes** (SaaS promo, tilted-device shots, multi-image scenes, complex multi-overlay HTML) that used to live inline in this file. Read on demand when authoring a bespoke `motion.render-html` graphic.
- [`reference/templates.md`](reference/templates.md) — what each motion-graphic template looks like, with the slots it accepts and which aspect ratios it supports.
- [`reference/motion-philosophy.md`](reference/motion-philosophy.md) — **the aesthetic contract.** Laws, visual vocabulary, easing dictionary, canonical shell, pre-flight checklist. Load this BEFORE authoring any motion graphic. This is what raises output from "template-filled" to "HyperFrames-quality".
- [`reference/video-authoring.md`](reference/video-authoring.md) — **3-mode delivery playbook.** Mode A (9:16 camera-only), Mode B (9:16 screen-rec + PiP face — PandaStudio's unique mode), Mode C (16:9 YouTube side-overlay). Face choreography, caption safe zones, audio-sync protocol, frame verification. Load this for any shorts/YouTube authoring task.
- [`reference/promo-and-mg-videos.md`](reference/promo-and-mg-videos.md) — **the design bar for a from-scratch promo / all-motion-graphics video** (the graphics ARE the video). Show-don't-tell map, scene-variety archetypes, the templated-slideshow anti-pattern, and the motion/depiction/variety quality gate. Load this FIRST for any promo / teaser / explainer-from-scratch.
- [`reference/motion-recipes.md`](reference/motion-recipes.md) — menu of ~30 named, seek-safe motion patterns + scene transitions + the **determinism guardrails** (incl. the `data-duration`/`data-start` are-in-SECONDS rule, the GSAP-must-load rule, and the motion-quality gate). Read when authoring custom motion for a specific beat.
- [`reference/motion-templates.md`](reference/motion-templates.md) — background modes, designed segments, and the full bundled-template catalog (incl. podcast layouts). Read when picking/rendering a template via `motion.generate`.
- [`reference/custom-html.md`](reference/custom-html.md) — the render verbs (`motion.screenshot`/`render-html`/`concat`), transparent overlays + frosted glass, add-by-jobId. Read alongside motion-philosophy when authoring custom HTML.
- [`reference/visual-edits.md`](reference/visual-edits.md) — zooms (incl. follow-cursor + `--anchorSourceMs`), trims, speed, crop/reframe, face centering, webcam + per-section podcast layouts, speaker-driven editing. Read for any visual edit.
- [`reference/audio-color-music.md`](reference/audio-color-music.md) — `audio.clean`, background-audio regions, bundled + Lyria music, and LUT color presets.
- [`reference/captions-metadata.md`](reference/captions-metadata.md) — captions (toggle/style/font), AI title/description/timestamps, YouTube thumbnails.
- [`reference/fx-transitions.md`](reference/fx-transitions.md) — scene transitions + FX overlays, with the restraint rules.
- [`reference/media-generation.md`](reference/media-generation.md) — Replicate narration (TTS) and B-roll image generation (always Ken-Burns a still).
- [`reference/shorts.md`](reference/shorts.md) — turn an export into vertical clips: discover shots, fork per shot, the 9:16 playbook, batch.
- [`reference/publishing.md`](reference/publishing.md) — connect + publish to YouTube and Instagram, with the privacy/account/workspace hard rules.
- [`reference/projects-and-transcription.md`](reference/projects-and-transcription.md) — folders, rename, transcription languages, transcribing a standalone file.
