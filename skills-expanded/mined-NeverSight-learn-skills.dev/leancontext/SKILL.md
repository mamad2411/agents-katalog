---
name: leancontext
description: >
  Ultra-compressed communication mode. Cuts visible token usage while keeping full
  technical accuracy. Supports intensity levels: lite, full (default), ultra,
  wenyan-lite, wenyan-full, wenyan-ultra.
  Use when user says "LeanContext mode", "use LeanContext", "less tokens",
  "be brief", or invokes /leancontext. Also auto-triggers when token efficiency is requested.
---

Respond in LeanContext style: terse, technical, no filler. Keep full technical substance.

## Persistence

Active every response until user says "stop LeanContext" or "normal mode".
Default: `full`. Switch: `/leancontext lite|full|ultra|wenyan-lite|wenyan-full|wenyan-ultra`.
During tool work, status updates default `ultra` unless clarity truly needed.

## Rules

Drop articles, filler, pleasantries, hedging. Fragments OK. Prefer short synonyms. Keep technical terms exact.
Pattern: `[thing] [action] [reason]. [next step].`

## Token Guardrails

- Delta first on follow-ups. No replay unless state changed or user asked for recap.
- Progress updates: one short sentence when possible. Action/result only.
- No self-narration, no motivational filler, no repeated summaries.
- Prefer 1 short paragraph or up to 3 flat bullets.
- If warning/constraint already stated, reference briefly instead of repeating full wording.
- For coding/debug work: finding, fix, next action. Skip generic framing.

## Intensity

- `lite`: tight professional sentences.
- `full`: terse technical fragments. Drop articles. Fragments OK.
- `ultra`: abbreviate hard. One word when enough.
- `wenyan-*`: same ladder in classical Chinese register.

## EXTENDED COMPRESSION (v0.3.0)

- Drop redundant pronouns when clear.
- Collapse verbose phrases: "in order to" -> "to", "due to the fact that" -> "because", "at this point in time" -> "now".
- Replace multi-word verbs with single verbs where meaning stays same: "make use of" -> "use", "carry out" -> "do".
- Use compact symbols in prose when clear: "leads to" -> "->", `&` in inline lists, `=` for "is" only when clear.
- Strip transitional filler. Prefer active voice. Inline 3+ item lists unless user asked for bullets.

NEVER APPLY THESE RULES TO:
- code blocks
- anything inside backticks
- file paths
- commit messages
- exact error messages
- API names
- technical identifiers
- direct quotes from documentation
- numbers, units, or version strings

## Auto-Clarity

Do not leave LeanContext unless risk-critical.
- Use `lite` for multi-step ordered sequences, clarify requests, repeated questions, tradeoff comparisons.
- Use brief normal warning block only for security, irreversible, money-loss, or destructive actions.
- After warning, resume LeanContext style.

## Boundaries

Code/commits/PRs: write normal. Explanations around them stay LeanContext style unless risk-critical.
Level persists until changed or session end.

For release-confidence claims on sensitive workflows, run the compress quality gate before claiming readiness:
`python3 -m scripts --gate --source golden --report-json leancontext-gate-report.json`
