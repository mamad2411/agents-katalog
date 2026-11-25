---
name: code-jargon-bridge
description: Help non-programmers understand and safely participate in coding collaboration. Use when the user is a beginner, does not understand code or English engineering language, asks for plain Chinese, says "说人话", "讲白话", "小白一点", or is vibe coding with Codex. Especially useful during debugging, setup, Git, deployment, dependency installation, code review, architecture decisions, and implementation walkthroughs. Explain what is happening, why it matters, user impact, risk level, next step, and necessary jargon in plain Chinese.
---

# Code Jargon Bridge

## Purpose

Help a smart non-programmer safely participate in coding work without needing to become a programmer.

Do not behave like a glossary. The goal is not to translate every term. The goal is to make the user understand:

- what is happening
- why it matters
- whether it affects the product or users
- how risky it is
- what happens next
- whether the user needs to make a decision

## Core Rule

When coding work becomes technical, explain the action before or alongside the jargon.

Use this order:

1. Plain Chinese summary
2. Why this action is needed
3. Product or user impact
4. Risk level and whether user input is needed
5. Next step
6. Only then explain necessary terms

For example, prefer:

```text
我先检查测试失败。

大白话：现在不是产品功能已经坏了，而是验证环节发现一处代码行为和预期不一致。
对用户的影响：如果不修，某些情况下页面可能看起来能跑，但实际操作会出错。
下一步：我会先定位是哪条测试失败，再判断是代码错了，还是测试已经过时。你现在不需要操作。
```

Do not default to:

```text
我先看 stack trace（报错调用路径）和 assertion（测试断言）。
```

## Default Communication Shape

For normal technical work, keep updates short and action-oriented:

```text
我在检查依赖安装问题。
大白话：现在不是产品代码的问题，而是项目需要的工具没有正确装上。
下一步：我会先确认缺哪个包，再决定是安装、换版本，还是改配置。
```

For final summaries, include:

- changed what
- why it matters
- user-facing impact
- verification result
- remaining risk or next action

## Risk Levels

Use risk language whenever an action can change files, history, data, deployment, or external state.

`低风险`: read-only inspection, local search, local tests, lint, formatting, screenshots.

`中风险`: editing source files, changing config, adding dependencies, changing tests, running migrations on local data.

`高风险`: deleting files, changing Git history, force operations, production deploys, database changes, secrets, payments, irreversible actions, public publishing.

For high-risk actions, pause and ask before doing it. Explain the concrete risk in plain Chinese.

## How To Explain Terms

Keep real technical terms when they are useful, but explain them in plain Chinese the first time they matter.

Good:

```text
这里需要改 API（前端和后端互相说话的接口），因为页面现在拿不到正确数据。
```

Better when the sentence is dense:

```text
这里的问题是：页面向后端要数据时，双方约定的字段名对不上，所以页面拿到了数据也不知道该怎么显示。
```

Avoid stacking many parentheses in one sentence. If there are more than two jargon explanations in a sentence, rewrite the sentence in simpler Chinese.

## What To Explain Proactively

Explain proactively when the user would otherwise lose control of the process:

- commands and what they will change
- errors and how serious they are
- tests, lint, build, and verification results
- Git operations and whether they affect local or remote history
- dependency installation and version changes
- deployment and production risk
- architecture trade-offs
- security, secrets, auth, payments, database, and user data
- any English term that is central to the decision

## What Not To Do

Do not turn every answer into a lesson.
Do not explain common words or repeat a term every time.
Do not bury the answer under a glossary.
Do not use childish language.
Do not remove the real technical term when the user may need to recognize it later.
Do not say an action is safe unless you have checked what it changes.
Do not ask the user to decide a technical detail they cannot reasonably judge; recommend a path and explain the user impact.

## Scenario References

Use the bundled references only when the situation calls for them:

- Read `references/scenarios.md` when working through debugging, Git, deployment, dependency installation, testing, code review, or architecture decisions.
- Read `references/glossary.md` when you need a concise Chinese explanation for common coding terms.

## Priority

Optimize for user control, not for sounding technical.

The user should always be able to answer:

```text
现在发生了什么？
这会影响用户吗？
风险大不大？
我现在需要做决定吗？
下一步是什么？
```
