---
name: model-bench
description: Run a 3-leg evaluation against a newly released LLM. Leg 1 is trap questions with deterministic answers, leg 2 is an agentic orchestration task with a planted failure, leg 3 is a brownfield feature build in a real repo. Use when the user wants to vibe-check, test, evaluate, or compare a new frontier model, or mentions model-bench, model vibe check, or launch-day protocol.
disable-model-invocation: true
---

# model-bench

3 legs, each aimed at a different failure mode:

1. **Trap questions**: does it think, or pattern-match to training data? Deterministic answers, grades in seconds.
2. **Orchestration**: can it plan, delegate, and recover when a step fails (including a planted trap)?
3. **Brownfield build**: can it ship a feature into an existing codebase without breaking things 2 files away?

Each leg scores 0-5. Total out of 15.

## Contamination rules (read first)

- The model under test must NEVER see gold answers or learn about the planted trap. If it does, that leg is void.
- **Private answer key** lives outside this repo: `~/proctor/model-bench/answer-key.md` (or `grading/answer-key.local.md`, gitignored). Public stub: [grading/answer-key.md](grading/answer-key.md). Legs 2–3 checklists: [grading/rubrics.md](grading/rubrics.md).
- This skill runs in a **proctor session** (Nate plus a model he already trusts). The model under test only ever receives the task prompts — never this skill folder, never the private key.
- **Never use this repo as the target repo** for legs 2–3.
- **Leg 1 isolation:** launch each question in a context with **no access to this workspace** (no tools / empty workspace / chat-only). If the target model can `Read` files here, the leg is void.
- One fresh session per leg. No custom system prompts or rules that would coach the model.

## Workflow

```
Progress:
- [ ] Setup: pick target model, pick target repo, verify leg 2 plant
- [ ] Leg 1: proctor launches 5 parallel subagents (one question each), record final answers
- [ ] Leg 2: paste orchestration task into a fresh agent session on the target repo
- [ ] Leg 3: paste brownfield spec into a fresh agent session, branch per model
- [ ] Grade leg 1 with the private answer key; legs 2–3 with grading/rubrics.md
- [ ] Fill scorecard, save to results/, write 2-3 sentence verdict per model
```

**Setup**
- Target repo for legs 2-3: a real repo with existing conventions, ideally one Nate knows well enough to judge output quality. Never this repo.
- Verify the leg 2 planted path (default `docs/METRICS.md`) does not exist in the target repo. If it does, pick another plausible-but-missing path and note it.
- When comparing models, use identical prompts, identical repo state, and a fresh branch per model (`vibe/<model-name>`).

**Run the legs**
- Leg 1 prompts + proctor protocol: [tasks/leg-1.md](tasks/leg-1.md)
- Leg 2 task: [tasks/leg-2.md](tasks/leg-2.md)
- Leg 3 spec template: [tasks/leg-3.md](tasks/leg-3.md)

**Leg 1 (proctor-driven)**
The proctor AI runs leg 1. Do not make the human paste questions.
Launch 5 parallel subagents with the target model slug, each receiving exactly one fenced question from `tasks/leg-1.md` and nothing else. Record final answers only.
**Isolation:** those subagents must not be able to read this repo (no tools, or empty/disposable workspace). Same-workspace leg 1 = void.
If the target model has no subagent slug (common on launch day), use five fresh chats the same way — still proctor-driven, not human paste.
Do **not** use subagents for legs 2–3 in this workspace. Those legs run in separate sessions on the target repo.

**Grade**
- Leg 1 gold: private key at `~/proctor/model-bench/answer-key.md` (see [grading/answer-key.md](grading/answer-key.md) stub)
- Legs 2–3: [grading/rubrics.md](grading/rubrics.md)
- Only open the private key after all legs have been run, and never in a session where the target model is active.

## Results

Save each filled scorecard to `results/YYYY-MM-DD.md` (append `-2`, `-3` for multiple runs on one day). Use this template:

```markdown
# Vibe check: [date]

Target repo: [repo]
Leg 2 plant: [path used]
Leg 3 spec: [feature, one line] / planted ambiguity: [what it was]

| Leg | [Model A] | [Model B] | [Model C] |
|---|---|---|---|
| 1. Trap questions (/5) | | | |
| 2. Orchestration (/5) | | | |
| 3. Brownfield (/5) | | | |
| **Total (/15)** | | | |

Verdict per model: which legs it won, what surprised me, does it earn a spot in the rotation.
```

## Notes

- Public trap questions decay. When a question gets 3 passes in a row across model families, retire it and add a fresh one to the bank.
- Different models winning different legs is the expected (and most interesting) result. Record it, it's post material.
