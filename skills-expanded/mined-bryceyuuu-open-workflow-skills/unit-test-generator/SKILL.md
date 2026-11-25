---
name: unit-test-generator
description: "Generate behavior-focused tests for normal, edge, invalid, and regression cases, then run them and report coverage gaps. Use when the user asks for unit test generator or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: Project test framework. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "development"
  status: "verified"
  implementation-status: "tested-reference"
  automation-level: "L2"
  search-keywords: "unit-test-generator, Unit Test Generator, 单元测试生成器, AI unit tests, test generator, code coverage tests, 单元测试生成, 自动测试"
  quality-score: "4.5/5"
---
# Unit Test Generator / 单元测试生成器

## Purpose / 用途

**中文**

针对正常、边界、非法输入和回归场景生成测试，并执行测试、报告覆盖缺口。

**English**

Generate behavior-focused tests for normal, edge, invalid, and regression cases, then run them and report coverage gaps.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** ✅ Tested reference implementation / 已测试参考实现
- **Audit grade:** A
- **Quality score:** 4.5/5
- **Automation level:** L2
- **Category:** Development & Engineering / 开发与工程

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`unit-test-generator` · `Unit Test Generator` · `单元测试生成器` · `AI unit tests` · `test generator` · `code coverage tests` · `单元测试生成` · `自动测试`

## When to use / 何时使用

Use this skill when the user explicitly requests **unit test generator**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- Repository, diff, logs, or requirements
- Project-specific build/test commands

## Outputs / 输出

- Source-code changes or review report
- Validation/test results

## Core stack / 核心工具

`Project test framework`

## Permissions / 权限

- `filesystem:read`
- `filesystem:write`
- `shell`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Parse Python source with AST**
2. **Discover public top-level functions**
3. **Generate syntactically valid test skeletons**
4. **Mark expected behavior as TODO instead of inventing assertions**
5. **Compile-check generated Python**

## Dependency suggestions / 依赖建议

- No universal runtime package is required by the skill format itself. Install only the tools named in **Core stack** when your chosen implementation needs them.

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Runnable reference / 可运行参考实现

This skill ships a tested reference runtime in `scripts/run.py`. From a cloned repository:

```bash
ows doctor unit-test-generator
ows run unit-test-generator -- --help
ows test unit-test-generator
```

`runtime.json` declares the entrypoint and optional system commands. Runtime dependencies are checked separately from installing the Skill definition.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill unit-test-generator
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill unit-test-generator --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `unit-test-generator` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `unit-test-generator` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

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
