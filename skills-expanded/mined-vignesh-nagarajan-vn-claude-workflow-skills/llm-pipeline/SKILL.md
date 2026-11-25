---
name: llm-pipeline
description: Architecture rules for code that calls an LLM. Code owns the decision, schemas validate every model output, keys stay server-side, and a mock provider keeps demos and tests keyless. Use when adding or changing an LLM call, designing a multi-pass or multi-agent pipeline, choosing which model handles which pass, or reviewing an app that talks to Claude or another provider. Runs scripts/audit_llm_app.py.
---

# llm-pipeline

## Audit an existing app first

```bash
python <skill>/scripts/audit_llm_app.py
```

It reports keys reachable from the browser, model output parsed without a schema, Next.js LLM routes with no `maxDuration`, and an inventory of which models are called from where. Deep checks run only on files that import an SDK, so the output stays short.

The model inventory is worth reading even when there are no findings. It is the fastest way to see that an expensive model is doing a job a cheap one should.

## The five rules

**1. The model justifies, the code decides.** The model returns a per-item verdict with its reasoning. Any arithmetic, threshold, score, or final label is computed in code from those verdicts. When the rules change you edit one function, and the decision is inspectable without rerunning anything.

**2. Every model output is schema-validated.** Never `JSON.parse` a completion and use it. Where the provider supports structured outputs (on the Claude API, `output_config.format` or `strict: true` on a tool), let it enforce the schema and skip the repair loop. Still check in code what a schema cannot express, and treat a refusal or a `max_tokens` stop as a failure. Where it does not, parse into a schema, feed the validation error back for a bounded number of repair attempts, then fail loudly. Unbounded repair loops are how a 3-cent call becomes a 3-dollar one.

**3. Keys never reach the client.** All provider calls happen server-side. No `NEXT_PUBLIC_` secret, no `dangerouslyAllowBrowser`. The audit catches all three forms.

**4. A mock provider ships alongside the real one.** Same interface, deterministic output, no key needed. It makes tests fast and free, keeps CI keyless, and gives you a demo that works when the key is missing or the budget is gone.

**5. Long pipelines stream their stages.** A six-stage pipeline that returns one blob after ninety seconds looks broken. Emit one event per stage.

## Cost tiering

The largest cost lever is which model runs which pass, not prompt wording.

| Pass | Model tier |
| --- | --- |
| Retrieval, extraction, classification, routing, reformatting | cheap |
| Drafting where a critic reviews after | mid |
| Adjudication, final judgment, anything whose output is the product | expensive |

Two more that compound: put the stable part of a long prompt first so it can be cached across calls, and cap `max_tokens` to what the schema actually needs.

## Detail

Read [references/patterns.md](references/patterns.md) when implementing one of these, not before. It has the shapes for structured outputs, the repair loop, the mock provider, the critic pass, stage streaming, and provenance.

## Reviewing a change

Ask: if the model returns something absurd, what stops it reaching the user? If the answer is a prompt instruction, that is not an answer. Schema, code-side arithmetic, or a critic pass is.

Prose in comments and docs follows [prose-guard's rules](../prose-guard/references/rules.md).
