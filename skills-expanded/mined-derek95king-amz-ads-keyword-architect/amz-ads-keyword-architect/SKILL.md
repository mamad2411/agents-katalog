---
name: amz-ads-keyword-architect
description: 当用户需要做亚马逊关键词拓词、词库搭建/清洗/扩展/拆解/分级打标，或基于竞品 ASIN / 竞品词 / ABA / 选品指南针 / 评论 VOC 产出广告 campaign 架构（投放主题簇、ad group 分层、匹配方式、预算、攻守测分级），或进一步做 VOC 词库/收录排名追踪等关键词资产化交付时使用。覆盖「找词 → 拆解 → 需求三层分析(SIF) → 相关性×需求×竞争×趋势分级 → 属性 7 类分类 → 聚类成主题簇 → 广告架构落地 → VOC库/收录追踪 → Excel/飞书双通道交付」全链路。默认 SIF 分析 + Sorftime 找词/评论，自包含分类与评分，标品≤15/非标品≤30 ad group 主题簇，交付支持本地 Excel 与飞书在线表格双通道（按系统能力检测 + 用户偏好选择，默认 Excel），数值类指标只取数不编造。
---

# 亚马逊广告架构拓词 Skill

> 全链路覆盖「找词 → 广告架构 → 下游资产化 → 双通道交付」：在广告 campaign 架构之上，进一步纳入下游模块（VOC库 / 收录排名追踪），落到同一份工作簿的新增 Sheet。交付支持**双通道**——本地 Excel（默认）或飞书在线表格（可选，按系统能力检测 + 偏好选择），同一份数据两通道复用。受三道 CHECKPOINT / 反模式黑名单 / 簇上限 / 反虚构铁律统一约束。

## 核心理念

关键词资产的最终目的是**服务于广告架构产出**：从「词」到「ad group 主题簇」到「campaign 分层」，每一步都要有量化依据和可落地的执行动作。本 skill 覆盖「找词 → 拆解 → 需求/竞争分析 → 分类分级 → 聚类 → 广告架构 → 下游资产化 → 双通道交付（Excel/飞书）」全链路，自包含（不依赖其他 skill）。

### 绝对禁令

**不得虚构搜索量、SFR、ACOS、CTR、CVR、排名、市场份额等任何数值型指标。** 数值类指标只能通过工具（SIF / Sorftime / ABA 导出）取数；数据缺失时一律标「待数据验证」，仅做语义判断，不以经验值填充关键指标列。

## 标准执行流程

```
Step 0  锚点 + 类目门 + ASIN 回显
        └ 本品 spec + 必含/必排属性 + 竞品同类校验
          （本品 Listing/规格默认用 Sorftime ProductRequest 自抓，不需用户手填）
        └ 未指定类目 → 弹类目门提示 → 等确认
        └ 抓数据前回显竞品 ASIN 原文让用户确认（防串错）
        ↓
Step 1  多源采集
        └ ABA / 竞品反查 / 选品指南针 / 评论 VOC
        └ 按源打标签 + 置信度，以 ABA 为锚
        ↓
Step 2  归一化 + n-gram 拆解
        └ lemmatize、停用词过滤、单复数合并、保留错拼
        └ n-gram 词根拆解（bi/tri-gram → 词根）
        ↓
Step 3  需求量化（词频 ≠ 相关性）
        └ TF-IDF + SIF 需求三层：history / root_trend / demand
        └ 机会维度 ≠ 相关性维度，不得混用
        ↓
Step 4  双维打分  ← 🔴 CHECKPOINT 1（见下）
        └ 相关性（SIF top3 份额优先）× 需求 × 意图明确度
        └ 竞争维度：SIF competition 三维 + CPC + top3 click/conversion share
        ↓
Step 5  属性 7 类分类
        └ 优先级链：品牌 > 否词 > 人群 > 场景痛点 > 属性 > 核心大词 > 长尾
        └ 只取一个最高优先级；属性词备注删除核心产品词后的连续片段
        └ 详见 references/03-classification.md
        ↓
Step 6  聚类成投放主题簇
        └ 标品 ≤15 / 非标品 ≤30 ad group 主题簇
        └ 叠 coverage_ratio 验证覆盖率
        └ 详见 references/04-clustering.md
        ↓
Step 7  广告架构分级
        └ 四维：相关性/意图 × 搜索量 × 竞争/CPC × 趋势
        └ → campaign / ad group / 匹配方式 / 预算占比 / 攻守测
        └ 竞品 ad group 反查（SIF ads_get_ad_group_keyword_breakdown）为实证锚点
        └ 详见 references/05-ad-architecture.md
        ↓
Step 8  输出工作簿 + 否词池（双通道）  ← 🔴 CHECKPOINT 2（见下）
        └ 否词池贯穿 Step 0–7，交付前必须非空
        └ 恒定 Sheet(7)：拓词总表 / P0-P1优先词 / Listing埋词建议 / PPC投放建议 / 否词候选 / 来源汇总 / 执行说明
        └ 条件 Sheet：主题簇(传 --clusters-csv) / 广告架构(传 --architecture-csv) / ASIN画像(传 --asin-summary)
        ↓
Step 9  下游资产化（同一份工作簿，双通道交付 Excel/飞书）
        └ VOC词库：口语词 → 标准搜索表达映射，证据片段待填原文（≤20 词，不编造）
        └ 收录排名追踪：P0/P1/P2 词的待检测台账，指标列=待检测/待数据验证
```

详见 [references/01-flow.md](./references/01-flow.md)。

## 🔴 CHECKPOINT 0 · Step 0 🛑 STOP

**抓取任何数据之前必须完成以下校验，缺一项不进 Step 1：**

```
if 用户未指定具体类目:
    提示：「当前为通用默认阈值（SFR/搜索量/CPC 均为经验值）。正式分析前建议先定义类目并校准阈值。
           是否：(a) 继续用通用默认值  (b) 我先给你类目，按类目切分阈值」
    等待确认

抓数据前回显竞品 ASIN 串原文让用户确认（防串错）。
```

还需满足：
- 竞品 ASIN 3–5 个；不足 3 个先要求补足
- **ASIN 必须是真实串**（`B0` + 8 位真实字符）。若出现 `B08XYZ1234` / `B07ABC5678` 这类明显占位/示例串 → 🛑 停下要求用户给真实 ASIN，**不得拿占位串去取数**
- 本品锚点（spec / 必含属性 / 必排属性）已齐——**优先用 Sorftime `ProductRequest` 自抓本品 Listing（标题/五点/Property 规格/变体）填充，而非要求用户手填**；只有 A+ 图片内文案需手动补
- 竞品类目或形态不一致 → 先提示确认，不混拓
- **交付通道**：用户已点名 Excel/飞书则照办；未点名则默认 Excel，**不在此阶段阻塞**（最终交付前按 `references/09-feishu-delivery.md` 的决策树检测 + 选择即可）。仅当用户明确要飞书但未给已有表时，到交付环节再问「新建表还是写入已有表（给表格链接或标识）」

## 🔴 CHECKPOINT 1 · Step 4 双维打分前 🛑 STOP

抽样 10–20 行，核查**相关性是否被词频或搜索量代理**——词频高 ≠ 相关性高；SFR 低 ≠ 本品强相关。属性分类备注列不得为空。不过则回 Step 3 修正后再打分。详见 [references/07-quality-check.md](./references/07-quality-check.md)。

## 🔴 CHECKPOINT 2 · Step 8 交付前 🛑 STOP

逐项核查五个必要条件：否词池非空、广告分级四维（相关性/需求/竞争/趋势）均已填写、数值列无编造（缺失列必须留空并标「待数据验证」）、Excel 含全部必备 Sheet、**下游 2 Sheet（VOC库/收录追踪）的指标列保持「待检测/待数据验证」而非被编造填充**。任一不过先回对应 Step 修正，不带瑕疵交付。详见 [references/07-quality-check.md](./references/07-quality-check.md)。

## 工具编排 + 数据源双选项

**分工铁律**：Sorftime = 找词 + 评论正文 + 实时抓取；SIF = ABA 需求/竞争/竞品广告架构反查。两者互补，不可互换。

**数据源双选项**：
- 选项 A：用户已提供 ABA / 选品指南针导出文件 → 直接读取，作为 Step 1 锚源
- 选项 B：用户未提供 → 用 SIF `market_get_keyword_history` / `market_get_keyword_demand` + Sorftime `ASINRequestKeywordv2` 补数

站点默认 US，支持 US / CA / EU5（UK/DE/FR/IT/ES）。Sorftime domain 映射：US=1, UK=2, DE=3, FR=4, CA=7, IT=8, ES=9。

**失败兜底（if-then 三段式）**：

| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| SIF 某工具报错/无响应 | 重试一次；换等价工具（如 demand↔history） | 切 Sorftime 等价能力；仍不通 → 让用户手工粘原始数据，标该指标「待数据验证」 |
| Sorftime 调用失败/浏览器桥未连 | 确认 Chrome + Kimi WebBridge 已连后重试 | 改用 SIF 反查词替代；VOC 缺失则跳过并在交付说明标注 |
| 完全无外部数据（用户也不提供） | 转「语义版」：65 分语义评分 | 全程标「未补外部数据，待数据验证」，**绝不编造数值** |
| 竞品 ASIN < 3 / 含占位串 | 回 CHECKPOINT 0 要求补足/换真实串 | 用户坚持 → 仅语义拓词且开头声明范围不足 |
| VOC 源为空（无 Review/VOC 词且无 `--voc-csv`） | 提示用户补 Review 采集（Sorftime `ProductReviewsQuery`）；脚本仍出 VOC词库 表头脚手架 | 在执行说明标注「VOC 缺口」，跳过 VOC 映射，不影响其余 Sheet |
| `--voc-csv` 读取失败 / 列异常 | 回退到自动种词脚手架（证据片段留待填） | 标注「VOC 源异常」，提示用户核对 CSV 列后重跑 |
| `--asin` 未提供 | 收录排名追踪表 ASIN 列填「待填」继续生成 | 交付时提醒用户回填 ASIN，不阻塞其余流程 |
| 用户要飞书但 `lark-cli` 不可用（缺命令/`user.available=false`/无 `sheets:spreadsheet:create` scope）| 退回本地 Excel 交付，一句话说明「飞书未接入，需要可后续导入」| 标「飞书未接入」，不阻塞 |
| `lark-cli` 报 `needs_refresh` | 视为正常态，直接调用自动刷新；**不当失败处理** | — |
| 飞书 create/append 写入失败 | 重试一次；macOS Keychain 被沙盒拦截 → 沙盒外重试同条命令，**不改业务逻辑** | 保留本地 `.xlsx` + `.sheets.json` + 可重试命令，说明失败点，标「飞书待重试」，**不为交付成功而编数值** |

飞书通道完整失败表 + 降级见 [references/09-feishu-delivery.md](./references/09-feishu-delivery.md)；工具取数失败见 [references/06-tools-data.md](./references/06-tools-data.md)。

## 输出（双通道交付）

**先定通道，再生成**。交付前按 `references/09-feishu-delivery.md` 的决策树走：①用户点名 Excel/飞书 → 照办；②未点名 → 默认 **Excel**；③用户要飞书 → `lark-cli auth status` 检测能力可用后再选「新建表/写入已有表」，不可用则退回 Excel 并说明。两条通道**共用同一份脚本产物**，不另起炉灶。

**通道一 · 本地 Excel（默认）**：使用 `scripts/build_kw_architecture.py` 生成 `.xlsx`。

**通道二 · 飞书在线表格（可选）**：
- 路径甲（推荐）：脚本产物 `.xlsx` → 调 `lark-drive` skill 导入为飞书在线表格，一次带入全部 Sheet。
- 路径乙（需在飞书原生追加）：脚本加 `--emit-sheets-json` 导出每 Sheet 的 `{name, headers, rows, values}` → 调 `lark-sheets` skill 用 `+create`/`+create-sheet`/`+append` 逐页签构建。
- 细则、降级见 `references/09-feishu-delivery.md`。

支持的核心 CSV 入参：
- `--clusters-csv`（列：主题簇, 主属性维度, 相关性, 需求, 词数）
- `--architecture-csv`（列：campaign, ad_group, 匹配方式, 预算占比, 攻守测）

下游资产化入参（全部并入同一份工作簿）：
- `--voc-csv`（可选，列自定义；不传则从 VOC/Review 类词自动种出脚手架，证据片段留待填）
- `--asin`（本品 ASIN，用于给「收录排名追踪」表种 ASIN 列）
- `--no-downstream`（开关：跳过 VOC库/收录追踪，退回纯广告架构行为，不出下游 Sheet）
- `--emit-sheets-json`（飞书通道才需要：把每个 Sheet 导出为 JSON manifest，喂给 `lark-sheets` 原生构建；Excel 通道不传）

示例命令行（`拓词总表.csv` 为必填 positional 入参 = 关键词总表 CSV）：
```bash
python3 scripts/build_kw_architecture.py 拓词总表.csv \
  --product-name "yoga mat" --core-terms "yoga mat" --asin B0XXXXXXXX \
  --clusters-csv clusters.csv \
  --architecture-csv architecture.csv \
  --voc-csv voc.csv \
  -o 广告架构拓词_B0XXXXXX.xlsx \
  --emit-sheets-json 广告架构拓词_B0XXXXXX.sheets.json   # 仅飞书通道
```

默认追加 2 个下游 Sheet：`VOC词库` / `收录排名追踪`。其指标列默认填「待检测/待数据验证」，由分析人结合工具取数回填，**禁止脚本或模型编造数值**。下游模块细则见 [references/08-downstream-application.md](./references/08-downstream-application.md)。

不支持 Excel 时降级为 Markdown 表格 / 单文件 HTML 报告。数值缺失列留空并标「待数据验证」，绝不编造。飞书在线交付（导入 / 原生构建）见 [references/09-feishu-delivery.md](./references/09-feishu-delivery.md)。

## 簇上限

- **标品** ≤ 15 个 ad group 主题簇
- **非标品** ≤ 30 个 ad group 主题簇

超出上限须合并语义最近的簇，并用 `coverage_ratio` 验证合并后覆盖率不下降。详见 [references/04-clustering.md](./references/04-clustering.md)。

## 🚫 反模式黑名单（红灯）

执行中命中任一条 = 立即停手改正：

1. **别把词频/搜索量当相关性** —— 高频多是泛大词；相关性走「反查 ASIN 同类占比」，词频只进需求维。
2. **别编造数值** —— 搜索量/SFR/CPC/ACOS/份额/排名缺数据时标「待数据验证」，绝不用经验值填关键指标列。
3. **别跳类目门** —— 未指定类目先弹 CHECKPOINT 0 提示，不直接用通用阈值开跑。
4. **别用未确认/占位 ASIN 取数** —— ASIN 串必先回显确认；`B08XYZ1234` 类占位串禁止入流程。
5. **别把 VOC 口语直接当投放词** —— 评论词先映射成标准搜索表达再入池（如「light output adjustable」≠ 搜索词，归卖点/A+）。
6. **别把否词流后置** —— 否词池贯穿 Step 0–7 持续沉淀，不到交付才补。
7. **别只按竞争度单维分广告架构** —— 必走「相关性×需求×竞争×趋势」四维，否则金词与垃圾词混档。
8. **别擅自往飞书写** —— 用户没点名通道时默认本地 Excel；要飞书须先 `lark-cli auth status` 检测可用 + 确认新建/写已有表，不可用就退回 Excel 并说明，**不为「交付成功」而在任一通道编造数值**。

## 何时读取详细 references

按当前任务需要，读取对应 reference 文件：

- 走流程、查步骤细节 → `references/01-flow.md`
- 定量化阈值、校准类目参数 → `references/02-metrics.md`
- 做属性 7 类分类、查备注规范 → `references/03-classification.md`
- 语义聚类成主题簇、控簇上限 → `references/04-clustering.md`
- 广告架构决策矩阵、campaign/ad group 分层规则 → `references/05-ad-architecture.md`
- SIF/Sorftime 取数与评分、站点 domain 映射 → `references/06-tools-data.md`
- 交付前三大 CHECKPOINT 自检清单 → `references/07-quality-check.md`
- 下游资产化（VOC库/收录追踪）的列定义与回填纪律 → `references/08-downstream-application.md`
- 交付通道决策（Excel ↔ 飞书检测/偏好）、飞书导入/原生构建两条路径 → `references/09-feishu-delivery.md`

**不要一次读全，按需读取**，节省上下文窗口。
