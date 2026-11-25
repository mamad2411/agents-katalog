---
name: using-superpowers
description: Superpowers 工程方法论入口。在开始任何编码任务前自动加载，确保遵循 brainstorming → plan → TDD → review 的完整工作流。触发词：写代码、开发功能、重构、修bug、做项目、build、implement、refactor、debug。
agent_created: true
---

# Superpowers — WorkBuddy 版

基于 [obra/superpowers](https://github.com/obra/superpowers) 适配的软件工程方法论技能集。

## 核心理念

```
想法 → 头脑风暴 → 计划 → TDD 执行 → 代码审查 → 完成
```

**不是建议，是强制管线。** "太简单不需要设计" —— 这是最危险的幻觉。

## 技能管线总览

| 阶段 | 技能 | 触发条件 |
|:---|:---|:---|
| 0. 入口 | `using-superpowers` | 任何编码任务开始时 |
| 1. 设计 | `brainstorming` | 新功能/改动需求 → 先设计再动手 |
| 2. 计划 | `writing-plans` | 设计确认后 → 写详细实现计划 |
| 3. 执行 | `executing-plans` 或 `subagent-driven-development` | 按计划逐任务执行 |
| 4. TDD | `test-driven-development` | 每个实现步骤强制 TDD |
| 5. 调试 | `systematic-debugging` | Bug / 测试失败 → 四阶段系统调试 |
| 6. 审查 | `requesting-code-review` / `receiving-code-review` | 代码变更后审查 |
| 7. 验证 | `verification-before-completion` | 完成前强制验证 |
| 8. 收尾 | `finishing-a-development-branch` | 所有任务完成，测试通过 |
| 9. 并行 | `dispatching-parallel-agents` | 多子代理并行任务 |
| 10. 元技能 | `writing-skills` | 编写/改进 Skill 本身 |

## 四条铁律

1. **先设计再动手** → 没有例外，再简单的项目也要先过 brainstorming
2. **TDD 不可跳过** → 没有失败的测试，就没有生产代码
3. **先根因再修复** → 没有根因调查，不许提修复方案
4. **每一步都要验证** → 完成 ≠ 做完，验证通过才算完成

## 适配说明

原版为 Claude Code/Codex 设计，WorkBuddy 版做了以下适配：

- 子代理调度：`sessions_spawn` → WorkBuddy `Agent` 工具 + `TaskCreate`
- 代码审查：Claude Code Task → WorkBuddy `Agent`（审查子代理）
- 文件路径约定：`docs/superpowers/` → `docs/plans/`
- 语言支持：中英双语描述，代码示例以 Python/TypeScript 为主
- 移除了 `using-git-worktrees`（WorkBuddy 场景不常用）
