---
name: video-highlight-distill
description: Turn a long video into a shorter highlights cut by transcribing it with mlx-whisper, having the model choose the best clips for a requested theme, validating those selections, and cutting plus concatenating the source video with ffmpeg. Use when the user wants highlight reels, best clips, distilled videos, or shorter edits from longer source footage.
---

# Video Highlight Distiller

Use this skill when the user wants a long video reduced to a shorter highlights edit around a clear theme or takeaway.

This skill currently supports macOS only because the transcription path depends on `mlx-whisper`. It is optimized for Apple Silicon machines using `mlx-whisper` with the `mlx-community/whisper-large-v3-turbo-q4` model. It keeps the model in a repo-local folder instead of relying on the default Hugging Face cache.

Before doing any setup or transcription, ask the user for:

- target final video length
- key points, theme, or takeaway to highlight
- content mode
- output style

Also confirm the source video path before starting any file-processing steps.

## Required inputs

Collect these inputs before selecting clips:

- target final video length
- highlight theme or main idea
- content mode
- output style
- source video path

At the beginning of the interaction, ask for the target final length, the key points or theme to highlight, the content mode, and the output style if they are not already provided. If the user does not provide a target length, ask for it before doing highlight selection. The clip-selection step needs a duration budget.

If the user does not specify a content mode, infer the closest fit from the source material and confirm it. Supported content modes:

- `vlog`
- `podcast/interview`
- `meeting/demo`
- `lecture/tutorial`
- `talking-head/social clip`

If the user does not specify an output style, ask for it or propose a reasonable default. Supported output styles:

- `trailer`
- `recap`
- `educational summary`
- `best moments`
- `decision log`

## Before running anything

1. Check whether dependencies are already available:
   - `python3`
   - `ffmpeg`
   - `ffprobe`
   - repo-local virtualenv at `.venv`
   - model files at `models/whisper-large-v3-turbo-q4`
2. If any dependency is missing, stop and ask the user for permission before:
   - creating or updating `.venv`
   - installing Python packages
   - downloading the Whisper model
3. If the model directory already contains the expected files, do not re-download it.
4. Do not assume the scripts are executable. Prefer explicit invocation. First resolve the skill directory from the supported local or global locations:

If you are running this skill inside a sandboxed environment, `mlx-whisper` may crash during transcription. In that case, request elevated permission and run the setup and Python scripts outside the sandbox so they can complete normally. This commonly affects Codex.

```bash
for candidate in \
  "$PWD/.agents/skills/video-highlight-distill" \
  "$PWD/.claude/skills/video-highlight-distill" \
  "$HOME/.agents/skills/video-highlight-distill" \
  "$HOME/.claude/skills/video-highlight-distill"
do
  if [ -d "$candidate" ]; then
    SKILL_DIR="$candidate"
    break
  fi
done

if [ -z "${SKILL_DIR:-}" ]; then
  echo "video-highlight-distill skill directory not found" >&2
  exit 1
fi

bash "$SKILL_DIR/scripts/setup.sh"
python "$SKILL_DIR/scripts/transcribe_video.py" ...
python "$SKILL_DIR/scripts/validate_highlights.py" ...
python "$SKILL_DIR/scripts/render_highlight_video.py" ...
```

## What to use

- `scripts/setup.sh`: create `.venv`, install Python dependencies, verify `ffmpeg`, and download the Whisper model into `models/`.
- `scripts/transcribe_video.py`: extract temporary audio, run transcription with timestamps, and write structured transcript artifacts.
- `scripts/validate_highlights.py`: validate model-authored `highlights.json` and normalize timestamps before rendering.
- `scripts/auto_select_highlights.py`: optional heuristic fallback that can generate a first-pass `highlights.json` when manual/model selection is unavailable.
- `scripts/render_highlight_video.py`: cut and concatenate the selected time ranges from the original source video.
- `references/selection-schema.md`: JSON schema and selection rubric for choosing strong highlight segments.

## Workflow

1. Run setup once:

```bash
bash "$SKILL_DIR/scripts/setup.sh"
```

2. Transcribe the source video:

```bash
python "$SKILL_DIR/scripts/transcribe_video.py" \
  --input /absolute/path/to/video.mp4 \
  --output-dir /absolute/path/to/run-artifacts
```

This writes:

- `transcript.json`: full Whisper response plus metadata
- `transcript.txt`: readable transcript with segment timestamps
- `selection_input.json`: compact transcript payload for highlight selection

3. Read the transcript artifacts and choose highlights as the editor/director.

Use `transcript.txt` as the primary editorial input. It is the best default input for the model because it is readable and already pairs each spoken section with a timestamp range. Use `selection_input.json` as the structured fallback when you need exact machine-readable timestamps or word-level detail.

The model should usually select multiple highlight sections that will later be stitched into one final video. Do not assume the output should be one single continuous block unless the source material truly supports that.

The model should decide which sections to keep based on theme, content mode, output style, narrative value, pacing, and continuity.

The default output should be a `highlights.draft.json` file that follows [`references/selection-schema.md`](./references/selection-schema.md).

Selection rules:

- Prefer multiple strong sections over forcing one large continuous section.
- Prefer complete thoughts and complete sentence endings over hitting the target length exactly.
- Treat `target final video length` as a soft budget, not a hard cap.
- If the last strong sentence starts before the target and ends shortly after it, keep the full sentence instead of cutting mid-sentence.
- Prefer a few coherent sections with setup and payoff over many tiny isolated sound bites.
- Keep segments non-overlapping and sorted.
- Adapt segment length and pacing to the requested content mode.
- Adapt the overall cut shape to the requested output style.

4. Pause for user confirmation before cutting any video.

After drafting the highlight selection, summarize the chosen segments for the user before validation or rendering. Include:

- the content mode and output style used for selection
- segment start and end timestamps
- a one- or two-sentence synopsis of what happens in each segment
- the estimated total runtime across all selected segments
- any notable tradeoffs, such as strong moments that were excluded to stay near the duration budget

Ask the user to confirm or request edits. Do not cut or concatenate video until the user approves the selected segments.

Save the draft as `highlights.draft.json`, share the summary with the user, and wait for confirmation.

5. Validate the approved highlights:

```bash
python "$SKILL_DIR/scripts/validate_highlights.py" \
  --selection-input /absolute/path/to/run-artifacts/selection_input.json \
  --highlights /absolute/path/to/run-artifacts/highlights.draft.json \
  --output /absolute/path/to/run-artifacts/highlights.json
```

If validation fails, fix the JSON or re-run the selection pass with corrected timestamps. The validator is deterministic and should be treated as the source of truth for shape, ordering, and timestamp bounds.

If the model cannot produce a useful draft, or the user explicitly asks for an automatic first pass, use the heuristic fallback:

```bash
python "$SKILL_DIR/scripts/auto_select_highlights.py" \
  --selection-input /absolute/path/to/run-artifacts/selection_input.json \
  --theme "用户要保留的重点主旨" \
  --target-seconds 90 \
  --output /absolute/path/to/run-artifacts/highlights.draft.json
```

After the user confirms an auto-generated first pass, validate that approved draft into `highlights.json`.

6. Review the validated `highlights.json` and adjust if needed. Follow [`references/selection-schema.md`](./references/selection-schema.md).

7. Render the final edit:

```bash
python "$SKILL_DIR/scripts/render_highlight_video.py" \
  --input /absolute/path/to/video.mp4 \
  --segments /absolute/path/to/highlights.json \
  --output /absolute/path/to/highlights.mp4
```

If setup created `.venv`, prefer the interpreter inside it:

```bash
.venv/bin/python "$SKILL_DIR/scripts/transcribe_video.py" ...
.venv/bin/python "$SKILL_DIR/scripts/validate_highlights.py" ...
.venv/bin/python "$SKILL_DIR/scripts/auto_select_highlights.py" ...
.venv/bin/python "$SKILL_DIR/scripts/render_highlight_video.py" ...
```

## Selection guidance

- Optimize for the user’s requested theme, not generic “interesting” content.
- Treat the target final video length as a soft budget for selection.
- Use model-directed selection as the default path. Use `auto_select_highlights.py` only as a fallback or rough first pass.
- Use `transcript.txt` as the primary input for model selection. Use `selection_input.json` to validate or refine timestamps, not as the default reading format.
- Default to selecting multiple coherent highlight sections that will be stitched together into the final edit.
- Prefer continuous sections with setup, payoff, and clean exits.
- Avoid selecting isolated one-line sound bites unless the user explicitly wants a trailer-style supercut.
- Keep segments non-overlapping and sorted.
- Merge small gaps when the surrounding context belongs together.
- If the transcript is noisy, inspect neighboring segments before finalizing timestamps.
- Do not end the final selected segment mid-sentence just to land exactly on the target duration.

### Content mode guidance

- `vlog`: prefer shorter, more dynamic sections, clearer emotional beats, and tighter pacing. Tolerate more cuts if momentum improves.
- `podcast/interview`: prefer longer conversational chunks that preserve question-answer context, setup, and payoff. Avoid chopping dialogue too aggressively.
- `meeting/demo`: prioritize decisions, action items, concrete updates, questions with answers, and notable product moments. Remove repetitive status chatter.
- `lecture/tutorial`: preserve explanatory continuity, examples, and conclusions. Keep enough setup that the retained sections still teach clearly.
- `talking-head/social clip`: favor strong hooks, concise points, and clean punchy endings. Prefer segments that can stand alone with minimal context.

### Output style guidance

- `trailer`: maximize hooks, surprise, momentum, and curiosity. Prefer shorter segments and stronger contrast between beats.
- `recap`: summarize the most important points in a balanced, easy-to-follow order. Prefer coherence over intensity.
- `educational summary`: optimize for clarity, teaching value, and logical sequencing. Keep explanations intact.
- `best moments`: prioritize the strongest standout sections even if they are not fully comprehensive.
- `decision log`: prioritize decisions made, reasoning, owners, and next steps. Favor completeness around decision points over entertainment value.

## Constraints

- `ffmpeg` and `ffprobe` must be available on `PATH`.
- This setup assumes `mlx-whisper` is appropriate for the current machine. For non-Apple-Silicon environments, the transcription helper likely needs a different backend.
- This skill is macOS-only for now because it depends on `mlx-whisper`. Future versions can add Windows support through a Windows-compatible Whisper backend or a transcription API path.
- Do not read `.env` files.
