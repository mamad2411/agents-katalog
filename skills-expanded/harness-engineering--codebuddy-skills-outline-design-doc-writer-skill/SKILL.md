---
name: outline-design-doc-writer
description: 按 templates/outline-design.md 模板撰写概要设计文档。
allowed-tools: Read, Write, Edit, Glob
---

# Skill: outline-design-doc-writer

> 原文 §8.3 文档撰写类。

## 输入

- `requirement.md`（关联 REQ-*）
- `tech-research.md`（可选）
- 用户/Agent 给出的方案描述

## 强制章节

1. 总体方案（2-3 段）
2. 备选方案对比（至少 1 采纳 + 1 否决）
3. 系统架构图（ASCII / mermaid）
4. 关键决策点 DEC-*（每条带 `traces_to: [REQ-*]`）
5. 下游影响
6. 上线/灰度策略

## 写作准则

- DEC 编号连续，**不允许跳号**
- 架构图必须能反映"客户端 → 业务服务 → 下游依赖"的调用链
- 备选方案的"否决理由"必须写技术原因，不是"团队不熟"

## 输出

写到 `requirements/{project}/{req-id}/outline-design.md`。

## 自检

写完自动跑 `outline-design-quality-reviewer` Agent 的 O1~O6 检查，存在缺漏立刻 inline 补充并提示用户。
