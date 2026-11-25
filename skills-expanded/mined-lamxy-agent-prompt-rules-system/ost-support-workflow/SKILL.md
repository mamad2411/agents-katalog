---
name: ost-support-workflow
description: Use when creating or updating an open_supports support package end-to-end, especially when coordinating repo summary, install script, setup skill, clarification, resume, or optional install verification.
argument-hint: 'GitHub owner/repo, e.g. colbymchenry/codegraph'
---

# open_supports 支持包工作流

## When to Use

- 为 `open_supports/` 新增一个开源库支持包
- 更新已有支持包的摘要、安装脚本或安装 Skill
- 从 `.ost-workflow-state/` 恢复中断的支持包工作流

## Pre-read

主 workflow 执行前只允许预读 workflow-level 轻量材料：

1. `open_supports/README.md`
2. 目标状态文件 `open_supports/.ost-workflow-state/{OwnerName}_{RepoName}.json`（如存在）
3. 目标支持包目录和 `.ost-refs/` 的文件列表；只在判断恢复、存在性或短本地约定时读取必要短内容
4. 本 workflow 自身的状态脚本用法：`open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh --help`

主 workflow 不得预读：

- `open_supports/README-workflow-quickstart.md` 等设计/教程文档
- 任何阶段 Skill 全文，例如 `.copilot-skills/ost-repo-readme-summary/SKILL.md`
- 官方 README、官方文档长文、npm package metadata、API 文档长文
- 阶段产物草稿的完整内容，除非用于最终轻量审查

阶段 Skill 只在派发给该阶段子代理的 prompt contract 中引用。主 workflow 不得为了“熟悉阶段要求”提前读取所有阶段 Skill。

## External Skill Interference

本任务显式指定 `ost-support-workflow` 时，它是主流程。 workflow 主代理严禁主动执行 `superpowers:using-superpowers skill` 或其他外部流程 Skill 来扩大预读范围、替子代理读取阶段材料，或改变本 workflow 的状态/派发纪律。

If this workflow is explicitly selected, the workflow agent must not use external process skills such as `superpowers:using-superpowers skill` to expand pre-read scope, preload stage materials, or bypass this workflow's dispatch and state rules.

子代理在各自环境中遵循其可见规则，但主 workflow 不得因此替子代理预读阶段 Skill、官方文档或长上下文。

## Subagent Tool Discovery

三个核心阶段和用户同意后的 `optional_usage_examples` 必须优先由子代理串行执行。

开始派发前，主 workflow 必须确认子代理能力：

1. 如果当前可见工具列表中已经有可用的子代理 / multi-agent / spawn-agent 工具，使用该工具串行派发阶段。
2. 如果当前工具列表没有可见子代理工具，必须先通过 `tool_search` 搜索 `multi-agent`、`subagent` 或 `spawn agent` 能力。
3. 如果搜索到可用工具，必须使用它串行派发阶段；generic subagent 可作为 workaround，但状态摘要必须注明 `generic-agent workaround`。
4. 只有在工具不存在、`tool_search` 确认不可用、工具 schema 不满足最低调度要求、用户明确要求不用子代理，或子代理连续失败后用户明确同意 inline 接管时，才允许 inline fallback。
5. fallback 原因必须具体写入状态，不能写成泛泛的 `tool unavailable`。

## GitHub Source Policy

阶段子代理获取 GitHub 仓库事实、README、目录、release、issue、PR 或文件内容时，必须遵循以下来源优先级：

1. 本地支持包文件和 `.ost-refs/`
2. GitHub connector / GitHub app tools
3. `gh` CLI 或 GitHub 官方 API
4. 官方文档网站
5. `curl` / raw GitHub URL，仅作为记录原因的 fallback

`curl` 不是禁止项：官方安装文档明确给出的 `curl | sh`、release asset 下载、验证本地 HTTP 服务，或 GitHub connector / `gh` / 官方 API 不可用且需要降级时可以使用。除官方安装命令本身外，使用 `curl` 获取 GitHub 信息必须在阶段结果的 `fallbacks` 中说明原因。

主 workflow 不得为了审计来源而预读官方 README 或长文档。主 workflow 只把本 policy 放入 dispatch contract，并检查阶段子代理返回的 `sources_used` / `fallbacks` 摘要是否存在且合理。

## Workflow

按顺序执行五个阶段：

1. `repo_readme_summary`：串行派发阶段子代理，在 contract 中引用 `.copilot-skills/ost-repo-readme-summary/SKILL.md`，产出 `repo_readme_summary.md`
2. `install_script`：先从 Part 2 读取 A/B/C/D 安装作用域契约并写入状态，再串行派发阶段子代理，在 contract 中引用 `.copilot-skills/ost-install-script/SKILL.md`，产出 `scripts_for_install/install.*`
3. `skill_for_setup`：串行派发阶段子代理，在 contract 中引用 `.copilot-skills/ost-skill-for-setup/SKILL.md`，产出 `skill_for_setup/README.md` 和 `skill_for_setup/ost_*_install/SKILL.md`
4. `optional_usage_examples`：按 checklist 判断是否建议生成；用户同意后串行派发阶段子代理，在 contract 中引用 `.copilot-skills/ost-usage-examples/SKILL.md`，产出 `usage_examples.md`
5. `optional_test_install`：询问用户是否测试运行安装脚本并验证安装成功

不要假设客户端支持嵌套调用 Skill；本 Skill 的职责是编排、状态管理、澄清和恢复。阶段细节以对应阶段 Skill 为准。

三个核心产出阶段和可选 `optional_usage_examples` 阶段默认使用子代理执行，但必须串行执行，不能并行。`optional_test_install` 默认由主 workflow 控制，因为它可能真实修改本机 CLI / Agent 配置。

## Stage Subagents

主 workflow 是唯一状态管理者和唯一用户交互者。阶段子代理只执行一个阶段，不直接询问用户，不直接写 `.ost-workflow-state/*.json`。

派发阶段子代理前：

1. 使用状态脚本将阶段设为 `in_progress`
2. 构造并持久化 dispatch contract 摘要
3. 给子代理提供目标阶段、目标支持包目录、对应阶段 Skill 路径、必要的上一阶段产物路径、已有用户澄清答案
4. 明确要求子代理只返回结构化结果

最小 dispatch contract：

```json
{
  "stage": "install_script",
  "package_dir": "open_supports/ost_owner_repo",
  "stage_skill_path": "open_supports/.copilot-skills/ost-install-script/SKILL.md",
  "required_inputs": [
    "repo_readme_summary.md（包含安装作用域契约：分类、官方默认、目标目录机制、证据）"
  ],
  "installation_scope_contract": {
    "classification": "A | B | C | D",
    "official_default": "以官方命令为准",
    "target_directory_requirement": "无 / CWD 敏感 / 原生路径参数",
    "execution_mechanism": "direct / subshell_cd / native_path_flag",
    "evidence": ["官方一手文档 URL"]
  },
  "clarification_answers": [],
  "allowed_outputs": [
    "DONE",
    "NEEDS_CLARIFICATION",
    "FAILED"
  ],
  "tool_policy": {
    "github_source_priority": [
      "local package files and .ost-refs",
      "GitHub connector / GitHub app tools",
      "gh CLI or GitHub official API",
      "official documentation website",
      "curl/raw GitHub URLs only as recorded fallback"
    ],
    "curl_boundary": "Allowed for official install commands and explicit fallback only; not the default for repository fact gathering.",
    "fallback_reporting": "Return sources_used and fallbacks when lower-priority tools are used."
  },
  "context_hygiene": {
    "do_not_return": [
      "long official docs excerpts",
      "full README",
      "full generated files",
      "step-by-step private reasoning"
    ]
  }
}
```

派发前用状态脚本保存可审计 contract 摘要：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh contract OWNER/REPO install_script open_supports/ost_owner_repo open_supports/.copilot-skills/ost-install-script/SKILL.md repo_readme_summary.md DONE,NEEDS_CLARIFICATION,FAILED
```

在 `repo_readme_summary` 完成、`install_script` 开始前，主 workflow 必须读取 Part 2 的安装作用域表。若无法提取完整契约，标记当前阶段 `blocked` 并只向用户询问缺失事实；不得派发脚本阶段。可提取时，先写入状态再派发：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh scope-contract OWNER/REPO D global "仅 --local 时需要明确项目目录" subshell_cd "https://官方文档.example/install"
```

参数含义必须对应摘要中的真实事实：`CLASSIFICATION` 仅为 `A`、`B`、`C`、`D`；`OFFICIAL_DEFAULT` 不得由 workflow 猜测。阶段 dispatch contract 也必须携带同一份值。`skill_for_setup` 与 `optional_usage_examples` 的 contract 必须引用该已记录的契约，作为一致性输入。

阶段子代理只能返回：

- `DONE`
- `NEEDS_CLARIFICATION`
- `FAILED`

收到 `DONE`：主 workflow 审查产物路径，使用状态脚本记录 `agent-run ... DONE ...`，再将阶段设为 `done`。

收到 `NEEDS_CLARIFICATION`：主 workflow 使用状态脚本记录 `agent-run ... NEEDS_CLARIFICATION ...`，再用 `block ...` 写入阻塞问题，然后只向用户提出该问题。

收到 `FAILED`：主 workflow 使用状态脚本记录 `agent-run ... FAILED ...`，将阶段标记为 `failed`，再询问用户下一步。

`optional_usage_examples` 被用户同意后，按普通阶段子代理处理；用户拒绝或 checklist 未命中时不派发子代理，直接标记为 `skipped`。

如果允许 inline fallback，不能使用 `agent-run` 伪装成子代理结果；必须使用：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh inline-run OWNER/REPO STAGE STATUS SUMMARY "specific fallback reason"
```

最终报告必须说明是否使用过 fallback，以及每次 fallback 的具体原因。

## Context Hygiene

主 workflow 必须尽可能保持上下文干净、节省。阶段子代理用于隔离重上下文，避免把官方 README、长文档、详细推理过程或完整中间草稿回灌给主 workflow。

阶段子代理只返回满足编排所需的最小关键信息：

- `status`: `DONE`、`NEEDS_CLARIFICATION` 或 `FAILED`
- `stage`: 当前阶段名
- `summary`: 1-3 条结果摘要
- `files_changed`: 产物文件路径列表
- `verification`: 已执行的轻量检查及结果
- `sources_used`: 来源类别和关键路径摘要，例如 `github_connector: fetch_file owner/repo README.md` 或 `local: open_supports/ost_owner_repo/.ost-refs/install.md`
- `fallbacks`: 降级或保留 direct HTTP 的原因摘要；没有降级时返回空数组
- `clarification`: 仅当 `NEEDS_CLARIFICATION` 时返回，包含 `reason`、`question`、`suggested_default`
- `failure`: 仅当 `FAILED` 时返回，包含失败命令、退出码和关键输出摘要

阶段子代理不要返回：

- 大段官方文档摘录
- 完整 README 或完整安装文档
- 详细逐步推理过程
- 与当前阶段无关的发现
- 可从产物文件直接读取的完整内容

主 workflow 若需要审查产物，应读取目标文件本身，而不是要求子代理复制文件内容。状态文件只保存恢复和决策所需信息，不保存长文档或冗余中间过程。

## State Management

状态目录：

```text
open_supports/.ost-workflow-state/
```

状态文件：

```text
open_supports/.ost-workflow-state/{OwnerName}_{RepoName}.json
```

状态 JSON 包含阶段状态和可选用法示例决策，例如：

```json
{
  "stages": {
    "repo_readme_summary": "pending",
    "install_script": "pending",
    "skill_for_setup": "pending",
    "optional_usage_examples": "pending",
    "optional_test_install": "pending"
  },
  "usage_examples": {
    "offered": false,
    "decision": "pending",
    "matched_criteria": [],
    "result": null
  },
  "installation_scope": {
    "classification": null,
    "official_default": null,
    "target_directory_requirement": null,
    "execution_mechanism": null,
    "evidence": []
  },
  "execution": {
    "mode": "subagent_preferred",
    "fallback": "inline",
    "current_agent_stage": null,
    "dispatch_contracts": [],
    "agent_runs": [],
    "inline_runs": []
  }
}
```

状态 JSON 默认不提交 Git。恢复工作流时，先读取对应状态文件：

- 若存在 `blocked` 或 `waiting_user`，先复述当前断点和唯一待回答问题
- 用户回答后，把回答写入状态，再回到下一阶段检测
- 若不存在状态文件，创建新状态并从 `PreparePackage` 开始

状态读写必须优先通过内部脚本完成：

```text
open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh
```

该脚本使用 `sh + jq`，只负责 JSON 状态机械读写，不负责 workflow 决策。只有主 workflow 可以调用该脚本；阶段子代理不能直接调用。

所有 `state.sh` 写操作必须串行执行。主 workflow 不得用 `multi_tool_use.parallel` 或其他并行机制同时调用 `set-stage`、`contract`、`agent-run`、`inline-run`、`usage-examples`、`test-result`、`complete` 等写命令。每次写入后，如阶段推进或恢复依赖状态文件，先确认状态 JSON 仍可被 `jq` 解析。

常用命令：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh init OWNER/REPO
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh show OWNER/REPO
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh set-stage OWNER/REPO STAGE STATUS
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh block OWNER/REPO STAGE REASON QUESTION [SUGGESTED_DEFAULT]
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh answer OWNER/REPO ANSWER
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh scope-contract OWNER/REPO CLASSIFICATION OFFICIAL_DEFAULT TARGET_DIRECTORY_REQUIREMENT EXECUTION_MECHANISM EVIDENCE
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh contract OWNER/REPO STAGE PACKAGE_DIR STAGE_SKILL_PATH REQUIRED_INPUTS ALLOWED_OUTPUTS
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh agent-run OWNER/REPO STAGE STATUS SUMMARY
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh inline-run OWNER/REPO STAGE STATUS SUMMARY FALLBACK_REASON
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh offer-usage-examples OWNER/REPO MATCHED_CRITERIA
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh usage-examples OWNER/REPO DECISION MATCHED_CRITERIA [RESULT]
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh test-result OWNER/REPO RESULT COMMAND EXIT_CODE SUMMARY
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh complete OWNER/REPO
```

`RESULT` 可省略；省略时 `accepted` 默认 `pending`，`declined` / `not_applicable` 默认 `skipped`。

阶段状态只使用：

```text
pending
in_progress
done
blocked
waiting_user
skipped
failed
```

## Package Preparation

目标支持包目录不存在时，可以自动创建最小目录结构：

```text
ost_{OwnerName}_{RepoName}/
ost_{OwnerName}_{RepoName}/scripts_for_install/
ost_{OwnerName}_{RepoName}/skill_for_setup/
ost_{OwnerName}_{RepoName}/skill_for_setup/ost_{OwnerName}_{RepoName}_install/
```

可以创建缺失目录，但不要自动覆盖已有文件。目标产物已存在时，进入对应阶段的更新或确认逻辑。

## Clarification / Blocking

任何阶段遇到关键行为无法从官方文档、现有支持包文件或 `.ost-refs/` 可靠判断时：

1. 不要猜测关键行为
2. 将当前阶段标记为 `blocked`
3. 记录一个澄清项：
   - `stage`
   - `reason`
   - `question`
   - `suggested_default`（如有）
4. 将 `workflow_status` 标记为 `blocked`
5. 向用户提出这个问题，等待回答

最小恢复策略：只处理当前唯一 open clarification，不维护多问题队列。

## Optional Usage Examples

三个核心产出阶段完成后，先按以下 checklist 判断是否建议生成 `usage_examples.md`：

- 官方文档包含 CLI 或可执行命令示例
- 官方文档包含项目初始化流程
- 支持包涉及配置文件或状态目录
- 支持包涉及 Agent、MCP、IDE、Copilot、Claude 或 Codex 接入
- 安装后存在常见工作流或后续操作
- 官方文档提供多个用法场景
- `.ost-refs/` 中存在本地约定、项目约定或推荐实践

命中 2 项或以上才询问用户是否生成用法示例。未命中时：

- 将 `optional_usage_examples` 标记为 `skipped`
- 将 `usage_examples.decision` 记为 `not_applicable`
- 将 `usage_examples.offered` 记为 `false`
- 将 `usage_examples.matched_criteria` 记为 `[]`
- 将 `usage_examples.result` 记为 `skipped`
- 继续进入 `optional_test_install`

命中 2 项或以上时，询问用户：

提问前必须先持久化等待决策状态：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh offer-usage-examples OWNER/REPO "CLI, Agent integration"
```

这会记录 `usage_examples.offered = true`、`usage_examples.decision = "pending"`、命中的 `usage_examples.matched_criteria`、`usage_examples.result = "pending"`，并将 `optional_usage_examples` 标记为 `waiting_user`、`workflow_status` 标记为 `blocked`，以便断点恢复。

```text
检测到该支持包适合生成 usage_examples.md，命中原因：
- CLI, Agent integration

是否要派发 ost-usage-examples 阶段子代理生成安装后的用法示例？这不影响核心支持包完成。
回复“是”则生成，回复“否”则跳过并继续 optional_test_install。
```

主 workflow 在 checklist 判断或用户回答后，必须使用状态脚本记录 `usage_examples.decision`、`usage_examples.matched_criteria` 和 `usage_examples.result`：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh usage-examples OWNER/REPO DECISION MATCHED_CRITERIA [RESULT]
```

`MATCHED_CRITERIA` 是 checklist 命中摘要字串，状态中以单元素数组保存；不要求 shell 解析多值列表。

用户拒绝：

- 将 `optional_usage_examples` 标记为 `skipped`
- 将 `usage_examples.offered` 记为 `true`
- 将 `usage_examples.decision` 记为 `declined`
- 可保存传入的 checklist 命中摘要到 `usage_examples.matched_criteria`
- 将 `usage_examples.result` 记为 `skipped`
- 继续进入 `optional_test_install`

用户同意：

- 将 `usage_examples.offered` 记为 `true`，记录命中的 `usage_examples.matched_criteria`
- 将 `usage_examples.decision` 记为 `accepted`
- 先将 `usage_examples.result` 记为 `pending`
- 将 `optional_usage_examples` 标记为 `in_progress`
- 串行派发阶段子代理，在 contract 中引用 `.copilot-skills/ost-usage-examples/SKILL.md`
- 子代理产出 `usage_examples.md`
- 主 workflow 审查产物后，记录 `agent-run ... DONE ...`，再使用状态脚本将 `usage_examples.result` 记为 `generated`，并将 `optional_usage_examples` 标记为 `done`

推荐调用顺序：

```sh
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh offer-usage-examples OWNER/REPO "CLI, Agent integration"
# 用户同意后：
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh usage-examples OWNER/REPO accepted "CLI, Agent integration" pending
# 子代理 DONE 且主 workflow 审查 usage_examples.md 后：
sh open_supports/.copilot-skills/ost-support-workflow/scripts/state.sh usage-examples OWNER/REPO accepted "CLI, Agent integration" generated
```

## Optional Test Install

三个核心产出阶段和 `optional_usage_examples` 完成或跳过后，必须询问用户：

```text
是否要测试运行 scripts_for_install/install.* 并验证安装是否成功？
这可能会修改本机 CLI / Agent 配置。回复“是”则执行，回复“否”则跳过并完成工作流。
```

用户拒绝：

- 将 `optional_test_install` 标记为 `skipped`
- 将 `test_install.offered` 记为 `true`
- 将 `test_install.decision` 记为 `declined`
- 将 `test_install.result` 记为 `skipped`
- 使用 `test-result OWNER/REPO skipped ...` 记录拒绝测试；`workflow_status` 保持 `in_progress`
- 之后由 `complete OWNER/REPO` 统一验证并完成工作流

用户同意：

- 将 `optional_test_install` 标记为 `in_progress`
- 只在隔离 Docker 容器中运行安装脚本和验证命令；将测试项目目录挂载为容器内临时路径。不得在宿主机真实 CLI、用户配置目录或真实项目中安装／配置，即使脚本默认全局模式也不例外。
- 运行验证命令
- 记录执行命令、结果和关键输出摘要

验证命令优先来自 `repo_readme_summary.md` 第 2 部分，其次来自安装脚本或 setup Skill；仍不能判断时进入澄清。

## Test Failure

测试安装失败后不要自动修复。保存失败状态并暂停：

- `optional_test_install` 标记为 `failed`
- `workflow_status` 标记为 `blocked`
- 记录失败命令、退出码和关键输出摘要
- 询问用户下一步：修复支持包文件、跳过测试并完成，或停在失败状态稍后恢复

## Completion

完成时确认：

- 必须调用 `complete OWNER/REPO`
- `complete` 会验证 `repo_readme_summary`、`install_script`、`skill_for_setup` 都为 `done`
- `complete` 会验证 `optional_usage_examples` 为 `done` 或 `skipped`；legacy state 缺少该 stage 时会补为 `skipped`
- `complete` 会验证 `optional_test_install` 为 `skipped`，或 `test_install.result` 为 `passed` 且 stage 状态为 `done`
- `workflow_status` 为 `done`
- `installation_scope` 已包含 A/B/C/D 分类、官方默认、目标目录机制和至少一条官方证据
- 摘要 Part 2、脚本 `--help`、setup Skill、以及存在时的 usage examples 对该契约一致；B 使用子 shell CWD，C 使用原生路径参数，D 保留官方默认
- 已在 `open_supports/INDEX.md` 的「已收录支持包」与「安装命令速查」两张表各追加一行，分类首字母与摘要一致；在仓库根目录运行 `sh scripts/tests/test-open-supports-index.sh` 通过
