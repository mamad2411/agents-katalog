---
name: ml-model-config-registry-dispatch
description: Centralize per-engine ML model configuration in a declarative registry so route, service, and backend layers stay free of if/elif chains.
category: architecture
version: 1.0.0
version_origin: extracted
tags: [architecture, registry, ml-models, dispatch, configuration]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# ML model config registry dispatch

## When to use
Your app supports multiple ML engines (TTS/STT/image) with per-engine quirks: different HF repos, size variants, languages, feature flags (instruct support, hallucination trim, etc.). Left unchecked, the same if/elif chain spreads across routes, services, UI selectors, and download screens.

## Steps
1. Define a `@dataclass ModelConfig` with fields: `model_name` (stable id), `display_name`, `engine`, `hf_repo_id`, `model_size` (default `"default"`), `size_mb`, plus any boolean feature flags relevant to your domain (`needs_trim`, `supports_instruct`, etc.) and a `languages: list[str]`.
2. Write small generator functions per engine family (`_get_qwen_model_configs()`, `_get_non_qwen_tts_configs()`, etc.) that return `list[ModelConfig]`. Centralize platform branching (CUDA vs MLX repos) inside the generator so callers never see it.
3. Expose aggregate accessors: `get_all_model_configs()`, `get_tts_model_configs()`, `get_model_config(model_name)`. Downstream code uses these — never hardcodes an engine name.
4. Route lookups through the registry. Replace `if engine == "qwen": ... elif engine == "chatterbox": ...` with `engine_needs_trim(engine)`, `engine_has_model_sizes(engine)`, `get_tts_backend_for_engine(engine)`, etc. Each is a one-liner over the registry.
5. Keep a thread-safe factory (`dict + Lock`) that lazily instantiates backend classes on first access and caches them. Double-check-locked to avoid duplicate instantiation under load.
6. Unify load/unload/check through config-driven helpers (`unload_model_by_config(cfg)`, `check_model_loaded(cfg)`, `get_model_load_func(cfg)`) so the HTTP routes become single-call functions with no engine branching.

## Counter / Caveats
- Two engines cannot share a `model_name`. Treat `model_name` as the stable public id used by HTTP payloads and DB rows, and never let the display name leak into persistence.
- When a new feature applies to only one engine (e.g. `supports_instruct` for Qwen CustomVoice), add the flag to `ModelConfig` and set it per-engine rather than branching by engine name downstream.
- Do not put runtime state (loaded model, weights) on the config. Configs are declarative; the backend instance holds runtime state.
- Per-engine backend classes still expose their own tiny dispatch for load signatures (`load_model(model_size)` vs `load_model()`) — keep that dispatch in one place (`load_engine_model`) rather than rediscovering it per caller.

Source references: `backend/backends/__init__.py` (the `ModelConfig`, config generators, lookup helpers, `get_tts_backend_for_engine`, `load_engine_model`, `check_model_loaded`, `unload_model_by_config`).
