---
name: document-diff
description: "Compare two versions of a document and identify additions, deletions, numeric changes, and semantic clause changes. Use when the user asks for document diff or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: Document parser / OCR optional / diff / LLM. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "data-analytics"
  status: "verified"
  implementation-status: "tested-reference"
  automation-level: "L2-L3"
  search-keywords: "document-diff, Document Diff, 文档语义差异比较, PDF compare, contract compare, document comparison, 合同对比, 文档差异, data automation, AI data analysis, Excel automation, analytics workflow, 数据自动化, 数据分析"
  quality-score: "4.0/5"
---
# Document Diff / 文档语义差异比较

## Purpose / 用途

**中文**

比较两版 PDF/DOCX 的新增、删除、数字和语义条款变化；扫描 PDF 可结合 OCR。

**English**

Compare two versions of a document and identify additions, deletions, numeric changes, and semantic clause changes.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** ✅ Tested reference implementation / 已测试参考实现
- **Audit grade:** A
- **Quality score:** 4.0/5
- **Automation level:** L2-L3
- **Category:** Data & Analytics / 数据与分析

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`document-diff` · `Document Diff` · `文档语义差异比较` · `PDF compare` · `contract compare` · `document comparison` · `合同对比` · `文档差异` · `data automation` · `AI data analysis` · `Excel automation` · `analytics workflow` · `数据自动化` · `数据分析`

## When to use / 何时使用

Use this skill when the user explicitly requests **document diff**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- User-provided source material or connected authorized data
- Desired output and constraints

## Outputs / 输出

- Structured change report
- Optional annotated output

## Core stack / 核心工具

`Document parser / OCR optional / diff / LLM`

## Permissions / 权限

- `filesystem:read`
- `filesystem:write`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Extract text from supported files**
2. **Use pdftotext only when available for PDF**
3. **Compute unified diff**
4. **Write deterministic diff artifact**
5. **Never claim semantic/legal interpretation from a textual diff alone**

## Dependency suggestions / 依赖建议

- No universal runtime package is required by the skill format itself. Install only the tools named in **Core stack** when your chosen implementation needs them.

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Runnable reference / 可运行参考实现

This skill ships a tested reference runtime in `scripts/run.py`. From a cloned repository:

```bash
ows doctor document-diff
ows run document-diff -- --help
ows test document-diff
```

`runtime.json` declares the entrypoint and optional system commands. Runtime dependencies are checked separately from installing the Skill definition.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill document-diff
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill document-diff --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `document-diff` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `document-diff` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

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
