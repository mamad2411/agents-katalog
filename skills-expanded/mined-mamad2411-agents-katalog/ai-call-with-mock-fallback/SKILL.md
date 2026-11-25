---
name: ai-call-with-mock-fallback
description: "Wrap unreliable LLM/AI calls with a deterministic mock fallback so the UI always receives a valid shape — annotate the response with a `mock: true` or `error:` field so the client can show a badge."
category: ai
tags: [llm, resilience, fallback, mock, ux, error-handling]
triggers: ["AI 생성 실패", "mock data", "ANTHROPIC_API_KEY", "fallback response", "mock: true", "degraded mode"]
source_project: webtoon_ai_project_with_wrapper
version: 0.1.0-draft
---
