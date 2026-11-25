---
name: ai-voice-tools
description: Five open-source AI voice and TTS repos for cloning, multilingual speech, and local narration — OpenVoice, F5-TTS, Fish Speech, Kokoro, and CosyVoice — with setup guidance and when to use each.
---

# AI Voice Tools

Five open-source repos from @zhiprompts covering the best free voice AI options as of 2026.

## 01 — OpenVoice (`myshell-ai/OpenVoice`)

**Use when**: you need instant voice cloning from a short sample, with style control (emotion, accent, rhythm).

```bash
git clone https://github.com/myshell-ai/OpenVoice
cd OpenVoice
pip install -r requirements.txt
```

- 37K+ stars, Python
- Zero-shot voice cloning in seconds
- Cross-lingual voice transfer

## 02 — F5-TTS (`SWivid/F5-TTS`)

**Use when**: you want flow-matching TTS with high naturalness and zero-shot cloning, fully open-source.

```bash
git clone https://github.com/SWivid/F5-TTS
cd F5-TTS
pip install -e .
```

- 15K+ stars, Python
- Flow-matching architecture
- In-context voice cloning (no fine-tuning)

## 03 — Fish Speech (`fishaudio/fish-speech`)

**Use when**: you need a multilingual, expressive, actively-maintained TTS system for production workflows.

```bash
git clone https://github.com/fishaudio/fish-speech
cd fish-speech
pip install -e .[stable]
```

- 32K+ stars, Python
- Multilingual (EN, ZH, JP, and more)
- Expressive speech with style control

## 04 — Kokoro (`hexgrad/kokoro`)

**Use when**: you need a compact, lightweight TTS model that runs locally without a heavy stack — ideal for narration and quick deploys.

```bash
# Install via npm (JS) or pip
pip install kokoro-onnx
python -c "from kokoro_onnx import Kokoro; k = Kokoro('kokoro-v1.0.onnx', 'voices.bin')"
```

- 8.2K+ stars, JavaScript (also Python via ONNX)
- Lightweight — runs on CPU
- No GPU required for basic narration

## 05 — CosyVoice (`QwenAudio/CosyVoice`)

**Use when**: you need enterprise-grade multilingual voice synthesis from Qwen/Alibaba's speech research, with zero-shot and fine-tuned modes.

```bash
git clone https://github.com/QwenAudio/CosyVoice
cd CosyVoice
pip install -r requirements.txt
```

- 23K+ stars, Python
- Zero-shot and cross-lingual cloning
- Instruction-based voice control

## Quick Selection Guide

| Need | Best choice |
|---|---|
| Clone any voice fast | OpenVoice or F5-TTS |
| Multilingual production TTS | Fish Speech or CosyVoice |
| Lightweight local narration | Kokoro |
| Enterprise / Qwen ecosystem | CosyVoice |
| Fine control over emotion/style | OpenVoice |
