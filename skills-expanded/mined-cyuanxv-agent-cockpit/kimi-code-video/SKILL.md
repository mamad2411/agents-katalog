---
name: kimi-code-video
description: Use local Kimi-Code from Codex to analyze video files, producing Chinese summaries, scene timelines, key moments, and editing suggestions while keeping Codex as the main harness.
---

# Kimi-Code Video

Use this skill when the user asks Codex to analyze a local video with Kimi-Code, asks for video summaries, scene or shot timelines, key moments, editing suggestions, or explicitly mentions Kimi-Code's video ability.

## Inputs

Ask for a local video path if the user did not provide one. Accept common video files such as `.mp4`, `.mov`, `.m4v`, and `.webm`.

Default analysis goal:
- Chinese Markdown output.
- One-sentence conclusion.
- Content summary.
- Scene/timeline breakdown with timestamps when possible.
- Key visuals, people, actions, subtitles, narration, and UI flow.
- Editing suggestions and follow-up processing ideas.
- Uncertainties, separated from observed facts.

## Procedure

1. Verify that the video file exists before running Kimi.
2. Run `kimi --version` and `kimi doctor` if Kimi-Code availability is uncertain.
3. If `kimi -p` fails with `No model configured`, stop and tell the user to run `kimi login`, then `kimi -p "ping" --output-format text`.
4. Prefer the direct path first:

   ```bash
   skills/kimi-code-video/scripts/kimi_video_analyze.sh "<video_path>" "<analysis_goal>"
   ```

5. If Kimi does not actually inspect the video and only treats the path as text, retry with extracted frames:

   ```bash
   skills/kimi-code-video/scripts/kimi_video_analyze.sh --mode frames "<video_path>" "<analysis_goal>"
   ```

6. Read the output file path printed by the script. Summarize the result for the user and point to the full output file.

## Output Contract

For normal analysis, return the generated Markdown file path plus a concise summary. For structured downstream handoff, follow `references/output-format.md`.

## Safety

- Do not delete or overwrite the source video.
- Do not upload the video to public locations.
- Do not run Kimi with `--yolo`.
- Do not start `kimi web` with `--dangerous-bypass-auth`.
- Keep generated outputs local.
