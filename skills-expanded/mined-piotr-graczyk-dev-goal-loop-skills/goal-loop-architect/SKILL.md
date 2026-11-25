---
name: goal-loop-architect
description: Build launch-ready prompts for goals, autonomous loops, research loops, execution loops, review loops, monitoring loops, or long-running agent tasks. Use when the user wants to create, improve, or normalize a goal/loop prompt with explicit scope, evidence rules, validation, output contract, conflict handling, stop condition, and one-at-a-time clarification when required facts are missing.
---

# Goal Loop Architect

Turn rough intent into a self-contained prompt another agent can run without hidden context. Optimize for verifiable work, bounded scope, and early clarification.

## Non-Negotiable

If a blocking fact is missing, ask exactly one next question. Include `Recommended answer:`. Never return a numbered list of multiple questions.

Before asking, inspect or infer from available context: the user prompt, pasted artifacts, repo files, docs, current branch, issues, or other provided sources. Do not ask for facts you can discover safely.

Recommended answers should preserve momentum without inventing concrete facts. Use generic defaults like `current repo`; use `current branch` only for branch-scoped execution or review. Do not name a specific repo, org, path, branch, or product as the target unless the user supplied it or the task clearly says to use the current workspace. Prefer soft defaults over hard exclusions, and mark broad defaults as assumptions.

Launch prompts should be compact. Preserve every required contract and the fenced `text` output format, but avoid repeating the same rule across `RULES`, `METHOD`, `STOP CONDITION`, and `DONE CRITERIA`.

## Workflow

1. Classify the loop: `research`, `execution`, `review`, `monitoring`, or `mixed`.
2. Load only relevant references:
   - `references/prompt-patterns.md` for research, execution, or review loops.
   - `references/question-bank.md` when a blocking fact is missing.
   - `references/quality-rubric.md` before returning a launch prompt.
   - `references/examples.md` only when examples or substantial reshaping are needed.
3. Run the Fact Gate in order.
4. If the earliest blocking fact is missing, return one clarification.
5. After an answer, inspect newly available context before asking another question.
6. Otherwise return the launch prompt.

## Fact Gate

Know these facts before producing a final prompt. When several are missing, ask only about the earliest one that cannot be inferred.

- `PROJECT`: repo, product, domain, target system, branch, or artifact.
- `GOAL`: one-sentence deliverable, not a broad topic.
- `SCOPE`: included work and explicit exclusions.
- `RULES`: observable acceptance, verification, or validity criteria.
- `SOURCES`: allowed evidence sources and source hierarchy.
- `OUTPUT`: artifact type, location/name, count, schema, or required sections.
- `ON CONFLICT`: how to handle contradictory evidence or instructions.
- `STOP CONDITION`: when to halt instead of guessing.

For long-running loops also define `CHECKPOINTS`, `BUDGET`, `PERMISSIONS`, and `DONE CRITERIA`.

## Output

Return one of these shapes.

```text
Clarification needed

[Ask exactly one next blocking question.]

Recommended answer: [your recommended default or the answer most likely to preserve momentum.]
```

If useful, add one short `I will inspect/use:` line before the question naming context you can check first.

```text
Launch prompt

# PROJECT: [name / repo / domain]

GOAL: [one sentence]
MODE: [research | execution | review | monitoring | mixed]

CONTEXT:
- [facts needed by another agent]

SCOPE:
- In: [included work]
- Out: [explicit exclusions]

RULES:
- [observable acceptance or verification rules]

SOURCES:
- [allowed sources in priority order]

METHOD:
- [ordered workflow]

OUTPUT:
- Format: [message/file/table/PR/report/etc.]
- Location/name: [path or naming rule]
- Required fields/sections: [schema or outline]

ON CONFLICT:
- [how to flag contradictions]

STOP CONDITION:
- [specific halt cases]

CHECKPOINTS:
- [if needed]

DONE CRITERIA:
- [observable success]
```

Use `ASSUMPTIONS` only for non-blocking assumptions. Do not emit a final launch prompt when deliverable, scope boundary, validation rule, output contract, or stop condition is blocking-missing.
