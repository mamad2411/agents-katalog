---
name: bootstrap-gate
description: Use when entering a frontend project that may need dev-frontend-pro initialization, mission recovery, or minimum context validation
---

# Bootstrap Gate

## 核心规则

先确认入口和 mission，再进入任何开发阶段。

## 检查

- `.ai/dev-frontend-pro/agents/orchestrator/AGENTS.md`
- `.ai-src/dev-frontend-pro/`
- `.ai-src/dev-frontend-pro/missions/`
- `missionId`
- `.ai-src/dev-frontend-pro/missions/{missionId}/config.json`

## 处理

- `.ai` 入口缺失：停止并提示安装或链接。
- `.ai-src` 缺失：询问是否初始化。
- mission 缺失：新需求可初始化，继续任务必须确认 `missionId`。
- 字段不足：只询问当前阶段最低必要字段。

## 工具

- `scripts/init-mission.mjs`
- `scripts/validate-mission.mjs`
