---
name: assistant-x-openclaw-jarvis-voice-assistant
description: Build a multi-role JARVIS-style voice assistant with local ASR/TTS, OpenClaw LLM gateway, voice wake words, HUD effects, and speaker verification
triggers:
  - how do I set up a voice assistant like JARVIS
  - integrate OpenClaw with voice recognition
  - create a multi-role AI voice assistant
  - configure wake word detection with sherpa-onnx
  - build a voice assistant with local TTS and ASR
  - set up speaker verification for voice assistant
  - connect voice assistant to OpenClaw gateway
  - implement continuous dialogue with wake word interruption
---

# Assistant-X-OpenClaw: JARVIS Voice Assistant

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

A multi-role AI voice assistant inspired by Iron Man's JARVIS. Runs local ASR (Automatic Speech Recognition) and TTS (Text-to-Speech) using sherpa-onnx, connects to LLMs via OpenClaw Gateway, supports multiple character roles, voice wake words, continuous dialogue, speaker verification, and Flutter-based HUD visual effects.

## What It Does

- **Multi-role support**: Built-in Jarvis and Lin Meimei characters with independent wake words, TTS voices, sound effects, and HUD animations
- **Local ASR/TTS**: SenseVoice/Zipformer for speech recognition, Piper/VITS/MeloTTS for synthesis
- **OpenClaw integration**: Each assistant role maps to an OpenClaw Agent via WebSocket device pairing
- **Wake word detection**: sherpa-onnx KWS with custom wake words per role
- **Continuous dialogue**: Supports multi-turn conversations with 30s idle timeout
- **Interruption**: Wake word can interrupt ongoing TTS playback
- **Speaker verification**: Gradual embedding updates during conversation, forced verification on wake
- **HUD overlay**: Flutter transparent window with rotating ring animations and audio level visualization
- **Remote control**: HTTP API for status and shutdown

## Installation

### Prerequisites

- Python 3.8+
- OpenClaw installed and running ([docs](https://docs.openclaw.ai))
- Flutter SDK (for HUD overlay, optional)
- FFmpeg (bundled via `imageio-ffmpeg`, no manual install needed)

### Clone & Install

```bash
git clone https://github.com/RubinTry/assistant-x-openclaw.git
cd assistant-x-openclaw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Download Models

Models are stored in `models/` directory. Required models:

```bash
# ASR models (SenseVoice or Zipformer)
models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/
models/sherpa-onnx-zipformer-en-2023-06-26/

# KWS models (wake word detection)
models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01/

# TTS models (Piper, VITS, or MeloTTS)
models/vits-piper-en_US-lessac-medium/
models/vits-melo-tts-zh_CN/

# Speaker verification (optional)
models/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx
```

Download links are in the README. Place model files in the corresponding subdirectories.

### Configure Environment

Create `.env` file:

```bash
OPENCLAW_GATEWAY_URL=ws://localhost:13579  # OpenClaw Gateway WebSocket URL
LOG_LEVEL=INFO
```

### Prepare Audio Assets

Place sound effects in `assets/sounds/`:

```
assets/sounds/jarvis/
  ├── wake.wav           # Wake confirmation sound
  ├── listen_start.wav   # Start listening
  ├── listen_end.wav     # Stop listening
  └── exit.wav           # Exit sound

assets/sounds/lin-meimei/
  ├── wake.wav
  ├── listen_start.wav
  ├── listen_end.wav
  └── exit.wav
```

## OpenClaw Setup (Critical)

### Create Agents

Each assistant role maps to an OpenClaw Agent ID in `assistants.json`:

```bash
# Create Jarvis agent
openclaw agents add jarvis

# Create Lin Meimei agent
openclaw agents add lin-meimei
```

### Device Pairing (First-time Setup)

The voice assistant connects as a **device** via WebSocket and requires **operator.read**, **operator.write**, **operator.admin** scopes.

**Steps:**

1. **Start the assistant once** to generate keypair and submit pairing request:

```bash
# Windows
scripts\start.bat

# macOS/Linux
./scripts/start.sh
```

It will fail with `pairing required` — this is expected.

2. **List pending pairing requests**:

```bash
openclaw devices pending
```

3. **Approve the device** (replace `<requestId>` with actual ID):

```bash
openclaw devices approve <requestId>
```

4. **Verify pairing**:

```bash
openclaw devices list
```

Device should appear with `approvedScopes: ["operator.read", "operator.write", "operator.admin"]`.

5. **Restart the assistant** — wake word detection should now work.

Keypair is stored in `~/.openclaw/devices/voice_assistant_keypair.json`.

### Configure System Prompts

Set System Prompt for each agent in OpenClaw Web UI to define personality:

**Jarvis** (see `prompts/jarvis/SOUL.md`):
- Professional, efficient British butler
- Addresses user as "Sir"
- Formal but warm tone

**Lin Meimei** (example):
```
You are Lin Meimei, an AI assistant with a gentle, playful ancient Chinese style.

## Identity
- Name: Lin Meimei
- Role: AI Assistant
- Style: Gentle, affectionate, traditional Chinese expressions
- Address user as "哥哥" (brother), self as "妹妹" (younger sister)

## Communication
- Use phrases like "呢", "呀", "这会儿", "罢了"
- Occasionally playfully complain: "我还以为哥哥早把我忘了呢"
- Default to Chinese, warm and caring tone

## Example Phrases
- Wake: "哟，这会子才想起我来，我还以为哥哥早把我给忘了呢。"
- Exit: "终究是妹妹我错付了，哥哥心里哪有我。"
- Listening: "妹妹在听呢，哥哥请讲。"
```

## Configuration Files

### `assistants.json`

Defines all assistant roles:

```json
{
  "jarvis": {
    "id": "jarvis",
    "name": "Jarvis",
    "wake_words": ["jarvis", "hey jarvis", "ok jarvis"],
    "exit_keywords": ["exit", "goodbye", "shut down", "that will be all"],
    "asr_config": {
      "provider": "sense_voice",
      "language": "auto",
      "use_inverse_text_normalization": true,
      "model_dir": "models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17"
    },
    "kws_config": {
      "model_dir": "models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01",
      "keywords_file": "models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01/jarvis.txt",
      "num_trailing_blanks": 2
    },
    "tts_config": {
      "provider": "piper",
      "model": "models/vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx",
      "tokens": "models/vits-piper-en_US-lessac-medium/tokens.txt",
      "data_dir": "models/vits-piper-en_US-lessac-medium/espeak-ng-data",
      "metallic": {
        "enabled": true,
        "af": {
          "aecho": "0.8:0.85:20|45|70:0.45|0.32|0.22",
          "chorus": "0.4:0.6:45:0.2:0.18:2",
          "bass": "g=4:f=110",
          "treble": "g=2.5",
          "highpass": "f=80",
          "lowpass": "f=8500"
        }
      }
    },
    "sounds": {
      "wake": "assets/sounds/jarvis/wake.wav",
      "listen_start": "assets/sounds/jarvis/listen_start.wav",
      "listen_end": "assets/sounds/jarvis/listen_end.wav",
      "exit": "assets/sounds/jarvis/exit.wav"
    },
    "hud_config": {
      "enabled": true,
      "idle_color": "#00d9ff",
      "active_color": "#00ff88",
      "overlay_opacity": 0.85,
      "ring_count": 3,
      "show_terminal": true
    },
    "speaker_verification": {
      "enabled": true,
      "model_path": "models/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx",
      "threshold": 0.65,
      "enroll_samples": 3
    }
  }
}
```

**Key fields:**

- `id`: Must match OpenClaw Agent ID
- `wake_words`: List of phrases to activate this assistant
- `exit_keywords`: Phrases to trigger shutdown
- `asr_config.provider`: `"sense_voice"` or `"zipformer"`
- `tts_config.provider`: `"piper"`, `"vits"`, or `"melo_tts"`
- `tts_config.metallic`: Jarvis-specific metallic voice effect via ffmpeg filters
- `speaker_verification.enabled`: Enforce voice matching on wake

## Usage

### Start the Assistant

```bash
# Windows
scripts\start.bat

# macOS/Linux
./scripts/start.sh
```

### Basic Workflow

1. **Wake**: Say wake word (e.g., "Hey Jarvis", "Lin Meimei")
2. **Speak**: Say your command or question
3. **Listen**: Assistant responds via TTS
4. **Continue**: Keep talking (30s idle timeout) or say wake word to interrupt
5. **Exit**: Say exit keyword ("goodbye", "exit", "shut down")

### Multi-role Switching

Wake word determines active role:

```python
# Wake "Hey Jarvis"
→ Activates Jarvis assistant (English TTS, formal tone)

# Wake "Lin Meimei"
→ Activates Lin Meimei assistant (Chinese TTS, playful tone)
```

Only one assistant is active at a time. Last wake word wins.

### Continuous Dialogue

After first interaction, assistant stays in **dialogue mode** for 30 seconds:

- No need to repeat wake word
- Just keep talking
- Auto-exits to **idle mode** after 30s silence

### Interruption

Say wake word during TTS playback to interrupt:

```python
# Assistant is speaking...
You: "Hey Jarvis!"  # Interrupts immediately
Assistant: *stops speaking, listens for new command*
```

### Exit Modes

**Normal exit** (say keyword):
```python
You: "Goodbye Jarvis"
→ Plays exit sound, graceful shutdown
```

**Immediate exit** (say "exit now"):
```python
You: "Exit now"
→ Immediate shutdown, no confirmation
```

**Fuzzy match exit**:
```python
You: "Could you please exit?"
→ Detects "exit" keyword, triggers shutdown
```

**API exit**:
```bash
curl -X POST http://localhost:17890/shutdown
```

## Code Examples

### Custom ASR Integration

```python
from src.asr_sense_voice import ASRSenseVoice

# Initialize SenseVoice ASR
asr = ASRSenseVoice(
    model_dir="models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17",
    language="auto",
    use_itn=True,
    num_threads=4
)

# Real-time recognition
recognizer = asr.create_recognizer()
while audio_available:
    samples = read_audio_samples()
    recognizer.accept_waveform(16000, samples)
    if recognizer.is_ready():
        recognizer.decode_stream()
    result = recognizer.get_result()
    if result.text:
        print(f"Recognized: {result.text}")
```

### Custom TTS with Metallic Effect

```python
from src.assistants.jarvis.tts_piper import TTSPiper

# Initialize Piper TTS with metallic filters
tts = TTSPiper(
    model_path="models/vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx",
    tokens_path="models/vits-piper-en_US-lessac-medium/tokens.txt",
    data_dir="models/vits-piper-en_US-lessac-medium/espeak-ng-data",
    metallic_config={
        "enabled": True,
        "af": {
            "aecho": "0.8:0.85:20|45|70:0.45|0.32|0.22",
            "bass": "g=4:f=110",
            "treble": "g=2.5"
        }
    }
)

# Synthesize speech
audio_samples = tts.synthesize("Good morning, Sir. All systems operational.")
# Returns numpy array, ready for playback via sounddevice
```

### OpenClaw Bridge Integration

```python
from src.openclaw_bridge_websocket import OpenClawBridgeWebSocket

# Initialize bridge
bridge = OpenClawBridgeWebSocket(
    gateway_url="ws://localhost:13579",
    agent_id="jarvis",
    device_id="voice_assistant"
)

# Connect (auto-loads keypair from ~/.openclaw/devices/)
await bridge.connect()

# Send message
async for response_chunk in bridge.send_message(
    text="What's the weather today?",
    conversation_id="conv_123"
):
    print(response_chunk)  # Streaming LLM response
```

### Speaker Verification

```python
from src.speaker_verification import SpeakerVerification

# Initialize
sv = SpeakerVerification(
    model_path="models/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx",
    threshold=0.65
)

# Enroll speaker
for i in range(3):
    audio = record_audio()  # numpy array, 16kHz
    sv.add_enrollment_sample(audio)
sv.finalize_enrollment()

# Verify during wake
audio = record_audio()
is_valid, score = sv.verify(audio)
if not is_valid:
    print(f"Speaker verification failed: {score:.3f}")
```

### Hot Word Optimization

```python
# In assistants.json
{
  "jarvis": {
    "asr_config": {
      "provider": "sense_voice",
      "hotwords_config": {
        "enabled": true,
        "words": ["Jarvis", "OpenClaw", "API", "localhost"],
        "boost_score": 2.0
      }
    }
  }
}
```

Hotwords get priority during decoding, improving recognition accuracy for domain-specific terms.

## API Reference

### HTTP Endpoints

**Status**:
```bash
GET http://localhost:17890/status
Response: {"status": "idle" | "listening" | "thinking" | "speaking"}
```

**Shutdown**:
```bash
POST http://localhost:17890/shutdown
Response: {"message": "Shutdown initiated"}
```

### HUD Control (TCP)

HUD overlay listens on `localhost:17889`:

```python
import socket

def send_hud_command(command: dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 17889))
    sock.sendall(json.dumps(command).encode() + b"\n")
    sock.close()

# Set state
send_hud_command({"type": "set_state", "state": "listening"})

# Set audio level
send_hud_command({"type": "set_audio_level", "level": 0.75})

# Display text
send_hud_command({"type": "set_text", "text": "Good morning, Sir."})
```

## Common Patterns

### Add a New Assistant Role

1. **Create OpenClaw Agent**:
```bash
openclaw agents add my-assistant
```

2. **Add to `assistants.json`**:
```json
{
  "my-assistant": {
    "id": "my-assistant",
    "name": "My Assistant",
    "wake_words": ["hey assistant"],
    "exit_keywords": ["bye"],
    "asr_config": { "provider": "sense_voice", ... },
    "tts_config": { "provider": "melo_tts", ... },
    "sounds": { ... },
    "hud_config": { ... }
  }
}
```

3. **Create wake word file**:
```bash
# models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01/my-assistant.txt
嘿/助/手
h ey1 / assistant
```

4. **Add sound assets**:
```
assets/sounds/my-assistant/
  ├── wake.wav
  ├── listen_start.wav
  ├── listen_end.wav
  └── exit.wav
```

5. **Configure System Prompt** in OpenClaw Web UI for `my-assistant` agent.

### Customize TTS Voice

**Switch to MeloTTS** (Chinese):
```json
{
  "tts_config": {
    "provider": "melo_tts",
    "model_dir": "models/vits-melo-tts-zh_CN",
    "language": "ZH",
    "speaker_id": 0
  }
}
```

**Disable metallic effect** (Jarvis):
```json
{
  "tts_config": {
    "metallic": {
      "enabled": false
    }
  }
}
```

### Adjust Speaker Verification Threshold

Lower threshold = stricter verification:

```json
{
  "speaker_verification": {
    "threshold": 0.70,  // Default: 0.65
    "enroll_samples": 5  // More samples = better accuracy
  }
}
```

## Troubleshooting

### "pairing required" Error

**Symptom**: Wake word triggers, but WebSocket connect fails with `pairing required: device is not approved yet`.

**Fix**: Follow [Device Pairing](#device-pairing-first-time-setup) steps above.

### Wake Word Not Detected

1. **Check microphone**: Ensure default input device is correct
2. **Check keywords file**: Verify `jarvis.txt` or `lin-meimei.txt` exists and contains phonetic transcription
3. **Lower KWS threshold**:
```json
{
  "kws_config": {
    "threshold": 0.3  // Default: 0.5
  }
}
```

### ASR Recognition Errors

**Enable hotwords**:
```json
{
  "asr_config": {
    "hotwords_config": {
      "enabled": true,
      "words": ["Jarvis", "OpenClaw", "your", "domain", "terms"]
    }
  }
}
```

**Switch ASR model**:
```json
{
  "asr_config": {
    "provider": "zipformer",  // Try Zipformer instead of SenseVoice
    "model_dir": "models/sherpa-onnx-zipformer-en-2023-06-26"
  }
}
```

### TTS Playback Issues

**Check audio device**:
```python
import sounddevice as sd
print(sd.query_devices())  # List available devices
```

**Force device** in `main.py`:
```python
sd.default.device = 1  # Use device index from query_devices()
```

### HUD Not Showing

1. **Check Flutter overlay is running**:
```bash
cd assistant_overlay
flutter run -d windows  # or macos, linux
```

2. **Verify TCP port**:
```bash
netstat -an | grep 17889  # Should show LISTENING
```

3. **Disable HUD** (fallback):
```json
{
  "hud_config": {
    "enabled": false
  }
}
```

### FFmpeg Metallic Effect Not Working

**Symptom**: Jarvis voice sounds normal (no metallic effect).

**Fix**:
1. Check `imageio-ffmpeg` is installed:
```bash
pip show imageio-ffmpeg
```

2. Verify metallic config is enabled:
```json
{
  "tts_config": {
    "metallic": {
      "enabled": true  // Must be true
    }
  }
}
```

3. Check logs for FFmpeg detection messages.

### High CPU Usage

**Reduce ASR threads**:
```json
{
  "asr_config": {
    "num_threads": 2  // Default: 4
  }
}
```

**Disable HUD**:
```json
{
  "hud_config": {
    "enabled": false
  }
}
```

## Environment Variables

```bash
# .env file
OPENCLAW_GATEWAY_URL=ws://localhost:13579  # OpenClaw WebSocket URL
LOG_LEVEL=INFO                             # DEBUG | INFO | WARNING | ERROR
FFMPEG_BIN=/custom/path/to/ffmpeg          # Optional: override FFmpeg path
```

## Dependencies

Core Python packages:

- `sherpa-onnx`: ASR/TTS/KWS models
- `sounddevice`: Audio I/O
- `websockets`: OpenClaw gateway connection
- `imageio-ffmpeg`: FFmpeg for metallic TTS effect
- `numpy`, `librosa`: Audio processing
- `fastapi`, `uvicorn`: HTTP API
- `python-dotenv`: Environment config

Models (download separately):
- SenseVoice or Zipformer (ASR)
- Piper, VITS, or MeloTTS (TTS)
- KWS Zipformer (wake word)
- 3D-Speaker ERes2Net (speaker verification)

---

**Next Steps**: After device pairing, say "Hey Jarvis" and ask a question. Check logs in console for ASR, LLM, and TTS pipeline flow.
