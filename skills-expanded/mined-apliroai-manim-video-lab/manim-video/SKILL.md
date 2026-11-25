---
name: manim-video
description: "Create production-quality Manim Community Edition explainer videos, math animations, algorithm visualizations, paper/PDF explainers, data stories, and architecture diagrams. Use when a user asks for 3Blue1Brown-style programmatic animation, Manim scene planning/coding/rendering, Docker-based Manim setup, or troubleshooting Manim renders."
---

# Manim Video Lab Production Pipeline

## Scope

Create 3Blue1Brown-style explainer videos, algorithm visualizations, equation derivations, architecture diagrams, research-paper explainers, and data stories using Manim Community Edition.

## Attribution

Use this skill as an independent workflow helper built with gratitude for Manim, the open-source mathematical animation engine originally written by Grant Sanderson and now maintained by the Manim Community. Do not imply affiliation with or endorsement by Grant Sanderson, 3Blue1Brown, or the Manim Community.

## Creative Standard

This is educational cinema. Every frame teaches. Every animation reveals structure.

**Before writing a single line of code**, articulate the narrative arc. What misconception does this correct? What is the "aha moment"? What visual story takes the viewer from confusion to understanding? The user's prompt is a starting point — interpret it with pedagogical ambition.

**Geometry before algebra.** Show the shape first, the equation second. Visual memory encodes faster than symbolic memory. When the viewer sees the geometric pattern before the formula, the equation feels earned.

**Design for first-render excellence.** The draft should be visually clear and aesthetically cohesive before review. Use the bounded review loop to verify rendered evidence and make targeted fixes, not to rescue vague planning.

**Opacity layering directs attention.** Never show everything at full brightness. Primary elements at 1.0, contextual elements at 0.4, structural elements (axes, grids) at 0.15. The brain processes visual salience in layers.

**Breathing room.** Every animation needs `self.wait()` after it. The viewer needs time to absorb what just appeared. Never rush from one animation to the next. A 2-second pause after a key reveal is never wasted.

**Retention rhythm.** Something meaningful changes every 1-3 seconds, but only one thing owns attention at a time. No static span over ~4 seconds without a declared reason; no metronomic identical timings; one ~1s breath before each key reveal; finished results shrink to a corner instead of vanishing. The quantified rules and audit live in `references/attention-and-retention.md`.

**Cohesive visual language.** All scenes share a color palette, consistent typography sizing, matching animation speeds. A technically correct video where every scene uses random different colors is an aesthetic failure.

For premium, dynamic, research-teaser-style output, read `references/director-packet.md` before coding, then run `references/preflight-gates.md`. Use `references/cinematic-directing.md` with `references/attention-and-retention.md`, choose a scene architecture from `references/source-backed-patterns.md`, and apply `references/codegen-craft.md` while writing Manim code. For algorithm or data-structure content add `references/algorithm-choreography.md`; finish with `references/visual-polish.md` once attention, pacing, and hierarchy are solved. Together they define the directing contract, stable scaffolds, semantic beats, retention rhythm, protected overlays, attention handoffs, live dependency motion, logical motion, source anchors, deterministic gates, implementation craft, and final hero landings.

## Prerequisites

Docker is the default runtime. Run `scripts/setup.sh` on macOS/Linux/WSL/Git Bash or `scripts\setup.ps1` on Windows PowerShell from this skill folder to build and verify the local `manim-video-runtime:v0.20.1` image from the pinned `manimcommunity/manim:v0.20.1` base plus ffmpeg. The host only needs Docker plus Bash or PowerShell; Python, Manim, LaTeX, and ffmpeg run inside the container. Reference docs tested against Manim CE v0.20.1.

Use local `manim`, `pdflatex`, or `ffmpeg` only when the user explicitly requests a host install or Docker is unavailable.

## Portable Skill Contract

This is an Agent Skills-compatible folder, not a Codex-only folder. The portable core is:

```
SKILL.md + scripts/ + references/
```

Keep this folder together when installing into any agent or tool:

```
manim-video/
  Dockerfile
  SKILL.md
  scripts/      # Bash and PowerShell Docker wrappers
  references/
  agents/        # optional OpenAI/Codex UI metadata; safe for other tools to ignore
```

Install the folder as `manim-video` so the directory name matches `name: manim-video` in this file.

For cross-client project installs, copy the whole folder to `.agents/skills/manim-video/`. For user-level cross-client installs, use `~/.agents/skills/manim-video/`. For Claude Code, `.claude/skills/manim-video/` and `~/.claude/skills/manim-video/` are also valid. For Codex, use `${CODEX_HOME:-$HOME/.codex}/skills/manim-video/`. For Antigravity, OpenCode, VS Code/Copilot, Goose, Amp, and similar tools, use `.agents/skills/` when supported or the tool's configured skills directory.

Agents should read `SKILL.md`, load only the relevant `references/*.md` files, and run the Docker wrappers from the project directory.

Render wrapper:

```bash
/path/to/manim-video/scripts/manim.sh -ql script.py Scene1
```

Windows PowerShell:

```powershell
& "C:\path\to\manim-video\scripts\manim.ps1" -ql script.py Scene1
```

ffmpeg wrapper:

```bash
mkdir -p outputs
/path/to/manim-video/scripts/ffmpeg.sh -y -f concat -safe 0 -i concat.txt -c copy outputs/final.mp4
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force outputs
& "C:\path\to\manim-video\scripts\ffmpeg.ps1" -y -f concat -safe 0 -i concat.txt -c copy outputs/final.mp4
```

The wrappers mount the current project directory into the container at `/manim`. Set `MANIM_PROJECT_DIR=/path/to/project` or `$env:MANIM_PROJECT_DIR = "C:\path\to\project"` when the shell cannot run from the project directory. Set `MANIM_BASE_IMAGE=manimcommunity/manim:stable` and rerun `scripts/setup.sh --rebuild` or set `$env:MANIM_BASE_IMAGE = "manimcommunity/manim:stable"` and run `scripts\setup.ps1 -Rebuild` to rebuild from the latest Manim release. Set `MANIM_DOCKER_IMAGE=your-image` to use a fully custom runtime.

The Bash and PowerShell wrappers accept the same Manim/ffmpeg arguments. For Windows, map later `/path/to/manim-video/scripts/*.sh` examples to `C:\path\to\manim-video\scripts\*.ps1`.

## Modes

| Mode | Input | Output | Reference |
|------|-------|--------|-----------|
| **Concept explainer** | Topic/concept | Animated explanation with geometric intuition | `references/scene-planning.md` |
| **Equation derivation** | Math expressions | Step-by-step animated proof | `references/equations.md` |
| **Algorithm visualization** | Algorithm description | Step-by-step execution with data structures | `references/algorithm-choreography.md` |
| **Data story** | Data/metrics | Animated charts, comparisons, counters | `references/graphs-and-data.md` |
| **Architecture diagram** | System description | Components building up with connections | `references/mobjects.md` |
| **Paper explainer** | Research paper or attached PDF | Source-grounded claim, method, evidence, visuals, and limitations animated | `references/paper-explainer.md` |
| **3D visualization** | 3D concept | Rotating surfaces, parametric curves, spatial geometry | `references/camera-and-3d.md` |

## Stack

Single Python script per project. Docker supplies the render stack. No browser, Node.js, GPU, or host LaTeX install required.

| Layer | Tool | Purpose |
|-------|------|---------|
| Core | Manim Community Edition in Docker | Scene rendering, animation engine |
| Math | Container LaTeX | Equation rendering via `MathTex` |
| Video I/O | Container ffmpeg | Scene stitching, format conversion, audio muxing |
| TTS | ElevenLabs / Qwen3-TTS (optional) | Narration voiceover |

## Pipeline

```
PLAN --> GATE --> CODE --> RENDER --> STITCH --> AUDIO (optional) --> REVIEW
```

1. **PLAN** — Write `plan.md` with narrative arc, continuity architecture, scene list, visual elements, color palette, voiceover script, and a director packet for complex scenes
2. **GATE** — For ambitious output, run the contract, prompt-preservation, LMIR, operator, camera/pacing, assertion, and source-anchor gates in `references/preflight-gates.md`; fix `plan.md` before coding if gates fail
3. **CODE** — Write `script.py` with one class per justified scene segment, not one class per beat; keep each class independently renderable and source-anchored to the packet; for premium scenes, apply `references/codegen-craft.md`
4. **RENDER** — `/path/to/manim-video/scripts/manim.sh -ql script.py Scene1 Scene2 ...` or `scripts\manim.ps1 -ql script.py Scene1 Scene2 ...` for draft, `-qh` for production
5. **STITCH** — `/path/to/manim-video/scripts/ffmpeg.sh` or `scripts\ffmpeg.ps1` concat of scene clips into `outputs/final.mp4`
6. **AUDIO** (optional) — Add voiceover and/or background music via the ffmpeg wrapper. See `references/rendering.md`
7. **REVIEW** — Run the feedback loop in `references/review-loop.md`: direct video review when available, or ffmpeg frame extraction fallback

## Project Structure

```
project-name/
  plan.md                # Narrative arc, scene breakdown
  script.py              # All scenes in one file
  concat.txt             # Temporary ffmpeg scene list
  outputs/               # Final/shareable exports
    final.mp4
  media/                 # Auto-generated by Manim
    videos/script/480p15/
```

### Artifact Hygiene

Docker runs with `--rm`, so the container is removed after each wrapper command. Files written under the mounted `/manim` directory are local project files and persist after Docker exits.

Keep generated files organized:
- Put final/shareable videos under `outputs/`, not loose in the project root.
- After an accepted single-scene render, copy the chosen Manim render from `media/videos/...` into `outputs/` and present that `outputs/...` file as the primary final path.
- Treat `media/` as Manim's generated render cache/output, not the canonical final location; it can be deleted and regenerated.
- Treat `review-frames/`, `concat.txt`, and `audio_concat.txt` as temporary review/stitching artifacts. Remove or overwrite them before final handoff so stale review frames do not accumulate.
- Do not copy videos into hidden tool or agent cache directories such as `.gemini/.../brain`, `.codex/`, `.agents/`, or UI-specific artifact stores unless the host tool explicitly requires an embedded artifact. If a host tool creates a secondary artifact copy, disclose it as secondary and keep `outputs/` as the user-facing source of truth.
- Do not delete `script.py`, `plan.md`, source assets, narration files, or final files under `outputs/` unless the user explicitly asks.

## Creative Direction

### Color Palettes

| Palette | Background | Primary | Secondary | Accent | Use case |
|---------|-----------|---------|-----------|--------|----------|
| **Classic 3B1B** | `#1C1C1C` | `#58C4DD` (BLUE) | `#83C167` (GREEN) | `#FFFF00` (YELLOW) | General math/CS |
| **Warm academic** | `#2D2B55` | `#FF6B6B` | `#FFD93D` | `#6BCB77` | Approachable |
| **Neon tech** | `#0A0A0A` | `#00F5FF` | `#FF00FF` | `#39FF14` | Systems, architecture |
| **Monochrome** | `#1A1A2E` | `#EAEAEA` | `#888888` | `#FFFFFF` | Minimalist |
| **Colorblind-safe (Wong)** | `#1C1C1C` | `#56B4E9` | `#009E73` | `#E69F00` | Data-heavy, accessibility-first |

### Animation Speed

| Context | run_time | self.wait() after |
|---------|----------|-------------------|
| Opening hook reveal | 1.5s | 1.0s |
| Routine derivation/loop step | 1.0-1.5s | 0.6-1.0s |
| Key equation reveal | 2.0s | 2.0s |
| Transform/morph | 1.5s | 1.5s |
| Supporting label | 0.8s | 0.5s |
| FadeOut cleanup | 0.5s | 0.3s |
| "Aha moment" reveal | 2.5s | 3.0s |

These are tiers, not a metronome: mark the few landing moments per scene and give them the slow tier; keep routine steps brisk (`references/attention-and-retention.md`).

### Typography Scale

| Role | Font size | Usage |
|------|-----------|-------|
| Title | 48 | Scene titles, opening text |
| Heading | 36 | Section headers within a scene |
| Body | 30 | Explanatory text |
| Label | 24 | Annotations, axis labels |
| Caption | 20 | Subtitles, fine print |

### Fonts

Prefer monospace fonts for labels, captions, code, and body text. Manim's Pango renderer can produce inconsistent proportional-font kerning in Docker, especially at small sizes. See `references/visual-design.md` for full recommendations.

```python
MONO = "Noto Sans Mono"  # Docker-safe; define once at top of file

Text("Fourier Series", font_size=48, font=MONO, weight=BOLD)  # title
Text("n=1: sin(x)", font_size=20, font=MONO)                  # labels
MathTex(r"\nabla L")                                            # math (uses LaTeX)
```

Minimum `font_size=18` for readability.

### Purposeful Continuity And Variation

Do not randomize style just to avoid sameness. Preserve semantic color, spatial roles, and motion vocabulary across connected scenes. Vary only when the meaning changes:
- **Color** changes only when the concept or role changes; the same concept keeps the same color.
- **Layout** changes only for a new scene family, comparison, density failure, or semantic reset.
- **Animation entry** matches the visual function: `Create` for geometry, `Transform*` for continuity, `FadeIn` for supporting context, `Write` for notation/text.
- **Visual weight** follows the beat: quiet setup, active mechanism, readable payoff.

## Workflow

### Step 1: Plan (plan.md)

Before any code, write `plan.md`. See `references/scene-planning.md` for the comprehensive template. Decide continuity architecture early: use one continuous canvas by default, and split scenes only with a specific reason and state handoff. For ambitious or "world-class" animations, also use `references/director-packet.md`, `references/preflight-gates.md`, `references/cinematic-directing.md`, `references/source-backed-patterns.md`, and `references/codegen-craft.md`; define a beat list with focus, mechanism, camera, memory, landing, selected pattern stack, source anchor requirements, and pre-code gate results for each complex scene.

### Step 2: Code (script.py)

Before writing an ambitious scene, skim `references/worked-example.md` once — a complete, render-verified exemplar whose shape (hook → driver → live numbers → sweep → breath → landing → sealed payoff) is the target for every number-heavy scene.

Use one class per justified scene segment. Do not split every beat into a class. Prefer one continuous class when the same scaffold, symbols, or comparison should stay in memory; split only for a domain shift, hard reset, renderer/API reason, runtime isolation, or density failure with a state handoff. Every class should still be independently renderable.

```python
from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
MONO = "Noto Sans Mono"

class Scene1_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG
        curve = FunctionGraph(lambda x: 0.2 * x**2, x_range=[-4, 4], color=PRIMARY)
        dot = Dot(color=ACCENT).move_to(curve.get_start())
        self.add_subcaption("Watch this point. Why does it speed up?", duration=3)
        self.play(Create(curve), run_time=1.2)
        self.play(MoveAlongPath(dot, curve), run_time=2.0, rate_func=rush_into)
        question = Text("Why does it speed up?", font_size=36, color=ACCENT, font=MONO)
        question.to_edge(UP, buff=0.5)
        self.play(Write(question), run_time=1.0)
        self.wait(1.5)
```

Open with the object of study already doing its job, then pose the question as an overlay — never a bare title card that fades in and out (`references/attention-and-retention.md`).

Key patterns:
- **Subtitles** on every animation: `self.add_subcaption("text", duration=N)` or `subcaption="text"` on `self.play()`
- **Shared color constants** at file top for cross-scene consistency
- **`self.camera.background_color`** set in every scene
- **Scene exits** — carry, park, or transform context forward when continuity matters. Use `self.play(FadeOut(Group(*self.mobjects)))` only for final cleanup or a director-packet semantic reset.

### Step 3: Render

```bash
/path/to/manim-video/scripts/manim.sh -ql script.py Scene1_Introduction Scene2_CoreConcept  # draft
/path/to/manim-video/scripts/manim.sh -qh script.py Scene1_Introduction Scene2_CoreConcept  # production
```

For updater/tracker-heavy scenes add `--disable_caching` — Manim CE's animation cache can hang such renders silently at ~0% CPU (`references/troubleshooting.md`).

### Step 4: Stitch

```bash
cat > concat.txt << 'EOF'
file 'media/videos/script/480p15/Scene1_Introduction.mp4'
file 'media/videos/script/480p15/Scene2_CoreConcept.mp4'
EOF
mkdir -p outputs
/path/to/manim-video/scripts/ffmpeg.sh -y -f concat -safe 0 -i concat.txt -c copy outputs/final.mp4
```

### Step 5: Review

```bash
/path/to/manim-video/scripts/manim.sh -ql --format=png -s script.py Scene2_CoreConcept  # preview still
```

For full video review, read `references/review-loop.md`. If the agent/model can inspect video, review the `.mp4` directly. If not, use the ffmpeg wrapper to extract representative frames into `review-frames/`, review those images, and make at most one or two targeted revision passes.

## Critical Implementation Notes

### Raw Strings for LaTeX
```python
# WRONG: MathTex("\frac{1}{2}")
# RIGHT:
MathTex(r"\frac{1}{2}")
```

### buff >= 0.5 for Edge Text
```python
label.to_edge(DOWN, buff=0.5)  # never < 0.5
```

### FadeOut Before Replacing Text
```python
self.play(ReplacementTransform(note1, note2))  # not Write(note2) on top
```

### Never Animate Non-Added Mobjects
```python
self.play(Create(circle))  # must add first
self.play(circle.animate.set_color(RED))  # then animate
```

## Performance Targets

| Quality | Resolution | FPS | Speed |
|---------|-----------|-----|-------|
| `-ql` (draft) | 854x480 | 15 | 5-15s/scene |
| `-qm` (medium) | 1280x720 | 30 | 15-60s/scene |
| `-qh` (production) | 1920x1080 | 60 | 30-120s/scene |

Always iterate at `-ql`. Only render `-qh` for final output.

## References

| File | Contents |
|------|----------|
| `references/animations.md` | Core animations, rate functions, composition, `.animate` syntax, timing patterns |
| `references/mobjects.md` | Text, shapes, VGroup/Group, positioning, styling, custom mobjects |
| `references/visual-design.md` | 12 design principles, opacity layering, layout templates, color palettes |
| `references/equations.md` | LaTeX in Manim, TransformMatchingTex, derivation patterns |
| `references/graphs-and-data.md` | Axes, plotting, BarChart, animated data, algorithm visualization |
| `references/camera-and-3d.md` | MovingCameraScene, ThreeDScene, 3D surfaces, camera control |
| `references/scene-planning.md` | Narrative arcs, layout templates, scene transitions, planning template |
| `references/director-packet.md` | Portable Text2Animation-style directing packet: ledgers, beat graph, layout/motion IR, gates, repair rules |
| `references/preflight-gates.md` | Production-derived contract, prompt-preservation, source-anchor, direction-execution, assertion, visual-audit, and review gates |
| `references/codegen-craft.md` | Prompt-derived implementation playbook: key-map morphs, lagged reveals, attention baton, contract pacing, groups, live drivers, protected lanes, source anchors |
| `references/cinematic-directing.md` | Premium directing rules: semantic beats, camera grammar, memory rail, protected overlays, hero landing |
| `references/attention-and-retention.md` | Quantified retention grammar mined from the 3Blue1Brown corpus: change cadence, attention thread, camera fusion, overlap dial, hook architecture, dead-air audit |
| `references/algorithm-choreography.md` | Logical motion for algorithms/data structures: sync law, state→style contract, swap/compare/pointer idioms, traversal wavefronts, synced pseudocode panel, step traces |
| `references/visual-polish.md` | Premium finish layer: glow, sheen, spotlight dimmer, micro-motion, organic entrances, data-as-style, semantic palette with state variants, polish budget |
| `references/worked-example.md` | Complete render-verified exemplar scene (secant → derivative) with its mini director packet — the imitation target that composes hook, driver, live numbers, sweep, breath, landing, and sealed payoff |
| `references/source-backed-patterns.md` | Source-backed scene architecture selector: derivative, simulation, pipeline, derivation, comparison, proof, dual-space, recursive/state-space, and 3D patterns |
| `references/review-loop.md` | Model-assisted post-render feedback loop with direct video review and ffmpeg frame extraction fallback |
| `references/rendering.md` | CLI reference, quality presets, ffmpeg, voiceover workflow, GIF export |
| `references/troubleshooting.md` | LaTeX errors, animation errors, common mistakes, debugging |
| `references/animation-design-thinking.md` | When to animate vs show static, decomposition, pacing, narration sync |
| `references/updaters-and-trackers.md` | ValueTracker, add_updater, always_redraw, time-based updaters, patterns |
| `references/paper-explainer.md` | Turning research papers into animations — workflow, templates, domain patterns |
| `references/decorations.md` | SurroundingRectangle, Brace, arrows, DashedLine, Angle, annotation lifecycle |
| `references/production-quality.md` | Pre-code, pre-render, post-render checklists, spatial layout, color, tempo |

---

## Creative Divergence (use only when user requests experimental/creative/unique output)

When the user asks for a fresh, experimental, or unconventional treatment, do not add effects — change ONE structural decision and follow it honestly through the normal pipeline. Pick a single move and commit:

- **Swap the representation.** Explain the concept in a different visual space than the standard one (number line → winding path, matrix → city grid, probability → falling balls). The standard representation exists for a reason, so the swap must reveal something it hides — name that something in `plan.md` before coding.
- **Invert the reveal.** Start from the finished result and deconstruct backward to first principles. Strongest when the result is famous but the path to it is not.
- **Eliminate the notation.** Explain purely through motion, color, and spatial relationships — formulas withheld until the final seal, or absent entirely. This forces every relationship to be shown rather than stated.
- **Exaggerate one parameter.** Push a quantity to an absurd extreme (10x the learning rate, 1000x the sample size, dx = 2 instead of 0.001) and let the visible failure teach why the normal value matters.
- **Impose a constraint.** One continuous shot with no scene cuts; a single hue plus one accent; every object derived from one seed shape. Constraints read as style and force inventive staging.
- **Challenge the standard assumption.** List what is "standard" about how this topic is visualized (left-to-right, 2D, discrete steps), pick the most fundamental assumption, reverse it, and keep the reversal only if it reveals something the standard view hides.

Whatever the move: the retention rhythm, focal discipline, and honest-numbers rules still apply. Divergence changes the representation strategy, never the craft floor.
