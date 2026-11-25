---
name: writing-plans
description: 将设计规格转化为细粒度实现计划（plan.md）。每个任务 2 到 5 分钟，遵循 DRY/YAGNI 原则。支持注释循环。触发短语："编写计划"、"写计划"、"制定方案"。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /writing-plans — 编写实现计划

将设计规格文档（spec.md）转化为可逐步执行的实现计划。plan.md 是后续所有实现工作的唯一真相来源。

## 核心原则

- plan.md 比聊天记录更可靠（上下文压缩后仍完整保存）
- 每个任务 2 到 5 分钟可完成，粒度足够细才能被子代理独立执行
- 遵循 DRY 和 YAGNI：只规划当前需要的改动，不为假想需求设计
- 先读代码再写计划：每个改动必须基于对现有实现的理解

## 流程

### 第一步：加载设计规格

读取最近的 spec.md（在 `docs/sdlc/` 下查找），确认设计意图和范围。

如果没有 spec.md，建议用户先执行 /brainstorming。

### 第二步：调研现有代码

使用 Glob、Grep、Read 工具深入分析需要修改的文件：
- 理解现有实现的结构和逻辑
- 识别依赖关系和影响范围
- 记录需要注意的约束条件

### 第三步：编写计划

在 `docs/sdlc/YYYY-MM-DD/{slug}/plan.md` 中写入实现计划：

```markdown
# [任务标题]

## 方案说明

[基于 spec.md 的设计决策，描述实现策略]

## 改动文件

- `path/to/FileA`：修改 xxx，添加 yyy
- `path/to/FileB`：新增 zzz

## 代码片段

[关键改动的代码示例，展示核心逻辑]

## 考量与权衡

[为什么选这个方案，有哪些 trade-off]

## 影响的测试

[需要修改或新增的测试]

## Todo List

### Phase 1: [阶段名]
- [ ] 任务 1（2 到 5 分钟描述）
- [ ] 任务 2

### Phase 2: [阶段名]
- [ ] 任务 3
- [ ] 任务 4
```

任务粒度指南：
- 每个任务应该是一个独立的、可验证的改动
- 描述要足够具体，让不了解上下文的代理也能执行
- 包含文件路径、函数名、预期行为

### 第四步：计划审查

使用 Agent 工具派遣子代理审查 plan.md。子代理的 prompt 使用 `references/plan-reviewer-prompt.md` 的内容。

将审查结果呈现给用户，根据反馈修改 plan.md。

### 第五步：用户审阅

告知用户：**"实现计划已写入 `docs/sdlc/YYYY-MM-DD/{slug}/plan.md`，请审阅并添加注释。"**

## 注释循环

当用户发送"我加了注释"或类似指令时：

1. 读取 plan.md 中用户添加的注释
2. 根据注释修改 plan.md
3. 回复末尾注明：**（尚未实现，等待确认）**
4. **绝不提前写代码**

循环直到用户满意。用户确认后，建议执行 /executing-plans 或 /subagent-driven-development。

## 不做的事

- 不写实现代码
- 不使用内置 Plan Mode（聊天内计划不持久、不可编辑）
- 不跳过代码调研直接写计划
