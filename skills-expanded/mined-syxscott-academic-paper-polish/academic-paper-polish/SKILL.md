---
name: academic-paper-polish
description: 学术论文写作、润色、改稿与投稿的全流程助手。10 个模块覆盖摘要、引言、文献综述、研究方法、结果、讨论、结论、期刊匹配与投稿、审稿意见回复、去 AI 化终稿润色。内置地学 SCI 写作与投稿的硬规则：期刊结构硬约束（GCA/ES&T/PPP 的 Results-Discussion 分离vs合并、有无独立结论段）、引言倒金字塔与 opening-resolution 对齐、引文密度表、讨论六步框架、结论局限句式、综述 18 步、图表硬参数（300dpi/<10MB/<180mm/禁对角线缩放）、图件设计体系（图序/五种原型/语义色字典/图注模板）、送审三段流程、参考文献五误区、审稿回复四要素。触发词：写论文、论文写作、论文润色、SCI、投稿、返修、审稿意见、文献综述怎么写、review paper、cover letter、期刊要求、GCA、ES&T、PPP、Earth-Science Reviews、制图规范、图件要求、配色方案、图序怎么排、图注怎么写、J. Micropalaeontology、JM、混淆矩阵画法、Highlights、行号、论文自查、降低AI率、去AI化、论文结构、文献检索、关键词怎么选、微体古生物、放射虫、有孔虫、系统描述论文、新种描述、Holotype、Paratype、类群怎么描述、图版 Plate、Micropaleontology、化石照片怎么排、introduction 怎么写、discussion 怎么写、论文结构怎么排、讨论部分怎么写、
引言有几种写法、讨论骨架、Remarks 怎么写、类群块标签、系统描述模板、
研究问题式引言、结论怎么编号。
license: MIT
metadata:
  author: syxscott
  version: "2.16.1"
  source_material:
    - "论文写作方法论骨架：章节写法、综述流程、投稿与返修"
    - "格式硬参数与文献检索实操：图表规范、引文密度、送审流程、时间预算"
---

# 学术论文写作与润色全流程

覆盖从选题到返修的完整链路。**不是模板，不是填空，是给 LLM 的角色定义 + 约束 + 输出规范。**

## 何时使用

- 「帮我润色一下论文摘要 / 引言 / 讨论」
- 「我要投 X 期刊，需要注意什么」
- 「审稿意见怎么回复」
- 「文献综述怎么组织结构」
- 「这张图合规吗 / 参考文献怎么排序」
- 「怎么降低 AI 率」

不适用：纯文献检索（用检索工具）、数据统计分析、英文写作（先英化再用）。

---

## 🔴 铁律 0：先定期刊，再动笔

**这一步决定后面所有结构决策。** 不是流程形式。

| 期刊 | Results/Discussion | 结论段 | 收录边界 |
|---|---|---|---|
| **GCA** | 🔴 **必须分离**，各自独立编号 | 允许 | ❌ 不收纯方法学/技术/模型论文；❌ 不收 regional case studies；Cover Letter 必推荐 3 位副主编 |
| **ES&T** | 🔴 **合并**为 R&D | ❌ *"A separate conclusion is not to be used"* | Research Article 限 **7,000 词** |
| **PPP** | — | — | Articles **5000–7000 词 / 4–8 图**；图单栏 **<85 mm** / 双栏 **<180 mm** |
| **Paleobiology**<br>★化石/古生物方向，规则最细 | — | — | 送审图 **<40 兆像素**；终稿 **线条 1200 / 半调 600 / 组合 800 dpi**；单栏 9 cm / 双栏 18 cm / 最大高 24 cm；🔴 **须提供 Non-technical Summary + Abstract 各 ≤300 词**；全稿 **12 号 TNR + 双倍行距 + 连续行号**；**Ga/Ma/ka = 年代，Gyr/Myr/kyr = 跨度** |
| **Acta Palaeontologica Polonica** | — | — | 图件参数最精确：单栏 **89 mm** / 双栏 **183 mm** / 最大长 **237 mm**；**Calibri 8 pt**；线宽 **0.2 mm**；照片 **400 dpi**；🔴 **ZooBank 强制注册** |
| **Palaeontologia Electronica** | — | — | 🔴 **无页限、无版面费**；图宽 **175 mm / 84 mm**，**300 ppi**，**RGB 不用 CMYK**；🔴 文件名 **ISO 9660**（≤8 字符，仅小写/数字/`_`/`.`）；须提供 plain language summary |
| **J. Micropalaeontology**<br>★ 微体古生物（Copernicus 平台） | — | — | 图 **300 dpi**、**单图 <5 MB / 全文件 <30 MB**、**图宽 ≥8 cm**；🔴 **复合图必须合并成单文件**；🔴 **图例必须画在图里**（不许靠图注解释虚线/空心圆）；🔴 须过 **Coblis 色觉模拟器**；矢量优先（eps/pdf，字体须嵌入）；单栏版心 177 mm |
| **PalZ** | — | — | Systematic Palaeontology：分类单元名**粗体**，authority **加逗号**（与 Paleobiology/APP 系相反），同义名列表**隔行缩进** |
| **Micropaleontology** | — | — | 微体古生物专业刊；🔴 图件标签用 **"TEXT-FIGURE"** 而非 "Fig."；地质图用**黑白花纹 + 插图定位图 + 比例尺 + 指北针** |
| **Earth-Science Reviews** | — | — | **IF 11.3**（2026-11 官方刊页）；只发综述 |
| **Biological Reviews / Chemical Reviews / Nature Reviews** | — | — | **IF > 14 / > 50 / 46–123** |

> 🔴 **格式不过关，直接拒稿 —— 走不到学术编辑和审稿人那一步。**
> 原因：① 第一印象 ② 基本学术素养 ③ 评审是挑错过程 ④ 格式意见往往比内容意见多

详见 `references/journal-constraints.md`。

> 🔴 **期刊硬规则一律用官方原文**：`references/` 里每条期刊硬约束都附**官方英文原句**，
> 中文只作定位标注，**转述不算数**。回答时**直接引原句**，不要用中文概括代替 ——
> 转述会丢强度词（required / encouraged / must / may）并凭空造出原文没有的要求。

---

## 模块索引

| # | 模块 | 一句话定位 | 中文 | English |
|---|---|---|---|---|
| 01 | 📝 摘要 | 把整篇压缩进 300 词 | `prompts/01-abstract.md` | `prompts-en/01-abstract.md` |
| 02 | 🔭 引言 | 倒金字塔 · 缺口 · 路线图 | `prompts/02-introduction.md` | `prompts-en/02-introduction.md` |
| 03 | 📚 文献综述 | 让文献"对话"而非罗列 | `prompts/03-literature-review.md` | `prompts-en/03-literature-review.md` |
| 04 | 🧪 研究方法 | 经得起同行复现 | `prompts/04-methods.md` | `prompts-en/04-methods.md` |
| 05 | 📊 结果 | 只讲"发现了什么" | `prompts/05-results.md` | `prompts-en/05-results.md` |
| 06 | 💡 讨论 | 结果 ↔ 文献 ↔ 理论 ↔ 局限 | `prompts/06-discussion.md` | `prompts-en/06-discussion.md` |
| 07 | 🎯 结论 | 升华但不引入新信息 | `prompts/07-conclusion.md` | `prompts-en/07-conclusion.md` |
| 08 | 🤖 去 AI 化 | 终稿通篇润色 | `prompts/08-deai-polish.md` | `prompts-en/08-deai-polish.md` |
| 09 | 🎯 期刊匹配与投稿 | 先定期刊再动笔 | `prompts/09-journal-submission.md` | `prompts-en/09-journal-submission.md` |
| 10 | 💬 审稿意见回复 | 逐条答复的四要素 | `prompts/10-reviewer-response.md` | `prompts-en/10-reviewer-response.md` |

> 🌍 **英文用户**：直接读 `prompts-en/` 对应模块 —— 每个文件**自包含**（含所需硬规则与期刊数字），
> 单文件复制进任意 LLM 即可用，无需先读 `references/`。英文入口见 `docs/PROMPTS-EN.md`。


**推荐顺序**：`① 期刊匹配(9) → ② 写/润色正文(2-7) → ③ 返修回复(10) → ④ 终稿去 AI 化(8)`

### 快速调用

```
读取 prompts/02-introduction.md，按其中的规则帮我润色引言：【粘贴初稿】
```

---

## 🔴 八条硬规则（跨模块通用）
### 1. 引言 = 倒金字塔，且 opening 必须与 resolution 对齐

| 图形 | 英文 | 后果 |
|---|---|---|
| 开口 > 收口 | *overpromising* | 读者觉得被欺骗 |
| **开口 = 收口** | ***on target*** | ✅ 认可 |
| 收口 > 开口 | *underpromising* | 读者看不到值得关注的 story |

### 2. 引文密度（最易自查的一张表）

| 章节 | 引文要求 |
|---|---|
| **Introduction** | 除**问题句和过渡句**外都要有引用 |
| **Results** | **几乎没有**引用 |
| **Discussion** | **每段 5–8 句** = topic sentence + **3–4 句带引用** + **2–3 句自己数据** |
| **Abstract / Conclusion** | **不应出现**引用 |

> ⚠️ 以为多引他人工作会降低原创性，**实际效果常常相反**。不充分引用 → 审稿人**至少会认为你阅读文献不够**。

### 3. 段落：5–8 句最合理

**1–2 句话的段落是非常差的结构。** 换了对象主体就分段 —— 一段集中讲清一个问题。

### 4. 讨论必须走完六步（含"局限性"）

```
① 引言空白 → ② 重述发现(用数据/图) → ③ 解释并与他人比较
→ ④ 表明局限性 → ⑤ 对以后研究的启示 → ⑥ 结论
```

### 5. 结论要含"局限性 + 未来方向"

```
Despite its advantages, the [方法名] also has some limitations.
First, [限制1]. Second, [限制2].
Further research should focus on [方向].
```

### 6. 措辞分寸

| ❌ 避免 | ✅ 改用 |
|---|---|
| *for the first time* | 直接陈述与前人工作的差异 |
| "首次提出 / 首次发现 / 国际先进水平" | 只陈述客观增量 |
| *The deficiency of Wang's approach is…* | *However, the mechanism has not been fully understood.* |

### 7. 参考文献五误区

**知而不引 · 断章取义 · 引而不确 · 来源不实 · 盲目自引**

综述约 **100 篇**是质量标志；优先近 5 年（最好 1–3 年）、优先一次文献。

### 8. 🔴 地质年代：Ga/Ma/ka ≠ Gyr/Myr/kyr

地学论文最常见的形式错误，两个方向都要查：

| | 表示什么 | 例 |
|---|---|---|
| **Ga / Ma / ka** | 🔴 **年代（dates）** | 距今十亿 / 百万 / 千年 |
| **Gyr / Myr / kyr** | 🔴 **时间跨度（duration）** | — |

- **upper / middle / lower** → 岩石或时间地层单位；**early / late** → 时间单位
- **仅正式 ICS 时间单元**才大写 Early / Middle / Late
- 界线用 **/**，时间范围用 **–**（en-dash）
- 规范依据：**ICS 年代表**（stratigraphy.org/chart）与 **ICS Guide**（stratigraphy.org/guide）
- ⚠️ *"Middle Cretaceous"* 不规范 → 用 *Upper/Lower Cretaceous*，或作形容词时 *mid-Cretaceous*

---

## 🔴 技术检查卡口（这层不过直接拒稿）

### 图表硬参数

| 项 | 要求 |
|---|---|
| 格式 | TIFF / JPG |
| 🔴 **分辨率** | **300 dpi 至少** |
| 🔴 单图 / 总文件 | **<10 MB / <50 MB** |
| 图中字体 | Arial、Helvetica、Times New Roman |
| 图宽度（双栏刊） | 单栏 **<85 mm** / 双栏 **<180 mm** |
| 线条粗细 | **0.25 与 0.5 mm 组合** |
| 字号 | **10&6** 或 **12&8** 组合；🔴 严禁 <4 号 |
| 图注 | 🔴 **只看图注就能把图看明白** |
| 表名 | **写在表上** |

**🔴🔴 Word 铁律**：**从制图 → 导出 → 插入 Word，全程严禁拉对角线或等比例缩放！**

**🔴 版权红线**：严禁直接复制已发表的图（除 OA/获许可）；改后必标来源；**不使用有政治分歧的地图**。

> ⚠️ 上表是**通用 / 地球化学方向**的参数。**若投 *Paleobiology*（古生物 / 化石形态学），参数不同**：
> 线条图 **1200 dpi** / 半调图 **600** / 组合图 **800**；单栏 **9 cm**、双栏 **18 cm**、最大高 **24 cm**；
> 线条 ≥**0.3 pt**、字号 ≥**8 pt**；🔴 **标本照片必须带比例尺，不可用 ×40 等放大倍数代替**；
> 🔴 送审图须 **<40 兆像素** 才能进 PDF proof。
> 详见 `references/paleobiology-journal.md`。

### 排版

**12 号字 + 双倍行距 + 连续行号 + 页码**

*Paleobiology* 另要求：**US Letter 纸张、四边 1 英寸、不用两端对齐、不在右边界断词**。

详见 `references/figure-specs.md` 与 `references/paleobiology-journal.md`。

---

## 🔴 图件设计体系（图序 → 原型 → 语义色）

**硬参数只管「能不能过」，这一层管「读者看不看得懂」。**

### 1. 图序即论证顺序

```text
方法图 → 数据/对象图 → 模型性能图 → 误差案例图
→ 一致性图（换 3 种量纲各来一次：绝对量 / 相对量 / 群落结构）
→ 生态/业务意义图 → 成本/效率图
```

🔴 **「一致性」至少三个量纲** —— 只给一个，审稿人必问「换成相对比例呢」。
🔴 **每张图只回答一个问题**；同一方法的对比图**全篇只用一对颜色**。

### 2. 五种图件原型

| 原型 | 干什么 | 必备元素 |
|---|---|---|
| **A 流程图** | 系统全景 / 成本分解 | 🔴 箭头颜色必须有语义**并写进图注**；框体写「动词+对象」；标注人的动作 |
| **B 图像对照版** | 展示对象与误差案例 | 🔴 纯黑/纯白底；**比例尺**（不用放大倍数）；物种名斜体；面板字母粗体置左上 |
| **C 性能矩阵** | 混淆矩阵 / 评估表 | 🔴 **单色阶**（禁彩虹）；深浅格**文字自动反色**；图上方写 accuracy + precision |
| **D 成对比较** | 新旧方法 / 两条件对照 | 🔴 **跨所有图不变色**；1:1 参考线用**虚线**；背景色带只表类别并单列图例 |
| **E 回归/排序** | 定量一致性与群落结构 | R² **写在左上角**；统计标注给 **点估计 + p 值**；排序图用**多形状**承担类别 |

### 3. 语义色字典（实测，非目测）

| 角色 | HEX |
|---|---|
| 人工 / 基准 | `#D30203` |
| AI / 自动 | `#75489A` |
| 单一系列散点 | `#F6A100` |
| 环境量验证 | `#308E2C` |
| 拟合线 / 单色阶 | `#093576` → `#00509D` |

🔴 **同一色相全篇只承载一个含义**。
⚠️ 蓝本论文把颜色语义**写进了正文**（"manual (red) versus automated (purple)"）——
**颜色语义要进正文，不能只写在图注里**。

详见 `references/figure-design-system.md`（14 图逐图拆解、版式规范、图注模板、交稿自查表）。

---

## 🔴 微体古生物 / 放射虫论文的写作与制图模式

**这个领域的图不是彩色的，章节也不是通用 SCI 模板。**（依据：本地语料 8162 篇的分层抽样统计）

| 事实 | 样本量与口径 |
|---|---|
| 🔴 **93% 的图是灰度**（376 张嵌入图），图内平均饱和度中位数 = 0.000 | 40 篇抽样 |
| 🔴 图注前缀是**多语种**的：Fig.(1219) / Figure(257) / Рис.(163) / Таблица(170) / 图 / 图版 / Abb.(34) / TEXT-FIGURE | 4035 条多语种图注（v2.15.0 重抽） |
| 🔴 **65%（101/156）的论文没有独立 Discussion 段** | 156 篇逐字精读笔记（v2.15.0 横切统计） |
| 地质体用**黑白花纹**，不用颜色 | Micropaleontology 实刊 |

🔴 **三条推论（写微体古生物论文时照用）**：
1. **分组用形状 / 灰度 / 花纹，不是颜色** —— 轴和位置已经用掉信息通道，
   形状与灰度才是剩下的通道（见 `references/color-system.md` 的"一通道一变量"）
2. **展示分类单元形态 → 图版 Plate；展示分布 / 关系 / 趋势 → Fig.**
3. **借用与改造的图，必须在图注里写来源**：From X / Slightly modified from X /
   modified from X (year) / Original.

详见 `references/micropaleo-paper-patterns.md`（四类主题的章节骨架、图注面板字母体系、
地质图制式、图版规则、前置要素实测覆盖率、交稿自查表）。

> 🆕 **v2.15.0 新增两份实证文件**（读到这一节时按需加载）：
> - `references/figure-conventions-evidence.md` —— **图件制图实证**：449 张渲染图实看。
>   核心：**比例尺 vs 放大倍数按刊分**（Palaeo 3P/Pal J/QSR 用比例尺条；Geologica Carpathica/
>   Micropaleontology/Revue de micropaléontologie 只写 × magn.）；图注前缀多语种词汇表（实测 4035 条）；
>   图版说明四种制式；表格表注符号体系；Elsevier 彩色图强制话术。
> - `references/fulltext-reading-evidence.md` —— **全文逐字精读实证**：181 篇分层随机样本。
>   核心：章节链五类骨架、Methods 三档详略、**Discussion 四拍结构**、Conclusion 两种形态、
>   **短篇三种讨论形态**、引言六种起手、类群块跨语种模板。
> - `references/ai-ml-paper-patterns.md` —— **方法类（AI/数据）地学论文的写作实证**：
>   第二批语料（225 篇「AI × 分类学」专题 PDF，A 组 50 篇化石+AI **逐字精读**）。
>   🔴 **描述类与方法类骨架不可混用**：Geological setting / Repository / Systematic 在描述类
>   几乎必选、在方法类 **0/50**；而方法类有独立 Results **46%**、Discussion **48%**、
>   Conclusion **52%**、Data availability **54%**（27/50）、Code availability **24%**（12/50）。
>   另含：声明块五种逐字写法（Zenodo/OSF/机构库/补充材料/录用后提供）、数据集交代六件、
>   模型交代五种粒度、基线三种强度、混淆矩阵与特征空间图、结论的「适用边界」段。
>   **v2.16.1 追加 §九**（8 个分片 31 篇横向观察交叉统计，合并口径）：
>   混淆矩阵 **45.8%（11/24，不是「标配」）**、独立超参表 **9.5%（2/21）**、
>   统计检验 **16.7%（5/30）**、训练曲线 **13.6%（3/22）**；
>   局限自陈**七种句式**、可解释性图件**三条路线**、标注方式**四种**、划分比例**十二种写法**、
>   文件名误标**全量清单（9 例完全不符 / 225 = 4.0%）**、声明块机器层 vs 人工层**口径差**。
>   ⚠️ §九 对 §4.2 / §5.1 / §3.1 / §8 第 3 条四处表述给出**口径更正**（见 §9.2），引用时一并读。

### 🔴 系统描述类论文（写新种/新属）专章

**这类论文的"讨论"不在 Discussion 段，而在每个类群块的 Remarks 里。**（v2.15.0：164 篇分层随机样本逐字精读实测）

| 环节 | 实测写法 |
|---|---|
| 章节链 | INTRODUCTION → [Geological setting] → [Material & methods / **Repository**] → **Systematic description**（逐类群并列小节）→ [Discussion 常缺省] |
| 类群块标签 | **A 完整型** synonym→diagnosis→description→remarks→occurrence／**B 标准型** material→description→occurrence→remarks→diagnosis→holotype／**C 度量型** remarks→description→material→holotype→paratype→remarks→occurrence／**D 度量短文型** description→measurements→occurrences→remarks／**E 目录式** type species→original diagnosis→diagnosis→age and location→taxon code→status→remarks |
| **属 / 目 / 科级标签**（与种级不同） | 目级 **definition→range→origin**；科级 **type genus→diagnosis→occurrence**；种级 **type species→diagnosis→description→etymology→type→measurements→comparison** |

| **Remarks 三种模板** | 四步：**吻合**（fit well the descriptions）→ **差异点**→ **分类处置**（must be placed in the Genus …）→ **与他人处理不同**／同义五步：判定→原区分点→**差异归因**→模式标本复核→结论／**待观察特征清单**（定种不足时列出还缺哪些形态部件） |
| 必备 | **Holotype / Paratype**（新属还要 **Type Species**）、**Repository**（**单列一节 或 写在系统描述段第一句**）、**Occurrences**（逐产地） |
| 图版说明 | **放大倍数制**（× 175：图号. 分类单元名 + 命名人 + 时代缩写 + 标本号 + (× N)）或**图版引用制**（Plate 3.1, figure 7） |
| 命名 | 属级标题带命名人与年代（Genus X Author, 19xx）；种名斜体；记号 sp. nov. / cf. / aff. / ex gr. / emend. |

详见 references/micropaleo-paper-patterns.md 第十章（含 17 条系统描述类交稿自查）。

### 🔴 本领域的 Introduction / Discussion 写法与通用模板不同

> 🔴 **方法说明与口径（不夸大）**：① 第一轮 **130 篇只做骨架扫描**（抽章节名、段落数、图注格式），
> **不构成逐篇精读**；② 第二轮 **17 篇通读 Introduction / Discussion / Conclusions 连续散文全文**
> （≈21.6 万字符：引言 16 篇、讨论 7 篇、结论 6 篇；另 1 篇 PDF 文本层抽取失败，不计入）。
> **不是词频统计** —— 关键词出现率只能证明"某个词出现过"，**不能**证明"作者在这里做了什么论证动作"。
> v2.10.0 曾用命中率下结论，v2.11.0 起作废；v2.12.0 的"48 篇可读引言逐段读"口径**已于 v2.14.0 作废**
> （那一轮引言只摘了首句、目的句、末句三处）。**每条结论都附论文名与逐字原文**。
> 🔴 **结论强度分级（务必先看）**：references/fulltext-reading-evidence.md §12 ——
> 本 skill 的结论分 A/B/C 三级；**94% 的刊只有 1 篇样本**，「某刊用 X」属 C 级，
> 只能写「在本样本 N 篇中观察到」，不得写成刊规或领域规律。所有百分比必须带分母与语种限定。

> 🆕 **v2.15.0 重做**：旧样本另有两个缺陷（抽取器 dict 覆盖同名章节导致正文重复计数；
> 旧"130 篇"取自按文件大小升序的清单，实为全语料最小的 130 篇）。已重抽**分层随机**样本 181 篇
> （种子 20261103、**不按大小排序**），其中 **164 篇逐字读完**，正文约 570 万字符；
> 图件另渲染 449 张 PNG 由 5 组**实际打开看图**。详见 `references/fulltext-reading-evidence.md`。

| 环节 | 本领域实际写法 | 与通用 SCI 模板的差别 |
|---|---|---|
| Introduction 首句 | **给事实**（放射虫是什么 / 材料何时何地发现），不是"本文做了什么" | 模板通常开门见山说目的 |
| Introduction 结构 | 🔴 **没有统一模板**，实测**八种并存**：A 缺口→目的 ｜ B 必要性论证 ｜ C 教科书铺陈 ｜ D 材料发现 ｜ E 铺垫→目的→新意声明 ｜ **F 地质背景前置** ｜ **G 综述—反例（But…）** ｜ **H 编号问题式**。**按体裁选** | 模板只给一种 |
| 目的句 | **独立成句**，实测**十类句式**（aim / purpose / goal / objective / It is the purpose of… / In this work we… / We present here… / **Therefore, …（推理式）** / **否定式划边界** / **Our study focused on…**）；**必须带具体对象与产地** | 模板通常把目的句放第一句 |
| 引言长度 | 🔴 **17 篇全文通读实测 1,712–12,184 字符**（中位约 7.6k），无规范；短引言多见于数据报告与短通信 | 模板给固定字数 |
| 新意声明 | 目的句后**另起一段**说明"为什么值得看"（"of particular interest as …"） | 模板无此动作 |
| 缺口写法 | **具体或数量化**（"only 19 occurrences in the entire Phanerozoic"、"哪个层没研究过"） | 模板爱用空泛的 "remains unclear" |
| 局限坦陈 | **材料/数据局限可写在引言里**（"incompletely exposed"） | 模板要求藏到方法或讨论 |
| Discussion 首句 | **直接进入比较对象 / 用标志性种锁定时代 / 证据→推论**，三种起手并存 | 模板教你在开头重述结果 |
| Discussion 主体 | **逐项对照**（按形态类型、属种一项一项比）+ **"Because …, we propose that …"** 显式焊合证据与推论 | 模板强调逐条罗列文献 |
| Discussion 起手 | 实测**十三种**，常用：比较对象型 / 标志性种定年型 / 结论先行 / 否定排除 / 让步 / 复述目的 / 子标题+综述铺陈 / 子标题+结合已发表数据 / 数据→推断 / 结果陈述 / 自承不完整 / **竞争假说二选一** / **已知事实+从未有人做过** | 模板只给"重述结果"一种 |
| Discussion 收尾 | 实测**八种**：让步限定 / "需要进一步研究" / 归因 / 地层陈述 / 审慎推测 / 否定限定 / 结论重述 / **方法缺陷自陈** —— **没有一种是"未来展望"** | 模板要求展望未来 |
| 讨论骨架 | **三种可抄骨架**：甲 逐项对照 ｜ 乙 **反常→可能原因→坦承未决（并指名缺哪类数据）** ｜ 丙 **已有说法→本文新证据→结论** | 模板只给逐条罗列 |
| 引言 ↔ 结论 | **引言末尾用编号问句列研究问题，结论按同编号逐条回答**（Can → can 镜像） | 模板无此配对 |
| 章节必备 | **Geological setting 几乎必选，且排在 Methods 之前**；系统描述类**没有独立 Results 段**；老刊常把 Results 与 Discussion 合并 | 模板要求标准 IMRaD 五段 |
| 中文 / 日文稿 | 章节对应词：**提要**=Abstract、**地質概説/地质概况**=Geological setting、**考察**=Discussion、まとめ=Conclusions；中文刊常**没有引言节**，直接以地质概况起头 | 模板默认五段 |

---

## 送审流程

| 体裁 | 流程 |
|---|---|
| SCI 论文 | 技术检查（格式）→ **学术编辑（期刊符合度）** → 审稿人 |
| 学位论文 | 组内导师 → **校外评审** → 校内评审 |

---

## 时间预算

一篇期刊文章（4–8 图 + 5000–7000 词）≈ **6–8 周**
```
每周 1–2 个图 + 每天 2–3 句（约 15 词/句）
= 每 3 天一个图，每天 3 句话 = 两个月一篇
```

⚠️ 仿写句子练手可以，但**连续 5 个字相同 = 抄袭；不标注引用 = 抄袭嫌疑**。

---

## 🔴 去 AI 化的红线

| ❌ 不能做 | 原因 |
|---|---|
| 改动数据、单位、图表编号 | 学术不端 |
| 把"结论 A"改成"结论 B" | 改变科学主张 |
| 加未经证实的推测并写成事实 | 学术不端 |
| 为降重而删关键引用 | 知而不引 |

**目标不是"过检测"，是"读起来像人写的、且信息密度高"。**
部分期刊要求声明 AI 使用情况，按目标期刊要求处理。

---

## 参考文件

| 文件 | 内容 |
|---|---|
| `references/checklist.md` | 投稿前自查清单（A–J 十组，可打印） |
| `references/journal-constraints.md` | 期刊结构硬约束 + 体裁篇幅 + 引文密度 + 送审流程 |
| `references/figure-specs.md` | 图表硬参数 + 构图 + 版权红线 + 版式范例 |
| `references/color-system.md` | ★ **配色系统与视觉编码** —— 对照冷/处理暖、色相编码主变量、连续色阶、红绿禁忌、灰度检验 |
| `references/figure-design-system.md` | ★ **图件设计体系** —— 图序即论证顺序、五种图件原型、实测语义色字典、版式规范、图注模板、交稿自查表 |
| `references/figure-conventions-evidence.md` | ★ **图件制图实证（v2.15.0）** —— 449 张渲染图实看：比例尺 vs 放大倍数按刊分、图注前缀多语种词汇表、图版四种制式、表格表注符号体系、Elsevier 彩色图话术、交稿自查 |
| `references/fulltext-reading-evidence.md` | ★ **全文逐字精读实证（v2.15.0）** —— 181 篇分层随机样本的章节链实测、Methods 三档详略、Discussion 四拍结构、Conclusion 两种形态、短篇三种讨论形态、引言六种起手、类群块跨语种模板 |
| `references/ai-ml-paper-patterns.md` | ★ **AI/ML 方法类地学论文的写作实证（v2.16.0，v2.16.1 追加 §九）** —— 第二批语料（225 篇「AI × 分类学」专题 PDF，A 组 50 篇化石+AI 逐字精读）：**描述类 vs 方法类骨架对照**、声明块实测频率与五种逐字写法（Data/Code availability）、数据集交代六件、模型交代五种粒度、评估指标实测、基线三种强度、混淆矩阵/ROC/特征空间等方法类专属图件、局限自陈三类写法、结论的「适用边界」段；**§九 横向观察交叉统计（31 篇合并口径）**：图件真实频率（混淆矩阵 45.8%、超参表 9.5%、统计检验 16.7%、训练曲线 13.6%）、局限自陈七种句式、标注四种 / 划分十二种 / 不平衡五种处理、文件名误标全量清单、声明块机器层 vs 人工层口径差 |
| `references/micropaleo-paper-patterns.md` | ★ **微体古生物 / 放射虫论文的写作与制图模式** —— 四类主题骨架、逐字精读的 Introduction/Discussion 写法（8 种引言模式 / 13 种讨论起手 / 8 种收尾 / 3 种讨论骨架 / 引言编号问题↔结论编号答案）、**系统描述类专章（类群块模板 A–E / Remarks 三种模板 / 图版两制式）**、Fig. vs 图版、灰度优先、面板字母体系、地质图制式、来源声明 |
| `references/paleobiology-journal.md` | ★ *Paleobiology* 全刊规范（图件 + 文体 + 数据可用性）+ 官方原文速查 |
| `references/multi-journal-style-guides.md` | ★ **10 份官方 style guide 汇总**（ESR / Nature / PNAS / CVPR / Palaeoworld / APP / PE / PalZ / Elsevier 微体古生物系 / JM）+ 横向对比与选刊建议 |
| `references/literature-search.md` | 检索工具 + 关键词尺度 + 素材库积累 + review proposal |
| `references/论文写作方法论骨架.md` | 写作方法论全篇：章节写法、综述流程、投稿与返修 |
| `references/格式硬参数与文献检索实操.md` | 格式硬参数全篇 + 文献检索实操 |
| `references/sentence-bank.md` | 句式库（引出不足 / 讨论动词 / 局限句式 / 回复审稿人） |
| `docs/COMPATIBILITY.md` | 各 AI 工具兼容性矩阵与安装路径 |
| `docs/PROMPTS-EN.md` | 英文版 prompt（English version of the 10 modules） |