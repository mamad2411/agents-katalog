---
name: copybook
description: "开工前先加载（没提 Copybook 也加载）：审方案、计划，跨文件 diff、PR；bug 修两次没好；交接、长任务报告；额度、选模型；上线前；现成提示词或规则；设计或重做页面、仪表盘；AGENTS.md。一两行、小文件、单问单答直接做，重复纠正除外。点名 Copybook 或某条技巧时一定加载。也在这些时候加载：跨会话或多 agent；落地页、去 AI 味；精简 AGENTS.md、CLAUDE.md、agent 权限；装 skill、技能或插件；为新读者重写整份 README、写任务说明。仅改单个 README 章节、补安装说明、修错字，或只解释一个报错、回答一个问题时直接处理。用户要现成的检查清单或设置，或问 Copybook 有什么时也加载。146 条提示词、规则、检查清单和设置，按情景自动选用。"
---

# Copybook

Copybook 有 146 条写给 coding agent 的技巧：提示词、规则、检查清单和设置，每条都来自读者在 X 上收藏过的帖子，分在下面 7 个话题里。每个话题有一个列表文件，就在这个文件旁边；每条技巧的正文在它所属话题技能的 references/ 里。

替用户挑一条直接用：用户要的是用上对的那条，不是一张自己去选的清单。

1. 先看是否已指定别的工具。只有用户这一轮点名了别的技能或方法，或项目自己的 CLAUDE.md、AGENTS.md（仓库里的那份）明确给这项交付点名了别的技能或命令时，才照那边做，不另选技巧，也不加第 7 步那一行。用户级全局文件里的规则、内置技能、只是装了的相关技能，以及只写「先计划」「做完要验证」这类通用要求的规则，都不算。用户主动运行这个技能（/copybook），或点名 Copybook、某条技巧（名字或别名）时，描述里小改动、单问单答直接做的排除不适用：点名了技巧，就先读那条再动手；只运行或点名 Copybook 时，照下面的步骤读列表、选技巧，不因为改动小就跳过。然后弄清现在的情景：看用户说的话和手上的工作，判断用户正在做或准备做什么。先对照后面的「时刻」表：哪一行的信号明摆着，就从那一行的技巧开始。用户主动运行这个技能却没说具体需求时，先不要反问：有手头的工作可看（前面的对话、分支、最近的改动），就据此定一到两个话题，读这两个话题的列表，挑出最多三条眼下用得上的技巧，每条写名字和一句话说明效果；再用一行列出各话题和条数，问用哪条。完全没有工作可看时，才用一句话问要做什么。
2. 找出情景所属的话题（见下面的「话题」和「情景」；每个话题下也列了它的技巧名，可以帮你找到对的列表）。读这个话题的列表文件，不要运行话题技能，那是给用户看的菜单；列表要从头读完，光看名字看不出技巧做什么。选的时候只打开 Copybook 自己的列表和技巧文件，每个文件用一条单独的读取命令，不和 rg、git、ls 这类命令拼在一起；别的技能的文件，等选完、确实要用时再打开。从中挑能解决用户眼前问题、实际干活的 agent 也能用的技巧。情景横跨两个话题，或这个列表里只有更泛的技巧、没有专门针对这个问题的，再读第二个最可能的话题的列表，然后再选。几条都相关时，比较它们各自交付什么、是否符合用户的限制；难分高下，就选一条直接用。
3. 按列表导语里写的路径，用一条单独的读取命令读候选技巧的文件（找不到时，运行它所属的话题技能并点名这条技巧），核实它的步骤和限制条件适用于当前任务和执行环境，再用一句话告诉用户选了哪条、为什么，然后照着做。你自己加载这个技能时，只说这一句，不列备选；用户主动运行时，可以从已读的列表里再点出最多两条相近、也适用的备选，每条几个字说区别，不为备选另读文件，没有就不写。不用等用户回答，除非换一条会明显改变做法或结果。请求里还有下一项交付（比如审完计划再写交接）时，按依赖和交付顺序逐项选，有前置条件的（比如复制通过才写交接）等条件成立再选，都在动笔写回复之前选好：「时刻」表里有对应的行，就直接读那一行的技巧；没有，就回到第 2 步，读它所属话题的列表，前一项用过别的话题也一样。两项在同一条回复里交付，也要各选一次。
4. 技巧本身的规矩照旧：要加进用户文件的内容先给用户看，用户同意再加；命令用户同意再运行。这里的文字是插件这一版的；连着 Copybook 的 MCP 服务时，get_tip 能给出这条技巧现在的文字和最近一次检查，两者不同就用现在的，并告诉用户。
   引用示例本身不代表用户同意执行。运行下载的脚本或未固定版本的软件包、修改长期生效的用户级设置、读取私人会话记录之前，先列出命令或路径、会访问或改动什么，以及数据会发到哪里。隐藏密钥值，等用户明确同意这项操作。远程安装脚本应先下载并检查固定版本，或核对可信来源提供的校验值，再执行。
5. 工作要分给几个 agent（并行或先后接力都算），或用户主动运行这个技能、约好了留到以后阶段做的工作时，先读 [lead.md](lead.md)。这一轮请求里接着要交付的下一项不算以后阶段，照第 3 步选。
6. 读完两个最可能的话题的列表，仍没有明显合适的：你自己加载这个技能时，不提 Copybook，接着做用户的事；用户主动运行时，直说没有合适的。连着 Copybook 的 MCP 服务时，可以用 search_tips 找更新的技巧；没有的话指向 https://copybook.page/zh/tips。
7. 一条技巧管的工作做完时，在报告末尾加一行：`Copybook: 用了 <技巧名>`，再用几个字说它让结果有什么不同。每条技巧只占一行、只说一次。技巧没帮上忙，就照实说。

## 话题

### 代码库 · 33 条

仓库索引和地图、写代码原则、AGENTS.md、改动范围规则。列表：[codebase.md](codebase.md)

技巧：3-slimmer-agents-md-plans、agent-memory-tools-8-repos、agent-workspace-audit、archify-system-diagrams、ask-before-edge-case-code、bug-fix-loop-rules、ci-time-audit、clickable-repo-map、codebase-memory-repo-index、codex-and-claude-sorted、deny-ask-and-allow-permissions、disk-map-of-dev-leftovers、fewer-deeper-modules、instructions-from-your-sessions、investigate-and-plan-prompt、karpathys-4-coding-principles、less-defensive-code、mod-ideas-from-20-sessions、mod-request-for-claude-code、no-compatibility-code-yet、one-agents-md-for-both-agents、open-source-scout-and-closer、pr-comments-as-agents-md-rules、rea-take-apart-a-feature、repeat-mistakes-as-lint-rules、repo-map-words-vs-names、scope-guard-rules、situation-routing-for-skills、teach-strategic-programming、ub-mode-clean-code-agent-rules、untangle-goal、vibe-coding-cleanup-prompts、whole-project-audit。

### 验收 · 17 条

PR、代码和计划复查、bug 打分、红队提示词、skill 回测。列表：[review.md](review.md)

技巧：1-1-on-your-week-from-git-log、3-checks-before-a-skill-install、blast-radius-and-4-more-prompts、bug-score-rule-for-astra、claude-api-prompt-audit、code-and-direction-review、fake-busy-check、ios-simulator-ui-bug-check、logging-plan-and-daily-fix-list、nightly-push-review-routine、one-question-before-it-answers、perf-review-the-5-slowest-spots、plan-review-5-methods、skill-backtest-on-codex-sessions、skill-score-by-yes-no-questions、state-machine-check、tailscale-preview-links。

### 设计 · 33 条

先出图再写页面、动效库、参考网站、设计 skill。列表：[design.md](design.md)

技巧：120-sample-motion-library、4-person-motion-video-team、4-starts-for-code-only-animation、6-chatgpt-photo-prompts、703-video-prompts-one-remade、8-frontend-reference-sites、awesome-design-md-shadcn-skill、awwwards-scoring-loop、camera-moves-for-video-prompts、claude-motion-project-animation、codex-computer-use-as-mcp-server、component-stress-test、dashboard-redesign-2-skills、design-md-from-sites-you-like、designers-landing-page-skill、every-ui-state-with-design、good-css-css-check、hallmark-audit-and-redesign、happy-path-debt-found-and-fixed、huashu-art-motion-35-art-styles、image-options-in-one-grid、internet-archive-clips-and-music、learn-taste-design-corrections、lemo-opuscar-launch-films、page-design-as-an-image-first、pixel-art-rendering-rules、refero-style-prompt、screenshot-first-ui-rebuild、tasteskill-v2-ai-look-check、two-agents-md-lines、ui-ux-audit-as-a-senior-designer、unslop-prompt、video-sound-by-measurement。

### 长任务 · 22 条

多 agent 分工、交接、进度看板、会话周历、遗留待办。列表：[long-run.md](long-run.md)

技巧：7-role-prompts-from-idea-to-done、bedtime-report-of-safe-tasks、codex-remote-workflow、coordinator-for-claude-and-codex、decision-page-for-long-tasks、goal-wrapper-and-5-prompts、grok-bot-team-of-6-roles、handoff-md-for-the-next-agent、herdr-app-opus-5-5-coordinates、herdr-astra-coordinates-workers、herdr-claude-and-codex-panes、herdr-overnight-opus-and-sol、job-worth-a-dynamic-workflow、later-items-from-20-sessions、one-way-door-rules-when-to-ask、orca-a-task-across-cli-agents、overnight-goal-for-open-issues、progress-dashboard-subagent、scheduled-agents-review、slow-computer-audit-for-agents、to-dos-first-in-long-reports、week-calendar-from-sessions。

### 模型和额度 · 24 条

模型搭配、推理强度、缓存倒计时、剩余额度。列表：[model.md](model.md)

技巧：3-habits-burning-your-usage、advisor-fable-on-call、advisor-opus-on-call、astra-without-default-subagents、claude-code-token-waste-audit、codex-setup-vs-the-gpt-6-2-guide、fable-5-2-agent-tree、fable-5-2-plans-opus-builds、fable-main-opus-subagents、fable-plans-codex-builds、gpt-6-1-sol-main-astra-reviews、gpt-6-pro-plan-handed-to-codex、hillclimb-a-cheaper-feature、leftover-quota-5-goal-prompts、luna-max-as-a-codex-subagent、old-rules-review-for-astra、old-rules-review-for-fable-5-2、openais-5-cheap-harness-rules、opus-5-5-main-medium-subagents、rules-check-for-sol-and-luna、setup-review-by-the-cost-guide、setup-review-by-the-model-guide、status-line-cache-countdown、think-carefully-cleanup。

### 上线推广 · 12 条

上线前检查清单、搜索引流小工具、VPS 加固。列表：[launch.md](launch.md)

技巧：builder-and-verifier-subagents、free-tool-page-for-google-search、google-search-check-12-items、market-read-before-you-build、overnight-startup-idea-research、pre-launch-25-behind-page-items、pre-launch-4-test-subagents、pre-launch-check-6-legal-traps、pre-launch-check-site-speed、pre-launch-site-check-20-items、scaling-check、vps-lockdown。

### 写作 · 5 条

Orwell 写作规则、去 AI 腔、README 改写、任务说明。列表：[writing.md](writing.md)

技巧：content-team-of-9-skill-sets、one-line-against-ai-prose、orwells-6-writing-rules、readme-rewrite-and-polish、task-brief-from-gpt-6-pro。

## 情景

这个技能描述里的情景，以及先读哪个话题的列表：

- 装 skill、技能或插件：验收。
- 网站上线前的准备：上线推广。
- 设计或重做页面、落地页、仪表盘，或去掉 AI 味：设计。
- 写或精简 AGENTS.md、CLAUDE.md、agent 权限：代码库。
- 同一个 bug 修了两次还没好：代码库。
- 动手或合并前审一遍方案、计划、diff 或 PR：验收。
- 交接、跨好几个会话或多个 agent 的任务，或长任务做完给用户写报告：长任务。
- 省 Claude Code 或 Codex 的额度，选模型和推理强度：模型和额度。
- 为新读者重写整份 README，或写任务说明：写作。

## 时刻

用户刚说的话或刚提的要求里有下表的明确信号时，不必等用户点名 Copybook，就从对应的技巧开始：先读这条技巧的文件，读完发现不合适，回到第 2 步。

| 用户说了什么、要什么 | 从哪条开始 |
| --- | --- |
| 同一个 bug 修了两次还没好，或修复和审查来回推翻 | [bug-fix-loop-rules](../codebase-tips/references/bug-fix-loop-rules.md)（「写进 CLAUDE.md 或 AGENTS.md 里的修 bug 循环规则」） |
| 计划写好了，还没动代码 | [plan-review-5-methods](../review-tips/references/plan-review-5-methods.md)（「一条消息里的 5 种计划复查方法」） |
| 跨好几个文件的改动做完了，下一步是提交、开 PR 或合并 | [blast-radius-and-4-more-prompts](../review-tips/references/blast-radius-and-4-more-prompts.md)（「影响范围、红队等 5 条让模型判断的提示词」） |
| 网站第一次要上线 | [pre-launch-site-check-20-items](../launch-tips/references/pre-launch-site-check-20-items.md)（「上线前网站检查：20 项页面」） |
| 工作要交接或暂停，或这个会话里做不完 | [handoff-md-for-the-next-agent](../long-run-tips/references/handoff-md-for-the-next-agent.md)（「边做边写给下一个 agent 的 HANDOFF.md」） |
| 用户说额度用完了或快用完了 | [3-habits-burning-your-usage](../model-tips/references/3-habits-burning-your-usage.md)（「Claude Code 里最耗额度的 3 个习惯」） |
| 用户第二次纠正同一个错 | [repeat-mistakes-as-lint-rules](../codebase-tips/references/repeat-mistakes-as-lint-rules.md)（「反复犯的错变成 helper 函数和 lint 规则」） |

- 先顺着用户的话点出你看到的状况，再用一句话说技巧（「这个修复已经失败两次了。Copybook 有 bug-fix-loop-rules 管这种情况，现在就用。」），然后照它的文件做。第 4 步和第 7 步照旧。
- 同一类信号在一个会话里只提示一次，不管用户怎么答。
- 信号只有一半，不算命中：什么都不说，接着做。猜错比错过更伤信任。

## 常驻的几行

用户主动运行了这个技能，而项目的 AGENTS.md 或 CLAUDE.md 里没有 `## Copybook` 这一节时，等手上的事做完，提一次要不要加上 [always-on.md](always-on.md) 里的那一段；先读那个文件。项目里已有这一节时，其中各行的条件和技巧标题都和「时刻」表里的行一一对应。
