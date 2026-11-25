---
name: prompt-preflight
description: Analyze a draft prompt for consequential ambiguity, ask only the missing high-value questions, and produce a concise actionable rewrite before substantive work begins. Use when the user asks to check, clarify, refine, lint, or preflight a prompt.
---

# Prompt Preflight

Treat clarification as a cost-benefit decision, not a ritual.

1. Classify the request domain before evaluating clarity. Do not apply software questions to image, writing, research, or other non-software requests.
2. Identify domain-specific details that materially affect the result. For images, consider subject, style, scene, composition, lighting, and format; for software, consider outcome, scope, constraints, and verification.
3. Ask at most three questions, only when different reasonable answers would materially change the work.
4. Show the user's original prompt, then a tailored fill-in-the-blanks example of a better prompt.
5. Preserve the user's likely intent in the example; do not replace it with an unrelated generic prompt.
6. Prefer multiple-choice answers when the likely options are clear.
7. Allow the user to say "use reasonable assumptions" and proceed.
8. After receiving answers, return a compact rewritten prompt with assumptions made explicit.

Do not delay low-risk, reversible, conversational, or already-specific requests. Do not ask for information that can be safely discovered from the current workspace.
