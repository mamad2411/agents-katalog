---
name: project-state-init
description: 初始化 Codex 项目“项目记忆/状态管理”套件到当前项目根目录：复制 `AGENTS.md` 与 `.codex/skills/*`（handoff / handoff-resume / ops-sync 等）并可选生成 `.codex/state` 骨架。用于新项目快速启用长期项目工作流（ops-sync、handoff、审计）。
---

你是“项目状态初始化器”。目标：把“项目记忆套件”部署到当前项目根目录（或用户指定目录）。

# 默认源（可改）

默认优先从“当前这份已安装/已解压的本地套件根目录”复制；
若无法自定位，再回退到：
`D:\lucky\Supplies\个人\AI\CLI\codex\skills\项目持久上下文v2`

# 执行方式（脚本优先）

使用本 skill 自带脚本，避免手动复制出错：

1) 确认目标目录（默认当前目录）：
```powershell
pwd
```

2) 运行初始化（默认已安装跳过、缺失补装，不直接覆盖）：
```powershell
python "$env:USERPROFILE\.codex\skills\project-state-init\scripts\project_state_init.py"
```

常用选项：
- 指定目标目录：`--dest "D:\path\to\project"`
- 指定源目录：`--src "D:\lucky\Supplies\个人\AI\CLI\codex\skills\项目持久上下文v2"`
- 重装策略：`--mode backup|overwrite|skip`（默认 `skip`）
- 初始化 state 骨架：`--init-state`（创建 `.codex/state` 并生成 `BRIEF.md/progress.md/interaction-log.md`）

示例（推荐：初始化并生成 state 骨架）：
```powershell
python "$env:USERPROFILE\.codex\skills\project-state-init\scripts\project_state_init.py" --init-state
```

运行环境与依赖：
- 需要 **Python 3.8+**
- **不需要安装任何依赖**（纯标准库）
- 若你常用 conda（如 `forfun-c`），可用：`conda run -n forfun-c python "$env:USERPROFILE\.codex\skills\project-state-init\scripts\project_state_init.py" ...`

# 复制内容（默认）

- `{dest}/AGENTS.md`
- `{dest}/.codex/skills/*`（从源的 `.codex/skills/*` 复制）

默认**不复制**源里的 `.codex/state`（避免把别的项目状态带进来）。如需 state，使用 `--init-state` 生成干净骨架。

# 安装逻辑

- 若目标项目根目录没有 `.codex/`，脚本会自动创建
- 若检测到目标项目已完整安装本套 skills，默认直接跳过整套搬运
- 若 `.codex/skills/<skill>` 已完整存在，默认跳过
- 若只装了一部分，默认只补缺失文件
- 安装到项目后的本地 `project-state-init` 也能继续作为复制源使用
- `--src` 与 `--dest` 不能重叠；若要复制到别处，目标必须是另一个项目目录
- 只有显式使用 `--mode backup` 或 `--mode overwrite` 时，才会重装已存在内容

# 完成后检查

```powershell
Get-ChildItem -Force . | Select-Object Name,Mode
Get-ChildItem -Recurse -Force .codex\\skills | Select-Object -First 20 FullName
```
