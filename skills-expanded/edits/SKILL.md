---
name: edits
description: Use when the user wants something done in Instagram Edits for Mac through the `edits` MCP tools - opening or creating a project, importing footage, adding text, captions, effects, transitions, sound or music, or exporting - or when an Edits tool call fails and you need to know why.
---

# Working in Instagram Edits through the `edits` tools

The `edits` MCP server is Edits for Mac's own automation server, reached through the Insta Edits for Claude bridge (`insta-edits`).
It is undocumented and updated weekly, so treat the live tool list and `getCapabilities` as the source of truth over anything below.

## Before the first call

- If a call fails with "Cannot reach Edits", Edits is closed or its server is off: ask the user to open Edits and turn on Settings > Automation > Enable Automation Server.
- If it fails with HTTP 401/403, the token changed in Edits. Ask the user to update it in `/plugin` (or run `insta-edits set-token`). Never ask them to paste the token into the chat.
- `insta-edits doctor` in a terminal checks every link and is the first thing to run when something is off.

## How the server behaves

- **The tool list follows the screen.** About 30 tools on the home screen (projects, import, catalogs); the editing tools appear once a project is open. Call `appState` to see the screen, then `projects` and `openProject` (or `newProject`). Edits never announces the change itself; the bridge checks after each call and tells Claude, so the new tools show up without reconnecting. If they don't, call `tools/list` again or check that `edits` runs through the bridge.
- **Discover, don't guess.** `getCapabilities` returns conventions, catalogs and recipes. `listCatalogKinds`, `listCatalog` and `getCatalogItem` say which value each `apply…` tool accepts (effects, filters, LUTs, transitions, text animations and presets, caption styles, fonts, speed curves, masks). Speed curves: apply them with `setSpeedCurve` (`id`, `preset`), using the ids from `listSpeedCurvePresets`. Edits' own catalog names `selectSpeedPanelPreset`, a tool whose description says it is deprecated, refused and crashed the app; the bridge rewrites that entry to `setSpeedCurve`, but if you ever see the old name, don't call `selectSpeedPanelPreset` or `dragSpeedPanelCurve`.
- **Conventions:** time is seconds on the composition timeline; the canvas is normalised 0-1 from the top-left with x/y at the element's centre; colours are `#RRGGBB` or `#RRGGBBAA`; rotation is degrees clockwise.
- **Edits is sandboxed.** `Sandbox bookmark unavailable` means Edits may not read that folder. `~/Movies` works; `~/Downloads`, `~/Desktop`, temp folders and project folders do not. Copy the footage into `~/Movies` first, and export into `~/Movies` too. You cannot write into Edits' own container either: macOS blocks it.
- **Paths must be absolute.** Edits doesn't expand `~`: pass `/Users/<name>/Movies/...`.
- **Check your work with rendered frames.** `captureFrame` (with `atSeconds` or `times`) is the quick check. Use `previewVideo`, then `previewVideoStatus` / `previewVideoFrames`, for a full render rather than screenshots of the app window.
- **New projects start in HDR.** Phone footage looks fine, but screen recordings of the preview blow out to white. Call `setProjectDynamicRange` with `SDR` when the user is recording the screen or delivering SDR.
- **Beats:** `beatMarkers` can return zero beats on the user's own music at any `setBeatDensity`. Fall back to `audioOnsets` on the music element, read the pulse from the onsets, and place markers with `addBeatMarker` before trimming clips onto them.
- **Keyframes:** `setTransformKeyframes` takes a JSON array where every keyframe has `time`, `x`, `y` and `scale`. Read `getTransform` first and keep x/y unless you mean to move the clip.
- **Export:** `export` refuses until a complete preset exists. Call `setExportSettings` first with `resolutionType` (`720p`, `HD`, `2K` or `4K`), `aspectRatio` (such as `nineBySixteen`), `frameRate`, `quality` and `dynamicRange`, then `export` and poll `exportStatus` until it reports complete.

## Rules for the user's account

- **Never publish, share or schedule anything without the user's explicit go-ahead for that specific post.** Edits signs in to the user's Instagram account. The automation server has no tool that posts, shares or schedules: posting happens in Edits' own share screen, so hand that step to the user.
- Ask before deleting a project (`deleteProject`); prefer `duplicateProject` to experiment.
- **Library songs do not survive an automation export.** Songs added with `addSongToComposition` come in as licensed, even ones the catalog lists as royalty-free, and `export` writes silence where they play. The user's own audio files (`addMedia` with `audioKind`) export fine. When a library song matters, leave the final export or post to the Edits window, and say so.
- Add a library song by its exact title: passing a track id sometimes adds a different song. Check the result with `elements`.
