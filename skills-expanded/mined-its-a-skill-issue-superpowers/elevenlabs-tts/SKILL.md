---
name: elevenlabs-tts
description: "ElevenLabs text-to-speech via inference.sh: Eleven v4 and v4 Turbo (newest, most expressive, audio tags, realtime streaming), Eleven v3, Multilingual v2 and Flash v2.5, each as its own app with 22+ premium voices. Capabilities: text-to-speech, realtime text-to-speech streaming, audio tags for emotion and delivery, voice selection, stability control, custom and cloned voices. Use for: voiceovers, audiobooks, video narration, podcasts, voice agents, accessibility, IVR. Triggers: elevenlabs, eleven labs, eleven v4, eleven v4 turbo, eleven v3, elevenlabs tts, premium tts, realtime tts, streaming tts, professional voice, ai voice, high quality tts, multilingual tts, voice generation, natural speech, realistic voice, voice over, speech synthesis"
allowed-tools: Bash(belt *)
---

> **Install the belt CLI skill:** `npx skills add belt-sh/cli`

# ElevenLabs Text-to-Speech

Premium text-to-speech with 22+ voices via [inference.sh](https://inference.sh) CLI. Each ElevenLabs model is its own app, at one price.

![ElevenLabs TTS](https://cloud.inference.sh/u/4mg21r6ta37mpaz6ktzwtt8krr/01jz00krptarq4bwm89g539aea.png)

## Quick Start

> Requires the inference.sh CLI (`belt`). [Install instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

```bash
belt login

# Generate speech with Eleven v4
belt app run elevenlabs/eleven-v4 --input '{"text": "Hello, welcome to our product demo.", "voice": "aria"}'
```

The result has an `audio` URL to the generated file.

## Which App

| App | Model | Use it for | Text limit | Price per 1K characters |
|-----|-------|------------|-----------:|------------------------:|
| `elevenlabs/eleven-v4` | Eleven v4 | Newest and most expressive; 90+ languages; audio tags | 10,000 | $0.08 |
| `elevenlabs/eleven-v4-turbo` | Eleven v4 Turbo | The low-latency v4; realtime voice agents | 10,000 | $0.04 |
| `elevenlabs/eleven-v3` | Eleven v3 | Previous generation; 70+ languages; audio tags | 5,000 | $0.08 |
| `elevenlabs/eleven-multilingual-v2` | Eleven Multilingual v2 | Stable long-form narration | 10,000 | $0.08 |
| `elevenlabs/eleven-flash-v2-5` | Eleven Flash v2.5 | Fastest and cheapest; long texts and high volume | 40,000 | $0.04 |

- Every app has `run`: the whole text in, an audio file out.
- The two v4 apps also have `realtime`: text streamed in, speech streamed back as it is written (see Realtime Speech).
- `elevenlabs/eleven-v4` and `elevenlabs/eleven-v3` also have `dialogue`: several voices in one take (see Dialogue).
- Check the current price with `belt app pricing elevenlabs/eleven-v4`.

`elevenlabs/tts` is the older app that takes the model as an input. It still works; prefer the per-model apps above.

## Voice Library

### Female Voices

| Voice | Style |
|-------|-------|
| `aria` | American, conversational |
| `alice` | British, confident |
| `bella` | American, warm |
| `jessica` | American, expressive |
| `laura` | American, professional |
| `lily` | British, soft |
| `sarah` | American, friendly |

### Male Voices

| Voice | Style |
|-------|-------|
| `george` | British, authoritative |
| `adam` | American, deep |
| `bill` | American, mature |
| `brian` | American, conversational |
| `callum` | Transatlantic, intense |
| `charlie` | Australian, natural |
| `chris` | American, casual |
| `daniel` | British, commanding |
| `eric` | American, friendly |
| `harry` | American, young |
| `liam` | American, articulate |
| `matilda` | American, warm |
| `river` | American, confident |
| `roger` | American, authoritative |
| `will` | American, bright |

## Examples

### Basic Speech

```bash
belt app run elevenlabs/eleven-v4 --input '{"text": "Welcome to our quarterly earnings presentation.", "voice": "george"}'
```

### Audio Tags (v4 and v3)

Tags in square brackets are performed, not read aloud. They are free-form directions: emotion, delivery, accents, sounds.

```bash
belt app run elevenlabs/eleven-v4 --input '{
  "text": "[excited] We did it! [whispers] Nobody saw this coming. [laughs] What a day.",
  "voice": "jessica"
}'
```

Common tags: `[laughs]`, `[whispers]`, `[sighs]`, `[excited]`, `[sad]`, `[shouts]`, `[slow]`, `[fast]`. The other models read tags aloud, so leave them out there.

### Choose a Model

```bash
# Long narration, stable delivery
belt app run elevenlabs/eleven-multilingual-v2 --input '{
  "text": "Chapter one. It was a quiet morning in the harbour town.",
  "voice": "daniel"
}'

# High volume at the lowest price
belt app run elevenlabs/eleven-flash-v2-5 --input '{
  "text": "Your order has shipped and will arrive on Thursday.",
  "voice": "sarah"
}'
```

### Voice Tuning

```bash
belt app run elevenlabs/eleven-v3 --input '{
  "text": "Fine-tune the voice characteristics for your use case.",
  "voice": "bella",
  "stability": 0.3,
  "similarity_boost": 0.9,
  "style": 0.4
}'
```

| Parameter | Range | Effect | Apps |
|-----------|-------|--------|------|
| `stability` | 0-1 | Higher = more consistent, lower = more expressive | all |
| `similarity_boost` | 0-1 | Higher = closer to original voice character | all |
| `style` | 0-1 | Higher = more style exaggeration | v3, Multilingual v2, Flash v2.5 |
| `use_speaker_boost` | true/false | Enhances speaker clarity | v3, Multilingual v2, Flash v2.5 |

Eleven v4 and v4 Turbo have two settings only, `stability` and `similarity_boost`. Shape their delivery with audio tags.

### Custom Voices

Pass `voice_id` to use a cloned or designed voice (from `elevenlabs/voice-clone` or `elevenlabs/voice-design`). It overrides `voice`.

```bash
belt app run elevenlabs/eleven-v4 --input '{"text": "This is my own voice.", "voice_id": "YOUR_VOICE_ID"}'
```

### Output Formats

```bash
# High-quality MP3
belt app run elevenlabs/eleven-v4 --input '{
  "text": "High quality audio output.",
  "voice": "daniel",
  "output_format": "mp3_44100_192"
}'
```

| Format | Description |
|--------|-------------|
| `mp3_44100_128` | MP3 at 44.1kHz, 128kbps (default) |
| `mp3_44100_192` | MP3 at 44.1kHz, 192kbps |
| `pcm_16000` | Raw PCM at 16kHz |
| `pcm_22050` | Raw PCM at 22.05kHz |
| `pcm_24000` | Raw PCM at 24kHz |
| `pcm_44100` | Raw PCM at 44.1kHz |

### Other Languages

Write the text in the language you want spoken.

```bash
# Spanish
belt app run elevenlabs/eleven-v4 --input '{
  "text": "Hola, bienvenidos a nuestra presentación.",
  "voice": "aria"
}'

# French
belt app run elevenlabs/eleven-v4 --input '{
  "text": "Bonjour, bienvenue à notre démonstration.",
  "voice": "alice"
}'
```

## Dialogue

`dialogue` speaks a conversation in one take and returns one file. Each line has its own voice.

```bash
belt app run elevenlabs/eleven-v4 --function dialogue --input '{
  "segments": [
    {"text": "[excited] Did you hear? The release went out last night.", "voice": "jessica"},
    {"text": "[surprised] Already? I thought that was next week.", "voice": "george"},
    {"text": "[laughs] Nope. Everything shipped.", "voice": "jessica"}
  ]
}'
```

Up to 10 different voices. Keep one dialogue under about 2,000 characters and split a longer script into scenes. The price is the app's rate per character, counted across all lines.

## Realtime Speech

`realtime` on `elevenlabs/eleven-v4-turbo` and `elevenlabs/eleven-v4` is a live function: you stream text as it is written (an LLM's tokens, say) and get speech back while it is still coming. It runs over a socket, so call it from the SDK or the app's page, not with `belt app run`.

```python
# pip install "inferencesh[async]"
import asyncio
from inferencesh import async_inference

async def main():
    client = async_inference(api_key="...")
    task, session = await client.live({
        "app": "elevenlabs/eleven-v4-turbo",
        "function": "realtime",
        "input": {"voice": "george"},
    })

    async def speak():
        for piece in ["Hello there. ", "This is spoken ", "while it is being written. "]:
            await session.send({"events": {"type": "text", "text": piece}})
        await session.send({"events": {"type": "end"}})   # finish speaking, then end

    asyncio.create_task(speak())
    async for frame in session:
        if isinstance(frame, bytes):
            play(frame)            # raw PCM, 16-bit mono, 24 kHz
        else:
            print(frame)           # {"characters": 54, "seconds": 3.9}

asyncio.run(main())
```

What you send, as `{"events": {...}}`:

| Event | Meaning |
|-------|---------|
| `{"type": "text", "text": "..."}` | Text to speak. Send it in pieces as it arrives. |
| `{"type": "flush"}` | Speak what was sent so far without waiting for more |
| `{"type": "end"}` | No more text: finish speaking, then end the session |

- Speech starts once about 40 characters and 8 words have arrived. For a short line, send `flush`.
- Closing the socket ends the session at once. Send `end` when you want to hear the rest first.
- The voice (`voice` or `voice_id`), `stability` and `language_code` are set when the session opens.
- A session ends by itself after `idle_minutes` (default 2) without text.
- You pay for the characters sent, at the app's rate.

## Voice + Video Workflow

```bash
# 1. Generate voiceover
belt app run elevenlabs/eleven-v4 --input '{
  "text": "Introducing the future of AI-powered content creation.",
  "voice": "george"
}' > voiceover.json

# 2. Create talking head video
belt app run bytedance/omnihuman-1-5 --input '{
  "image": "https://portrait.jpg",
  "audio": "<audio-url-from-step-1>"
}'
```

## Use Cases

- **Voiceovers**: Product demos, explainer videos, commercials
- **Audiobooks**: Long-form narration with consistent voices
- **Podcasts**: AI hosts with natural delivery
- **E-learning**: Course narration in multiple languages
- **Accessibility**: High-quality screen reader content
- **IVR**: Professional phone system messages
- **Voice agents**: Speak an LLM's answer while it is still being written, with `realtime`
- **Video Narration**: Documentary and social media content

## Related Skills

```bash
# ElevenLabs multi-speaker dialogue
npx skills add inference-sh/skills@elevenlabs-dialogue

# ElevenLabs voice changer
npx skills add inference-sh/skills@elevenlabs-voice-changer

# ElevenLabs sound effects
npx skills add inference-sh/skills@elevenlabs-sound-effects

# All TTS models (Kokoro, DIA, Chatterbox, Inworld TTS, and more)
npx skills add inference-sh/skills@text-to-speech

# Full platform skill (all apps)
npx skills add inference-sh/skills@infsh-cli
```

Browse all audio apps: `belt app list --category audio`
