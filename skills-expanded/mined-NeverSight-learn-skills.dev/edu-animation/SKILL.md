---
name: edu-animation
description: "Generate educational science explainer videos (60s-10min) using Manim + Edge TTS + FFmpeg. Optimized for popular science (通识科普): visual metaphor design, narrative animation patterns, and density-controlled storytelling. Triggers when user asks to create an educational video, explainer animation, science explainer, 科普视频, 科普动画, 教学视频, or 视频制作."
---

# Educational Animation Generator (Manim)

Generate short educational videos using Manim, Edge TTS, and FFmpeg.
Optimized for **通识科普** — making one concept crystal clear through visual metaphor.

## Prerequisites

- Python 3.10+ with Manim (`pip install manim`)
- System Cairo library (`brew install cairo` on macOS)
- `edge-tts` (`pip install edge-tts`)
- FFmpeg (`brew install ffmpeg`)
- Sox (`brew install sox`)
- Chinese font: PingFang SC (macOS built-in) or Source Han Sans SC

**Quick environment setup:**
```bash
mkdir -p /audio
[ -f /tmp/manim-env/bin/activate ] && source /tmp/manim-env/bin/activate
python3 -m pip install manim edge-tts -q 2>&1 | tail -1
```

## ⚠️ Context Recovery Protocol

Every conversation turn may follow a context loss. **Before doing ANY work:**

1. **Check** if `PROGRESS.md` exists in the project directory
   - If YES → Read it to determine current phase and last completed step
   - If NO → This is a new project, proceed to Phase 1
2. **Read supporting files** referenced in PROGRESS.md
3. **Verify** files listed in "Files Created" section actually exist on disk
4. **Resume** from the first unchecked item in the current phase

## Progress Tracking — Mandatory Protocol

Maintain `PROGRESS.md` using [progress-template.md](assets/progress-template.md). Create it at Phase 1 start.

### Checkpoint Rule

**Every time you complete a checkbox item, you MUST immediately:**
1. Mark the item `[x]` and add brief notes
2. Update the "Current State" section
3. Then proceed to the next item

### Phase Transition Gate

**Before starting any new Phase, you MUST:**
1. Verify ALL items in the previous phase are `[x]`
2. Update "Current Phase" to the new phase

## References

**Core design:**
- [design_system.py](assets/design_system.py) — Design tokens: colors, fonts, sizes, reusable components
- [scene_template.py](assets/scene_template.py) — Standard scene structure

**Popscience extensions:**
- [metaphor-patterns.md](references/metaphor-patterns.md) — Visual metaphor library & mapping protocol
- [narrative-patterns.md](references/narrative-patterns.md) — Narrative-level animation patterns (BuildUp, CauseEffect, Compare, Zoom)
- [popscience-structure.md](references/popscience-structure.md) — Short video structure (Hook→Setup→Core→Aha→Linger) & density control

**Visual & animation:**
- [style-guide.md](references/style-guide.md) — Color system, typography
- [animation-guide.md](references/animation-guide.md) — Animation patterns, timing, spring presets
- [visual-principles.md](references/visual-principles.md) — Composition, layout, information density
- [mobject-patterns.md](references/mobject-patterns.md) — Reusable Mobject component recipes

**Script & QA:**
- [script-and-narration.md](references/script-and-narration.md) — Script writing and TTS notes
- [storyboard-template.md](references/storyboard-template.md) — Storyboard format
- [quality-checklist.md](references/quality-checklist.md) — QA workflow and style check rules
- [requirements-guide.md](references/requirements-guide.md) — Requirements gathering questionnaire

## Workflow

### Phase 1: Requirements Gathering

Confirm with user:
- **Topic**: What concept to explain?
- **Audience**: Who is watching? (general public / students / experts)
- **Language**: Chinese / English / other?
- **Duration**: Short (60-90s), Medium (2-5min), or Long (5-10min)?
- **Key takeaway**: What one thing should the viewer be able to retell?

Create `PROGRESS.md` from [progress-template.md](assets/progress-template.md).
For detailed question templates, see [requirements-guide.md](references/requirements-guide.md).

### Phase 1.5: Core Metaphor Design ★

> This phase is the **soul** of a popscience video. A great metaphor decides the ceiling of the video.

**Goal**: For each key concept, find a visual metaphor that the audience instantly understands.

**Consult** [metaphor-patterns.md](references/metaphor-patterns.md) for the metaphor pattern library.

**For each core concept, produce:**

1. **Core metaphor** — what everyday thing to use as analogy
2. **Mapping table** — source domain ↔ target domain correspondences
3. **Boundary** — where the analogy breaks down, and how to handle it in narration

```
Example:
  Concept: mRNA translation
  Metaphor: Factory assembly line
  Mapping: mRNA = blueprint, ribosome = worker, amino acid = part, protein = product
  Boundary: Factories are designed; mRNA is evolved → mention in narration
```

**Output**: Save as `metaphor.md`

### Phase 2: Visual Narrative Design ★ (画面优先)

> **画面驱动, NOT 旁白驱动.** Design what the viewer SEES first, then write narration to complement it.
> The visuals should tell the story even without narration.

**Consult** [narrative-patterns.md](references/narrative-patterns.md) for narrative animation patterns.
**Consult** [popscience-structure.md](references/popscience-structure.md) for video structure and density control.

Tasks:
1. Choose video structure based on duration:
   - **60-90s**: Hook → Setup → Core Metaphor → Aha → Linger (see popscience-structure.md)
   - **2-10min**: Traditional multi-section with transitions
2. Design the visual story for each section — what the viewer sees
3. Assign a narrative animation pattern to each section (BuildUpAndReveal, CauseAndEffect, CompareAndContrast, ZoomIntoDetail, BeforeAndAfter)
4. Mark density level for each section (画面密度: low/medium/high, max on-screen elements)
5. Note which metaphor pattern drives each section

Use [storyboard-template.md](references/storyboard-template.md) for format.

**Output**: Save as `storyboard.md`

### Phase 2.5: Narration Writing (后于画面)

> Write narration to **complement** the visual story, not to drive it.
> Narration explains what visuals cannot convey; it should NOT describe what's already on screen.

Write complete narration for each scene:
1. **Full text** — every word to be spoken, with emphasis markers (`**bold**` for stress)
2. **Pause markers** — `[.]` short, `[..]` medium, `[PAUSE]` dramatic
3. **Educational markers** — `[THINK_PAUSE:3s]` (viewer question), `[MISCONCEPTION]` (common error to address), `[RECAP]` (review point)
4. **Self-review** — run through checklist in [script-and-narration.md](references/script-and-narration.md)

Quality gate: **Present the script to the user for approval before proceeding.**

**Output**: Save approved script as `script.md`

### Phase 3: Visual Design

> ⚠️ **Checkpoint Rule active**: Update PROGRESS.md after EACH item.

1. **Choose color palette** — Select from [design_system.py](assets/design_system.py) `T` class, or extend with topic-appropriate colors
2. **Copy design_system.py** — Copy to project directory for local import
3. **Create shared Mobject components** — Build reusable visual elements following [mobject-patterns.md](references/mobject-patterns.md)
4. **Design scene layouts** — Plan visual layers per scene following [visual-principles.md](references/visual-principles.md)

See [style-guide.md](references/style-guide.md) for complete visual standards.

### Phase 4: Animation Implementation

> ⚠️ **Checkpoint Rule active**: Update PROGRESS.md after EACH item.

1. **Initialize project**: `bash scripts/init-project.sh <project_name>`
2. **Generate TTS audio**: Use `scripts/generate_tts.py` (see below)
3. **Write Manim scene code** following [scene_template.py](assets/scene_template.py)
4. **Match `self.wait()` to audio durations** exactly

**TTS Generation:**
```bash
source /tmp/manim-env/bin/activate
python3 scripts/generate_tts.py --segments segments.json --output-dir <project>/audio/narration
```

Where `segments.json`:
```json
[
  {"id": "hook_1", "text": "天空为什么是蓝色的？"},
  {"id": "setup_1", "text": "太阳光看起来是白色的。"}
]
```

This generates mp3 files + `timeline.json` with exact durations for each segment.

**Audio integration in Manim:**
```python
self.add_sound(audio_path("hook_1"))
self.play(Write(title), run_time=1.5)
self.wait(dur("hook_1") - 1.5)  # fill remaining time
```

**Critical rules:**
- Import colors/fonts from `design_system.py` — NO hardcoded color hex strings
- Use `T.FONT` for all Chinese text
- Every element has exact coordinates — no ambiguity
- Use narrative animation patterns from [narrative-patterns.md](references/narrative-patterns.md) for scene-level animations
- Respect density limits from [popscience-structure.md](references/popscience-structure.md) per section
- See [animation-guide.md](references/animation-guide.md) for timing patterns

### Phase 5: QA & Review

#### Step 1: Code Scanning

```bash
source /tmp/manim-env/bin/activate
python3 scripts/style-scan.py <project_dir> --output /tmp/style-report.md
```

Checks: hardcoded colors, invalid font sizes, missing imports, unsafe zone violations.

#### Step 2: Keyframe Screenshot Review

```bash
bash scripts/render-keyframes.sh <project_dir> --output-dir /tmp/keyframes
```

Then analyze each screenshot for:
- Overall aesthetics, visual balance, color harmony
- Text readability, element overlap
- **Visual richness** — scenes with only text must be redesigned
- **Content fill ratio** — content ≤30% of canvas = "Thumbnail Syndrome"
- **Density compliance** — element count matches section's density rule

#### Step 3: Auto-Fix

Fix 🔴Critical first, then 🟡Important. Re-run scan after fixes.
Maximum 3 rounds. See [quality-checklist.md](references/quality-checklist.md).

#### Step 4: Final Render

```bash
bash scripts/render.sh <project_dir> --output <output.mp4> -qh
```

## Quality Checklist

- [ ] All scenes have narration matching TTS audio duration
- [ ] `self.wait()` durations match scene audio lengths
- [ ] Font set to `"PingFang SC"` for Chinese (via `T.FONT`)
- [ ] `camera.background_color` is dark (`T.BG`)
- [ ] Visual hierarchy is clear (size + color + position)
- [ ] Each concept has a visual metaphor — not just text
- [ ] Density rules respected per section
- [ ] Narrative animation patterns used for scene-level storytelling
- [ ] No hardcoded color hex strings outside `design_system.py`
- [ ] Final MP4 has both video + audio tracks synced

## Example

See [examples/sky_blue/](examples/sky_blue/) for a complete 46s popscience video:
- "Why is the sky blue?" explained via the **pinball machine metaphor**
- Structure: Hook → Setup → Core Metaphor → Aha → Linger
- 11 TTS segments, auto-synced audio, 1080p30
