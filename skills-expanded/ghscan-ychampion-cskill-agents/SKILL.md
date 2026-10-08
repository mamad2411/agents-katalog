---
name: withheld-max-output-token-errors
description: "Delay surfacing max-output-token failures until the recovery loop completes, then emit sanitized tool_result errors."
metadata:
  author: ychampion
---

# SKILL: Withheld Max Output Token Errors
**Domain:** tool-orchestration  
**Trigger:** Use this when a user turn hits the max-output-token limit but the system keeps retrying so the recovery loop should finish before reporting an error.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Detect the API’s `max_output_tokens` error inside the streaming loop, suppress it while recovery continues, and only expose it once all retries settle. During that delay, emit placeholder `tool_result` messages that say each tool is missing so the user sees a focused failure summary instead of a raw API error. This keeps recovery logic intact while still surfacing helpful, per-tool diagnostics after the recovery path finishes.

## Key Rules
- Guard every assistant message against `apiError === 'max_output_tokens'` and only mark it for reporting once the recovery loop decides no more progress can happen.
- Track tool_use IDs for the assistant messages that triggered the error and emit sanitized messages with the standard `tool_result` shape so downstream components can handle them like any other tool failure.
- Log the withheld message only after `isWithheldMaxOutputTokens` returns true; do not surface the API error early or the SDK context may terminate the session.
- Keep the placeholder text short, include the original error message, and mark `is_error: true` so tooling knows it’s still an error.
- Preserve the tool ID so any transcripts or sidecars referencing the tool use still match the replayed replacement.

## Example Application
When the per-turn token budget is exceeded while streaming a multi-tool answer, let the recovery loop run; once it fails, emit one user-facing `tool_result` block per tool use with the stored error message instead of leaking the API’s `max_output_tokens` field.

## Anti-Patterns (What NOT to do)
- Do not throw or propagate the API error immediately; SDK callers might abort and the recovery path would never execute.
- Do not drop the tool_use IDs when rewriting the error, or transcripts/resumes will lose their references.
