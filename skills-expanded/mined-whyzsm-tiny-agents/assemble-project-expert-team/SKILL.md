---
name: assemble-project-expert-team
description: "项目专家团编排器。用于优先读取目标项目和本机已有 Skill/Agent，必要时读取远端专家团索引、SkillHub 和 find-skills，根据目标项目和任务要求动态选择最小充分的专家团，覆盖需求澄清、架构、实现、测试、调试、审查、发布和质量验证。 Project expert-team assembler. Use it to inspect project and installed capabilities first, then fill gaps from the remote expert-team catalog, SkillHub, and find-skills while selecting the smallest sufficient team for requirements clarification, architecture, implementation, testing, debugging, review, release, and quality verification."
metadata:
  source: "https://github.com/whyzsm/tiny-agents/tree/main/indexes"
  catalog: "expert-team-file-list.md"
  team_type: "dynamic-router"
---

# 根据现有的技能（skill）手搓专家团 / Assemble an Expert Team from Existing Skills

Use this skill as the dynamic expert-team entry point for project work. 使用本 Skill 作为项目工作的动态专家团入口。

It inspects the target repository and installed capabilities first, then reads the remote expert-team catalog, SkillHub, or find-skills only to fill verified capability gaps. 它先检查目标代码仓库和本机已有能力，只有能力不足时才读取远端专家团目录、SkillHub 或 find-skills，并且只纳入通过校验的能力；它按能力组合小型专家团，而不是使用固定人格包。

## 工作流 / Workflow

1. Read `references/guide.md` to separate the target project from the remote capability catalog and classify the delivery mode. 读取 `references/guide.md`，区分目标项目与远端能力目录，并判断交付模式。
2. Run `scripts/compose_team.py` from this skill directory to scan the target project and generate the roster, member prompts, phase DAG, and prerequisites. 从本 Skill 目录运行 `scripts/compose_team.py`，扫描目标项目并生成成员清单、成员 Prompt、阶段 DAG 和前置条件。
3. Read shortlisted router and child `SKILL.md` files before dispatching members; read only selected sources and never install them into the target project. 调度成员前完整读取入选入口和子 `SKILL.md`；只读取选中源，不把 Skill 安装到目标项目。
4. Follow `references/runtime-orchestration.md` for automatic team creation, phase dispatch, lead handoff, and the Codex fallback. 按 `references/runtime-orchestration.md` 执行自动建团、阶段调度、主理人中转和 Codex 兼容回退。
5. Follow `references/workflow.md` to coordinate execution or generate a reusable team package. 按 `references/workflow.md` 协调执行或生成可复用团队包。
6. Return the roster, phase dependencies, handoff contracts, exclusions, verification evidence, and remaining gaps. 返回成员清单、阶段依赖、交接契约、排除项、验证证据和剩余缺口。

## 自动组团 / Automatic Team Assembly

The default for requests to build, test, fix, review, or deliver is `auto-execute`: scan the project, compose the smallest sufficient team, dispatch independent members by phase, and integrate their reports. 用户要求实现、测试、修复、审查或交付时，默认使用 `auto-execute`：扫描项目、自动组建最小充分专家团、按阶段调度独立成员并集成报告。

Run the deterministic composer before making a manual roster:
先运行确定性编排脚本，再手工决定成员：

```bash
python3 <assemble-project-expert-team-dir>/scripts/compose_team.py \
  --project-root <target-project> \
  --task "<user request, risks, and deliverable>" \
  --mode auto-execute \
  --format json
```

The JSON is the dispatch contract. Each roster item contains an exact Skill source, one owned output, selection evidence, verification status, and a ready-to-send member prompt. JSON 是调度契约；每个成员包含准确 Skill 来源、一个负责产出、选择证据、校验状态和可直接发送的成员 Prompt。

## 本地优先 / Local-First Routing

Select sources in this order: qualified expert teams already in the target repository; target-repository Skills or Agents; locally installed Skills and Agents from `$CODEX_HOME/skills`, `~/.agents/skills`, and their Agent roots; verified remote `expert-team-file-list.md` entries; verified SkillHub packages; then verified `find-skills` GitHub sources. 按以下顺序选择来源：目标仓库中已符合条件的专家团；目标仓库已有 Skill 或 Agent；`$CODEX_HOME/skills`、`~/.agents/skills` 及其 Agent 目录中的本机能力；已校验的远端 `expert-team-file-list.md`；已校验的 SkillHub 包；最后是已校验的 `find-skills` GitHub 源。

The composer marks every member with `project-expert-team`, `project-skill`, `project-agent`, `installed-skill`, `installed-agent`, `catalog-local`, `remote-catalog`, `skillhub`, or `find-skills`. 编排器会用 `source_kind` 标记成员来自仓库专家团、仓库 Skill/Agent、本机安装能力、专家团目录、SkillHub 还是 find-skills。

Only use a remote expert-team entry directly when its router and selected child `SKILL.md` files are reachable and have matching frontmatter names. SkillHub candidates must contain a readable matching `SKILL.md` inside the downloaded package. `find-skills` candidates must resolve to a readable matching GitHub `SKILL.md`. Broken or unverified sources are candidate gaps, not usable team members. 只有远端专家团入口及选中的子 `SKILL.md` 均可访问且 frontmatter 名称匹配时，才可直接使用；SkillHub 候选必须能从包内读取名称匹配的 `SKILL.md`，find-skills 候选必须能解析到可读取且名称匹配的 GitHub `SKILL.md`；损坏或未校验的来源只是候选缺口，不是可用成员。

Use `--skill-root` or `--agent-root` to add an explicit local installation path, and `--no-local` only for testing remote-only routing. 使用 `--skill-root` 或 `--agent-root` 添加明确的本机路径；只有测试纯远端路由时才使用 `--no-local`。

Use `--mode blueprint` only when the user explicitly asks for planning only, simulation, or no execution. 用户明确要求“只规划”“模拟”或“不执行”时，才使用 `--mode blueprint`。

Do not generate avatar assets for dynamic teams or draft packages. 动态专家团和草稿团队包均不生成头像资源。

## 能力来源 / Source Capability Modules

- `requirements-analysis` — clarify goals, scope, stakeholders, and acceptance criteria. 澄清目标、范围、利益相关者和验收标准。
- `test-patterns` — unit, integration, mocking, coverage, and test-runner workflows. 提供单元测试、集成测试、Mock、覆盖率和测试运行器流程。
- `e2e-testing-patterns` — browser journeys, stable selectors, network isolation, and flaky-test control. 提供浏览器流程、稳定选择器、网络隔离和不稳定测试治理。
- `qa-api-tester` — HTTP contract checks, response validation, auth cases, and executable API test plans. 提供 HTTP 契约检查、响应校验、认证场景和可执行 API 测试计划。
- `find-skills` — discover standalone Skills from the skills.sh ecosystem when indexed and local sources leave a gap; discovery does not install. 当索引和本地来源仍有缺口时，从 skills.sh 生态查找独立 Skill；只查找，不安装。
- `https://skillhub.cn/` — search SkillHub metadata and verify a selected package's `SKILL.md`; package discovery does not install. 查询 SkillHub 元数据并校验选中包内的 `SKILL.md`；只查找和校验，不安装。

These are bootstrap capabilities for common requests, not a fixed roster. 这些是常见请求的启动能力，不是固定成员名单。

Select only the indexed capabilities required by the target task. 只选择目标任务实际需要、且已登记在索引中的能力。

## 输出 / Output

Produce only the deliverables required by the request. 只产出请求所需的交付物。

A blueprint contains the objective, roster, phased workflow, input/output dependencies, exclusions, assumptions, and verification gates. 蓝图包含目标、成员、分阶段流程、输入输出依赖、排除项、假设和验证门。

An execution result additionally contains changed artifacts, commands, evidence, and residual risks. 执行结果还要包含变更产物、执行命令、证据和残余风险。

A reusable package must follow `references/team-package-spec.md`. 可复用团队包必须遵循 `references/team-package-spec.md`。
