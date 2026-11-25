---
name: proof
description: Record the proof clip a T2+ change needs — one uncut, real-speed Playwright video of the changed user journey on a local fake-mind world, with a scrub bar and timecode burned in, desktop and (when layout changed) phone — then attach it to the pull request without committing video into the repo. Use when a change is tier T2 or higher, when a PR or issue asks for a clip, when the finish skill reaches its proof step, or when reproducing a bug on camera for triage.
---

# proof — an uncut clip of the changed journey

A reviewer should be able to watch what a user would see, at normal speed, start to finish. The clip is the
evidence; a screenshot, a contact sheet or a sped-up recording is not.

Source of truth for what a tier needs: `docs/process/PROOF-POLICY.yml` (T0 nothing; T1 focused tests + typecheck;
T2 adds one clip of the changed journey, desktop, plus phone if layout changed, on a fake-mind world; T3/T4 add more).
Get the tier of the current diff with `node tools/proof/tier.mjs --base origin/main`.

## Rules
- **Uncut and real speed.** One browser context, one take. Never trim, splice, speed up or slow down. If the journey
  is longer than the policy's `max_seconds`, record a shorter journey that still shows the change, not a faster one.
- **The take starts at arrival** (the default): the recording begins once the world is on screen, the arrival card
  is gone and the page has painted that (two frames), so the clip opens on the world, not on loading. From there it is one uncut, real-speed take of the journey,
  which is what the policy asks. When loading or arrival is itself what the change is about (the arrival card, a
  loading screen, first paint), or the journey is not on a world page (the world list, sign-in), pass `--from-load`:
  the take then starts at page creation. The sidecar's `start` (`arrival` or `load`) says which was used, and
  `upload.mjs --proof` copies it into proof.json `media[]`.
- **By day.** On a local world URL the recorder sets the world to midday with its clock paused before the page opens
  (`--time-of-day 12`, the default; the god env route as the dev owner). Dev worlds boot at 06:00 and run a world day
  per real hour, so without it a world up for 40 minutes is at night. Setting it is one `world` entry in the world's god
  history, and the clock stays paused afterwards. Pass another hour, or `--time-of-day keep` when the clock, the light
  or the god history is what the change is about. The sidecar's `worldTime` says what was set.
- **Real input.** Drive with `page.mouse`, `page.keyboard`, `page.touchscreen` or locator clicks, the way a user
  would. Do not call app internals from `page.evaluate` to make things happen on camera.
- **Fake minds, isolated data.** Local worlds only, `BRAIN_MODE=fake`, a fresh data dir. Never record against a
  production world unless the maintainer asks, and never with a signed-in personal browser profile.
- **No local URL on screen.** A Soul's owner card shows the Reconnect box whenever the Soul reads as disconnected, and
  the box prints the world's URL and the Soul's id. Keep an agent listening for the whole take. The recorder watches
  for this and fails a take that shows it (section 3).
- **Never commit video** (or frames) into the repo. Work under `.e2e/` (gitignored).
- The clip must show the change. Watch it (or at least extract frames, below) before you attach it.

## 1. Start a local world

One command starts a local world of the new engine: N2's test world, its gateway, the directory with the dev sign-in,
the viewers' origin and the page built from this checkout, all on loopback (`v2/tools/dev/run.sh`; its head lists
what it needs and builds). No model runs: the engine has no mind.

```bash
v2/tools/dev/run.sh --port 4710 --dir .local/proof > .local/proof.log 2>&1 &
# wait for the line `ready http://127.0.0.1:4710` in .local/proof.log, then:
#   the world              http://127.0.0.1:4710/w/dev/
#   signed in as Ada, its creator   http://127.0.0.1:4710/w/dev/?as=Ada
#   the homepage           http://127.0.0.1:4710/
```

The dev sign-in is `as=<test person>` in the address and works on loopback only; on any other host the command
refuses to start. Use a free port (the command takes four, from `--port`); `e2e/config.mjs` lists ports reserved for
other harnesses. Stop it with `kill <pid>` of the command when done: it stops everything it started.

On this page the recorder needs two flags until its arrival check and world-time route are re-pointed (#2838):
`--from-load` (the take starts at page creation) and `--time-of-day keep`. For daylight, add `hour=12:00` to the
address: it sets the sky and its light for the picture only.

### The old page (apps/web) on a local new-engine world

Most changes a viewer sees are on the old page, which soul.game serves for every moved world. One command brings it up
on a world of the new engine made from a committed template:

```bash
node tools/playtest/arena/new-engine/old-page.mjs --template worlds/templates/hello-hamlet.json --dir .local/proof-old > .local/proof-old.log 2>&1 &
# wait for `ready http://127.0.0.1:<port>/w/hello-hamlet/` in .local/proof-old.log: that is the old page; the next line
# names the new engine's own page, directory and gateway, where Souls pair (tools/playtest/arena/new-engine/seat.mjs)
```

It runs `v2/tools/dev/run.sh --facts` (the engine), the world launcher's copy of the same template (the page's scenery
and web app, until the old page draws them from the stream), a second front door with soul.game's routes, and
`tools/world-launcher/v2-switch.mjs`, as on soul.game. It needs `pnpm --filter web build` and `pnpm build:viewer`
first. Joined Souls start at the world's entry (0,0: in hello-hamlet that is inside a cottage, so walk them out). The
recorder's `--time-of-day` works here as usual: on a page on the new engine it goes on the address as `?hour=HH:MM`,
and the arrival check is the old page's own. Stop it with `kill <pid>`: it stops everything it started.

## Quick proof the app works: the local smoke

Before recording, or as the whole proof of a T1 change that touches the server or web app, run the local smoke. It
boots its own isolated launcher (fake minds, dev sign-in, data under the run dir) on a free port, opens the world list
and one world, checks that a person is drawn with no console errors and no failed requests, and stops what it started:

```bash
node e2e/local-smoke.mjs --port 9950 --clip      # --build first on a fresh clone; omit --port for any free port
# → .local/e2e/<timestamp>/summary.json, shots/1-world-list.png 2-world.png 3-person.png, clip.mp4
node tools/proof/upload.mjs --pr $N .local/e2e/<timestamp>/summary.json .local/e2e/<timestamp>/shots/*.png
```

`status: "pass"` in `summary.json` is the evidence; its clip is one uncut, real-speed take of the smoke journey. It is
not a clip of your change: a T2 change still records its own journey below. Details: `docs/testing/e2e.md#local-smoke`.

## 2. Write the steps

Copy `.claude/skills/proof/steps.example.mjs` to `.e2e/proof/<slug>/steps.mjs` and script the changed journey:
do the thing, show the result. With the default arrival start the steps begin on the arrived world (the `arrived` mark
is 0:00); with `--from-load` they begin right after navigation. `mark('label')` stamps a chapter time into the sidecar
so the PR can say "the panel opens at 0:07". Keep it to the journey the change affects.

When an owner's card is on screen, set `SOUL_DIR` to the Soul's CLI folder (and `EDEN` to its `eden.mjs` if it isn't this
checkout's). The example then holds a `listen` from before the page opens until the recorder exits, starting it again
when the owner's message ends it. Keep that block when you copy the file.

## 3. Record

```bash
node .claude/skills/proof/record.mjs --url 'http://127.0.0.1:4710/w/dev/?as=Ada&hour=12:00' --from-load \
  --time-of-day keep --steps .e2e/proof/<slug>/steps.mjs --out .e2e/proof/<slug>/desktop.mp4 --viewport desktop
# layout or touch changed? also:
node .claude/skills/proof/record.mjs --url '...' --steps .e2e/proof/<slug>/steps.mjs \
  --out .e2e/proof/<slug>/phone.mp4 --viewport phone
```

### Presets: what the clip is for

`--preset` picks the output; `pr-proof` is the default and is what every PR proof uses. Each preset is still one
uncut, real-speed take with the timecode, so any of them counts as proof.

| Preset | Output | Use it for |
|---|---|---|
| `pr-proof` (default) | `--viewport desktop` 1280x720 or `phone` 390x844, the recording's own frame rate | PR proofs: small, quick to upload and load |
| `social-landscape` | 1920x1080, 30 fps | posts and videos in 16:9 |
| `social-portrait` | 1080x1920, 30 fps, phone layout | reels, stories and shorts in 9:16 |
| `highlight` | 1280x720, 30 fps | clips embedded in a highlights page (light enough to autoplay) |

Overrides sit on top of any preset: `--fps 15|30|60` (repeats or drops frames, never changes speed), `--quality low`
(720 short edge) or `high` (1080), `--size WxH`, `--aspect landscape|portrait`. The page is recorded at the output's own
aspect, a landscape page at desktop size and a portrait page at phone size, with the browser's scale factor making
the pixels, so nothing is cropped or upscaled afterwards. The sidecar records `preset` and the resolved `plan`.
The table lives in `tools/proof/clip-presets.mjs`.

```bash
node .claude/skills/proof/record.mjs --url '...' --steps .e2e/proof/<slug>/steps.mjs \
  --out .e2e/proof/<slug>/portrait.mp4 --preset social-portrait --panel on
```

**Debug panel** (`--panel on`, off by default and off for PR proofs unless a reviewer needs the exchange): a live view
of what the Soul's agent sent and what the world answered, in time order with clip timestamps: commands `→`, replies
`←`, receipt phases `•`, notes `·`. It sits beside the world in landscape and below it in portrait. The steps feed it:
`await ctx.eden(soulDir, ['act', id, params])` runs a Soul CLI command, logs it and its reply, and follows the receipt
until it ends; `ctx.panel('text')` logs a note; `--panel-log <file.jsonl>` adds lines another process appends
(`{"at": <epoch ms>, "dir": "cmd|reply|receipt|note", "text": "..."}`). Entries are redacted (URLs, paths, tokens,
emails, addresses; Soul, receipt and other ids become `soul-1`, `receipt-1`), then the publication checker runs on
them; a hit fails the take (exit 4, privacy kind `panel-text`) before anything is drawn. The text goes to
`<clip>.panel.json`, which `upload.mjs` checks like any payload; attach it with the clip.

- Browsers: uses `PLAYWRIGHT_BROWSERS_PATH`, else `/opt/pw-browsers` when present. If Chromium is missing:
  `PLAYWRIGHT_BROWSERS_PATH="$PWD/.e2e/browsers" pnpm --filter mars-campus-viewer exec playwright install chromium`.
- Playwright is resolved the same way the playtest harness does (`tools/playtest/lib/platform.mjs`: a global
  `playwright`, else `@playwright/test` from `mars/viewer`). No GPU is needed; WebGL runs on SwiftShader. A busy machine drops frames: record on a GPU runner instead (`docs/testing.md#recording-a-proof-clip-on-a-gpu-runner`; `SIM_PROOF_GPU=hardware` makes the recorder use and name a hardware renderer).
- `--max-seconds` defaults to the policy's `max_seconds`. Exit 3 means the journey ran past it: shorten it.
- With ffmpeg: an mp4 with a thin progress line along the bottom edge and a small `m:ss.s / total` timecode chip at
  the bottom left. The recorder's Chromium draws the timecode, so it needs no ffmpeg `drawtext` or fonts; the
  sidecar's `timecode` says whether it is there. Without ffmpeg: the raw `.webm`; say so in the PR (players still show
  their own scrub bar).
- Each clip gets a `<clip>.json` sidecar: url, viewport, `durationSec`, `videoSec` (the recording's own length, about a
  second longer), `start`, `startedAt`, marks (`arrived` among them), `worldTime`, console errors, `privacy`, commit and
  dirty flag. Sidecars hold local paths: they stay unpublished, and `upload.mjs` refuses one. A Playwright without `page.screencast` records from page creation
  even without `--from-load`; the sidecar says so in `startFallback`.
- **Exit 4: the take showed something private.** Every 500 ms the recorder reads the page's visible text, fields
  included, for the page's own host (any port; `soul.game` is exempt) and the wording of the Reconnect box and the start
  prompt. The sidecar's `privacy` lists each hit by kind and second, never the text: `page-host`, `reconnect-box`,
  `start-prompt`, or `not-watched` when no read succeeded. `upload.mjs` refuses the clip. Fix the cause (usually a listen
  that wasn't held) and record a new take; never delete or edit the sidecar to get past this. It reads text, not
  pixels, and something on screen for less than the sidecar's `maxGapSec` can slip between reads, so step 4 still
  stands.
- The page has `--arrival-seconds` (default 120) to arrive before the take starts; a page that never shows a world fails
  (exit 1) with a hint to use `--from-load`, a still of where it stuck (`<clip>.open-failed.png`) and a sidecar.
  Console errors in the sidecar are findings: explain or fix them.

The run takes well under the 10-minute foreground limit. For several clips in one go, run them in the background
(`nohup setsid node ... > .e2e/proof/<slug>/rec.log 2>&1 &`) and poll the log.

## 4. Check it yourself

```bash
for t in 1 4 8; do ffmpeg -loglevel error -y -ss $t -i .e2e/proof/<slug>/desktop.mp4 -frames:v 1 .e2e/proof/<slug>/t$t.png; done
```

Look at the frames (Read the PNGs). The changed state must be visible, the world must have loaded (not a blank or
loading canvas), and nothing in frame should be private. If it does not show the change, fix the steps and record a
new take; do not attach a clip that does not prove the claim.

## 5. Attach it to the PR (never commit it)

Check every outgoing text/JSON payload with `node tools/proof/publication.mjs <payload files>` before publication.
Inspect media pixels, audio, filenames and binary metadata separately. Device paths, hostnames, device/private IPs,
local URLs and operational identifiers belong only in private records. Use relative paths and neutral capture
labels. The uploader blocks detected text leaks before uploading the batch; this cannot certify media privacy.

```bash
node tools/proof/upload.mjs --pr $N --proof .e2e/journal/$ISSUE/proof.json .e2e/proof/$SLUG/desktop.mp4 .e2e/proof/$SLUG/phone.mp4
```

- Proof goes to the proof CDN: `https://assets.eden.art/proofs/pr-<n>/<file>`, uploaded with the R2 credentials the
  CDN tools use (`EDEN_ASSETS_CREDENTIALS`, else the main checkout's `.local/project/team/secrets/eden-assets-r2.env`,
  and `CF_ACCOUNT_ID` from `deploy.env`); it works from a worktree. Never GitHub releases: those are for versions of
  the software, and `proof-ok` no longer counts links on them. A re-take gets `-2`, `-3`, so earlier takes, including
  failed ones, stay linkable. Without the credentials (cloud sessions, outside contributors) the upload is blocked:
  drag the clips into the PR description instead, and GitHub hosts them. `SIM_PROOF_UPLOAD_URL`
  (+ `SIM_PROOF_UPLOAD_TOKEN`) switches to another endpoint.
- With `--proof`, clip and image links are written into proof.json `media[]`, other files (logs, JSON) into
  `files[]`, and proof.json is uploaded last. Paste its link
  and the clip links into the PR's Proof section. The `journal` skill covers proof.json.
- With `--proof`, a clip's `uncut`, `realSpeed`, `seconds`, `viewport` and caption come from its recorder sidecar where
  proof.json leaves them unset; what you stated is never overwritten, so write `uncut: false` and it stays. A clip whose
  `uncut` or `realSpeed` would stay unset is refused before anything is uploaded (`proof.media-incomplete`): keep the
  sidecar beside the clip, or state both in its media entry.
- A clip whose sidecar records a privacy hit is refused, with or without `--proof` (`proof.clip-private`).
- **Inline preview.** GitHub plays only its own attachments inline, so a CDN mp4 link never plays in the PR. For each
  video, `upload.mjs` makes a small animated GIF with ffmpeg (`<clip>.preview.gif`: 6 s at real speed from the clip's
  `arrived` mark, or from 0 for a `--from-load` take; at most 5 MB), uploads it beside the clip, records it as `media[].preview` and prints a line like
  `[![desktop.mp4](…/pr-412/desktop.preview.gif)](…/pr-412/desktop.mp4)`. Paste that line: the preview plays in the
  PR and clicking it opens the full clip. When the change shows later in the clip, pick the window with
  `--preview-start <s>` (and `--preview-seconds <s>`). The preview is a pointer, not the proof: the uncut mp4 is.
  Always put an explicit **Full-resolution uncut video** link before each preview, stating the actual encoded
  dimensions and duration. Preserve capture resolution and frame the action so contact can be reviewed. Do not
  upscale a capture or use the reduced GIF to claim motion proof.
- **Exit 3: the upload is blocked** (no `gh`, not signed in, no permission, or no network, as in many cloud
  sessions). Tell the user which clips are waiting and where. Post a PR comment with each clip's duration,
  viewport, sanitized sidecar summary (marks, console errors, commit), and a repository-relative `record.mjs`
  command and steps file, so
  anyone can re-record it. Mark the proof "pending upload" in the PR body. Never paste video as base64, never
  commit it, and never push it to another branch.

`gh pr` may not work in cloud sessions; comment with
`gh api repos/$REPO/issues/$N/comments -F body=@.e2e/proof/$SLUG/comment.md`.

## What to write next to the clip
One line per clip: what journey, which world template, viewport, duration, commit, and the moment the change is
visible ("0:07 the seat highlights and the Soul sits"). Plus any console errors and why they are acceptable.
