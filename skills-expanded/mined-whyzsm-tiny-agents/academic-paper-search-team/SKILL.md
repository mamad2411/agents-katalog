---
name: academic-paper-search-team
description: >-
  从多数据库学术论文检索下载与引文提取（arXiv/PubMed/Semantic Scholar/Google Scholar）、跨平台系统性文献检索（IEEE/ACM/Scopus/Web
  of
  Science）与批量PDF下载元数据提取索引生成，到科研文献智能监测与中文摘要定时推送、知网CNKI高级检索自动化与真实参考文献引用规范管理的完整论文检索工作流。覆盖文献搜索、批量下载、智能监测、引用管理全链路。
---

# 论文检索

Use this skill as the routing entry point for the 论文检索 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide sections in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$academic-research-hub`
- `$literature-search`
- `$deepxiv-cli`
- `$research-paper-monitor`
- `$cnki-advanced-search`
- `$academic-citation-manager`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
