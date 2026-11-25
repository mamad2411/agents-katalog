---
name: deliver-and-review
description: Export a saved Cutbolt edit, inspect the delivered file and optionally create an OTIO handoff with explicit loss acknowledgement.
---

# Deliver a saved edit

Use $PROJECT_ID at its intended saved head. Choose a new $OUTPUT (for example delivery.mp4)
and an $INPUT_TRANSFER matching the project's working RGB declaration. Do not guess a
different transfer to make an export pass. Use listed cutbolt_* tools or cutbolt_run.
Examples are engine requests with placeholders replaced by actual values.

If the saved project does not exist yet, load the cutbolt setup skill first and use its
source inspection and initial linked snapshot. Do not guess setup operations from delivery
examples. Return here with the created project ID and revision.

## Export and wait

<!-- example: export -->
~~~json
{"command":"job.start","request_id":"delivery-export","run":"export.run","arguments":{"project":{"project_id":"$PROJECT_ID"},"output":"$OUTPUT","profile":"h264_aac","streams":"audio_video","input_transfer":"$INPUT_TRANSFER"}}
~~~

Use its ticket as $JOB_ID. A running job needs
another bounded wait; failed, interrupted or cancelled is not a successful delivery.

<!-- example: wait-export -->
~~~json
{"command":"job.wait","job_id":"$JOB_ID","timeout_seconds":120}
~~~

## Review the actual delivered file

Start review only after job.wait reports the export completed. Queuing export and review
together does not create a dependency; a review can run before the file exists.
The export receipt verifies the encoded file. Review adds contact sheets, timing checks
and audio measurements. Set $REVIEW_OUTPUT to a new directory name, such as review.
If the project has changed since export, use the exact exported revision in the project
reference rather than comparing the file with an unrelated new head.

<!-- example: review -->
~~~json
{"command":"job.start","request_id":"delivery-review","run":"export.review","arguments":{"path":"$OUTPUT","output":"$REVIEW_OUTPUT","project":{"project_id":"$PROJECT_ID"},"frames":4,"rendition_height":0}}
~~~

Use its new ticket as $JOB_ID.

<!-- example: wait-review -->
~~~json
{"command":"job.wait","job_id":"$JOB_ID","timeout_seconds":120}
~~~

Inside result, check timing.video.ok and timing.audio.ok, the review summary, image sheet and relevant
audio/playback. A passing duration check alone does not establish editorial quality.
The full measurements remain in review.json inside the review folder.

## Optional OTIO handoff

Run this section only when the user requests project interchange.

<!-- example: inspect-handoff -->
~~~json
{"command":"interchange.export.inspect","project":{"project_id":"$PROJECT_ID"}}
~~~

Read losses and required_acknowledgements. Only acknowledge losses acceptable for the
requested handoff; editing_links omits Cutbolt link groups, and declared_transfer omits
the RGB transfer declaration. Keep that declaration in delivery notes if accepting its loss.
Blocking losses
need another representation or explicit editing changes. $ACKNOWLEDGEMENTS is the accepted
list from that result, and $HANDOFF_OUTPUT is a new .otio filename.

<!-- example: handoff -->
~~~json
{"command":"interchange.export","project":{"project_id":"$PROJECT_ID"},"output":"$HANDOFF_OUTPUT","acknowledged_losses":"$ACKNOWLEDGEMENTS"}
~~~

Return the actual output paths and material limitations. Do not claim portable behavior for
another editor/build without a tested transfer. Preserve the source assets required by a handoff.
For OUTPUT_EXISTS choose a new path. For source changes, revalidate/rebind the intended media;
never bypass a content-identity mismatch. For job failure, follow retry/path/hint before retrying.

This workflow runs on Windows and Linux with external FFmpeg/ffprobe. Speech recognition,
when needed, requires a separately configured local runtime and model. Recording and hardware
decode have no Linux backend. The plugin bundles no engine, fonts, models or media tools.
