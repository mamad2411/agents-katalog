---
name: cueframe-cli
description: Use when editing, clipping, or rendering video via the CueFrame CLI — e.g. "make a 9:16 short from this podcast", "pull the best moments out of this MP4", "render a clip", or any task that calls the `cueframe` binary. Also use when comparing CueFrame against direct-ffmpeg approaches.
---

# CueFrame CLI

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

## MCP is the primary surface — read this before using the CLI

**For a tool-driven workflow, prefer an existing supported MCP connection. For an explicitly requested terminal or CI workflow, use the CLI.** MCP is the supported, maintained integration surface: it hides transport and
contract details, its tools are generated from the same OpenAPI SSOT the CLI is, and it is where
new capability lands first. The `cueframe-connect` skill owns the setup for every host
(Claude Code, Claude/ChatGPT connectors, Cursor/Codex/VS Code/Windsurf/Zed, and the
no-account pay-per-call path) — load it rather than copying a connection command from here.

**Use this CLI when MCP is not available to you:** a terminal or CI job with no MCP host, a
scripted batch, or a human at a shell. It is a first-class path, not a deprecated one — but it is
the *second* thing to reach for.

**Do not hand-roll `curl` against `/v1`.** Raw REST is the fallback beneath the fallback: it is
where undocumented contract edges bite (components' runtime params were discovered that way), and
both MCP and this CLI exist so you do not have to.

## Overview

The `cueframe` CLI drives the CueFrame platform from the terminal. Optimized for agents — every command supports `--json` (NDJSON event stream) and the binary self-describes via `npx -y cueframe@0.12 describe --json`.

**Run it as `npx -y cueframe@0.12 …` — every command in this skill is written that way, and
that form is executable verbatim.** There is no `cueframe` on your PATH unless you put it
there: `npx -y cueframe@0.12 install` wires the MCP server and drops these skills, but npx
unpacks to an ephemeral cache, so it installs no binary. `npx` re-resolves the current
version on each call (~0.5s warm, ~5s cold), which also means these commands never go
stale. If you are running many in a row and want to skip that, `npm i -g cueframe` once
and drop the `npx -y ` prefix — but it needs a user-writable npm prefix (a default Linux
install fails `EACCES` on `/usr/local/lib/node_modules`), so it is an optimization, not
the documented path.

**The framework is three verbs:** `upload` (register media) → `composition put` (author the timeline) → `render` (→ MP4). The `Composition` is the contract — render takes the saved composition, nothing else. Everything domain-specific (AI clip suggestions, FCPXML/Premiere export) is a **use-case on-ramp** layered on top, not part of the core.

**Core principle — discover, don't guess.** Never author a composition from the
examples below alone. The live contract is `npx -y cueframe@0.12 schema composition` (prints
the real wire schema the server enforces); confirm any draft with
`npx -y cueframe@0.12 composition validate -b @file.json` BEFORE you render. Validation is
free and instant; a render is neither. The examples here are orientation — the
schema is the source of truth.

**Core principle:** once you are ON this path, drive everything through `cueframe` — never `curl` the v1 API around it, which invalidates the work and hides CLI bugs. (Choosing MCP over the CLI in the first place is not "going around it"; see the banner above.)

## Framework workflow (upload → compose → render)

The general path for any agent. Author the timeline yourself and render it — no
clip suggestion required.

For iteration, use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md).
Validate first, then use `preview_card` / `preview_component` for isolated graphics,
`preview_frame` for composition stills, or `preview_clip` for a motion window. Use the available
MCP tools or the CLI's `api` escape hatch with the live request contract. Full `render` is for
delivery, not checking each edit. CLI validation does not replace visual evidence.

To compare a certified reference frame with an existing saved preview, use `compare`:

```bash
npx -y cueframe@0.12 compare <projectId> --reference-media <mediaId> --reference-representation <identity> --reference-frame 117 --candidate-job <jobId> --candidate-artifact <artifactId> --out ./comparison --json
```

The command calls the shared comparison operation; it does not rerender the composition. `--views overlay,difference` selects diagnostics and `--crop x,y,width,height` uses one common-coordinate crop. NDJSON contains source identities and image receipts, never base64 payloads. `--out` saves verified PNGs; without it, image receipts explicitly say `metadata_only`. Inspect those images and relevant motion before judging the film.

```bash
# 0. Always use --json for agent-driven runs (NDJSON to stdout, no spinners).
#    Commands run against production; auth is stored in ~/.cueframe/auth.json.

# 1. Register media (one or many — mixed video / image / audio).
npx -y cueframe@0.12 upload "/path/to/source.mp4" --json   # → mediaItemId (process_complete)

# 2. Create a project (sets aspect/format).
npx -y cueframe@0.12 project create -n "promo" -a 9:16 --json   # → projectId

# 3. Author the composition: tracks of clips (per-clip reframe/trim), optional
#    captions (captions.segments), brandKitId. The composition is the SSOT.
#    Discover the live schema, then validate the draft BEFORE saving/rendering:
npx -y cueframe@0.12 schema composition                                 # → live wire schema
npx -y cueframe@0.12 composition validate -b @composition.json          # → ✓ valid | per-field errors (no render)
npx -y cueframe@0.12 composition get <projectId> --json                  # → etag (not found = no composition yet)
npx -y cueframe@0.12 composition put <projectId> -b @composition.json --if-match <etag>
#    --if-match is required: a save made since your `get` fails with 409 stale_etag
#    instead of being overwritten. Re-`get`, re-apply your edit, retry. Use --create
#    only for the first composition of a project (refused 409 if one exists).

# 4. Render the saved composition to MP4. SSE-watches + downloads when done.
npx -y cueframe@0.12 render <projectId> -o ./out.mp4 --json
# → render_queued → render_progress* → render_complete
#
# `render` takes ONLY a projectId and renders the SAVED composition (tracks +
# captions). A clip suggestion is NOT required. Re-running the same command on an
# unchanged composition replays the same render (the Idempotency-Key hashes the
# project, the composition ETag and the request: --aspect/--fps/--resolution/
# --priority/--intent); editing the composition or changing a flag starts a new one.
# Without --aspect it renders the composition's own format. --aspect must match the
# composition's aspect (a new aspect is a `derive_composition`, not a render flag);
# pass it with --resolution hd|fhd|4k to change only the output resolution.
# Captions: render reads composition.captions — put caption words there to caption
# a hand-authored composition; if absent, the clip is rendered without captions.

# Reattach to an in-flight render later (e.g. after disconnect):
npx -y cueframe@0.12 render watch <renderId> -p <projectId> -o ./out.mp4 --json
```

## Anatomy of a composition.json

This section orients you to the shape; the authoritative contract is
`npx -y cueframe@0.12 schema composition` (the live wire schema) — run it when a field is
unclear, and `npx -y cueframe@0.12 composition validate -b @file.json` to check a draft.

`composition put` takes the **bare** `Composition` object (no wrapper; the CLI PUTs
the `@file` verbatim with your `--if-match` ETag). Minimal valid shape:

```json
{
  "v": 1,
  "format": { "aspectRatio": "9:16", "fps": 30 },
  "tracks": [
    { "id": "v1", "kind": "video", "contents": [
      { "id": "c1", "startTime": 0, "duration": 10, "source": { "kind": "media", "mediaId": "<mediaId>" } }
    ] }
  ]
}
```

- **Required**: `v: 1`, `format.aspectRatio` (`16:9` | `9:16` | `1:1` | `4:5`), `tracks`.
- Tracks hold **`contents`** (not `clips`); each clip wraps a `source`. A clip's
  `source.kind` must match the track `kind`: `media` → `video`/`image`/`audio`,
  `overlay` → `overlay`, `effect` → `effect`.
- `source.kind`s: `media` (`mediaId` + optional `trim`/`reframe`/`volume`), `overlay`
  (`primitiveId` + `params` + optional `zPlane`), `effect` (`primitiveId` + `params`).
- Times are **seconds** (`startTime`/`duration`/`trim`, and `reframe` `startSec`/`endSec`);
  caption word times are **milliseconds**. `region`/`fit` (PiP/inset) are clip-level.
- Clips on one track can't overlap — simultaneous layers go on separate tracks.
- Optional top-level: `captions` (`segments[].words[]`), `brandKitId`, `markers`.

For full per-video-type examples (auto-zoom demo, PiP, split-screen, captions,
behind-subject title), see the `cueframe-product-video` skill.

## Render resolves expensive intents automatically — author, don't pre-bake

You author *intent* on the composition; `render` materializes the expensive
artifacts it implies. Nothing to pre-bake, no compose step required:

- An overlay with `"zPlane":"behind-subject"` → the person **matte** is baked
  on-miss and the text is placed behind the speaker (shoulder-band anchor +
  occlusion handled). Author it and render — it just works.
- A clip whose `reframe.focus` is `{mode:"face",faceId}` / `{mode:"active-speaker"}`
  / `{mode:"all-faces"}` → **subject detection** runs on-miss so the crop tracks the
  real person. (`{mode:"point"}` / `{mode:"frame-center"}` need no detection.)

During this the SSE `render_progress` phases read
`resolving → baking-matte | detecting → rendering → complete` — the first behind/face
render of a source pays a one-time bake (cached after; re-renders are fast).

### Render error codes (fail-loud — render never ships a wrong frame silently)

| `code` | meaning | fix |
|---|---|---|
| `media_not_found` | a referenced `mediaId` doesn't exist or isn't your org's | reference media you uploaded |
| `media_not_ready` | the media has no file yet (still uploading/generating) | wait for `upload`'s `process_complete` |
| `source_dims_unknown` | a `reframe` clip's source has no width/height/fps yet | let the source finish processing before authoring a reframe |
| `content_anchor` | a clip's trim frames *different* footage than its captions show (wrong-footage) | align the trim window to the captioned moment |
| `behind_split_unsupported` | one media used under two *different* behind-subject windows | one behind window per media (split into separate clips/media) |
| `BehindMatteUnresolved` / `TrajectoryUnresolved` | the matte/detection bake produced no result for a behind/face clip | the source may have no detectable person; retry, or drop the behind/face intent |

## Clip-suggestion on-ramp ("podcast → short clip")

ONE use-case layered on the framework: the AI clip-finder picks a moment and
**authors a composition for you** (trim + speaker framing + captions sliced from
the transcript). Use it when you want CueFrame to choose the clip; otherwise author
the composition yourself (above).

```bash
# 1. Upload + chain the AI clip pass.
npx -y cueframe@0.12 upload "/path/to/source.mp4" --analyze --json   # mediaItemId + suggestions
# (or run it explicitly: npx -y cueframe@0.12 analyze <mediaItemId> --wait --json)

# 2. List clip suggestions (publicId sug_…, title, startMs/endMs, score).
npx -y cueframe@0.12 clips <mediaItemId> --json

# 3. Create a project AND author its composition from the chosen suggestion.
npx -y cueframe@0.12 project create -n "paul-klein-shorts" -a 9:16 --from-suggestion <sug_…> --json
#   (or, on an existing project: npx -y cueframe@0.12 composition from-suggestion <projectId> -s <sug_…>)

# 4. Render — same framework verb as above.
npx -y cueframe@0.12 render <projectId> -o ./out.mp4 --json
```

Both flows converge on `composition put` → `render`; the on-ramp just authors the
composition from a suggestion instead of you hand-writing it.

Pipe `--json` output through `jq -c 'select(.event=="…")'` to grab specific lifecycle events.

## Component authoring: scaffold your own

Own the motion-graphics components you render (shadcn-style): scaffold a native component as
editable source, customize it, and render it on CueFrame. The source lives in your repo under
version control; CueFrame bakes it to a transparent video and composites it (the shared
renderer never runs your code). The CLI does not fork built-ins: the maintained builtin
presets and recipes are placed as they are (list them with `list_catalog`
projection `component-library`).

```bash
# 1. Scaffold a workspace (writes cueframe.json + cueframe/components/). Idempotent.
npx -y cueframe@0.12 init --json

# 2a. Scaffold a component in cueframe/components/<id>/ as owned, editable source.
npx -y cueframe@0.12 new component my-badge --category ui-blocks --json

# The scaffold is a native (version 4) source: template.html + definition.json, with its
# manifest in cueframe.json.

# 3. Edit cueframe/components/<id>/template.html (one HyperFrames sub-composition ending in
#    __cfScene.mount(...)) and definition.json (inputs, defaults, timing, capabilities).

# 4. Publish to CueFrame so it can render (the server admits the source or names the rule it breaks).
npx -y cueframe@0.12 push my-badge --json            # one component
npx -y cueframe@0.12 sync --json                      # every component in the workspace

# 5. Reference the component id in your composition as a {kind:'component', componentId, props}
#    clip, then render with the same verb. Preview a single component first via the MCP
#    preview_component loop.
npx -y cueframe@0.12 render <projectId> -o ./out.mp4 --json
```

## Quick reference

| Need to… | Command |
|---|---|
| See every command + flags | `npx -y cueframe@0.12 describe --json` |
| Install/refresh managed skills | `npx -y cueframe@0.12 install` (shared `~/.agents/skills` and Claude `~/.claude/skills`; locally changed or untracked packages are preserved and reported) |
| List projects | `npx -y cueframe@0.12 list -n 50` |
| List your media | `npx -y cueframe@0.12 clips` (no mediaId arg) |
| Discover the live composition schema | `npx -y cueframe@0.12 schema composition` |
| Validate a draft (no save, no render) | `npx -y cueframe@0.12 composition validate -b @plan.json` |
| Read composition + ETag | `npx -y cueframe@0.12 composition get <projectId> --json` |
| Write composition | `npx -y cueframe@0.12 composition put <projectId> -b @plan.json --if-match <etag>` (`--create` for the first composition) |
| Export to Final Cut | `npx -y cueframe@0.12 export fcpxml <projectId> -s <sug> --wait -o cut.zip` |
| Export to Premiere | `npx -y cueframe@0.12 export premiere <projectId> -s <sug> --wait -o cut.zip` |
| Anything not wrapped | `npx -y cueframe@0.12 api GET /v1/...  -i` (escape hatch, like `gh api`) |
| Validate a composition without mutating | `npx -y cueframe@0.12 composition validate -b @plan.json` |

## Auth

Commands run against production. Authenticate once:

- `npx -y cueframe@0.12 login` — OAuth device flow (laptops).
- `npx -y cueframe@0.12 auth <cf_live_… key>` — save a static API key (CI / headless).

Creds are stored in `~/.cueframe/auth.json`; the key can also come from the `CUEFRAME_API_KEY` env var.

## NDJSON event shape

Every `--json` line:
```json
{"_":0,"schemaVersion":"v1","ts":1779250551614,"event":"<verb>_<phase>", ...payload}
```
Phase lifecycle: `<verb>_prepare` → `<verb>_ready` → `<verb>_progress` (0+) → `<verb>_complete` | `error`. The `_:0` field is a pino formatter placeholder — ignore it.

Errors come as `{"event":"error", "phase":"<step>", "message":"...", "code":"...", "exitCode":N}` *and* a non-zero process exit. Read both.

## Common mistakes

| Mistake | Reality |
|---|---|
| Reaching for `curl …/v1/...` because the CLI didn't have a command | Use `npx -y cueframe@0.12 api METHOD /v1/...` — same auth, same JSON pipeline. |
| Polling for render completion with a sleep loop | `npx -y cueframe@0.12 render` already SSE-watches and exits when done. Use `render watch <id>` to reattach. |
| Skipping `--json` and trying to parse human output | Human output is for humans. Agents always use `--json`. |
| Hand-editing the composition without an ETag | `composition put` refuses without `--if-match <etag>` from the `composition get` your edit started from. Don't fetch a fresh ETag right before the put: that overwrites anyone who saved in between. `--create` is only for a project's first composition; there is no unconditional overwrite. |
| Calling `npx -y cueframe@0.12 render <projectId> <suggestionId>` (old two-positional shape) | `render` takes ONLY a projectId; commander rejects the extra arg. It renders the SAVED composition — author it first via `composition put` (hand-author) or `project create --from-suggestion <sug>` (clip-finder on-ramp). |
| Assuming `render` needs a clip suggestion / that captions only come from a suggestion | No — `render` renders the saved composition directly; a suggestion is optional. Captions come from `composition.captions` (author them in the `put` JSON). The clip-suggestion on-ramp just fills those captions for you by slicing the transcript at author time. |

## When this skill applies (routing)

Use this skill for a requested terminal/CI workflow or when the available CLI is the supported path for the task. If supported MCP tools are already connected, use their narrow edit/preview guidance instead. A mechanical operation inside a creative task does not require a different project or new installation. If a required capability is absent, report the limitation and a supported alternative; do not invent a command or silently change lanes.

CLI development and internal backend inspection are outside this usage skill.
