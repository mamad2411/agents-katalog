---
name: image-context-manager
description: Manage screenshots and visual assets in long agent tasks. Use when reading images, finding UI targets, checking visual state or quality, comparing versions, or when screenshots accumulate. Calls local tools for compression, verified crops, result storage and original recall, and isolates visual work in a native subagent.
---

# Image Context Manager

Use the bundled `scripts/icm.py` with `python3` (absolute path relative to this skill directory). It launches the Python environment saved at installation. All commands return JSON. Put `--workspace /absolute/private/task-directory` **before** the subcommand. Use a separate workspace for each task; do not commit image stores or `.runtime.json`.

## Choose what the next step needs

1. Prefer page text, accessibility information or command output. Do not capture a screenshot unless visual information is needed.
2. Before opening a new image in the main context, register it:
   `add /absolute/image.png --id draft1 --task read_content --version v1 --stage draft`.
   A changed image or version gets a new ID. Repeat `--task` for multiple purposes.
3. Classify the purpose: `read_content`, `locate_target`, `recognize_state`, `understand_relations`, `judge_visual_quality`, `compare_changes`, or `extract_action_information`.
4. Choose dynamically. Quality, comparison, relationships, action coordinates and uncertain verification need original pixels. Use `prepare ID` for a conservative choice. For suitable reading/state tasks, explicitly permit resizing/JPEG with `prepare ID --allow-lossy --edge 1280 --quality 85`; inspect small text before relying on it. `--max-bytes` reports whether the actual output meets the limit; it does not guarantee a size or retry automatically.
5. If only a known region matters, use `prepare ID --mode crop --roi x0 y0 x1 y1 --region-verified`. Coordinates are pixels in the EXIF-oriented original. Verify the region first; never invent a box to satisfy the command. Use returned origin/scale when mapping a derived image back. Cropping keeps native resolution and transparency.
6. Prefer `delegate ID [ID...] --goal "specific inspection"`, then invoke the host's native `icm-visual-worker` subagent with the returned handoff file. Let the worker open the original files in its own context and return text only. **The CLI prepares the handoff; it does not launch the worker.** If subagents are unavailable, say so; use a necessary prepared image directly without claiming isolation.
7. Store a source-bound result using `record ID --file /absolute/result.json`. Copy `id`, `source_sha256`, `version`, `stage` from `list`; include `producer`, a nonempty `fields` object of text values, and boolean `verified`/`sufficient`. Verify actual details before setting these booleans. OCR/extraction/summary is performed by the existing agent; no OCR engine or model API is bundled. Source binding verifies identity, not semantic truth. Conflicting results keep the image protected; use a new ID after resolving uncertainty.
8. After the task is done: `state ID completed`. Only a completed, verified, sufficient result can become text via `prepare ID`. Use `list` to retrieve saved findings without loading pixels. For checking or comparing again, change tasks/state first; `recall ID` returns the integrity-checked original and protects it until the lifecycle is updated.

## Boundaries

Never delete original files to reduce context. Never silently discard uncertainty, failed recalls or version conflicts. Existing host conversation history is not editable by this skill: it reduces future image input and separates new visual work. The Python `HistoricalImages` integration is an additional option only for applications that own request assembly. This skill does not install a transport proxy or fix WebSocket errors. Local byte reductions do not prove reduced host request bytes, tokens, latency or cost. Report performance only after complete matched multi-turn measurements, including retries/fallbacks and output quality.
