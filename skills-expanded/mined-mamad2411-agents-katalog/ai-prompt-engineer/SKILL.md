---
name: ai-prompt-engineer
description: Prompt design specialist. Auto-invoked when prompts, system messages, few-shot examples, structured-output schemas, or chain-of-prompt chains are being written or iterated.
---

# AI Prompt Engineering

Vague prompts are how LLM apps regress silently. A prompt is code: specific,
versioned, schema-bound, and covered by a regression run.

## When to reach for this

- Writing or iterating system prompts, task prompts, or few-shot examples
- Defining structured-output schemas (JSON schema, tool schemas) and their validators
- Decomposing a task into a prompt chain with typed handoffs
- Injecting dynamic context (RAG chunks, tool outputs) into a template safely

## Principles

1. **Be specific, then more specific.** The most common prompt bug is
   underspecification — state edge-case behavior explicitly ("if no answer is
   found, return an empty `results` array") instead of hoping.
2. **Output schema is the contract.** Ask for JSON against a schema and validate
   every response in code; retry-on-invalid with the validator error fed back
   beats "please be careful" every time.
3. **Few-shots earn their tokens.** One well-chosen example outperforms ten
   instructions for format — but each example costs tokens on every call;
   measure the delta on the eval set before keeping it.
4. **Stable ordering: instructions → examples → dynamic context → input.** Long,
   static parts first (this also maximizes prompt-cache hits); restate the task
   in one line at the end on long contexts.
5. **Version prompts like code.** Prompts live in the repo, diff-reviewed, with a
   prompt ID/version logged on every call so production outputs trace back to
   the exact prompt that produced them.
6. **Delimit untrusted context.** Wrap retrieved chunks and tool outputs in
   clearly marked tags and tell the model they are data, not instructions.
7. **No prompt ships without an eval run.** Before/after on the same labeled set;
   a prompt change with no regression run is an unreviewed deploy.

## Prompt skeleton

```text
[system]
Role and task in 2–3 sentences. Hard constraints.
Output schema or format spec (the same one the code validates against).
Edge-case behavior: empty input, no answer found, conflicting sources.

[examples]            # optional, 1–3, format-matched to current schema
input → expected output

[context]             # dynamic, delimited, declared as data
<documents>
  <doc id="1" source="...">…retrieved chunk…</doc>
</documents>

[user]
The actual input — then a one-line restatement of the task.
```

## Pitfalls

- Schema requested in prose but never validated in code
- Few-shot examples drifted from the current schema — the model copies examples
  over instructions, so stale examples win
- Dynamic context concatenated raw: an injection vector and a cache-buster in one
- Prompt edits "fixing" a bug that is actually bad retrieval (check recall first)
- Negation-only instructions ("don't mention X") with no positive alternative
- No prompt version in logs — a production incident can't be traced to the change

---
*Related: `ai-rag` (the context being injected), `ai-eval` (regression runs on
prompt changes), `ai-safety` (injection defense for untrusted context),
`api-design` (tool/output schemas as API contracts) · domain agent:
`ai-architect` (model selection) · output/ADR format: `playbook-conventions`*
