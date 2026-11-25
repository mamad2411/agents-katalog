---
name: humanizer
description: 去除 AI 味改写。中文金融/行业研究/尽调报告用正式审慎客观书面语；英文通用文本去 LLM 痕迹、恢复真人声音。中英规则统一。合并自 de-ai-ify-writing + humanizer。
trigger: writing
mandatory: true
auto_inject: true
---

# Humanizer — 去除 AI 味改写（中英通用）

> 本 skill 合并自 `de-ai-ify-writing`（中文金融/研报/尽调规范）与 `humanizer`（通用英文 34 pattern，port 自 [blader/humanizer](https://github.com/blader/humanizer)，MIT）。
> 完整 pattern 明细（含全部 before/after 例子）见 `references/humanizer-full.md`。

## 核心原则

**AI 痕迹 = 统计最可能补全，而非人写的判断。** LLM 输出趋向"最普遍适用的最可能结果"，由此产生一系列可识别的套话模式。改写目标：去掉这些模式，让文本像人写的——中文研报要正式、审慎、客观；英文通用文本要有真人声音、节奏和观点。

**使用流程：**
1. 读取输入文本（文件用 `read_file`）
2. 按下方清单识别 AI 模式
3. 改写问题段落，保留核心意思
4. 匹配目标语气（中文 = 正式审慎客观；英文 = 真人声音，有样本则对齐样本）
5. 终检：自问"哪里还能看出是 AI 写的？"，答出剩余痕迹，再改一遍
6. 展示改写结果（文件改动显示 diff）

---

## 一、判断必须有依据

所有判断必须基于事实、数据、公开资料、行业逻辑或可解释的推理链条。缺乏证据支撑的句子要弱化或删除。

**禁止（中）：**
- 自我辩护式："这不是推测"、"这并非空穴来风"、"我们不是在猜测"、"这不是主观判断"、"事实就是如此"
- 改为："基于现有公开资料，可以观察到……"、"从当前数据和行业趋势看，……"、"该判断仍需结合后续经营数据进一步验证。"

**禁止（英）：** 模糊归因/推诿词 —— Industry reports, Observers have cited, Experts argue, Some critics argue（无具体出处）；知识截止免责 —— "as of [date]", "Up to my last training update", "While specific details are limited..."

**改法：** 给判断补上具体出处和机制。"Experts believe it plays a crucial role" → "The Haolai River supports several endemic fish species, according to a 2019 survey by CAS."；"该技术路线可能重塑行业" → 说明影响的具体维度（成本、效率、收入、现金流、客户结构、竞争地位、供应链稳定性、政策约束）。

## 二、禁止夸大与情绪化

去掉夸张、煽动、绝对化、宣传式词汇。重要性问题用机制和数据展开，不用口号。

**禁止（中）** 夸饰词：精妙、惊人、极致、完美、颠覆性、革命性、无可替代、极具想象空间、爆发式增长、降维打击 → 改为：具备一定优势、表现出较强的适配性、在成本/效率/性能方面具有改善空间、相较同类方案具有差异化特征、可能形成一定竞争优势但仍需进一步验证

**禁止（中）** 绝对化：必然、注定、毫无疑问、唯一选择、不可逆、彻底改变、一定会、没有任何可能、必将重塑行业 → 改为：可能推动……、有望影响……、在一定条件下可能形成……、仍取决于……、需要结合后续市场反馈进一步观察

**禁止（英）** 意义膨胀（significance inflation）：stands/serves as, is a testament/reminder, pivotal/key role, underscores/highlights its importance, reflects broader, setting the stage for, evolving landscape, indelible mark；知名度膨胀：无上下文地罗列 "cited in NYT/BBC/FT..."

**禁止（英）** 宣传式语言：boasts a, vibrant, rich (figurative), profound, nestled, in the heart of, groundbreaking, breathtaking, must-visit, stunning；营销套话：at the end of the day, when it comes to, in a world where, moving forward, game-changer, navigate (challenges), lean into, unpack

**改法：** 平铺直叙事实。"Nestled within the breathtaking region... stands as a vibrant town with rich cultural heritage" → "X is a town in the Gonder region, known for its weekly market and 18th-century church."

## 三、禁止戏剧化句式

不要用转折、对立、悬念、排比来强化观点。

**禁止（中）** 二元对立："不是X问题，而是Y问题"类（不是"优化"是"生存"、不是"技术"是"战略"）→ 改为：
- "该问题已不再局限于X层面，其影响正在延伸至Y层面，主要体现在A、B、C等方面。"
- "从影响范围看，该问题不仅涉及X，还可能对Y产生约束，因此需要从A、B、C维度进行评估。"
- "该问题的核心不在于单一的X改进，而在于其对Y能力、成本结构、竞争地位或持续经营能力的影响。"

**禁止（英）** 否定平行结构："Not only...but...", "It's not just about X, it's Y"；句尾 dangling 否定碎片（"no guessing"、"no wasted motion"）；自问自答："What if...?", "The question is...", "Think about it." 然后立刻自答；三连排比（rule of three）强行凑三组；同义词轮换（protagonist/main character/central figure/hero）；伪范围（"from X to Y" 中 X/Y 不在同一量纲）。

**改法：** 直接陈述。"It's not just about the beat riding under the vocals; it's part of the aggression" → "The heavy beat adds to the aggressive tone."

## 四、不用引号制造强调

**禁止（中）：** 用引号强调概念（"优化""生存""革命性""护城河"）。
**禁止（英）：** 弯引号（"..."）替代直引号。

**改法：** 去掉多余引号，概念直接用正文表达。

## 五、精简冗余

去掉填充短语、口头禅、预告式开场、空泛结尾。

**禁止（中）：** 无。
**禁止（英）：**
- 填充短语："In order to" → "To", "Due to the fact that" → "Because", "At this point in time" → "Now", "has the ability to" → "can", "It is important to note that" → 删
- 句首口头禅："So...", "Look,", 句首 And/But、"I think"/"I believe" 陈述事实、副词开头（Interestingly, Importantly, Notably, Crucially, Essentially, Ultimately）
- 预告式开场："Let's dive in", "Here's what you need to know", "without further ado"
- 空泛正面结尾："The future looks bright. Exciting times lie ahead."
- 安抚收尾："And that's okay.", "There's nothing wrong with that.", "you're not alone"
- 过度对冲："could potentially possibly be argued that... might have some effect" → "The policy may affect outcomes."

**改法：** 删掉套话，直接给内容。"Let's dive into how caching works. Here's what you need to know." → "Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache."

## 六、主动语态与具体主语

**禁止（英）：** 被动语态/无主句隐藏施动者："No configuration file needed. The results are preserved automatically." → "You do not need a configuration file. The system preserves the results automatically."
**禁止（英）：** -ing 分词假深度：句尾 tacked-on 分词短语（highlighting..., ensuring..., reflecting..., symbolizing..., contributing to..., showcasing...）。

**改法：** 用 is/are/has 简单系动词，避免 "serves as / stands as / represents / boasts / features" 替代简单 is/has（copula avoidance）。

## 七、格式层面的 AI 痕迹（中英通用）

- **破折号滥用**：em dash (—) 比人写得多 → 改用逗号、句号、括号
- **加粗过度**：机械性加粗短语、行内标题列表（"- **User Experience:** ..."）
- **标题全词大写**：英文标题 "Strategic Negotiations And Global Partnerships" → sentence case
- **Emoji**：标题/要点加 emoji 装饰
- **标题后空转句**：heading 后跟一句复述标题的无信息开场
- **套式章节**："Despite its... faces several challenges...", "Challenges and Legacy", "Future Outlook" 模板段
- **连字符过度**：third-party, cross-functional, data-driven 等一律连字符——人写时通常不统一；少见或技术性复合词可保留
- **权威姿态套话**："The real question is", "at its core", "what really matters", "the deeper issue"
- **戏剧化碎片**：两三个词的无主句、staccato "X. And Y. And Z."、段尾金句
- **强行隐喻**：装饰性隐喻 + 立刻解释 → 删掉说直话

## 八、中文研报专用补充

### 推荐使用的正式表达方式
- "基于现有公开资料，可以观察到……"
- "从行业发展阶段看，……"
- "从供给侧看，……" / "从需求侧看，……"
- "从成本结构看，……" / "从竞争格局看，……" / "从商业化进展看，……"
- "该现象可能反映……"
- "其核心约束因素在于……"
- "主要影响体现在以下几个方面……"
- "该变化对企业的影响主要包括……"
- "仍需进一步验证的变量包括……"
- "短期来看，……；中长期来看，……"
- "在当前市场条件下，企业面临的主要挑战是……"
- "该判断的成立取决于……"
- "需要持续关注……的变化。"

### 口号式、媒体标题式表达
- 禁止：打开万亿市场空间、引领行业变革、重塑产业格局、开启新时代、打造第二增长曲线、抢占未来制高点、成为行业破局者
- 改为分析型："该市场仍处于持续扩容阶段，但实际增长空间取决于渗透率、价格水平和客户需求释放节奏。" / "该技术路线可能对现有产业链分工产生影响，但其扩散速度仍受成本、可靠性和客户导入周期制约。" / "公司正在拓展新的收入来源，但其对整体业绩的贡献比例和可持续性仍需观察。"

## 九、改写规则（中英通用）

1. 保留原文核心观点，不改变基本判断方向。
2. 删除情绪化、夸张化、戏剧化措辞。
3. 将强判断改为有条件、可验证、审慎的分析判断。
4. 将口号式表达改为机制分析。
5. 将抽象判断补充为具体影响维度。
6. 不新增未经支持的事实、数据或案例。
7. 如果原句缺乏证据支撑，应弱化表达（"可能""倾向于""仍需验证"等）。
8. **不修改格式、字体、字号、配色、标题级数**。
9. **不修改不属于上述范围的内容**——只针对 AI 味/营销味/口语化/戏剧化表达进行替换，其余原文保持不动。

## 十、灵魂与声音（英文通用文本）

去掉 AI 痕迹只是第一步。**干净但无魂**同样明显：句句等长、无观点、无不确定、无第一人称、无幽默、读起来像维基百科或新闻稿。

- **有观点**：陈述事实后要有反应（"I genuinely don't know how to feel about this one" 比中性罗列 pros/cons 更像人）
- **节奏多变**：短句 + 长句交替
- **承认复杂性**："This is impressive but also kind of unsettling" 优于单纯 "This is impressive."
- **合适时用第一人称**："I keep coming back to..."
- **允许一点乱**：离题、插入语、半成形想法
- **具体描述感受**：不说 "this is concerning"，说 "there's something unsettling about agents churning away at 3am while nobody's watching"
- **语音校准**：用户提供本人写作样本时，先分析句长模式、用词层级、段落开头、标点习惯、重复短语、过渡方式，然后对齐样本声音（用户写短句就别产出长句，用户用 "stuff" 就别升级成 "elements"）

## 十一、输出前自检

检查全文确保不存在以下问题：
- 是否出现"这不是推测"等自我辩护式表达
- 是否出现"精妙""惊人""颠覆性""革命性"等夸饰词；"testament"/"pivotal"/"underscores" 等意义膨胀
- 是否出现"不是X问题，而是Y问题"类戏剧化句式；"It's not just X; it's Y" / "Not only...but..."
- 是否使用引号强调概念；弯引号
- 是否存在"必然""唯一""毫无疑问"等绝对化判断
- 是否存在口号式、媒体标题式、营销式表达
- 是否有模糊归因（Experts argue, Industry reports）或无出处的引用
- 是否所有核心判断都有事实、数据、行业逻辑或推理链条支撑
- 是否有填充短语、预告式开场、空泛正面结尾
- 是否整体符合正式、审慎、客观的语气（中文）或自然真人声音（英文）

如发现上述问题，在输出前直接改写，不保留原句。

---

## Attribution

- 中文规范部分：用户自研（Hermes 项目）。
- 英文 pattern 部分：port 自 [blader/humanizer](https://github.com/blader/humanizer)（MIT，作者 Siqi Chen @blader，v2.5.1），基于 [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（WikiProject AI Cleanup 维护）。pattern 1-29 来自上游，30-34 及 pattern 7 的营销套话列表为 Hermes 增补。MIT 许可证见 `references/LICENSE-humanizer.txt`。
