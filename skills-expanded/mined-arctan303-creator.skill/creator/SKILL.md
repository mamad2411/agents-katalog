---
name: creator
description: Install or upgrade creator.skill, or adapt scenario design references into new or existing project conventions while preserving local decisions. 安装升级工作流，或按项目裁切、合并设计准则，保留本地约定。
---

# Creator gateway / 工作流与设计适配入口

## Choose the requested route / 按请求分流

- **Install/upgrade:** follow the installation workflow below. Installation permission does not include rewriting project design documents.
- **Establish/adapt/enrich project design:** read the [shared adaptation procedure](../.creator/references/design-adaptation.md), then the [scenario library index](../design-library/README.md) and only applicable modules. Reuse installed design-brief-builder for design decisions and project-knowledge for reconciliation when available and consistent with the procedure; otherwise perform that same procedure here. A design-only request does not require or authorize workflow installation.
- **Ordinary UI development/repair:** use the project's adopted rules and [reading procedure](../.creator/references/project-design.md); do not load the scenario library or regenerate conventions as a side effect.

设计适配可用于新项目，也可补充已有准则。先读取项目文档、逐层适用引用、真实组件与有效例外，再把相关参考转成本项目的具体规则。保留原文件、语言和约定；资料升级不会自动改变项目准则。只在必要未决体验边界处提问，已有充分依据时直接完成授权范围。

例如：“为这个项目建立设计准则，只采用相关场景”；“完善现有后台表单规范，保留品牌和整体保存”；“按新参考库检查这部分准则是否值得更新”。这些是自然语言任务，不是安装器 CLI 参数。无必要变更时报告保留理由即可。

## Installation / 安装

Install the prepared package; do not generate another policy tree. Both hosts use `creator-workflow.zip`, canonical `AGENTS.md` and `.agents/skills/`. Claude discovery uses thin `.claude/skills/` adapters. No `CLAUDE.md` or legacy slash commands are generated.

安装预构建包，不重新生成规则。两宿主共享一个包、一份 AGENTS.md 和一套技能正文；Claude 只增加发现入口。

## Workflow / 工作步骤

1. Establish the exact target project and authorized scope. Existing permission to upgrade covers the normal dry-run and conflict-free apply; do not ask again. Installing the workflow does not authorize migrating project docs, changing a user-level gateway, or upgrading other repositories.
2. Obtain `creator-workflow.zip` from the user's selected local build or the trusted [official release](https://github.com/arctan303/creator.skill/releases/latest). Inspect release version and artifact names first; do not claim an unreleased version is available. Hashes detect content changes but do not authenticate an untrusted publisher.
3. Read [host compatibility and commands](references/cli-adapters.md). Use the bundled `scripts/install_workflow.py` with an explicit `--root` and `--package`. The default is a read-only JSON plan. Do not manually extract the workflow ZIP over the project.
4. For a pre-1.6 installation, supply the matching trusted old official ZIP with `--baseline-package`; repeat for both old host packages if needed. A filename or `.version` alone does not prove ownership. Unknown or modified files remain intact and appear as conflicts. There is no force-overwrite option.
5. When the plan is conflict-free and within the user's authorized scope, rerun with `--apply`. A conflict blocks all installation writes. For an interrupted transaction inspect `--recover`, then use `--recover --apply` within the installation authorization. Recovery will not overwrite concurrent edits. Keep the journal when manual reconciliation is necessary.
6. Validate installed version, manifests and canonical files, then run the packaged structural evaluator. Diagnose Claude discovery separately: known host version, local/ancestor CLAUDE files, settings and `/context`. File installation does not prove live host discovery or model behavior.
7. Report package/version, preserved/merged/removed paths, unresolved conflicts and compatibility evidence. Report docs migration state separately; never create `complete` merely because installation succeeded. If docs adaptation was authorized, continue with the [migration guide](../.creator/references/docs-migration-1.5.md).

## Preservation and compatibility / 保留与兼容

- Preserve all existing signals, `.creator/docs-state.json`, project knowledge, custom cases and unrelated skills/commands. New installations create `.creator/evolution/signals.md`; existing `.codex/` and `.claude/` ledgers stay where they are. The installer does not combine their history.
- Same-ID official cases update only when they match the recorded official baseline; custom differences are conflicts. Recommend `project:<project>:<case>` IDs for new local cases; older project IDs remain valid.
- Obsolete official `CLAUDE.md`, duplicated Claude Skill files and old commands are removed only when their content exactly matches a trustworthy baseline. Customized remnants stay visible as conflicts; preserve their useful project rules before deliberately resolving the conflict.
- Native AGENTS discovery depends on the Claude version/session. An existing project or ancestor `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` can shadow it. User `~/.claude/CLAUDE.md` itself is not a shadowing file; user/managed settings can disable discovery. Do not alter those settings automatically.
- When native discovery is unavailable, explain the confirmed cause and, within explicit authorization, use an import such as `@AGENTS.md` in an appropriate existing `CLAUDE.md`. Do not create this fallback by default, replace project rules, or treat plain prose saying “read AGENTS.md” as an automatic import.

只在指定项目内应用可核实归属的文件变化；未知/定制冲突保留并报告，不能先覆盖再恢复。工作流安装、docs 迁移、真实宿主发现和模型行为是不同证据，不混写为全部通过。
