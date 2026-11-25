---
name: codebase-tips
description: "代码库 · 33 条：仓库索引和地图、写代码原则、AGENTS.md、改动范围规则。"
disable-model-invocation: true
---

# 代码库 · 33 条

Copybook 的 33 条「代码库」技巧，收藏多的在前。每条要用的文字、放到哪里、最后得到什么，都在 references/ 里它自己的文件中。

- 用户点名技巧时，用点名的那条。用户只说了要做什么时，从适用于实际执行者的技巧里，选最符合用户目标和限制的一条。几条同样合适时，选一条即可。选中后，用一句话说明选了哪条、为什么，再读它的文件照着做。另一条也合适，而且换用它会明显改变做法或结果时，顺带点出它的名字和区别。
- 用户什么都没说：把下面的列表（每条的名字和做什么）给用户看，问用哪条。
- 都不合适就直说，并建议用 copybook，它会在全部 146 条里找。

| 技巧 | 做什么 |
| --- | --- |
| [开源侦察员和收尾者提示词](references/open-source-scout-and-closer.md) `open-source-scout-and-closer` | 不熟的功能从零写、问要不要继续：先搜 GitHub，再把整个活干完，附一份大白话总结。 |
| [codebase-memory 仓库索引](references/codebase-memory-repo-index.md) `codebase-memory-repo-index` | 每个问题几十轮 grep 和读文件：仓库连成一张函数、文件和依赖的图，顺手找出能安全删的死函数。 |
| [Karpathy 的 4 条写代码原则](references/karpathys-4-coding-principles.md) `karpathys-4-coding-principles` | 过度设计、顺手改旁边的代码：先想再写、简单优先、改动要准、目标驱动，4 行写进 CLAUDE.md。 |
| [vibe coding 后的清理：5 条 Codex /goal 提示词](references/vibe-coding-cleanup-prompts.md) `vibe-coding-cleanup-prompts` | 额度重置时还剩一半：清掉死代码、重复实现和用不上的依赖，给定时任务和旧 worktree 分好类。 |
| [能点的仓库地图](references/clickable-repo-map.md) `clickable-repo-map` | 改一个仓库前先看清它：点任一模块，看到调用方、依赖、相关测试和源码证据，地图随代码更新。 |
| [Scope Guard：不让小任务越做越大的规则](references/scope-guard-rules.md) `scope-guard-rules` | 改个配置就搭框架、修个 bug 就加一层：够用的最小改动，复用现有代码，扩大范围先问你。 |
| [开发遗留文件的磁盘地图](references/disk-map-of-dev-leftovers.md) `disk-map-of-dev-leftovers` | 硬盘快满时先别乱删：只读扫一遍，树状图标出开发留下的大文件夹，清理脚本只删你勾选的。 |
| [Claude Code 和 Codex 共用的 AGENTS.md](references/one-agents-md-for-both-agents.md) `one-agents-md-for-both-agents` | 两个 agent 同一套做法：先规划、最小改动、分活、修 bug、做完先验证，每次纠正记进 Lessons。 |
| [理清面条代码的 /goal](references/untangle-goal.md) `untangle-goal` | 几个月 vibe coding 让代码缠成一团：一页 HTML 接线图，最严重的结标红编号，再逐个修、逐个跑测试。 |
| [Codex 动手前先调查和计划的提示词](references/investigate-and-plan-prompt.md) `investigate-and-plan-prompt` | 怕 agent 做错方向：先查仓库、复述目标、列假设和计划，批准才动手。 |
| [反复的 PR 意见写成 AGENTS.md 规则](references/pr-comments-as-agents-md-rules.md) `pr-comments-as-agents-md-rules` | 同一个 reviewer 反复提的问题：gh 扫最近 50 个 PR 排出来，选中的写成全局规则，不用再靠人提醒。 |
| [Archify：从代码画系统图](references/archify-system-diagrams.md) `archify-system-diagrams` | 要给人讲清系统结构：从代码生成一张能搜索、能追踪上下游、能对比版本的 HTML 图，可导出 PNG。 |
| [REA：拆开别家 app 的功能](references/rea-take-apart-a-feature.md) `rea-take-apart-a-feature` | 看中别家 app 的功能却不知道怎么做的：一层层拆开，每个结论标出证据，最后拿到自己实现的计划。 |
| [少写防御式代码：4 条 AGENTS.md 规则](references/less-defensive-code.md) `less-defensive-code` | 改一点点也要层层判空：Codex 只在数据进来的地方检查一次，之后直接用。 |
| [代码清理提示词：模块更少、更深](references/fewer-deeper-modules.md) `fewer-deeper-modules` | 功能跑通了，代码却到处重复：重复的删光，核心逻辑归到一处。 |
| [CI 耗时审计：150 次运行，9 项检查](references/ci-time-audit.md) `ci-time-audit` | 代码几分钟写完，每个 PR 却在等 CI：最慢的 5 个任务拆成排队、准备和运行，每处改动指到哪一行。 |
| [agent 工作区清点](references/agent-workspace-audit.md) `agent-workspace-audit` | agent 越用越笨先别怪模型：说明、skill、MCP 和记忆列成「保留 / 删除」清单，你批准后再清。 |
| [agent 记忆工具：8 个仓库分 4 类](references/agent-memory-tools-8-repos.md) `agent-memory-tools-8-repos` | agent 记不住代码、资料、对话和长任务：8 个仓库分 4 类，每类挑一个装，装前先给你看命令。 |
| [带 ASCII 图的全项目审查](references/whole-project-audit.md) `whole-project-audit` | 坏的、不一致或用不上的代码：改动前先讲清它怎么连起来，有把握的修掉，其余列出来。 |
| [AGENTS.md 瘦身：3 套方案并排](references/3-slimmer-agents-md-plans.md) `3-slimmer-agents-md-plans` | AGENTS.md 超过 200 行就不照做了：3 版更精简的并排，一版比一版激进，不丢规则，改前先给你看。 |
| [还没用户就不写兼容代码：AGENTS.md 规则](references/no-compatibility-code-yet.md) `no-compatibility-code-yet` | 项目还没人用，agent 却在写兼容代码：跳过兼容和迁移，每次改动走文档、测试、最小实现、清理。 |
| [deny、ask、allow 权限规则](references/deny-ask-and-allow-permissions.md) `deny-ask-and-allow-permissions` | 顺手删过「看起来没用」的配置：危险命令直接拦，push 和发布前先问，日常放行，deny 永远优先。 |
| [加边界代码前先问：AGENTS.md 一行](references/ask-before-edge-case-code.md) `ask-before-edge-case-code` | agent 总为几乎不会发生的边界情况加代码：一行规则让它先说会出什么问题、概率多大，等你点头。 |
| [从会话里写出的项目说明](references/instructions-from-your-sessions.md) `instructions-from-your-sessions` | 每开新会话都要重讲一遍背景：从最近 20 个会话里捞出来，写成一份项目说明，以后不用再说。 |
| [让 Claude Code 给自己做 Mod 的提示词](references/mod-request-for-claude-code.md) `mod-request-for-claude-code` | 想改 Claude Code 自己的界面或行为：这段提示词先找现成的 Mod，没有就提一个最小的方案。 |
| [清理前的 \~/.codex 和 \~/.claude 分类](references/codex-and-claude-sorted.md) `codex-and-claude-sorted` | 怕清理时把聊天记录也删了：每项分到 Keep、History、Work、Clearable 或 Unknown，命令逐条批准。 |
| [最近 20 个会话里的 mod 点子](references/mod-ideas-from-20-sessions.md) `mod-ideas-from-20-sessions` | 反复提的要求、中途叫停或撤销的命令、检查改动的方式：按帮助大小排好，引用你的原话。 |
| [/teach：拿自己的项目学战略型编程](references/teach-strategic-programming.md) `teach-strategic-programming` | 贵的 token 花在 AI 替代不了的事上：先问你代码库的 3 个问题，写出 MISSION.md 和课程，拿项目教你。 |
| [写进 CLAUDE.md 或 AGENTS.md 里的修 bug 循环规则](references/bug-fix-loop-rules.md) `bug-fix-loop-rules` | agent 既修又审，就会一直来回拉扯：修两次不好就停，只审这一轮的改动。 |
| [ub-mode：Clean Code 作者的 agent 规则](references/ub-mode-clean-code-agent-rules.md) `ub-mode-clean-code-agent-rules` | agent 的代码藏着 bug，测试骗你：每次改动都照这个 skill 来，自带 crapper、dryer、mutator 检查。 |
| [能点的仓库地图：叫法 vs 代码名](references/repo-map-words-vs-names.md) `repo-map-words-vs-names` | 你怎么叫一个模块，和代码里怎么叫它对不上：每一处都标红，最容易导致改错的排在最前。 |
| [反复犯的错变成 helper 函数和 lint 规则](references/repeat-mistakes-as-lint-rules.md) `repeat-mistakes-as-lint-rules` | 老犯同一个错：正确写法封装成 helper，lint 禁掉旧写法，报错写明该用哪个，它跑检查时自己改。 |
| [skill 按场景路由的规则](references/situation-routing-for-skills.md) `situation-routing-for-skills` | agent 常常忘了用装好的，你只好一个个点名：每个任务挑最合适的，一句话说明哪个、为什么。 |
