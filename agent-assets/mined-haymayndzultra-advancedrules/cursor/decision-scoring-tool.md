---
description: "Invoke local scorer tool to rank candidates deterministically"
globs: ["**/*"]
alwaysApply: false
---

# Usage
- Prepare input JSON with: { "context": {...}, "candidates": [...] }
- Run:
  !bash mkdir -p logs/decisions && \
  TS="$(date +%Y%m%d_%H%M%S)" && \
  python3 tools/decision_scoring/score.py tools/decision_scoring/weights.json < input.json | tee logs/decisions/$TS.json

- If decision.type == "ASK_CLARIFY", ask for the single most blocking field only.
- If winner is COMMAND_TRIGGER and action is destructive/compliance-sensitive, add DRY-RUN by default or require confirm.

# Output
- Return the scorer JSON plus a brief natural-language rationale (2–3 sentences).
