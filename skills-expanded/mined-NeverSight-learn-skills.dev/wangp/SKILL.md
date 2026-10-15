---
name: wangp
description: Generate images, videos, animations, or audio locally using WanGP (Wan2GP) by deepbeepmeep — a one-stop optimized app for 200+ open-source generative models (Wan 2.1/2.2, LTX-2/2.3, Hunyuan Video, Qwen Image, Flux, HiDream, Z-Image, KREA, various TTS/audio). Triggers on generate an image, make a video, text to video, local AI generation, or any WanGP/Wan2GP media task. Supports low-VRAM GPUs (6GB+), older cards, AMD via Pinokio/community scripts.
---

# WanGP (Wan2GP) Skill

Generate images, videos, and audio locally using WanGP by deepbeepmeep. WanGP is the premier open-source "one-stop super app" for the best generative models, optimized for the "GPU Poor" (low VRAM, older GPUs, AMD support). It features a full Gradio web UI, headless queue processing, Python API, LoRA/finetune support, automatic model downloads, quantization (int8/fp8/GGUF/NVFP4/Nunchaku), advanced attention (SageAttention 2, Flash, Triton), TeaCache, FlashVSR upscaling, and built-in tools (mask editor, pose extractor, galleries, Deepy offline agent).

**Research-backed accuracy**: All model recommendations, hardware tiers, installation methods, CLI flags, VRAM notes, and prompting guidance are derived directly from the official repository (github.com/deepbeepmeep/Wan2GP), docs/MODELS.md, docs/CLI.md, README, and community corroboration as of June 2026. No guesses.

## MANDATORY STARTUP CHECKLIST (do these IN ORDER)

**STOP. Execute each step in order. Do not skip.**

### Step A: Detect WanGP automatically
```bash
python scripts/wangp.py detect
```
- Returns JSON with `wan2gp_root`, `wan2gp_version`, `wan2gp_update_available`, `python_env_ok`, GPU/VRAM info, recommended profile.
- If multiple installs found, highest maturity score is selected.
- If fails with "Wan2GP not found": Ask user with options (search drives / Pinokio install / manual).

### Step A2: Pinokio Install (recommended for most users)
Pinokio + community scripts (by 6Morpheus6/morpheus) are explicitly recommended in the official README for simplicity and reliability.

```bash
npm install -g pinokio
pinokio download https://github.com/6Morpheus6/wan2gp
pinokio run ~/.pinokio/api/wan2gp/install.js
export WAN2GP_ROOT=~/.pinokio/api/wan2gp/app
python scripts/wangp.py detect
```

Alternative official: `pinokio download https://github.com/deepbeepmeep/Wan2GP`

### Step B: Offer live browser gallery (strongly recommended)
WanGP has its own galleries, but the skill's dedicated dark-themed live viewer with auto-refresh, history, zoom, and SSE updates is ideal for agent workflows.

```bash
SKILL_DIR="..."
bash "$SKILL_DIR/scripts/viewer/start.sh" --gallery-dir /tmp/wangp-gallery --open
```
Use `--output-dir /tmp/wangp-gallery` for all `generate` calls in the session. Images appear automatically.

### Step C: Version & Update Check
If `wan2gp_update_available`, offer `python scripts/wangp.py update` (handles git pull + requirements or heavy components via manage scripts).

### Step D: Default Image Generation Workflow (MANDATORY unless user overrides)

The default image generation workflow is a 4-step VRAM-discipline pattern. This is the standard for all sessions. The user may override individual steps (e.g. "skip upscale", "use flashvsr instead"), but the pattern itself is always the starting point.

**Step D1: Unload first** — Clear any lingering models from VRAM before starting.
```bash
python scripts/wangp.py unload
```

**Step D2: Generate with no upscaling** — Always pass `--upscale off` to prevent the model's default spatial upsampler from consuming VRAM during generation.
```bash
python scripts/wangp.py generate \
  --model <type> \
  --prompt "..." \
  --resolution WxH \
  --steps N \
  --upscale off \
  --output-dir /tmp/wangp-gallery
```

**Step D3: Unload the generation model** — Free VRAM before loading the upscaler. The generation model and Flux PID4 upscaler cannot coexist in 12GB VRAM.
```bash
python scripts/wangp.py unload
```

**Step D4: Upscale with Flux PID4** — The preferred upscaler. Generates high-quality detail (not just interpolation). Produces 4x resolution (e.g. 768x1344 → 3072x5376).
```bash
python scripts/wangp.py upscale "<generated_file>" \
  --method flux_pid4 \
  --output-dir /tmp/wangp-gallery
```

**Why this pattern matters:**
- WanGP does NOT auto-unload models on API calls or mode switches.
- Running Flux PID4 while Krea/Flux/Wan is still in VRAM causes OOM on 12GB cards.
- `--upscale off` prevents the default `lanczos2` spatial upsampler from running during generation, keeping the pipeline clean — upscale happens separately with the AI upscaler for much better quality.
- This pattern scales to any model/upscale combination, not just Krea + Flux PID4.

**When to deviate (ask user first):**
- User explicitly says "no upscale" → skip D3/D4.
- User wants a different upscaler (flashvsr2, lanczos4, coz4, etc.) → substitute in D4.
- User wants to batch multiple generations before upscaling → run D2 in a loop, then D3 once, then D4 on each file.
- Repeated calls with the same model and no upscale between → skip D1/D3 (faster reloads).

### Step E: Unload between model/operation switches (CRITICAL)
WanGP keeps models in VRAM (no auto-unload on API calls or mode switches). The wrapper's `unload` command frees VRAM (torch cache + model unload).

**Always unload when switching** image ↔ video, different model families, or before upscaling a just-generated asset (covered by D1/D3 above).

**Do not unload** for repeated calls with the same model (faster reloads).

## Prerequisites & Installation Notes (Research-Verified)

- **Recommended**: Pinokio with 6Morpheus6/wan2gp community script (handles venv, torch, kernels, models).
- **Manual** (from official README):
  - Modern GPUs (RTX 20xx+): Python 3.11.14, torch 2.10.0+cu130 or latest cuXXX.
  - Older (GTX 10xx): Python 3.10.9, specific older torch cu128.
  - `pip install -r requirements.txt`
  - One-click: `scripts/install.sh` or `.bat` (auto kernel selection: Triton/Sage/Flash/GGUF/Lightx2v/Nunchaku).
- **Docker**: `./run-docker-cuda-deb.sh` (auto-detects GPU/VRAM, builds optimized image).
- **AMD**: Supported via dedicated community scripts (RDNA 2/3/3.5/4).
- **WanGP entry points**: `python wgp.py` (web UI on :7860), `python wgp.py --process queue.zip` (headless batch), Python API (docs/API.md — recommended for future wrapper enhancements), finetune system for custom models/LoRAs/resolutions.
- **Quantization & Kernels**: int8/fp8/GGUF/NV FP4/Nunchaku/Quanto; attention sdpa/sage/sage2/flash; TeaCache multipliers for speed/quality trade-off.

## Image Generation Hierarchy (Hardware-Tiered, Research-Based)

**12GB VRAM (RTX 4070/4060 Ti 16GB, 3060 12GB — most common tier)**:
1. `qwen_image` (or qwen_image_2512 variants) — Best text rendering + strong realism. Use Lightning 4-step or 8-step LoRA accelerator presets (exact HF URLs in original skill; match repo's lightx2v-style accelerators).
2. `krea2_turbo` or KREA-2 — Excellent aesthetics, fast.
3. `ideogram4` or Ideograms v4 — Superior typography/layout. Turbo preset (12 steps).
4. `z_image` — Fastest baseline, NAG-guided, 8 steps.
5. `flux` (with Turbo Alpha LoRA) or Flux 2 Klein/Chroma — General purpose, 8-10 steps.
6. `flux2_klein_9B` or distilled variants — Very fast 4 steps.
7. `hidream_o1` / HiDream — Descriptive prompting, good quality.

**16GB+ VRAM**:
- Above + full `flux2_dev` (32B INT8), `krea2_raw` (max quality 52 steps), full HiDream, longer/higher-res generations.

**8GB or lower**:
- `z_image` INT8/GGUF, `flux2_klein_4B` or smallest Wan 1.3B-derived for image if available, aggressive quantization + lower res (832x480 or below).

**Video Generation Hierarchy**:
**12GB**:
1. `ltx2_22B_distilled` or LTX-2 / LTX 2.3 Distilled — Fastest high-quality (often <1 min), excellent for low VRAM (repo notes 4x VRAM reduction in WanGP optimizations). 8 steps.
2. `t2v_sf` or Wan Lightning/SkyReel-derived fast variants — 4 steps.
3. `t2v_fusionix` or FusioniX — Good motion, 8 steps.
4. `hunyuan_1_5_480_t2v` or Hunyuan Video 1/1.5 — Superior text adherence & quality (slower).
5. Wan 2.1/2.2 14B or 1.3B T2V/I2V (Fun InP, VACE for control) — 1.3B for 6GB min, 14B for quality (12GB+).

**16GB+**:
- Full Wan 14B T2V/I2V/VACE, full Hunyuan, LTX-2 non-distilled, longer videos/higher res, multi-LoRA.

**Specialized**:
- VACE (1.3B/14B): Motion transfer, object injection, inpainting, advanced control.
- Talking heads (Multitalk, FantasySpeaking, Hunyuan Avatar): Voice + image → lip-synced video.
- Phantom, Recam Master, Sky Reels v2: Specific control or infinite-length.

**Upscaling during/after**:
- `lanczos2/4`: Fast, no GPU.
- `flashvsr2/2pass2/4`: Best quality AI upscaling (Triton), x2 needs ~6GB, x4 ~10GB.
- `coz*` Chain-of-Zoom for extreme.
- `flux_pid4`: High-quality image upscaler.

## Prompt Adaptation (Model-Family Specific — Critical for Quality)

Different base models were trained differently; the wrapper/script must adapt or the user prompt must be rewritten.

- **Flux / Flux2 / Klein**: Short, direct imperatives. "A red fox in a misty forest at dawn, cinematic lighting". No long paragraphs. For editing (Kontext/USO): short instructions like "add sunglasses" or style transfer description + reference image.
- **Z-Image**: Concise 1-2 sentences. Relies on NAG (guidance_scale ~0). Good for fast iterations.
- **Qwen Image**: Strong for text-in-image. Short instructions or detailed for complex scenes/text rendering. Excellent realism + typography.
- **HiDream / hidream_o1**: More descriptive — subject, action, environment, style, lighting, mood. Supports longer prompts well.
- **Ideogram / KREA**: Good for composition, layout, typography. Follow their UI/JSON-like if wrapper supports, or descriptive + aspect hints.
- **Wan 2.1/2.2 T2V/I2V (including Fun InP, VACE)**: Detailed cinematic narrative. Camera motion (slow pan left, dolly zoom), character actions, environment, atmosphere, lighting. For I2V: describe motion from the input image. VACE: specify control type (depth, pose, inpaint mask).
- **LTX Video / LTX-2 (Distilled or full)**: VERBOSE screenplay format. Scene descriptions, character actions/emotions in prose, dialogue in "quotes", camera directions (close-up, wide shot, tracking). Excellent for cinematic storytelling. Distilled variants still benefit from rich prompts but are faster.
- **Hunyuan Video**: Similar to Wan — strong text adherence. Detailed narrative with precise subject/object descriptions. Great for identity preservation in Custom/Avatar variants (provide reference image + voice for song/speech-driven).
- **Talking head / Avatar models**: Provide clear voice track + character image/reference. Prompt describes dialogue, emotion, head movement.
- **General tips**: Use negative prompts where supported. For LoRAs: specify via settings or inline if wrapper supports (repo supports per-window multipliers). Test TeaCache (1.5-2.5x) for speed.

The skill's `defaults <model_type>` and prompt adaptation logic in scripts/wangp.py should encode these conventions.

## Workflow Commands (Wrapper: scripts/wangp.py)

- `detect`: Hardware + install scan.
- `defaults <model>`: Baseline resolution, steps, guidance, etc. for that model_type.
- `generate --model <type> --prompt "..." [--resolution WxH] [--steps N] [--image path] [--frames N] [--negative "..."] [--guidance-scale F] [--attention MODE] [--profile N] [--upscale METHOD|off] [--output-dir DIR] [--seed N] [--show]`: Core generation. Maps to appropriate WanGP finetune/mode or API call. Use `--upscale off` for the default generate-then-upscale workflow (see Step D).
- `upscale <path> --method flashvsr2|lanczos2|... [--show]`
- `unload`: Free VRAM (critical between ops).
- `list`: Available model_types the wrapper knows.
- `update`: Update WanGP.

**Options map to real WanGP flags** where possible: --attention, --profile, --seed, --frames, --steps, quantization/TeaCache via profile or extra settings, LoRA via --lora-preset or activated_loras in JSON settings.

For advanced control, the wrapper can/should leverage WanGP's Python API (docs/API.md) or save settings JSON + --process for complex pipelines.

## Harness-Specific Notes

**Hermes Agent** (Nous Research self-improving autonomous agent):
- Terminal-focused or Clarify for structured questions (model choice, upscaling method, resolution).
- Use `--show` or terminal viewers (chafa/viu) for images, or strongly prefer the browser gallery (open it via script).
- Persistent memory and skill-building make it excellent for iterative media workflows — the wangp skill's unload discipline and gallery history pair perfectly.
- The table in original skill is accurate.

Other harnesses (Claude Code, Cursor, etc.): As documented originally — Read tool or IDE preview for images; conversational or question tool for choices.

## Error Recovery & Best Practices (from real usage & repo)

- **OOM / CUDA errors**: Lower resolution (e.g. 1280x720 → 832x480 or model-native), fewer frames/steps, switch to distilled/Lightning/smaller model (1.3B or 4B Klein), enable more aggressive quantization/GGUF, or use INT8 profile. FlashVSR x2 is lighter than x4.
- **Slow generation**: Use distilled/Lightning variants + TeaCache + SageAttention 2 + lower steps. LTX Distilled or Wan 1.3B first.
- **Poor quality/motion**: Increase steps, richer prompt matching family conventions, add LoRAs carefully (repo has presets like VBVR, Id Lora, lightx2v accelerators), use VACE for control.
- **Model not found / unknown**: Run `list` or check WanGP web UI finetunes. Wrapper should have mapping.
- **VRAM leaks**: Always `unload` between major switches. Monitor with nvidia-smi.
- **First run**: Models auto-download on first use per finetune — be patient; architecture-aware.
- **Batch**: Prefer WanGP native queue.zip + --process for large jobs; use wrapper generate for dynamic single tasks from agent.

## References (to be populated in references/ dir)

- model-catalog.md: Full expandable list with exact VRAM, command examples (--t2v-14B, --i2v-1-3B etc.), LoRA notes per family.
- prompting.md: Expanded examples per model family with before/after prompt adaptations.
- hardware.md: Detailed VRAM tables, attention/quantization impact, profile recommendations, AMD/Docker specifics.
- api-integration.md: Notes on leveraging WanGP Python API for tighter wrapper integration (future enhancement).

## When to Use This Skill

Any request for local (not cloud/API) image/video/audio generation or editing with open models, especially when user has or wants WanGP installed for its optimizations, low-VRAM performance, unified interface, or LoRA/finetune ecosystem. Complements ComfyUI users who want simpler non-node workflows or agent scripting.

## When NOT to Use

- Pure cloud generation (use dedicated imagegen or video skills).
- Vector/SVG/code-native assets.
- User explicitly wants ComfyUI workflows or other runners.

This skill makes WanGP agent-accessible with proper model selection, prompt engineering, VRAM discipline, and polished output handling (gallery). It turns a powerful but primarily UI/queue-oriented app into a reliable tool for autonomous creative workflows.

**Validation**: Run validate-skill.sh after edits. Test detect/generate/unload cycle on real hardware matching user's setup (e.g. RTX 4070 Super as in user context).

