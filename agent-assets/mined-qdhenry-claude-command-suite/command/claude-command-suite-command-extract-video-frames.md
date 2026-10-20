---
description: Extract frames and audio segments from video files for agent review
argument-hint: [path/to/video.mp4] [interval] [output-dir]
allowed-tools: Skill(extract-video-frames), Bash, Read, Glob
---

## Argument Validation

You have been given: `$ARGUMENTS`

Before invoking the skill, validate the arguments:

1. **Check a path was provided**: If `$ARGUMENTS` is empty or blank, ask the user for the video file path. Do not proceed without it.

2. **Check the file exists**: Verify the file at the given path exists using a quick check. If not found, report the error and stop.

3. **Warn on unusual extensions**: If the file extension is not one of `.mp4`, `.mov`, `.gif`, `.avi`, `.webm`, `.mkv`, warn the user that the format may not be supported, but allow them to proceed.

4. **Parse optional arguments**: The user may provide up to 3 arguments:
   - Arg 1 (required): Video file path
   - Arg 2 (optional): Interval in seconds (default: 1)
   - Arg 3 (optional): Output directory (default: `./frames`)

## Pre-Flight Checks

Before running extraction:

1. **Verify ffmpeg installed**: Run `which ffmpeg` -- if not found, tell the user to install with `brew install ffmpeg` and stop.

2. **Verify ffprobe installed**: Run `which ffprobe` -- if not found, tell the user it comes with ffmpeg: `brew install ffmpeg`.

3. **Check file size**: If the file is larger than 500MB, warn the user that extraction may take a while and confirm they want to proceed.

## Execution

Invoke the `extract-video-frames` skill with the validated arguments.

## Post-Execution Guidance

After extraction completes:

1. **Read the manifest**: Read `{output-dir}/manifest.json` and summarize what was extracted (frame count, audio segment count, whether audio was detected).

2. **Spot-check**: Read the first extracted frame (`frame_001.png`) to verify it's a valid image.

3. **Report results**: Show the user:
   - Total frames extracted
   - Whether audio was detected and how many segments were created
   - Output directory location
   - Manifest file location

4. **Suggest next steps**: Based on what was extracted, suggest:
   - "Pass this directory to a reviewing agent for visual analysis"
   - If audio exists: "Audio segments can be transcribed or analyzed by another agent"
   - "Read individual frames with the Read tool for visual inspection"

## Agent Handoff Template

If the user wants to hand off to a reviewing agent, provide this ready-to-use prompt:

```
Analyze the frames and audio extracted from the recording at {output-dir}.
Read {output-dir}/manifest.json for the full list of frames with timestamps and paired audio segments.
The full continuous audio track is at {output-dir}/full_audio.aac.
For each frame, describe what you see. For audio segments, note any speech or notable sounds.
```
