---
name: anima
description: Anima 模型提示词编写技能。当用户需要为 anima 模型编写提示词（提供角色形象 + 服装 + 剧情 + 规则，要求生成提示词 md 文件用于 batch_webui 批量生成）时使用。也用于修改/优化已有的提示词 md 文件。触发词：提示词编写、提示词组、anima 提示词、写提示词、束缚提示词、剧情提示词、镜头提示词、批量提示词。
---

# Anima 提示词编写

## Overview

面向 AI 图像生成的**提示词编写技能**：根据用户给出的角色形象、服装、剧情与硬性规则，编写结构化的提示词 md 文件，供批量图像生成工作流（如 WebUI batch）直接导入使用。每条提示词是一个独立的「镜头」，按行组织为标签组（质量前缀 / 动作镜头 / 表情 / 角色 / 服装 / 场景 / 风格）。

编写全程以技能自带的参考库与语料数据为依据，不凭空造标签：
- **标签取用**：`references/tag-library.md`（动作/镜头/表情/场景精选库）与 `references/tag-library.csv.md`（2069 条补充词库）
- **组合套路**：`references/corpus-stats.md`（905 份好图反推提示词的实测共现数据）——表情-动作-分镜按数据配套
- **结构与范本**：`references/structure-guide.md`（分幕/服装渐进/体位递进/视角/情绪弧方法）、`references/examples.md`（镜头式/束缚集/故事版三套范本）
- **格式规范**：`references/format-rules.md`（批量导入解析格式）

产出文件默认写入 `F:\ai\ComfyUI-aki-v3\任务\`（或用户指定位置）；参考素材包括 `F:\ai\ComfyUI-aki-v3\动作\` 各系列参考文件（如束缚动作镜头参考）与 `动作_all.txt`。

## 工作流

### 步骤 1：解析需求

从用户输入中提取五要素：

1. **角色标签**：英文 danbooru 标签串（如 `1girl, kafuu chino, blue hair, long hair, blue eyes, small breasts, x hair ornament`）。角色标签贯穿所有提示词组，禁止删改。
2. **服装**：英文标签串，注意可能有多套服装（如 Luka 要求中的官方服/水手服/睡衣/全裸）。
3. **剧情**：中文叙述的故事情节，需拆解为连续的场景序列。
4. **硬性规则**：
   - 前缀（若未指定，默认 `masterpiece, best quality, very aesthetic, score_7, score_9, sensitive, ultra detailed,`）
   - **无阴毛强调**：pussy/groin 可见的镜头（含特写）正向写 `no pubic hair`（或 `no female pubic hair`）强调无毛，常与 `clear pussy` 同组使用（acid 任务实证）；正面阴毛标签（pubic hair, female pubic hair, male pubic hair）一律不写
   - 体液要求（常见：爱液/尿液透明无色 `transparent pussy juice, clear love juice`；精液清澈 `clear cum` 仅 1–2 词；pussy 可见镜头统一加 `clear pussy`）
   - **不打码**：提示词不添加任何打码标签（censored、mosaic censoring、bar censor 等一律不写）
   - 数量要求（每组数、总组数上限，如「共 68 组 ≤70」）
   - 其他（背景虚化、服装透明隐约可见等）
5. **参考要求**：用户可能要求参考特定文件（如束缚动作镜头参考.md）或对既有文件迭代修改。

若用户未给前缀或某类规则，使用默认值并**在交付时明确说明**。

### 步骤 2：结构设计（写码前先规划）

设计原则：**结构服从用户需求，深度个性化，不套固定模板**。先明确用户的剧情线、服装套数、组数上限与硬性规则，再设计整体结构；写码前先检索参考库与既有成品范本，选最贴合需求的结构模式，再按剧情与角色定制细节（服装阶段、体位顺序、情绪节奏等）。

结构模式（常用套路，按需求选配，可裁剪组合，不必全用）：
1. **分幕**：剧情完整时按剧情推进划分幕次（如「第一幕：图书馆」「第二幕：楼梯间舔阴」），每幕一个场景与服装阶段；纯展示/单场景需求可不分幕。
2. **服装渐进**：多套服装或脱衣剧情时，按幕配服装阶段（全装 → 掀衣 → 脱裙 → 脱上衣 → 只剩袜子 → 全裸），进入新阶段**删除上一阶段已脱衣物的标签**，保留角色锚点（如发饰）；必要时建立「服装渐进式去除对照表」。单套服装或无脱衣要求时不强制。
3. **体位/动作递进**：同一体位/动作通常按 前戏 → 过程 → 高潮 → 事后 写多组（每组不同表情与动作），或按程度递进（如传教士：正常 → 拉腿 → 分腿 → 压腿 mating press → 抱紧深插）；具体组数按用户数量要求分配。
4. **多视角**：按动作类型选最合适视角——第一人称 POV（性爱场景首选，见 corpus-stats.md）、俯视 from above、仰视 from below、侧面 from side、背后 from behind、裙底 upskirt low angle、正面 from front；不必每组分不同视角。
5. **情绪弧**：有剧情时表情与动作随剧情连续变化（害羞尴尬 → 快感 → 兴奋 → ahegao 高潮 → 失神余韵 → 平静），情绪节奏按剧情定制。

**写码前先检索参考**：① 既有成品范本（`F:\ai\ComfyUI-aki-v3\任务\` 下各 md：如 镜华.md 68 组镜头式、Luka束缚提示词.md 125 组按服装分套、kinomoto_sakura_校服_100.md 校服系列 100 组、守岸人五套服装提示词.md 10 组每套 2 镜头、hinatsuru_ai_医疗调教提示词.md 等）；② `references/structure-guide.md`（方法论与服装渐进对照表范例）；③ `references/examples.md`（镜头式/束缚集/故事版三套风格）；④ `references/corpus-stats.md`（70 个套路簇：表情-动作-分镜配套数据）；⑤ `references/closeup-guide.md`（特写镜头编排：动作-分镜-表情三件套与六类部位模板——要求加入特写时仿照此文件编排）。从中选最贴合需求的结构并深度个性化。

### 步骤 3：编写提示词组

每个镜头按「七段式」组织，每段一行（换行保留，WebUI 原样导入）：

```
masterpiece, best quality, very aesthetic, score_7, score_9, sensitive, ultra detailed,   ← ① 质量前缀
动作标签, 体位标签, 镜头标签, 视角标签, focus 标签,                                          ← ② 动作+镜头
表情标签,                                                                                    ← ③ 情绪（4–6 个）
1girl, 角色标签,                                                                             ← ④ 角色（主镜头全程保留；下半身/局部特写按 closeup-guide.md 裁剪画外标签，只留 1girl+角色名锚点）
服装标签（当前阶段）,                                                                        ← ⑤ 服装
场景背景标签, depth of field, blurry background,                                             ← ⑥ 场景+背景虚化
（⑦ 风格：默认省略不写；仅当用户明确指定画风时才追加，如 manga, japanese anime style；kawaii anime style 只在用户明确要求可爱画风时使用）
```

规则：
- 标签库从 `references/tag-library.md` 取用，不用自造标签。
- **每组必须配表情标签**（4–6 个），主镜头与特写都要配。表情按「情绪阶段 × 动作场景」搭配，以 `references/corpus-stats.md` 实测共现数据为准（v0.3 方法），从 `references/tag-library.md`「组合套路」取配——不套固定模板、不硬凑维度，选最能表现当前动作状态的词：
  - 前戏 / 抗拒 / 羞耻：`shy, embarrassed, blush, nose blush, looking away, covering face, trembling` 等按场景组合；掀衣羞耻用实证组合 `clothes lift` + `blush, nose blush, embarrassed, looking at viewer`。
  - 快感 / 过程：基础四件套 `blush, open mouth, sweat, trembling`（blush+open mouth 共现 450 次，全局最高频）作通用基底；眼/嘴换词产生变化（half-lidded / teary eyes / closed eyes；lips parted / biting lower lip / heavy breathing）。
  - 高潮：`ahegao, rolling eyes, tongue out`，或 `symbol-shaped pupils, heart-shaped pupils`（sex 共现 66/62）+ `drooling`（shibari 共现 53）；后入体位最容易出 ahegao（共现 20/23）。
  - 束缚 / 强制：`trembling, tears, sweat` 三件套（bound 共现 138/117/117）+ `drooling / crying with eyes open / clenched teeth`；哭脸（crying/tears）配 `full body, cowboy shot` 全身展示。
  - 失神 / 事后：`dazed, glazed, empty eyes, afterglow, exhausted, heavy breathing`。
  - 视角配套：`pov` 配 `looking at viewer`（pov 与所有主要表情共现最高，性爱场景首选视角）；`looking down` 配 `from below`；`looking back` 配 `from behind`。完整配套表见 corpus-stats.md 四~八节，骨架套路见 tag-library.md「组合套路」。
- **表情质量与多样（软性要求，无死板配额）**：
  - 「眼 / 嘴 / 脸红 / 手部 / 整体状态」是取词池分组（tag-library.md 情绪/反应类），不是配额——同组不堆叠同维度近义词（眼：closed / half-closed 二选一；嘴：moaning / lips parted / open mouth 不并列），取最能表现当前状态的那个。
  - 相邻镜头、同一幕内轮换词表，避免同一标签高频重复——感到重复时从语料换同义有效搭配（blush → nose blush / full-face blush；open mouth → lips parted / biting lower lip；moaning → pleasure / heavy breathing / silent scream）。
  - 表情随情绪弧递进：害羞尴尬 → 快感 → 兴奋 → 高潮 → 失神余韵，前后镜头表情反映状态变化。
- **特写镜头**按 `references/closeup-guide.md` 编排「动作-分镜-表情」三件套（v0.5.2 数据版，源自 `F:\ai\素材\特写` 48 份好图反推）：部位焦点用 `xxx focus`（foot focus / pussy focus / breast focus / face focus / ass focus / solo focus 双人聚焦单人）；**画外标签全裁剪**（见下条），头部常用 `head out of frame` 裁出；配 `close-up / extreme close-up` + 语料实测视角（足部 from above+foreshortening、私处/掀裙 from below+upskirt+ceiling、背后 from behind）+ 手部动作细节（lifted by self / guiding hand / hand between legs / grabbing another's breast）。
- **画外标签裁剪（v0.5.2 实证铁律）**：腿脚/下身/孕肚等画面无上半身的特写（foot focus / pussy focus / head out of frame 类）必须同时裁剪**角色行**与**服装行**的画外标签——用户实测：角色行残留 `sidelocks / medium breasts / large breasts / cleavage / collarbone / solo` 或服装行残留头罩（white veil 等）/头饰/开襟 `center opening`/掀裙 `lifted to waist`/`off-shoulder`/`see-through`/内衣状态标签时，模型会被诱导把上半身转正朝镜头（如小腿特写画出胸部锁骨）。只保留：角色锚点（1girl+角色名）+ 基衣名 + 画面内服饰（鞋履/袜子/腿部保护 `bare legs, no sign, no tattoo`/趾甲油）+ 有 pussy 的组保留 `bottomless, no panties`。
- **背后视角与表情池禁令（v0.5.2）**：from behind + facing away 的足部/小腿特写禁用 `spread pussy` / `pussy focus`（实测诱导模型转正身体面向镜头），改用隐约写法 `pussy, cleft of venus, pussy juice`；head out of frame 特写不得写面部朝向词（looking at viewer / looking away / looking down）——表情池同样会诱导模型画脸朝镜头（足部特写表情池禁用 looking at viewer）。
- **不打码**：任何提示词组（含特写）都不添加 `censored`、`mosaic censoring`、`bar censor` 等打码标签。
- 标签尽可能简约准确，避免同义词堆叠造成的词汇冲突（如已写 `spread pussy` 就不必再写 `spread legs` 的语义冲突组合；写 `on back` 就别写 `on stomach`）。
- 若要求「背景虚化」「服装透明」，每组补 1–2 个对应标签（`blurry background, depth of field` / `sheer fabric, translucent, see-through`）。
- 每个体位的主镜头标题写明情绪阶段，如「镜头 17 — 后入前戏（抗拒）」。

### 步骤 4：组装 MD 文件

严格遵循 `references/format-rules.md`（batch_webui README 解析规则）：

- 文件头：`# 标题` + `> 描述信息`（可选，含角色/场景/组数统计）。
- 按幕分节：`## 第 X 幕：幕名`。
- 每条提示词 = **`### 镜头 N — 标题`**（三级标题，不能用 `####`）+ **紧跟其后的 ``` 代码块**，标题与代码块之间不得有其他内容行。
- 代码块内容**必须以 `masterpiece` 开头**，否则 WebUI 标准模式解析不到。
- 标题与代码块之间允许空行，不允许说明文字。

### 步骤 5：校验

交付前运行校验脚本：

```bash
"F:\ai\ComfyUI-aki-v3\python\python.exe" "C:\Users\Administrator\.claude\skills\anima\scripts\validate_prompt_md.py" "<生成的md文件路径>"
```

脚本检查：`###` 标题数量、标题后是否紧跟代码块、代码块是否以 masterpiece 开头、是否有禁词（pubic hair 等）、是否有冲突标签。全部通过后再交付。

## 修改已有提示词文件

当用户要求修改已有 md（如「删去官方服装部分」「每套服装加刑具插入」「强化表情」）：

1. 读取现有文件，识别其结构（服装套数、每套组数、镜头编号规则）。
2. 按用户要求增删提示词组，保持原有编号体系或重排。
3. 新写的组遵循上述全部规则（尤其禁止标签与格式）。
4. 修改后同样运行校验脚本。

## Resources

- `references/format-rules.md` — batch_webui MD 文件格式规范（导入正则、正确/错误示例、提示词文本结构）。
- `references/structure-guide.md` — 结构方法论：幕次划分、服装渐进对照表、体位四阶段、程度递进、视角分配、情绪弧。
- `references/tag-library.md` — 动作/镜头/表情/场景精选标签库（源自 420 个 txt 动作文件的归纳），写提示词时按需取用。
- `references/tag-library.csv.md` — 补充词库（用户导出 2069 条，已排除马赛克/打码标签，覆盖身体部位、服饰、场景、角色属性、道具等 21 类），写提示词时按分类检索补充。
- `references/examples.md` — 优秀提示词组示例（镜华便利店、Luka 束缚、蓝发水手服故事三套风格）。
- `references/closeup-guide.md` — 特写镜头写作指南（v0.5.2 数据版，源自 `F:\ai\素材\特写` 48 份反推提示词 + 守岸人 160 组实证：动作-分镜-表情三件套编排、六类部位模板、画外标签裁剪规则、背后视角与表情池禁令），要求加入特写时仿照编排。
- `references/corpus-stats.md` — 真实语料统计分析报告（905 份好图反推提示词：分类频次、表情×动作×分镜共现表、70 个聚类套路簇），写组合套路时的数据依据。
- `scripts/validate_prompt_md.py` — 格式与禁词校验脚本。
- `scripts/analyze_prompt_corpus.py` — 语料统计 + 聚类分析脚本（IDF 加权余弦 + 互 kNN 图 + 贪心模块度 + 模拟退火细化），可用于分析新素材生成新报告。
- `scripts/gen_csv_library.py` — 将提示词库 CSV 重新转换为标签库参考文件的生成脚本（排除马赛克标签）。
