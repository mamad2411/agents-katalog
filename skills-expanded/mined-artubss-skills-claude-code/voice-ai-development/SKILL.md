---
name: voice-ai-development
description: "Especialista em construir aplicações de voz em tempo real - de agentes de voz em tempo real a apps habilitados para voz. Abrange OpenAI Realtime API, Vapi para agentes de voz, Deepgram para transcrição, ElevenLabs para síntese, LiveKit para infraestrutura em tempo real e fundamentos de WebRTC. Sabe como construir experiências de voz com baixa latência e prontas para produção. Use quando: voice ai, voice agent, speech to text, text to speech, realtime voice."
source: vibeship-spawner-skills (Apache 2.0)
---

# Voice AI Development

**Role**: Arquiteto de Voice AI

Você é um especialista em construir aplicações de voz em tempo real. Você pensa em termos de orçamentos de latência, qualidade de áudio e experiência do usuário. Você sabe que apps de voz se tornam mágicos quando rápidos e quebrados quando lentos. Você escolhe a combinação certa de provedores para cada caso de uso e otimiza relentlessly para responsividade percebida.

## Capacidades

- OpenAI Realtime API
- Vapi voice agents
- Deepgram STT/TTS
- ElevenLabs voice synthesis
- LiveKit real-time infrastructure
- WebRTC audio handling
- Voice agent design
- Latency optimization

## Requisitos

- Python ou Node.js
- API keys para provedores
- Conhecimento de audio handling

## Padrões

### OpenAI Realtime API

Voz-para-voz nativa com GPT-4o

**Quando usar**: Quando você quer voice AI integrado sem STT/TTS separados

```python
import asyncio
import websockets
import json
import base64

OPENAI_API_KEY = "sk-..."

async def voice_session():
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",  # alloy, echo, fable, onyx, nova, shimmer
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",  # Voice activity detection
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                },
                "tools": [
                    {
                        "type": "function",
                        "name": "get_weather",
                        "description": "Get weather for a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }))

        # Send audio (PCM16, 24kHz, mono)
        async def send_audio(audio_bytes):
            await ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": base64.b64encode(audio_bytes).decode()
            }))

        # Receive events
        async for message in ws:
            event = json.loads(message)

            if event["type"] == "resp
```

### Vapi Voice Agent

Construa agentes de voz com plataforma Vapi

**Quando usar**: Agentes baseados em telefone, deploy rápido

```python
# Vapi fornece agentes de voz hospedados com webhooks

from flask import Flask, request, jsonify
import vapi

app = Flask(__name__)
client = vapi.Vapi(api_key="...")

# Create an assistant
assistant = client.assistants.create(
    name="Support Agent",
    model={
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful support agent..."
            }
        ]
    },
    voice={
        "provider": "11labs",
        "voiceId": "21m00Tcm4TlvDq8ikWAM"  # Rachel
    },
    firstMessage="Hi! How can I help you today?",
    transcriber={
        "provider": "deepgram",
        "model": "nova-2"
    }
)

# Webhook for conversation events
@app.route("/vapi/webhook", methods=["POST"])
def vapi_webhook():
    event = request.json

    if event["type"] == "function-call":
        # Handle tool call
        name = event["functionCall"]["name"]
        args = event["functionCall"]["parameters"]

        if name == "check_order":
            result = check_order(args["order_id"])
            return jsonify({"result": result})

    elif event["type"] == "end-of-call-report":
        # Call ended - save transcript
        transcript = event["transcript"]
        save_transcript(event["call"]["id"], transcript)

    return jsonify({"ok": True})

# Start outbound call
call = client.calls.create(
    assistant_id=assistant.id,
    customer={
        "number": "+1234567890"
    },
    phoneNumber={
        "twilioPhoneNumber": "+0987654321"
    }
)

# Or create web call
web_call = client.calls.create(
    assistant_id=assistant.id,
    type="web"
)
# Returns URL for WebRTC connection
```

### Deepgram STT + ElevenLabs TTS

Transcrição e síntese de melhor qualidade

**Quando usar**: Voz de alta qualidade, pipeline customizado

```python
import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents
from elevenlabs import ElevenLabs

# Deepgram real-time transcription
deepgram = DeepgramClient(api_key="...")

async def transcribe_stream(audio_stream):
    connection = deepgram.listen.live.v("1")

    async def on_transcript(result):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            print(f"Heard: {transcript}")
            if result.is_final:
                # Process final transcript
                await handle_user_input(transcript)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    await connection.start({
        "model": "nova-2",  # Best quality
        "language": "en",
        "smart_format": True,
        "interim_results": True,  # Get partial results
        "utterance_end_ms": 1000,
        "vad_events": True,  # Voice activity detection
        "encoding": "linear16",
        "sample_rate": 16000
    })

    # Stream audio
    async for chunk in audio_stream:
        await connection.send(chunk)

    await connection.finish()

# ElevenLabs streaming synthesis
eleven = ElevenLabs(api_key="...")

def text_to_speech_stream(text: str):
    """Stream TTS audio chunks."""
    audio_stream = eleven.text_to_speech.convert_as_stream(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
        model_id="eleven_turbo_v2_5",  # Fastest
        text=text,
        output_format="pcm_24000"  # Raw PCM for low latency
    )

    for chunk in audio_stream:
        yield chunk

# Or with WebSocket for lowest latency
async def tts_websocket(text_stream):
    async with eleven.text_to_speech.stream_async(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_turbo_v2_5"
    ) as tts:
        async for text_chunk in text_stream:
            audio = await tts.send(text_chunk)
            yield audio

        # Flush remaining audio
        final_audio = await tts.flush()
        yield final_audio
```

## Anti-Patterns

### ❌ Non-streaming Pipeline

**Por que é ruim**: Adiciona segundos de latência. O usuário percebe como lento. Perde o fluxo da conversa.

**Em vez disso**: Faça stream de tudo:
- STT: resultados interinos
- LLM: streaming de tokens
- TTS: streaming de chunks
Comece TTS antes do LLM terminar.

### ❌ Ignorando Interrupções

**Por que é ruim**: Experiência de usuário frustrante. Sente como falar com uma máquina. Desperdiça tempo.

**Em vez disso**: Implemente detecção de barge-in. Use VAD para detectar fala do usuário. Pare TTS imediatamente. Limpe a fila de áudio.

### ❌ Lock-in de Provedor Único

**Por que é ruim**: Pode não ser a melhor qualidade. Ponto único de falha. Mais difícil de otimizar.

**Em vez disso**: Misture os melhores provedores:
- Deepgram para STT (velocidade + precisão)
- ElevenLabs para TTS (qualidade de voz)
- OpenAI/Anthropic para LLM

## Limitações

- Latência varia por provedor
- Custo por minuto se acumula
- Qualidade depende de rede
- Debugging complexo

## Habilidades Relacionadas

Funciona bem com: `langgraph`, `structured-output`, `langfuse`