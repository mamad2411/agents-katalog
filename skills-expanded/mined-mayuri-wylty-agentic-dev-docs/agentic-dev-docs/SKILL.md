---
name: agentic-dev-docs
description: >-
  Strict manual-trigger skill for lightweight docs-first agentic development planning.
  Use only when the user explicitly invokes it (/agentic-dev-docs in Claude Code, $agentic-dev-docs in Codex,
  or "use agentic-dev-docs skill"). Three usages: (1) init - scaffold the project workspace
  (docs/rules/tests directories plus bundled brainstorming, writing-plans and grill-me/grilling skills);
  (2) default plan mode - docs-first DAG planning with a fixed prompt, brainstorming interview and writing-plans,
  then DAG (+ Agent Teams) execution after approval; (3) grill / super-interview mode - same flow but the interview uses grilling.
disable-model-invocation: true
metadata:
  version: 1.0.0
---

# agentic-dev-docs

轻量化文档优先开发规划：固定提示词 + plan 模式 + 头脑风暴采访 → DAG plan → 批准后备份并执行。

## 子命令路由

本 skill 目录 = 本 `SKILL.md` 所在目录，下文记作 `<skill_dir>`。调用方式：Claude Code `/agentic-dev-docs [init|grill] <需求>`（`disable-model-invocation` 使其只能由用户斜杠调用）；Codex `$agentic-dev-docs`；其他 harness 按其显式调用 skill 的方式。

子命令只看用户参数的**首个词**：`init`、`grill`、`grill-me`、`update-vendor`；参数以「超级采访」开头也进入 grill。这些词出现在其他位置不触发。

| 用户输入 | 动作 |
|---|---|
| `init` | 不进入 plan 模式（用户显式要求的初始化动作，直接执行）。读 `references/init.md`，运行 `python <skill_dir>/scripts/init_workspace.py --root <项目根> --harness <当前 harness>`（`claude-code`/`codex`/`workbuddy`/`dsh`，按自身身份传入，不要依赖 `auto`；建议先加 `--dry-run`）。npx 可能较慢，用后台运行或设置 ≥300 秒超时；网络受限加 `--offline`。Windows 无 `python` 用 `py -3`；无 Python 按 `references/init.md` 的兜底步骤手工完成。结果不自动提交，提示用户检查后自行提交，或授权 agent 提交 |
| 默认（无子命令，含用户描述的需求） | 执行下文「默认规划流程」 |
| `grill` / `grill-me` / 以「超级采访」开头 | 同默认流程，但采访用 `grilling`（见 `references/planning-workflow.md` 第 6 节） |
| `update-vendor` | 用户项目：`python <skill_dir>/scripts/update_vendor.py --project <项目根> --check`，确认后去掉 `--check`。不带 `--project` 是维护者刷新 skill 自带 `vendor/` |

## 硬规则

1. 仅在用户显式点名本 skill 时使用，不自行触发。
2. plan 批准前只读：只可写 harness 指定的 plan 文件；不写项目文件、不装依赖、不 commit、不派发实施子代理。
3. 规划阶段只持久化 plan，不写 spec、需求、用户故事等其他文档，除非用户要求。
4. 批准后第一步：把批准版 plan 原样备份到 `docs/05-agent-prompts/plans/YYYY-MM-DD-<topic>.md`，并立即单独本地提交（`docs(plan): ...`，非 git 仓库跳过提交），再做其他事。
5. `init` 绝不覆盖已有文件；`CLAUDE.md` / `AGENTS.md` 已存在时只给建议，`.gitignore` 只追加。
6. 每个 DAG 节点验证通过后做一次本地 commit；未经用户显式授权，禁止 push、创建 PR、修改远程与 tag。
7. 派发子 agent 必须显式给出 model + effort；用户显式指定的优先于 plan 与档位表（见 `references/model-tiers.md`）。
8. 运行时拒绝所选模型或 effort 时如实报告，不静默降级、不静默换模型。

## 默认规划流程

细则见 `references/planning-workflow.md`。

1. **plan 模式关卡**：Claude Code 立即调用 `EnterPlanMode`；其他 harness 按 `references/harness-matrix.md` 第 3 节降级（提示用户切换，或自行遵守只读纪律）。
2. **定位内置 skill**：用户已装的同名 skill 优先（含插件命名空间，如 `superpowers:brainstorming`）；否则读项目 `.agents/skills/` 或 harness skills 目录；再否则读本 skill `vendor/` 快照的 SKILL.md 并按其执行；快照也缺失说明本 skill 安装损坏，停止并告知用户重新安装本 skill，不得凭记忆复述。
3. **载入总指令**：把下方固定提示词与本轮需求一并作为采访输入。
4. **采访**：用 `brainstorming`（grill 模式用 `grilling`）；能靠只读手段查清的事实不问用户；用户确认理解一致后结束。
5. **写 plan**：用 `writing-plans` 产出 DAG plan，骨架 `assets/workspace/plan.template.md`；每个节点含 id / 目标 / 写入文件 / depends_on / 档位与 model+effort / 验证。
6. **请求批准**：Claude Code 调 `ExitPlanMode`；其他 harness 在对话中贴出 plan 并明确请求批准。未获批准不实施。
7. **备份**：批准后第一步按硬规则 4 备份 plan。
8. **执行**：按 `references/execution-dag.md`。

## 固定提示词（逐字，不得改写）

> 使用头脑风暴分析理解并梳理完善，并采访我对齐不明确的需求，再拆分任务并制定一份面向agent的执行plan：1.允许混排采用DAG+Agent Teams 模式 2.若涉及前端页面，则前端页面避免不必要的辅助标签与说明。让布局本身发挥解释作用。

## 对上游内置 skill 的关键覆盖

冲突时以本节为准，完整对照表见 `references/planning-workflow.md` 第 3 节。

- 不写 `docs/superpowers/specs|plans`：设计内容并入 plan；plan 模式下写 harness 指定文件，批准后备份到 `docs/05-agent-prompts/plans/`。
- writing-plans 末尾的「选择执行方式」删除，改为本 skill 的 `references/execution-dag.md`。
- 未打包的 skill（`subagent-driven-development`、`executing-plans`、`using-git-worktrees`、`test-driven-development` 等）降为「若已安装可用」，未安装不报错。
- brainstorming 允许「跳过提问」，但跳过后仍须产出 plan 并走批准关卡。
- grill 模式直接调用 `grilling`；`grill-me` 带 `disable-model-invocation`，只是转调，不要调用它。

## 执行模式

检测到 Agent Teams 用「DAG + Agent Teams」，否则用「单 DAG」（子代理并行或串行）；写同一文件的节点不并行；lead 只协调、验收、提交。判定与派发细则见 `references/execution-dag.md`。

## 模型三档

核实于 2026-11-17，模型名与 effort 更新快，以运行时为准，详见 `references/model-tiers.md`。其他 harness 只记档位。

| 档位 | 适用任务 | Claude Code（model / effort） | Codex（model / reasoning effort） |
|---|---|---|---|
| 高 | 架构、跨模块设计、安全、最终审查、复杂算法 | `opus` / `high` | `gpt-6.1-sol` / `high` |
| 中 | 常规实现、测试、文档 | `sonnet` / `medium` | `gpt-6.1-sol` / `medium` |
| 低 | 机械搬运、格式化、检索与摘要 | `haiku` / `low` | `gpt-6-luna` / `medium` |

## 文件索引

- `references/init.md`：init 细则、参数、幂等规则、无 Python 兜底。
- `references/planning-workflow.md`：固定提示词融合、上游覆盖对照表、plan 必备内容、备份与 grill 规则。
- `references/execution-dag.md`：执行模式判定、派发 brief、节点验收与提交、阻塞处理、收尾。
- `references/model-tiers.md`：三档到各 harness 模型与 effort 的映射及核实来源。
- `references/harness-matrix.md`：各 harness 的 plan 模式、skills 目录、子代理与 Teams 能力，`npx skills` 说明。
- `assets/workspace/`：init 使用的模板（`CLAUDE.md.tmpl`、`AGENTS.md.tmpl`、`gitignore.tmpl`、`plan.template.md`）与 `rules/` 种子。
- `scripts/`：`init_workspace.py`（初始化）、`install_vendor.py`（安装内置 skill）、`update_vendor.py`（刷新上游快照）。
- `vendor/`：内置 skill 快照（superpowers 的 `brainstorming`、`writing-plans`，mattpocock 的 `grill-me`、`grilling`）、`VENDOR.lock.json` 与许可证。
