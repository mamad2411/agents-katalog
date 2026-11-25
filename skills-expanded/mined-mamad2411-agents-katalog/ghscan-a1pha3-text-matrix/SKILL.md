---
title: "blader/humanizer 项目导读：把「去 AI 味」从一句玄学 prompt 变成一种可校验的工程"
slug: blader-humanizer-anti-ai-writing-skill
github_repo: "blader/humanizer"
source_key: "gh:blader/humanizer"
date: 2026-09-01T14:50:00+08:00
lastmod: 2026-09-01T14:50:00+08:00
draft: false
categories: ["技术笔记"]
tags: ["AI 写作", "Skill", "去 AI 味", "Agent", "Claude Code"]
description: "Humanizer 是 39k+ stars 的 agent skill，把维基百科『AI 写作迹象』整理成 35 条规则，让任何 agent 能把 AI 味文本改成人的写法而不改事实。本文解读它的规则结构、三遍工作流与自我校验设计。"
---

# blader/humanizer 项目导读：把「去 AI 味」从一句玄学 prompt 变成一种可校验的工程

## 核心判断

Humanizer 解决的不是「让 AI 写出更好的文章」的问题，而是「让 AI 自己识别出什么是 AI 味」的问题。它给出的答案很反直觉：**把「不像 AI」这件事拆成 35 条可以一条条指认的规则，做成一个只有 456 行 Markdown 的可安装 skill，让任何 agent 照着规则把文本改回人话，同时保证不增减一个事实。**

这跟大多数人「去 AI 味」的做法刚好相反。普通做法是给 AI 一句「写得更自然一点」，把判断完全交给模型自己。Humanizer 的立场是：**判断不能靠感觉，要靠清单**。维基百科的编辑们攒出了一套「AI 写作迹象」手册，Humanizer 把它变成了可执行代码一样的规则集——这是「审美可机检」这个命题的一次很干净的工程化。

## 项目坐标

| 维度 | 数据 |
|------|------|
| 仓库 | blader/humanizer |
| Stars | 约 39.4k（截至 2026-09）|
| 仓库大小 | 149 KB |
| GitHub 语言标签 | Python |
| 产品本体 | 一份 456 行的 `SKILL.md` |
| License | MIT |
| 版本 | 2.11.2 |
| 规则数 | 35 条 pattern，分 5 组 |
| 规则来源 | Wikipedia: Signs of AI writing（WikiProject AI Cleanup 维护）|
| 适配 | Claude Code / Cursor / Codex 等任何支持 skill 的 agent |

> 注意语言标签那个反直觉的点：GitHub 把这个仓库标成 Python，是因为里面有一个 88 行的自校验脚本 `validate-package.py`。真正的产品是纯 Markdown——**一个以 prompt 为产品、脚本只是测试的仓库**。语言标签是给机器看的，产品是给人（和 agent）看的。

## 问题拆分：AI 味到底是什么

要理解 Humanizer，先得理解它要消灭的东西。

### 根源是「回归均值」，不是「不够努力」

维基百科的 AI Cleanup 项目给了个很准的解释：LLM 用统计算法猜下一个词，结果自然趋向「统计上最可能、适用范围最广」的那个答案。这在统计上叫回归均值。后果是，模型会把具体、罕见、有棱角的事实抹掉，换成通用、正面、听起来很重要的描述。

原文那个比喻很形象：**「就像对着画像越喊越大声‘这是个重要人物’，画像却从锐利的照片糊成了一幅模糊的草图。主角越来越不具体，同时越来越夸张。」**

这就是 AI 味的本质：细节消失，重要性膨胀。

### 检测的困境：人和工具都不可靠

Humanizer 引用的维基百科资料里，记录了几个反直觉的研究结论：

- 2025 年一项研究显示，人类区分 LLM 文本和人写文本的能力**不比随机猜测好**。
- 另一项对德语论文的研究，人类识别率只有 AI 文本 57%、人类文本 64%。
- 重度 LLM 用户能做到约 90% 准确——但意味着标记 10 页就差不多有 1 个误伤。
- 自动检测工具（GPTZero 这类）错误率不可忽略，文本改写过就可能失效。

所以「去 AI 味」为什么难？因为**凭感觉既看不准，又容易误伤**。这正说明规则化的必要：感觉不可靠，那就列清单。

## 核心机制：35 条规则 + 三遍工作流 + 一条红线

### 第一层：35 条 pattern，五组分类

Humanizer 的规则集从维基百科手册里精炼成 35 条，分五组：

| 组 | 编号 | 管什么 | 例子 |
|------|------|--------|------|
| 内容模式 | #1-6 | 重要性膨胀、点名攀附、浅层 -ing 分析、广告腔、模糊来源、套话式挑战展望 | "marking a pivotal moment" → "was established in 1989 as part of a wider decentralization" |
| 语言与语法 | #7-13 | 高频 AI 词、回避 is/are、否定排比、三连排比、同义词轮换、假 X 到 Y 范围、被动语态 | "Additionally... landscape... testament" → "also... remains common" |
| 风格模式 | #14-19, #26-35 | em dash 滥用、过量加粗、加粗小标题列表、标题首字母大写、emoji、花引号、连字符堆砌、伪深刻、宣布下一节、标题重复、写旧版本、强行金句、格言腔、伪坦诚开场、回应没人提的反对、拒绝假选项 | "Let's dive in" → 直接讲内容 |
| 聊天机器人类 | #20-22 | 残留的机器人客套、知识截止声明、过度恭维 | "I hope this helps!" → 删掉 |
| 填充与含糊 | #23-25 | 填充短语、过量限定词、万能正能量结尾 | "Due to the fact that" → "Because" |

每组规则都配了「before / after」对照——这是规则可执行的关键。不是抽象告诫「别写套话」，而是具体到「`Additionally` 这个词，换成 `also`」。

### 第二层：三遍工作流，不把原结构当金科玉律

README 里那句 "It makes a first pass without treating the original structure as fixed" 是理解这套机制的关键。Humanizer 的改写不是逐句修补，而是：

1. **第一遍**：通读原文，标出所有 AI pattern，但**不把原段落结构当作必须保留的骨架**——可以合并段落、拆分句子、重组顺序，只要信息不丢。
2. **检查**：把草稿对着 35 条 pattern 和原文的事实再过一遍，找出仍然像 AI 的部分。
3. **重写**：只对仍然有问题的段落动手，围绕它的核心意思重写整段，而不是一句句打补丁。

SKILL.md 里给了两个强制自问：「哪里还像 AI 生成的？」和「这次改写有没有新增或删掉任何事实、名字、数字、日期、引语、引用？」——第二个问题就是事实保全的硬校验。

### 第三层：一条红线——不编造事实

这是 Humanizer 区别于大多数「润色 prompt」的关键所在。它的规则写得很硬：

> **不要编造事实。** 不得加入任何来源或用户没提供的名字、数字、日期、引语、引用。句子缺一个必要细节，就开口问，或者换一个更简单的写法。

一个例子很说明问题：里斯本游记里如果原文没说月份和街区，Humanizer 应该**问**，而不是脑补「十月」「阿尔法玛区」。唯一的豁免是虚构创作——因为虚构本来就是任务的一部分。

这条红线直接回应了「去 AI 味」最大的风险：**为了更像人，反而造了假**。Humanizer 用规则把「像人」和「诚实」焊死在一起。

### 声音匹配：给它两段你的文字，它按你的节奏改

Humanizer 支持「写作样本匹配」：你丢给它 2-3 段自己写的东西，它会先分析你的句子长度、用词、段落开头、标点习惯，然后按你的节奏改写。这个功能还有一个微妙的优先级设计——**写作样本可以覆盖默认风格规则**。比如默认规则禁止 em dash，但如果你本人爱用，样本匹配会按你的频率保留。

## 任务流案例：一段里斯本游记怎么穿过这套机制

用 README 里那个完整例子，把上面的机制串成一次真实流转。

**输入（AI 味）：**

> I recently spent five unforgettable days in Lisbon, and let me tell you — this city completely stole my heart... Nestled along the banks of the Tagus River, Lisbon stands as a vibrant testament to Portugal's enduring spirit... No trip would be complete without riding the iconic Tram 28... And the food? Simply divine. The original pastéis de nata... savoring one still warm was a moment I will never forget...

**机制逐层做了什么：**

- **#4 广告腔**：`Nestled along the banks`、`vibrant testament` 这些推销式语言被识别，删掉夸张，留下事实。
- **#14 em dash**：全文的破折号全部拆成逗号或句号。
- **#31 强行金句**：「Simply divine」「a moment I will never forget」这类戏剧化收尾被降级成具体陈述。
- **#25 万能正能量结尾**：原文那句 "If you're dreaming of your next getaway, this is one destination that promises memories to last a lifetime" 被整体砍掉，换成最后一个具体事实。
- **事实保全**：README 在示例上方明确注明，月份和街区这类细节必须来自作者，缺失就问而不是编造。示例的 After 里出现 `last October`、`Alfama`、`Graça`，正是演示「这些细节从作者那里拿到之后」的合法改写——红线不是「模糊化」，而是「细节必须有出处」。
- **第一遍不固定结构**：原文六个段落的骨架被重组——新稿从「十月去的、对这座城市心情复杂」直接切入，中间把山丘、电车、蛋挞、城堡串成一条更紧的线，结尾落回「春天再去、换双好鞋」这个具体计划。

**输出（人味）：**

> I spent five days in Lisbon last October and still have mixed feelings about it. Beautiful, yes. Also harder on the knees than anyone warned me.
>
> The hills are the whole story and somehow never make the brochures. My hotel was up in Alfama...

对比两版能看出这套机制的真正功力：**信息基本全保住了**（五天、电车 28 路、葡式蛋挞、圣若热城堡、山丘、阿尔法玛），但情绪从「浮夸的惊艳」变成了「诚实的五味杂陈」——人味来自具体和克制，不来自形容词。

## 数据解读：39.4k stars 说明什么，不能推出什么

### 这个数字主要在测什么

GitHub stars 测的是**关注度**，不是**效果**。它反映的是「有多少人觉得这个项目值得收藏」，不反映「用过的用户里有多少说它真的把 AI 味去掉了」。

### 数字更可能反映了哪部分事实

39.4k stars 放在 2025-2026 这个时段看，更多说明的是**生态**而不是单点产品力：

- 技能生态在爆发。「把一种能力做成可安装的 skill」这个模式被越来越多人接受，`skills.sh` 安装量、Claude Code 插件化都是佐证。
- 「去 AI 味」成了内容生产者的刚需。AI 生成内容泛滥，反过来让「看起来不像 AI」变成了有市场的商品。
- Humanizer 命中了「以 Wikipedia 手册为源」的权威背书——规则有出处，不是作者拍脑袋。

### 不能从这里推出什么

- **不能推出它能骗过所有检测器。** Humanizer 自己的文档都引用研究说检测工具错误率不可忽略，它也从不承诺「过检」。
- **不能推出 35 条规则完备。** SKILL.md 白纸黑字写了大量「false positives」提醒，维基母版也说这是「描述性」而非「规范性」清单——这些迹象只是「可能的」问题信号，不是「就是」问题的判决。
- **不能推出它适合中文。** 这是必须划清的边界：35 条规则里绝大多数是英文特征——`Additionally`、`landscape`、title case、花引号、em dash。中文的 AI 味是另一套信号（「值得注意的是」「综上所述」「赋能」「闭环」），需要另一套信号库。Humanizer 解决的是英文语境的工程问题。

## 采用建议与适用边界

### 谁该先用

- **英文内容创作者**：博客、newsletter、产品文案，要快速把 AI 初稿改成「像自己写的」，且不想逐句动脑。
- **用 agent 写文档的团队**：把它装进 Claude Code / Cursor，让文档输出先过一遍 Humanizer 再交付。
- **研究「审美可机检」的人**：它是把写作审美工程化的极简范本——456 行 Markdown 就是全部产品，可读性极佳。

### 谁可以等等

- **纯中文写作场景**：直接套用会失灵，需要自己的信号库（这也是中文技术写作 skill 存在的空间）。
- **追求「过 AI 检测」的**：Humanizer 的哲学恰恰反对这个目标——它要的是诚实和自然，不是伪装。

### 落地顺序

1. 最轻：`npx skills add blader/humanizer --global`，在任意 agent 里用 `/humanizer` 直接改一段文本。
2. 标准：把「粘贴文本」换成「指向文件」，让它只改正文、不动代码块和 frontmatter。
3. 进阶：给它 2-3 段你自己的旧文做声音样本，让改写按你的节奏来。
4. 参考：读一遍它 456 行 SKILL.md 本身——它同时是产品、文档和教学材料。

## 结尾判断

Humanizer 真正的价值，不在那 35 条规则本身（很多有经验的编辑本来就在这么做），而在它证明了**「写作审美可以降维成可执行清单，并且可以被自动化校验」**。

一个只有 456 行的 Markdown 文件，配上 88 行的自校验脚本（检查版本号三处同步、编号 1-35 连续、Plain Language 规则齐全、SKILL.md 不超过 500 行），撑起了一个 39.4k stars 的项目。它用事实回答了那个经常被当成哲学问题的疑问：**「像不像人」不是玄学，是可以一条条列出来、一条条检查的工程。**

对任何一个想让自己写的东西「不那么 AI」的人来说，这个仓库给出的启示比规则本身更值钱：别急着让 AI 更聪明，先把它要遵守的规则写清楚。规则清楚了，工具才有得做。

---

## 参考来源

- [blader/humanizer GitHub 仓库](https://github.com/blader/humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
