---
name: dispatching-parallel-agents
description: 在面对 2 个以上互不依赖、无共享状态的独立任务时使用
---

# 派发并行 Agent

## 概述

当你有多个不相关的失败或独立任务时，按顺序调查浪费时间。每个调查都是独立的，可以并行进行。

**核心原则：** 每个独立的问题域派发一个 agent。让它们并发工作。

## 何时使用

**使用条件：**

- 3 个以上测试文件因不同根因失败
- 多个子系统独立出问题
- 每个问题可以不依赖其他问题的上下文来理解
- 调查之间没有共享状态

**不要使用的情况：**

- 失败是相关的（修复一个可能修复其他）
- 需要理解完整的系统状态
- Agent 之间会互相干扰（编辑同一文件）

## 模式

### 1. 识别独立域

按出问题的部分分组：

- 文件 A 的测试：订单表单验证
- 文件 B 的测试：WebSocket 订阅
- 文件 C 的测试：仓位计算

每个域是独立的——修复订单表单不影响 WebSocket 测试。

### 2. 创建聚焦的 Agent 任务

每个 agent 获得：

- **具体范围：** 一个测试文件或子系统
- **明确目标：** 让这些测试通过 / 修复这个具体问题
- **约束：** 不要改其他代码
- **预期输出：** 你发现了什么以及修复了什么的总结

### 3. 并行派发

使用 Task 工具同时派发多个 `worker` droid：

```
Task("Fix order-form.test.tsx failures")
Task("Fix websocket-subscription.test.tsx failures")
Task("Fix position-calc.test.tsx failures")
// 三个同时运行
```

### 4. 审查与集成

当 agent 返回时：

- 阅读每个总结
- 验证修复之间没有冲突
- 运行完整测试套件
- 集成所有改动

## Agent Prompt 结构

好的 agent prompt 特点：

1. **聚焦** — 一个清晰的问题域
2. **自包含** — 理解问题所需的所有上下文
3. **明确输出** — agent 应该返回什么？

示例：

```markdown
修复 src/modules/trade/components/**tests**/OrderForm.test.tsx 中的 3 个失败测试：

1. "should validate minimum order amount" - 预期验证错误但没有
2. "should calculate fee correctly" - 费用为 0 而不是预期值
3. "should disable submit when balance insufficient" - 按钮没有被禁用

这些测试使用 Vitest。组件使用 BigNumber 做计算，Zustand 做状态管理。

你的任务：

1. 阅读测试文件，理解每个测试验证什么
2. 找到根因
3. 修复问题
4. 运行 `pnpm test src/modules/trade/components/__tests__/OrderForm.test.tsx` 验证

不要修改此组件之外的其他测试文件或生产代码。

返回：根因和修复内容的总结。
```

## 常见错误

**❌ 范围太广：** "修复所有测试" — agent 会迷失
**✅ 具体：** "修复 OrderForm.test.tsx" — 聚焦的范围

**❌ 没有上下文：** "修复竞态条件" — agent 不知道在哪里
**✅ 有上下文：** 贴出错误信息和测试名称

**❌ 没有约束：** Agent 可能重构所有东西
**✅ 有约束：** "不要修改此组件之外的生产代码"

**❌ 输出模糊：** "修好它" — 你不知道改了什么
**✅ 输出明确：** "返回根因和改动的总结"

## 何时不应使用

**相关失败：** 修复一个可能修复其他 — 先一起调查
**需要全局上下文：** 理解问题需要看完整系统
**探索性调试：** 你还不知道什么坏了 — 先用 `/systematic-debugging`
**共享状态：** Agent 之间会干扰（编辑同一文件、使用同一资源）

## 验证

Agent 返回后：

1. **审查每个总结** — 理解改了什么
2. **检查冲突** — Agent 之间是否编辑了同一代码？
3. **运行完整套件** — `pnpm test` 验证所有修复协同工作
4. **抽查** — Agent 可能犯系统性错误

## 核心收益

1. **并行化** — 多个调查同时进行
2. **聚焦** — 每个 agent 范围窄，追踪的上下文少
3. **独立性** — Agent 之间不会互相干扰
4. **速度** — 3 个问题在 1 个问题的时间内解决
