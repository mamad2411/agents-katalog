---
name: doc-hygiene
description: >-
  文档卫生纪律——写或更新 skills-engineering 下任何 .md 时，文档正文只陈述「最终态事实」，
  禁止写入过程叙事（迁移/owner 纠正/此前承载/待平移等），变更过程记入 CHANGELOG / evolution。
  作为 writing-docs.md 的纪律约束；实际触发靠 invocation.md 关键词行 + 写作约定（writing-docs.md 建议文档任务在 frontmatter 用 depends_on 声明本 skill，但 CI 不强制校验）。
locale: zh-CN
supported_locales: [zh-CN]
depends_on: []
owner: doc-hygiene
scope: global
---

# Doc Hygiene（文档卫生）

## 强制入口

命中本 skill 时，**必须先完整阅读** [references/doc_hygiene.md](references/doc_hygiene.md) 并按其中条款执行。不得以摘要代替全文。

## 核心铁律（一句话）

> **文档只描述「现在是什么」，不描述「怎么变成这样的」。**

过程叙事（迁移/owner 纠正/此前承载/待平移/抽象归属倒置…）是变更记录的内容，不是文档正文的内容。

## 规则索引

| rule_id | owner | scope | phase | precedence | conflicts_with | merges_into | field_owner |
|---------|-------|-------|-------|------------|---------------|-------------|-------------|
| DH-001 | doc-hygiene | global | structure | 500 | [] | [] | {} |
| DH-002 | doc-hygiene | global | structure | 500 | [] | [] | {} |
| DH-003 | doc-hygiene | global | structure | 500 | [] | [] | {} |

（条文见 [references/doc_hygiene.md](references/doc_hygiene.md)；元数据语义见 `cognitive-reasoning/references/rule_index.md`）

## 何时加载

- **依赖触发**：`writing-docs.md` 建议文档写作/更新任务在 frontmatter 中 `depends_on: [doc-hygiene]`（CI 不强制校验；实际落地路径为 invocation.md 关键词触发行 + 约定）。
- **显式触发**：用户写「更新文档」「加个说明」「记录这个结论」或任何产生/修改 `.md` 的操作。
- **跳过**：纯代码、纯脚本、不涉及文档正文的改动。

## 与 writing-docs.md 的关系

本 skill 是 `.agents/writing-docs.md`「变更约定」的**纪律强化**：writing-docs 规定变更要走演进流程（proposal→validate→promote），本 skill 规定**流程的产物（文档）里不许出现流程本身**。二者正交，同时生效。
