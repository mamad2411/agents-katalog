---
name: dynamic-agent-context
description: 在项目中安装并刷新动态学习上下文（.agent-context、AGENTS.md、learned-conventions.mdc）。适用于编写代码、工程架构代码设计、测试、重构、代码审查、修复 bug 任务。
---

# Dynamic Agent Context 安装与使用

将项目已有代码自动提炼为 AI 可执行约定，并在代码任务中按需加载。

## 什么时候使用

- 在新项目启用 AI 编程规范
- 在旧项目把“人工口头规范”变成“自动学习规则”
- 代码风格漂移明显，需要统一 AI 输出

## 标准操作

### 1) 部署脚本到项目

```bash
mkdir -p scripts
cp ~/.cursor/skills/dynamic-agent-context/scripts/generate_agent_context.py scripts/
cp ~/.cursor/skills/dynamic-agent-context/scripts/refresh_agent_context.py scripts/
cp ~/.cursor/skills/dynamic-agent-context/scripts/sync_agent_entrypoints.py scripts/
```

### 2) 首次生成

```bash
python scripts/refresh_agent_context.py --full
```

### 3) 验证输出

```bash
test -f .agent-context/conventions.md
test -f .agent-context/project-context.md
test -f .agent-context/metadata.json
test -f AGENTS.md
test -f CLAUDE.md
test -f .cursor/rules/learned-conventions.mdc
```

## AI 加载路径

- Cursor: `.cursor/rules/learned-conventions.mdc`（`alwaysApply: false`，代码相关任务按需加载）
- Claude Code/OpenCode/Codex: 通过 `AGENTS.md` / `CLAUDE.md` 进入 `.agent-context/*`

## 刷新策略

- 全量：`python scripts/refresh_agent_context.py --full`
- 增量：`python scripts/refresh_agent_context.py --changed-only`

## 注意事项

- `.agent-context/*` 属于机器生成文件，手改会被刷新覆盖（`Maintainer Notes` 区域除外）
- `learned-conventions.mdc` 为自动生成文件，不建议手改
