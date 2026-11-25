---
name: happy-audio-gen
description: Universal AI voice / text-to-speech skill supporting OpenAI TTS (gpt-4o-mini-tts, tts-1), ElevenLabs multilingual TTS with voice cloning, Bailian Qwen TTS (qwen-tts / qwen3-tts-vd with voice-design custom voices, long-text chunking built in), MiniMax speech-02-hd, SiliconFlow CosyVoice / SenseVoice, and PlayHT 2.0. Use this skill whenever the user asks to read text aloud, synthesize speech, generate narration, create voice-over, dub a script, or turn any text into audio (mp3 / wav / ogg / flac). Typical phrases include "read this aloud", "generate voice for ...", "create a narration of ...", "tts this", "把这段念出来", "做个配音", "合成语音", or mentions of voices / TTS model names like Alloy, Ash, Cherry, Rachel, CosyVoice, PlayHT. Always use this skill even if the user does not specify a provider — pick one from EXTEND.md defaults or available env keys.
version: 0.1.0
---

# happy-audio-gen

Turns text into speech across 6 providers through one CLI. All providers are synchronous (TTS is fast — typically under 10 seconds) except Bailian's voice-design flow (which is still covered but uses a longer poll window).

## Quick usage

```bash
# Shortest path — OpenAI default voice
bun scripts/main.ts --text "Hello, world" --out ./hello.mp3

# Chinese, MiniMax
bun scripts/main.ts --provider minimax --text "大家好" --voice male-qn-qingse --out ./hello.mp3

# Long-form, Bailian (auto-splits by sentence)
bun scripts/main.ts --provider bailian --textfiles ./script.md --out ./narration.mp3
```

## When to invoke this skill

- User asks to synthesize speech / TTS / read aloud / narrate / dub / make a voice-over.
- User asks to convert script / text / article into audio.
- User names a TTS voice or model.

Do **not** route here when the user wants to transcribe audio → text (that's STT, different domain), or edit / mix audio files (use a dedicated audio editor).

## Step 0: Preflight (BLOCKING)

1. **Locate EXTEND.md**:
   - `./.happy-skills/happy-audio-gen/EXTEND.md`
   - `$XDG_CONFIG_HOME/happy-skills/happy-audio-gen/EXTEND.md`
   - `~/.happy-skills/happy-audio-gen/EXTEND.md`

   If none found, run `bun scripts/main.ts --setup` and walk the user through `references/config/first-time-setup.md`.

2. **Verify at least one provider has credentials** (env var or 1Password reference).

3. **Verify Bun** is available. Fallback: `npx -y bun`.

## Step 1: Choose provider

Preference order:

1. `--provider <id>`
2. EXTEND.md `default_provider`
3. Auto-detect env vars: `openai > elevenlabs > bailian > minimax > siliconflow > playht`

Pick by language / voice intent:

- **English, natural + fast** → `openai` (gpt-4o-mini-tts / tts-1).
- **Multilingual, voice cloning** → `elevenlabs`.
- **Chinese, long-form** → `bailian` (qwen-tts auto-chunks long scripts) or `minimax`.
- **Chinese dialect / voice design** → `bailian` (voice-design with qwen3-tts-vd) or `siliconflow` (CosyVoice2).
- **Ultra-realistic, short-form** → `playht` (2.0).

## Step 2: Fill parameters

- **`--text`** or **`--textfiles`**: input. Always quote.
- **`--out <path>`**: REQUIRED. Extension determines format (`.mp3` / `.wav` / `.ogg` / `.flac`).
- **`--voice <id>`**: provider-specific. See `references/voices.md` for the short list of well-known voices.
- **`--rate 0.5..2.0`**: speaking rate.
- **`--instruction "..."`**: voice direction (only `openai` gpt-4o-mini-tts and `siliconflow` honor this).
- **`--language <code>`**: `en`, `zh`, `ja` — only a few providers honor this explicitly.

## Step 3: Run

```bash
bun scripts/main.ts \
  --provider openai \
  --model gpt-4o-mini-tts \
  --voice alloy \
  --text "..." \
  --out ./out.mp3
```

JSON mode:

```json
{ "success": true, "provider": "openai", "model": "gpt-4o-mini-tts", "voice": "alloy", "output": "/abs/out.mp3", "size_bytes": 76032, "format": "mp3" }
```

## Step 4: Long text handling

- `happy-audio-gen` automatically splits long input for providers that cap per-call length (Bailian ≤ 200 Chinese chars per call). Chunks are concatenated byte-for-byte on output.
- For best fidelity with concatenated MP3s, stitch the segments with ffmpeg afterward rather than relying on byte concat.

## Step 5: Errors

- `[openai] OpenAI TTS 400` with `invalid voice` → the voice name is not supported by the model. Use one of `alloy`, `ash`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`.
- `[minimax] ... 2049 invalid api key` → try `MINIMAX_BASE_URL=https://api.minimaxi.com/v1` (different region).
- `[bailian] ... 400 DataInspectionFailed` → Aliyun content filter. Surface to the user.
- `[elevenlabs] 401` → key invalid or subscription expired.

## References

- `references/providers.md` — per-provider env vars, default models, voice lists.
- `references/voices.md` — curated voices for each provider.
- `references/error_codes.md` — common errors and fixes.
- `references/config/first-time-setup.md`
- `references/config/extend-schema.md`
- `assets/EXTEND.template.md`
