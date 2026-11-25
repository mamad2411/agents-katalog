---
name: secret-scanner
description: "Scan repositories and history with dedicated secret-detection tools and produce remediation guidance without exposing secrets in reports. Use when the user asks for secret scanner or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: gitleaks/trufflehog/GitHub scanning. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "devops-system"
  status: "verified"
  implementation-status: "tested-reference"
  automation-level: "L2-L3"
  search-keywords: "secret-scanner, Secret Scanner, 密钥泄露扫描, secret scanning, API key scanner, credential leak detector, 密钥扫描, API Key泄露, DevOps automation, system automation, infrastructure automation, DevOps自动化, 运维自动化, 系统自动化"
  quality-score: "5.0/5"
---
# Secret Scanner / 密钥泄露扫描

## Purpose / 用途

**中文**

使用专用密钥扫描工具检查仓库和 Git 历史，并生成修复建议，报告中不回显完整密钥。

**English**

Scan repositories and history with dedicated secret-detection tools and produce remediation guidance without exposing secrets in reports.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** ✅ Tested reference implementation / 已测试参考实现
- **Audit grade:** A
- **Quality score:** 5.0/5
- **Automation level:** L2-L3
- **Category:** DevOps & System / 系统与运维

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`secret-scanner` · `Secret Scanner` · `密钥泄露扫描` · `secret scanning` · `API key scanner` · `credential leak detector` · `密钥扫描` · `API Key泄露` · `DevOps automation` · `system automation` · `infrastructure automation` · `DevOps自动化` · `运维自动化` · `系统自动化`

## When to use / 何时使用

Use this skill when the user explicitly requests **secret scanner**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- Authorized infrastructure target or repository
- Environment and approval constraints

## Outputs / 输出

- Redacted findings report
- Remediation checklist

## Core stack / 核心工具

`gitleaks/trufflehog/GitHub scanning`

## Permissions / 权限

- `filesystem:read`
- `network:optional`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Walk text files under an authorized path**
2. **Skip large/vendor/.git content**
3. **Match a conservative set of credential patterns**
4. **Redact secret values in reports**
5. **Optionally fail CI when findings exist**

## Dependency suggestions / 依赖建议

- Recommended scanner: Gitleaks or TruffleHog (install separately and review their release/source before use).

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Runnable reference / 可运行参考实现

This skill ships a tested reference runtime in `scripts/run.py`. From a cloned repository:

```bash
ows doctor secret-scanner
ows run secret-scanner -- --help
ows test secret-scanner
```

`runtime.json` declares the entrypoint and optional system commands. Runtime dependencies are checked separately from installing the Skill definition.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill secret-scanner
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill secret-scanner --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `secret-scanner` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `secret-scanner` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

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
