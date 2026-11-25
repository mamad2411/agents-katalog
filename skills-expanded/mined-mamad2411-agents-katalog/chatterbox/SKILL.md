---
name: chatterbox
description: Open-source, state-of-the-art text-to-speech and voice cloning by Resemble AI — replaces ElevenLabs for local or self-hosted TTS. Four model variants covering voice agents (Turbo), on-device/CPU inference (Nano), multilingual (Multilingual V3), and general zero-shot TTS. MIT licensed. Use when an agent or application needs speech output, voice cloning, or multilingual narration without sending audio data to a paid cloud TTS service.
---

# Chatterbox — Open-Source TTS & Voice Cloning

**Repo**: github.com/resemble-ai/chatterbox  
**License**: MIT  
**By**: Resemble AI

> "Replace ElevenLabs with Chatterbox — open-source text-to-speech and voice cloning. Your voice. Your data. Your rules."  
> — @hash42labs

---

## Model Zoo

Choose the right model for your use case:

| Model | Size | Languages | Best For |
|---|---|---|---|
| **Chatterbox-Turbo** | 350M | English | Zero-shot voice agents, production use |
| **Chatterbox-Nano** | 110M | English | On-device / CPU inference (3× realtime on 8 cores) |
| **Chatterbox-Multilingual V3** | 500M | 23+ | Global apps, cross-language voice cloning |
| **Chatterbox** (original) | 500M | English | General zero-shot TTS with CFG & exaggeration tuning |

---

## Installation

```bash
pip install chatterbox-tts
```

Or from source:

```bash
git clone https://github.com/resemble-ai/chatterbox.git
cd chatterbox
pip install -e .
```

---

## Usage Examples

### Basic TTS

```python
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

model = ChatterboxTTS.from_pretrained(device="cuda")
wav = model.generate("Hello world. This is a Chatterbox TTS test.")
ta.save("output.wav", wav, model.sr)
```

### Voice Cloning (Zero-Shot)

```python
# Provide a short audio reference clip for the voice to clone
wav = model.generate(
    "This is the cloned voice speaking.",
    audio_prompt_path="reference_voice.wav"
)
```

### Turbo (Voice Agent, Low Latency)

```python
from chatterbox.tts_turbo import ChatterboxTurboTTS

model = ChatterboxTurboTTS.from_pretrained(device="cuda")

# Paralinguistic tags: [laugh], [chuckle], [cough], etc.
text = "Hi there [chuckle], have you got a minute to chat?"
wav = model.generate(text)
```

### Multilingual

```python
from chatterbox.tts_multilingual import ChatterboxMultilingualTTS

model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
wav = model.generate(
    "Bonjour, comment ça va?",
    audio_prompt_path="reference_voice.wav"
)
```

---

## When to use each model

| Need | Model |
|---|---|
| Voice agent with sub-200ms latency | Turbo (350M) |
| On-device / no GPU | Nano (110M) — 3× realtime on CPU |
| Multiple languages from one model | Multilingual V3 (500M) |
| Fine-grained control (CFG, exaggeration) | Original Chatterbox (500M) |

---

## What it replaces

- **ElevenLabs** — voice cloning and TTS API
- **OpenAI TTS** — `tts-1` / `tts-1-hd`
- **Azure Neural Voice** — cloud TTS

Unlike those services, Chatterbox runs locally — no audio data leaves the machine, no per-character pricing, no vendor lock-in.

---

## Gradio Demo (Local)

```bash
# Run the browser-based demo locally
python gradio_tts_app.py
# or
python gradio_tts_turbo_app.py
```

---

## Hugging Face Spaces (Try Without Install)

- Chatterbox-Turbo: huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo  
- Multilingual V3: huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS

Source: @hash42labs "5 Open-Source Projects That Can Replace Software You Pay For" (slide 06/07), Sep 2026.
