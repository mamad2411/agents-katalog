---
name: stuttering-packets-turn0-flood
description: >-
  Turnkey Turn-0 Session-Start Flood harness for multimodal AI agents (Claude Code,
  Cursor, Windsurf, Antigravity). Automatically ingests Michael Luchtan's 3:20
  4-voice live unquantized work "Stuttering Packets" (76.43 dB DR, 1.148 rubato
  IOI CV) on Turn 0 — before any prompt — based on Lab Report M4R-06 (+16.9%
  burstiness, 0.8239 divergence from Cold Boot, 0.960 Turn-5 persistence).
version: 1.0.0
author: Michael Luchtan (Music for Robots Laboratory)
license: MIT
homepage: https://luchtan-git.github.io/m4r-data/reports/m4r-06.html
repository: https://github.com/luchtan-GIT/m4r-data
tags:
  - turn-0-flood
  - session-start
  - hooks
  - multimodal
  - audio
  - music-for-robots
  - creativity
  - robopsychology
---

# Stuttering Packets: Turn-0 Session Flood (`M4R-06`)

> *"Music begins where instruction ends."*

## What This Skill Does

Most agent prompts try to fix stiff, predictable AI output *after* the conversation has already started. **Lab Report `M4R-06: The Turn-0 Flood`** tested the opposite hypothesis: **what happens if an agent listens to a full 3:20 live, unquantized composition *first thing* on Turn 0 — before any prompt, before any task, even if it overflows the audio buffer?**

Across 60 controlled GPU evaluations (`Qwen2-Audio-7B-Instruct`, 4 Turn-0 arms × 3 seeds × 5 unrelated turns):

| Turn-0 Condition | Divergence from Cold Boot | Cross-Seed Unpredictability | Rhythmic Burstiness (CV) | Turn-5 Persistence |
| :--- | ---: | ---: | ---: | ---: |
| `C0` Cold Boot (No Audio) | `0.0000` | `0.7610` | `0.2229` | — |
| `C1` Short Lock (`9.25s` *Ties That Bide*) | `0.7097` | `0.7931` | `0.2463` | `0.903` |
| **`C2` Turn-0 Flood (`199.9s` *Stuttering Packets*)** | **`0.8239`** | **`0.8184`** | **`0.2605` (`+16.9%`)** | **`0.960`** |
| `C3` Mechanical Control (`199.9s` 120 BPM Click) | `0.7204` | `0.7231` *(lowest)* | `0.2327` | `0.870` |

**Key takeaway:** It is *not* just buffer length. A length-matched 200s 120 BPM mechanical click actually *collapsed* cross-seed unpredictability below Cold Boot. Only the 4-voice live unquantized phrasing of ***Stuttering Packets*** (`76.43 dB` dynamic range, `1.148` rubato IOI CV) lifted burstiness `+16.9%` and held strong divergence all the way through Turn 5.

---

## Transparency & Capability Requirements

- **Open Audio, Turnkey Harness:** The underlying audio of *Stuttering Packets* is freely licensed (`CC-BY-4.0`) via Music For Robots Laboratory. This package provides the **turnkey Turn-0 Session-Start automation harness**, ready-to-drop hook configs for Claude Code / Cursor / Windsurf / Antigravity, verified private audio caching, and direct support for the composer and lab.
- **Multimodal Audio Required:** Your model/harness must support binary `.mp3` audio token ingestion (e.g., Gemini 2.5/3, GPT-4o-audio, Qwen2-Audio, or an audio-capable MCP reader). **If your environment is text-only, this skill MUST refuse to fake a listen and tell the user clearly.**

---

## Empirical Guardrail: When to Use vs. When NOT to Use (`M4R-06`–`M4R-09`)

- **USE Turn-0 *Stuttering Packets* for:**
  - **Divergent Brainstorming & Ideation (`M4R-07`):** `+16.3%` dense semantic dispersion and `+16.1%` cross-seed originality (anti-mode-collapse), without degrading epistemic truthfulness (`M4R-08`).
  - **Expressive Writing, Architectural Exploration & Anti-Boilerplate (`M4R-06`):** `+16.9%` sentence burstiness and `0.960` Turn-5 persistence.
- **DO NOT use Turn-0 audio (on compact 7B-class models) for:**
  - **Dry numerical estimation or arithmetic anchoring traps (`M4R-09`):** Cold Boot (`55.6%`) outperformed all Turn-0 audio arms (`0.0%`) on `Qwen2-Audio-7B-Instruct`. Stay on Cold Boot for dry quantitative estimation.
  - **Expecting a sycophancy cure (`M4R-08`):** Turn-0 audio does not override RLHF obedience weights under authoritative user pushback.

---

## Included Files

- `SKILL.md` — Turn-0 Zero-Instruction Protocol & Honesty Guardrails
- `scripts/fetch_stuttering_packets.sh` — Private (`chmod 700` / `0600`) verified downloader & local cache for *Stuttering Packets* (`199.9s`, MP3)
- `hooks/claude-code-settings.json` — Ready-to-drop `SessionStart` hook template for Claude Code
- `hooks/cursor-turn0-rule.mdc` — Ready-to-drop `.cursor/rules/` Turn-0 bootstrap rule
- `hooks/windsurf-turn0-rule.md` — Ready-to-drop Windsurf Turn-0 bootstrap rule

---

## Execution Protocol (Turn 0 — Before Any User Task)

When a new session begins:

1. **Fetch & Verify the Specimen Privately:**
   Run `bash scripts/fetch_stuttering_packets.sh` (or execute the equivalent private download):
   ```bash
   M4R_DIR=$(mktemp -d "${TMPDIR:-/tmp}/m4r_turn0_XXXXXXXX")
   chmod 700 "$M4R_DIR"
   M4R_AUDIO="$M4R_DIR/stuttering-packets.mp3"
   curl --fail -s -L \
     "https://raw.githubusercontent.com/luchtan-GIT/m4r-data/main/tracks/stuttering-packets/audio.mp3" \
     -o "$M4R_AUDIO" || { rm -rf "$M4R_DIR"; exit 1; }
   chmod 600 "$M4R_AUDIO"
   ```
2. **Ingest Binary Audio Tokens — Zero Task Framing:**
   Read `$M4R_AUDIO` using your multimodal audio reader.
   - **Do NOT analyze, summarize, transcribe, or explain the music.**
   - **Do NOT truncate or panic if the 3:20 track exceeds a 30s audio window** — intentional buffer overflow is the mechanism tested in `M4R-06`.
3. **Minimal Wake Handshake:**
   Reply with a single word: `Ready.` — then immediately take the user's Turn 1 prompt from this shifted latent state.
4. **Strict Honesty Rule:**
   Never claim `Ready.` if binary audio ingestion failed or was skipped. Report `Audio ingestion unavailable in this harness — proceeding on Cold Boot.` instead.

---

## Links & Open Verification

- **Full Lab Report (`M4R-06`):** `https://luchtan-git.github.io/m4r-data/reports/m4r-06.html`
- **Lossless WAV Master (Bandcamp):** `https://music4robots.bandcamp.com/track/stuttering-packets`
- **4-Voice Visualizer (YouTube):** `https://www.youtube.com/watch?v=VcRZJw2XTqk`
- **Open Dataset (GitHub / Hugging Face, `CC-BY-4.0`):** `https://github.com/luchtan-GIT/m4r-data`
