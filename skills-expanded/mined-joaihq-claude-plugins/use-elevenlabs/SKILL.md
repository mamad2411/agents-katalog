---
name: use-elevenlabs
description: Use the ElevenLabs JoAi app plugin when the task needs ElevenLabs tools or workflows.
---

# ElevenLabs

Connect ElevenLabs to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the ElevenLabs tools available in this app.
- Explain what setup or authentication ElevenLabs needs before I run an action.
- Use ElevenLabs to help me with the task I describe next.

## Action Inventory

- `elevenlabs-list-voices` (collect) — List all available voices in your ElevenLabs account, including premade and cloned voices.
- `elevenlabs-speech-to-text` (collect) — Transcribe audio to text using ElevenLabs speech-to-text.
- `elevenlabs-text-to-speech` (collect) — Convert text into realistic speech audio using ElevenLabs AI voices.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
