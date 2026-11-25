---
name: aiops-implement
description: Delivery overlay — orchestrates lean ladder, tdd, prune, review with sub-phase gates; commits only on user approval.
disable-model-invocation: true
---

# aiops-implement

Implement from PRD, issue brief, or tech-spec. **Not** for grill/alignment — lean active only while writing code.

Invoked by Flow Conductor **delivery** phase (`builder` agent). Update `flow.state.yaml` → `delivery_sub_phase` as you progress.

## Preconditions

- Issue brief or `issues/<current>` AC, or `tech-spec.md` + `NOTES.md`
- `DESIGN_REVIEW.md` APPROVE when design review ran in this flow
- If `/prototype` ran: `VERDICT.md` before absorbing prototype learnings

## Impact analysis (before implement)

If `graphify-out/graph.json` exists, tell the user "查询代码图谱评估修改影响面" then query `/code-graph query impact <target-file>` before writing code to understand the blast radius. Log affected modules in the journey context so the builder knows what might break.

## Orchestration (hard gates — fixed order)

Run sub-phases in order. Do not skip unless user explicitly exempts a step (e.g. mechanical fix → skip new tests).

| Sub-phase | `delivery_sub_phase` | Who | Skill / action | Gate to advance |
| --- | --- | --- | --- | --- |
| 1 | `implement` | builder | lean ladder + write code | Tests for changed behaviour pass |
| 2 | `implement` | builder | `/tdd` at public interfaces | Red-green on agreed surface |
| 3 | `prune` | quality-auditor | `/prune` on diff | Findings listed or "Lean already" |
| 4 | `review` | code-reviewer | `/review` vs NOTES/tech-spec/issue | `REVIEW.md` APPROVE |
| 5 | `ready_for_commit` | — | Set journey gate `ready_for_commit` | User may ask gitops to ship |

Record in journey `gates_satisfied`: `prune_done`, `review_approve`, `ready_for_commit`.

## File size

If any file you touch approaches **500 lines**, invoke `/file-refactor` before advancing to prune — split per that skill (types → utils → hooks → sub-components). Skip only when the user exempts or the file is intentionally monolithic.

## Wave-based execution (when tasks.md has frontmatter)

When `.scratch/<slug>/tasks.md` contains YAML frontmatter with `waves:`, execute tasks wave by wave:

1. Read the `waves` list from frontmatter.
2. For each wave, implement all tasks in the wave (they are independent).
3. After completing a wave, verify tests pass before starting the next.
4. Within a wave, prefer the order listed in the frontmatter.

If no `tasks.md` frontmatter exists, implement tasks sequentially in document order.

**Commit** — only when user explicitly asks. Never commit autonomously. Shipping is `/gitops` in conductor **ship** phase.

Run typechecking and targeted tests during implement; full suite once before `review`.

## Narration (when conductor shows novice text)

Sub-phase 1–2: 「写代码 + 测试」→ sub-phase 3: 「精简 diff」→ sub-phase 4: 「对照设计评审」→ sub-phase 5: 「等你确认再提交」.

## Lean off during grill

Alignment uses `/grill-with-docs` without lean. Switch to lean when sub-phase `implement` starts.
