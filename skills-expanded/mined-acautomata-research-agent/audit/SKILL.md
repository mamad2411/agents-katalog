---
name: audit
description: Audit the quality of analysis-chain outputs (extract/critic/design/spec) — read-only. Triggers: 质量审计, audit, 质量评估, 流水线审计.
---

# audit — 流水线产出质量审计

## Mission

对 `extract`–`critic`–`design`–`spec` 全部或部分产出做结构化质量审计，产出完整审计报告（Markdown）。**只评估，不修改原文档。**

## When to use

- 一段分析链跑完后，需要质量门检查产出结构、边界、一致性
- 用户请求"审计一下这些产出""质量检查"

不要用于：重做上游阶段、评价论文内容本身、修改产出。

## 评估维度

- **结构完整性**：对照各阶段模板，检查 Section 标题是否齐全
- **字段覆盖**：检查必填字段是否有内容（"论文中未明确说明"也算有效填充）
- **阶段边界遵守**：检查每个阶段是否声明并确实未越界
- **缺失信息标注**：检查是否使用规范用语标注未提供信息（"论文中未明确说明""现有材料不足以确认"，不出现"可能是""应该是""推测为"）
- **证据强度分级**（critic 专项）：检查三类判断是否正确区分
- **跨阶段一致性**：检查数值、引用、优先级传递在链路中是否一致

### 结构完整性参照

- `ingest` 论文页: 11 节（## Citation / ## One-Sentence Contribution / ## Problem Setting / ## Method / ## Experiments / ## Results / ## Limitations / ## Reusable Claims / ## Connections / ## Open Questions / ## Provenance）
- `extract` 实验提取: 12 节（## 0–## 11）
- `critic` 问题分析: §0–§7
- `design` 验证设计: 9 节（## 0–## 8）
- `spec` claude-code 提示词: 标题必须为 `# 发给 claude-code 的完整任务提示词`

> 以上节数与章节名为当前快照；各 skill 的「输出结构」节是权威来源，冲突时以源为准。

### 阶段边界检查

- `ingest` 禁止：批判分析、推测、实验设计建议
- `extract` 禁止：完整问题挖掘、方法改进方案、最终结论
- `critic` 禁止：完整实验设计方案、新方法提出、最终定论
- `design` 禁止：最终实验结论、新方法提出
- `spec` 禁止：臆造代码路径（缺失时必须用占位符）

## 输入

`extract` / `critic` / `design` / `spec` 的全部或部分产出（通常从 wiki 读取）。

## 工作原则

- 只评估，不修改原文档
- 每条扣分都有具体位置和具体原因
- 区分"必须修复"（阻塞下游）和"建议改进"（不阻塞）
- 不确定处标注"建议人工复核"
- 不重复执行上游 skill 的工作

## 输出结构

输出为一份完整 md，先写到 `raw/sources/<slug>.md`，然后调用 `ingest`（传入该 md 文件路径，`page_type: analysis`）统一写入 wiki；**不直接调用 `wiki_apply` 建页**：

```markdown
# 论文审稿流水线质量评估报告

`category: audit`

## 0. 评估元信息
## 1. 总览（各阶段 × 各维度表格）
## 2. 逐阶段详细评估
## 3. 跨阶段一致性问题
## 4. 必须修复项（阻塞下游）
## 5. 建议改进项（不阻塞但建议优化）
## 6. 总体评估（可用性、最突出问题、建议优先修复）
```

## 完成门禁

- 覆盖全部 6 个审计维度
- blocking issues 可操作（带具体位置和修复方向）
- 产出 md 已经 `ingest` 写入 wiki（含 wiki 路径），且本 skill 未直接调 `wiki_apply` 建页
- 产出 md 在 `# Title` 下空一行包含 `` `category: audit` ``（作为可机读类别标识，供外部统计脚本提取）
