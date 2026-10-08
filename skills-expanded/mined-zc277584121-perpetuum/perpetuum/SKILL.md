---
name: perpetuum
description: 为一个或多个项目建立、运行和管理长期 Agent 队伍。适用于初始化长期自主工作、按项目 cron 计划持续推进 Story、查看或调整 Story 看板，以及处理人类输入。
---

# Perpetuum

Perpetuum 把真实项目目录组织成可长期运行的 Story 看板。本地 Runner 按每个项目自己的 cron 计划创建临时 Project Supervisor；Project Supervisor 再通过 `cc-use` 调度 Story Supervisor 和下级 Agent。长期 Goal、队伍契约、Story、可信历史、人类输入和运行状态都保存在项目自己的 Harness 中。

## 依赖

- **必须依赖 [cc-use](https://github.com/zc277584121/cc-use)**：负责所有 Agent 上下级之间的交互式 TUI session 创建、观察、继续对话和关闭。当前 Agent 无法加载 `cc-use` 时，不要建立或启动 Harness；先让用户按 cc-use 仓库说明安装或修复。Perpetuum 只描述调用意图，不复制 cc-use 的具体命令和参数。
- **必须依赖 [uv](https://docs.astral.sh/uv/)**：管理 Perpetuum 本地 Python 运行时。
- **可选依赖 [MemSearch](https://github.com/zilliztech/memsearch)**：初始化时用于召回项目历史。不可用时直接检查项目文件并通过对话补齐信息，不影响核心运行。

## 核心名词

- **Project**：一个需要长期推进的真实项目目录。前端中一个 Project 对应一个 Story 看板页面。
- **Harness**：Perpetuum 为 Project 保存的 Goal、队伍契约、Story、人类输入、运行计划和状态，默认位于 `~/.perpetuum/projects/<project-id>/`。
- **Runner**：非 Agent 的本地后台服务。它解释 cron、创建顶层交互式 TUI、维护生命周期并提供前端，不做业务判断。
- **Project Supervisor**：Runner 为某个项目的一次激活创建的临时管理 Agent。它选择至多一张 Story，并通过 `cc-use` 调用 Story Supervisor。
- **Story Supervisor**：只服务一张 Story，是具体任务的 Supervisor；按 `team.md` 调度必选 Executor 和可选的 Validator、Explorer。
- **Story**：唯一的业务工作粒度。一张卡片对应一个完整、可验证的业务成果和一条连续的 Agent 工作链。
- **session**：由 tmux 承载的交互式 Agent TUI。每个父节点只管理自己明确创建并保存了精确名称的直属 session。
- **Playbook**：某个角色的软性工作指南；它不是必须逐字发送的固定 Prompt。

完整结构和调用方向见 [architecture.md](references/architecture.md)。Story 文件格式和渐进式披露规则见 [story.md](references/story.md)。

## 按当前工作读取参考

| 当前工作 | 必读参考 |
|---|---|
| 理解整体结构或职责边界 | [architecture.md](references/architecture.md) |
| 初始化或注册项目 | [setup.md](references/setup.md)，再读 [story.md](references/story.md) 和 [runtime.md](references/runtime.md) |
| 创建、查看或调整 Story | [story.md](references/story.md) |
| 启动、停止、查看、暂停、恢复或调整 cron | [runtime.md](references/runtime.md) |
| 处理人类指令、业务问题或管控异常 | [human-communication.md](references/human-communication.md) |
| 调整 Project Supervisor | [project-supervisor.md](references/playbooks/project-supervisor.md) |
| 调整 Story 和 session 生命周期 | [story-supervisor.md](references/playbooks/story-supervisor.md) |
| 调整执行、验证或后续探索 | [executor.md](references/playbooks/executor.md)、[validator.md](references/playbooks/validator.md)、[explorer.md](references/playbooks/explorer.md) |

只读取与当前工作相关的参考，不要把全部文档无差别加载进上下文。

## 核心规则

1. 初始化时先检查项目和可用历史，再通过可多轮的对话与用户共同形成完整 Goal、队伍契约、第一批 Story 和运行计划。用户没有明确指定、也没有明确委托 Agent 决定的长期行为或授权都必须询问；建议、默认值、历史偏好和沉默都不算确认。待决项清零并由用户确认合并后的完整契约后，才能建立 Harness。
2. `goal.md` 是长期业务契约；`team.md` 是角色启用、职责、触发条件、调用图和完成门槛的唯一事实来源；`stories/*.md` 是 Story 的唯一事实来源；`history.md` 只保存通过已配置完成门槛的结论和重要决定；`schedule.yaml` 是该项目自动启动计划的唯一事实来源。
3. Runner 只机械解释标准五字段 cron。匹配后，如果该项目没有活动的 Project Supervisor，就创建新的交互式 Codex 或 Claude Code TUI，并发送一次启动 Prompt；已有活动链路时不重复创建，也不重复发送 Prompt。
4. Project Supervisor 先读取 `team.md` 和 Story front matter，从已有 `in_progress` 或 `ready` Story 中选择一张，再通过 `cc-use` 启动唯一的 Story Supervisor。没有可运行 Story 时，只有 `team.md` 启用 Explorer 且配置了空看板触发点才调用它；空看板 Explorer 新建了当前已经到期且可立即执行的 `ready` Story 时，同一个 Project Supervisor 重新读取元数据并继续选择，否则正常 Idle。
5. Story Supervisor 必须创建一个 Executor。Validator 和 Explorer 均为可选，只能按 `team.md` 的职责、触发点与顺序创建；不得因为通用 Playbook 提到某个角色就擅自启用。每个已启用角色正常只创建一个 session，并在反馈往返时复用原 session；父 Supervisor 在创建后立即持久化精确名称，在关闭时先保存 `finish` 的结构化结果再清除活动记录。
6. 启用 Validator 时，由独立 Validator 决定接受或退回；未启用时，由 Story Supervisor 根据 Story 验收标准、Executor 的可复查证据和 `team.md` 约定的完成门槛判断本轮结果。启用 Explorer 时，只在契约指定的稳定触发点维护未来 Story。取消使用 `cancelled`，不物理删除 Story 文件。
7. 同一 Project 同时最多执行一个 Story；不同 Project 可以并行，不设置跨项目的全局 Story 数上限。
8. cron 只决定是否开始一次新的 Project 激活。已经开始的 Story 可以跨出 cron 匹配时间继续完成，不设置固定 Story 时长。
9. Story 需要等待人类、管控处理或长期外部条件时，先把进展、证据、等待原因和恢复入口写入 Story 文件，再关闭本轮实际创建的下级角色和 Story Supervisor。恢复时仍是同一个 Story，但使用新的物理 session。
10. 需要人类做业务选择时写入 `questions.md`；环境、权限、认证、进程、配额、磁盘、网络或基础设施问题写入 `escalations.md`。两者都要关联 Story ID，并写清背景、影响、证据、建议和人类需要做的最小决定。
11. Runner 对每个新建的 Project Supervisor 只发送一次中文启动 Prompt。启动、承载 session、项目路径和完成回执属于确定性边界；Story 选择、下级 Prompt 和具体工作方式由 Playbook、Harness 与真实结果决定。
12. 所有顶层 Agent 都使用交互式 TUI，不以 `codex exec`、Claude Code `-p` 或其他非交互模式代替。其他父 Supervisor 只在新建 session、收到实际结果、已启用角色返回反馈、人类补充决定或外部条件实质变化时发送 Prompt。
13. 无人值守运行期间，不自动更新 Codex、Claude Code、模型或认证配置。遇到更新提示时跳过并继续；因此无法继续时记录管控异常。
14. `project.yaml` 只记录 Agent 类型，`team.md` 记录业务角色编排，`schedule.yaml` 只记录时区和 cron 等运行控制。Runner 通过 `PATH` 解析真实可执行文件；下级 Agent 的运行细节由 cc-use 管理，不依赖 shell alias，也不写入项目配置。

## 脚本入口

所有运行时和 Story 文件操作都使用本 Skill 的 `scripts/perpetuum`。默认用 Skill 安装目录下的绝对路径调用；只有用户明确把它加入 `PATH` 后，才使用 `perpetuum` 简写。

初始化必须遵循 [setup.md](references/setup.md) 的确认流程。查看 Story 命令和 front matter 规则时读取 [story.md](references/story.md)；查看目录、状态、cron、顶层 TUI 和前端行为时读取 [runtime.md](references/runtime.md)。
