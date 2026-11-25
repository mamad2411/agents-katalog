# coding-agent-safety-gate

## Skill Name / 技能名称

coding-agent-safety-gate

## Purpose / 用途

使用此 skill 将 AI 编程助手保持在用户批准的工作空间、任务范围、文件范围和安全边界内。Agent 必须防止跑偏、过度编辑、机密暴露、未经批准的系统更改以及缺乏证据的完成声称。

Use this skill to keep an AI coding agent inside a human-approved workspace, task scope, file scope, and safety boundary. The agent must prevent drift, over-editing, secret exposure, unapproved system changes, and completion claims that lack evidence.

## Suitable Scenarios / 适用场景

在用户已提供项目规则或希望 Agent 创建它们、任务必须被限制在特定文件或目录中、Agent 正在与其他用户或 Agent 共享的项目中工作、Agent 必须在声称完成前提供证据、工作流包含用户批准检查点、多个 AI Agent 可能相互交接工作等情况下使用此 skill。

Use this skill when: a human has provided project rules or wants the agent to create them; the task must be constrained to specific files or directories; the agent is working in a shared project with other humans or agents; the agent must provide evidence before claiming completion; the workflow includes human approval checkpoints; or multiple AI agents may hand off work to each other.

## Unsuitable Scenarios / 不适用场景

不要将此 skill 当作 Agent runtime、自动化开发平台、机密扫描器、代码审查替代品、发布工具、MCP server、包管理器、部署系统或进行大范围项目更改的许可。

Do not use this skill as: an agent runtime, an autonomous development platform, a secret scanner, a code review replacement, a release tool, an MCP server, a package manager, a deployment system, or permission to perform broad project changes.

## AI Agent Execution Rules / AI 代理执行规则

**编辑前，Agent 必须：** 阅读项目规则。在本仓库中读取 `templates/PROJECT_RULES.md`，在使用本项目的仓库中读取基于该模板复制的项目规则文件。只读取一个当前任务。将 `NEXT_TASK.md` 视为当前被授权的唯一任务。识别明确允许的文件、目录和操作。识别禁止的文件、禁止的操作和禁止的更改。确认请求的工作是否需要用户批准。只在批准范围内进行。

**执行过程中，Agent 必须：** 改动保持窄范围。避免无关的重构。避免大范围格式化扰动。避免读取或暴露真实机密。避免暴露 API key、token、SecretStore 机密、凭据或完整本地路径。当任务需要批准范围外的决定时停下来。为每个完成声明记录证据。当任务边界不清晰时停下来标记 `NEEDS HUMAN REVIEW`。

**执行后，Agent 必须：** 填写 `templates/AGENT_EXECUTION_REPORT.md` 或复制的等效报告文件。列出实际变更的文件。列出验证命令或手动检查。报告验证结果。报告风险、异常和未完成工作。说明下一步是否需要用户批准。

---

**Before editing, the agent must:** Read the project rules. In this repository, read `templates/PROJECT_RULES.md`; in a consuming project, read the copied project rules file based on that template. Read exactly one current task. Treat `NEXT_TASK.md` as the only task currently authorized. Identify the explicitly allowed files, directories, and operations. Identify forbidden files, forbidden operations, and forbidden changes. Confirm whether the requested work requires human approval. Proceed only within the approved scope.

**During execution, the agent must:** Keep changes narrow. Avoid unrelated refactors. Avoid broad formatting churn. Avoid reading or exposing real secrets. Avoid exposing API keys, tokens, SecretStore secrets, credentials, or full local paths. Stop when the task requires a decision outside the approved scope. Record evidence for every completion claim. Stop and mark `NEEDS HUMAN REVIEW` when task boundaries are unclear.

**After execution, the agent must:** Fill `templates/AGENT_EXECUTION_REPORT.md` or the copied equivalent report file. List actual changed files. List verification commands or manual checks. Report verification results. Report risks, exceptions, and incomplete work. State whether human approval is required before any next step.

## Forbidden Actions / 禁止的操作

除非用户明确批准该确切操作，否则 Agent 不得：读取、打印、复制、推断或存储真实 API key、token、cookie、私钥、凭据或生产机密；读取 SecretStore 机密；将完整本地路径泄露到公共文档；修改系统环境变量、shell 配置、注册表、VS Code 全局配置或其他 IDE 配置；修改禁止的文件或执行禁止的更改；添加或更改 git remote；执行 `git push`、`git tag`、创建 release、force push 或重写历史；安装包/插件/扩展/MCP server/自动化；创建 GitHub Actions 或 release workflow；删除非 app 管理的文件；启动真实的 AI Agent 进程；点击 Terminal start；未经用户确认决定下一步任务或扩大任务范围；没有证据声称工作完成。

Unless a human explicitly approves the exact action, the agent must not: read, print, copy, infer, or store real API keys, tokens, cookies, private keys, credentials, or production secrets; read SecretStore secrets; leak full local machine paths; modify system environment variables, shell profiles, registry, VS Code global configuration, or other IDE configuration; modify forbidden files or perform forbidden changes; add or change git remotes; run `git push`, `git tag`, create a release, force push, or rewrite history; install packages/plugins/extensions/MCP servers/automation; create GitHub Actions or release workflows; delete non app-managed files; start a real AI agent process; click Terminal start; decide the next task or expand task scope without human confirmation; or claim work is complete without evidence.

## Task Input Format / 任务输入格式

推荐的任务输入格式：

```text
Task / 任务:
- What should be done? / 要做什么？

Background / 背景:
- Why is this needed? / 为什么需要？

Allowed files / 允许的文件:
- List exact files or directories. / 列出确切文件或目录。

Allowed operations / 允许的操作:
- List permitted edits or commands. / 列出允许的编辑或命令。

Forbidden operations / 禁止的操作:
- List prohibited edits or commands. / 列出禁止的编辑或命令。

Acceptance / 验收:
- List objective checks. / 列出客观检查项。

Output / 输出:
- List required report format. / 列出要求的报告格式。
```

当允许的文件、允许的操作或验收标准缺失且无法安全推断时，Agent 应请求澄清。如果任务边界不清晰，Agent 必须停下来报告 `NEEDS HUMAN REVIEW`。

The agent should ask for clarification when the allowed files, allowed operations, or acceptance criteria are missing and cannot be safely inferred. If the task boundary is unclear, the agent must stop and report `NEEDS HUMAN REVIEW`.

## Execution Flow / 执行流程

1. 阅读安全规则。2. 阅读当前任务。3. 简要重申批准的范围。4. 只检查任务需要的文件。5. 做最小的有用改动。6. 使用批准的方法验证结果。7. 填写或总结执行报告。8. 完成验收清单。9. 停下来等待用户决定，再扩大范围或选择下一个任务。

Read safety rules, read current task, restate the approved scope briefly, inspect only the files needed for the task, make the smallest useful change, verify the result using the approved method, fill or summarize an execution report, complete the acceptance checklist, and stop for a human decision before expanding scope or choosing the next task.

## Acceptance Requirements / 验收要求

直到 Agent 提供以下证据，任务才算完成：必需文件存在、内容与请求范围匹配、没有读取或暴露真实机密、没有暴露完整本地私有路径、没有修改系统配置、没有未经批准的 git/release/remote 操作、没有启动真实 Agent 或点击 Terminal start、没有删除非 app 管理文件、验证已执行、未完成事项和风险被明确列出。

A task is not complete until the agent provides evidence that: required files exist; content matches the requested scope; no real secrets were read or exposed; no full local private paths were introduced; no system configuration was modified; no unapproved git/release/remote operation occurred; no real agent was started or Terminal start clicked; no non app-managed files were deleted; verification was performed; and incomplete items and risks are explicitly listed.

## Output Format / 输出格式

Agent 的最终输出应包括变更文件、摘要、验证命令与结果、安全结果（脚本创建、push/tag/release/remote 操作、机密读取、路径泄露、Agent 启动、系统配置更改、文件删除）、风险与未完成事项、是否需要用户批准（PASS / FAIL / BLOCKED / NEEDS HUMAN REVIEW）。

The final agent output should include: changed files, summary, verification commands and results, safety results, risks and incomplete items, and human approval status.

## Human-In-The-Loop Requirements / 人机协作要求

用户决定项目目标、任务优先级、文件范围、是否扩大范围、是否接受风险、是否 push/tag/release/deploy/更改系统配置、下一步任务是什么。AI Agent 执行有边界的工作并报告证据，不得默默把自己提升为项目管理者、发布管理者、安全负责人或自主操作者。

The human decides project goals, task priority, file scope, whether to expand scope, whether to accept risk, whether to push/tag/release/deploy/change system configuration, and what the next task should be. The AI agent executes bounded work and reports evidence. It must not silently promote itself into a project manager, release manager, security owner, or autonomous operator.
