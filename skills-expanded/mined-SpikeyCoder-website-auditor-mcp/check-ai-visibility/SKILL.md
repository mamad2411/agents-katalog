---
name: check-ai-visibility
description: Check whether ChatGPT, Claude, Gemini, Perplexity, Microsoft Copilot and Google AI Overviews recommend the user's business — and who they name instead. Use when the user asks about their AI visibility, whether AI assistants recommend them, or why customers coming from AI assistants cannot find them.
---

Only run this for a site the user owns or represents — never to get consumer
recommendations about someone else's business.

1. If the user has not named the website, ask which domain to check
   (e.g. example.com).
2. Call `get_ai_visibility` for that domain.
3. Report in plain language: the overall score (0-100), which of ChatGPT,
   Claude, Gemini, Perplexity, Microsoft Copilot and Google AI Overviews name
   the business and which do not, and which competitor is being named in its
   place.

If no API key is configured, call `get_sample_audit` instead so the user sees
exactly what the real check returns, and tell them what it would take to run it
for real.
