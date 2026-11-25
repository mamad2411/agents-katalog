---
name: cron-builder
description: "Convert scheduling requirements into cron or scheduler configuration, validate timing, and generate safe executable wrappers. Use when the user asks for cron builder or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: cron/systemd/scheduler. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "development"
  status: "verified"
  implementation-status: "tested-reference"
  automation-level: "L2"
  search-keywords: "cron-builder, Cron Builder, 定时任务生成器, cron generator, scheduled job generator, task scheduler, 定时任务生成, Cron表达式"
  quality-score: "5.0/5"
---
# Cron Builder / 定时任务生成器

## Purpose / 用途

**中文**

把自然语言时间需求转换成 Cron 或调度配置，校验时区和频率，并生成安全执行脚本。

**English**

Convert scheduling requirements into cron or scheduler configuration, validate timing, and generate safe executable wrappers.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** ✅ Tested reference implementation / 已测试参考实现
- **Audit grade:** A
- **Quality score:** 5.0/5
- **Automation level:** L2
- **Category:** Development & Engineering / 开发与工程

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`cron-builder` · `Cron Builder` · `定时任务生成器` · `cron generator` · `scheduled job generator` · `task scheduler` · `定时任务生成` · `Cron表达式`

## When to use / 何时使用

Use this skill when the user explicitly requests **cron builder**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- Repository, diff, logs, or requirements
- Project-specific build/test commands

## Outputs / 输出

- Validated schedule expression
- Executable wrapper/config

## Core stack / 核心工具

`cron/systemd/scheduler`

## Permissions / 权限

- `filesystem:write`
- `shell`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Parse a deliberately limited natural-language schedule grammar**
2. **Convert supported schedules to cron expression**
3. **Append the requested command**
4. **Fail on unsupported ambiguous schedules instead of guessing**

## Dependency suggestions / 依赖建议

- No universal runtime package is required by the skill format itself. Install only the tools named in **Core stack** when your chosen implementation needs them.

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Runnable reference / 可运行参考实现

This skill ships a tested reference runtime in `scripts/run.py`. From a cloned repository:

```bash
ows doctor cron-builder
ows run cron-builder -- --help
ows test cron-builder
```

`runtime.json` declares the entrypoint and optional system commands. Runtime dependencies are checked separately from installing the Skill definition.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill cron-builder
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill cron-builder --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `cron-builder` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `cron-builder` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

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

- `runtime.json` — runtime manifest
- `scripts/run.py` — runnable reference implementation
- `tests/smoke.py` — deterministic smoke test
