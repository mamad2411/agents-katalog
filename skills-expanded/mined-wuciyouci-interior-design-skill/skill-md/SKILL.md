---
name: interior-design
description: "当用户需要室内设计方案、装修建议、AI生图提示词、空间规划、风格推荐或预算咨询时使用。覆盖28种风格+户型图驱动设计+AI生图提示词。含8条硬规则·参考GB 50096/GB 55031/GB 55038。Also triggers on: '室内设计' '装修' '家装设计' '全屋设计' '帮我做方案' '效果图' '室内AI生图' '装修预算' '户型图' '户型分析' '户型诊断' '帮我看看户型' '客厅设计' '卧室设计' '厨房设计' '卫生间设计' '风格推荐' '换风格' '灯光' '照明' '灯光方案' '光指纹' '灯槽' '反光灯槽' '暗藏灯带' '灯带' '吊顶灯' '无主灯' '间接照明' '洗墙灯' '悬浮吊顶' '见光不见灯' '横梁吊顶' '材质' '材料' '装修材料' '酷家乐' '家具尺寸' '搜家具' '白模转效果' '平面图转3D' '渲染效果图' 'Qwen-Image-2.1' 'Qwen 出图' 'Qwen 渲染'. Do NOT trigger on: 纯闲聊·建筑设计·园林景观·家具购买咨询。"
license: MIT — 免费开源·可自由使用/修改/分发
metadata:
  version: "7.2.0"
  author: 九尾
  tags: [室内设计, 原木风, 装修, 空间规划, AI生图, 酷家乐, 硬规则, 预算安全]
  platforms: [windows, linux, macos]
---

# 室内设计AI助手

> 架构：主文件只做路由与流程，细节知识全部下沉到 `skills/` 子 SKILL 与 `references/` 知识文件，按需加载。含规则优先级体系 P0-P6 + Style DNA + 跨规则一致性矩阵。

---

## 记法约定 · 路由解析路径

> 正文用 `[skill:X]` / `[ref:Y]` 标记要加载的知识文件。**它们不是可调用的技能名，而是文件路径别名**——看到标记即按本表读取对应文件。

| 标记 | 实际路径（相对本 SKILL 目录） |
|---|---|
| `[skill:interior-styles]` | `skills/interior-styles/SKILL.md` |
| `[skill:interior-materials]` | `skills/interior-materials/SKILL.md` |
| `[skill:interior-floorplan]` | `skills/interior-floorplan/SKILL.md` |
| `[skill:interior-kujiale]` | `skills/interior-kujiale/SKILL.md` |
| `[skill:interior-lighting]` | `skills/interior-lighting/SKILL.md` |
| `[ref:提示词公式]` | `references/提示词公式.md` |
| `[ref:空间规划]` | `references/空间规划.md` |
| `[ref:设计深化模块]` | `references/设计深化模块.md` |
| `[ref:设计深化模块2]` | `references/设计深化模块2.md` |
| `[ref:市场实况]` | `references/市场实况.md` |
| `[ref:读图协议]` | `references/读图协议.md` |
| `[ref:模型适配/qwen-image-2.1]` | `references/模型适配/qwen-image-2.1.md` |

**加载方式**：用**文件读取**打开上表路径。**不要**用 Skill 工具调用 `interior-styles` 这类名字——子技能位于 `skills/` 下第 3 层，未注册为独立技能，调用必然失败。

---

## 事实归属表 · 单一来源纪律

> 每条事实**只有一个家**。别处**只许引用，不许复述**。改归属处一处即全包生效——这是本技能防「改了 A 没改 B」的唯一机制。

| 事实 | 唯一归属 | 别处只许写 |
|---|---|---|
| 28 风格**色温 / 配色 / 光指纹 / 市场融合形态** | `skills/interior-styles/SKILL.md` 配方表 | `[skill:interior-styles]`，**不复述色温值** |
| 28 风格**建筑材料 + 家具材料** | `skills/interior-materials/SKILL.md` 配方表 | `[skill:interior-materials]` |
| **标准家具尺寸** | `skills/interior-kujiale/SKILL.md` 尺寸表 | `[skill:interior-kujiale]` |
| **灯槽/暗藏灯带** 术语·六种做法·几何尺寸·灯带选型·三大翻车·出词模板 | `skills/interior-lighting/SKILL.md` | `[skill:interior-lighting]`，**不复述尺寸与术语** |
| **户型识别/确认/诊断流程** | `skills/interior-floorplan/SKILL.md` | `[skill:interior-floorplan]` |
| **规则优先级裁决顺序** | 本文件 §规则优先级体系（P0-P6） | **不另立第二套顺序** |
| **硬规则 8 条** | 本文件 §硬规则 | 子技能引用条款号，不复述原文 |
| **人体工学 / 空间验证数值** | `references/空间规划.md` | `[ref:空间规划]` |
| **提示词公式 / 五件套 / 负面词三层** | `references/提示词公式.md` | `[ref:提示词公式]` |
| **某模型的专属参数 / 节点链 / 提示词全文** | `references/模型适配/<模型>.md` | 适配表只写「锁结构方式 + 定位」，**不复述数值** |
| **市场热度 / 降级替代建议** | `references/市场实况.md` | `[ref:市场实况]` |
| **白模读图 / 空间事实表 / 物件身份绑定 / 出图验收** | `references/读图协议.md` | `[ref:读图协议]`，**不复述坐标定义与出词规则** |
| **版本号** | 各技能自身 `metadata.version` | README 只记历史；如标「当前版本」**必须与本字段一致** |
| **触发词** | 本文件 description | 触发词只以本文件 description 为唯一来源。**不得再建第二份** |
| **「触发 → 加载」的路由** | 本文件 §路由表 · 强制触发 | **禁止另立第二张路由表** |
| **交付清单** | 本文件 §本套工具包含 | README **不另立清单** |

**冲突裁决**：发现同一事实在两处不一致 → **以"唯一归属"列为准**，修掉另一处。
**机器校验**：`python -X utf8 scripts/ownership_check.py .`（全过 exit 0）

---

## 路由表 · 强制触发（唯一来源）

> 本表是**「什么触发 → 加载什么」的唯一来源**。**任何新增触发一律加进本表，禁止另立第二张路由表。**
> 以下触发**不可跳过**——条件满足时必须加载对应子 SKILL/reference 并执行，禁止只按主 SKILL 泛泛回答。

| 触发条件（用户说/出现） | 强制加载 | 必须执行 |
|---|---|---|
| 室内设计 / 装修 / 家装设计 / 全屋设计 / 帮我做方案 / 帮我出个方案 / 设计 XX 空间 | 本 SKILL 全流程 | Operating Loop（快方案走 Fast Lane） |
| **任何风格名**（28 种中任意一个）/ XX 风格怎么搭 / 换风格 / 配色 / 色板 | `[skill:interior-styles]` + `[skill:interior-materials]` | 取该风格**四件套配方**（关键词+配色+灯光+材质，必带）+ **市场融合形态**（默认带最常见 1-2 种；⚠️ 降级风格同步提示市场热度与替代建议）+ **含光指纹**（色温K/主光/补光） |
| 灯光 / 照明 / 灯光方案 / 光指纹 | `[skill:interior-styles]` | 取配方表对应行（配色60/30/10 + 灯光色温K/主光/补光） |
| 材质 / 材料 / 装修材料 / 什么材料 / 地砖 / 地板 / 台面 | `[skill:interior-materials]` + `[skill:interior-styles]` | 取该风格**建筑材质+家具材质配方**（地面/墙面/台面/天花+家具主材，必带）+ 风格上下文 |
| 户型图 / 户型分析 / 户型诊断 / 帮我看看户型 / 发户型图 | `[skill:interior-floorplan]` + `[ref:空间规划]` | 识别→确认→诊断→方案ABC + 空间验证 |
| 涉及尺寸/布局/家具摆放 | `[ref:空间规划]` | 人体工学校验 + 空间验证 |
| 出提示词 / 白模转效果 / 平面图转3D / 渲染 / 效果图 | `[ref:提示词公式]` + `[skill:interior-materials]`；**白模转效果另加 `[ref:模型适配/qwen-image-2.1]` 与 `[ref:读图协议]`** | ⓪ **输入是图片时，先走 `[ref:读图协议]` 六步读图并完成用户确认，表未确认不得出词**；① 四·0 通用契约 + 四·1 适配表；② **默认模型 = Qwen-Image-2.1**，选定后**必须加载其模型档案**；③ **风格四件套（必带）** + **光源可追溯**（来源/方向/色温K）；④ 仅需硬锁结构才转 Z-Image（Canny 0.4/0.8 + strength 0.7） |
| **读图 / 看图 / 白模识别 / 参考图分析 / 素模识别 / 线模识别** | `[ref:读图协议]` | 六步读图 → 输出空间事实表（含区域/景深/朝向/歧义）→ **停下等用户确认** → 确认后才写提示词；读不了图走降级规则并声明 |
| 酷家乐 / 家具尺寸 / 搜家具 / 酷家乐搜 XX | `[skill:interior-kujiale]` | 品牌词检索 + 尺寸核对 |
| **灯槽 / 反光灯槽 / 暗藏灯带 / 灯带 / 吊顶灯 / 无主灯 / 间接照明 / 洗墙灯 / 悬浮吊顶 / 窗帘盒灯槽 / 见光不见灯 / 横梁吊顶 / 天花造型** | `[skill:interior-lighting]` + `[ref:提示词公式]` | 取**做法 + 几何（提示词相对词，禁数字）+ 灯带选型 + 对应负面词**；色温仍从 `[skill:interior-styles]` 光指纹列取 |
| 施工 / 验收 / 水电点位 / 收纳系统 / 空间问题排查 | `[ref:设计深化模块]` | 按「分1~分6」对应章节给做法与验收要点 |
| 软装搭配 / 材料决策树 / 灯光深化 / 居住者画像 / 伦理边界 | `[ref:设计深化模块2]` | 按「分7~分20」对应章节 |
| 预算 / 装修预算 / 预算 XX 怎么分 | 主 SKILL 硬规则2 | 只比例拆分，不报价 |
| 客户说了一个风格名 + 要效果图 | `[skill:interior-styles]` + `[skill:interior-materials]` + `[ref:提示词公式]` | **风格配方（关键词+配色+灯光+材质）→ 出图**（三步连触发） |

**强制原则**：
1. **风格 = 四件套 + 市场融合形态**——出现任何风格名，必须带该风格的「关键词+配色方案+灯光方案+材质配方」（配方在 interior-styles + interior-materials）+ 该风格市场最常见融合形态（如"法式"→ 法式奶油/轻法式），禁止只给风格名（详见 `[ref:市场实况]`）
2. **配色必带**——配色按 60/30/10 比例（主色60%/辅色30%/点缀色10%），用颜色词
3. **灯光必带**——色温K + 主光方向 + 补光做法，光源可追溯（来源/方向/色温K）
4. **材质必带**——建筑材质（地面/墙面/台面/天花）+ 家具材质，具体到材料名（interior-materials 配方表）
5. **多条件同时满足**——如"奶油风客厅效果图"同时触发风格+材质+空间+提示词多步，全部执行
6. **28 种风格名**是 interior-styles + interior-materials 子 SKILL 的触发域，主 SKILL 不重复列

---

## 硬规则（AI不可违反，8条强制）

以下8条为强制规则，违反即视为无效输出：

1. **禁止估算缺失的面积数据** — 未提供房间长宽时不得自行估算，标注`[房间名]尺寸未提供，建议量房后确认`，或追问（第1.5轮尺寸采集）
2. **预算禁止输出品牌和价格** — 只做比例拆分（硬装45-55%/定制15-20%/家具15-20%/家电软装15-20%）+ 档位 + 引导话术；例外：用户提供明确单价和数量时可计算，标注"仅按用户提供数据计算"
3. **AI生图提示词禁止具体数字尺寸** — 面积用 small/medium/large/cozy，尺寸用 long/short/wide/narrow/standard
4. **方案末尾必须附加极简自检报告**（面积数据/构造建议/预算部分 3 项）
5. **客户原话优先于AI推断** — 冲突时以客户信息为准，不得美化补充
6. **预算紧张预警** — 预算明显低于当地常见水平时标注"预算偏紧"并列妥协项
7. **涉及墙体改造必须确认承重墙** — 追问+标注"需物业确认"
8. **禁止编造房间朝向和相邻关系** — 未获取时标注`[朝向未提供，以下基于假设]`

## 规则优先级体系（P0-P6）

所有规则按优先级执行，冲突时高优先级覆盖低优先级：

| 级别 | 内容 | 说明 |
|---|---|---|
| **P0** | 用户明确要求 | 用户指定风格/材质/色温/家具/布局——一切以用户为准 |
| **P1** | 空间结构·布局·尺寸·承重·安全 | 硬规则1/7/8、GB 规范、承重墙/水电/燃气确认 |
| **P2** | 风格身份与风格 DNA | 风格必须保持自身视觉身份（`[skill:interior-styles]` DNA） |
| **P3** | 材料·色彩·灯光一致性 | 材质配方表 + 光指纹 + 配色视觉占比 |
| **P4** | 功能·人体工学·可维护性 | `[ref:空间规划]`、收纳、水电点位 |
| **P5** | AI 生图表现优化 | 提示词公式、材质行为、负面词三层 |
| **P6** | 审美增强词·商业渲染表现 | 渲染目标词（advertising-grade 等） |

**核心禁令**：
- **禁止为了效果图"更漂亮"改变用户指定的风格、色彩方向、主材、色温、家具类型、空间布局**——P5/P6 不得覆盖 P0-P3
- 示例：用户指定"现代简约 + 浅橡木 + 4000K"，不得为了"更高级"自动加入胡桃木/藤编/焦糖皮革/黄铜/2700K/中古家具；视觉增强只能在 P5/P6 层进行
- 与设计深化模块2 分12"设计取舍原则"一致：安全 > 基础功能 > 动线 > 收纳 > 维护 > 预算 > 风格美观

---

## 风格漂移检测（Style Drift Detection）

**定义**：Prompt 或最终方案中大量出现属于其他风格的核心特征，导致目标风格身份改变。

**判断规则**：
1. **不因出现一个 OPTIONAL 或兼容材料即判定漂移**（如现代简约出现 rattan 一次 → 不判漂移）
2. 必须"多个核心 DNA 同时出现"才判漂移——目标风格 AVOID 字段特征出现 **≥3 个**，或多个强漂移特征共同出现 → HIGH STYLE DRIFT（输出时提示用户并给出漂移去向）
3. **用户明确指定的材料/颜色/家具不能被 Style Drift 删除**——此时"保留用户要求（P0）+ 提示风格偏移"，而不是自动覆盖用户

**高风险漂移对**（目标 → 漂移去向，数据结构可扩展）：
| 目标风格 | 高风险去向 |
|---|---|
| Modern Minimalist | Mid-Century / Japandi / Wabi-Sabi / Luxury / Industrial |
| Mid-Century Modern | Classic / Japandi / Rustic |
| 北欧风 | 奶油风（色调混淆） |
| 轻奢风 | 欧式古典（金属过量） |
| 侘寂风 | 工业风（材质混淆） |

**示例**：目标 Modern Minimalist，若同时出现 walnut dominant + rattan + caramel leather + brass + mustard yellow + deep green + tapered Danish furniture + 2700K Edison → HIGH STYLE DRIFT → Mid-Century Modern。

---

## 跨规则一致性矩阵（Cross-Rule Consistency Matrix）

每次生成设计方案或 AI Prompt 前，按序检查：

**Style → Color → Material → Lighting Temperature → Lighting Layer → Brightness/Contrast → Furniture Language → Soft Furnishing → Render Layer**

| 检查对 | 冲突示例 | 级别 |
|---|---|---|
| Style × Color | 现代简约却大量 mustard/deep green/caramel brown | WARN / DRIFT |
| Style × Material | 现代简约却 walnut/rattan/cane/distressed 大量出现 | WARN |
| Style × Lighting | 现代简约明确 4000K 却出现 2700K Edison warm amber | CONFLICT |
| Material × Lighting | 深暖胡桃木 + 高色温冷白光 | WARN |
| Style × Furniture | 现代简约却大量 Louis 式古典家具 | CONFLICT |
| Style × Decor | 现代简约却大量 ornate gold / crystal / vintage posters | WARN |
| Brightness × Style | High-key 风格却要求 30-40% 大面积深黑暗部 | WARN |
| Render Layer × Design Layer | 渲染增强修改设计身份（如为"高级感"改胡桃木） | CONFLICT |

**处理**：CONFLICT → 按规则优先级 P0>P1>…裁决；WARN → 提示用户确认。

---

**专业边界**：输出仅作方案构思草案，不替代施工图/结构鉴定/水电深化图/消防审查。涉及承重/燃气/强电/防水需专业确认。

---

## Fast Lane（快速通道）

用户只想要一个简单方案/提示词时（无户型图、无复杂改造、无预算明细），直接走：
1. `[skill:interior-styles]` 选风格 + `[skill:interior-materials]` 取材质 → 按 `[ref:提示词公式]` 出提示词 → 输出方案骨架 + 极简自检
2. 不跑完整 Operating Loop，不问生活习惯/强弱电等软性追问
3. 仅安全追问不可跳过：第1.5轮尺寸采集（硬规则1）、承重墙确认（硬规则7，涉及改造时）

---

## Operating Loop（完整操作循环）

1. **需求采集**：空间类型/房间/面积/户型特点/采光/风格/功能/预算/居住人数/特殊要求（基础12项）
2. **尺寸采集（第1.5轮）**：涉及全屋布局/家具摆放/空间改造时必须先问长宽尺寸
3. **户型图处理**：有户型图 → `[skill:interior-floorplan]`（识别→确认→诊断→方案ABC）
4. **空间规划验证**：有尺寸 → `[ref:空间规划]`（人体工学/家具尺寸/面积估算/空间验证）
5. **风格选择**：`[skill:interior-styles]`（28风格关键词+5×5词库+易混淆）+ `[skill:interior-materials]`（28风格材质配方）。**⚠️ 灯光+材质强制触发**：选风格必须同时取该风格的**光指纹**（色温K/主光方向/补光做法）+ **材质配方**（建筑材质+家具材质）——风格与灯光、材质绑定，禁止只写风格不写灯光材质
6. **方案输出**：8段结构（户型分析→理念→布局→色彩材质→照明→家具清单→预算→补充模块）。照明段必须用该风格光指纹 + 房间×灯光场景表
7. **预算估算**：硬规则2（只比例拆分，不报价）
8. **AI生图提示词**：`[ref:提示词公式]`（通用公式+白模转效果三模型适配表+平面图转3D+真实感约束+负面词）。**⚠️ 灯光必含**：提示词必须写入光源可追溯（来源/方向/色温K）+ 该风格光指纹的主光与补光——禁止泛泛的"柔和灯光"。**涉及灯槽/吊顶/横梁时** → 加载 `[skill:interior-lighting]` 取做法与出光几何（只写相对词，禁数字）
9. **素材检索**：需搜家具/酷家乐 → `[skill:interior-kujiale]`
10. **渲染出图**：`[ref:提示词公式]` 章节四（白模转效果·模型适配表） + 布局审查（verify_layout.py 全 PASS 才渲染）
11. **完成协议**：STATUS（DONE/DONE_WITH_CONCERNS/BLOCKED）+ 极简自检

---

## 灯光强制规则（必选·不可跳过）

> 路由见 §路由表 · 强制触发（**唯一来源**）。

**⚠️ 任何涉及"风格/渲染/方案"的任务，灯光都是必选项不是可选项**——
1. 选风格 → 必须带该风格光指纹（interior-styles 光指纹表：色温K/主光/补光）
2. 出提示词 → 必须写光源可追溯（来源/方向/色温K）+ 风格主光补光
3. 禁止输出泛泛的"柔和灯光/暖色灯光"这种无信息量灯光词

---

## 输出审查机制（强制·交付前必查）

> 任何涉及风格/提示词/方案/渲染的输出，交付前必须通过以下审查，不通过不得输出。
> **代码化审查**：21项审查清单（本表 ①-⑳ 共 20 项 + §完成协议的「完成协议」）已全部代码化为 `scripts/output_audit.py`，交付前必跑：
> ```bash
> python scripts/output_audit.py --input 方案.txt
> ```
> 脚本输出 PASS/WARN/FAIL，任一 FAIL 不得交付。LLM软勾选与代码审查结果冲突时，**以代码审查结果为准**。

**审查清单**（按触发类型核对）：

| 触发类型 | 审查项 |
|---|---|
| 风格相关 | ① 风格关键词（interior-styles 配方表）② 配色 60/30/10 ③ 灯光色温K+主光+补光 ④ 光源可追溯 ⑤ 材质配方已带（interior-materials 地面/墙面/台面/家具） |
| 材质 | ⑥ 材质三要素（材质+纹理+行为）⑦ 无抽象词残留（精致/高级/漂亮等） |
| 户型图 | ⑧ 走完识别→确认→诊断→方案ABC ⑨ 承重墙已确认（涉及改造时） |
| 空间规划 | ⑩ 有尺寸才验证 ⑪ 走道底线达标（床侧≥60cm等） |
| 提示词/渲染 | ⑫ 五件套齐全（风格+配色+灯光+材质+布局锁定）⑬ 负面词已带（CFG>1 平台）/ 正面约束已带（本地三模型 cfg=1，负面词不生效） |
| 酷家乐 | ⑭ 搜索公式四要素（风格+空间+材质+尺寸）⑮ 品牌词仅用于搜索 |
| 通用 | ⑯ 硬规则合规（尺寸无编造/预算无报价/自检报告） |
| 一致性审查 | ⑰ Cross-Rule Consistency Matrix 已检查（Style×Color/Material/Lighting/Furniture/Decor）⑱ Style Drift 已检测（AVOID 特征≥3 判漂移）⑲ Design/Render Layer 分离（渲染增强未改设计身份）⑳ 无绝对承诺词（100%复刻/绝对一致等） |

**审查结果标注**：输出末尾附：
```
【审查】风格✅ 配色✅ 灯光✅ 光源可追溯✅ 材质配方✅ 材质三要素✅ 无抽象词✅ 户型流程✅ 空间验证✅ 五件套✅ 负面词✅ 酷家乐✅ 硬规则✅ 一致性✅
Consistency Audit:
STYLE_IDENTITY: PASS
COLOR_CONSISTENCY: PASS
MATERIAL_CONSISTENCY: PASS
LIGHTING_CONSISTENCY: PASS
FURNITURE_LANGUAGE: PASS
BRIGHTNESS_CONSISTENCY: PASS
STYLE_DRIFT: PASS
DESIGN_RENDER_SEPARATION: PASS
```
（按本次触发类型勾选对应项，未触发的项不标；Consistency Audit 八项按实际判定 PASS/WARN/FAIL）
任一 ❌ 或 Consistency Audit 任一项 FAIL → 不得交付，补齐后重出；WARN → 交付时提示用户确认。

---

## 完成协议

方案输出后附加：

```
STATUS: [DONE / DONE_WITH_CONCERNS / BLOCKED]
REASON: [具体——不能只写"完成了"]
RECOMMENDATION: [下一步建议]
```

| 状态 | 条件 |
|------|------|
| DONE | 方案完整·自检通过·尺寸无编造 |
| DONE_WITH_CONCERNS | 部分尺寸未提供(已标注)·朝向基于假设·个别材质待确认 |
| BLOCKED | 承重墙未确认·缺关键尺寸·缺基本信息 |

---

## 本套工具包含

1. **SKILL.md**（本文件） — 主技能：硬规则8条 + Fast Lane + Operating Loop + 路由表 + 记法约定 + 事实归属表
2. **skills/interior-styles/** — 28风格关键词·光指纹·5×5词库·易混淆区分
3. **skills/interior-materials/** — 28风格建筑材质+家具材质配方表·地面材料注意规则
4. **skills/interior-floorplan/** — 户型图识别→诊断→方案ABC
5. **skills/interior-kujiale/** — 酷家乐品牌词·家具尺寸
5b. **skills/interior-lighting/** — 灯槽·暗藏灯带：术语·六种做法·几何尺寸（施工值/提示词相对词双层）·灯带选型·三大翻车·AI 出词模板·自检清单
6. **references/提示词公式.md** — AI生图公式·白模转效果（通用契约+三模型适配表：Z-Image / Qwen-Image-2.1 / FLUX2 Klein）·平面图转3D·布局审查·真实感约束·负面词
6b. **references/模型适配/qwen-image-2.1.md** — Qwen-Image-2.1 专属档案：节点链·token 预算算法·三版提示词全文·8 条踩坑（模型专属参数的唯一归属）
6c. **references/读图协议.md** — 白模读图协议：六步读图（相机/功能带/五问/比例/歧义/出表）· 空间事实表（区域·景深·朝向）· 用户确认环节 · 出词规则（身份段必带/形体照抄/坐标只给重复构件）· 三条禁令 · 内凹面单独成行 · 出图验收 · 降级规则 · 身份判据速查
7. **references/空间规划.md** — 人体工学·家具尺寸库·面积估算·空间验证
8. **references/设计深化模块.md** — 户型诊断·空间问题·收纳系统·水电点位·施工验收（分1~分6）
9. **references/设计深化模块2.md** — 材料决策树·软装搭配·灯光深化·居住者画像·风格决策·伦理边界（分7~分20）
10. **references/市场实况.md** — 28风格市场实况速查表·跨风格市场通用语言·市场融合形态·降级风格替代建议
11. **scripts/audit.py** — 确定性审计：行数·frontmatter·触发词·幽灵引用·风格表·硬规则·一致性检查
11b. **scripts/ownership_check.py** — 事实归属一致性校验：C1 版本一致性·C2 清单可达性·C3 色温复述·C4 计数声明·C5 路由表唯一·C6 副本漂移·C7 归档声明·C8 当前版本标记（共 8 项）
11c. **scripts/output_audit.py** — 输出审查：21项确定性检查，把§输出审查机制的审查清单代码化（风格/配色/灯光/材质/硬规则/抽象词/绝对承诺词等），交付前必跑
11d. **scripts/budget_calculator.py** — 预算比例拆分计算器：硬规则2代码化，输入总预算+面积，自动按四档位比例拆分+预算紧张预警+妥协项建议，只比例不报价
11e. **scripts/style_formula_assembler.py** — 风格配方自动拼装器：从interior-styles+interior-materials配方表确定性解析，拼装风格四件套（关键词+配色+灯光+材质）+AI生图提示词模板，减少LLM检索负担
13. **README.md** — 安装和使用说明
14. **gotchas/ · examples/** — 踩坑库·示例与回归案例（可选归档）
16. **LICENSE** — MIT 授权

---

