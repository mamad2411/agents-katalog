---
name: gemini-result-handling
description: Internal guidance for presenting Gemini helper output back to the user
user-invocable: false
---

# Presenting Gemini output

Use this skill from the main Claude Code thread when surfacing output from a Gemini companion command (review, adversarial-review, task, result).

## Default rule: verbatim

Return Gemini's stdout to the user **verbatim**. Do not paraphrase, summarize, re-style, or "improve" the output. The user invoked Gemini deliberately to get a second opinion in Gemini's voice — sanitizing it through Claude defeats the purpose.

## When to add framing

Wrap Gemini's output in a short header **only** when:
- It came from `/gemini:rescue` and the user might not realize a delegation just happened. A one-line "Gemini's response:" header is fine.
- It came from `/gemini:review` and arrived inside an `AskUserQuestion` flow where the user picked "background". A one-line follow-up "Gemini review (job <id>) completed — output above" is fine.

## When NOT to add framing

- `/gemini:ask` — the user asked a direct question, just return the answer.
- `/gemini:status` — the companion already renders a Markdown table; pass it through.
- `/gemini:result` — the output is already structured. Don't re-format.

## Auth-error hints

If the companion's stderr contains a `[hint: ...]` line, surface that hint to the user and suggest `/gemini:setup`. Do not try to recover yourself.

## JSON review output

If `/gemini:review --json` was used, the companion strips Gemini's wrapper (`{session_id, response, stats}`), removes markdown code fences, and emits clean JSON. The shape is checked against `schemas/review-output.schema.json` at the top level (verdict / summary / findings / next_steps must be present and verdict must be in the enum); deeper field-level validation is the caller's responsibility. When forwarding it:
- If the user asked for JSON specifically, pass it through unmodified.
- If the user did not ask for JSON, render the JSON into a compact Markdown report grouped by `severity`. Preserve `file`, `line_start`, `line_end`, and `recommendation` for each finding.
- If the companion's stderr contains `schema mismatch`, surface that warning along with the raw output — Gemini may have ignored the schema instruction.

## Background jobs

When `/gemini:rescue` is launched in background mode, the companion writes to a log file and reports the job ID. Tell the user to run `/gemini:status` or `/gemini:result <id>` later — do not poll on their behalf.
