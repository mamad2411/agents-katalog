---
name: bid-analyze-tender
description: |
  解析招标文件，3步生成：事实库（含术语）→ 评分点清单（含F1-F5分类+需求矩阵）→ 本地化策略分析。
  支持断点续传，已有产物自动跳过。
  前置条件：已执行 /bid-init 且招标文件已放入 inputs/tender/。后续步骤：/bid-plan-scheme。
  触发关键词：招标分析、评分点、需求矩阵、tender analysis、解析招标、分析招标文件、本地化策略、赢标策略、差异化分析。
argument-hint: "[tender-file-path]"
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# 招标文件分析

## 动态上下文

输入文件：$ARGUMENTS
默认路径：inputs/tender/

断点状态：
用 Glob 检查 output/ 下 tender_facts.md、scoring_map.md、bid_strategy.md 是否存在来判断断点。

---

## 三级职责定位

本技能负责**理解**阶段——提取事实、解析规则、推导策略。需要直接读取招标原文。

```
analyze-tender: 提取什么(facts) → 怎么评(scoring) → 怎么赢(strategy)
         ↓
plan-scheme: 口径 + 风险 + 将策略落地为写作蓝图
         ↓
write-solution: 按蓝图执行写作
```

---

## 执行流程

### Step 0: 一次性读取招标文件

招标原文只读一次，三步共享 context。

1. **定位文件**：按 $ARGUMENTS 路径或 Glob `inputs/tender/*` 找到招标文件
2. **全文读取**：PDF 用 pages 参数分批读完，Markdown/Word 直接 Read
3. 后续 Step 1-3 直接使用 context 中的内容，**不再重复 Read 招标文件**

**断点续传**：从 checkpoint 恢复时（某步骤产出已存在），仍需在 Step 0 读取全文一次（因上次 context 已丢失），然后跳过已完成的步骤。

---

严格按步骤 1→3 顺序执行。目标输出文件已存在时跳过该步骤。全部完成后生成汇总报告。

| 步骤 | 读取 reference 文件 | 输入 | 输出（output/下） |
|------|-------------------|------|-----------------|
| 1 | [extract-facts.md](references/extract-facts.md) | context 中的招标内容 + 联网搜索 | `tender_facts.md`（含专业术语库） |
| 2 | [parse-scoring.md](references/parse-scoring.md) | context 中的招标内容 + facts | `scoring_map.md`（含 F1-F5 分类 + 需求响应矩阵） |
| 3 | [localized-strategy.md](references/localized-strategy.md) | context 中的招标内容 + facts + scoring | `bid_strategy.md` |
| 汇总 | [summary-report-template.md](references/summary-report-template.md) | 各步骤摘要 | 输出报告 |

每步执行方式：Read 对应 reference 文件全文，按其中指导从 context 中的招标内容提取信息，写入输出文件。

### 步骤1特殊要求

- **行业自动识别**：根据招标文件内容判断行业分类（IT/工程建设/医疗器械/咨询服务/政府采购/通用），在 tender_facts.md 中增加 `行业分类：{类型}` 字段。

- **行业研究（必选）**：识别行业分类后，执行以下联网搜索，结果写入 tender_facts.md 的新章节「行业研究」：
  1. **现行标准规范**：搜索该行业最新的国标/行标/团标编号和名称（如 GB/T、YD/T、JGJ 等），标注发布年份
  2. **评标惯例**：搜索该行业招标评审的典型侧重点和常见扣分项
  3. **行业禁忌用语**：搜索该行业投标方案中应避免的表述，以及常被误判为禁用词的正当术语
  4. **术语核实**：对缩写全称、行业标准名称、设备标准叫法、定义不充分的术语逐一核实

- 提取事实信息后，继续提取专业术语，按类别分组整理

### 步骤2特殊要求

- 拆解评分点后，按 F1-F5 格式分类每个评分点（判断依据是评分标准的**表述方式**而非名称）
- 标记每个评分点是否「需要生成方案」（F1/F2→是，F3/F4/F5→否）
- 继续构建需求响应矩阵：读取 tender_facts.md 的技术要求摘要，关联评分点生成需求矩阵

### 步骤3特殊要求

- 本地化策略分析必须在招标原文上下文中执行（不是仅读摘要），以捕捉隐性需求和项目特异性细节
- 5个分析维度：评分权重ROI → 得分空间 → 项目特异性锚点 → 隐性需求 → 应答策略矩阵
- 产出独立文件 `bid_strategy.md`，供 plan-scheme 消费并织入作战清单

---

所有文件完成后提示下一步：`/bid-plan-scheme`。

> **效率建议**：尽量在单次 conversation 中完成全部 3 步。断点续传每次恢复都需重新读取招标文件（context 已丢失），比一次性执行多花约 1 倍 token。
