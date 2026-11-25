---
name: long-run-tips
description: "长任务 · 22 条：多 agent 分工、交接、进度看板、会话周历、遗留待办。"
disable-model-invocation: true
---

# 长任务 · 22 条

Copybook 的 22 条「长任务」技巧，收藏多的在前。每条要用的文字、放到哪里、最后得到什么，都在 references/ 里它自己的文件中。

- 用户点名技巧时，用点名的那条。用户只说了要做什么时，从适用于实际执行者的技巧里，选最符合用户目标和限制的一条。几条同样合适时，选一条即可。选中后，用一句话说明选了哪条、为什么，再读它的文件照着做。另一条也合适，而且换用它会明显改变做法或结果时，顺带点出它的名字和区别。
- 用户什么都没说：把下面的列表（每条的名字和做什么）给用户看，问用哪条。
- 都不合适就直说，并建议用 copybook，它会在全部 146 条里找。

| 技巧 | 做什么 |
| --- | --- |
| [Claude Code 会话做的周日历](references/week-calendar-from-sessions.md) `week-calendar-from-sessions` | 一周的会话多到记不清：本机记录做成 HTML 周日历，标出没提交就停的会话，顺手写好 3 行周报。 |
| [6 个角色的 Grok Bot 团队](references/grok-bot-team-of-6-roles.md) `grok-bot-team-of-6-roles` | 哪些活该有自己的 Bot：6 个角色各有职责、交接和边界，其余留作 Skill 或 routine。 |
| [最近 20 个会话里的「以后再弄」](references/later-items-from-20-sessions.md) `later-items-from-20-sessions` | 说过「以后再弄」就忘了的事：从过去的会话翻出来，排好优先级，每件变成能直接开新会话的卡片。 |
| [Herdr 桌面版：Opus 5.5 协调执行者](references/herdr-app-opus-5-5-coordinates.md) `herdr-app-opus-5-5-coordinates` | 不离开 Claude Code 也能多开 agent：Opus 5.5 通过 Herdr 协调最多 10 个执行者，Codex 负责审查。 |
| [从想法到成品的 7 个角色提示词](references/7-role-prompts-from-idea-to-done.md) `7-role-prompts-from-idea-to-done` | 还把资深 AI 当实习生带：技术负责人、需求负责人、调试、性能、前端、后端、reviewer，各一条。 |
| [Herdr：Astra 协调 Claude Code 执行者](references/herdr-astra-coordinates-workers.md) `herdr-astra-coordinates-workers` | Codex 里也能用你的 Claude Code 订阅：Astra 通过 Herdr 协调最多 10 个 Opus 执行者，重活交给它们。 |
| [长任务的进度看板 subagent](references/progress-dashboard-subagent.md) `progress-dashboard-subagent` | 长任务跑着不知道进展：后台搭一个 HTML 看板，显示进度、卡点和等你拍板的问题，主会话不停。 |
| [Herdr：Claude 和 Codex 同跑一个任务](references/herdr-claude-and-codex-panes.md) `herdr-claude-and-codex-panes` | 结论靠你在窗口间搬来搬去：拆任务，每个 agent 自己的 worktree 和目标，一个执行、一个审查。 |
| [长报告先列待办：AGENTS.md 规则](references/to-dos-first-in-long-reports.md) `to-dos-first-in-long-reports` | 要你做的事埋在长报告中间：AGENTS.md 加一节，每份长报告最上面先列编号待办。 |
| [多 agent 时电脑变慢的排查](references/slow-computer-audit-for-agents.md) `slow-computer-audit-for-agents` | 开着很多 agent 电脑就卡：先 dry run 理清进程树和开机启动项，再只清理你批准的那些。 |
| [最该用动态工作流跑的活](references/job-worth-a-dynamic-workflow.md) `job-worth-a-dynamic-workflow` | 哪件活值得交给一批 agent：全仓库检查、迁移或修复循环，先在一个目录、10 个 agent 以内排好计划。 |
| [Herdr 通宵：Opus 5.5 写，Sol 审](references/herdr-overnight-opus-and-sol.md) `herdr-overnight-opus-and-sol` | 一个卡住的步骤吃掉整晚：每步最多 3 次尝试，还不行就记下错误，转去下一个独立步骤。 |
| [睡前报告：今晚能放心跑的任务](references/bedtime-report-of-safe-tasks.md) `bedtime-report-of-safe-tasks` | 额度每晚用不完：睡前一小时从今天的活里挑 3-5 个可撤回、能验证的，写好提示词，什么都不改。 |
| [Orca：一个任务分给多个 CLI agent](references/orca-a-task-across-cli-agents.md) `orca-a-task-across-cli-agents` | 几个 CLI agent 同跑没人盯进度：各有目标，reviewer 只读，写代码的各用 worktree，一人整合。 |
| [边做边写给下一个 agent 的 HANDOFF.md](references/handoff-md-for-the-next-agent.md) `handoff-md-for-the-next-agent` | 任务一个会话做不完：进度、决定、相关文件、验证结果和下一步边做边记，下一个 agent 接得上。 |
| [长任务的决策页规则](references/decision-page-for-long-tasks.md) `decision-page-for-long-tasks` | 总结只说一切顺利，藏起了 agent 替你拿的主意：改变结果的列在一屏里，要你确认的标红。 |
| [按 OpenAI 指南设计的 Codex 远程工作流](references/codex-remote-workflow.md) `codex-remote-workflow` | 离开电脑时项目还能推进：按 OpenAI 的 Remote 指南排出哪些任务自己跑、哪些决定在手机上做。 |
| [定时 agent 检查：按 Anthropic 指南](references/scheduled-agents-review.md) `scheduled-agents-review` | 定时任务写「最近 24 小时」会漏会重：固定时间窗口、读取失败不报和发帖风险，各附最小改法。 |
| [通宵 /goal：未关闭的 issue 和 TODO](references/overnight-goal-for-open-issues.md) `overnight-goal-for-open-issues` | 睡前：每个 issue 和 TODO 不靠你推进到最远，最后一张 HTML 看板列出完成、卡住和等你拍板的。 |
| [目标外壳和 5 条配套提示词](references/goal-wrapper-and-5-prompts.md) `goal-wrapper-and-5-prompts` | 一个偏好写了 3 处还要说第四遍：一个目标外壳，加组件库、并行、互审、交互状态、纠正清单 5 条。 |
| [AGENTS.md 单向门规则：什么时候该问](references/one-way-door-rules-when-to-ask.md) `one-way-door-rules-when-to-ask` | 只需要你走个过场的提问：撤得回的先做完再给你看，撤不回的先停下。 |
| [Claude Code 和 Codex 的协调者 skill](references/coordinator-for-claude-and-codex.md) `coordinator-for-claude-and-codex` | 一个会话做不完的活：每条 lane 一份带边界和完成检查的任务说明，再在 Herdr 里跑 Claude 和 Codex。 |
