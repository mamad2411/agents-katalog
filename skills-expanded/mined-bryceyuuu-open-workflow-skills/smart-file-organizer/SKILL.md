---
name: smart-file-organizer
description: "Classify and reorganize local files by content, project, date, and type with dry-run enabled by default. Use when the user asks for smart file organizer or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: Python / MIME detection / optional LLM. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "office-productivity"
  status: "verified"
  implementation-status: "tested-reference"
  automation-level: "L2"
  search-keywords: "smart-file-organizer, Smart File Organizer, 智能文件整理, AI file organizer, automatic file sorting, Downloads organizer, 文件自动整理, 桌面整理, office automation, AI productivity, workflow automation, 办公自动化, 效率工具, AI办公"
  quality-score: "4.5/5"
---
# Smart File Organizer / 智能文件整理

## Purpose / 用途

**中文**

按照内容、项目、日期和文件类型整理本地文件，默认先 Dry Run，禁止静默删除。

**English**

Classify and reorganize local files by content, project, date, and type with dry-run enabled by default.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** ✅ Tested reference implementation / 已测试参考实现
- **Audit grade:** A
- **Quality score:** 4.5/5
- **Automation level:** L2
- **Category:** Office & Productivity / 办公与效率

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`smart-file-organizer` · `Smart File Organizer` · `智能文件整理` · `AI file organizer` · `automatic file sorting` · `Downloads organizer` · `文件自动整理` · `桌面整理` · `office automation` · `AI productivity` · `workflow automation` · `办公自动化` · `效率工具` · `AI办公`

## When to use / 何时使用

Use this skill when the user explicitly requests **smart file organizer**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- User-provided source material or connected authorized data
- Desired output and constraints

## Outputs / 输出

- Primary requested artifact
- Validation or review notes

## Core stack / 核心工具

`Python / MIME detection / optional LLM`

## Permissions / 权限

- `filesystem:read`
- `filesystem:write`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Scan only the requested directory**
2. **Classify files by deterministic extension groups**
3. **Generate a dry-run plan**
4. **Copy files only when --apply is provided**
5. **Write organize-plan.json**
6. **Verify originals remain present**

## Dependency suggestions / 依赖建议

- No universal runtime package is required by the skill format itself. Install only the tools named in **Core stack** when your chosen implementation needs them.

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Runnable reference / 可运行参考实现

This skill ships a tested reference runtime in `scripts/run.py`. From a cloned repository:

```bash
ows doctor smart-file-organizer
ows run smart-file-organizer -- --help
ows test smart-file-organizer
```

`runtime.json` declares the entrypoint and optional system commands. Runtime dependencies are checked separately from installing the Skill definition.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill smart-file-organizer
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill smart-file-organizer --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `smart-file-organizer` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `smart-file-organizer` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

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
