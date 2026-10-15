---
name: karpathy-vibe-to-agentic
description: 'Transition from vibe coding (fast prototyping) to agentic engineering (rigorous iteration). Use this skill when the user has a rough prototype and wants to level it up, needs to go from "it kind of works" to production-quality, wants to understand the difference between vibe coding and agentic coding, or says "polish this", "make this production-ready", "level up from prototype", "vibe coded this now what". Based on Karpathy posts 3 and 6.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-agentic-engineering
  - karpathy-minimalism
  - karpathy-supply-chain-hygiene
  - karpathy-understanding-first
---

# Skill 5: Vibe Coding → Agentic Leap（Vibe编码 → 代理跃迁）

> Source: https://x.com/karpathy/status/2004607146781278521 | https://x.com/karpathy/status/2026731645169185220
> "I've never felt this much behind as a programmer" — 56k likes

## Core Principle

**Vibe coding raises the floor. Agentic engineering raises the ceiling.**

They're not the same thing and you need both:

| | Vibe Coding | Agentic Engineering |
|---|---|---|
| **Goal** | Fast prototype, explore ideas | Reliable, maintainable, verifiable |
| **How** | Natural language → run it | Task specs + success criteria + loops |
| **When** | First 20% (exploration) | Last 80% (execution) |
| **Risk** | You don't understand what you built | Agent doesn't understand what you want |
| **Karpathy says** | "raises the floor" | "raises the ceiling" |

## The Transition Protocol

When you have a vibe-coded prototype and need to level it up:

### Step 1: Audit What You Built

```
I vibe-coded this [project/script/app]. I need to understand what I actually have before leveling it up.

[PASTE CODE OR DESCRIBE IT]

Please:
1. Describe exactly what this does in plain English (3-5 sentences)
2. List every assumption baked in (hardcoded values, expected input format, etc.)
3. Identify the 3 most likely failure modes
4. List what's missing for this to be production-ready
5. What would break if I ran this on a different machine / with different data?

Be blunt. I'm about to invest more time in this and need to know if it's worth it.
```

### Step 2: Define Success Criteria

```
Based on this audit of my prototype:

[AUDIT OUTPUT FROM STEP 1]

Help me define clear, verifiable success criteria for the "production-ready" version.

Format each criterion as a testable assertion:
- GIVEN [input/condition]
- WHEN [action]
- THEN [expected output/behavior]

List 5-7 criteria. Start with the most important.
```

### Step 3: Agentic Cleanup Loop

```
You are a senior engineer reviewing this prototype. Your job is to systematically improve it.

Prototype: [CODE]
Success criteria: [FROM STEP 2]

Work incrementally:
1. First fix: address the most critical issue only (one diff)
2. After I approve each fix, suggest the next
3. Never refactor unrelated code
4. For each fix, explain: WHAT changed, WHY this matters, RISK of this change

Start with fix #1.
```

## Common Vibe Coding Smells to Clean Up

```
Review this vibe-coded project for these specific anti-patterns:

[PASTE CODE]

Check for:
1. Hardcoded credentials, paths, or magic numbers → suggest config/env vars
2. No error handling on file I/O or network calls → add try/except with clear messages
3. print() debugging left in → identify and offer to remove
4. Functions doing 3+ things → suggest split points
5. No way to run without human supervision → suggest automation hooks
6. Dependencies that aren't in requirements.txt / package.json

For each issue found: show the exact line and suggest the minimal fix.
```

## The Two-Track System

Karpathy runs these in parallel:

```
TRACK A (IDE / Human)          TRACK B (Agent)
─────────────────────          ───────────────
- Review diffs                 - Implement incrementally
- Apply taste/judgment         - Run tests automatically  
- Verify understanding         - Suggest next steps
- Commit good work             - Generate options
- Ask "is this right?"         - Never commit autonomously
```

Always keep a human in the loop for the taste judgment. Agents are for execution, not for deciding what's worth building.

## Quick Upgrade Prompt

For fast one-shot upgrade of a simple vibe script:

```
Upgrade this vibe-coded script to production quality.

[PASTE SCRIPT]

Requirements:
1. Add proper error handling (no unhandled exceptions)
2. Make all hardcoded values configurable via CLI args or env vars
3. Add a --dry-run flag that shows what would happen without doing it
4. Add basic logging (not print) with timestamps
5. Keep the core logic identical — only add robustness
6. Maximum 20% increase in line count

Output the complete upgraded script.
```

## Workflow

**属于工作流：想法到上线（开发者）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第5步（收尾） | karpathy-supply-chain-hygiene（安全审查后） | 部署/交付 |

完整链路：idea-files → agentic-engineering → minimalism → supply-chain-hygiene → vibe-to-agentic

## Prompt Contract

```text
I have a vibe-coded prototype: <PASTE_CODE_OR_DESCRIBE>. Step 1: Audit — describe what it does, list hidden assumptions, identify failure modes, list what's missing for production. Step 2: Define 5-7 verifiable success criteria in GIVEN/WHEN/THEN format. Step 3: Start the agentic cleanup loop — one incremental fix at a time, explain WHAT/WHY/RISK for each.
```

## Verification Checklist

- [ ] 原型的隐含假设已全部列出
- [ ] 成功标准已定义为可测试的 GIVEN/WHEN/THEN 格式
- [ ] 每轮修复只改一个问题
- [ ] 核心逻辑没有被破坏（功能不变）
- [ ] 增加了错误处理和日志
- [ ] 硬编码值已替换为配置项
