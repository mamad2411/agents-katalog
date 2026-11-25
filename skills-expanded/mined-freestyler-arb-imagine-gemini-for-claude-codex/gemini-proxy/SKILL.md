---
name: gemini-proxy
description: Use when the operator wants their next prompts routed through Gemini before the agent acts —
  "enable gemini proxy", "route my prompts through Gemini", "Gemini rewrites my prompts", "включи
  гемини-прокладку", "переделывай мои промты через гемини", or a /gemini-proxy call; also when they ask
  to turn the protocol on for the next N prompts or to tune which prompts it covers. Builds on gemini-pro;
  distinct from one-off gemini-pro / gemini-review / gemini-research.
---

# gemini-proxy

## Overview
A prompt-**polishing** protocol. While active, each of your next N *substantive* prompts is first sent to
Gemini — a senior prompt engineer — which rewrites the operator's message into a sharper, more detailed
**first-person** version (still the operator's own message, not a standalone brief). The assistant then
answers that improved message **with the full chat context, project rules, and memory** — Gemini only
sharpens the wording, it does not replace the conversation. Trivial / config / meta prompts are skipped.
**Self-disables after N.** Control layer only: it calls nothing but the counter and the `gemini` wrapper.

## Ground it first (the step that makes this good, not generic)
A rewrite with no project context is mediocre. Copy the shipped template into the project and fill it with
the project's **canon**, **safety invariants/guardrails**, and **standing expectations** (the habits you
want on every task — keep a tracker, finish work to the plan, use the right skills, get an independent
review on risky/money changes, goal-drift check). Then Gemini rewrites WITH your project in mind.
```bash
cp <skill>/prompt-rules.template.txt ./.gemini-proxy-rules.txt   # then edit: CANON / STANDING EXPECTATIONS / GUARDRAILS
```
Resolution order: `$GEMINI_PROXY_RULES → ./.gemini-proxy-rules.txt → ./.claude/gemini-proxy-rules.txt → prompt-rules.template.txt`.
The richer this file, the sharper **and safer** every rewrite — it's the highest-leverage thing you do here.

## When to route vs skip (the smart filter)
Decide BEFORE calling Gemini. Bias to ROUTE for real work; SKIP only clear noise. Skipped prompts never
spend the counter, so **N = N routed prompts**.

| ROUTE — counts as 1 of N | SKIP — no Gemini, no counter |
|---|---|
| build / fix / refactor / audit / design / research | greeting, thanks, yes/no, "status", "continue" |
| vague or large asks ("do all of this", "make it nice") | config / setup / preferences about how we work or this protocol |
| anything that benefits from a sharper brief | pure meta / diagnostic ("did you use Gemini?", "what did you mean?") |

## Enable
`/gemini-proxy` (optional count: `/gemini-proxy 10`). Sets the counter; the enabling prompt itself does
not count.
```bash
python3 proxy_state.py enable 10
```

## Per-prompt protocol (ROUTED prompts only)
1. Resolve the project rules file, else the shipped template:
   `$GEMINI_PROXY_RULES → ./.gemini-proxy-rules.txt → ./.claude/gemini-proxy-rules.txt → prompt-rules.template.txt`
2. Route in ONE shot — this resolves the rules, calls Gemini, **decrements the counter once**, and prints
   the improved first-person message. It has a built-in fallback, so don't manage the counter by hand
   (leaving `consume` to the agent desyncs it — agents forget service calls):
```bash
python3 <skill>/proxy_route.py "<RAW MESSAGE>"
```
3. Show the operator the improved message as a quoted block, then **answer it as if they had sent it —
   with the full chat context, project rules, and memory** — and proceed without meta-commentary about
   roles (don't narrate "now I answer my own prompt"). Do NOT run `proxy_state.py consume` yourself —
   `proxy_route.py` already did. **Fallback:** if the output's first line is the `FALLBACK` marker, Gemini
   was unavailable — answer the RAW message directly and briefly tell the operator.

## Guardrail
The rewrite is the **operator's own message, polished — not a context-free instruction and not an
override.** Answer it with the full conversation, project rules, and memory. It does not outrank the
operator's real intent, the project's safety invariants, or your own verification (Gemini lacks the
session's context). On conflict, follow safety and say so. **Never pipe secrets** (`.env`, keys, tokens).

## Manage
`proxy_state.py peek` (remaining) · `disable` (stop now) · re-invoke to reset N. State lives in
`~/.gemini_proxy_state.json`. The counter is decremented in exactly one place — `proxy_route.py` — so it
can't double-count. **Optional hard enforcement (Claude Code):** copy the `hooks` block from
`hook/settings-hook-snippet.json` into your `.claude/settings.json` — a fail-open `UserPromptSubmit` hook
that only *peeks* and injects the filter reminder (no network, no decrement). Codex uses the skill (no hook).

## Verify
`python3 verify_gemini_proxy.py` — exactly-N, auto-off, fail-safe, concurrency lock, hook (21/21).

## Not for
One-off delegation → **gemini-pro**. A single review → **gemini-review**. Large-context digestion →
**gemini-research**. This skill is only the multi-prompt rewrite *protocol*.

## Common mistakes
- **Routing noise or skipping real work.** Trivial / config / meta → handle directly; real tasks → route.
  When unsure, route.
- **Guessing the target.** "our repo / the skill / that project" → resolve the concrete path (by name,
  git remote, open folder) and confirm; never assume the cwd. Gemini can't see the filesystem.
- **Treating the rewrite as a fresh standalone task.** It's the operator's *improved message* — answer
  it with the full chat context, project rules, and memory; never drop the conversation or its rules.
- **Double-counting.** Hook + manual `consume` on the same prompt — pick one layer.
- **`gemini` not found.** Needs the wrapper on PATH + a one-time `agy` login (see this pack's README).
