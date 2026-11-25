---
name: ziwei-xiaomeng
description: 紫微斗数独立分析 Skill。当用户提供出生时间（阳历/农历、时辰、性别）询问紫微斗数、紫微盘、命盘、十二宫、四化、大限流年、紫微合婚/合作盘时触发。基于 Yiqi 算法核心（vendored, MIT）确定性排盘（杜绝 LLM 自行排盘出错），支持紫微独立分析 / 多流派交叉印证 / 单文件 HTML 命盘海报三种模式。本 Skill 只做紫微斗数，八字分析请交给 bazi-xiaomeng。
version: 1.0.0
author: WorkBuddy
license: MIT
metadata:
  hermes:
    tags: [ziwei, 紫微斗数, purple-star, 命盘, 排盘, 四化, 大限, 流年, poster]
    related_skills: [bazi-xiaomeng]
---

# 紫微斗数独立分析 Skill（ziwei-xiaomeng）

## 定位

**纯紫微斗数**分析技能。与 `bazi-xiaomeng`（八字）明确分工：凡命主只问紫微、十二宫、四化、大限流年、紫微合婚/合作，用本 Skill；问八字/日主/用神，转 `bazi-xiaomeng`；两者都不混在一盘里。

设计目标——吸收两个开源项目的优点并组合：
- **bazi-ziwei-skill 的优点**：算法精准可验证（确定性排盘，不靠 LLM 猜）、分析有章法（流派分层 + 流年密度三档 + 置信度自评）、严谨安全（决策门 + 冲突明说 + 不替决策）。
- **Horosa 的优点**：流派深度（多四化流派可切换）、分歧点精细（大限跨度 / 天马 / 星集 / 三盘 / 闰月 / 晚子时 / 定年界线 / 火铃 / 空劫）、推运完整（大限 → 流时）、展示维度多（天地人三盘 / 格局本地化 / 长生标签层）。

本 Skill 把"bazi 的分析脑子"套在"经过验证的紫微排盘引擎"上，并吸收 Horosa 的流派/分歧点/推运/展示维度作为**分析层与配置层**（引擎目前固定一套通行·飞星基表，多流派在提示词里做交叉印证，见下文"流派与分歧点"）。

## 何时触发

- 用户给出生时间并问"紫微 / 命盘 / 紫微斗数 / 十二宫 / 四化 / 大限流年 / 看紫微盘"。
- 用户贴来紫微排盘软件（文墨天机风等）导出文本，希望深度解读。
- 问特定大限/流年的吉凶、紫微合婚/合作盘对比。

**不触发**：八字日主/用神（→ bazi-xiaomeng）、星座/塔罗/周公解梦/风水/姓名学。

## 必需输入

```
公历或农历日期 (YYYY-MM-DD)
出生时刻 (HH:MM, 24 小时制)
性别 (男/女)
```

若用户没给时辰，**必须主动询问**，不要默认子时。时辰决定命宫落点，影响全盘。
> 出生地可选（`--location 城市`）：做**真太阳时校正**（钟表时 + (经度−120°E)×4 分 + 当日均时差，±16 分内）= 真太阳时，并记录气候，提高命宫/身宫精度。紫微对时辰敏感，有出生地尽量问。

## 执行流程

### Step 0 — 决策门（开场必做）⭐

**问题：要看哪种紫微分析？**
> "我可以做四种紫微分析：
> 1. **紫微独立分析**（十二宫 + 大限 + 生年四化 + 流年 —— 长文输出）
> 2. **紫微多流派印证**（三合 / 钦天四化 / 飞星 / 河洛 四派交叉对账，冲突明说 —— 长文输出）
> 3. **紫微命盘海报**（单文件 HTML：天地人三盘 + 四化染色 + 长生/格局标签，可截图分享）— **待定/按需**：默认不主动出，用户明确要再单独给（文档已覆盖盘面信息，海报为可视化增强）
> 4. **紫微合婚 / 合作盘**（两份生辰 → 命宫互动 / 夫妻宫互看 / 四化禄忌冲 / 五行局互补 —— 长文输出）"

| 用户选 | 加载提示词 | 模板 | 输出 |
|---|---|---|---|
| 1 | `prompts/ziwei-prompt.md` | — | Markdown 对话回复 |
| 2 | `prompts/ziwei-prompt.md`（多流派印证分支） | — | Markdown 对话回复 |
| 3 | `prompts/ziwei-poster.md` | `templates/ziwei-poster.html` | `<name>-ziwei.html` |
| 3b | （分析结论 JSON，见下） | `templates/zonghe-poster.html` | `<name>-综合印证.html` |
| 4 | `prompts/ziwei-compare.md` | — | Markdown 对话回复 |

> 模式 3 也需要先排盘（Step 1）+ 让 LLM 输出结构化分析 JSON，再渲染。模式 4 需两人各排一盘（Step 1 跑两次）后用 `compare.js` 出对比事实，再组织长文。

#### 模式 3b — 综合印证报告海报（固定模板，任何盘通用）⭐

用户说"给我出个海报 / 综合报告 / 一张图看全"时，**统一用这个模板**（深色高对比，A4 纵向单文件 HTML）。板块固定：
表头（命格标签/评级/命主星/身主星/子年斗君/五行局）→ 基本信息 + 两盘主轴 + 三大优势/隐忧 → 命盘核心数据（格局/旺衰/调候/月令旺相/五行）→ 紫微十二宫盘（命宫朱框、身宫标记、当前大限金框、四化染色）→ 01 主轴印证 → 02 阶段时间轴 → 03 六维交叉 → 04 冲突清单 → 05 综合定论 → 06 置信度 → 免责声明。

```bash
NODE="C:/Users/Admin/.workbuddy/binaries/node/versions/22.22.2/node.exe"
cd scripts
"$NODE" ziwei.js --year=2002 --month=8 --day=3 --hour=22 --minute=0 \
  --gender=male --location=邯郸 --json > zw.json
"$NODE" render-zonghe.js --chart=zw.json --output=<name>-综合印证.html \
  --year=2026 [--analysis=analysis.json] [--meta=meta.json]
```

**两类内容分工（别混）：**
- **事实层自动填**：四化、十二宫星曜、大限、命身宫、五行局、命主/身主星、子年斗君、真太阳时 —— 全部由 `ziwei.js` 数据推出，**不用手写、不准手改**。
- **分析结论层要你填**：主轴、优势/隐忧、时间轴判读、六维交叉、冲突清单、综合定论、置信度 —— 引擎不产出，靠 `--analysis` 注入；**不传则显示"（待分析）"占位，绝不许臆造填满**。

`--analysis` JSON 完整契约（**照这个字段名写，别自己发明**）：
```json
{
  "baziAxis":  "八字主轴一句话（紫微单盘时可留空，会显示占位）",
  "ziweiAxis": "紫微主轴一句话",
  "strengths":  [{"t":"优势标题","d":"说明"}],
  "weaknesses": [{"t":"隐忧标题","d":"说明"}],

  "mainConclusion": "01 主轴印证结论，整段文字",

  "timeline": {
    "marks": [{"trend":"up|flat|down","note":"节点判读","current":true}],
    "conclusion": "02 阶段时间轴的印证结论"
  },

  "sixDim": {
    "dims": ["事业","财运","婚恋","子女","六亲","健康"],
    "rows": [{"bazi":"八字观点","ziwei":"紫微观点","verdict":"yes|no|partial","fused":"融合结论"}]
  },

  "conflicts": [{"point":"冲突点","bazi":"八字视角","ziwei":"紫微视角",
                 "impact":"high|mid|low","advice":"建议"}],

  "final": {
    "axis": "终极主轴（短句）",
    "nodes":     ["关键节点1","关键节点2"],
    "risks":     ["高风险窗口1","高风险窗口2"],
    "leverages": ["优势放大1","优势放大2"],
    "advice":    ["行动建议1","行动建议2"]
  },

  "confidence": {
    "bazi":"高|中高|中|中低|低", "baziScore":"依据说明",
    "ziwei":"…",               "ziweiScore":"…",
    "consistency":"…",         "consistencyScore":"…",
    "stability":"…",           "stabilityScore":"…",
    "note": "置信度总说明（会覆盖默认免责语）"
  }
}
```

> **字段别名（模板已做归一化，两种写法都吃）**：`axes:{bazi,ziwei}` 等价于 `baziAxis/ziweiAxis`；
> `strengths/weaknesses` 里的 `{title,desc}`、`{name,text}` 都等价于 `{t,d}`，纯字符串数组也接受；
> 顶部「三大隐忧」未给 `weaknesses` 时回落读 `risks`。**但 `final.risks` 是 05 段的"高风险窗口"，与顶部隐忧不是同一处，别混。**
>
> ⚠️ **交付前自查**：渲染完必须搜一遍产物里还有几处「（待分析）」。若你本意是填满却仍有残留，就是字段名写错了（最常见：把 `final.axis` 写成 `verdict`、把 `confidence` 写成 `{overall,items}`）——回来对照上表改，**不要靠编内容把页面填满**。

`--meta` 可传 `{name,title,subtitle,grade}` 覆盖表头标题与评级（`grade` 如"上中"）。

> **本 skill 只排紫微**，故八字四柱盘/大运/流年段自动隐藏，核心数据区改显五行局与命身主星并标注"见合参"。要八字+紫微双盘全版海报，走 `hecan` skill 的同名模板。

### Step 4 — 合婚 / 合作盘（仅模式 4）

需要**两人**的生辰（各自按 Step 1 必需输入）。流程：

```bash
cd <skill-root>/scripts
NODE="C:/Users/Admin/.workbuddy/binaries/node/versions/22.22.2/node.exe"
NODE_PATH="C:/Users/Admin/.workbuddy/binaries/node/workspace/node_modules"
# 两人各排一盘
"$NODE" ziwei.js --year=<A年> --month=<A月> --day=<A日> --hour=<A时> --minute=<A分> --gender=<A性别> --output=A.json
"$NODE" ziwei.js --year=<B年> --month=<B月> --day=<B日> --hour=<B时> --minute=<B分> --gender=<B性别> --output=B.json
# 出对比事实（--mode=marriage 合婚 / cooperation 合作）
"$NODE" compare.js --a=A.json --b=B.json --mode=marriage --output=cmp.json
```

把 `cmp.json` 交给 `prompts/ziwei-compare.md` 组织成合婚/合作分析长文。

### Step 1 — 排盘（算法层，产出 JSON + 文本盘）

**绝对不要让 AI 自己排紫微**。调用脚本：

```bash
cd <skill-root>/scripts
NODE="C:/Users/Admin/.workbuddy/binaries/node/versions/22.22.2/node.exe"
NODE_PATH="C:/Users/Admin/.workbuddy/binaries/node/workspace/node_modules"
# 基础：紫微 JSON
"$NODE" ziwei.js --year=1990 --month=3 --day=15 --hour=10 --minute=30 --gender=male --output=zw.json
# 文本盘（喂给 LLM 分析用）
"$NODE" ziwei.js --year=1990 --month=3 --day=15 --hour=10 --minute=30 --gender=male --text > zw.txt
# 有出生地：真太阳时经度校正
"$NODE" ziwei.js ... --location 北京 --text > zw.txt
# 多流派（--school 见"流派与分歧点"；默认 standard 通行·飞星）
"$NODE" ziwei.js ... --school zhongzhou --text > zw.txt
# 流运推运（--at 指定问事时刻算流月/流日/流时，默认=系统当前时间）
"$NODE" ziwei.js ... --at=2026-08-10 --qhour=15 --text > zw.txt
# 逐年流年事实表（前事逐年 + 未来四维度 五维交叉底座，对齐 bazi liunian.py/events.py）
"$NODE" liunian_ziwei.js --year=1990 --month=3 --day=15 --hour=10 --minute=30 --gender=male --from=2015 --to=2035 --output=liunian.json
```

脚本输出（含本次扩展）：
- `zw.json`：紫微-only 结构（`meta` 含公历/农历/四柱/阴阳/五行局/geo/流派；`mingGong`/`shenGong`；`sihuaSummary` 生年四化；`gongs` 十二宫含主星/辅星/生年四化/**长生十二神(changsheng)**/大限/流年/**流年四化落宫(liuNianSihua)** + **流月/流日/流时四化落宫(liuYueSihua/liuRiSihua/liuShiSihua)**/**当前流运宫标记(isLiuNian/Yue/Ri/Shi)**；`current` 含当前流运链 大限→流年→流月→流日→流时 及各级四化）。
- `zw.txt`：文墨天机风文本盘（含长生、当前流运链）。
- `liunian.json`：逐年流年事实表（`liunian_ziwei.js` 产出），含每年 流年宫位/流年四化/大限落宫/神煞引动宫，是「前事逐年推算」与「未来四维度」五维交叉的事实底座（对齐 bazi 的 `liunian.py`/`events.py`）。

> 海报"天地人三盘"：本命盘（天）星曜与宫名原始；大限盘（地）以**当前大限宫**为新的命宫重锚十二宫名（星曜不移动，只移宫名，紫微运盘标准画法）；流年盘（人）以**流年宫**为新命宫重锚。三盘共用同一组星曜落点。

> **硬约束**：排盘交给确定性算法（Yiqi core，vendored MIT）。纯 LLM 排盘会错排命宫→身宫→大限→四化，全链失真。算法层不可绕过。
>
> **重要**：紫微斗数与八字是两套完全不同的体系（详见 `references/ziwei-vs-bazi.md`），本 Skill 只按紫微的"星曜落宫 + 四化飞化"逻辑看盘，绝不混入八字的"日主五行生克/十神/用神"语言。

### Step 2 — 分析（按 Step 0 选择）

读取对应提示词，喂入 `zw.txt`，输出 Markdown 长文（模式 1/2）；或喂入 `zw.txt` 让 LLM 输出严格 JSON（模式 3，见 `prompts/ziwei-poster.md`）。

### Step 3 — 海报（仅模式 3）

```bash
cd <skill-root>/scripts
"$NODE" render.js --chart=zw.json --analysis=analysis.json \
  --template=../templates/ziwei-poster.html --output=<user-name>-ziwei.html --currentYear=2026
```

把生成的 HTML 路径告诉用户，浏览器打开即可；LLM 只产数据（analysis.json），视觉由模板决定。

### Step 5 — 复盘检查（交付前必做）⭐

生成分析/报告后、**交付用户前**必须自查一遍，对应"最后复盘检查才能交付"：
1. **排盘基础核对**：真太阳时/晚子时/定年界线（若用 quanshu）/起运年龄/宫位 dizhi 已确认；命宫/身宫/大限无误。
2. **五维交叉到位**：前事逐年与未来窗口的每条断语都来自「宫位+主星庙陷+四化+长生+神煞」交叉，且标注「推算」/带证伪条件；无泛化套规则、无空话。
3. **神煞/格局/星情/庙陷/长生/辅星有出处**：神煞查过 `references/shen_sha_ziwei.md`、**格局须先跑 `scripts/pattern_detect.js` 确定性识别**（再对照 `references/geju-database.md` 看破格/细则，禁止凭印象漏判格局）、星情查过 `references/star_traits.md`（含 §2.1 令东来逐星化曜 + §2.2 陈希夷原赋口诀 + **§2.3 中州派陆斌兆/王亭之 per-star 化曜，三源互补**）、**飞星派飞化/来因宫解读查 `references/baipai_feihua.md`**（来因宫取法、生年四化=质、禄因忌果、飞宫八大理则、**§九 三合派宫干飞四化应用**）、**长生十二神查 `references/changsheng.md`**、**辅星/杂曜星情查 `references/aux_stars.md`**、**四化入宫象义查 `references/sihua_into_gong.md`**、**空宫借星查 `references/konggong.md`**、**大限小限查 `references/daxian_lunduan.md`**、**流月流日查 `references/liuyue_shizhen.md`**、**星系组合查 `references/star_traits.md` §4**、**自化各宫象义/应期三层四化查 `references/baipai_feihua.md` §四/§十一**、**庙陷读 zw.json 的 `mainStarsMiao` 或查 `references/miaoxian.md`**（禁止凭印象估庙陷），不凭印象；模式4 合婚/合作须查 `references/heming.md`。
4. **流派声明一致**：分析所用流派与 `meta.school` 一致；多流派印证模式已显式列各派结论与冲突处理。
5. **双轨自查**（若已出小白版）：零术语、关键结论标红、前事+未来+性格外貌+家人关系四节齐全、未来表含「方面」列且四维度+学业事业婚恋各至少一行。
6. **免责声明**已附。
> 任一项不达标，先补正再交付，绝不带缺交付。

7. **忠实性核查（参考 horosa faithfulness eval · 与 bazi 环节9 同款闸）**：逐条过本场断语——
   - **星曜/宫位/四化都在事实层**：每条断语引用的主星/辅星/四化落宫，都来自 `zw.json`/`zw.txt` 事实底座，无凭空捏造（如说"命宫紫微"但 zw.json 命宫无紫微则删）。
   - **无偷换流派**：所引断语与声明的 `meta.school` 一致，多流派印证模式已显式列冲突处理（关键约束4）。
   - **未替用户决策**：投资/择偶/医疗/堕胎等给信号不给指令（关键约束7）。
   - 任一项不达标 → 先补正再交付。

## 流派与分歧点（配置层 + 部分引擎级，已做实差距）

`--school` 可切换六派：**standard 通行·飞星**（默认）/ quanshu 全书系 / zhongzhou 中州派 / beipai 北派·通用飞星 / feixing 飞星派 / toupai 透派。

各派差异分**三个层次**，本 Skill 如实落地，不假装"星曜全变"：

- **① 引擎级（真正改盘，已落地）**：
  - **定年界线** `yearBoundary`：默认 `lichun`（立春分界，命理年柱标准）；`quanshu` 全书系设为 `spring`（正月初一为界）。对"春节后—立春前"出生者，两套年干/生年四化**实盘不同**（如 1990-02-01：立春界=己巳年、春节界=庚午年，四化随之重排）。这是六派间唯一会产生不同星盘的组合。
  - **晚子时** `midnight`：代码路径存在（`school.midnight==='late'` 会重排命身宫），但 **SCHOOLS 预设表全为 `early`，当前任何 `--school` 都不会触发晚子时**——实际所有 preset 都走早子时。需晚子时须引擎另加参数（如 `--midnight=late`），非预设能力。
- **② 星曜主体各派一致**：除①外，十二宫星曜落点、生年四化基表（按年干 禄/权/科/忌，所有流派通用且正确）**不因流派改变**。宣称"中州派盘"与"飞星派盘"星曜位置相同，差异在解释框架而非盘面。
- **③ 分析层（提示词切换）**：天马基准、星集、三盘、天伤天使、闰月、火铃（三合/南派）、空劫命名，以及各派推演重点（飞星派重自化飞化、中州派重星性赋义、北派重河洛理数）——由 `prompts/ziwei-prompt.md` 按所声明流派切换解释框架。

> 诚实声明：本 Skill 不虚构"某派专属安星诀"。多流派印证的价值在**同一星盘下四化串联/赋义/分歧点的不同结论对账**，而非渲染出不同星图。用户选某派时，须明说采用的是该派框架，不偷换成另一派断语。

## 推运深度（大限 → 流时，已完整）

- **大限**：十年一步，含起止年龄/宫位（顺逆随阴阳男女）。
- **流年**：流年地支宫 + 对应年龄 + 流年四化（按流年天干）。
- **流月 / 流日 / 流时**：已补全。默认取**系统当前时间**作为问事时刻，或 `--at=YYYY-MM-DD --qhour=H` 指定。`ziwei.js` 按"正月(寅月)入流年宫顺行→流月；初一入流月宫顺行→流日；子时入流日宫顺行→流时"起例，并用 lunar-typescript 取该时刻月/日/时干支，算出各级四化落宫，标记在 `current` 与宫位 `isLiuNian/Yue/Ri/Shi` 上（海报同步高亮）。
- **长生十二神**：按日干落宫算「长生/沐浴/冠带/临官/帝旺/衰/病/死/墓/绝/胎/养」，已接出至每宫 `changsheng` 字段与海报。

> 流月/流日/流时四化为"当年/当月/当日/当时"动态四化，与"生年四化"是两个层次，分析时务必区分（如问某月财运看流月财帛宫+流月四化，不混淆生年四化）。

## 关键约束

1. **装好不自检**：不要主动跑示例排盘 / smoke test / 分析示例命主。等用户给生辰再工作。
2. **决策门必做**：先问模式，避免无意义 token 消耗与输出截断。
3. **排盘必须走算法层**：禁止徒手排命宫/四化/大限。
4. **流派要声明**：用哪派四化、哪套分歧点，结论里明说，不偷换。
5. **冲突明说**：多流派印证时矛盾结论要讲清谁优先、为什么，不和稀泥。
6. **置信度自评**：旺衰临界、格局模糊、流派对立，必须标"置信度：低"。
7. **不替用户决策**：投资/择偶/医疗/堕胎等给信号不给指令。
8. **命盘外变量隔离**：不引入风水、姓名、阳宅等命盘没有的变量（紫微专注星盘）。
9. **敏感拒答**：下蛊、断人财路、害人命运等违禁内容直接拒绝。
10. **免责声明**：每次输出末必带"仅供文化研究与娱乐参考"。
11. **复盘检查必做**：交付用户前的分析/报告，必须按 Step 5 复盘检查逐项自查，任一项不达标先补正再交付，绝不带缺交付（对应"最后复盘检查才能交付"）。

## 文件清单

```
ziwei-xiaomeng/
├── SKILL.md                      本文件
├── scripts/
│   ├── ziwei.js                  排盘入口：生辰 → 紫微 JSON / 文本盘（含 --location 真太阳时）
│   ├── render.js                 JSON + 分析 → 单文件 HTML 海报（天地人三盘 + 流运四化）
│   ├── render-zonghe.js          ⭐ziwei.js JSON → 综合印证报告海报（固定模板，事实自动填/结论 --analysis 注入）
│   ├── compare.js                两份 zw.json → 合婚/合作对比事实 JSON
│   ├── liunian_ziwei.js          逐年流年事实表：出生盘一次取数 → 逐年 流年宫/四化/大限/神煞引动（前事逐年 + 未来四维度 底座）
│   ├── pattern_detect.js        格局自动识别：zw.json → 吉格/凶格/中性清单（移植 renhuai patterns.ts 逻辑，确定性事实识别），分析先用它避免漏判格局
│   ├── scan_feihua.js            飞星派来因宫追溯：zw.json → 飞化全表(来因宫→飞入宫) + 化忌来因宫（解厄关键），飞星派分析必读
│   ├── selftest.js               自检：11 项回归（排盘/四化表锁/庙陷锁/合婚/流年表/海报…），改知识库/引擎后先跑它
│   ├── city_climate.json         45 城市经纬度 + 1/7 月均温（真太阳时/气候校正）
│   └── engine/                   Yiqi core（vendored, MIT）+ lunar-typescript 依赖解析
├── prompts/
│   ├── ziwei-prompt.md           紫微独立/多流派印证 分析提示词
│   ├── ziwei-poster.md           紫微海报 分析 JSON 输出提示词
│   └── ziwei-compare.md          紫微合婚/合作盘 分析提示词
├── templates/
│   ├── ziwei-poster.html         紫微命盘海报模板（天地人三盘占位符）
│   └── zonghe-poster.html        ⭐综合印证报告海报模板（数据驱动，__CHART_DATA__ 占位；与 hecan 共用同一份）
├── references/
│   ├── index.md                  ⭐ 参考库总索引（问题→查哪个文件 / 按文件查用途 / 按脚本查用途 / 分析纪律速记），断盘前先查此导航
│   ├── ziwei-reference.md        流派/分歧点/宫位/四化 参考（**2026-08-27 重写对齐 ziwei.js 真实能力**：长生/流月流日流时/格局识别/合婚 均已实现；--school 仅切定年界线+晚子时路径存在但无 preset 触发；SIHUA_BY_GAN 固定不随学派换）
│   ├── ziwei-vs-bazi.md          紫微斗数 vs 八字：看盘方向/细节差异（与 bazi-xiaomeng 分流依据）
│   ├── geju-database.md          常见格局库（名称/条件/破格规则，已逐字核对《大德山人·紫微斗数精成》格局概论），声明格局须查此库
│   ├── shen_sha_ziwei.md         神煞库（红鸾/天喜/天姚/天马/天魁/天钺/禄存/文昌/文曲/羊陀火铃/空劫/天刑 + 已补孤辰/寡宿/咸池/华盖/龙池/凤阁 落宫主象 + 引动用法 + 与 bazi 对照；其余次要杂曜见 aux_stars.md），分析须查此库
│   ├── changsheng.md             长生十二神解读库（本命长生落宫义 + 流年博士/岁前/将前十二神参考；源自大德山人《精成》☆47-50），读 changsheng 字段时查
│   ├── aux_stars.md              辅星/杂曜属性字典（佐曜吉辅/凶煞/杂曜 五行·化气·庙陷·性质·与他星配合；源自大德山人《精成》☆16-50，补 shen_sha 未覆盖的辅曜），写辅星须查此库
│   ├── sihua_into_gong.md        四化入十二宫系统象义表（化禄/权/科/忌 × 命·兄·妻·子·财·疾·迁·友·官·田·福·父 逐宫象义全表；陈希夷全书+大德山人+共识），写四化入宫论断必查
│   ├── konggong.md               空宫（无正星）借星专章（借对宫规则/庙旺随原宫/四化借入/折扣原则/十二空宫组合/断不准边界；大德山人☆15），空宫论断必查
│   ├── daxian_lunduan.md         大限与小限论断章（起运=五行局数/顺逆以 ziwei.js 引擎为准/小限算法/大限叠原局/破格损格；大德山人第10章），断运限必查
│   ├── liuyue_shizhen.md         流月/流日/流时方法论（斗君起正月/流月顺布/流日一日一宫/流时一时辰一宫/闰月处理；大德山人第10章），定应期到月日必查
│   ├── star_traits.md            星曜特性字典（十四主星五行特性+十二宫位主管，倪海厦天纪蒸馏移植；§三 四化本义+五行已逐字核对《紫微斗数全书》；§3.2 主表+§2.1 令东来逐星释读+§2.2 陈希夷原赋口诀/化曜问答+§2.3 中州派 per-star 化曜（陆斌兆/王亭之）+ **§4 星系组合系统表（紫微星系六组+其他主星固定组合，陆斌兆《星曜性质讲义》）** + **§5 十八星辰分男女（飞星派取用神：男星9/女星8/廉贞化禄男化忌女）** 六层互补闭环——**古籍原赋缺口已闭合**），写星情须查此库
│   ├── baipai_feihua.md          飞星派（北派）+ 三合派 双轨方法论：来因宫/生年四化=质/禄权科忌人事物三分/自化离心向心 + **§四 自化系统象义表（北派河洛《止观录》理论锚定：生年(质)/自化(量)、离心出散向心入聚、自化象态分类八类、同类离心=破象；附自化禄权科忌各宫象义共识查表）**/飞宫八大理则/禄因忌果/飞宫法象生年/忌星棋谱 + 宫干飞四化应用（大德山人三合派 事因事体定位/各层力量差异）+ §十 白派飞宫进阶（四化分组AD/BC跟随/六阳六阴富贵论+破格损格/河图同宗同源/洛书交感+气数位）+ **§十一 应期三层四化叠加（生年→大限→流年→流月 时序框架/叠加信号/实战步骤）**。飞星派飞化解读必查（强化 scan_feihua.js 输出语义）
│   ├── heming.md                 合婚/合作知识库（双宫联参、天作之合、五步法、缘分类型、婚期三层法、各宫结婚、克夫/克妻标志、事业合作、兼容性速判★级、倪师名言、婚姻辅助星评分；移植自 renhuai heming-knowledge.ts，中-高可信度），模式4 合婚/合作分析必查
│   ├── topic_diagnosis.md        专题论断方法论（五大专题入手点 婚姻/财运/事业/健康/六亲 + 专题聚焦规则 单宫/运限/四化 + 每宫证据结构 + **六、补强专题 学业考试/迁移出国/官非诉讼/灾厄意外 4 专项**；**白派飞宫深化已并入**：婚姻(夫妻宫坐生年四化定基调+来因宫定婚期)、事业(官禄/财帛四化+生年禄位置+媒介论职业)、灾厄(疾厄/子女/迁移交感+自化定大运时间点) + §5 分男女取用神联动；综合 tasky 五大专题框架 + Brhiza 聚焦引擎逻辑 + 大德山人凶灾应期 + 白派飞宫论职业/婚姻/伤灾，属方法论非断语库），写专题报告必查
│   ├── miaoxian.md               庙旺利陷查表（十四主星×十二地支 庙/旺/地/利/平/陷，以《紫微斗数全书》为准，含辅煞），断"星有没有力"须查此表或读 zw.json 的 mainStarsMiao
│   ├── anxing_jue.md            安星诀全集与排盘自查卡（全套安星诀 文昌文曲/左右/魁钺/天马/禄存/羊陀/火铃/四化/空劫/天伤天使/太岁杀禄/刑姚/三台八座/哭虚/龙池凤阁/台辅封诰/长生/红鸾/丧门白虎/斗君/天德月德/截路空亡/大限 + 安身命/十二宫序/起五行寅例 + **排盘自查卡：真太阳时/晚子时/闰月/夏令时/engine 输出核对**，覆盖原清单⑪），排盘/核对引擎必查
│   ├── star_quickref.md         星曜属性总表（速查）：十四主星 + 辅星/杂曜 的 五行·阴阳/南北斗·化气·庙陷要点 一张表，避免反复翻多文件；详查仍回各专库
│   ├── schools_overview.md       流派用法总纲：飞星(北派)/三合/中州/白派 四家定位与擅长 + 何时用哪家 + 交叉验证与冲突收口（主星庙陷+四化本性定夺，置信度标定），分析前定流派口径必读
│   └── geo-tiaohou.md            ⚠️ 八字模块误置（属 bazi-xiaomeng 地理调候），紫微不用——紫微 --location 只取经度做真太阳时校正，不读其气候温度；保留以免误删，分��层勿引用
└── evals/evals.json             验证案例（排盘一致性回归）
```

## 依赖与运行

- 运行时：Node.js ≥ 18（建议用托管 Node `C:/Users/Admin/.workbuddy/binaries/node/versions/22.22.2/node.exe`）。
- 依赖 `lunar-typescript` 已装入托管 Node workspace，经 `NODE_PATH=C:/Users/Admin/.workbuddy/binaries/node/workspace/node_modules` 解析；若报模块缺失，运行：
  ```
  cd C:/Users/Admin/.workbuddy/binaries/node/workspace
  npm install lunar-typescript
  ```
- 算法核心 Yiqi 已 vendored 在 `scripts/engine/`，离线可用。

## 失败模式

| 现象 | 原因 | 处理 |
|---|---|---|
| 排盘脚本报错 | 日期超范围 / 时辰格式错 | 询问用户校正 |
| AI 想"凭记忆排盘" | 偷懒 | 拒绝，算法层不可绕过 |
| 输出被截断 | 长文超 token | 回到决策门拆分输出 |
| 与用户其他软件结果不一致 | 流派/分歧点差异 | 按采用的流派与 `notes` 解释，不偷换 |
| 模块缺失 lunar-typescript | NODE_PATH 未设 | 设 NODE_PATH 或重装依赖 |

## 免责声明（每次输出末必带）

> 本分析基于传统紫微斗数理论框架，仅供文化研究与娱乐参考，不构成医疗、投资、婚姻、法律等任何决策依据。命运由个人选择与客观环境共同塑造。
