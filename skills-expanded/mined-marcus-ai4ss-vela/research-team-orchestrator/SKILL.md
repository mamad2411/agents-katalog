---

name: research-team-orchestrator

description: Use when a research task has entered project-type multi-agent planning and Codex must turn the selected route into a concrete clarification card, agent set, target-specific review mapping, dispatch artifact, and canonical project skeleton without breaking the V6.4 contract.

---



# Research Team Orchestrator



当研究任务已经被 `research-autopilot` 判定为项目型多 agent 路径时，使用这个 skill。



它不是新的总入口，也不替代 `research-autopilot`。

它只负责一件事：



把“已经选好的 route”变成一套可执行、可校验、可阻断的项目级多 agent 编排结果。



Runtime-stable IDs still use `agent_id`, but user-facing notes, dispatch metadata, and orchestration results should also include `display_name`, preferably in this form:


- `文献智能体（literature-producer）`

- `审稿智能体（reviewer）`



## Do Not Use



以下情况不要用这个 skill：



- 单篇论文审稿

- Python / Git / PowerShell / Codex 环境维护

- 长时实验运行监督

- 还没确定 route，只是泛泛讨论研究方向



这些任务分别仍由：



- `academic-paper-review`

- `vela-runtime-manager`

- `long-running-experiment-ops`

- `research-autopilot`



处理。



## Required References



执行前必须先读：



- `<VELA_RUNTIME_ROOT>\skills\catalog\project_scope_rules.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\research_team_playbooks.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\governance_kernel.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\agent_execution_modes.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\subagent_registry.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\reviewer_allowlist.json`

- `<VELA_RUNTIME_ROOT>\skills\schemas\agent_dispatch_card.schema.json`

- `<VELA_RUNTIME_ROOT>\skills\schemas\project_agent_definition.schema.json`

- `<VELA_RUNTIME_ROOT>\skills\scripts\validate_agents_contract.py`

- `<VELA_RUNTIME_ROOT>\skills\scripts\plan_research_team.py`

- `<VELA_RUNTIME_ROOT>\skills\scripts\bootstrap_agent_dispatch.py`



## Required Inputs



进入本 skill 前，至少要有这些输入：



- `project_root`

- `route_id`

- `project_type`

- `stage`

- `clarification_card`

- `explicit_project_mode`

- `deliverable_types`

- `route_confirmation_required`

- `route_confirmation_question`

- `user_confirmed_route`



如果这些字段不完整，就不能直接编排 dispatch；必须先补 clarification card。

如果 `route_confirmation_required = true` 但 `user_confirmed_route = false`，不得编排 dispatch；必须把 `route_confirmation_question` 返回给用户等待确认。



## Hard Rules



1. `force_single_agent` 只压缩 producer 数量，不取消 mandatory reviewer。

2. 命中必审子集的产物必须配置 target-specific reviewer。

3. reviewer 不能碰任何有持久副作用的能力。

4. dispatch 只能收缩权限，不能扩权。

5. 所有路径必须落在 canonical 目录中。

6. 每个 producer / reviewer 都必须拿到详细任务卡：任务目标、输入材料、禁止范围、允许工具、输出文件、迭代要求、验证方式、回报格式和失败上报规则。

7. 主 agent 只保留干净的项目主线和协调状态；大体量阅读、检索、盘点、对比、测试和初审应尽量交给独立子 agent 上下文。

8. 不得绕过这些硬链路：

   - `citation-verifier -> zotero-sync`

   - `writing-reference-capture`

   - `social-platform-reader`

   - `reproducibility-package`

   - `obsidian-research-sync`



## Execution Order



1. 读取当前 route、project scope class、clarification card 和 `research_team_playbooks.json` 中对应 route 的 squad。

2. 检查 clarification card 是否要求路线确认；如尚未确认，停止并询问用户。

3. 检查项目根目录下是否已有真实落盘的项目 contract：

   - `AGENTS.md`

   - `.codex/agents/*.json`

4. 如果缺少这些文件，先调用：

   - `python -m skills.scripts.envctl ensure-project-contract --path "<project_root>"`

5. 不要临时伪造 `AGENTS.md`、临时 agent JSON 或用 `audit/` 目录替代项目 contract。项目运行时必须有自己的真实项目级 contract；系统环境里的 contract 只作为模板源和校验源。

6. 读取项目级 `AGENTS.md` 和 `.codex/agents/*.json`。

7. 决定 producer 集合。

8. 决定每个 producer 是否需要 reviewer。

9. 决定 `review_agents[target_agent_id]` 映射。

10. 生成中文编排说明卡。

11. 优先调用本地编排脚本：

   - `plan_research_team.py`

12. 只有在脚本确认 route、producer、reviewer 和 review mapping 后，才进一步调用：

   - `bootstrap_agent_dispatch.py`

13. 确认每个 selected agent 都带有来自 `subagent_registry.json` 的 `control_bindings`。

14. 让脚本写出：

   - dispatch card

   - context packets

   - canonical output dirs

   - handoff / gate log 占位

   - project state board

15. 运行 contract validator 的 bootstrap 模式。

16. 只有校验通过，才把 dispatch artifact 当成有效结果。



## Default Agent Shapes



优先从项目级 `.codex/agents` 读取 agent 定义。



如果某个项目 agent 还没启用，先按 `skills/catalog/research_team_playbooks.json` 的 route playbook 选择默认队形：



- `default_agents` 是该 route 的最小 squad。

- `optional_agents` 只在 clarification card 的 work units、deliverable types 或 sync targets 命中时加入。

- `review_chain` 是 reviewer 映射的最低参考；命中必审产物时，仍以 mandatory review gate 为硬约束。



不要在没有理由的情况下把所有 producer 都塞进同一个 run。

如果一个 run 的 producer 太多，就先按阶段拆。



## Script



优先复用：



- `<VELA_RUNTIME_ROOT>\skills\scripts\plan_research_team.py`



- `<VELA_RUNTIME_ROOT>\skills\scripts\bootstrap_agent_dispatch.py`



示例：



```powershell

& "<VELA_RUNTIME_ROOT>\.venv\Scripts\python.exe" `

  "<VELA_RUNTIME_ROOT>\skills\scripts\plan_research_team.py" `

  --project-root "<USER_DESKTOP>\你的项目" `

  --route-id "literature-review" `

  --target-item-count 20 `

  --work-unit "discovery" `

  --work-unit "writing" `

  --deliverable-type "literature_synthesis" `

  --sync-target "zotero" `

  --sync-target "obsidian" `

  --bootstrap

```



`plan_research_team.py` 默认会自动补齐缺失的项目级 `AGENTS.md` 和 `.codex/agents/*.json`。只有用户明确要求不写项目 contract 时，才加 `--no-auto-init-project-contract`。



低层 bootstrap 示例：



```powershell

& "<VELA_RUNTIME_ROOT>\.venv\Scripts\python.exe" `

  "<VELA_RUNTIME_ROOT>\skills\scripts\bootstrap_agent_dispatch.py" `

  --project-root "<USER_DESKTOP>\你的项目" `

  --route-id "literature-review" `

  --project-type "literature-review" `

  --stage "planning" `

  --agent "literature-producer" `

  --agent "reviewer" `

  --review-pair "literature-producer:reviewer" `

  --deliverable-type "literature_synthesis"

```



## Output Contract



先输出中文编排说明卡，至少包含：



- `project_scope_class`

- `execution_mode`

- `selected producers`

- `selected reviewers`

- `每个 agent 的 display_name`

- `为什么这样拆`

- `使用了哪个 squad playbook`

- `为什么没选其他 agent`

- `哪些产物必须 review gate`

- `每个 selected agent 的 control_bindings`

- `dispatch artifact 会写到哪里`

- `project state board 会写到哪里`

- `每个 agent 的详细任务卡`

- `每个 agent 必须带回的报告字段`



然后输出结构化结果：



```markdown

# Research Team Orchestration



## Project Scope



## Clarification Card



## Selected Agents



## Review Mapping



## Dispatch Artifact



## Canonical Paths



## Validation Result



## Next Step

```



## Canonical Project State



除 dispatch、handoff 和 gate 之外，这个 skill 还应维护：



- `logs/project-state/current.json`

- `logs/project-state/history.md`



至少记录：



- 当前 owner agent

- 当前 pipeline stage

- 下一个 quality gate

- blockers

- 关键 milestones



## Failure Rules



遇到以下情况必须停止：



- `project_root` 不存在

- 自动补齐后仍缺少 `AGENTS.md`

- 自动补齐后仍缺少 `.codex/agents/*.json`

- `review_agents` 映射不合法

- producer 命中必审子集但没有 reviewer

- dispatch 超出 effective 权限

- bootstrap validator 不通过



阻塞时必须说明：



1. 缺了什么

2. 为什么这会破坏 contract

3. 最小修复动作是什么
