---
name: creative-ideation
title: Creative Ideation — Routed Library of Creative Methods
description: "Generate ideas via named methods from creative practice."
version: 2.1.0
author: SHL0MS
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Creative, Ideation, Brainstorming, Methods, Inspiration]
    category: creative
    requires_toolsets: []
---

# 创意构思

涵盖各领域的创意方法库。先分析用户处境，匹配相应方法，再加以应用，最终生成具体且富有新意的成果。这些方法只是工具——需根据具体情况选择最合适的，而非全部使用。

## 适用场景

任何开放式生成型或筛选型问题：“我想创造/构建/撰写/启动某件事”、“我陷入僵局了”、“给我一些灵感”、“让这个更奇特些”、“帮我做选择”、“我需要发明X”、“给我一个研究课题”。

## 操作规则

1. **约束加方向才是创造力**。没有约束则缺乏方向，没有方向则难以成形。这些方法能同时提供两者。
2. **舍弃前三个想法**。它们往往质量低下。需反复生成、筛选后再尝试。详情参见 `references/anti-slop.md`。
3. **除非用户另有要求，每次回复仅使用一种方法**。避免同时堆砌多种方法。
4. **具体性优于抽象性**。应使用真实的专有名词、真实材料与真实机制。“一个用于X的应用程序”属于空泛表述；而“一个200行长的CLI工具，当Z发生时能输出Y”则更具方向性。仅提及技术栈并不算具体，需明确具体的实现机制。
5. **奇特的同时也要实用**。打破常规是目标，但若某个想法仅凭奇特性存在，却缺乏实际背景、机制或合理依据，那它本身就是一种失败模式。每组创意中至少应包含一个真正*当前即可构建/实施*的方案——虽不寻常但有现实基础，并且有明确的第一个行动步骤。切勿为追求惊喜而牺牲实用性。
6. **需注明所使用的方法及其发明者**。明确归属能提升内容的严谨性。
7. **用户选定一种方法后，立即着手实现**。用户做出选择后不要再继续生成新想法。

## 路由机制——四步流程

在生成任何内容之前必须完成此步骤。若路由失败，生成的成果将质量低下。

如果简化叙述更清晰，可省略对路由步骤的说明，但**绝不能以牺牲每个创意的深度为代价**：每个创意的具体实现机制、与情境的关联以及诚实的缺陷分析，才是决定输出质量的关键要素——它们并非临时框架，不可省略。

### 第一步：从提示语中提取三个信号

**阶段**——用户当前处于哪个阶段？

| 阶段 | 关键提示 |
|---|---|
| **构思阶段** | “给我一个想法”、“我该做什么”、“给我灵感”，尚未形成具体想法 |
| **扩展阶段** | “还有哪些可能？”、“类似的东西再给我一些”、“给我一些变体”——已有一个初步想法 |
| **选择阶段** | “帮我做选择”、“我该选哪个？”、“我有这些选项” |
| **破局阶段** | “我陷入僵局了”、“进展不顺”、“一直在重复同样的思路”、“内容缺乏新意”——已有素材可供利用 |
| **颠覆阶段** | “让这个更奇特些”、“不要那么常规”、“这太安全了” |
| **优化阶段** | “这样还行，但缺少点什么”、“感觉不够完善” |
| **综合阶段** | “我有一堆笔记/访谈记录/观察结果” |

**领域**——用户正在创造/处理的是什么类型的内容？

| 领域 | 关键提示 |
|---|---|
| **文本** | 小说、散文、诗歌、歌词、剧本、广告文案 |
| **视觉作品** | 视觉艺术、音乐、声音、表演、装置艺术、雕塑 |
| **人造物** | 软件、硬件、机械装置、设备 |
| **系统** | 组织、公民团体、机构、生态系统、社区 |
| **个人成长** | 生活决策、职业规划、个人实践 |
| **研究** | 论文、学位论文、学术课题 |
| **产品** | 商业项目、市场方案、服务设计 |

**具体性程度**——提示语中包含多少约束条件？

| 程度 | 关键提示 |
|---|---|
| **无约束** | “我好无聊”、“给我一些灵感”——既未明确领域，也未指定具体项目 |
| **仅明确领域** | “我想写点东西”——知道所属领域，但未确定具体项目 |
| **已明确项目** | “我正在研究具体的X” |
| **存在具体问题** | “在X领域中我遇到了特定的难题” |

### 第二步：应用优先级更高的规则

这些规则优先于常规路由表：

- **情绪信号**——用户提到“奇特”、“奇怪”、“令人惊讶”、“不那么常规”、“更有趣”等 → 无论属于哪个领域，均优先使用 `references/methods/lateral-provocations.md` 或 `references/methods/pataphysics.md` 中的方法。
- **用户指定了某种方法**——直接使用该方法。
- **用户请求推荐方法**（如“用哪种方法？”）——列出2–3种候选方法，每一种简述一行，再询问用户选择哪一种。切勿擅自默认。
- **属于低质量创意领域**——如“AI相关点子”、“创业点子”、“习惯追踪工具”、“提升效率/健康/健身/饮食/旅游类的应用” → 强制使用 `references/methods/lateral-provocations.md` 或 `references/methods/pataphysics.md`，而非常规方法。需舍弃前**5个**想法，而非3个。

### 第三步：先按阶段路由，再按领域分类

**按阶段路由（适用于所有领域）：**

| 阶段 | 默认路由路径 |
|---|---|
| 构思阶段 + 无具体约束 | `references/full-prompt-library.md` 的 **通用** 部分（约束分配模块） |
| 构思阶段 + 已明确领域 | 按对应领域路由（见下表） |
| 扩展阶段 | `references/methods/scamper.md` |
| 选择阶段 | `references/methods/premortem-and-inversion.md`（若需积极方向则使用 `references/methods/compression-progress.md`） |
| 破局阶段 | `references/methods/oblique-strategies.md` |
| 颠覆阶段 | `references/methods/lateral-provocations.md`（备用方案为 `references/methods/pataphysics.md`） |
| 优化阶段（文本类） | `references/methods/defamiliarization.md` |
| 优化阶段（其他类型） | `references/methods/creative-discipline.md`（Tharp的创作法则） |
| 综合阶段 | `references/methods/affinity-diagrams.md` |
| 需要快速生成大量内容 | `references/methods/volume-generation.md` |

**按领域路由（当已明确领域且处于构思阶段时）：**

| 领域 | 默认路由路径 |
|---|---|
| **文本——正式文体/诗歌** | `references/methods/oulipo.md` |
| **文本——叙事类** | `references/methods/story-skeletons.md` |
| **文本——有可混编的素材** | `references/methods/chance-and-remix.md` |
| **视觉作品（音乐、视觉艺术、表演）** | `references/methods/oblique-strategies.md` |
| **视觉作品——实体制作类/需要初始约束条件** | `references/full-prompt-library.md` 的 **实体/视觉作品** 部分 |
| **人造物——需要初始约束条件** | `references/full-prompt-library.md` 的 **软件/人造物** 部分 |
| **人造物——存在参数冲突的工程发明** | `references/methods/triz-principles.md` |
| **人造物——软件架构设计** | `references/methods/pattern-languages.md` |
| **人造物——有自然系统类比** | `references/methods/biomimicry.md` |
| **人造物——需要质疑现有假设** | `references/methods/first-principles.md` |
| **系统（公民组织、机构等）** | `references/methods/leverage-points.md` |
| **系统——集体/参与式类型** | `references/full-prompt-library.md` 的 **社会/集体** 部分 |
| **个人成长（生活、职业、学习方向）** | `references/methods/derive-and-mapping.md` |
| **研究——选择研究课题** | `references/methods/compression-progress.md` |
| **研究——解决已知问题** | `references/methods/polya.md` |
| **产品（商业、服务）** | `references/methods/jobs-to-be-done.md` |
| **需要打破常规思维/寻找类比** | `references/methods/analogy-and-blending.md` |

### 第四步：处理歧义与矛盾情况

- **存在多条合理路径** → 选择最符合用户原文表述的路径。切勿为了显得高明而选择最有趣的方法。
- **确实存在歧义** → 只询问一个澄清问题，切勿擅自猜测。例如：“您是在构思新想法，还是在已有的想法中做选择？” / “这是用于写小说、散文，还是其他类型的内容？”
- **不同信号相互矛盾**（例如“奇特的创业点子”——产品领域 + 奇特的情绪需求） → **明确组合使用两种方法**。需说明所采用的方法：*"针对产品框架使用`jobs-to-be-done`方法，同时用`lateral-provocations`方法打破常规思路。"*
- **没有匹配到合适方法** → 采用约束分配机制（`references/full-prompt-library.md`）作为安全备选。
- **同一问题被重复提出** → 更换使用不同的方法。方法的多样性能带来创意分布的差异。

### 防止默认模式检查（在生成内容前执行）

- 正准备输出“以下是5个想法：”或仅列出编号列表？→ 停下。先选择一种方法。
- 正准备采用通用的LLM式头脑风暴模式？→ 停下。先按照上述规则选择路径。
- 生成的成果看起来像未经路由处理的LLM会产生的内容？→ 路由失败，需重新处理。

默认的LLM模式正是该功能旨在替代的。若不经过路由流程就直接生成内容，就等于违背了该功能的设计初衷。更多边缘案例（如情绪信号、方法组合、反模式等）可参见 `references/heuristics.md`。

## 输出格式

对于采用约束分配机制的默认路径：

```
## Constraint: [Name] — from [Source]
> [The constraint, one sentence]

### Ideas

1. **[One-line pitch]**
   [2-3 sentences — what specifically is made, why it's interesting]
   ⏱ [weekend/week/month]  •  🔧 [stack/medium/materials]

2. ...
3. ...
```

对于其他方法，则需遵循该方法所规定的格式（TRIZ用于生成矛盾分析；OuLiPo用于生成受限文本；Oblique Strategies则输出一张应用卡片及后续步骤）。切勿强行将所有方法都套入约束模板中。

**无论采用何种方法，每组创意都需满足以下要求：**
- 明确标注所使用的方法。在“平庸地形”模式下，还需列出那些被你否决的显而易见创意。
- 为每个创意详细说明其具体运作机制，以及其潜在的失败模式、权衡因素，还有适用人群。唯有具备这样的深度，创意才能真正落地——注重实用性而非表面装饰。
- 至少要确定一个**可行型**创意——即当前即可着手实施、虽非显而易见但确实存在明确第一步的创意。其余创意可以朝着更奇特的方向发展，但这个创意必须是真正可操作的。切勿让整组创意都流于奇怪却不可行。

## 文件结构

- `references/full-prompt-library.md` — 约束库，按领域分类（通用、软件、物理、社会、列表）。当设置 SPECIFICITY=NONE 时使用的默认路径。
- `references/method-catalog.md` — 每种方法的一行概要说明及适用场景。
- `references/heuristics.md` — 针对边缘情况的扩展决策树。
- `references/anti-slop.md` — 防止创意平庸化的规则，需应用于所有输出结果。
- `references/exercises.md` — 定时练习任务（5分钟/30分钟/1小时/每日/每周）。
- `references/methods/` — 包含22种命名方法，每个方法对应一个文件，只需加载当前正在使用的方法对应的文件即可。

## 出处说明

约束调度核心功能改编自 [wttdotm.com/prompts.html](https://wttdotm.com/prompts.html)。各方法则源自相应方法文件中引用的原始资料。
