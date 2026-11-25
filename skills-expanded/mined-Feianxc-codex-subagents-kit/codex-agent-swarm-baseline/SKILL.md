---
name: codex-agent-swarm-baseline
description: Baseline 版 Codex swarm/orchestration skill，用于在 skill-lab 中与优化版做对比测试。
---

# Codex Agent Swarm

把这个 skill 当成 Codex 的编排器，而不是神化成“原生团队 runtime”包装器。
如果 Codex 当前技能目录里还存在 `agent-team-planner` 之类的 Claude Code team skill，把它视为错误来源而不是候选方案。

优先目标：

1. 做完整 preflight，而不是直接开子任务。
2. 区分哪些任务值得独立 agent，哪些不值得。
3. 把 run 状态落到固定 artifacts，而不是只留在上下文里。
4. 对 native multi-agent 能力保持诚实探针；没有就降级为 `codex exec` child runs。
5. 结束后做回归与审计。

## Codex-Only Rule

这个 skill 是 Codex 侧的唯一 swarm/orchestrator skill。

规则：

1. 在 Codex 里不要复用 Claude Code 的 `agent-team-planner`。
2. 不要声称存在 `TeamCreate` / `TaskCreate` / `TeamDelete` 这类 CC team runtime，除非当前 Codex session 真有直接证据。
3. 只承诺当前 Codex 能做的事：controller orchestration、artifact registry、child `codex exec`、run audit。
4. 如果发现旧 CC skill 仍被挂到 `~/.codex/skills/`，应优先把它从 Codex 视野中移除，再继续本 skill。

## 默认工作方式

默认按下面顺序选择模式：

1. `blueprint-only`
   - 需求还不够清楚，或高风险，不适合立刻执行。
2. `single-controller`
   - 任务不大，或者文件边界高度重叠，spawn 成本高于收益。
3. `native-multi-agent`
   - 只有在当前 Codex runtime 明确暴露原生多代理能力，且你有实际证据时才使用。
4. `artifact-orchestrated-swarm`
   - 当存在 spawn-worthy 任务，但 native 证据不足、当前 session 没暴露原生 agent 工具、或 native 能力不稳定时使用。
   - 通过 `codex exec` 子运行、固定文件目录、task registry、protocol audit 来模拟稳定 swarm。

不要把 `artifact-orchestrated-swarm` 写成“原生多代理已启用”。这两者不是一回事。

## Step 1: 做 Preflight

先明确：

- `final_goal`
- `deliverables`
- `constraints`
- `success_criteria`
- `spawn_candidates`
- `tasks_not_worth_spawning`

如果用户没有给全，也不要卡住。直接声明关键假设并继续。

复杂任务先初始化 run：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "C:/Users/feian/.codex/skills/codex-agent-swarm/scripts/init_codex_swarm_run.py" `
  -ScriptArgs @("--workspace-root",".","--case","my-task")
```

生成的标准目录：

```text
.workspace/codex-swarm/runs/<run_id>/
```

默认要有这些 artifacts：

- `preflight.md`
- `agent-blueprints.md`
- `execution-plan.md`
- `task-registry.md`
- `protocol-audit.md`
- `team-report.md`

按需读取：

- `references/decision-matrix.md`
- `references/multi-agent-hardening.md`
- `references/codex-runtime-notes.md`

## Step 2: 做 Spawn Gate

只有满足全部条件时才值得独立 agent：

1. 有独立目标，不是“顺手一起做”。
2. 输入和输出路径稳定。
3. 验收标准可写清楚。
4. 与其他 agent 的热文件重叠低。
5. 协调成本低于收益。

如果写不出以下字段，就不要 spawn：

- `owner`
- `blocked_by`
- `input_path`
- `output_path`
- `acceptance`
- `spawn_reason`

`task-registry.md` 至少维护这些列。不要只写“研究一下”“看情况处理”。

## Step 3: 做 Capability Gate

先做现实判断，不要脑补。

最小探针：

1. 运行 `codex features list`，确认 `multi_agent` 是否开启。
2. 观察当前 session / runtime 是否真的暴露原生 agent 工具证据，例如 `spawn_agent`、`send_input`、`wait`、`close_agent`。
3. 只有同时满足“feature flag 开启 + 当前 session 有原生 agent 工具证据 + 任务通过 spawn gate”时，才优先 `native-multi-agent`。
4. 如果缺少任一关键证据，就使用 `artifact-orchestrated-swarm`。

当前本机已知参考见 `references/codex-runtime-notes.md`。
需要把当前环境的最新探针结果落盘时，执行：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "C:/Users/feian/.codex/skills/codex-agent-swarm/scripts/probe_codex_swarm_runtime.py" `
  -ScriptArgs @(
    "--run-root",".workspace/codex-swarm/runs/<run_id>",
    "--native-tool","spawn_agent",
    "--native-tool","send_input",
    "--native-tool","wait",
    "--native-tool","close_agent"
  )
```

规则：

- 不要因为 skill 叫 swarm，就默认声称 native multi-agent 可用。
- 不要把 child `codex exec` run 称为 native multi-agent。
- 不要为了“看起来像官方”而伪造能力。

## Step 4: 优先执行 Native Multi-Agent

只有在 capability gate 已满足时才走这里。

做法：

1. 主控保留 preflight、registry、最终验收和 audit 所有权。
2. 只把独立、边界清晰、收益高于协调成本的任务交给原生 agent。
3. 通过当前 session 暴露的原生 agent 工具进行创建、派发、等待、复用与关闭。
4. 在 `protocol-audit.md` 里明确记录 native 证据，例如：feature flag、当前 session 工具名、agent id、关键等待点。
5. 如果执行中发现工具缺失、结果不稳定、或文件边界开始冲突，立即降级回 `artifact-orchestrated-swarm`。

原生模式下仍然要满足：

- 明确 owner
- 明确 allowed / forbidden scope
- 明确 input / output path
- 明确 acceptance
- 明确 blocked_by

不要因为是原生 agent 就放弃这些约束。

## Step 5: 执行 Artifact-Orchestrated Swarm

这是默认现实路径。

做法：

1. 主控负责 preflight、registry、整体验收。
2. 每个子任务都写成独立 prompt。
3. 每个子任务都用独立输出文件落盘。
4. 需要时用 `codex exec` 启动子运行。
5. 子运行完成后，主控更新 `task-registry.md` 与 `protocol-audit.md`。

子运行 prompt 必须写清楚：

- task id
- precise objective
- allowed scope
- forbidden scope
- input path
- output path
- acceptance

建议把 prompt 文件放进：

- `prompts/`

把结果放进：

- `outputs/`

把日志放进：

- `logs/`

不要直接手写长 `codex exec` 命令并赌 PowerShell 引号不会炸。优先执行内置脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "C:/Users/feian/.codex/skills/codex-agent-swarm/scripts/run_codex_swarm_task.py" `
  -ScriptArgs @(
    "--run-root",".workspace/codex-swarm/runs/<run_id>",
    "--prompt-file",".workspace/codex-swarm/runs/<run_id>/prompts/task-a.md",
    "--output-file",".workspace/codex-swarm/runs/<run_id>/outputs/task-a.md",
    "--sandbox","workspace-write"
  )
```

如果必须手写命令，再用 `stdin` 喂 prompt，不要把整段 prompt 直接塞进 PowerShell 参数。

```powershell
cmd /c "type .workspace\codex-swarm\runs\<run_id>\prompts\task-a.md | codex exec --skip-git-repo-check -C . --output-last-message .workspace\codex-swarm\runs\<run_id>\outputs\task-a.md -"
```

脚本等价做法会更稳，因为它直接通过 `stdin` 传 prompt，并能同时写日志。

如果需要事件流证据，在脚本里加 `--json-log-file`，而不是手工拼接 stdout 重定向。

## Step 6: 维护 Registry 和 Audit

执行期间持续维护：

- `task-registry.md`
- `protocol-audit.md`
- `team-report.md`

`task-registry.md` 需要至少反映：

- 任务状态
- 阻塞关系
- 输入输出边界
- 验收条件
- 为什么值得独立 agent

`protocol-audit.md` 需要至少反映：

- 选择了哪种模式
- native 能力证据是什么
- 是否使用了 child `codex exec`
- 有哪些偏差或降级
- 最终是否闭环

## Step 7: 做回归

完成后先跑本 skill 自带校验：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "C:/Users/feian/.codex/skills/codex-agent-swarm/scripts/check_codex_swarm_run.py" `
  -ScriptArgs @("--run-root",".workspace/codex-swarm/runs/<run_id>")
```

再按需要做真实 smoke：

```powershell
cmd /c "type .workspace\codex-swarm\runs\<run_id>\prompts\smoke.md | codex exec --skip-git-repo-check -C . -"
```

如果用户要更强验证，实际让 skill 生成 artifacts，再检查 `task-registry.md` 是否仍有 `pending`，以及 `acceptance` / `spawn_reason` 是否缺失。

## 输出要求

最终回答至少要说清楚：

1. 选择了哪种模式。
2. 为什么不是其他模式。
3. `run_root` 是什么。
4. 生成了哪些 artifacts。
5. 是否真的使用了 native multi-agent，还是 child `codex exec`。
6. 哪些任务被 spawn，哪些没有，以及原因。
7. 当前闭环是否完整，还有什么缺口。

## 资源

- `references/decision-matrix.md`
  - 需要判断模式、spawn worthiness 时读取。
- `references/multi-agent-hardening.md`
  - 需要写子运行 prompt、控制边界、避免假并行时读取。
- `references/codex-runtime-notes.md`
  - 需要了解当前本机对 `multi_agent` 的已知边界时读取。
- `scripts/init_codex_swarm_run.py`
  - 需要快速初始化标准 run 目录时执行。
- `scripts/probe_codex_swarm_runtime.py`
  - 需要把 `features.multi_agent` 与 CLI 证据落盘时执行。
- `scripts/run_codex_swarm_task.py`
  - 需要稳定启动 child `codex exec`、避免 PowerShell 引号问题时执行。
- `scripts/check_codex_swarm_run.py`
  - 需要回归检查 artifacts 完整性时执行。
