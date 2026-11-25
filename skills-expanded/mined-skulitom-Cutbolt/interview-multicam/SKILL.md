---
name: interview-multicam
description: Assemble two synchronized local camera angles in Cutbolt with explicit camera cuts and one continuous master audio angle.
---

# Cut a two-camera interview

Use this when the angle timing is known. For unsynchronized recordings, obtain checked
offsets first with sync.inspect and review the match; do not assume their clocks align.
The example uses equal-duration, already-aligned sources at a shared native project clock.
Nested camera sequences currently need the reference FFV1/PCM profile. Eligible direct
compressed assets work on ordinary tracks but must be explicitly prepared for this nested path.

Start from the cutbolt setup recipe with camera A on linked v/a tracks. Read the saved
head to identify the placed clips. $OLD_CLIP_IDS is their actual
selection, $ASSET_A_ID the imported source ID, $DURATION the shared aligned interval.
Use listed cutbolt_* tools or cutbolt_run; replace all placeholders with actual values.

<!-- example: current -->
~~~json
{"command":"session.get","project_id":"$PROJECT_ID"}
~~~

Inspect camera B as $SOURCE. Use timeline.asset as $ASSET_B, ID as $ASSET_B_ID.
If its identity is absent, add bytes/sha256 from the inspection's identity.
If it needs normalization for nesting, queue media.conform and use that returned asset.

<!-- example: inspect -->
~~~json
{"command":"media.inspect","path":"$SOURCE"}
~~~

$SWITCH is a whole-frame switch within $DURATION. This single edit builds the two
angle sequences, fixes audio to A, replaces the initial placements and links the program
picture/sound. IDs here must be unused; adapt them when adding to an existing arrangement.

<!-- example: assemble -->
~~~json
{"command":"session.apply","project_id":"$PROJECT_ID","expected_revision":"$REVISION","request_id":"interview-assembly","operations":[
{"op":"media.add","asset":"$ASSET_B"},
{"op":"sequence.create","id":"cam-a","duration":"$DURATION"},
{"op":"sequence.edit","id":"cam-a","edit":{"op":"add","track":{"id":"video","kind":"video","clips":[],"enabled":true,"locked":false}}},
{"op":"sequence.edit","id":"cam-a","edit":{"op":"add","track":{"id":"audio","kind":"audio","clips":[],"enabled":true,"locked":false}}},
{"op":"sequence.edit","id":"cam-a","edit":{"op":"place","track_id":"video","collision":"reject","clip":{"id":"video","asset_id":"$ASSET_A_ID","start":0,"source_in":0,"duration":"$DURATION"}}},
{"op":"sequence.edit","id":"cam-a","edit":{"op":"place","track_id":"audio","collision":"reject","clip":{"id":"audio","asset_id":"$ASSET_A_ID","start":0,"source_in":0,"duration":"$DURATION"}}},
{"op":"sequence.create","id":"cam-b","duration":"$DURATION"},
{"op":"sequence.edit","id":"cam-b","edit":{"op":"add","track":{"id":"video","kind":"video","clips":[],"enabled":true,"locked":false}}},
{"op":"sequence.edit","id":"cam-b","edit":{"op":"add","track":{"id":"audio","kind":"audio","clips":[],"enabled":true,"locked":false}}},
{"op":"sequence.edit","id":"cam-b","edit":{"op":"place","track_id":"video","collision":"reject","clip":{"id":"video","asset_id":"$ASSET_B_ID","start":0,"source_in":0,"duration":"$DURATION"}}},
{"op":"sequence.edit","id":"cam-b","edit":{"op":"place","track_id":"audio","collision":"reject","clip":{"id":"audio","asset_id":"$ASSET_B_ID","start":0,"source_in":0,"duration":"$DURATION"}}},
{"op":"multicam.create","id":"program","group":{"duration":"$DURATION","locked":false,"angles":[{"id":"a","sequence_id":"cam-a","start":0,"duration":"$DURATION","source_in":0,"audio_in":0},{"id":"b","sequence_id":"cam-b","start":0,"duration":"$DURATION","source_in":0,"audio_in":0}],"cuts":[{"id":"first","at":0,"angle_id":"a"},{"id":"second","at":"$SWITCH","angle_id":"b"}],"audio":{"mode":"fixed","angle_id":"a"}}},
{"op":"tracks.edit","edit":{"op":"remove","clip_ids":"$OLD_CLIP_IDS","links":"include"}},
{"op":"tracks.edit","edit":{"op":"place","track_id":"v","collision":"reject","clip":{"id":"program-v","sequence_id":"program","start":0,"source_in":0,"duration":"$DURATION"}}},
{"op":"tracks.edit","edit":{"op":"place","track_id":"a","collision":"reject","clip":{"id":"program-a","sequence_id":"program","start":0,"source_in":0,"duration":"$DURATION"}}},
{"op":"tracks.edit","edit":{"op":"link","id":"interview-av","clip_ids":["program-v","program-a"]}}
]}
~~~

Keep the new revision. Deliver with deliver-and-review; verify the picture switches at
$SWITCH while A's sound remains continuous. For later changes, use multicam edits against
the saved program rather than flattening and rebuilding unrelated footage.

On stale revisions, refresh before replacing clips. A collision or locked selection requires
reconsidering that edit. A mismatched rate/size needs explicit preparation, not metadata edits.
The fixture proves two bounded synchronized reference sources, not automatic alignment of
arbitrary camera recordings or every compressed profile inside nested sequences.

This workflow runs on Windows and Linux with external FFmpeg/ffprobe. Speech recognition,
when needed, requires a separately configured local runtime and model. Recording and hardware
decode have no Linux backend. The plugin bundles no engine, fonts, models or media tools.
