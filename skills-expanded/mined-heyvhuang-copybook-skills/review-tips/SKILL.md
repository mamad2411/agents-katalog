---
name: review-tips
description: "验收 · 17 条：PR、代码和计划复查、bug 打分、红队提示词、skill 回测。"
disable-model-invocation: true
---

# 验收 · 17 条

Copybook 的 17 条「验收」技巧，收藏多的在前。每条要用的文字、放到哪里、最后得到什么，都在 references/ 里它自己的文件中。

- 用户点名技巧时，用点名的那条。用户只说了要做什么时，从适用于实际执行者的技巧里，选最符合用户目标和限制的一条。几条同样合适时，选一条即可。选中后，用一句话说明选了哪条、为什么，再读它的文件照着做。另一条也合适，而且换用它会明显改变做法或结果时，顺带点出它的名字和区别。
- 用户什么都没说：把下面的列表（每条的名字和做什么）给用户看，问用哪条。
- 都不合适就直说，并建议用 copybook，它会在全部 146 条里找。

| 技巧 | 做什么 |
| --- | --- |
| [手机上的 Tailscale 预览链接规则](references/tailscale-preview-links.md) `tailscale-preview-links` | agent 给的链接是 localhost：预览、审查页面、看板都换成 Tailscale 链接，手机上直接打开。 |
| [Astra 审查的 bug 打分规则](references/bug-score-rule-for-astra.md) `bug-score-rule-for-astra` | Astra 总挑几乎不会发生的 bug，Opus 一条条去修：给 bug 打分，分低的记成 issue，代码不动。 |
| [影响范围、红队等 5 条让模型判断的提示词](references/blast-radius-and-4-more-prompts.md) `blast-radius-and-4-more-prompts` | 只说「修这个 bug」只拿到默认答案：影响范围、并行目标、红队计划、真实用户走查、思考预算。 |
| [iOS 模拟器 UI bug 检查，含 iPhone Duo](references/ios-simulator-ui-bug-check.md) `ios-simulator-ui-bug-check` | iOS app 里的 UI 问题：主要页面都点一遍，有 Duo 模拟器就查各形态，建议最小改法。 |
| [性能审查：最慢的 5 处](references/perf-review-the-5-slowest-spots.md) `perf-review-the-5-slowest-spots` | 想让代码变快，多半换来一层缓存：profile 测出的耗时，每处对上的改法，要改的行和预计提速。 |
| [回答前先问一个问题](references/one-question-before-it-answers.md) `one-question-before-it-answers` | 一次问 10 个你就不想答：先摆出没说的假设、缺的信息和常见错误，再只问最可能改变做法的那个。 |
| [skill 回测：过去的 Codex 会话](references/skill-backtest-on-codex-sessions.md) `skill-backtest-on-codex-sessions` | 凭记忆写的 skill 和实际做法对不上：拿过去的 Codex 会话回测，先出 dry run 的 diff，再定期复查。 |
| [代码和方向复查提示词](references/code-and-direction-review.md) `code-and-direction-review` | 代码越来越复杂，或忙了很久不知道通向哪里：一条找出不必存在的代码，一条重新审视方向。 |
| [/claude-api prompt-audit：换 Fable 5.1 后的 skill 审查](references/claude-api-prompt-audit.md) `claude-api-prompt-audit` | skill 里还留着旧模型名和失效命令：官方 skill 审一遍，列出重复约束和过度强调，附 diff。 |
| [瞎忙检查：今天的 git 历史](references/fake-busy-check.md) `fake-busy-check` | 开了一堆会话，回头看什么都没做成：分清今天真合并的和来回改的，一句话定下明天第一件事。 |
| [每晚审查当天推送的 routine](references/nightly-push-review-routine.md) `nightly-push-review-routine` | 今天推到 main 的代码，睡觉时再看一遍：每个 bug 开 draft PR 附先失败的测试，笔记本合上也跑。 |
| [日志方案和每天的待修清单](references/logging-plan-and-daily-fix-list.md) `logging-plan-and-daily-fix-list` | 坏掉的功能、卡住的用户、太慢的步骤：按影响人数排序，附日志原文，最严重的一条已有测试。 |
| [一条消息里的 5 种计划复查方法](references/plan-review-5-methods.md) `plan-review-5-methods` | 计划写完代码还没动：一条消息要第一性原理、对抗性审查、消融测试、奥卡姆剃刀和高内聚低耦合。 |
| [skill 的是非题评分](references/skill-score-by-yes-no-questions.md) `skill-score-by-yes-no-questions` | skill 改了一版有没有变好：10 个真实任务、8 道是非题、不知情的评分 subagent，只留提分的那版。 |
| [装 skill 前的 3 项检查](references/3-checks-before-a-skill-install.md) `3-checks-before-a-skill-install` | 有人在 ClawHub 上放了 314 个恶意 skill：装之前查来源、扫代码、问清权限，不到 5 分钟。 |
| [1:1 on your week from git log and sessions](references/1-1-on-your-week-from-git-log.md) `1-1-on-your-week-from-git-log` | Moving this week or just busy: 7 days of git log and sessions, every judgment backed by a commit or conversation, 3 commitments. |
| [状态机检查：错误的转换标红](references/state-machine-check.md) `state-machine-check` | 功能状态间的 bug：从 UI 到服务端的每个状态画在一页 HTML 上，附编号清单，写明文件、行号和原因。 |
