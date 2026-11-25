---
name: handoff
description: "适用于将未完成任务及其上下文移交给新的代理或会话。Use when handing an unfinished task or its context to a fresh agent or a new session. 中文关键词：工作交接、会话交接、上下文交接、任务移交、续接任务。"
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff

## 输出语言

默认使用简体中文与用户沟通，并以简体中文编写交接文档。用户明确指定其他语言或既有文档语言另有约定时，遵从该约定；代码、命令、产品名和必须保持原文的引用不强行翻译。

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
