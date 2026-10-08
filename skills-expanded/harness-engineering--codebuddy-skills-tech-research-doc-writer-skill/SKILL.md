---
name: tech-research-doc-writer
description: 写 tech-research.md。把候选方案、benchmark、风险、POC 建议组织成机读结构。
allowed-tools: Read, Write, Edit, WebSearch, WebFetch
---

# Skill: tech-research-doc-writer

> 原文 §8.3 文档撰写类。是 `tech-feasibility-assessor` Agent 的输出器。

## 强制章节

1. 背景与目标
2. 约束（性能 / 成本 / 合规）
3. 候选方案（≥ 2）
4. 多维度评分表
5. 推荐 + 理由
6. 风险与 mitigation
7. POC 建议（可选）
8. 关联设计决策（待 detail-design 引用）

## 评分表格式

| 方案 | 可靠性(30) | 性能(20) | 熟悉度(15) | 运维(15) | 锁定(10) | 安全(10) | 总分 |

每个分数必须 cite 证据（文档 / benchmark / 团队历史）。

## 反模式

- ❌ 无 cite 的评分
- ❌ 候选方案 < 2
- ❌ 把"推荐"写在"对比"之前（影响客观性）
