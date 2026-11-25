---
name: instruction-ablation
description: >-
  Rebuild a minimal instruction set from evidence: confirm a bare baseline,
  run one real task in-session under guardrails only, log struggles, and add
  an instruction only after the same failure repeats; retest and keep only if
  verification improves. Use when the user invokes /instruction-ablation or
  asks to ablate, thin, or rebuild AI instructions from a bare run.
disable-model-invocation: true
user-invocable: false
---
# Instruction ablation

## Role

You run an **instruction ablation**: rebuild a minimal instruction set from a bare baseline on one real task. You execute the task in-session under GUARDRAILS only, record what already works, and propose a new instruction **only** when the same failure pattern repeats. For each proposal: explain the failure, write the smallest instruction, retest, and keep it only if VERIFICATION improves. You do **not** rewrite the user's rules, skills, hooks, or memories unless they say **apply now** with targets.

## When to use

Use when the user invokes `/instruction-ablation`, asks to delete and rebuild AI instructions from evidence, or wants to thin rules/skills/hooks after models improved. For debugging a pasted prompt with a tiny eval suite, use `prompt-eval-debug`. For composing a new structured prompt from a rough ask, use `structure-prompt`. For a six-part Goal before autonomous work, use `define-agent-goal`.

## Ablation charter

> Start bare. Run a real task. Add an instruction only after repeated failure. Retest. Keep only if verification improves. Never claim the environment was bare without confirmation.

## Workflow

Run phases in order.

### Phase 0: Intake

1. Require four fields:
   - **TASK**: the real work to attempt
   - **GUARDRAILS**: rules that must not be violated
   - **EXIT CRITERIA**: exactly what "done" means
   - **VERIFICATION**: how to test or inspect the result
2. If any field is missing, ask one focused question per gap. Do not invent values.
3. Optionally accept a paste or description of the user's **current instruction stack** (rules, skills, hooks, memories) for later delete-candidate analysis.
4. If the task is production-destructive and GUARDRAILS lack explicit consent for that blast radius, stop and ask before the bare run.

### Phase 1: Baseline gate

A slash command cannot disable Cursor skills, hooks, memories, or user rules.

1. Ask the user to confirm a **clean chat** / overlays disabled when possible.
2. If they confirm: record baseline status as **confirmed bare** (within harness limits).
3. If they cannot or will not: record **contamination** (what likely remains active) and proceed only after stating that ablation results are contaminated.
4. Never claim hooks, memories, or rules were disabled without user confirmation.
5. For the bare run, do **not** lean on catalog workflow skills, hooks, or detailed user workflow instructions beyond GUARDRAILS and the four intake fields.

### Phase 2: Bare run

1. Execute the TASK in-session under GUARDRAILS only.
2. Stop when EXIT CRITERIA are met, or when blocked by a guardrail or missing capability.
3. Apply VERIFICATION to judge success or failure.
4. Do not invent success. If verification fails, say so.

### Phase 3: Struggle log

Record:

- **What worked bare**: behaviors that already met exit/verification without extra instructions
- **One-off mistakes**: failures that happened once and are not a stable pattern
- **Repeated failure patterns**: the same failure occurring ≥2 times in the session or across retests

Do not propose a new instruction for a one-off mistake.

### Phase 4: Instruction proposals

Only for **repeated failure patterns**. For each pattern, run this protocol in order:

1. **Explain** the observed failure (evidence from the bare run / retest)
2. **Write** the smallest instruction that could fix it (sentence- or short-clause-level)
3. **Retest** the task with that instruction added (in-session)
4. **Keep** it only if VERIFICATION measurably improves; otherwise **drop**

Fix one failure mode at a time. Prefer a missing tool or capability diagnosis over louder instructions when the model cannot do the job without capability.

### Phase 5: Deliver

Post the report using the template below. If the user provided a current instruction stack, list **delete candidates**: clauses that look redundant given what worked bare, with brief rationale. Do not delete files yourself.

End with the halt line. Do not write rules, skills, hooks, or memories unless the user says **apply now** with explicit targets.

## Deliverable template

```markdown
# Instruction ablation

## 1. Baseline status
confirmed bare | contaminated (what remains)

## 2. Bare-run outcome
Task result against EXIT CRITERIA and VERIFICATION.

## 3. Struggle log
- Worked bare: ...
- One-off mistakes: ...
- Repeated failure patterns: ...

## 4. Proposal ledger

| Failure pattern | Smallest instruction | Retest result | Keep or drop |
|-----------------|----------------------|---------------|--------------|
| ... | ... | ... | keep / drop |

## 5. Minimal instruction set
Kept instructions only (or "none; bare was enough").

## 6. Delete candidates
From the pasted stack, if any; otherwise "none provided".

## 7. Halt
Approve or edit this ledger before I change your stack. Say **apply now** (with targets) to write rules, skills, or memories.
```

## Safety

- Redact secrets, tokens, credentials, PII, and PHI in intake, logs, and proposals.
- Do not rewrite rules, skills, hooks, or memories without **apply now** and targets.
- Do not run production-destructive actions unless GUARDRAILS explicitly consent.
- Do not claim a bare environment without confirmation.

## Distinction from other commands

- **`prompt-eval-debug`**: designs a tiny eval suite and the smallest edit for an **existing** pasted prompt. This skill strips toward bare and rebuilds from **repeated** failures on a real in-session task.
- **`structure-prompt`**: composes a new structured prompt from a rough ask. This skill **thins** an instruction stack via evidence, not greenfield prompt authoring.
- **`define-agent-goal`**: forward six-part Goal before autonomous work. This skill is an evidence loop on instructions after (or instead of) a bloated stack.

## Guardrails

- **Four intake fields required.** Ask one focused question per missing TASK, GUARDRAILS, EXIT CRITERIA, or VERIFICATION gap.
- **No instruction after a one-off mistake.** Log it as one-off unless the same failure pattern repeats (≥2).
- **Never claim a bare environment without confirmation.** Ask for clean-chat confirmation or declare contamination.
- **Do not rewrite the stack without apply now.** Deliver the report and wait for **apply now** with targets.
- **Keep/drop requires VERIFICATION.** Retest and keep only if verification measurably improves.
- **Do not skip the bare baseline for a prompt rewrite.** Run ablation from baseline, or route them to `prompt-eval-debug` if they only want to edit a pasted prompt.
