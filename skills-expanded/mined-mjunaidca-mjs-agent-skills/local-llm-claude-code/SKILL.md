---
name: local-llm-claude-code
description: >
  Set up a FREE local LLM (via Ollama) and connect Claude Code to it so it runs offline
  with no API costs. Use this whenever the user wants to run Claude Code on a local/self-hosted
  model, use Ollama/Qwen/Llama/Mistral/DeepSeek with Claude Code, get a "free" or "offline"
  coding agent, avoid Anthropic API costs, point ANTHROPIC_BASE_URL at localhost, or asks
  "can my machine/VPS run a local LLM for Claude Code". Trigger even if they only say
  "run Claude Code locally", "local model for coding", "self-hosted Claude Code", or name a
  local model (qwen3, llama3, deepseek-coder). Handles install, model tuning, wiring, and an
  honest hardware reality-check (a capable model AND fast hardware are BOTH required).
---

# Local LLM → Claude Code

Connect Claude Code to a locally-served open model. Since **Ollama v0.14+ natively speaks the
Anthropic Messages API** (`/v1/messages`), this needs **no proxy** — just three env vars.

## The one thing to say up front (set expectations honestly)

Making this *work* and making it *usable* are different. Two independent thresholds must BOTH
be cleared, and cheap hardware usually misses both:

1. **Capability** — the model must emit **valid structured tool calls, turn after turn**.
   Small models (≤1.7B) malform them (`args` object vs string, skipped tools). Fixed by a
   **bigger model** (≥14B, ideally a 30B-class MoE), NOT by faster hardware.
2. **Throughput** — the box must chew Claude Code's **~18,000-token system prompt** every turn
   fast enough to beat its request timeout. CPU-only = minutes/turn. Fixed by a **GPU**, NOT
   by a smarter model.

Say this to the user before installing, then read `references/hardware-sizing.md` and run
`scripts/check-hardware.sh` to give them a specific, honest verdict for their box.

## Workflow

Run these in order. Each script is idempotent and needs **no root** (user-space install).

### 1. Reality-check the hardware
```bash
bash scripts/check-hardware.sh
```
Reports CPU/RAM/GPU/disk and recommends a model tier (or warns it'll only be a learning rig).
Details + the sizing table: `references/hardware-sizing.md`.

### 2. Install Ollama (lean, user-space)
```bash
bash scripts/install-ollama.sh
```
Streams the release tarball through `zstd` and **excludes the CUDA/ROCm/MLX GPU libraries**,
so a CPU box installs in **~112 MB instead of ~3 GB**. Starts `ollama serve` on `:11434`.
(On a GPU box, drop the `--exclude` flags — see the script's header.)

### 3. Pull + tune a model
```bash
bash scripts/make-model.sh <base-model> <derived-name>
# e.g. bash scripts/make-model.sh qwen3:14b qwen3-cc
```
Pulls the base model and builds a derived model with a Modelfile that sets
**`num_ctx` large enough for Claude Code's ~18K prompt** (default 32768). This is the #1 cause
of "local Claude Code is broken" — the Ollama default of 4096 silently truncates the prompt.

### 4. Launch Claude Code against it
```bash
bash scripts/launch.sh <derived-name>     # e.g. qwen3-cc
```
Exports the three env vars and runs `claude --model <name>`. The wiring:
```bash
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"   # required but ignored locally
export ANTHROPIC_API_KEY=""            # MUST be empty so the token is used
```
On slow (CPU) boxes the launcher also sets `API_TIMEOUT_MS=900000` so turns don't 500 mid-prefill.

### 5. Verify end-to-end
```bash
bash scripts/verify.sh <derived-name>
```
Tests, in order: native `/v1/messages` chat → a real **tool call** → `count_tokens` (a 404 here
is FINE on v0.14+, not a hang) → measures prompt-eval tok/s so you can predict per-turn latency.

## Hard-won gotchas (all verified the hard way)

- **No proxy needed.** Ollama v0.14+ serves the Anthropic API natively. Do NOT install LiteLLM
  or claude-code-router for Ollama. (vLLM/LM Studio DO need a proxy — see `references/other-backends.md`.)
- **`num_ctx` ≥ 32768.** Claude Code's system prompt is ~18K tokens. The 4096 default breaks it.
- **Reasoning models (Qwen3, DeepSeek-R1) think by default and it's slow.** You CANNOT disable
  thinking through the Anthropic `/v1/messages` path (no `think` field passes; there's no
  `PARAMETER think` in Modelfiles; template edits don't change server-side parse). For Claude
  Code, either accept the overhead or choose a non-reasoning model. For YOUR OWN agents, call
  Ollama's native `/api/chat` with `"think": false` — that DOES disable it (big speed win).
- **`count_tokens` returns 404** on v0.14+ — harmless; Claude Code falls back to local estimation.
  A *hang* (not a 404) means your Ollama is too old — upgrade.
- **Prompt cache helps a lot.** Turn 2+ reuses the cached ~18K system-prompt prefix, so only the
  first turn pays full prefill. Any context growth past the cached prefix re-triggers eval.
- **Install lean or run out of disk.** The full tarball unpacks to ~3 GB (GPU libs); stripping
  them → ~112 MB. Critical on small VPSs.

## When the user's box can't do it

Be direct: it's a great **learning rig** (the wiring, API, and agent-loop mechanics all work),
but not a usable coding agent. Point them to a **14B–30B model on a GPU** (even a modest rented
one) — same Ollama, same three env vars, the setup transfers 1:1. See `references/hardware-sizing.md`.

## References
- `references/hardware-sizing.md` — model-by-RAM/VRAM table, the two-threshold model, GPU guidance
- `references/troubleshooting.md` — every failure mode seen and its fix (timeouts, 404s, truncation, malformed tool calls)
- `references/other-backends.md` — vLLM / LM Studio / llama.cpp (need a proxy) and how to wire them
