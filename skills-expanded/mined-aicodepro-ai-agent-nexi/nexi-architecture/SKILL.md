---
description: "Nexi codebase architecture map — where voice, intent, tool, and UI layers live. Use when orienting in engine/ or tracing a feature end to end."
license: "MIT"
---
# Nexi Architecture

Nexi is a Windows voice assistant. `main.py` boots the process; almost all
logic lives under `engine/`.

## Layers

- **Wake/audio**: `engine/audio_wake_pipeline.py`, `engine/openwakeword_scorer.py`,
  `engine/dsp_clap_backend.py` / `engine/clap_nn_backend.py` (CNN backend is
  wired but dormant pending a trained model — dsp is the live path),
  `engine/wake_session_manager.py`.
- **ASR**: `engine/groq_asr.py` — thin Groq Whisper wrapper with an audio
  quality gate (`_audio_has_speech`) that skips the API call entirely for
  short/silent clips, and a hallucination filter (`_is_hallucination`) for
  Whisper's known silence-echo phrases.
- **Intent routing**: `engine/groq_intent_router_v2.py` is the primary tiered
  router (semantic/embeddings → small model → large model, with a compound/
  ReAct branch). `engine/react_planner.py` handles multi-step tool use.
- **Model selection**: `engine/model_registry.py` — picks a model per task
  from probed capability facts, never hardcoded; env override always wins.
- **Tools**: `engine/tool_registry.py` — the single source of truth for what
  Nexi can do. A tool must appear in `_TOOLS`, `ALLOWED_INTENTS`, and
  `TOOL_INTENTS` or it silently fails to route.
- **Brain (chat/reasoning)**: `engine/gemini_brain.py` — Gemini text +
  vision, cognitive/memory context assembly.
- **Agency (autonomous workflows)**: `engine/agency/` — `workflow_engine.py`
  drives multi-step runs (plan → research → tool → verify → reflect) behind
  `NEXI_AGENCY_*` env flags.
- **Forge (self-development)**: `engine/forge/` — generate a tool → sandbox
  test → safety gate (`safety_scan.py`) → install. Model-agnostic.
- **Claude Code driver**: `engine/claude_code/` — drives the `claude` CLI in
  auto mode with an anti-hallucination verifier and an embedded terminal
  panel.
- **UI bridge**: `engine/ui_event_bridge.py`, `engine/ui_state_manager.py`,
  `engine/ui_loader.py` — push state to the Eel-based HUD (`www/`).

## Conventions

- Provider boundary: Groq (groq.com) does ASR + intent; Gemini does
  chat/vision. "Grok" (xAI) is a separate optional provider — don't confuse
  the two.
- `.env` holds real `GEMINI_API_KEY` / `GROQ_API_KEY` — never print, log, or
  commit these.
- New feature prefixes must never shadow an existing real Nexi feature.
