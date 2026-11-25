---
name: youtube-study-note
license: MIT
description: "Analyze YouTube or local videos for private learning notes: transcript-first summarization, timestamped evidence, authorized keyframe extraction with yt-dlp/ffmpeg, adversarial viewpoint analysis, and original local hand-drawn explainer visuals. Trigger when user asks to summarize, study, extract notes, capture key frames, critique viewpoints, or create visual learning reports from a video."
metadata:
  author: "dragon"
  version: "0.1.0"
---

# youtube-study-note Skill

## Core philosophy

Treat a video as a time-indexed evidence source, not just a blob of media.

1. Define the goal first: quick skim, full study note, critique, screenshots, or visual summary.
2. Prefer text timeline over raw visual analysis: subtitles > auto subtitles > local audio transcription > visual sampling.
3. Use screenshots only as evidence for important visual moments, not as decoration.
4. Default the HTML report to **core-content mode**: suppress creator intros, channel promotion, series setup, repeated disclaimers, and other edge context unless the user asks for a complete archive. Lead with the video's actionable core ideas.
5. Translate domain jargon before using it. For technical/finance/trading videos, add plain-language concept cards that explain what each term solves, not just what it is called.
   When a video is jargon-heavy, generate one built-in imagegen concept illustration per core term and render it inside that term's concept card.
   Put these concept cards before the overview and route sections so later summaries can use the terms without forcing the reader to guess them first.
6. Separate evidence from interpretation:
   - `[FACT]`: explicitly stated or shown in the video.
   - `[AUTHOR_VIEW]`: the creator's claim, opinion, framework, or recommendation.
   - `[MODEL_INFERENCE]`: inferred by the agent from transcript/frames.
   - `[COUNTERPOINT]`: adversarial or alternative explanation.
   - `[JUDGMENT]`: final synthesis with confidence.
7. Generate new explanatory images as original learning aids. Do not reproduce video frames with image generation.
8. Treat the default HTML as a **video replacement course pack**, not a summary page. The main reading path must teach the core ideas without requiring the learner to open the original video. Original links and screenshots are source evidence only.
9. For trading, finance, medicine, law, or other high-risk domains, add a safety layer: clarify that concepts are learning frameworks, list misuse risks, and require independent validation before action.

Default note packages are written under `~/Documents/video-note` unless the user passes `--out`. Each video gets one self-contained folder named from the video title:

```text
~/Documents/video-note/<video-title-slug>/
```

Treat that folder as the video learning package. Keep the transcript, JSON artifacts, Markdown report, HTML preview, screenshots, source transcript copies, and logs inside it so the package can be reopened or moved as one unit. For human browsing, also write chapter-level notes under:

```text
~/Documents/video-note/<video-title-slug>/chapters/<chapter-title-slug>/
```

Each chapter folder should include `chapter.md`, `chapter.json`, and any selected frames for that chapter.

## Boundaries

Default to **private-note safe mode**:

- Do not download full YouTube video unless the user says the content is their own, authorized, or they explicitly accept local private-study processing.
- First attempt metadata and subtitles/auto subtitles without downloading media.
- If no subtitles exist, extract audio only for transcription.
- Extract video frames only after a timestamped frame plan exists.
- Prefer short sections around selected timestamps over full-video downloads.
- Do not bypass paywalls, DRM, private access controls, or platform restrictions.
- Do not publish, redistribute, or claim ownership over extracted frames.
- For public sharing, use YouTube timestamp links/embeds instead of screenshots.
- Generated summary images must be original explainer visuals. Prefer a clear 小黑-style viewpoint map over decorative metaphors: pure white 16:9 canvas, thin black hand-drawn linework, one matte-black blob protagonist actively explaining the map, sparse colored handwritten Chinese labels, and no beige paper texture, shadows, gradients, dense cards, or copied video imagery. Use metaphors only when they make the actual video argument easier to understand.

## Preflight

Before running tools, check local dependencies:

```bash
node "<skill-dir>/scripts/check-deps.mjs"
```

Required:
- macOS Apple Silicon recommended
- Python 3.10+
- Node.js 20+
- yt-dlp
- ffmpeg / ffprobe

Optional:
- mlx-whisper Python package for local transcription when no subtitles exist
- Built-in `imagegen` skill/tool for raster learning illustrations.

## Recommended workflow

### Fast path: one-shot safe mode

Use `run` for the default private-note workflow. It prepares evidence, generates deterministic first-pass analysis files, renders the report, and writes run-review artifacts under `~/Documents/video-note/<video-title-slug>` when `--out` is omitted. YouTube URLs may use the `v=` video id only as a temporary bootstrap path before metadata is known; the final package should be rehomed to the title folder.

```bash
python3 "<skill-dir>/scripts/video_tool.py" run \
  --input "https://www.youtube.com/watch?v=VIDEO_ID"
```

If YouTube asks for bot/sign-in confirmation during metadata or subtitle extraction, retry with a local browser cookie source only for private local processing:

```bash
python3 "<skill-dir>/scripts/video_tool.py" run \
  --input "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies-from-browser chrome
```

Or use an exported Netscape-format cookies file:

```bash
python3 "<skill-dir>/scripts/video_tool.py" run \
  --input "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies "/path/to/youtube-cookies.txt"
```

The helper passes `--js-runtimes node` to yt-dlp by default because modern YouTube extraction may require a JavaScript runtime.
Use `--tool-timeout 120` or lower when diagnosing a browser-cookie or network stall.

For an existing transcript file, avoid media access entirely:

```bash
python3 "<skill-dir>/scripts/video_tool.py" run \
  --input "https://www.youtube.com/watch?v=VIDEO_ID" \
  --transcript "/path/to/transcript.json" \
  --title "Original video title"
```

When YouTube has no caption track but a reviewed external transcript is available, pass both `--input` and `--transcript`. The note package keeps the YouTube URL/ID for timestamp links while avoiding media download.

The one-shot safe-mode output includes:

- `metadata.json`
- `transcript.json`
- `transcript.md`
- `summary.json`
- `debate.json`
- `frame_plan.json`
- `lesson_units.json`
- `visual_storyboard.json`
- `assessment.json`
- `asset_health.json`
- `replacement_review.json`
- `image_prompts.json`
- `generated_images.json`
- `generated/` after running the image step
- `chapters/` with one folder per chapter title
- `run_review.json`
- `notes_for_next_run.md`
- `report.md`
- `report.html`
- `index.html`
- `frames/`
- `source_transcripts/`
- `logs/`

Safe mode does not save public-video frames. Use timestamp links in `frame_plan.json` and `report.md` unless the user explicitly authorizes local frame extraction.

### 1. Prepare evidence packet

Use `prepare` to collect metadata and transcript.

```bash
python3 "<skill-dir>/scripts/video_tool.py" prepare \
  --input "https://www.youtube.com/watch?v=VIDEO_ID" \
  --languages "zh.*,en.*" \
  --whisper-model "mlx-community/whisper-large-v3-turbo"
```

The tool writes:

- `metadata.json`
- `transcript.json`
- `transcript.md`
- `agent_packet.json`
- `logs/prepare.log`

### 2. Agent analysis

Run the deterministic first-pass analyzer, or have the agent read `agent_packet.json` and `transcript.md` for deeper model-assisted analysis.

```bash
python3 "<skill-dir>/scripts/video_tool.py" analyze \
  --out "~/Documents/video-note/VIDEO_ID"
```

- `summary.json`
- `debate.json`
- `frame_plan.json`
- `image_prompts.json`

Follow the schemas in `references/schemas.md`.

Frame plan rules:

- Choose 3-12 timestamps maximum.
- Prefer frames where visual content adds meaning: diagrams, slides, whiteboard, code, charts, UI operations, formulas, or final summary cards.
- For each timestamp, include `reason`, `topic`, `evidence_quote`, and `need_frame`.
- If a segment is pure talking head and no visual evidence is needed, set `need_frame: false`.

### 3. Extract authorized frames

Only run this when user allows local frame extraction.

```bash
python3 "<skill-dir>/scripts/video_tool.py" frames \
  --input "https://www.youtube.com/watch?v=VIDEO_ID" \
  --out "~/Documents/video-note/VIDEO_ID" \
  --frame-plan "~/Documents/video-note/VIDEO_ID/frame_plan.json" \
  --mode authorized
```

The tool extracts candidates at `t-2`, `t`, `t+2`, then creates `frames/index.json` for agent review.

### 4. Frame review

For each candidate group, choose the best frame or discard all. Write:

- `frames/selected_frames.json`

Keep only frames that improve the core content. Discard frames for intros, self-promotion, creator biography, and transition filler unless they contain an essential concept.

### 5. Generate original hand-drawn summary images

The analyzer creates `image_prompts.json`, including overall viewpoint maps and concept-level illustrations for extracted jargon. Use the built-in `imagegen` skill/tool to generate each prompt as a real bitmap image. Built-in imagegen saves under `$CODEX_HOME/generated_images/...`; copy or register those final images into the video package before rendering.

After built-in imagegen returns image files, register them:

```bash
python3 "<skill-dir>/scripts/video_tool.py" image \
  --out "~/Documents/video-note/VIDEO_ID" \
  --image-prompts "~/Documents/video-note/VIDEO_ID/image_prompts.json" \
  --asset sketch_map_01="~/.codex/generated_images/.../first.png" \
  --asset review_card_01="~/.codex/generated_images/.../second.png" \
  --render
```

The image step writes:

- `generated/sketch_map_01.png`
- `generated/review_card_01.png`
- `generated_images.json`

These are real raster image files rendered in `index.html` and `report.md`, not prompts for the user to copy.
Keep these visuals as built-in imagegen drawings rather than SVG approximations. The default style should feel like a 小黑 hand-drawn explainer: pure white background, 16:9 landscape, lots of whitespace, and legible short labels. Concept images must teach one term at a time; viewpoint maps should expose the video's core argument, objections, and practical takeaway. Do not make abstract machinery if it hides the meaning.

### 6. Render report

```bash
python3 "<skill-dir>/scripts/video_tool.py" render \
  --out "~/Documents/video-note/VIDEO_ID"
```

Output:

- `report.md`
- `report.html`
- `index.html`

Open `index.html` first for the interactive study view. The HTML is a standalone local page that uses only files from the same video folder. It should include:

- a 5-minute route, plain-language concept course cards, and the core learning path before chapter details
- chapter-level screenshots from `frames/selected_frames.json`, aligned to the chapter they support
- chapter-level Agent judgment with four fields: useful point, misuse, verification condition, and personal handling
- all-video controversy synthesis before chapter-by-chapter author/skeptic/judge comparison
- source timestamp links for evidence checking, not as the main learning path
- scored review questions with answers and explanations, plus a local scratchpad saved in the browser
- a replacement score from `replacement_review.json`; below 85 means the package is useful but should not be described as a complete replacement for the video

## Adversarial analysis pattern

Always run four passes, even if implemented by one model:

1. `Summarizer`: explain the author fairly.
2. `Skeptic`: identify missing evidence, ambiguity, bias, weak causality, survivorship bias, or overclaiming.
3. `Counter-Analyst`: reconstruct the strongest alternative interpretation.
4. `Judge`: synthesize what is useful, what is questionable, what needs verification, and how confident the agent is.

Use timestamp evidence for every major claim.

## Self-optimization loop

After each successful run, update local experience only with verified observations:

```bash
python3 "<skill-dir>/scripts/video_tool.py" remember \
  --out "./video_notes/VIDEO_ID" \
  --source "youtube.com" \
  --note "Auto captions for this channel were noisy; mlx-whisper large-v3-turbo performed better for mixed Chinese/English audio."
```

Write experience under `references/video-patterns/`. Do not store private transcript excerpts there unless the user explicitly wants that.

## References index

- `references/boundaries.md`: legal/safety/product boundaries for private notes.
- `references/schemas.md`: JSON schemas for summary, debate, frame plan, image prompts.
- `references/prompts.md`: reusable prompts for summarization, critique, frame selection, and image generation.
- `references/video-patterns/`: local verified experience, updated incrementally.
