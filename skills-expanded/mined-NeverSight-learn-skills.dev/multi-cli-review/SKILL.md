---
name: multi-cli-review
description: Use when analyzing a skill, command, workflow, document, or code artifact for problems and outputting a structured defect report, either standalone or together with start/brainstorm.
---

# Multi-CLI Review

## Overview

Multi-CLI Review 是一个多 CLI 协作的问题分析和优化流程。CLI 1 负责分析问题并输出问题报告，CLI 2 负责审查、讨论和执行优化操作。两个 CLI 通过同一个 run 目录传递上下文，避免固定临时文件被覆盖。

## When to Use

- 需要分析 skill、command、workflow、文档、配置或代码中的问题
- 需要输出结构化的问题报告给另一个 CLI 继续处理
- 需要在优化操作后重新分析问题
- 需要和 `$start`、`/trellis:brainstorm` 组合使用

## When Not to Use

- 只需要澄清需求，不需要结构化问题报告
  - 使用 `$brainstorm` 或 `/trellis:brainstorm`
- 只需要对当前 git diff 做代码审查
  - 使用 `code-review-router` 或 `requesting-code-review`
- 只需要直接修改文件，不需要 CLI 1 / CLI 2 分工
  - 直接执行普通实现流程

## Trigger Conditions

以下任一情况都应触发本 skill：

- 显式单独调用：`/multi-cli-review <问题描述> [目标路径] [--md-a <路径>] [--md-b <路径>]`
- 组合调用：`$start /multi-cli-review ...`、`/trellis:brainstorm /multi-cli-review ...`
- 自然语言请求：
  - “分析这个 skill 在实际使用场景里的问题”
  - “输出一个结构化问题报告”
  - “先分析问题，再交给另一个 CLI 执行优化”

## Composition Rules

- 与 `$start` 一起出现时：
  - `$start` 先完成初始化和上下文读取
  - 然后继续执行 `multi-cli-review`
- 与 `/trellis:brainstorm` 一起出现时：
  - `brainstorm` 负责澄清问题边界和分析目标
  - `multi-cli-review` 负责产出结构化问题报告
- 同一条消息里出现多个 skill 时：
  - 不得静默忽略 `multi-cli-review`
  - 如果不能并行执行，必须明确按阶段串行执行
  - 必须向用户说明当前执行到哪个阶段

## Path Protocol

### 默认路径

首次调用且未显式提供 `--md-a` / `--md-b` 时：

1. 扫描 `tmp/multi-cli-review/` 下已有的数字目录
2. 取最大数字 + 1 作为 `<run-id>`
3. 如果目录不存在或为空，则从 `1` 开始
4. 使用以下默认路径：
   - md 文件 A：`tmp/multi-cli-review/<run-id>/cur_defect.md`
   - md 文件 B：`tmp/multi-cli-review/<run-id>/optimize.md`

### 续跑规则

- 同一个问题的后续迭代必须复用同一个 `<run-id>`
- 如果只传 `--md-b`，应优先根据其同级目录推导 `cur_defect.md`
- 如果只传 `--md-a`，应优先根据其同级目录推导 `optimize.md`
- 如果用户显式传入路径，则以用户路径为准

### 回显要求

每次执行结束时，必须明确说明：

- 本次读取的 `md-a` 实际路径
- 本次读取或写入的 `md-b` 实际路径
- 当前 `<run-id>` 或实际运行目录

## Workflow

### 步骤 1：首次分析

**推荐触发方式**：`/multi-cli-review <问题描述> [目标路径] [--md-a <路径>] [--md-b <路径>]`

**执行流程**：
1. **确认问题边界**：
   - 仅在问题描述模糊、目标不清、严重程度可疑时才质疑
   - 对于明确的问题，直接进入分析
2. **确定输出路径**：
   - 优先使用用户显式提供的路径
   - 否则按默认 run-id 规则分配新目录
3. **分析问题**：分析目标文件或目标目录，识别问题
4. **输出问题报告**：
   - 同步输出到对话中
   - 写入 md 文件 A
5. **回显实际路径**：
   - 明确告诉用户 `cur_defect.md` 和 `optimize.md` 的实际路径

### 步骤 3：重新分析

**推荐触发方式**：`/multi-cli-review --md-a <路径> --md-b <路径>`

**兼容触发方式**：
- `/multi-cli-review --md-b <路径>`：从同级目录推导 `cur_defect.md`
- `/multi-cli-review --md-a <路径>`：从同级目录推导 `optimize.md`

**执行流程**：
1. **读取 md 文件 B**：获取优化方案
2. **定位配对的 md 文件 A**：确保仍然绑定同一个 run 目录
3. **先检查 CLI 2 状态**：
   - 如果 `md-b` 标记为 `blocked`，默认停止自动迭代，先向用户报告阻塞原因并等待确认是否继续
   - 如果 `md-b` 标记为 `abandoned`，本轮流程终止，除非用户明确要求重新开启新一轮
4. **读取最新的项目文件内容**：获取最新项目状态
5. **重新分析问题**：
   - 重点：原问题是否解决
   - 其次：md 文件 A 中的问题是否仍存在
   - 其次：md 文件 B 中的优化方案是否有效
   - 其次：是否有新问题出现
6. **输出更新后的问题报告**：
   - 覆盖原 md 文件 A
   - 未解决的问题必须补充“必须解决原因”
   - 新问题按同样格式追加
7. **回显实际路径**

## Input Parameters

| 参数 | 必需 | 说明 |
|------|------|------|
| `<问题描述>` | 是（首次分析） | 用户提出的问题，贯穿始终 |
| `[目标路径]` | 否 | 需要分析的目标文件或目录 |
| `[--md-a <路径>]` | 否 | 问题分析报告路径；未提供时自动分配 `tmp/multi-cli-review/<run-id>/cur_defect.md` |
| `[--md-b <路径>]` | 否 | 优化方案路径；未提供时自动分配 `tmp/multi-cli-review/<run-id>/optimize.md` |

## Output Files

### md 文件 A（问题分析报告）

最小可用格式：

```markdown
# 问题分析报告

## 问题描述
<用户输入的问题描述，贯穿始终>

## 分析结果
### 问题 1：[问题标题]
- **位置**：文件路径 + 行号范围
- **问题描述**：具体是什么问题
- **严重程度**：高/中/低
- **影响范围**：[具体影响什么]
- **关联部分**（可选）：[路径 + 行号] / `N/A`
- **依赖关系**（可选）：[哪些部分会受影响] / `N/A`
- **必须解决原因**：（仅对未解决的问题）说明为什么 CLI 2 必须解决

### 问题 2：...

## 迭代状态
- 当前迭代次数：1
- 上次分析时间：2026-03-20
- 当前运行目录：tmp/multi-cli-review/<run-id>/
- 上次优化方案来源：tmp/multi-cli-review/<run-id>/optimize.md
```

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

## Iteration Rules

- **最大迭代次数**：5 次
- **达到最大迭代次数**：
  - 允许继续，但必须明确说明为什么继续
  - 或者标记为 `blocked` / `abandoned`
- **问题解决**：当首次问题描述中的核心问题全部解决时，流程结束
- **状态建议**：
  - `pending`：等待用户确认
  - `completed`：已完成本轮操作
  - `blocked`：被文件缺失、权限、格式错误等问题阻塞
  - `abandoned`：用户选择终止

## Error Handling

- **md 文件不存在**：
  - 明确提示缺失路径
  - 如果是首次分析，应重新创建报告
  - 如果是后续分析，应要求用户提供正确路径或重新生成
- **md 文件格式不完整**：
  - 明确缺少哪些字段
  - 不得假设缺失内容
- **优化方案未生成成功**：
  - 不得声称流程已完成
  - 应说明失败原因和下一步
- **CLI 2 返回 `blocked`**：
  - CLI 1 默认停止自动迭代
  - 先同步 `blocked` 的原因、涉及路径和建议动作
  - 等待用户确认是否修复阻塞后继续
- **CLI 2 返回 `abandoned`**：
  - 视为本轮流程结束
  - 除非用户明确重新开启，否则不要继续重新分析
- **并行场景**：
  - 推荐显式传 `--md-a` / `--md-b`
  - 不要依赖“最近一次 run-id”推断

## Common Mistakes

### ❌ 只支持单独显式调用
- 问题：只能在 `/multi-cli-review` 单独出现时触发
- 后果：与 `$start`、`/trellis:brainstorm` 组合时容易被忽略
- 正确做法：支持组合触发和自然语言触发，并明确串行阶段

### ❌ 继续使用固定路径
- 问题：始终写到 `tmp/cur_defect.md`
- 后果：并行任务会互相覆盖
- 正确做法：使用 `tmp/multi-cli-review/<run-id>/` 协议

### ❌ 无条件质疑
- 问题：对每个问题都先质疑
- 后果：效率低，用户体验差
- 正确做法：只在问题模糊或证据不足时质疑

### ❌ 不回显实际路径
- 问题：生成文件后没有说明实际写入位置
- 后果：CLI 2 无法稳定接续
- 正确做法：每次执行末尾都明确输出本次读写路径

## Tips

1. **问题描述要具体**：避免“代码有问题”这类模糊表达
2. **优先最小可用报告**：先保证必填字段完整，再补可选字段
3. **组合调用时先说阶段**：例如“先 brainstorm，再输出 defect report”
4. **显式路径优先**：并行场景尽量总是显式传路径

## Examples

### 示例 1：单独调用

```text
用户：/multi-cli-review 检查这个文档的逻辑完整性 ./docs/api.md

CLI 1：
1. 问题描述明确，直接进入分析
2. 未传路径，自动分配 run-id=1
3. 输出问题报告到 tmp/multi-cli-review/1/cur_defect.md
4. 告知后续优化方案路径为 tmp/multi-cli-review/1/optimize.md
```

### 示例 2：与 brainstorm 组合调用

```text
用户：/trellis:brainstorm /multi-cli-review 根据该 skill[./skills/multi-cli-review]的作用和实际实践使用场景进行分析

执行：
1. brainstorm 先澄清分析目标和边界
2. multi-cli-review 再输出结构化问题报告
3. 报告写入 tmp/multi-cli-review/2/cur_defect.md
4. 明确告知 optimize.md 的配对路径
```

## Related Skills

- `multi-cli-review-action`：CLI 2，负责审查、讨论和执行优化操作
- `$start`：初始化上下文，不替代问题分析
- `/trellis:brainstorm`：澄清边界，不替代结构化问题报告
