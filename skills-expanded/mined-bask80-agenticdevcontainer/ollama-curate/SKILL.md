---
name: ollama-curate
description: >
  Reports what local ollama models are installed, what tier each one fits at
  (fast/fully GPU-resident vs slow/CPU-RAM-bound) on your current hardware,
  what gaps exist against your offline coverage needs, and what to pull or
  drop with disk reclaimed. Portable across opencode, Claude Code, and the
  GitHub Copilot CLI — shell and file reads only, no harness-specific APIs.
  Use when you ask "what local models should I have", "curate my ollama
  models", "what should I pull/drop", or want your local model lineup
  reviewed after a hardware change or a while away from it.
---

# ollama-curate

Decides what should be installed in ollama on your machine — never by
reciting model names from memory, always by re-deriving from the live ollama
instance and, at refresh time, the live ollama.com/registry.ollama.ai
catalogue. The full method (endpoint/data-dir setup, formula, tiering, gap
analysis, slow-tier evaluation, file-write rules) is in
[REFERENCE.md](REFERENCE.md) — read it before doing anything nontrivial here.
This file is the checklist.

## Must not

- **Never hardcode a model name, size, or hardware number in this prose.**
  Every fact like that belongs in the data directory (see REFERENCE.md
  § Configuration) — read it live, don't recite it. If the catalogue or
  hardware has moved on, the data files are what's wrong, not this file.
- **Never require the network to report on what's already installed.** One
  call to the resolved ollama endpoint's `/api/tags` (see REFERENCE.md
  § Ollama endpoint discovery) plus the cached data files is enough for "what
  do I have and what tier is it." Only the *refresh* path (re-scraping the
  catalogue, re-measuring a model, asking for new hardware specs) may touch
  the network.
- **Never pull a model without saying its size first and getting a go-ahead**
  — a multi-GB download is a real disk/bandwidth cost, not a free action.
- **Never write to `preferences.json`.** That file is owned exclusively by
  `pick-model`. This skill only writes `hardware.json`'s `hardware` and
  `ollamaEndpoint` keys and the `ollama/*` entries (+
  `ollamaKvCacheAssumptions`) in `models.json`.
- **Never assume a discrete NVIDIA-style GPU.** The VRAM-tiering math (see
  REFERENCE.md § Tiering formula) assumes a fixed VRAM pool separate from
  system RAM — that doesn't hold on unified-memory hardware (e.g. Apple
  Silicon) or CPU-only machines. Say so plainly rather than producing a
  confidently wrong fit prediction on hardware the formula doesn't cover.

## Checklist

1. **Resolve the ollama endpoint and data directory** — see REFERENCE.md
   § Ollama endpoint discovery and § Configuration. Don't assume either;
   both are environment-specific.
2. **Load state.** Read `hardware.json` and `models.json` from the data
   directory. If `hardware.json` is missing or its `hardware` key has no
   `source`, this is a first run — ask for GPU vendor/VRAM, system RAM, CPU
   (see REFERENCE.md § Hardware refresh), write it, then continue. Never
   guess hardware silently.
3. **List what's installed.** `GET <ollama endpoint>/api/tags`. No other
   network call needed for this step.
4. **Classify each installed model's tier** using the formula and procedure in
   REFERENCE.md § Tiering formula — fully-GPU-resident ("fast") up to some
   context, or explicitly a measured, deliberate "slow" tier, or neither (drop
   candidate). Cache any newly derived `fitFormula`/`decodeThroughput` facts
   back into `models.json`.
5. **Find gaps** against the coverage categories in REFERENCE.md § Coverage
   gaps — report what's well-served offline and what isn't, plainly.
6. **Recommend pulls/drops**, each with its disk delta, following REFERENCE.md
   § Recommending changes (this is where the "ask before a multi-GB pull"
   rule and the "don't add a redundant same-class slot" rule live).
7. **On refresh** (explicitly asked, or data looks stale): re-scrape the live
   ollama.com catalogue and re-derive architecture facts from
   `/api/show`/manifests — never from memory. See
   REFERENCE.md § Refreshing.

## Packaging

Canonical file: this one, at `.agents/skills/ollama-curate/SKILL.md`.
Discovered via symlinks at `.claude/skills/ollama-curate` and
`.opencode/skill/ollama-curate` (both → `../../.agents/skills/ollama-curate`).
Copilot CLI needs no extra step — it reads `.agents/skills/` natively.
