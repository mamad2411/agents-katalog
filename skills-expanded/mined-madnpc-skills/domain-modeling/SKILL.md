---
name: domain-modeling
description: "适用于构建或完善项目领域模型、统一代码库术语、创建或编辑 CONTEXT.md，以及记录或更新 ADR。Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR. 中文关键词：领域建模、领域模型、统一术语、术语表、上下文地图、CONTEXT.md、架构决策记录、ADR。"
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. Merely reading `CONTEXT.md` for vocabulary is not this skill; that is a one-line habit any skill can follow. Use this skill when changing the model, not just consuming it.

## 输出语言

默认使用简体中文与用户沟通，并以简体中文编写领域术语表和 ADR。用户明确指定其他语言或既有文档语言另有约定时，遵从该约定；代码、命令、产品名和必须保持原文的引用不强行翻译。

## File structure

Most repositories have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repository has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. For example: “Your glossary defines ‘cancellation’ as X, but you seem to mean Y. Which is it?”

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. For example: “You're saying ‘account’: do you mean the Customer or the User? Those are different things.”

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: “Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?”

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` immediately. Do not batch these updates; capture terms as they crystallise. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` must be devoid of implementation details. Do not treat it as a specification, scratch pad, or repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three conditions are true:

1. **Hard to reverse**: changing the decision later would have a meaningful cost.
2. **Surprising without context**: a future reader would wonder why it was done this way.
3. **The result of a real trade-off**: genuine alternatives existed and one was chosen for specific reasons.

If any condition is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
