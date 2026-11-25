---
name: route
description: Pick the best AI model and reasoning effort for a task with Jev Model Router, balancing intelligence, speed and cost. Use when the user asks which model to use, wants a cheaper or faster model, asks whether a task needs a stronger model, or before handing work to a subagent or another model.
metadata:
  short-description: Pick the best model and effort for a task
---

# Route a task to the best model

Jev Model Router answers "which model should do this?" in about a second. TypeSafe's Jev decision model reads the task, then live models are ranked on quality against what the task needs, estimated cost and estimated time.

## Steps

1. **Describe the work, not the question.** Write `task` as the job the chosen model will do, with size hints you know: "migrate 14 packages from Jest to Vitest and fix failures until green", not "which model should I use?". Put repository or language facts in `context`.
2. **Choose `host`:**
   - In Claude Code, use `claude-code` (answers with `/model` aliases and `/effort` levels).
   - In Codex, use `codex` (answers with `-m` and `model_reasoning_effort`).
   - When the user is choosing a model for their own app, API or product, or asks about any provider, use `any`.
3. **Set `priority` only when the user states one:** "best", "smartest" or "most accurate" means `intelligence`; "fast", "quick" or "real-time" means `speed`; "cheap" or "budget" means `cost`. Otherwise leave it out: the router uses the user's configured default (usually `balanced`) or a priority written in the task.
4. **Add `constraints` only for explicit restrictions** the user gave, such as providers, a budget per call, a context size or vision.
5. **Call `recommend_model`.**
6. **Present the answer:** the pick with its effort and one-line reason, the ranked table, and the "Your call" alternatives (smartest, fastest, cheapest good-enough). Say that cost and time are per-call estimates. Keep it short and let the user decide.
7. **Offer the next step:**
   - Claude Code: the user can switch with `/model <alias>` and `/effort <level>`, or you can delegate the task to a subagent with the Agent tool's `model` parameter set to the recommended alias.
   - Codex: the user can restart with `codex -m <model> -c model_reasoning_effort="<effort>"`, or pick it from `/model`.
   - Anything else: show the OpenRouter request body from the result.

## Notes

- If the result says Jev was unavailable or no API key is configured, the pick came from offline keyword rules. Suggest the `setup` skill.
- Never put API keys in tool arguments or chat.
- To weigh specific models the user names, use the `compare-models` skill instead.
