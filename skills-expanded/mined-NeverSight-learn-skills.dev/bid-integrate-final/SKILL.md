---
name: bid-integrate-final
description: |
  审计所有方案质量并整合为完整标书。
  Step 1 自动审计（7维度+口径校验），不通过则中止；Step 2 可选模拟评分；Step 3 方案整合；Step 4 可选格式转换。
  前置条件：output/solutions/ 中有方案文件。后续步骤：/bid-archive 归档。
  触发关键词：合规审计、质量检查、口径校验、模拟评分、最终整合、integrate、生成标书、输出文档、bid audit。
---

# 审计与整合

## 断点续传

| Step | 完成标志 | 恢复行为 |
|------|---------|---------|
| Step 1 | `output/audit_report.md` 存在且结论为 ✅/⚠️ | 跳过审计 |
| Step 2 | `output/simulate_scoring_report.md` 存在 | 跳过模拟评分 |
| Step 3 | `final/标书技术方案完整版.md` 存在 | 跳过整合 |

---

## Step 1: 自动审计（必选）

读取 `output/` 下的 `tender_facts.md`、`scoring_map.md`、`plan_budget.md`、`canon_current.md`、`risk_alert.md`，以及 `output/solutions/*.md`、`output/summaries/*.md`，执行以下检查，生成 `output/audit_report.md`。

### 检查项 0: 废标风险验证（最高优先级）

读取 `risk_alert.md`，逐项验证★项响应情况：
- ✅已验证：响应明确 + 证据完整（或有效占位符）
- ⚠️待补证：响应存在 + 证据缺失（有占位符）
- ❌未响应：无响应或不满足 → 结论直接判定"❌ 不可提交（废标风险）"

### 检查项 1-4

| # | 检查项 | 目标 |
|---|--------|------|
| 1 | 评分点覆盖率（对照 `scoring_map.md`） | 100% |
| 2 | ★项完整性（响应段落+证据支撑） | 100% |
| 3 | 篇幅达标（对照 `plan_budget.md` 配额） | ≥ 80% |
| 4 | 图表密度（每个 H2 至少 1 图 1 表） | 100% |

### 检查项 5: 口径一致性（含跨方案深度校验）

加载 `canon_current.md`，遍历 `output/solutions/*.md`，检测冲突：

| 冲突类型 | 说明 | 严重级别 |
|---------|------|---------|
| 数值冲突 | 同一字段在不同方案中数值不同 | 严重 |
| 术语冲突 | 同一概念使用不同术语 | 警告 |
| 承诺冲突 | 同一服务承诺值不一致 | 严重 |
| 缺失引用 | 使用了未定义的口径 | 提示 |

严重冲突需人工裁决，参考招标文件原文。口径模板见 [canon-templates.md](references/canon-templates.md)。

### 检查项 6-7

| # | 检查项 | 目标 |
|---|--------|------|
| 6 | 需求响应矩阵（从 `scoring_map.md` 提取需求） | ★项 100%，其他 ≥ 95% |
| 7 | 占位符格式（编号唯一、SS-XX001 格式） | 100% |

### 审计结论判定

| 优先级 | 条件 | 结论 |
|-------|-----|------|
| 最高 | ★项响应率 < 100% | ❌ 不可提交（废标风险） |
| 高 | 有严重口径冲突或高优先级问题 | ❌ 不可提交 |
| 中 | 有中低优先级问题 | ⚠️ 建议修复后提交 |
| 低 | 所有检查项达标 | ✅ 可提交 |

- ❌ → 输出问题清单，**中止执行**，不进入 Step 2-4
- ⚠️ → 询问用户继续还是修复
- ✅ → 自动继续

### 精简审计模式

当 `plan_budget.md` 中 `项目规模：small` 时，仅检查 3 维度：★项响应率、评分点覆盖率、篇幅达标率。

---

## Step 2: 模拟评分 [可选]

> 默认不执行。用户明确要求"模拟评分"/"模拟打分"时执行。

加载 `scoring_map.md` 评分标准 + 所有方案文件，逐项模拟评分。

**评分维度**（100 分制，按权重折算）：

| 维度 | 权重 | 说明 |
|------|------|------|
| 针对性 | 30% | 是否针对本项目特点而非通用模板 |
| 完整性 | 25% | 是否覆盖评分点要求的所有方面 |
| 可行性 | 20% | 方案是否切实可行、有具体措施 |
| 量化程度 | 15% | 是否有具体数据、指标、时间节点 |
| 表达质量 | 10% | 逻辑清晰、图表丰富、格式规范 |

**评审专家行为模型**：浏览时间有限（每方案 15-30 分钟）→ 标题/图表/摘要影响第一印象；关键词匹配 → 对照评分表逐条查找；对比心态 → 差异化亮点更易获高分；疲劳效应 → ★项和高分值评分点应排前面。

详细评委模型见 [evaluator-scoring-guide.md](references/evaluator-scoring-guide.md)。

输出：`output/simulate_scoring_report.md`（预测总分、逐项评分、薄弱环节、改进优先级）

---

## Step 3: 方案整合

运行 [integrate.py](scripts/integrate.py)，脚本自动完成：扫描方案文件 → 按编号排序 → 统一标题和图表编号 → 输出 `final/标书技术方案完整版.md`。

## Step 4: 格式转换 [可选]

1. 运行 [render.py](scripts/render.py)，参数：`--input final/标书技术方案完整版.md --output final/标书技术方案完整版-带图片.md --images-dir final/images/`
2. 运行 [convert.py](scripts/convert.py)，参数：`--input final/标书技术方案完整版.md --output final/标书技术方案完整版.docx --reference` [reference.docx](reference.docx)

---

## 输出文件

| 文件 | 说明 |
|------|------|
| `output/audit_report.md` | 审计报告（含口径校验结果） |
| `output/simulate_scoring_report.md` | 模拟评分报告（可选） |
| `final/标书技术方案完整版.md` | 标准化整合稿 |
| `final/标书技术方案完整版-带图片.md` | 图表已渲染版本（可选） |
| `final/标书技术方案完整版.docx` | Word 版本（可选） |

## 依赖

| 功能 | 依赖 | 安装 |
|------|------|------|
| Mermaid 渲染 | mermaid-cli | `npm install -g @mermaid-js/mermaid-cli` |
| DOCX 转换 | Pandoc | pandoc.org/installing.html |

完成后提示下一步：`/bid-archive`。
