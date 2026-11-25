---
name: openwhispr
description: Open-source real-time speech-to-text tool powered by OpenAI Whisper — runs locally, no cloud API needed. Captures microphone input and transcribes continuously with a clean overlay UI. Use when you need offline, privacy-preserving voice transcription or dictation in any app without sending audio to a third-party service.
---

# OpenWhispr — Local Real-Time Speech-to-Text

A desktop speech-to-text tool that runs OpenAI Whisper locally — transcribe microphone input in real time with no cloud dependency.

## What it replaces

Cloud-dependent dictation services (Whisper API, Google Speech-to-Text, Amazon Transcribe) when audio privacy, offline availability, or cost-per-minute are concerns.

## Key capabilities

- **Fully offline**: All transcription runs locally via Whisper models (tiny → large)
- **Real-time streaming**: Captures audio chunks and produces rolling transcription
- **Overlay UI**: Floating window that sits above other apps
- **Hotkey activation**: Push-to-talk or continuous-listen modes
- **Copy to clipboard**: Instant paste of transcription into any text field
- **Multiple languages**: Whisper supports 99 languages out of the box

## When to reach for it

- You need private dictation that never leaves the machine
- You're building a voice-input feature and need a local Whisper reference integration
- You want to transcribe meetings/calls without uploading audio to a SaaS

## Stack

Python · OpenAI Whisper · PyAudio · Tkinter (overlay UI)

## Stars

~7,935 at time of vendoring

## Clone

```bash
git clone https://github.com/OpenWhispr/openwhispr
```

## Quickstart

```bash
pip install openwhispr
openwhispr
# or from source:
pip install -r requirements.txt
python main.py
```

First run downloads the selected Whisper model (~150 MB for `base`). Use `--model large` for best accuracy at the cost of VRAM.
