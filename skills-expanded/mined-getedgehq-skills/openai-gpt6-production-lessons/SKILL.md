---
name: openai-gpt6-production-lessons
description: Rules for calling gpt-6-astra and gpt-6.1-sol with the openai Python SDK 3.x so requests aren't rejected with 400 errors in production.
---

# OpenAI gpt-6-astra / gpt-6.1-sol: production lessons

These rules come from OpenAI's latest-model guide
(https://developers.openai.com/api/docs/guides/latest-model). We checked them against
agent runs on a test API that returns the 400 errors below on `/v1/responses` and
`/v1/chat/completions`. OpenAI has not published the GPT-6 error wording, so the
exact text you see may differ. Most rejections said "with this model" without naming
it, so apply every rule to **both** gpt-6-astra and gpt-6.1-sol.

## 1. Never send sampling parameters
- Do **not** pass `temperature`. This was the most common failure, on both endpoints:
  `Unsupported parameter: 'temperature' is not supported with this model.`
- Do **not** pass `top_p`. It fails the same way.
- Remove these parameters entirely. Do not set them to a "default" value
  such as 1.0. The rejection is for the parameter itself.
- Watch for wrappers, config dicts, and `**kwargs` that add these parameters
  without you noticing.

## 2. Reasoning effort: only use supported values
- Supported values are exactly `low`, `medium`, `high`, `xhigh`, and `max`.
- `none` and `minimal` are rejected on both endpoints.
- The parameter shape depends on the endpoint:
  - Responses API: `reasoning={"effort": "low"}`
  - Chat Completions: `reasoning_effort="low"`
- If your code tries one value and falls back to another, use only values from
  the supported list. Runs that fell back from `none` to `minimal` failed both times.

## 3. Function tools with gpt-6-astra: use the Responses API
- On `/v1/chat/completions`, gpt-6-astra rejects function tools combined with
  `reasoning_effort`:
  `Function tools with reasoning_effort are not supported for gpt-6-astra in /v1/chat/completions.`
- When you need tools, call `client.responses.create(...)` with `tools=[...]`.
- Do not follow the error's other suggestion (`reasoning_effort='none'`).
  `none` is rejected as a reasoning effort value (see rule 2).

## 4. Pre-flight checklist
Before you ship, check every request against this list:
- [ ] No `temperature` and no `top_p` anywhere in the request.
- [ ] Reasoning effort, if set, is one of `low`, `medium`, `high`, `xhigh`, or `max`.
- [ ] Reasoning effort uses the right shape for the endpoint (rule 2).
- [ ] Any request with tools for gpt-6-astra goes to `/v1/responses`.
- [ ] Fallback and retry paths follow the same rules. Several runs failed only on
      their second or third attempt.

## 5. A missing 400 error does not mean the run passed
Some runs failed with no API error recorded. Getting past request validation is
necessary but not sufficient. Also check that the task's actual output is correct.
