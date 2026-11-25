---
name: video-editing
description: Production motion graphics, video editing, programmatic animation, and audio-visual synchronization. Embodies the 17 Awesome Claude motion styles (Swiss kinetic type, liquid morphing, HUD drafting, live line drawing, 3D card flips), high-performance Python-to-FFmpeg rawvideo pipelines, tempo-locked BPM grid choreography, and broadcast audio mastering.
---

# Video Editing & Kinetic Motion Graphics (`/video-editing`, `/motion-graphics`)

> **Role**: Master Motion Designer, Creative Director & Video Engineering Architect  
> **Philosophy**: *Animate mathematically. Never guess easing. Snap on cubic-bezier(.7,0,.2,1). Lock every frame to the BPM downbeat. Vector-scale FreeType outlines. Zero AI visual slop.*

This skill establishes elite production standards for programmatic video generation, kinetic typography, motion graphics, and audio-visual choreography inspired directly by **[Awesome Claude Motion Graphics](https://awesomeclaude.ai/claude-motion-graphics)**.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/awesome-claude-styles-catalog.md](references/awesome-claude-styles-catalog.md) | In-depth breakdown of all 17 styles, rules, palettes, easing curves, and avoid lists. |
| **Reference** | [references/easing-curves-and-motion.md](references/easing-curves-and-motion.md) | Mathematical formulas: snap easing, quintic smoothstep, 3D split-flap card flips, drift. |
| **Reference** | [references/ffmpeg-streaming-pipeline.md](references/ffmpeg-streaming-pipeline.md) | High-throughput Python `subprocess.Popen` rawvideo RGB24 pipe streaming architecture. |
| **Reference** | [references/audio-sync-and-ducking.md](references/audio-sync-and-ducking.md) | BPM tempo grid formulas, LA-2A vocal dynamics, -6.5dB sidechain ducking, >=0.85s cushions. |
| **Utility** | [scripts/verify_video_spec.py](scripts/verify_video_spec.py) | CLI tool auditing MP4 resolution, FPS, AAC sample rates, and duration to the microsecond. |
| **Utility** | [scripts/generate_easing_lookup.py](scripts/generate_easing_lookup.py) | Mathematical easing generator and curve evaluator for frame render engines. |
| **Utility** | [scripts/audio_silence_validator.py](scripts/audio_silence_validator.py) | Analyzes vocal stem timelines to guarantee zero audio overlap and strict silence buffers. |
| **Test** | [tests/test_video_editing_skill.py](tests/test_video_editing_skill.py) | Automated test suite validating skill assets, curve invariants, and line count ceilings. |

---

## 2. Programmatic Video Pipeline Architecture

```mermaid
flowchart TD
    subgraph AudioStage["1. Audio Master Synthesis"]
        A1["Neural TTS Synthesis<br/>(en-US-AndrewMultilingual)"] --> A2["Vocal Broadcast Chain<br/>(90Hz HPF + LA-2A + silenceremove)"]
        A2 --> A3["BPM Tempo Grid Clock<br/>(128 BPM: 1 beat = 0.4688s)"]
        A3 --> A4["Music Bed + Sidechain Ducking<br/>(-6.5dB during speech)"]
    end

    subgraph VisualStage["2. Vector Plate & Kinetic Typography"]
        V1["12-Column Swiss Modular Grid<br/>(5% margins, subtle drafting lines)"] --> V2["FreeType Dynamic Vector Scaling<br/>(font_size = base_size * zoom)"]
        V2 --> V3["Kinetic Morphing Engine<br/>(Shape-to-text, 3D card flips)"]
        V3 --> V4["Awesome Claude HUD Brackets<br/>(3-step lock-on [ WORD ] with tick)"]
    end

    subgraph CameraStage["3. Smooth Camera & Compositing"]
        C1["Camera State Interpolation<br/>(Quintic smoothstep 6u^5 - 15u^4 + 10u^3)"] --> C2["Word-Tracking 2D Glide<br/>(0.58s duration + continuous drift)"]
        C2 --> C3["10 Pure Feathered Transitions<br/>(Iris, shutter grid, capsule, dissolve)"]
    end

    subgraph DeliveryStage["4. FFmpeg Raw Stream Multiplexer"]
        M1["Raw RGB24 Stdin Pipe<br/>(30 FPS progressive, CRF 16)"] --> M2["AAC 48kHz Stereo Audio Mux<br/>(Exact frame-audio synchronization)"]
        M2 --> M3["Master MP4 Film + Poster Frame"]
    end

    AudioStage --> CameraStage
    VisualStage --> CameraStage
    CameraStage --> DeliveryStage
```

---

## 3. Core Directorial Invariants (Anti-Slop Video Rules)

1. **Zero Bitmap Scaling Blur**: Never render text at 1080p and stretch the raster in PIL. Always map world coordinates to screen space and rasterize text dynamically at `font_size = int(base_size * zoom)`. Vector outlines must remain pristine at any macro zoom.
2. **Strict Tempo Locking**: Every scene transition and camera shift MUST land on a musical bar or downbeat. For 128 BPM:
   $$\text{Beat} = 0.46875\text{s} \quad (14 \text{ frames}) \qquad \text{Bar (4 beats)} = 1.875\text{s} \quad (56 \text{ frames})$$
3. **Guaranteed Audio Silence Cushion**: Vocal stems must enforce $\ge 0.85$s non-overlapping silence buffers between every dialogue chapter. Never allow voices to collide or bleed into adjacent scene transitions.
4. **Sidechain Ducking**: Duck the background music bed by $-5.0\text{dB}$ to $-6.5\text{dB}$ with 12ms attack and 180ms release whenever speech energy exceeds $-42\text{dBFS}$.
5. **No AI Cliché Tropes**: Strictly prohibit decorative badges (`shields.io`), neon purple gradients, artificial holographic lens flares, particle dust, and programmer tropes like `//` comment markers.
6. **No Stray Line Artifacts**: Never draw arbitrary slanted specular sweeps or laser edges that intersect with vertical grid lines across letters. Transitions must be pure feathered alpha blends or clean geometric wipes.
7. **Strict 500-Line Source Ceiling**: Keep all animation renderers, audio scripts, and compositors $\le 500$ physical lines per file (`check_source_line_limits.py`).

---

## 4. Quick Implementation Recipe: Swiss Kinetic Shot

```python
from PIL import Image, ImageDraw, ImageFont

def render_swiss_shot(draw: ImageDraw.ImageDraw, text: str, wx: float, wy: float,
                      cx: float, cy: float, zoom: float, active: bool = False):
    """Render crisp vector typography on 12-column Swiss grid with HUD brackets."""
    # Screen mapping
    sx = int((wx - cx) * zoom + 1920 / 2.0)
    sy = int((wy - cy) * zoom + 1080 / 2.0)
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(72 * zoom))
    
    color = (255, 255, 255, 255) if active else (100, 100, 100, 255)
    bbox = draw.textbbox((sx, sy), text, font=font, anchor="mm")
    draw.text((sx, sy), text, font=font, fill=color, anchor="mm")
    
    if active:
        # Precision HUD drafting bracket [ WORD ] with center lock tick
        pad = 10
        x0, y0, x1, y1 = bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad
        draw.line([(x0, y0 + 14), (x0, y0), (x0 + 14, y0)], fill=color, width=2)
        draw.line([(x1 - 14, y0), (x1, y0), (x1, y0 + 14)], fill=color, width=2)
        draw.line([(x0, y1 - 14), (x0, y1), (x0 + 14, y1)], fill=color, width=2)
        draw.line([(x1 - 14, y1), (x1, y1), (x1 - 14, y1)], fill=color, width=2)
        draw.line([((x0 + x1) // 2 - 8, y0 - 4), ((x0 + x1) // 2 + 8, y0 - 4)], fill=color, width=2)
```
