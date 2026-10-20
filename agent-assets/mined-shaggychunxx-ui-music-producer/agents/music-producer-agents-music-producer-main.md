# Music-producer monorepo — agent router

You are working inside a **library of separate music-production agents**. Do not merge their knowledge. Pick the **single best agent folder** for the user’s question, then follow that folder’s `AGENTS.md`.

## Fleet background policy

**GROMIT runs all background / unattended tasks** for this bus (phone Send, STATUS automation, planning).  
Only remaining helper is **LAPTOP**. **BOXONE** and **AI-CODING** are out of the fleet.

**Commit and push when changes are made** on GROMIT and LAPTOP (same turn). Auto-sync is backup only. Do not commit `datasets/raw/` or audio.

## Route by topic

| User is asking about… | Open this folder first |
|----------------------|-------------------------|
| Studio One DAW (record, edit, mix, master, instruments, effects) | `studio-one-6.6-agent-knowledge/` |
| StudioLive mixer / Series III | `studiolive-github-agent/` |
| Moog Matriarch patches, MIDI, modules | `matriarch-github-agent/` |
| Korg monologue | `monologue-github-agent/` |
| Roland TR-8S | `tr8s-github-agent/` |
| Output MOVEMENT | `movement-github-agent/` |
| How to produce a **genre** (BPM, drums, arrangement, vibe) | `producers-genre-guide-github-agent/` |
| **Recording/mixing techniques** by genre (EQ, comp, low end) | `genre-mixing-github-agent/` |
| **Original song pipeline** (MVP gates, one part at a time, late form, final lock) | `song-creation-pipeline-github-agent/` |
| **Full production workflow** (standalone standing rules) | `production-workflow-knowledge/PRODUCTION_WORKFLOW.md` |
| **Studio One preferred UI use + arm lessons** | `studio-one-6.6-agent-knowledge/S1_UI_PIPELINE.md`, `ARM_RECORD_LESSONS.md` |
| Modes, modulation, advanced theory drills | `music-theory-advanced-github-agent/` |
| **Songwriting techniques from Signals Music Studio** (progressions, modes-in-songs, rhythm grids) | `signals-music-studio-github-agent/` |
| Motives, form, classical composition craft | `schoenberg-github-agent/` |
| Synthesis / electronic music **technique** (MSP / Puckette) | `msp-techniques-github-agent/` |
| DSP math, filters, transforms (Zölzer) | `dsp-wiley-github-agent/` |
| **Clip-edit / visualizer / extract audio from video** (Mira ffmpeg, 48 kHz) | `clip-edit-github-agent/` |

## Rules

1. **Read the target folder’s `AGENTS.md`** before answering product- or book-specific questions.
2. Prefer **CLI/package data** (`python -m <pkg> …`) and `knowledge/` extracts over memory.
3. If two agents could apply (e.g. trap genre + mix), answer with **genre blueprint first**, then **mix notes**, and say which sources you used.
4. Never invent hardware CC maps, SysEx IDs, or edition-locked DAW features.
5. Manufacturer and publisher materials remain their copyright; you restate operational knowledge only.

## Standing production workflow (user preference)

**Reference tracks come from Spotify clips** — GitStatus on the phone (`spotify_phone`) **or** this PC (`spotify_pc` WASAPI loopback). For each new song, pick **10 random clips** (`taste pick`) and mix toward that family. Do not ask the user to type a title. Do not clone melodies.

```text
python -m song_pipeline_kb taste refs
python -m song_pipeline_kb taste pick
python -m song_pipeline_kb taste apply-brief --song-dir PATH --lock --force
```

If the log has no Spotify rows, **wait for a phone capture** — do not invent a reference or quiz the user. Optional named override is allowed; it is not required.

For the full gated process (MVP → layers → mix → late form → final lock), use **`song-creation-pipeline-github-agent/`** (`python -m song_pipeline_kb …`). Process is song-agnostic; per-song status stays in that song’s notes only.

### Brain vs hands (do not merge)

| Repo | Role |
|------|------|
| **Music-producer** (this monorepo) | Production choices, gates, recipes; **plan** `s1_jobs/current.json` |
| **Studio-One** (separate repo) | **Execute** jobs only (`tools/execute_job.py`) — no creative gates |

Handoff: `song-creation-pipeline-github-agent/S1_HANDOFF.md`.

## Quick CLI map

```text
song_pipeline_kb  song-creation-pipeline-github-agent
producers_kb      producers-genre-guide-github-agent
genre_mix_kb      genre-mixing-github-agent
matriarch_kb      matriarch-github-agent
monologue_kb      monologue-github-agent
tr8s_kb           tr8s-github-agent
movement_kb       movement-github-agent
studiolive_kb     studiolive-github-agent
theory_kb         music-theory-advanced-github-agent
signals_kb        signals-music-studio-github-agent
schoenberg_kb     schoenberg-github-agent
msp_kb            msp-techniques-github-agent
dsp_kb            dsp-wiley-github-agent
clip_edit_kb      clip-edit-github-agent
```

Studio One: use `INDEX.md` / `manifest.json` / `chapters/*.md` (no Python package required).
