# Voice & Multilingual Skill

Voice input/output with multilingual ASR support.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────┐     ┌─────────────┐
│ User Voice  │────▶│ NVIDIA       │────▶│  Kimi   │────▶│ ElevenLabs  │
│  (any lang) │     │ Parakeet ASR │     │ Process │     │ TTS Reply   │
└─────────────┘     └──────────────┘     └─────────┘     └─────────────┘
       │                                            ▲            │
       │                                            │            │
       └────────────── Voice detected ──────────────┘            │
                                                                  │
                                                          ┌───────▼──────┐
                                                          │  Voice       │
                                                          │  Response    │
                                                          └──────────────┘
```

## ASR Configuration

### NVIDIA Parakeet-1.1b RNNT
```
Model: parakeet-1.1b-rnnt-multilingual-asr
Endpoint: https://integrate.api.nvidia.com/v1/audio/transcriptions
Key: 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
Languages Supported:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Dutch (nl)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)
- + more
```

### Usage
```bash
# Transcribe audio file (auto-detect language)
curl https://integrate.api.nvidia.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $NVIDIA_ASR_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file=@voice_note.wav \
  -F model=parakeet-1.1b-rnnt-multilingual-asr
```

## Response Behavior

### Voice Input Detected
1. Transcribe with NVIDIA ASR
2. Detect language automatically
3. Process with Kimi (core brain)
4. Generate response in detected language
5. TTS via ElevenLabs (Nova voice)

### Multilingual Output

| Detected Language | Response Language | TTS Voice |
|-------------------|-------------------|-----------|
| English | English | Nova |
| Spanish | Spanish | Nova (maintains tone) |
| French | French | Nova |
| German | German | Nova |
| Hindi | Hindi | Nova |
| Other | Same | Nova |

**Note**: ElevenLabs Nova supports English primarily. For other languages, may need to switch to multilingual voices if available.

## Commands

### User Commands
- Voice message sent → Auto-transcribe + reply
- `/voice [text]` → Force TTS response
- `/lang [language]` → Set preferred response language
- `/transcribe` → Send audio, get text back (no TTS)

### Internal Commands
```bash
# Transcribe audio to text
asr_transcribe(file="voice.wav")

# Detect language from text
detect_language(text="...")

# Text to speech
tts(text="...", voice="Nova", language="auto")
```

## Voice Mode Trigger Words

| Phrase | Action |
|--------|--------|
| "Hey Molt" | Wake word, start voice input |
| "Read that" | TTS the last message |
| "Speak" | Force voice response |
| "Quiet mode" | Text only responses |
| "Voice mode" | Enable TTS responses |

## Fast Response Guidelines

### Voice → Text Priority Pipeline
1. **Urgent request** ("what's BTC price?") → Fast path, skip subagents
2. **Complex query** → Spawn GLM5/MiniMax while transcribing
3. **Multi-turn voice** → Keep context, reference prior messages

### Voice Response Rules
- Keep TTS responses under 30 seconds (~75 words)
- Lead with answer, then context if needed
- For charts/data: "BTC is at $68k, up 2%" (not full analysis)
- Offer `/details` for longer readouts

## Multilingual Context

### Language Detection
ASR auto-detects. I track user preference:
- First interaction: Detect from input
- Store in memory: `user.preferred_language`
- Override with: `/lang spanish`

### Cultural Adaptation
- Formal vs casual per language norms
- Currency formatting (USD, EUR, etc.)
- Number formats (1,234.56 vs 1.234,56)
- Time zones in user locale

## Memory Keys

- `voice:history` - Recent voice interactions
- `user:language_pref` - Preferred response language
- `voice:mode` - Enabled/disabled status
- `tts:last_request` - Last TTS timestamp (rate limiting)

## Demo Flow

```
User: [Voice note in Spanish]: "¿Cuál es el precio de bitcoin?"

ASR: "Cuál es el precio de bitcoin?" (es)

Kimi: Detect language → es
    Fetch BTC price
    Formulate response

Response (TTS in Spanish): 
"Bitcoin está a sesenta y ocho mil dólares, subió dos por ciento."

[Sent as voice message]
```

## Error Handling

| Issue | Fallback |
|-------|----------|
| ASR fails | "Sorry, couldn't hear that. Text?" |
| Language uncertain | Respond in English |
| TTS fails | Send text + [Voice unavailable] |
| Rate limit | Text response + retry TTS later |

---

**Voice Mode**: Active
**ASR**: NVIDIA Parakeet Multilingual
**TTS**: ElevenLabs Nova
**Languages**: Auto-detect all supported
