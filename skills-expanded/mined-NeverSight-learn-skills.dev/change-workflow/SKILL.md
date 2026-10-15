---
name: change-workflow
description: 用于执行任何仓库代码变更、新功能、缺陷修复、重构、与代码相关的文档更新，或需要计划、测试、验证、续作记录和干净提交的跨轮任务。
---

# 变更工作流

处理仓库变更时使用本 skill。必须与当前项目自己的规则合并执行；当项目规则更具体时，以项目规则为准。

## 必执行流程

1. **读取上下文**
   - 阅读项目说明，例如 `AGENTS.md`、`CODEX.md`、`README`、测试文档和相关源码。
   - 编辑前检查当前 worktree 状态。
   - 如果已有匹配计划文档，先读计划，不要从聊天记忆重新推理。

2. **判断变更规模**
   - **Small**：局部修复、文档微调，或低风险的单点行为。
   - **Medium**：影响一个子系统或多个文件，需要配套测试或文档。
   - **Large**：跨子系统、公共 API 变更、迁移，或可能跨会话完成。

3. **制定计划**
   - Small：在对话中简述计划即可。
   - Medium 或 Large：在项目中创建或更新计划文件，通常为 `docs/plans/<feature>.md`。
   - 计划文档中的 `Decisions` 是该任务的事实来源，除非用户明确要求重新设计。

4. **测试优先**
   - 新功能：可行时先为目标行为写失败测试。
   - Bug 修复：可行时先写复现测试。
   - 如果不适合自动化测试，在计划或最终回复中写清具体验证步骤。

5. **实现**
   - 改动范围紧扣目标。
   - 除非项目明确要求，不做无关重构、兼容层、别名、fallback 或臆测性抽象。
   - 与已有用户改动协作，不覆盖无关工作。

6. **验证**
   - 先运行最小相关测试或检查。
   - 再根据风险和项目规则运行更广的测试或构建。
   - 如果验证失败，继续修复直到通过，或记录真实阻塞。

7. **续作记录**
   - 如果任务未完成，必须更新计划文档中的 `Progress` 和 `Resume Notes`。
   - 续作记录必须包含 `Done`、`Currently Failing` 或 `Current State`，以及 `Next`。

8. **提交**
   - 当项目规则要求提交时，验证通过后只提交相关改动；新增文件只纳入本任务需要的路径。
   - 不提交无关未跟踪文件或用户工作。

## 计划文档要求

Medium 和 Large 变更的计划文档应包含：

- `Goal`
- `Decisions`
- `Non-Goals`
- `Public API / User-Facing Behavior`（不涉及时写明不适用）
- `Implementation Scope`
- `Test Plan`
- `Verification`
- `Progress`
- `Resume Protocol`
- `Resume Notes`

当项目没有本地模板时，可使用 `references/plan-template.md` 作为起点。

## 续作协议

继续已有任务时：

1. 阅读项目说明和计划文档。
2. 查看 worktree 状态。
3. 运行 `Resume Notes` 中最小相关失败测试或目标测试。
4. 从 `Next` 继续，不重新打开已经确定的设计决策。
5. 如果停止时任务仍未完成，更新 `Progress` 和 `Resume Notes`。

## 推荐交接格式

```md
## Resume Notes

Last updated: YYYY-MM-DD

Done:
- ...

Current State:
- ...

Currently Failing:
- ...

Next:
1. ...
2. ...
```
