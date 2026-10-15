---
name: novel-to-script-team
description: 完整的多Agent多Skill小说改编项目。开源版运行时依赖 agents/skills/references，原始 sources 不随仓库分发。
---

# novel-to-script-team

## 运行入口
1. `./AGENTS.md`：平台无关的 Agent 总入口（推荐）
2. `./CLAUDE.md`：Claude Code 兼容入口，会指向 `AGENTS.md`
3. `./SKILL.md`：项目 Skill 元信息

## 执行序列
`~ingest -> ~analyze -> ~plan -> ~write N -> ~review N -> ~storyboard-film N` 或 `~storyboard-seedance N`（可选 `~generate-images N`）

## 目录职责
1. `agents/`：职责角色
2. `skills/`：可执行规则
3. `references/`：精华方法论
4. `knowledge/`：注册表、吸收映射、项目记忆
5. `outputs/`：本地产出目录（被 `.gitignore` 忽略）

## 运行约束
1. 运行时优先读取 `references/`、`agents/`、`skills/`
2. `sources/` 与 `pending-knowledge/` 是可选的本地原始资料池，默认不随开源仓库分发
3. 所有产出必须通过两步审核（业务 + 合规）
4. 使用 `outputs/{剧本名}/.agent-state.json` 保持 agent 上下文连续性（详见 `AGENT-STATE-GUIDE.md`）
