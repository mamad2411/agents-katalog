---
name: capcut
description: Expert CapCut Desktop automation and timeline director. Uses the CapCut MCP server to autonomously create, edit, transform, speed scale, subtitle, transition, and keyframe CapCut / JianYing Pro video projects directly on the host machine.
---

# CapCut Desktop Automation & Timeline Director Skill

This skill equips AI assistants (such as Claude Desktop, Cursor, Google Antigravity, Cline, and Windsurf) with the operational knowledge required to edit videos using CapCut Desktop or JianYing Pro through the CapCut MCP Server.

## Core Capabilities

1. **Project & Lifecycle Management**:
   - Discover local projects (`capcut_list_projects`).
   - Create fresh drafts with custom canvas resolutions (`capcut_create_project`).
   - Duplicate or delete projects (`capcut_duplicate_project`, `capcut_delete_project`).
   - Launch projects directly in CapCut Desktop (`capcut_open_app`).

2. **Multi-Track Timeline Construction**:
   - Insert video clips, B-roll cutaways, and talking-head footage (`capcut_add_video_clip`).
   - Insert background music, sound effects, and voiceovers (`capcut_add_audio_clip`, `capcut_add_sound_effect`).
   - Trim, split, and reorder clips (`capcut_trim_clip`, `capcut_split_clip`, `capcut_remove_clip`).

3. **Motion Design & Transformations**:
   - 2D transforms: Position `(x, y)`, Scale `(1.0 = 100%)`, Rotation `(degrees)` (`capcut_set_clip_transform`).
   - Dynamic Speed Ramping & Easing: Set speed multiplier (`0.1x` to `100.0x`) with optional tone-correction (`capcut_set_clip_speed`).
   - Keyframe Animation: Animate scale, opacity, and coordinates over time (`capcut_add_keyframe`).
   - Seamless Transitions: Add dissolves, push, zoom, and whip transitions between clips (`capcut_add_transition`).

4. **Viral Typography & Subtitle Engine**:
   - Render synchronized SRT subtitles directly to native text tracks (`capcut_add_subtitles`).
   - Generate viral short-form typography with custom colors, strokes, and drop shadows (`capcut_add_viral_caption`).
   - Standard static and lower-third text elements (`capcut_add_text`).

5. **Headless Verification**:
   - Inspect media resolution, duration, and audio channels (`capcut_get_media_info`).
   - Render fast proxy preview MP4s headlessly without launching the GUI (`capcut_generate_preview`).

---

## Timeline Coordinate System & Invariants

When manipulating CapCut projects, the following invariants apply:

### 1. Time Units: Microseconds
- All timestamps (`start_time`, `duration`, `source_start`, `source_duration`) are measured in **microseconds** ($1\text{s} = 1,000,000\,\mu\text{s}$).
- Example: A 3.5-second clip has a duration of `3500000`.

### 2. Canvas Coordinates
- Canvas center is `(0.0, 0.0)`.
- Normalized range:
  - Horizontal (`x`): `[-1.0, 1.0]` (left to right).
  - Vertical (`y`): `[-1.0, 1.0]` (bottom to top, where `0.0` is middle, `0.6` is top third, `-0.6` is bottom third).
- Standard scale: `1.0` = 100% canvas fit.

### 3. Track Hierarchy
- **Track 0 (Base Video)**: Main A-roll / talking-head continuous footage.
- **Track 1+ (Overlay Video)**: B-roll cutaways, screen recordings, PIP (picture-in-picture).
- **Text Track 0**: Primary captions or synchronized subtitles.
- **Text Track 1+**: Floating titles, lower-thirds, emoji stickers.
- **Audio Track 0**: Background music (ducked to -12dB).
- **Audio Track 1+**: Sound design (whooshes, pops, impacts, risers).

---

## Viral Typography Styles Reference

When styling short-form captions with `capcut_add_viral_caption`:

### Style 6: Glow Pop
- **Font**: Bold Grotesk / Montserrat Black / Impact.
- **Primary Color**: High-saturation electric yellow (`#FFE600`) or lime (`#00FF66`).
- **Stroke**: Heavy black outline (`#000000`, width `12-16`).
- **Shadow**: Deep black drop shadow with soft blur.
- **Motion**: Scale pop (1.15x -> 1.0x) over 120ms at word boundary.

### Style 7: Hero Typography
- **Letter Spacing**: `-1.0` (tight letter tracking).
- **Casing**: Uppercase.
- **Shadow Offset**: `(26, 26)` with 85% opacity.
- **Color Accent**: Single focal word highlighted in cyan (`#00E5FF`) or electric magenta (`#FF0055`).

---

## Autonomous Editing Workflow Playbook

When an AI agent is requested to edit a raw video into a complete video reel, follow this exact sequence:

1. **Inspect Media**:
   Call `capcut_get_media_info` on the user's raw files to obtain precise duration, width, height, and FPS.

2. **Create Project**:
   Call `capcut_create_project` with name and target canvas resolution (e.g., `1080x1920` for 9:16 vertical shorts, or `1920x1080` for 16:9 widescreen).

3. **Assemble A-Roll**:
   Call `capcut_add_video_clip` to place the primary speech track onto track index 0.

4. **Add Subtitles / Captions**:
   Call `capcut_add_subtitles` with an SRT payload, or use `capcut_add_viral_caption` for styled kinetic text callouts.

5. **Insert B-Roll Overlays**:
   Call `capcut_add_video_clip` with `track_index: 1` over key narrative beats. Apply punch-in zoom transforms (`scale: 1.12`) where appropriate.

6. **Add Background Music & Sound Effects**:
   Call `capcut_add_audio_clip` with `volume: 0.25` (-12dB ducking). Call `capcut_add_sound_effect` at cutaway points (e.g. whoosh on B-roll entrance).

7. **Verify or Open**:
   Generate a quick proxy review using `capcut_generate_preview`, or open the project directly in the desktop app for the user using `capcut_open_app`.

---

## Reference Manuals

For deep video engineering standards, mathematical Quad Easing formulas, and Walter Murch's Rule of Six, consult:
- [CapCut Master Manual](./references/capcut_master_manual.md)
- [B-Roll Production Manual](./references/broll_production_manual.md)
