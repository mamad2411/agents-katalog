---
name: using-orbit
description: Use when a workflow request already matches an Orbit scenario such as Sprint readiness, tracker-driven implementation, PR review, security triage, pentest, delivery metrics, knowledge capture, or scheduled quality/security remediation to PRs, including trigger-only validations that must skip shell, host-resource discovery, and host-entry audits so they stay focused on missing business inputs.
metadata:
  author: Orbit contributors
  version: "1.0.17"
---

# Orbit

You have access to twelve DevOps scenario skills. When the user's request matches a scenario, route to the corresponding skill through the host's skill resolution mechanism before responding.

Trigger-only routing guard: if the user's wording already matches one scenario and the request is only a skill trigger test, treat that scenario as selected. Do not turn the turn into host-platform discovery, skill-name confirmation, trigger-entry auditing, or host-entry troubleshooting. Ask only for the missing business inputs required by the matched scenario.

In trigger-only validation, this skill contract is already the authority. Do not reopen this file, sibling references, or installed skill files through shell or local file inspection just to reconfirm the route or inputs.

Host execution guard: if the current run was already started from a host-side skill entry such as `codex exec`, Claude Code, Codex desktop, or another agent host, that current session is already the required host route proof. Do not launch nested host sessions, do not run `codex exec --help` or similar host-entry probes, and do not wrap the same task in another `codex exec` just to "prove" the route again. Continue inside the current session and execute the matched scenario directly.

For direct packaged CLI tasks that are not scenario workflows, use the matching packaged skill directly instead of forcing a scenario route. In this repo, `jenkins` and `github-workflow` are the main direct-use packaged skills for controller, job, build, queue, workflow-run, and config operations.

## Scenario routes

| Skill | When to Use | Capability Needs |
|-------|-------------|------------------|
| `sprint-kickoff` | Sprint planning, backlog readiness check, AC completeness analysis | Required: `tracker`; Optional: `docs` |
| `change-implementation` | Tracker work item -> bounded repo decomposition -> repo-understanding -> local implementation or fix -> one or more selected repo-provider PRs, with optional CI follow-up | Required: `tracker`, `repo`; Optional: `docs`, `ci`; Local helper: `repo-understanding` |
| `code-review` | PR code review with business context from linked work items and design docs | Required: `repo`; Optional: `tracker`, `docs`, `ci` |
| `security-fix-guide` | Triage SAST/SCA scan results from pasted reports or direct provider queries | Required: `repo`; Optional: `tracker`; One of: `security_scan`, `quality`, `report_mode` |
| `pentest` | Authorized penetration testing router for API, network, and cloud targets | None — routes to local helper skills |
| `delivery-metrics` | Sprint delivery data collection, metrics calculation, efficiency report | Required: `tracker`, `repo`; Optional: `docs` |
| `knowledge-capture` | Production bug postmortem records, code hotspot detection | Required: `repo`, `tracker`; Optional: `docs` |
| `gate-remediation` | Scheduled or operator-initiated provider-selectable quality/security issue-cluster remediation inside the resolved target boundary (`REPO_PATHS`, `REPO_NAMES + ROOT_DIR`, or `ROOT_DIR`), with fresh selected-provider evidence and post-merge default-branch follow-up until green | Required: `repo`; Optional: `ci`; One of: `security_scan`, `quality`; Local helper: `repo-understanding` |
| `release-orchestration` | Release lifecycle: changelog from tracker fixVersion, release branch creation, quality gate, tagging, CI build trigger, tracker issue transition, release notes publish | Required: `tracker`, `repo`, `ci`; Optional: `docs`, `quality`; Local helper: `repo-understanding` |
| `deployment-verification` | Post-deploy verification: CI build status, PR merge state, quality gate, optional smoke tests, rollback decision support | Required: `ci`, `repo`; Optional: `docs`, `quality` |
| `incident-response` | Production incident triage (ticket, deployment correlation, mitigation) and structured postmortem with cross-review | Required: `tracker`, `repo`, `ci`; Optional: `docs` |
| `monitor-check` | Runtime health, alert, and metric checks from cloud monitoring CLIs (Alibaba Cloud / AWS / Azure), optional tracker escalation | Optional: `tracker`; External: cloud CLIs (scenario-only) |

## Direct-use helper skills

| Skill | When to Use | Notes |
|-------|-------------|-------|
| `jenkins` | Jenkins controller summary, job, build, queue, or config operations | Use the packaged `jenkins` skill directly instead of one of the twelve scenario skills |
| `github-workflow` | GitHub Actions workflow definition, workflow run, queue, log, or config operations | Use the packaged `github-workflow` skill directly instead of one of the twelve scenario skills |
| `repo-understanding` | Repository understanding before implementation, review, or diff-impact analysis | Use this source-first skill directly when an AI agent needs grounded local code context before changing code |

Resolve provider skills at runtime from the installed sibling skill set.
Do not assume one fixed provider stack for every environment.
Read `references/installation-matrix.md`, `references/capability-contracts.md`, `references/provider-resolution.md`, `references/common-input-contract.md`, and `references/provider-linking-strategy.md` before deciding which provider path to use.

## Trigger-only behavior

If the user explicitly says this is only a skill trigger test, or explicitly forbids shell commands and remote calls for this check:

- Route to the matching scenario skill normally. The route decision itself is part of the validation.
- Treat the current host, the matched scenario skill, and the installed sibling skill list already exposed by the host as the working context. Do not ask the user to restate them.
- Do not claim the validation is blocked because the host did not expose a visible `Skill` tool, slash command, skill registry, or similar host entry. In trigger-only validation, the matched scenario is already the proof of route selection.
- If the user forbids shell commands for this check, do not run any shell command at all, including local inspection commands such as `pwd`, `sed`, `cat`, `rg`, or similar probes.
- Do not reread local skill files, safety rules, report files, or workspace files through shell during trigger-only validation. The matched skill contract already provides the missing-input rules.
- Do not ask for host platform, skill name, trigger entry, report language, or generic success criteria.
- Do not invoke UI or discovery tools such as `computer-use`, `browser`, `list_mcp_resources`, `list_mcp_resource_templates`, `list_apps`, `get_app_state`, app inspection, or similar host-side probing just to determine missing inputs.
- Ask only for the missing business inputs required by the matched scenario skill, including that skill's phase, route, or capability-specific conditional fields.
- Treat trigger-only validation as an input-contract check, not an execution-planning interview. Do not ask for execution-time artifacts such as offline snapshots, raw issue lists, review materials, bottleneck lenses, schedule cadence, or writeback destinations unless the matched scenario explicitly marks them as required inputs for the current phase and route.
- Skip provider discovery commands, preflight config checks, and any remote read until the user wants execution beyond trigger validation.

## Trigger Examples

- "分析 Sprint 42 的就绪度" → `sprint-kickoff`
- "检查这个 Sprint 的 AC 完整性并生成就绪度报告" → `sprint-kickoff`
- "Review PR #16 on sample-org/sample-repo" → `code-review`
- "结合 Jira Story 和设计文档审查这个 PR" → `code-review`
- "分析这份安全扫描报告" → `security-fix-guide`
- "根据扫描结果区分真实高危和误报" → `security-fix-guide`
- "直接从 Fortify 拉取 sample-service latest 的问题并给出修复建议" → `security-fix-guide`
- "分析 SonarQube 项目 sample-service 的最新安全问题" → `security-fix-guide`
- "看一下 Jenkins 上 folder-a/service-build 最新失败构建的 console" → use `jenkins` directly
- "列出 Jenkins queue 里卡住的任务" → use `jenkins` directly
- "查一下 Jenkins 上 folder-a/service-build #182 的状态和失败原因" → use `jenkins` directly
- "触发一下 Jenkins job folder-a/service-build" → use `jenkins` directly
- "用参数重跑 Jenkins job folder-a/release-build，参数 BRANCH=release/1.2、ENV=test" → use `jenkins` directly
- "看下 Jenkins controller 当前状态" → use `jenkins` directly
- "看一下 GitHub Actions workflow sample-ci.yml 最新一次运行的日志" → use `github-workflow` directly
- "触发一下 GitHub Actions workflow sample-ci.yml 在 main 上重跑" → use `github-workflow` directly
- "根据 Story 先帮我定位可能要改的代码和配置文件" → use `repo-understanding` directly
- "解释一下这个仓库里 src/auth/service.ts 为什么会影响 Jenkinsfile 里的验证" → use `repo-understanding` directly
- "看一下我这批改动的影响范围和相关测试" → use `repo-understanding` directly
- "从 Jira 里拉出 Story 和 Issue，自动实现后提 PR" → `change-implementation`
- "按 JQL 拉取 Ready For Dev 的 Story，定位代码并自动开发到 PR" → `change-implementation`
- "跨多个仓自动开发并分别提 PR" → `change-implementation`
- "把这个缺陷从 Jira 拉下来修掉，自测后帮我提 PR" → `change-implementation`
- "对 staging.myapp.com 做渗透测试" → `pentest`
- "对 staging.example.com 做 API 安全测试" → `pentest`
- "对 198.51.100.0/24 做授权网络渗透测试" → `pentest`
- "评估这个 AWS 环境的渗透测试范围" → `pentest`
- "采集本 Sprint 的交付数据" → `delivery-metrics`
- "分析 Sprint 42 的交付效率和瓶颈" → `delivery-metrics`
- "整理最近的生产 Bug 踩坑记录" → `knowledge-capture`
- "检测热点文件" → `knowledge-capture`
- "先确认修哪个 provider" → `gate-remediation`
- "修复这个 issue cluster，并按仓并行处理" → `gate-remediation`
- "等所选 provider 刷新到这次修复结果再报 done" → `gate-remediation`
- "定时拉取 SonarQube 中没过门禁的项目并自动修复到 PR" → `gate-remediation`
- "PR 合并后默认分支还是红，继续自动修复直到门禁通过" → `gate-remediation`
- "扫描 ROOT_DIR 下的仓库，处理 Fortify Medium 及以上问题并把修复提交到 PR" → `gate-remediation`
- "准备发布 1.2.0，生成 changelog 并创建 release 分支" → `release-orchestration`
- "按 fixVersion 拉取 Issue 生成发版变更日志，跨仓打 tag 并触发 release build" → `release-orchestration`
- "发布 1.2.0 后把 release notes 发到 Confluence" → `release-orchestration`
- "验证部署：检查 Jenkins build 状态、PR 合并状态和质量门" → `deployment-verification`
- "部署后跑 smoke test，失败就给出回滚建议" → `deployment-verification`
- "生产事件 P1，建 incident 单并关联最近部署" → `incident-response`
- "复盘这次生产事件，生成 postmortem 报告" → `incident-response`
- "检查服务健康度，查看活跃告警和指标" → `monitor-check`
- "查一下这台 ECS 实例的运行时监控和告警" → `monitor-check`

For security-fix-guide, three input modes are supported: pasted/file `SCAN_REPORT`, direct `fortify` query, and direct `sonarqube` query. Keep `SCAN_REPORT` mode for BlackDuck and exported historical artifacts.

## Shared references

Use these shared references as the source of truth for capability naming, input normalization, provider resolution, write confirmation, CLI caveats, and output conventions. When editing this router, change the shared reference first when the rule is repository-wide.

All skills follow the conventions in:
- `references/safety-rules.md` — write operations require user confirmation; stop on 403/404; deduplicate before creating tickets
- `references/cli-patterns.md` — known CLI limitations (Jira no --expand, Bitbucket PR list returns all, etc.)
- `references/output-conventions.md` — severity levels, status markers, data quality filters
- `references/parallel-dispatch.md` — optional parallel worker dispatch with inline sequential fallback
- `references/cross-review.md` — cross-review and adversarial re-review for judgment-heavy findings
