---
name: code-styleguide-skills
description: >
  Use when you need a single entry skill for code style guidance or
  router-based delegation to language-specific styleguide skills.
---

<!--
UpdatedAt: 2026-04-13 09:46:41 +0800
LatestChange: 移除 AGENTS.md 自初始化入口，安装与管理统一交给 skills.sh / npx skills add。
-->

# code-styleguide-skills

## 目标

提供一个统一入口，接收代码风格相关请求：

- `/code-styleguide-skills <代码风格问题>`

默认职责：

- 负责接收代码风格相关请求。
- 委托给 `styleguide-router` 识别语言、文件类型或上下文。
- 保持 styleguide 子技能体系不变，仅统一入口。

## 默认动作

1. 读取 `styleguide-router/SKILL.md`。
2. 由 router 识别语言、文件类型或上下文。
3. 再分发到对应 `styleguide-*` 子技能。

## 输出约束

- 风格问题保持“结论优先 + 最小示例 + 不改语义”。
