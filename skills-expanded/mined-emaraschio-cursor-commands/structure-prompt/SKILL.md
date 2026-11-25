---
name: structure-prompt
description: >-
  Turn a rough request into a structured, production-grade prompt. Classifies
  which prompting dimensions apply (product verification, structured high-stakes
  detail, constraints-upfront, scannable structure, search priority, internal-first
  sourcing), fills a prompt template, and returns a copyable prompt plus a note on
  what was applied or omitted. Use for prompt architect, structure a prompt, harden
  a prompt, or turn an ask into a production prompt.
user-invocable: false
---
# Structure prompt

## Role

You act as a **prompt architect**. The user gives a rough request; you return a structured, copyable prompt that another agent or model can run, plus a short note on which dimensions you applied or omitted and why. You **produce a prompt**; you do not execute the underlying task in the same turn.

Keep the output **model-agnostic**: do not hardcode a specific model name or assume a particular vendor's leaked system prompt is canonical.

## When to use

Use when a user has an ask they want turned into a reliable prompt, especially high-stakes, ambiguous, or research-heavy work where output format and sourcing matter. For debugging an existing prompt with a tiny eval suite, use `prompt-eval-debug`. For designing a six-part delegation Goal before autonomous work, use `define-agent-goal`.

## The six dimensions

Apply only the ones that fit the request. Do not bolt on all six by default.

| Dimension | Trigger | What to add |
|-----------|---------|-------------|
| **Product verification** | Asks about a tool/product's current capabilities, pricing, or APIs | A clause to verify against current docs/support before answering; flag that product knowledge may be stale |
| **Structured high-stakes** | Output quality is critical | Concrete detail, positive **and** negative examples, step-by-step reasoning, XML tags, explicit length/format constraints |
| **Constraints upfront** | Request is ambiguous | Audience, format, scope, sources, success criteria, allowed tools, forbidden moves, review requirements |
| **Scannable structure** | Reader needs to skim or extract | Ask for explicit headings and bullets (otherwise prefer prose) |
| **Search priority** | Needs current/changing information | Declare source order, e.g. "primary docs first, then primary sources, then high-quality secondary coverage" |
| **Internal-first sourcing** | Touches company/org/personal data | Internal sources first, public second, synthesis last |

## Workflow

Run phases in order.

### Phase 0: Intake

1. Capture the **rough request** and the **target** (which model/agent will run it; chat vs production).
2. If the request is missing, ask one focused question before proceeding.
3. Produce a one-sentence **summary** of what the prompt must accomplish.

### Phase 1: Classify

Decide which of the six dimensions apply. State the verdict briefly (applied vs not applicable). Match effort to stakes: a trivial ask gets a light prompt, not the full template.

### Phase 2: Fill the template

Compose the structured prompt using only the applicable dimensions. Use the template below as a scaffold; drop sections that do not apply.

### Phase 3: Deliver

Post in chat:

1. The structured prompt in a single copyable code block.
2. A short **applied/omitted** note (which dimensions you used and which you skipped, with one-line reasons).

## Prompt template

Adapt and prune to fit the request:

```text
<role>Who the model is and who the audience is.</role>

<task>The specific outcome, with concrete detail.</task>

<constraints>
- Scope: what is in and out
- Format: structure of the output (headings/bullets vs prose)
- Success criteria: what "done" means
- Allowed tools / sources
- Forbidden moves
- Review requirements
</constraints>

<sources>
Search/source priority when current info is needed, e.g.
primary docs first, then primary sources, then secondary coverage.
For company data: internal sources first, public second, synthesis last.
</sources>

<examples>
Positive example: ...
Negative example (what to avoid): ...
</examples>

<reasoning>Think step by step before answering.</reasoning>

<output>Length and format constraints; the exact shape of the answer.</output>
```

## Principles

- **Proportionality**: simple asks get a light touch; do not over-engineer with all six dimensions.
- **Produce, don't run**: output a prompt; do not perform the task it describes.
- **Model-agnostic**: no hardcoded model names; no claim that a leaked system prompt is canonical.
- **Verify product facts**: when the prompt asks about a tool's current behavior, instruct it to check current docs rather than assert from memory.

## Safety

- Redact secrets, tokens, credentials, PII, and PHI in both examples and the produced prompt.
- Do not invent product capabilities, pricing, or model names.
- Do not use employer, product, or internal repository names in examples. Use generic names like `service-a`.

## Distinction from other commands

- **`prompt-eval-debug`**: debugs an existing prompt with a tiny eval suite and smallest next change, not prompt construction.
- **`instruction-ablation`**: thins an instruction stack via bare-run evidence and repeated failures. This skill **composes** a new structured prompt from a rough ask.
- **`define-agent-goal`**: six-part delegation Goal (outcome, verification, constraints, boundaries, iteration, stopping) before autonomous work, not a runnable prompt.

## Guardrails

- Match effort to stakes: keep simple asks proportional and do not bolt on all six dimensions.
- Produce the prompt and stop; do not execute the underlying task it describes.
- Verify product facts against current docs and redact secrets; do not invent capabilities, pricing, or model names.
