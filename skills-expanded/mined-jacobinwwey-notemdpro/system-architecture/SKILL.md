---
name: system-architecture
description: Map the portable skill router, executable helpers and host-owned capabilities.
---

# System architecture

## English

This repository is a skill bundle, not the Obsidian plugin. `SKILL.md` routes tasks to `skills/*/SKILL.md`. Executable helpers are `skills/formula-healer/formulaFixer.ts` and `skills/mermaid-healer/mermaidProcessor.ts`; shared Markdown ownership lives in `scripts/markdown.ts`. The root package manifest supplies dependencies and test commands.

The calling agent owns file selection, provider access, output authorization, task transcripts and renderer/export capabilities. There is no local `main.ts`, Obsidian UI, provider registry, knowledge index or PDF engine. Do not invent these interfaces or import plugin-only modules.

For a requested workflow, map source paths -> skill -> helper or available host tool -> validation -> authorized output. Use [workflow-runner](../workflow-runner/SKILL.md) for stage diagnostics and [diagram-generator](../diagram-generator/SKILL.md) for semantic/geometry boundaries. Refer to the paired migration report under `docs/plans/` for adopted and deferred components.

## 中文

本仓库是技能包，不是 Obsidian 插件。`SKILL.md` 将任务路由至 `skills/*/SKILL.md`。可执行工具为 `skills/formula-healer/formulaFixer.ts` 与 `skills/mermaid-healer/mermaidProcessor.ts`，共享 Markdown 归属扫描器位于 `scripts/markdown.ts`。根目录包清单提供依赖与测试命令。

调用方智能体负责文件选择、provider 访问、输出授权、任务日志及渲染/导出能力。本地没有 `main.ts`、Obsidian 界面、provider 注册表、知识索引或 PDF 引擎，不得虚构这些接口或导入插件专属模块。

将请求的工作流映射为：源路径 -> 技能 -> 工具函数或可用宿主工具 -> 验证 -> 已授权输出。阶段诊断参见 [workflow-runner](../workflow-runner/SKILL.md)，语义与几何边界参见 [diagram-generator](../diagram-generator/SKILL.md)。已采用和推迟的组件详见 `docs/plans/` 下的双语迁移记录。
