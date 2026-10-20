# Text-to-Speech Basics

## Summary

**One-sentence:** Routes a single TTS call to OpenAI TTS, ElevenLabs, or Google Cloud TTS with a sha256-keyed cache and an explicit SSML-routing rule.

**One-paragraph:** Converts ≤4000-character text to natural speech using OpenAI TTS (fast, no SSML, 6 voices, $0.015/1k chars), ElevenLabs (best quality, multilingual, voice cloning), or Google Cloud TTS (400+ voices, SSML supported). Covers voice selection, content-hash caching (sha256 of text + voice + speed + model), text preprocessing for symbols and Markdown, and the hard SSML routing rule: never pass SSML to OpenAI — only to Google or Azure. Output is an audio file path plus duration estimate, deterministic per input.

**Ефективно для:** агента контент-конвеєра, що вибирає TTS-провайдера, кешує генерацію та готує текст до синтезу — закриває петлю між LLM-виходом і озвучкою без подвійних рахунків.

## Applies If (ALL must hold)

- Converting article, news, or notification text to audio in an agent pipeline.
- Text fits in a single API call (≤4000 characters; longer text goes to `tts-implementation`).
- Output format is a saved audio file (mp3 / opus / wav / pcm), not a live duplex stream.
- A deterministic cache key (text + voice + speed + model) is acceptable.
- The agent has at least one provider API key (OpenAI / ElevenLabs / Google Cloud).

## Skip If (ANY kills it)

- Text exceeds 4000 characters — use `tts-implementation` which provides LongTextTTS chunking.
- Sub-200ms first-byte latency required — OpenAI TTS adds 300-800ms minimum; cache phrases instead.
- A specific person's voice is required — use ElevenLabs voice cloning in `tts-implementation`.
- SSML markup (pauses, prosody, say-as) is needed against OpenAI TTS — OpenAI reads SSML literally.
- Heavy domain abbreviations (API, ETA, DB) without preprocessing — they are read literally.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Text payload | UTF-8 string, ≤4000 chars | upstream LLM / preprocessor |
| Voice label | semantic key (`news`, `assistant`, `narrator`) | content type router |
| Provider credentials | env var (`OPENAI_API_KEY`, `ELEVEN_API_KEY`) | secrets manager |
| Output path | filesystem path with rw access | pipeline orchestrator |
| Optional speed | float 0.25-4.0 | caller default 1.0 |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/structured-output-basics` | upstream LLM output is the text payload; needs to be JSON-shaped, then text-extracted before TTS |
| `geek/ai/multimodal-ai/tts-implementation` | downstream path when payload exceeds 4000 chars or streaming is required |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: model tier, SSML routing, cache key, preprocess, char cap, rate-limit delay | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema of synthesize() result + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: SSML to OpenAI, raw Markdown, async-on-sync, missing voice map, cache key without provider | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: preprocess → select voice → check cache → call provider → save → log | ~700 |
| `content/05-examples.xml` | medium | One worked synthesize() call with cache hit + cache miss paths | ~500 |
| `content/06-decision-tree.xml` | essential | Provider routing decision: SSML required? voice clone? language coverage? cost cap? | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-voice` | haiku | Lookup against semantic voice map; deterministic. |
| `preprocess-text` | sonnet | Strip Markdown, expand abbreviations; per-input judgment. |
| `route-provider` | sonnet | Decision-tree walk: SSML, language, voice clone, cost. |
| `synthesize-call` | haiku | Single API call with retry; mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts_basic.py` | OpenAI TTS wrapper with cache + preprocess hooks; ≤60 lines. |
| `templates/voice-map.py` | Semantic voice routing by content type (`news`, `assistant`, `narrator`). |
| `templates/prompt-tts.txt` | Agent task prompt for the TTS subagent (structured input/output contract). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tts-basics.py` | Validate synthesize() output JSON against 02-output-contract schema. | Post-call, before downstream consumes path. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tts-implementation]] — production layer for long-form, streaming, voice cloning.
- [[voice-basics]] — wraps TTS into a conversational STT→LLM→TTS loop.
- [[structured-output-basics]] — upstream JSON schema enforcement before text reaches TTS.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides provider routing before the synthesize call: SSML markup present → Google or Azure (never OpenAI); voice clone required → ElevenLabs; language not covered by OpenAI (≤30 supported) → Google or ElevenLabs; cost cap below $0.020/1k chars → OpenAI tts-1; default → OpenAI tts-1 with semantic voice map. Use the tree at the routing step inside the synthesize() entry point — before any API call.
