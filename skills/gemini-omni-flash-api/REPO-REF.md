# Repo Referensi: google-gemini/gemini-skills

Repo: https://github.com/google-gemini/gemini-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/google-gemini_gemini-skills
API: curl "localhost:27126/repos/readme?name=google-gemini_gemini-skills"
Dibuat: 2026-09-16

## Cuplikan README
# google-gemini/gemini-skills

Source: https://github.com/google-gemini/gemini-skills
Fetched: 2026-09-16

## README
# Gemini API skills

A library of skills for the Gemini API, SDK and model interactions.

## About

LLMs have fixed knowledge, being trained at a specific point in time. Software
dev is fast paced and changes often, where new libraries are launched every day
and best practices evolve quickly.

This leaves a knowledge gap that language models can't solve on their own. For
example, models don't know about themselves when they're trained, and they
aren't necessarily aware of subtle changes in best practices (like [thought
circulation](https://ai.google.dev/gemini-api/docs/thought-signatures)) or SDK
changes.

[Skills](https://agentskills.io/) are a lightweight technique for adding
relevant context to your agents. This repo contains skills related to building
apps powered by the Gemini API.

### Performance

Our evaluations found that adding this skill improved an agent's ability to
generate correct API code following best practices to 87% with Gemini 3 Flash
and 96% with Gemini 3.1 Pro. For more details, see our blog post:
[Closing the knowledge gap with agent skills](https://developers.googleblog.com/closing-the-knowledge-gap-with-agent-skills/).

## Skills in this repo

> [!IMPORTANT]
> The `vertex-ai-api-dev` skill has moved to
> [skills/cloud/gemini-api](https://github.com/google/skills/tree/main/skills/cloud/gemini-api).

| Skill | Description |
| :--- | :--- |
| [`gemini-api-dev`](skills/gemini-api-dev) | Skill for building apps with the [Gemini API](https://ai.google.dev/gemini-api/docs/interactions?ua=chat) (Interactions API). Covers text generation, multi-turn chat, streaming, function calling, structured output, image generation, Deep Research agents, deprecated model guardrails, and both Python and TypeScript SDKs. |
| [`gemini-live-api-dev`](skills/gemini-live-api-dev) | Skill for building real-time, bidirectional streaming apps with the Gemini Live API. Covers WebSocket-based audio/video/text streaming, voice activity detection, native audio features, function calling, and session management. |
| [`gemini-omni-flash-api`](skills/gemini-omni-flash-api) | Specialized generative AI video skill focused on Gemini Omni 1.1 Flash (`gemini-omni-1.1-flash`), video editing, image and video referenced generation, first and last frame transitions, and video extensions using the Interactions API. |

## Installation

You can install these skills
