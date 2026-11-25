---
name: cutbolt
description: "Edit existing footage with captions, loudness adjustment and delivery in saved Cutbolt timelines; route specialized edits to their workflow skills. For a complete talking-head cut with captions and delivery, use recut-talking-head directly."
---

# Edit existing footage

Use Cutbolt's local MCP tools for saved, reversible edits. The engine needs an installed
cutbolt executable and external FFmpeg/ffprobe; cutbolt doctor checks that setup.
Keep footage and generated files in the chosen workspace. Outputs must use new names.
Files outside it need an explicitly chosen input root; never overwrite an original.

For a new animated video from a brief, an HTML graphics tool may be a better authoring
choice. Cutbolt can finish its rendered graphics over footage. For a title on footage,
use an original built-in template with graphics.place.

## When Cutbolt isn't installed

The plugin starts cutbolt from PATH and installs nothing. With no cutbolt_* tools, or with
plugin:cutbolt:cutbolt failed in /mcp, the executable is usually missing from PATH; run
cutbolt --version in a terminal to check. If it prints a version, don't reinstall: run cutbolt
doctor and follow its repair hints; once it reports ready true, restart Claude Code from that
terminal, in the folder that holds the footage. Otherwise, with the user's agreement:

1. Install an engine that matches these recipes, which follow the repository's main branch.
   With a Rust toolchain supporting edition 2024 and a C compiler/linker, run
   cargo install --git https://github.com/skulitom/Cutbolt --locked
   A prebuilt archive from https://github.com/skulitom/Cutbolt/releases/latest is quicker:
   check it against SHA256SUMS, extract it and add its folder to PATH. It can be older than
   the recipes, though: INVALID_JSON naming an unknown field that a recipe uses means it is.
2. Put FFmpeg and ffprobe on PATH, or set CUTBOLT_FFMPEG and CUTBOLT_FFPROBE; Cutbolt
   bundles neither.
3. In a new terminal, run cutbolt --version and cutbolt doctor; doctor exits 0 with ready true.
4. Restart Claude Code from that terminal, in the folder that holds the footage. Don't also add
   the server with claude mcp add: the plugin already registers it.

Background jobs, which every MCP export uses, need Windows or Linux.

## Calls and results

The plugin starts local stdio MCP in the current project directory. A command such as
session.apply uses the listed cutbolt_session_apply tool without the command key.
When its direct tool is absent, use cutbolt_run with command and arguments.
Queue blocking work with job.start, then job.wait. Read the structured result.
For a large proposal, save_as writes it to a new JSON file and replaces the response with
a file receipt. Read that local file to review it before applying a file/select reference;
it does not also return the proposal or job status. This adds a file-reading call.
Prefer these recipes to schema discovery; request a schema only for a genuinely unknown operation.

Examples below and in the companion skills are engine requests. Replace uppercase
$PLACEHOLDERS with actual input or result values before calling. They are documentation
slots, not engine syntax. Use fresh request IDs for distinct edits; keep the same ID and
identical arguments when retrying an uncertain edit.

## Start a cut

Inspect the source before choosing the project clock and canvas. $SOURCE is a workspace
path; use the returned size/rate for $WIDTH, $HEIGHT and $FRAME_RATE unless the user requested
another delivery. When timeline.ready is false, use the proposed timeline.conform.recipe
canvas and clock if they meet the request (an omitted recipe frame_rate means 25 fps). Supported video normalization can be deferred
until the queued export; use the automatic-add recipe below for that source.

<!-- example: inspect -->
~~~json
{"command":"media.inspect","path":"$SOURCE"}
~~~

When timeline.ready is true and the size/rate fit, use timeline.asset as $ASSET and its
id/duration as $ASSET_ID/$DURATION. If asset.identity is absent, add the inspection identity's
bytes and sha256 (not its path). Preserve the returned decode binding. $TRANSFER declares
the working RGB transfer, for example bt709, from the media/project policy. If no ready
asset or supported video recipe is returned, follow the reported reason; never relabel an
unsupported original. Audio-only normalization still needs explicit media.prepare.

For a new project, create its initial linked picture/sound arrangement in one validated
snapshot. $PROJECT_ID is a new stable name. The clip and link IDs below are new IDs chosen
here; when revising an existing project, read and use its actual IDs instead.

<!-- example: create -->
~~~json
{"command":"session.create","request_id":"create","project":{"schema_version":1,"id":"$PROJECT_ID","revision":0,"width":"$WIDTH","height":"$HEIGHT","frame_rate":"$FRAME_RATE","transfer":"$TRANSFER","assets":["$ASSET"],"clips":[],"tracks":{"duration":"$DURATION","tracks":[{"id":"v","kind":"video","enabled":true,"locked":false,"clips":[{"id":"shot","asset_id":"$ASSET_ID","start":0,"source_in":0,"duration":"$DURATION"}]},{"id":"a","kind":"audio","enabled":true,"locked":false,"clips":[{"id":"shot-audio","asset_id":"$ASSET_ID","start":0,"source_in":0,"duration":"$DURATION"}]}],"links":[{"id":"shot-link","members":[{"clip_id":"shot","start":0,"source_in":0},{"clip_id":"shot-audio","start":0,"source_in":0}]}]}}}
~~~

Keep the returned revision as $REVISION (zero for a new session). The creation receipt records
its initial assets and tracks. Subsequent changes use session.apply with that revision and a
new request ID; retry an uncertain creation with identical arguments and the same request ID.

## Original videos that need normalization

For a new project whose original needs a supported conversion, use these two requests
instead of the populated snapshot above. Choose a new $ASSET_ID; $DURATION is the complete
proposed prepared duration, not the length of a selected excerpt. With a different project
clock, a duration error supplies actual_duration; use it after checking the requested edit.
The explicit input_root opts media.add into inspection and automatic source binding.
A workspace root is "."; the asset path is relative to that root.

<!-- example: create-empty -->
~~~json
{"command":"session.create","request_id":"create","project":{"schema_version":1,"id":"$PROJECT_ID","revision":0,"width":"$WIDTH","height":"$HEIGHT","frame_rate":"$FRAME_RATE","transfer":"$TRANSFER","assets":[],"clips":[]}}
~~~

<!-- example: attach-original -->
~~~json
{"command":"session.apply","project_id":"$PROJECT_ID","expected_revision":"$REVISION","request_id":"add-original","operations":[{"op":"media.add","input_root":".","asset":{"id":"$ASSET_ID","path":"$SOURCE","duration":"$DURATION"}},{"op":"tracks.edit","edit":{"op":"create","duration":"$DURATION"}},{"op":"tracks.edit","edit":{"op":"add","track":{"id":"v","kind":"video","enabled":true,"locked":false,"clips":[]}}},{"op":"tracks.edit","edit":{"op":"place","track_id":"v","clip":{"id":"shot","asset_id":"$ASSET_ID","start":0,"source_in":0,"duration":"$DURATION"},"collision":"reject"}},{"op":"tracks.edit","edit":{"op":"add","track":{"id":"a","kind":"audio","enabled":true,"locked":false,"clips":[]}}},{"op":"tracks.edit","edit":{"op":"place","track_id":"a","clip":{"id":"shot-audio","asset_id":"$ASSET_ID","start":0,"source_in":0,"duration":"$DURATION"},"collision":"reject"}},{"op":"tracks.edit","edit":{"op":"link","id":"shot-link","clip_ids":["shot","shot-audio"]}}]}
~~~

The receipt records the original identity and conversion recipe. Export jobs prepare it
once and reuse its verified cache. Synchronous previews or audio analysis may instead return
PREPARATION_REQUIRED: run detail.request unchanged, wait for completion and retry the command.
For an existing project, retain its head and use only media.add and the intended placements;
do not recreate its tracks. Remove the audio track/link steps for footage without sound.

## Simple trim, reorder and delivery

For a new cut, the populated snapshot can contain just the desired intervals: each clip's
source_in chooses its first source time, start is its timeline position, and duration is the
kept length. For reordered excerpts, use new clip IDs and one picture/sound link per excerpt,
with matching anchors. Set tracks.duration to the edited end. Asset duration always remains
the full source length. Keep times frame-aligned; exact fractions use {"num":1,"den":25}.
For an existing cut, read its head and revise selected clips with tracks.edit; a remove edit
requires clip_ids and links ("include" keeps linked picture/sound together).

For a straightforward MP4 delivery, $OUTPUT is a new .mp4 name and $INPUT_TRANSFER matches
the project. The h264_aac defaults are software H.264 High CRF 18 and stereo 48 kHz AAC
at a requested 320 kb/s. streams can be video for a silent source. Queued export includes
any required source preparation and verifies decoded output against the timeline.

<!-- example: export -->
~~~json
{"command":"job.start","request_id":"delivery-export","run":"export.run","arguments":{"project":{"project_id":"$PROJECT_ID"},"output":"$OUTPUT","profile":"h264_aac","streams":"audio_video","input_transfer":"$INPUT_TRANSFER"}}
~~~

<!-- example: wait-export -->
~~~json
{"command":"job.wait","job_id":"$JOB_ID","timeout_seconds":120}
~~~

Set $JOB_ID from job.start. Continue bounded waits while running; a failed job is not a
completed output. Use deliver-and-review when contact sheets, audio review or interchange
are needed. Review timing and relevant pictures/sound before claiming editorial correctness.

## Choose the next recipe

- Talking head through captions and delivery: recut-talking-head is self-contained; load it
  directly for that request. Its setup is only for a new project, so retain an existing head.
- Screen capture, B-roll or picture-in-picture: screen-tutorial, then deliver-and-review.
- Two synchronized cameras: interview-multicam, then deliver-and-review.
- Existing captions: captions; retain the same project and current revision.
- Feedback revision: session.get, make the smallest targeted session.apply, then preview
  the changed window. session.undo is another revision-checked edit, not a history deletion.

Load only the recipe needed for the request. The plugin exposes these as namespaced skills,
for example cutbolt:recut-talking-head.

## Recovery and boundaries

Use error retry, path, hint and detail; do not parse prose messages. For a stale revision,
read session.get, reconsider the edit against the new head, then submit the revised request.
For an uncertain saved edit, session.receipt with its request_id tells whether it committed.
For graphics.place use the inner edit request_id, not the enclosing job ID.
For an existing output, choose a new output name. A failed/cancelled job is not completion;
inspect its error before starting a replacement.

Windows and Linux support these editing, queue and speech workflows. Speech needs a separately
configured local runtime/model; a supplied transcript avoids recognition. Recording and
hardware decode currently require Windows. Do not promise those backends on Linux.
This plugin installs no models, fonts, media tools or engine binary, and starts no network server.
