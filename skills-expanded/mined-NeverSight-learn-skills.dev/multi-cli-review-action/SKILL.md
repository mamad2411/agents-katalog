---
name: multi-cli-review-action
description: Use when reviewing a multi-cli-review defect report, refining the action plan, and executing confirmed optimizations with explicit path handoff or run-id fallback.
---

# Multi-CLI Review Action

## Overview

Multi-CLI Review Action 是多 CLI 协作流程中 CLI 2 的 skill。CLI 2 负责审查问题分析报告，与用户讨论优化方案，执行优化操作，并输出优化方案报告。CLI 2 需要保持质疑态度，但只在有实际依据时质疑。

## When to Use

- 需要审查 `multi-cli-review` 生成的问题分析报告
- 需要与用户讨论优化方案
- 需要执行优化操作（新增/删除/编辑文件）
- 需要输出优化方案报告给 CLI 1 继续分析

## When Not to Use

- 只需要生成问题报告，不需要执行优化
  - 使用 `multi-cli-review`
- 只需要普通代码修改，不需要 CLI 1 / CLI 2 分工
  - 直接执行实现流程

## Trigger Conditions

以下任一情况都应触发本 skill：

- 显式调用：`/multi-cli-review-action [md-a-路径] [md-b-路径]`
- 在 `multi-cli-review` 产出 `cur_defect.md` 后继续处理
- 自然语言请求：
  - “基于 cur_defect.md 生成优化方案”
  - “审查这个问题报告并执行优化”

## Path Resolution Rules

优先级从高到低如下：

1. 用户显式传入 `md-a` / `md-b`
2. 只传 `md-a` 时，使用其同级目录下的 `optimize.md`
3. 只传 `md-b` 时，使用其同级目录下的 `cur_defect.md`
4. 两者都未传时：
   - 读取 `tmp/multi-cli-review/` 下最新的 `<run-id>/cur_defect.md`
   - 写入同级目录的 `optimize.md`
   - 这只是串行单任务场景的兜底策略
   - 并行场景仍推荐显式传路径

每次执行结束时，必须回显本次实际读取和写入的路径。

## Workflow

**推荐触发方式**：`/multi-cli-review-action [md-a-路径] [md-b-路径]`

**执行流程**：
1. **解析路径**：确定本轮实际使用的 `md-a` 和 `md-b`
2. **读取 md 文件 A**：获取问题分析报告
3. **输出分析摘要**：向用户展示问题清单
4. **质疑问题点**：基于实际情况选择性质疑
   - 仅在问题准确性、严重性、优先级、方案可行性存在疑点时质疑
   - 不得为了“显得认真”而对所有问题都质疑
5. **用户多轮讨论**：与用户讨论优化方案
6. **生成优化方案草稿**：包含被忽略的问题及原因
7. **用户确认**：用户输入“确认”后执行最终操作
8. **执行操作**：根据确认的方案执行操作
   - 如果执行失败，可合理重试
   - 多次失败后需要和用户确认新方案或思路
   - 同步更新 `md-b`
9. **回显实际路径**：
   - 明确说明读取了哪个 `cur_defect.md`
   - 明确说明写入了哪个 `optimize.md`

## Input Parameters

| 参数 | 必需 | 说明 |
|------|------|------|
| `[md-a-路径]` | 否 | 问题分析报告路径；默认按最新 run-id 回退 |
| `[md-b-路径]` | 否 | 优化方案路径；默认与 `md-a` 同级的 `optimize.md` |

## Output Files

### md 文件 B（优化方案）

```markdown
# 优化方案

## 问题 1：[对应 md 文件 A 中的问题标题]
- **方案描述**：具体的优化方案
- **执行内容**：实际执行的修改内容
- **是否忽略**：是/否
- **忽略原因**：如果忽略，说明原因

### 问题 2：...

## 总体状态
- 最后确认时间：2026-03-20
- 执行状态：completed/pending/blocked/abandoned
- 当前运行目录：tmp/multi-cli-review/<run-id>/
```

## Quoting Rules

### 选择性质疑

CLI 2 需要基于实际情况选择性质疑问题点，而不是对所有问题点进行空假的质疑。

**适合质疑的情况**：
- 问题描述与实际代码或文档不符
- 严重程度与影响范围不匹配
- 所谓“必须解决原因”站不住脚
- 提出的解决方案成本明显高于收益

**不适合质疑的情况**：
- 问题已经有明确证据且影响明显
- 用户只是需要你执行明确修改

## Confirmation Rules

用户输入以下任一确认方式后，才执行最终操作：

- `确认`
- `是的`
- `对的`
- `可以`
- `ok`
- `yes`
- `y`

## Error Handling

- **cur_defect.md 不存在**：
  - 立即报告缺失路径
  - 不得假装读取成功
  - 要求用户传正确路径，或先重新运行 `multi-cli-review`
- **cur_defect.md 格式错误**：
  - 明确指出缺了哪些关键字段
  - 不得自行脑补
- **代码修改失败**：
  - 可以重试
  - 多次失败后要把状态标记为 `blocked`
  - 说明阻塞原因和下一步建议
- **optimize.md 写入失败**：
  - 不得声明执行完成
  - 需要明确写入失败和影响范围

## Common Mistakes

### ❌ 默认盲读固定路径
- 问题：无论什么场景都直接读取 `tmp/cur_defect.md`
- 后果：多任务场景容易读错报告
- 正确做法：显式路径优先，再按最新 run-id 兜底

### ❌ 对所有问题都质疑
- 问题：把“质疑”当成每个问题的必经步骤
- 后果：交互成本高，用户体验差
- 正确做法：只在确有疑点时质疑

### ❌ 不回显实际路径
- 问题：执行后没有说明读写了哪个文件
- 后果：CLI 1 难以继续接续同一个 run
- 正确做法：每次结束都说明本次 `md-a` / `md-b` 路径

### ❌ 写入失败还声称完成
- 问题：优化方案文件没有落盘却说流程完成
- 后果：CLI 1 拿不到真实状态
- 正确做法：如实标记为 `blocked`

## Tips

1. **显式路径优先**：并行场景尽量传完整路径
2. **路径和执行结果一起回显**：不要只说“已生成”
3. **质疑要有证据**：没有依据就不要质疑
4. **优化方案先草稿后执行**：必须等用户确认

## Example

```text
用户：/multi-cli-review-action tmp/multi-cli-review/3/cur_defect.md

CLI 2：
1. 读取 tmp/multi-cli-review/3/cur_defect.md
2. 推导写入路径为 tmp/multi-cli-review/3/optimize.md
3. 输出问题清单和选择性质疑
4. 用户确认后执行修改
5. 回显本次读取和写入路径
```

## Related Skills

- `multi-cli-review`：CLI 1，负责分析问题并输出问题报告
- `$start`：初始化项目上下文
- `/trellis:brainstorm`：需要先澄清边界时使用
