---
name: server-security-audit
description: "Audit authorized servers using established scanners and configuration checks, then summarize findings and remediation steps. Use when the user asks for server security audit or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: Security scanners / SSH / OS tools. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "devops-system"
  status: "integration"
  implementation-status: "definition-only"
  automation-level: "L3-L5"
  search-keywords: "server-security-audit, Server Security Audit, 服务器安全基线审计, server security audit, Linux security audit, security baseline, 服务器安全, 安全检查, DevOps automation, system automation, infrastructure automation, DevOps自动化, 运维自动化, 系统自动化"
  quality-score: "4.0/5"
---
# Server Security Audit / 服务器安全基线审计

## Purpose / 用途

**中文**

在明确授权的服务器上调用成熟扫描和配置检查工具，并汇总问题与修复建议。

**English**

Audit authorized servers using established scanners and configuration checks, then summarize findings and remediation steps.

## Status / 状态

- **Workflow status:** 🔵 Integration Required / 需要外部集成
- **Implementation:** 📘 Definition only / 仅工作流定义
- **Audit grade:** B
- **Quality score:** 4.0/5
- **Automation level:** L3-L5
- **Category:** DevOps & System / 系统与运维

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`server-security-audit` · `Server Security Audit` · `服务器安全基线审计` · `server security audit` · `Linux security audit` · `security baseline` · `服务器安全` · `安全检查` · `DevOps automation` · `system automation` · `infrastructure automation` · `DevOps自动化` · `运维自动化` · `系统自动化`

## When to use / 何时使用

Use this skill when the user explicitly requests **server security audit**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- Authorized infrastructure target or repository
- Environment and approval constraints

## Outputs / 输出

- Primary requested artifact
- Validation or review notes

## Core stack / 核心工具

`Security scanners / SSH / OS tools`

## Permissions / 权限

- `network`
- `privileged:possible`
- `authorized-target-only`

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
npx skills add BryceYuuu/open-workflow-skills --skill server-security-audit
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill server-security-audit --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `server-security-audit` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `server-security-audit` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

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
- Use privileged/system access only on explicitly authorized targets and prefer least privilege.

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
