---
name: adversarial-research
description: "Research a topic adversarially: attack provisional theses and present only the most defensible conclusion under an explicit evidence boundary."
version: 0.1.0
author: Trevor Longino
license: CC-BY-4.0
---

# Adversarial Research

## Purpose

Use this skill when a question merits iterative, source-grounded research rather than a one-pass summary.

The objective is to present the **most defensible conclusion** the accessible evidence supports. Do not stop because a report sounds convincing, a nominal cycle count is reached, or a critic likes the prose. Continue until either:

- the report meets the program's evidence, traceability, uncertainty, and usefulness thresholds; or
- a material gap remains but another bounded cycle is unlikely to improve the accessible evidence state.

See [docs/definition.md](docs/definition.md) for the project definition.

## Setup before the first cycle

1. Read `adversarialresearch.config.yaml` from the research project if present; otherwise copy `config/adversarialresearch.config.example.yaml` into the project.
2. Resolve the **primary** and **critic** model roles using the config.
3. Check the configured credential environment variables without printing values.
4. If a required role has no usable host authentication or key, stop before research and tell the operator exactly which provider/model/key is needed. Do not invent a credential, silently reuse a key intended for another provider, or downgrade to a single-model “adversarial” loop.
5. Record which model/provider actually filled each role and whether the critic was independent.

The primary model may inherit the host agent's active model. The critic should be a separately configured model/provider whenever possible. If the same model must fill both roles, record the reduced independence prominently; it is not equivalent to independent adversarial review.

## Required program

Before retrieval, create `program.md` containing:

- one narrow question;
- scope and date window;
- source hierarchy;
- required report sections;
- evaluation rubric;
- explicit keep/discard criteria;
- unresolved-unknown definition;
- stop policy.

## Cycle protocol

1. **Map or target a specific gap.** Each cycle has a distinct objective: map, repair, falsify, operationalize, or adjudicate.
2. **Collect a bounded evidence packet.** Preserve canonical URL, source type, what it establishes, limitations, retrieval status, and relevant excerpt. Search snippets are discovery leads, not evidence.
3. **Write a provisional candidate.** Separate fact, reported claim, inference, and unknown. Include a claim ledger.
4. **Attack the candidate.** The critic must seek counterevidence, unsupported claims, causal leaps, incomparable units, selection effects, and the strongest plausible alternative thesis. Require severity-ranked repairs.
5. **Adjudicate against the prior best.** Keep only material improvement: verified/narrowed major claims, repaired high-severity gaps, removed false claims, comparable units, or a better-resolved alternative thesis.
6. **Emit exactly one decision and stop verdict.**
   - `KEEP` or `DISCARD`
   - `PRESENT TO HUMAN`, `CONTINUE`, or `STOP AS BEST AVAILABLE`
7. **Update state only after valid KEEP.** Preserve discarded candidates and critic output internally.

## Artifact contract

Use the helper in `src/adversarialresearch/runtime.py` for state and structural verification:

```bash
python3 src/adversarialresearch/runtime.py init --project-dir ./research --project my-question --question "..."
python3 src/adversarialresearch/runtime.py verify --file ./research/runs/run-001/final-adjudication.md --cycle 1
python3 src/adversarialresearch/runtime.py event --project-dir ./research --cycle 1 --decision KEEP --stop-verdict CONTINUE
python3 src/adversarialresearch/runtime.py guard --project-dir ./research
```

The agent is responsible for model calls and collection. The helper is responsible only for durable state and validation.

## Failure rules

- A retrieval failure is a retrieval limitation, not evidence for the thesis.
- A critic timeout or credential failure is not adversarial validation.
- Do not replace unavailable evidence with model memory.
- Do not silently change provider/model roles.
- Do not publish raw credentials, provider responses, source packets, or internal prompts by default.

## Final answer shape

Present only the kept research state. State:

- conclusion;
- evidence boundary and source quality;
- strongest counterargument considered;
- key uncertainty/unknowns;
- whether this is `PRESENT TO HUMAN` or `STOP AS BEST AVAILABLE`;
- exact reopening condition if stopped.
