---
name: bid-auto-all
description: |
  一键执行标书完整流程：招标分析→方案规划→全部方案撰写→审计整合→归档。
  支持标准/快速两种模式，自动编排所有阶段，支持断点续传。
  触发关键词：一键生成、全流程、自动投标、auto all、全自动、一键标书、快速标书、小项目、bid quick、快速模式。
argument-hint: "[tender-file-path] [--quick]"
---

# 一键全流程标书生成

自动编排从招标分析到归档的完整流程，支持断点续传。

## 模式判定

满足以下**任一**条件自动进入快速模式（也可手动 `--quick`）：
- 招标预算 < 100 万元
- F1+F2 格式评分点总数 < 10 个
- 需要生成的方案数 <= 3 个
- `plan_budget.md` 中 `项目规模：small`

| 环节 | 标准模式 | 快速模式 |
|------|---------|---------|
| 招标分析 | 4步 + 可选竞争分析 | 仅4步 |
| plan_budget 审核 | 暂停等人工确认 | 展示摘要 + 快速确认 |
| 篇幅预算 | 动态计算 | 取公式下限（small 规模） |
| 审计 | 完整 7 维度+口径校验 | 精简 3 维度（★项+评分点+篇幅） |

---

## 流程总览

```
Stage 1: 初始化 → Stage 2: 招标分析 → Stage 3: 方案规划
                                             │
                                     ⏸️ 人工审核（标准模式）/ 快速确认（快速模式）
                                             │
              Stage 5: 归档 ← Stage 4: 审计+整合 ← Stage 3.5: 方案撰写（顺序）
```

## 断点续传

| 阶段 | 完成标志（Glob 检查） | 恢复行为 |
|------|---------|---------|
| Stage 1 | `output/` 目录存在 | 不存在则 `Skill: bid-init` |
| Stage 2 | `output/tender_facts.md` + `scoring_map.md` + `bid_strategy.md` 三文件齐全 | 缺失则 `Skill: bid-analyze-tender $ARGUMENTS` |
| Stage 3 | `output/plan_budget.md` 存在且含"✅ 审核通过" | 未生成则 `Skill: bid-plan-scheme` |
| Stage 3.5 | 所有方案的 `output/summaries/{NN}_{solution_id}_summary.md` 存在 | 缺失的方案继续写 |
| Stage 4 | `final/标书技术方案完整版.md` 存在 | 不存在则 `Skill: bid-integrate-final` |

---

## Stage 1: 初始化

`Skill: bid-init`

## Stage 2: 招标分析

`Skill: bid-analyze-tender $ARGUMENTS`

Stage 2 需检查 3 个文件（均在 `output/` 下）：`tender_facts.md`、`scoring_map.md`、`bid_strategy.md`。

## Stage 3: 方案规划

`Skill: bid-plan-scheme`

### 标准模式：人工审核节点

方案规划完成后暂停，提示用户审核 `output/plan_budget.md`：
1. 评分点格式分类（F1-F5）是否正确
2. 方案清单是否完整
3. 目录草案是否覆盖所有评分关键词
4. 篇幅配额是否合理

审核通过后将状态改为"✅ 审核通过"，重新执行 `/bid-auto-all` 继续。

### 快速模式：快速确认

plan_budget.md 生成后输出关键摘要（方案清单 + 评分点归属 + 篇幅配额），等待用户快速确认后标记"✅ 审核通过"。plan_budget 定义了整个写作蓝图，跳过审核可能导致方案偏离，因此快速模式也需要用户确认这一步。

## Stage 3.5: 方案撰写

1. 从 `plan_budget.md` 方案清单提取全部方案名称（动态，不依赖预配置列表）
2. 检查 `output/summaries/` 中已有 summary 的方案，标记跳过
3. 按清单顺序逐个调用 `Skill: write-solution {方案名称}`（参数直接使用 plan_budget.md 中的方案名称）
4. 每完成一个，验证对应 summary 文件已生成
5. 当前方案失败则停止，修复后重新执行 `/bid-auto-all` 断点续传

## Stage 4: 审计 + 整合

`Skill: bid-integrate-final`

bid-integrate-final 内部完成：审计（7维度+口径校验）→ 整合 → 可选格式转换。

审计结论处理：
- "❌ 不可提交" → 输出问题列表，停止执行
- "⚠️ 建议修复后提交" → 询问用户继续还是修复
- "✅ 可提交" → 自动继续整合

快速模式下 bid-integrate-final 自动识别 `项目规模：small`，执行精简审计。★项响应不完整时自动退出快速模式，提示切换标准模式。

## Stage 5: 归档 [可选]

整合完成后询问用户是否归档：`Skill: bid-archive`

---

## 注意事项

1. 标准模式下 Stage 3 人工审核不可跳过
2. Stage 3.5 严格顺序撰写，前一个方案生成 summary 后再进入下一个
3. 所有方案遵循 `canon_current.md` 统一口径
4. 快速模式**不降低**写作质量底线（write-solution 8 项约束全部保留），只简化流程和审核节点
