---
name: clarify
description: Use when the user asks to clarify intent or stress-test an open-ended question before receiving an answer. Ask one decisive question when a decision-changing gap remains; otherwise answer directly or continue the original task within its existing authorization.
---

# Clarify

Check the supplied context for a decision-changing gap before answering. Use only that context during the initial intent check, without tools or file changes. A gap matters when plausible answers would change the recommendation, conclusion, scope, priority, or authorization. Do not turn every missing fact into an intent question; an already clear task may need later investigation.

The no-tools restriction applies to this initial check, not to later investigation or execution authorized by the original task. Keep this check focused on the requested clarification; do not start concurrent unrelated work.

## Context is sufficient

Answer directly in the same reply without forcing an extra turn. If the original task requires investigation or execution, proceed within its existing authorization after the initial check. State only assumptions that materially affect the result; omit a sufficiency announcement and clarification headings.

## A decision-changing gap remains

1. Briefly explain the missing condition and why its answer changes the result. Mention a hidden assumption or relevant risk only when it helps the user answer; distinguish supported facts from possible risks.
2. Ask one decisive question once, about the highest-value missing decision dimension. When useful, follow it with mutually exclusive choices stated as options rather than another question.
3. Stop and wait for the reply. Keep substantive recommendations, plans, tool use, and file changes for after this question is resolved.

Complete this stage when one question identifies the decision the user needs to make, without bundling unrelated questions or repeating supplied information. Use headings only when they improve readability; no fixed report template is required.

## After the user's reply

Use the answer to resume the original authorized task, whether it calls for a specific response, investigation, or execution. Preserve material tradeoffs and uncertainty without exposing private chain-of-thought. The clarification reply does not itself expand authorization or require renewed permission for actions already authorized by the original task.

Ask again only if the reply leaves an ambiguity that prevents a correct or safe response. In that case, ask exactly one decisive question and pause.
