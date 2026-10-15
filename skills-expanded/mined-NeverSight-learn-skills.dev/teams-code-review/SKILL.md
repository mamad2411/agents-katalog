---
name: 'teams-code-review'
description: '代码审查、review分支改动、审查分支差异、检查分支差异、审查master和uat的差异、代码审查报告、diff review。当用户要求对比两个分支的代码、检查代码改动有没有问题、审查代码变更时触发。'
---

# Teams Code Review - 多 Agent 协作代码审查

## 概述

4 Agent 流水线：DiffCollector → ChangeClassifier → RiskDetector → ReportWriter

**核心设计**：
- 分层过滤：先分类（A/B/C类），再检测，只分析高风险文件
- 流式处理：分类完一个文件就立即开始风险检测，无需等待全部完成
- Token优化：跳过A类（纯格式变更），只读B/C类代码

## 团队架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Teams 协作模型                      │
│                                                              │
│  DiffCollector ──file_ready──→ ChangeClassifier              │
│                                   │                          │
│                          B/C类文件 ──risk_check──→ RiskDetector
│                                                       │      │
│                                     risk_found ──→ ReportWriter
│                                                       │      │
│                                     全部完成 ──→ 生成报告     │
└─────────────────────────────────────────────────────────────┘
```

### 消息协议

| 消息类型 | 发送方 | 接收方 | 含义 | 数据 |
|----------|--------|--------|------|------|
| `diff_ready` | DiffCollector | ChangeClassifier | 所有 diff 采集完毕，manifest 已生成 | 无 |
| `file_classified` | ChangeClassifier | RiskDetector | 某文件被分为 B/C 类，需风险检测 | `{ id, path, type, class, cls_file }` |
| `a_class_complete` | ChangeClassifier | ReportWriter | A 类文件统计信息 | `{ id, path, type }` |
| `classify_all_done` | ChangeClassifier | RiskDetector, ReportWriter | 所有文件分类完毕 | `{ summary, total_a, total_b, total_c }` |
| `risk_checked` | RiskDetector | ReportWriter | 某文件风险检测完毕 | `{ id, path, severity, risks, todo }` |
| `risk_all_done` | RiskDetector | ReportWriter | 所有风险检测完毕 | `{ total_risk, total_safe }` |

### 数据流

```
.diff-pool/          ← DiffCollector 生成，所有 Agent 共享读取
.classify-results/   ← ChangeClassifier 生成，RiskDetector 读取
.risk-results/       ← RiskDetector 生成，ReportWriter 读取
```

## 工作流程

### 阶段一：差异采集（DiffCollector）

按照 [agents/DiffCollector.md](agents/DiffCollector.md) 执行：
1. 运行 `git diff <source>...<target> --name-only` 获取变更文件列表
2. 排除无需处理的文件
3. 逐文件提取 diff 并存储到 `.diff-pool/`
4. 生成 `.diff-pool/manifest.json`
5. **发送 `diff_ready` 消息给 ChangeClassifier**
6. 输出 `DIFF_COLLECT_COMPLETE: <总文件数>`

### 阶段二：变更分类（ChangeClassifier）— 流式输出

按照 [agents/ChangeClassifier.md](agents/ChangeClassifier.md) 执行：
1. 收到 `diff_ready` 后开始工作
2. 读取 `.diff-pool/manifest.json`
3. **逐文件分类，每分类完一个文件**：
   - **A 类**：发送 `a_class_complete` 给 ReportWriter（仅统计信息，不含代码）
   - **B/C 类**：写入 .cls 文件，**立即发送 `file_classified` 给 RiskDetector**
4. 全部完成后：发送 `classify_all_done` 给 RiskDetector 和 ReportWriter
5. 输出 `CLASSIFY_COMPLETE: A类<数量> B类<数量> C类<数量>`

### 阶段三：风险检测（RiskDetector）— 增量接收

按照 [agents/RiskDetector.md](agents/RiskDetector.md) 执行：
1. 收到 `file_classified` 就开始处理（不等全部完成）
2. 逐个文件加载规则并分析风险
3. **每检测完一个文件**：发送 `risk_checked` 给 ReportWriter
4. 收到 `classify_all_done` 后，确认所有任务处理完毕
5. 发送 `risk_all_done` 给 ReportWriter
6. 输出 `RISK_CHECK_COMPLETE: <风险项数量>项需人工检查`

### 阶段四：报告撰写（ReportWriter）— 增量聚合

按照 [agents/ReportWriter.md](agents/ReportWriter.md) 执行：
1. 收到 `a_class_complete` → 累积 A 类统计
2. 收到 `risk_checked` → 累积风险项
3. 收到 `risk_all_done` → 生成最终报告
4. 清理临时文件
5. 输出 `REPORT_WRITTEN: diff-review-report.md`

## 注意事项

- **逐文件处理**：避免上下文溢出
- **Token优化**：RiskDetector只读B/C类文件，跳过A类（纯格式变更）
- **流式处理**：分类完一个文件就立即开始风险检测
- **分类保守**：宁可误判为B类也不漏判
- **TODO可执行**：风险项需说明"检查什么+怎么检查"
- **自适应规则**：按文件类型加载前端/后端规则

## 资源文件

### Agent 指令
- [agents/DiffCollector.md](agents/DiffCollector.md) - 差异采集 Agent
- [agents/ChangeClassifier.md](agents/ChangeClassifier.md) - 变更分类 Agent（流式输出）
- [agents/RiskDetector.md](agents/RiskDetector.md) - 风险检测 Agent（增量接收）
- [agents/ReportWriter.md](agents/ReportWriter.md) - 报告撰写 Agent（增量聚合）

### 分类规则（按前后端分离）
- [rules/frontend/classify.md](rules/frontend/classify.md) - 前端分类规则
- [rules/backend/classify.md](rules/backend/classify.md) - 后端分类规则

### 风险检测规则（按前后端分离）
- [rules/frontend/risk.md](rules/frontend/risk.md) - 前端风险检测规则
- [rules/backend/risk.md](rules/backend/risk.md) - 后端风险检测规则

## 执行指令

当本 Skill 被触发后，你必须**严格**按照以下步骤执行。**禁止任何偏离此流程的操作。**

### 🚫 绝对禁止事项

- **禁止**自行审查代码、读取 diff、或做任何分析工作——这是成员的事
- **禁止**创建额外的 general-purpose Agent——流水线只有 4 个固定成员
- **禁止**按模块拆分审查任务——分层过滤由 ChangeClassifier 和 RiskDetector 负责
- **禁止**读取 rules/ 规则文件——规则由成员按需加载
- **禁止**重复成员已做的工作

你（Team Lead）的唯一职责是：**搭建团队 → 启动流水线 → 等待报告 → 通知用户**。仅此而已。

### 1. 解析用户意图

从用户消息中提取：
- **源分支**（默认 master）
- **目标分支**（默认 uat）

例如用户说"审查 develop 和 release 的差异"→ source=develop, target=release

### 2. 创建 Agent Team

使用 `team_create` 创建团队：
- team_name: "code-review"
- description: "代码审查流水线：master→uat 分支差异审查"

### 3. Spawn 四个团队成员

使用 `Task` 工具 spawn 4 个成员。**重要：不要在 spawn 时预加载规则文件！** 每个成员的 prompt 只需包含其 Agent 指令文件路径，成员会在运行时自行判断项目类型并按需加载对应规则，避免浪费 token。

**成员 1：diff-collector**
- name: "diff-collector"
- prompt 中包含：`agents/DiffCollector.md` 的文件路径 + 源分支和目标分支
- mode: "bypassPermissions"

**成员 2：change-classifier**
- name: "change-classifier"
- prompt 中包含：`agents/ChangeClassifier.md` 的文件路径
- **不要**预加载 rules/ 文件，成员会根据项目类型自行读取
- mode: "bypassPermissions"

**成员 3：risk-detector**
- name: "risk-detector"
- prompt 中包含：`agents/RiskDetector.md` 的文件路径
- **不要**预加载 rules/ 文件，成员会根据文件类型自行读取
- mode: "bypassPermissions"

**成员 4：report-writer**
- name: "report-writer"
- prompt 中包含：`agents/ReportWriter.md` 的文件路径
- mode: "bypassPermissions"

### 4. 启动流水线

向 `diff-collector` 发送第一条消息，告知源分支和目标分支，启动整个流水线：
- type: "message"
- recipient: "diff-collector"
- content: "请开始采集 <source> 和 <target> 分支之间的代码差异"
- summary: "启动差异采集"

### 5. 等待完成（不要干预流水线）

启动后，**你只需等待**。流水线会自动运行：
- diff-collector → change-classifier → risk-detector → report-writer
- 成员之间通过 send_message 自行协调，不需要你中转

你只需：
- 如果某个成员超过 2 分钟没有响应，`@成员名` 询问状态
- 收到 report-writer 的报告完成通知后，向用户报告最终结果
- 工作完成后清理团队
