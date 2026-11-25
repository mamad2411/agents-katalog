---
name: token-efficient-prompting
description: Reduce input and output tokens consumed by AI coding assistants and LLM calls without losing answer quality. Use when prompts feel bloated, costs are climbing, agent loops thrash, or responses are unnecessarily verbose.
source: self
date_added: 2026-05-01
---

# Token-Efficient Prompting

Every token costs money, latency, and context-window space. Treat the prompt as code you optimize.

## When to Use

- Copilot/agent sessions burn through quota faster than expected.
- LLM API bill is dominated by input tokens (usually means context bloat).
- Responses are long-winded, repeat the question back, or include filler.
- Agent re-reads the same files multiple times in a single task.
- You are designing a system prompt or tool description that runs on every call.

## Core Rules

1. **Tokens in = tokens paid.** Input is usually 70-90% of cost. Trim ruthlessly.
2. **Specify the output shape.** Vague asks produce verbose answers.
3. **Don't restate what the model already knows.** No "You are an AI assistant..." preamble for capable models.
4. **One job per prompt.** Multi-task prompts waste tokens on partial outputs you discard.
5. **Cache the static parts.** System prompts, schemas, examples should sit in prompt-cache friendly positions (front of context).

## Input-Side Optimizations

| Bloat source | Fix |
| --- | --- |
| Pasting whole files | Paste only the relevant function + signatures of callers |
| Large JSON / logs | Truncate, sample, or summarize before sending |
| "Here is the codebase..." dumps | Send a file index + load on demand |
| Repeated boilerplate per call | Move into cached system prompt |
| Long chat history | Summarize older turns into a rolling 1-3 sentence digest |
| Verbose few-shot examples | Use 1-2 minimal examples, not 5 elaborate ones |
| Markdown decoration in data | Send as compact JSON/CSV/TSV instead |

## Output-Side Optimizations

- Demand a format: "Reply with only the diff", "Return a JSON object with keys X, Y", "One sentence".
- Set `max_tokens` to a realistic ceiling. Don't rely on the model to stop.
- Forbid filler explicitly: "No preamble. No apologies. No restating the question."
- For yes/no or classification, ask for a single token answer.
- Stream and cancel early when you detect the answer is wrong/done.

## Prompt Structure That Saves Tokens

```
[SYSTEM — cached]
Role + non-negotiable rules. ~200 tokens max.

[CONTEXT — minimal, ordered stable→volatile]
Schema, then examples, then task-specific data.

[TASK]
One sentence. Imperative.

[OUTPUT FORMAT]
Exact shape, with a stop condition.
```

Order matters: providers (Anthropic, OpenAI) cache prefixes. Putting volatile data last preserves the cache hit on the static prefix.

## Working With Coding Agents (Copilot, Cursor, Claude Code, Codex)

- **Be specific about files.** "Edit `auth/login.ts`" beats "fix the login bug" — the latter triggers exploratory searches.
- **Front-load constraints.** State the acceptance criteria up front so the agent doesn't loop.
- **Cap exploration.** "Read at most 3 files before proposing a change."
- **Reuse prior context.** Don't restart sessions for related follow-ups; the model already has the relevant code in context.
- **Prefer diffs over rewrites.** Asking for a full file rewrite when you need 5 lines wastes 10x output tokens.
- **Disable unused tools.** Each tool definition adds tokens to every call.

## Few-Shot Discipline

- 0 examples beats 1 bad example.
- 1 great example often beats 3 mediocre ones.
- Strip examples to the minimum tokens that show the pattern (no narrative wrapping).
- Reuse the same example across calls so prompt caching kicks in.

## Measuring

Track per-task: input tokens, output tokens, cached tokens, $ cost, time to result, success rate.
You cannot optimize what you don't log. A single dashboard with cost-per-successful-task drives more savings than any individual trick.

## Quick Wins Checklist

- [ ] Removed "You are a helpful assistant..." style preambles
- [ ] System prompt < 500 tokens and stable across calls (cacheable)
- [ ] No file dumps > 200 lines without a reason
- [ ] Output format pinned (JSON schema, regex, or "one line")
- [ ] `max_tokens` set
- [ ] Few-shot examples stripped to essentials
- [ ] Tool list pruned to what this task actually needs
- [ ] Logging input/output/cached tokens per call

## Anti-Patterns

- "Think step by step" added to every prompt regardless of task — burns output tokens.
- Re-sending entire chat history when a 1-line summary would do.
- Dumping `package.json`, `tsconfig.json`, full schemas "for context" the model never uses.
- Using a frontier model for a task a small model handles fine (model-fit is the biggest cost lever).
- Optimizing prompts by hand without measuring the result.

## References

- Anthropic prompt caching documentation
- OpenAI "Prompt engineering" and pricing pages
- "Efficient prompting via Mode-Aware Decoding" — survey of compression techniques
- Related skills: `context-window-management`, `llm-cost-optimization`
