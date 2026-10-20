# AI Elicitation Prompt Patterns

## Summary

**One-sentence:** Reusable prompt-skeleton + slot library for BA elicitation tasks (interview prep, follow-up probes, paraphrase-back validation) with structural validation per call.

**One-paragraph:** Modern BAs run elicitation through a shared LLM (Copilot, Claude, internal RAG). Without a versioned prompt library, every BA reinvents prompts and outputs drift. This methodology codifies a closed pattern set: interview-prep prompts, follow-up question generators, paraphrase-back validators, and persona-driven probes. Each pattern has named slots, a schema for its output, and an eval harness. Output is a `playbook-step` that drops into the elicitation workflow.

**Ефективно для:**

- Stakeholder-interview prep (LLM drafts questions від project brief).
- Follow-up question generation (LLM пропонує наступні probes після initial answers).
- Paraphrase-back validation (LLM перефразовує requirement → BA confirms with stakeholder).
- Persona-driven probing (LLM генерує запитання з точки зору specific persona).

## Applies If (ALL must hold)

- You build, refine, or hand off an LLM workflow used by ≥2 BAs.
- The pattern's output is structurally validated (schema, regex, or downstream parser).
- Cost and latency budget per call are known before authoring.
- Versioning rule for the prompt is in place (Git, registry, or prompt-eval harness).

## Skip If (ANY kills it)

- One-off prompts used once and discarded.
- Output consumed by humans only, with no downstream parser.
- Provider-specific quirks change weekly — register the prompt, do not encode it here.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target model + provider | config (YAML) | infra team |
| Eval harness fixture set | JSONL | BA lead |
| Versioning convention | repo policy doc | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ai-assisted-requirements-elicitation]] | Upstream BABOK-grounded methodology this implements |
| [[ai-acceptance-criteria-generator-reviewer]] | Downstream rubric that scores the output of these prompts |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: slot discipline, schema gate, version tag, cost cap | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema for a prompt pattern + valid/invalid examples | 750 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: slot bleed, schema-less, version-orphan, cost runaway, prompt-injection | 850 |
| `content/04-procedure.xml` | essential | 5-step authoring procedure | 700 |
| `content/06-decision-tree.xml` | essential | Pattern selection by elicitation phase | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prompt_compile` | haiku | Mechanical slot-fill from inputs. |
| `eval_run` | sonnet | Run prompt against ground-truth fixture set. |
| `pattern_refactor` | opus | Identify drift and rewrite skeleton. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-pattern.yaml` | Prompt-pattern skeleton with slots + schema reference |
| `templates/_smoke-test.yaml` | Minimum viable filled pattern for interview-prep |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-elicitation-prompt-patterns.py` | Validate emitted pattern against output-contract schema | CI on each pattern change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-assisted-requirements-elicitation]]
- [[ai-acceptance-criteria-generator-reviewer]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes the BA from elicitation-phase observable (interview-prep vs follow-up vs paraphrase-back vs persona-probe) to a specific pattern + rule from `01-core-rules.xml`. Use when picking which pattern to instantiate for a given stakeholder session.
