---
name: codex-subagents-kit
description: Codex 专用多智能体 / 子智能体编排工作台。用于判断任务是否应保持单控制器，或升级为 manager-with-specialists、generator-verifier、research-swarm、Codex Subagents、`.codex/agents/`、`AGENTS.md`、`skills.config`、artifact-backed execution path。适用于需要控制上下文污染、选择协作拓扑、并用 runtime probe / audit / scorecard 验证方案的场景。
---

# Codex Subagents Kit

把这个 skill 当成 **Codex-only orchestration guide**：

- 优先对齐 **Codex Subagents / `.codex/agents/` / `skills.config`**
- 吸收最新 Anthropic / OpenAI / Codex 官方方法论：**single-controller first、context-centric decomposition、ownership-first routing、summary-only returns**
- 控制上下文体积，避免把长说明塞进主对话
- 用可验证 artifacts、脚本和 scorecard 构成闭环
- 对 native child-agent 能力保持诚实；证据不足时改走 artifact 路径

## Core rules

1. 先做 preflight，再决定是否并行。
2. 默认先尝试 **single-controller / one-agent-with-tools**；只有在 **context protection、parallel exploration、specialization** 其中至少一项明显成立时才升级。
3. 先决定 **ownership**，再决定 topology：谁保留最终综合权，谁只做 sidecar，谁只做 verifier。
4. 区分 **产品支持**、**会话证据**、**策略许可**、**任务适配** 四层事实。
5. 只把独立、边界清晰、验收明确、返回可摘要的任务交给子 agent。
6. 分工优先按 **上下文边界** 拆，不按岗位头衔机械拆。
7. 所有循环都必须有 **stop condition / time budget / fallback**。
8. 长计划、长结果、对比表优先落盘，不优先塞进聊天上下文；子 agent 默认只回传 **evidence-dense summary**。
9. 规则性动作优先脚本/CLI，不要把一切都做成 agent；工具、MCP、`AGENTS.md`、state 归属要写清。
10. **默认不要下调子 agent 模型档位**：除非用户明确要求省钱/提速，或任务是低风险、低复杂度 sidecar，否则不要显式把子 agent 改成更小模型。
11. **默认继承主控模型与思考强度**：调用 `spawn_agent` 时优先省略 `model` 与 `reasoning_effort`，让子 agent 继承当前主会话；只有在你能说明收益和风险时才覆盖。

## Default subagent model policy

- **默认策略**：子 agent 与主控保持同模型层级、同 reasoning effort。
- **推荐实现**：调用 `spawn_agent` 时不传 `model`、不传 `reasoning_effort`。
- **允许降级的场景**：
  1. 用户明确要求更便宜 / 更快
  2. 大规模并行探索，且每个子任务都很轻、验收清晰
  3. 低风险信息收集 sidecar，不阻塞关键路径
- **降级后的义务**：如果显式改用 mini / 更低 reasoning，必须在最终说明里写清楚“为什么降级、收益是什么、潜在损失是什么”。

## Minimal workflow

### 1) Preflight

先写清一版 **provisional preflight**：

- `final_goal`
- `deliverables`
- `constraints`
- `success_criteria`
- `spawn_candidates`
- `tasks_not_worth_spawning`

如果用户 prompt 已经隐含了这些信息，就直接提炼一版简洁 preflight，不要机械地回问字段名。  
只有当缺失信息会改变 **mode selection / acceptance / audit 结论** 时，才向用户追问。

复杂任务先初始化 run：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "<skill-root>/scripts/init_codex_swarm_run.py" `
  -ScriptArgs @("--workspace-root",".","--case","my-task")
```

最小 artifacts：

- `preflight.md`
- `agent-blueprints.md`
- `execution-plan.md`
- `task-registry.md`
- `protocol-audit.md`
- `team-report.md`
- `scorecard.md`

当 run 使用 `v2` 合同时，`task-registry.md` 还应补齐：

- `Stop Condition`
- `Escalation / Fallback`
- `Evidence Path`

### 2) Four gates

先判断四层门控：

1. **Product Gate**：Codex 产品层是否支持当前机制
2. **Session Gate**：当前 session 是否有 live native agent 工具证据
3. **Policy Gate**：当前任务/风险/用户要求是否允许真正 spawn
4. **Task Gate**：能否写出 owner / input / output / acceptance

如果需要完整判断规则，读：

- `references/selection-guide.md`

### 3) Decide whether multi-agent is warranted

先问：

- 单控制器 + tools 能否完成？
- 是否真的存在 `context protection / parallel exploration / specialization`？
- 子任务是否能只回传高信号摘要，而不是把原始噪音倒回主线程？

如果答案偏否，优先保持 `single-controller`。

### 4) Choose ownership and overlays

先决定谁保留最终综合权：

- `manager-with-specialists`
  - 主控保留最终 synthesis；specialist 只负责 sidecar / tool-like 工作
- `handoff-network`
  - 更适合外部 OpenAI Agents SDK / Responses runtime 方案蓝图；不要把它误称为当前 Codex session 的原生 handoff
- `generator-verifier`
  - 作为验证覆盖层附着在其他模式之上；只有 rubric 明确时才值得加
- `research-swarm / shared-findings`
  - 研究型任务专用；用共享 findings ledger + 角度去重 + 停止条件，而不是让所有 explorer 搜同一件事

如果需要跨官方资料对齐，读：

- `references/official-patterns-2026.md`
- `references/research-swarm-pattern.md`

### 5) Choose a Codex runtime mode

默认只在四层门控都通过时选 `native-subagents`。  
否则按任务目标选择：

- `single-controller`
- `config-guided-codex-subagents`
- `artifact-orchestrated-swarm`

工程快速路由提示（这是**基于官方原则落地到本 skill 的工程推断**，不是产品层硬保证）：

- 当 prompt 明确要求 `angle-map / shared-findings / dedupe / official-vs-inference / gap review` 这类研究交付物时，优先评估 `research-swarm`
- 当 prompt 明确要求 `.codex/agents / skills.config / team templates`，且 session 级 native 证据不确定时，优先评估 `manager-with-specialists + config-guided-codex-subagents`
- 当 prompt 明确要求 `run_root / per-task prompt-output / registry / protocol-audit / scorecard / replayable artifacts` 时，优先评估 `manager-with-specialists + artifact-orchestrated-swarm`
- 当任务只是**给出 routing / topology / mode 决策**，而不是要求你立刻实际启动 child agents 时，`manager-with-specialists` 默认优先落到 `config-guided-codex-subagents`；只有在 prompt 明确要求实际 live native delegation，或当前执行确实要马上使用子 agent 时，才优先写成 `native-subagents`

如果这些 lexical cues 与四层门控冲突，以门控诚实性优先；不要为了命中模式名而伪造 native 证据。

如果需要完整模式矩阵，读：

- `references/selection-guide.md`

### 6) Keep context small

默认只读：

- 当前 `SKILL.md`
- 与当前决策直接相关的少量 reference
- 必要入口文件

不要默认读完所有 references、logs、历史会话。

如果需要更细的 token 控制规则，读：

- `references/context-efficiency.md`

### 7) Use project agents when config-guided mode wins

当产品层支持，但当前 session 不适合直接 native spawn 时：

1. 优先在项目里维护 `.codex/agents/`
2. 保持 `AGENTS.md` 简短，只放高复用协作规则
3. 用 `skills.config` 精确指向 skill 路径
4. 用固定模板定义 explorer / worker / reviewer / verifier
5. 明确哪些规则应该进 `AGENTS.md`，哪些应该留在 task-specific prompt / MCP / runtime state 中

如果需要模板与复制规则，读：

- `references/project-agents.md`
- `assets/project-agents/*.toml`

### 8) Use artifact swarm when a stable artifact path is needed

当需要稳定降级路径时：

1. 每个子任务写独立 prompt
2. 每个子任务写独立 output file
3. 通过 `codex exec` 或现成脚本执行
4. 持续维护 registry / audit / scorecard
5. 对 research / review 类任务，优先让 child 输出结构化 findings，而不是长篇过程日志

执行子任务优先用：

- `scripts/run_codex_swarm_task.py`

如果需要 child prompt 合同、热文件规则、reviewer 分离规则，读：

- `references/multi-agent-hardening.md`
- `references/topology-catalog.md`
- `references/artifact-contract.md`

### 9) Probe and validate

需要 runtime 证据时执行：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "<skill-root>/scripts/probe_codex_swarm_runtime.py" `
  -ScriptArgs @("--run-root",".workspace/codex-swarm/runs/<run_id>","--workspace-root",".")
```

完成后先校验：

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/feian/.codex/tools/safe-run.ps1" `
  -ScriptPath "<skill-root>/scripts/check_codex_swarm_run.py" `
  -ScriptArgs @("--run-root",".workspace/codex-swarm/runs/<run_id>")
```

如果需要做真实 prompt 的 forward-test / regression，优先复用同一 `run_root`：

1. 保留 `runtime-probe.json`
2. 把 prompt、output、log 落到 run artifacts
3. 用 scorecard 区分 **官方方法论映射** 与 **工程闭环**
4. 只有在得分提高且无关键维度退化时，才把改动回写到 skill 本体

## Output contract

最终回答至少说明：

1. 是否真的值得多智能体；如果不值得，为什么保持单控制器
2. ownership shape / overlay 选择了什么
3. 四层门控的判断结果
4. 是否真的用了 native subagents / config-guided setup / artifact mode
5. `run_root` 和主要 artifacts
6. 哪些任务值得 spawn，哪些不值得
7. 哪些上下文被刻意不加载，以节省 token
8. `AGENTS.md` / tools / MCP / state / approvals 的边界决策
9. 停止条件、fallback、评估或 verifier 计划
10. 如果覆盖了子 agent 的 `model` 或 `reasoning_effort`，覆盖原因是什么

## Read-on-demand map

- `references/official-patterns-2026.md`
  - 需要对齐 Anthropic 五模式、OpenAI ownership/handoff、Codex subagents 最新官方方法论时读
- `references/selection-guide.md`
  - 需要判断“是否值得多智能体”、ownership shape、runtime 模式矩阵、并发预算时读
- `references/context-efficiency.md`
  - 需要控制 token / prompt 体积时读
- `references/project-agents.md`
  - 需要落地 `.codex/agents/` 模板时读
- `references/topology-catalog.md`
  - 需要选择研究/修复/审查队形时读
- `references/research-swarm-pattern.md`
  - 需要把资料研究任务拆成去重的 explorer 角度、共享 findings、收敛/停止条件时读
- `references/multi-agent-hardening.md`
  - 需要 prompt 合同、热文件规则、review 分离、summary-only return、stop condition 时读
- `references/artifact-contract.md`
  - 需要 artifacts / audit / scorecard 规范时读
- `references/scoring-rubric.md`
  - 需要把 OpenAI / Anthropic / Codex 方法论映射成 forward-test / regression 评分维度时读
- `references/codex-runtime-notes.md`
  - 需要本机 runtime 已知事实时读
