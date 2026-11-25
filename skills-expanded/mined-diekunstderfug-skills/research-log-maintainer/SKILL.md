---
name: research-log-maintainer
description: Use when preserving verified research findings, method or data-contract changes, or updating research handoff documentation (README, AGENTS.md, docs). Skip routine edits and queries that add no durable project knowledge.
---

# Research Log Maintainer

Keep research context recoverable from project files so a new agent can continue without prior chat or personal memory. Preserve useful knowledge with the smallest relevant documentation change.

## Scope and evidence

Read the applicable project instructions and existing documentation entry points, then inspect only the evidence needed for this update. Follow explicit user choices and local documentation contracts. Do not infer scientific results from a task title, proposed plan, remembered conversation, or code that has not run.

Use this workflow for substantive findings, decisions, reproducibility changes, or requested documentation maintenance. A routine code edit, unchanged rerun, or factual question does not automatically require a log entry. If nothing durable changed, leave documentation alone.

Memory can help locate prior work, but project files and verified artifacts are the durable source of truth. Resolve stale recollections against current evidence; do not rely on memory availability or write generated memory files as part of this workflow.

## Documentation layout

- Root `README.md` is the main human-facing entry: research purpose, current scope, working entry points, and links to supporting material.
- `AGENTS.md`, `CLAUDE.md`, and equivalents are the agent's research overview, essential working guidance, and index; see the content principles below.
- Supporting conclusions, run history, decisions, and method notes belong under `docs/` or the explicit project equivalent. Reuse existing topic files; create only documents with substantive content.
- Separate `docs/INSIGHTS.md`, `docs/CHANGELOG.md`, and `docs/DECISION_LOG.md` only when their different responsibilities justify separate maintenance. Small projects may use sections of one note. Do not require a standard file set per subproject.
- Subproject notes can live in `docs/<subproject>/`, or a standalone subproject's own `docs/`. Root README may link directly to a small collection; add `docs/README.md` only when a separate index helps navigation.
- Preserve required root files, licenses, and tool configuration. A log update does not authorize broad document migration. When reorganization is requested, preserve content and update inbound links and script references without leaving duplicate maintained copies.

## Agent entry: research overview plus index

A fresh agent should understand what the project studies and how to work on it without reconstructing the project from logs. Keep a brief, verified overview covering the information relevant to that project:

- Research question or objective, study objects/cohort or data types, and the main outcome or intended deliverable.
- Main study design, analytical methods, and essential technologies/languages/pipelines. Distinguish methods actually used from proposed future analyses; avoid a package inventory.
- Current research stage and the few confirmed conclusions or unresolved limitations that affect the next task. Include status only when verified and useful; point to the maintained detailed status record.
- Canonical input configuration, runnable entry points, results entry, and documentation links labelled with when to read them.
- Critical data-access, safety, and execution boundaries kept explicit in the entry file, even when detailed explanation lives elsewhere.

Use concise prose or a few bullets, not a mandatory template or arbitrary line limit. Keep enough subject context to orient a new agent; an index alone is insufficient. If purpose or method is uncertain, mark the gap or ask only what is needed rather than inventing it.

A short overview in README and agent instructions is intentional orientation, not a second full research report. Detailed evidence and history have one canonical home. Replace obsolete guidance instead of appending dated task summaries. Do not require every linked file to be read on every task or create multiple agent files just to repeat content.

## Update only the affected knowledge

1. **Identify the durable change.** Check whether the task changed research interpretation, a method/data contract, execution status, a reusable asset, or onboarding guidance. Use existing outputs and targeted read-only checks; documentation work does not itself justify rerunning analysis.
2. **Choose its canonical home.** Current conclusions belong in a synthesis note; dated run evidence and reproducibility changes in a history note; durable choices and rationale in a decision/method note. Update README or agent entry only when their overview, important constraints, or navigation changed.
3. **Write the smallest useful update.** State the conclusion, supporting evidence, and interpretation boundary. Link to detailed comparisons or canonical assets instead of copying tables and inventories. Record only real assets that changed; skip empty sections.
4. **Verify and stop.** Check changed claims against evidence, ensure links resolve relative to the containing document, confirm current conclusions agree across entry points, and report what changed and what remains unverified. Do not reopen the research task to fill a documentation template.

Read [research-log-patterns.md](references/research-log-patterns.md) when separating a large legacy log, recording a substantial method change, or choosing a conclusion/decision format. Small updates need no template.

## Scientific and privacy boundaries

- Distinguish a confirmed rule, edited code, updated data, executed analysis, and validated result. Record input/configuration versions or run dates when needed to identify the evidence; do not label old outputs as recomputed.
- Keep stable insights separate from run-by-run history. Preserve superseded evidence as labelled history when it matters for audit, while replacing obsolete current conclusions.
- State evidence strength, missingness/coverage when relevant, and whether a result is exploratory, negative, method-sensitive, or limited by data. Separate biological interpretation from technical limitations.
- Record model definitions, thresholds, scope, and output paths only to the extent needed to reproduce or interpret the change. Display relabeling is distinct from a cleaned-data recode; preserve the exact mapping and affected outputs when relevant.
- Never put patient-level rows, identifiers, raw matrices, secrets, or disallowed source text into documentation, logs, or agent context. Use permitted aggregate evidence and canonical paths, following project-specific access limits.

## Collaboration and style

Use one writer for ordinary updates. File count alone is not a reason to delegate. If a large update has independently useful work and delegation is authorized, give writers the same verified facts and disjoint file ownership; integrate and check consistency once. Do not prescribe a model or cost tier.

默认用中文维护研究文档；项目已有语言约定时服从约定。保留代码符号、文件名和必要专业术语。使用直接的研究语言，避免命令流水账、重复总结和为填模板而新增内容。
