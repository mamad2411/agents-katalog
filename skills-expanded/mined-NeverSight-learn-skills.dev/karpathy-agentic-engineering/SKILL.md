---
name: karpathy-agentic-engineering
description: 'Apply Karpathy-style agentic engineering to any coding or building task. Use this skill when the user wants to set up an agent-driven workflow, needs to write a CLAUDE.md or AGENTS.md, wants to orchestrate agents with clear success criteria, or says things like "agent loop", "let the agent handle it", "agentic coding", "set up agent workflow". Includes the 7-step inner loop from Karpathy claude coding notes.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-idea-files
  - karpathy-minimalism
  - karpathy-supply-chain-hygiene
  - karpathy-vibe-to-agentic
  - karpathy-understanding-first
---

# Skill 1: Agentic Engineering（代理工程）

> Source: https://x.com/karpathy/status/2004607146781278521 | https://x.com/karpathy/status/2015883857489522876 | https://x.com/karpathy/status/2026731645169185220
> "It is hard to communicate how much programming has changed." — ~37k likes

## Core Principle

You are no longer writing code. You are **directing a team of tireless junior engineers**.

The shift: `write code` → `write tasks with success criteria` → `agent loops` → `human taste review`

## The 7-Step Inner Loop (Karpathy's Incremental Coding Rhythm)

This is the micro-loop for every coding session:

1. **Stuff context** — Load entire project into context (`files-to-prompt`, relevant docs, recent diffs)
2. **Discuss plan** — Ask agent for high-level approaches with pros/cons before any code
3. **Request first draft** — Pick one approach, get a minimal first implementation
4. **Inline learning** — Manually review the diff; ask agent to explain any API you don't recognize
5. **Test** — Run tests, check outputs, verify success criteria
6. **Commit** — Only commit what you understand and have verified
7. **Ask for next** — Let agent suggest the next incremental step

**Never skip step 4.** Understanding atrophies if you rubber-stamp every diff.

## CLAUDE.md / AGENTS.md Template

Write this file at the project root to prevent the most common agent failure modes:

```markdown
# Agent Instructions for [Project Name]

## Behavior Rules
- Make one incremental change at a time. Do NOT refactor unrelated code.
- Always explain WHY you're making a change before the diff.
- If unsure about intent, ASK before implementing.
- Do NOT add new dependencies without explicit approval.
- Prefer simple, readable solutions over clever ones.

## Success Criteria (task-specific — fill in per session)
- [ ] Tests pass: `[test command]`
- [ ] No new lint errors: `[lint command]`
- [ ] Behavior matches: [description of expected output]

## Project Context
- Stack: [language, framework, key libs]
- Entry point: [file]
- Test command: [command]
- Forbidden: [list things agent must never do]
```

## Master Prompt Template

```
You are an agentic engineer on this project.

Project context: [paste relevant files or use files-to-prompt output]

Task: [specific, unambiguous description]

Success criteria (ALL must be true when done):
1. [verifiable check 1]
2. [verifiable check 2]
3. [verifiable check 3]

Constraints:
- Only change files relevant to this task
- No new dependencies without asking
- Output: one incremental diff at a time

Start by proposing a high-level plan with 2-3 options and trade-offs. Wait for approval before writing code.
```

## Common Failure Modes to Prevent

| Agent Sin | Prevention |
|-----------|-----------|
| Over-refactoring | "Only touch files directly related to the task" |
| Sycophantic confirmation | "Tell me what could go wrong with this plan" |
| Hallucinated APIs | "Cite the exact line in the docs for any API you use" |
| Dependency creep | "No new pip/npm installs without asking" |
| No success criteria | Always define DONE before starting |

## Workflow

**属于工作流：想法到上线（开发者）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第2步 | `karpathy-idea-files`（先定义想法） | `karpathy-minimalism`（极简实现） |

完整链路：`idea-files → agentic-engineering → minimalism → supply-chain-hygiene → vibe-to-agentic`

也常在反偏见决策工作流中作为执行层出现——当决策完成后需要落地时，切换到本 Skill。

## Prompt Contract

```text
You are an agentic engineer. Project context: <files, constraints, current state>. Task: <specific goal>. Success criteria: <verifiable checklist>. First propose a high-level plan with tradeoffs. Then make only the next incremental change. After each change, run the relevant verification and report: changed files, evidence of success, remaining risk, and next step.
```

## Verification Checklist

- [ ] 成功标准已经写成可检查项目（不是模糊描述）
- [ ] 每轮变更都有实际验证证据：测试通过、lint clean、diff 范围正确
- [ ] Agent 没有修改任务范围外的文件
- [ ] 人类已 review 每个 diff 中不理解的部分（不跳步）
- [ ] 最终提交前，能用一句话向同事解释改了什么、为什么

## When to Apply This Skill

- Starting any coding task > 30 minutes
- Setting up a new project with agent assistance
- Debugging a complex issue (agent as rubber duck + implementer)
- Writing CLAUDE.md / AGENTS.md for a repo
