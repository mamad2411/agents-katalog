---
name: debug-agent
description: "Reproduce failures, trace relevant code paths, isolate root causes, apply minimal patches, and run validation tests. Use when the user asks for debug agent or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: Git / shell / project tests. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "development"
  status: "verified"
  implementation-status: "definition-only"
  automation-level: "L2"
  search-keywords: "debug-agent, Debug Agent, 自动 Debug Agent, AI debugging, debugging agent, fix code errors, 自动Debug, 代码排错"
  quality-score: "4.5/5"
---
# Debug Agent / 自动 Debug Agent

## Purpose / 用途

**中文**

从复现问题开始，追踪相关代码，定位根因，最小修改并运行测试验证。

**English**

Reproduce failures, trace relevant code paths, isolate root causes, apply minimal patches, and run validation tests.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** 📘 Definition only / 仅工作流定义
- **Audit grade:** A
- **Quality score:** 4.5/5
- **Automation level:** L2
- **Category:** Development & Engineering / 开发与工程

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`debug-agent` · `Debug Agent` · `自动 Debug Agent` · `AI debugging` · `debugging agent` · `fix code errors` · `自动Debug` · `代码排错`

## When to use / 何时使用

Use this skill when the user explicitly requests **debug agent**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- Repository, diff, logs, or requirements
- Project-specific build/test commands

## Outputs / 输出

- Source-code changes or review report
- Validation/test results

## Core stack / 核心工具

`Git / shell / project tests`

## Permissions / 权限

- `filesystem:read`
- `filesystem:write`
- `shell`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Inspect / 检查输入** — Verify source files/data, format, scope, and user constraints.
2. **Plan / 制定计划** — Select the deterministic tools, model calls, and external integrations needed.
3. **Preflight / 运行前检查** — Check dependencies, credentials, permissions, destination paths, and destructive-action risk.
4. **Execute / 执行** — Run the smallest reliable sequence of steps. Prefer deterministic code for calculations, parsing, rendering, and file operations.
5. **Validate / 验证** — Verify output structure, counts, schemas, file readability, test results, or other task-specific invariants.
6. **Review / 审核** — For subjective or consequential outputs, present a reviewable result before external publication, sending, payment, deployment, signing, or irreversible action.
7. **Report / 汇报** — State what was produced, where it was saved, what was verified, and what still needs human review.

## Dependency suggestions / 依赖建议

- No universal runtime package is required by the skill format itself. Install only the tools named in **Core stack** when your chosen implementation needs them.

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill debug-agent
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill debug-agent --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `debug-agent` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `debug-agent` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

## Validation / 验证

At minimum:

- Verify all expected outputs exist and are readable.
- Verify the source was not unintentionally overwritten.
- Verify structured outputs against their expected schema or invariants.
- Record warnings, skipped steps, external dependencies, and failed checks.
- Never mark the workflow successful solely because a model produced text.

See `references/QUALITY.md` for skill-specific quality expectations.

## Safety / 安全

- Do not invent source facts or claim an external action succeeded without verification.
- Preserve source files unless the user explicitly requests in-place modification.
- Surface missing dependencies, permissions, credentials, and failed checks clearly.

## Failure handling / 失败处理

If a dependency, credential, connected service, browser session, file, or required permission is unavailable:

1. Stop the affected step.
2. Preserve completed safe outputs.
3. State exactly what is missing.
4. Do not fabricate a successful result.
5. Suggest the minimum next action needed to continue.

## Files / 文件

- `SKILL.md` — workflow instructions
- `references/QUALITY.md` — quality/evaluation guidance
- `tests/cases.yaml` — example evaluation cases

Implementation scripts may be added under `scripts/` when deterministic execution materially improves reliability.
