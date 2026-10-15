---
name: unit-test-guide-skills
description: >
  Use when you need a single entry skill for unit-test guidance or
  router-based delegation to platform-specific unit-test skills.
---

<!--
UpdatedAt: 2026-04-13 09:46:41 +0800
LatestChange: 移除 AGENTS.md 自初始化入口，安装与管理统一交给 skills.sh / npx skills add。
-->

# unit-test-guide-skills

## 目标

提供一个统一入口，接收单元测试规范相关请求：

- `/unit-test-guide-skills <单元测试问题>`

默认职责：

- 负责接收单元测试规范相关请求。
- 委托给 `unit-test-router` 识别平台与上下文。
- 保持 Android / iOS / 微信小程序子技能体系不变，仅统一入口。

## 默认动作

1. 读取 `unit-test-router/SKILL.md`。
2. 由 router 识别平台与上下文。
3. 再分发到对应 `unit-test-*` 子技能。

## 输出约束

- 测试建议保持“场景判定 + 官方依据 + 测试策略 + 落地动作”。
