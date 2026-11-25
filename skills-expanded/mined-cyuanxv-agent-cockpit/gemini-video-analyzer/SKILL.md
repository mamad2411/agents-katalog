---
name: gemini-video-analyzer
description: Analyze local video files with Gemini API native video understanding. Use when Codex needs to summarize, inspect, timestamp, batch-screen, or produce structured JSON and Markdown reports for local .mp4, .mov, .m4v, or .webm video files using Gemini. Supports model discovery, 24-hour lazy model refresh, model probing, cost estimation, inline video transfer for small files, File API upload for larger files, JSON validation, Markdown rendering, and reviewable timestamp evidence.
---

# Gemini Video Analyzer

Analyze local video files with Gemini API while keeping Codex as the local harness. The main contract is: fixed JSON first, Markdown report second, and timestamp evidence that a human can replay.

## Inputs

Ask for a local video path if the user did not provide one. Accept only `.mp4`, `.mov`, `.m4v`, and `.webm`.

Default analysis goal:
- Chinese output.
- One-sentence conclusion.
- Content summary.
- Timeline with reviewable timestamps.
- Key visuals, audio, subtitles, narration, UI flow, and actions.
- Key moments, editing suggestions, follow-up suggestions, and uncertainties.

## Procedure

1. Verify that the video file exists.
2. Tell the user that the video will be uploaded to Gemini API for analysis.
3. Run a cost estimate before analysis when the user has not already approved the run:

   ```bash
   python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py estimate "<video_path>"
   ```

4. Analyze with the recommended model and explicit confirmation:

   ```bash
   python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py analyze "<video_path>" --goal "<analysis_goal>"
   ```

   For non-interactive approved runs, pass `--yes`.

5. If the user names a model, pass it explicitly:

   ```bash
   python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py analyze "<video_path>" --model gemini-3.5-flash --goal "<analysis_goal>" --yes
   ```

6. Transfer mode defaults to `auto`: videos up to 20 MB use inline Gemini content parts; larger videos use Gemini Files API. Override only when needed:

   ```bash
   python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py analyze "<video_path>" --transport inline --yes
   python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py analyze "<video_path>" --transport files --yes
   ```

7. Read the printed run directory. Validate it if needed:

   ```bash
   python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py validate "<run_dir>"
   ```

8. Return the generated `report.md` and `analysis.json` paths plus a concise summary.

## Model Operations

Use these commands when the user asks about available models or routing:

```bash
python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py models
python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py models --refresh
python3 skills/gemini-video-analyzer/scripts/gemini_video_analyze.py models --refresh --probe
```

The script performs lazy model refresh before analysis. It uses the cached model list unless the cache is missing or older than 24 hours. It does not run a background timer.

## Output Contract

Normal analysis creates a run directory under `~/Downloads/gemini-video-analyzer-outputs/` containing:

- `metadata.json`
- `models-cache-snapshot.json`
- `cost-estimate.json`
- `prompt.txt`
- `file-api-response.json` and `file-api-active.json` when `--transport files` is used
- `raw-response.json`
- `analysis.json`
- `report.md`
- `run.log`

For schema details, read `references/output-schema.md`. For routing and cost details, read `references/model-routing.md`. For prompt variants, read `references/prompt-templates.md`. For validation, read `references/validation.md`.

## Safety

- Do not print `GEMINI_API_KEY`.
- Read `GEMINI_API_KEY` from the environment or the workspace root `.env`.
- Do not pass quota project, billing project, requester project, or "发起请求项目" parameters or headers.
- Do not delete or overwrite the source video.
- Do not upload the video to public locations.
- Keep generated outputs local.
- By default the script deletes the uploaded Gemini File API object after a `--transport files` run; pass `--keep-uploaded` only when the user asks to reuse the same uploaded file.
