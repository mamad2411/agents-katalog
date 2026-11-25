---
name: route
description: Use when you have a question and are not sure which of the six templates applies — classifies it, quotes the cost from measured runs before spending anything, and says so when none of them fits.
argument-hint: your question, one or two sentences, messy is fine
disable-model-invocation: true
---

Read `${CLAUDE_PLUGIN_ROOT}/prompts/06-router.md`. Everything below its "## Copy this block" line is your instruction set — execute it exactly, with one substitution: the "My question:" slot at the end is filled by the user's input below.

My question: $ARGUMENTS

Harness rules:

- If the question above is empty, ask the user what they are trying to find out — do not invent a question, and do not default to a route.
- If the question above is written in Chinese, use `${CLAUDE_PLUGIN_ROOT}/prompts/06-router.zh-TW.md` instead (its block starts at "## 複製這段", the slot is "我的問題：") and work in Traditional Chinese throughout.
- Step 3 is a hard gate. Show the classification and the quote, then stop and wait. Never dispatch a route in the same turn you chose it, even if the user's phrasing sounds impatient — the whole point of the quote is that it arrives before the spend.
- Once the user approves, hand off to the installed command rather than re-implementing the template: `/first-graph` → 00 · `/false-edge-audit` → 01 · `/diamond-research` → 02 · `/adversarial-review` → 03 (give it a file path) · `/consultant-roundtable` → 04 · `/issue-tree` → 05.
- "No route" is a real outcome, not a failure. If the question is answerable in one paragraph, say so and answer it.
