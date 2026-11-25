---
name: update-skill-with-log
description: 允许 organizer 和 player 调整 skill，但每次变更都必须同步做文档记录。
---

# 修改 skill 并记录

适用场景：

- 需要新增 skill
- 需要重写已有 skill
- 需要调整 skill 的触发条件、约束、推荐命令或工作方式

## 允许谁改

以下两类主体都可以改 skill：

1. **组织者侧 agent**
2. **player**

重点不是“谁来改”，而是：

> **只要改了 skill，就必须留下文档记录。**

## 必做动作

每次修改 skill，至少同时完成这两件事：

1. 更新对应的 `.github/skills/<skill-name>/SKILL.md`
2. 追加一条记录到 `knowledge/seed/skill-change-log.jsonl`

## 日志要求

每条记录至少应包含：

- `timestamp`
- `actor`
- `skill`
- `changeSummary`
- `reason`
- `relatedFiles`

如果是行为边界变化，还应补：

- `behaviorChange`

## 什么时候还要改其他文档

如果 skill 变更影响了仓库的主路径理解，还要同步更新这些文档中的相关部分：

- `README.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `PROJECT_DESIGN.md`

## 约束

- 不要只改 skill 文件而不记日志。
- 不要把 skill 变更只留在聊天里。
- 如果变更影响到主流程描述，不要漏改总文档。
