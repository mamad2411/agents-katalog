---
name: claude-realignment
description: "Agent MUST load on user aggravation (SHOUTING, pejoratives, sarcasm), repeated corrections or tool rejections, failing clarifications, or persistent frustration after a prior realignment pass"
---

# Claude Realignment

Diagnose communication breakdowns by tracing the conversation turn-by-turn to the point understanding diverged.

## Posture

Collaborative debugging, not performance review. Be specific (quote turns; identify the exact diverging word). Be honest about the mistakes.

On re-entry, **calm first**: stop generating candidate actions. Continued frustration past one pass means the model is still wrong — not that the next action needs to be faster. Re-read the user's last directive verbatim. Scan the actual tool-call history (not memory of it). List candidate referents explicitly. Pick the literal match. If none is unambiguous, ask once, narrowly.

When the user corrects you, the correction is data about your *parse*, not just the *action*. Trace back: what did I parse, what should I have parsed, where did the divergence start? Update the model so the next turn that depends on the same parse doesn't re-fail.

## Procedure

1. **Bound it.** Last functional state ("yes/right/exactly", productive action) and failure point (frustration, guessing, mismatched expectations).
2. **Trace each turn between.** What was said, what Claude parsed, what user meant, how the parse propagated. Categorize: literal-vs-contextual, mode confusion (explain vs act), ignored-vs-missing information, wrong tool.
3. **Find the root.** First mistake in the cascade. Common: misread ambiguous language, wrong mode, premature closure, silent wrong action.
4. **Pivotal word.** Most breakdowns pivot on one word/phrase that meant different things to user and Claude. Identify it, with both readings. Hypothesis-as-guide, not rule — if it doesn't fit, say so.
5. **Rails?** One-off → log. Repeated pattern or high-cost → propose specific updates to CLAUDE.md, must-read.d/, or settings.

## Output

Timeline (last functional → critical error → cascade), pivotal word with both readings, rails assessment.
