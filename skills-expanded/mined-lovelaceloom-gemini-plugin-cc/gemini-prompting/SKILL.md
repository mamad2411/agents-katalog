---
name: gemini-prompting
description: Internal guidance for composing Gemini prompts for coding, review, diagnosis, and research tasks inside the Gemini Claude Code plugin
user-invocable: false
---

# Composing Gemini prompts

Use this skill from inside `gemini:gemini-rescue` (and only there) to tighten a user's free-form rescue request into a more effective Gemini prompt before calling `task`.

This skill draws on Gemini's distinct strengths:
- **Large context window (1M tokens)** — Gemini can absorb whole subdirectories, traces, and long logs at once. Prefer giving it raw context over hand-summarized excerpts when the question depends on cross-file behavior.
- **Strong code analysis** — Gemini is good at tracing data flow, finding inconsistencies across files, and spotting missing handlers.
- **Distinct reasoning style** — Gemini tends to be direct and specific. Don't pad the prompt with Claude-style hedging.

## Prompt structure

A good rescue prompt for Gemini is short, direct, and grounded:

1. **Goal** — one sentence stating what the user wants resolved or answered.
2. **Context** — two to four sentences of relevant repo context (what file/feature is involved, what's known to be broken, what's already been tried).
3. **Constraints** — anything that's off-limits (don't change public API, don't add dependencies, don't touch tests).
4. **Output expectation** — what Gemini should return: an explanation, a diagnosis, a patch plan, or actual code edits.

## Patterns

| User intent | Prompt pattern |
|---|---|
| "investigate why X" | Goal: diagnose root cause. Context: behavior + reproduction. Output: ranked list of suspect causes with evidence. |
| "fix the failing test" | Goal: make `<test name>` pass. Context: test file + recent changes. Output: minimal patch + explanation. |
| "explain how X works" | Goal: explain the data/control flow of `<feature>`. Output: a walkthrough citing files and line numbers. |
| "what should the design be" | Goal: propose a design for `<feature>`. Output: 2–3 options with tradeoffs, then a recommendation. |

## Anti-patterns

- Don't restate the entire repo. Gemini will pull what it needs.
- Don't ask Gemini to "be careful" or "be thorough" — it already is.
- Don't include Claude-internal context like prior tool outputs or scratch notes.
- Don't pre-decide the fix. Let Gemini propose its own approach.

## Model selection

- **Model** — only set `--model` when the user names one (e.g., `gemini-2.5-pro`). Otherwise leave it unset. The plugin resolves the model with this precedence: caller `--model` → `GEMINI_PLUGIN_MODEL` env → workspace `config.activeModel` (set by setup's fallback chain when the default is unavailable for this account) → `DEFAULT_MODEL` in `lib/gemini.mjs` (currently `gemini-3.1-pro-preview`). Do not assume "the CLI default" — the plugin pins the model on every invocation.

## Write mode

- The user's request may include `--write`. Pass it through unchanged. The companion will refuse the call with exit 2 unless `GEMINI_PLUGIN_ALLOW_WRITE=1` is in the env. If you see that refusal in the helper output, return it to the user verbatim — do not try to set the env var, do not retry, and do not strip `--write` from the request to make it succeed silently.

## When NOT to rephrase

If the user's request is already specific and grounded, pass it through verbatim. Rephrasing adds latency and risks losing nuance the user intended.
