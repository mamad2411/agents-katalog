---
name: ai-future-is-now
description: 《AI未来已来》（李开复）蒸馏出的 18 个判断模块的统一入口。用于：判断某个 AI 项目值不值得投或算不算成功；诊断 AI 转型为什么推不动；AI 预算怎么编；评估 AI 方案、产品或供应商（是不是真 agent、为什么不好使）；规划企业 AI 底座、本体与数据飞轮；一号位信息穿透、承诺问责、人才识别；DRI 组织重塑、扁平化顺序、算力计价与薪酬；个人职业定位（会不会被 AI 取代、往哪转）；以及面对高代价、不可逆的重大决断（品味／远见／信念／勇气的分流）。不用于：纯信息查询、写提示词、常规数据工程、日常琐碎选择、以及定位某个员工的私人状况（应拒绝）。
license: MIT
metadata:
  version: 1.0.0
  source_book: 《AI未来已来：CEO、组织、个人的时代红利》 李开复 2026
  modules: 18
  generated_by: cangjie-skill (RIA-TV++)
  repo: https://github.com/Grruuu/ai-future-is-now-skill
---

# AI 未来已来 · 判断模块入口

李开复《AI未来已来》蒸馏出的 **18 个判断模块**。278 条候选经三重验证筛出 18 个（通过率 26.5%）。

## 怎么用

**两步：先分流，再执行。**

1. 用下面的分流表定位到 **1 个**模块（偶尔 2 个）。不要把多个模块一起套用——它们适用层级不同，混用会误诊。分流不确定时，先问用户一个具体问题定位症状，**不要猜**。
2. **读该模块的完整内容**：`modules/<模块名>/SKILL.md`（相对本文件的路径）。
   每个模块含六段：R 原文引用 / I 方法论骨架 / A1 书中真实案例 / A2 触发场景 / **E 可执行步骤（带判停条件）** / **B 边界（作者盲点与不适用场景）**。
   **E 和 B 两段是这套东西的核心**，不要跳过 B 直接执行 E。

## 分流表

| 用户的症状 | 模块 |
|---|---|
| 这个 AI 项目值不值得投／算不算成功／效率提升 40% 算成果吗 | `earnings-call-test` |
| AI 搞了一年没成果／项目老卡住／每次都说"数据不够干净" | `transformation-failure-diagnosis` |
| 模型降价了预算能不能砍／单价在跌账单却在涨 | `token-cheap-system-valuable` |
| AI 会不会颠覆我们这行／要不要现在动还是再等等 | `tech-shock-four-crushes` |
| 这个 AI 方案／供应商靠不靠谱／他们说沉淀了几十年专家规则 | `ai-solution-two-laws` |
| 供应商说这是 agent／为什么每步都要我确认／买的是不是真智能体 | `agent-level-ladder` |
| 它答得流畅但内容错／每次都要重新解释背景／引用旧模板 | `agent-four-components` |
| 模型接了数据导了，为什么还上不了生产 | `ai-decision-core` |
| 资料都喂了还是答不准／跨系统的问题答不了／数据中台没人用 | `living-ontology` |
| 大家都买同样的模型，我们靠什么赢／要不要一次铺到所有部门 | `data-flywheel` |
| 汇报上来全是好消息／坐得越高越听不到真话 | `boss-ai-engines` |
| 会上定好的事散会就没了／怎么建问责／要不要学桥水极度透明 | `commitment-ledger` |
| 谁是真正的顶尖／晋升总给会汇报的人／怎么找被低估的人 | `ruler-before-ranking` |
| 这事人人沾边没人负责／想设端到端 owner 但不知道选谁 | `dri-identify-empower` |
| 准备压扁层级／AI 能替代中层了要不要裁／同行裁了四成 | `sediment-before-flatten` |
| 人数在降算力账单在涨／没下属的人凭什么拿更多／扩招还是加算力 | `headcount-to-compute` |
| 我的工作会不会被 AI 取代／该往哪个方向转 | `work-quadrant-compass` |
| 数据不够但我觉得该做／所有人都不看好／该不该赌一把 | `four-faces-of-judgment` |

### 易混淆的三组（分流时特别注意）

- `agent-level-ladder`（**选型前**判等级）vs `agent-four-components`（**使用中**排故障）
- `ai-decision-core`（企业底座**缺哪块拼图**）vs `living-ontology`（**地图那块**具体怎么建）vs `agent-four-components`（**单个工具**的组件缺口）
- `work-quadrant-compass`（长期**往哪走**）vs `four-faces-of-judgment`（眼前这个**决定怎么做**）

### 一句话速查（确认分流对不对）

| 模块 | 它到底在做什么 |
|---|---|
| `earnings-call-test` | 三问把 AI 项目归到"投入指标／化妆／真实改善"三态之一 |
| `transformation-failure-diagnosis` | 三错因果链 + 识别不留痕的"口袋否决" |
| `token-cheap-system-valuable` | 降价时调**结构**不调总额：Token 降、配套系统升 |
| `tech-shock-four-crushes` | 四维打分判变革量级，产出"第一张靶纸" |
| `ai-solution-two-laws` | 一句提问定天花板："靠机器自学还是靠人工维护规则？" |
| `agent-level-ladder` | 四级阶梯，分水岭在"你做它帮"与"你定目标它来做"之间 |
| `agent-four-components` | 记忆→工具→知识→**模型排最后**的排查顺序 |
| `ai-decision-core` | 大脑／地图／导航／手脚，缺哪块补哪块 |
| `living-ontology` | 存活判据：业务方能不能自己读懂、自己改 |
| `data-flywheel` | 五步 + 小闭环必须跑通"读取—判断—执行—记录—衡量" |
| `boss-ai-engines` | 四引擎 + 交叉核验 + 看沉睡数据而不是看周报 |
| `commitment-ledger` | 承诺账本，**先划边界再建系统** |
| `ruler-before-ranking` | 先定尺子再量人，20→10→1 三问漏斗 |
| `dri-identify-empower` | **先验授权再验人**，四能力 + 四类人处置 |
| `sediment-before-flatten` | 三盏绿灯，先沉淀知识资产再精简层级 |
| `headcount-to-compute` | 算力单列科目 + 薪酬三支柱 + 董事会三指标 |
| `work-quadrant-compass` | 内容自由度 × 人际互动依赖度四象限 + 三个方向 |
| `four-faces-of-judgment` | 品味／远见／信念／勇气，**信念是认知、勇气是行动** |

---

## 三条全局边界（任何模块都适用，执行前先读）

**① 作者在卖这套系统。** 李开复是零一万物创始人兼 CEO，书中第 6、7 章的"企业 AI 决策中枢"与"老板AI"正是他公司在售的产品（书中承认"我每天都在用，也开始卖给客户用"）。`ai-decision-core`、`living-ontology`、`data-flywheel`、`boss-ai-engines` 四个模块受影响最大——它们同时承担方法论与销售论证两种功能，使用时需自行拆开。

**② 全书归因结构不可证伪。** 所有失败案例（Zappos／Klarna／Block／麦肯锡那个 39%）一律被解释为"顺序错了"，而非"方向有边界"。最明显的是 Klarna——它自己的结论其实是一条**能力边界**结论。用 `transformation-failure-diagnosis` 和 `sediment-before-flatten` 时**必须保留"可能真的是技术还不成熟"这个分支**，否则会把所有反馈都读成对方法论的佐证。

**③ 样本偏向大型、有钱、有数字化底子的企业。** 作者的一手材料来自数百家优秀传统企业 CEO、世界 500 强、全球前 20 矿业巨头，以及他自己那家 AI 创业公司。小微企业、低毛利行业、现金流紧张的公司、无 IT 底子的组织，适用性未被验证——遇到这类用户要**主动说明**，而不是硬套。

## ⚠️ 涉及员工数据的三个模块

`boss-ai-engines`、`commitment-ledger`、`ruler-before-ranking` 都要读取员工工作痕迹。

- 它们的 E 段**第一步都是"先划边界"**，这一步不能跳过。
- 原书只给了原则性边界（不读隐私／看聚合／员工知情／数据留公司内），**没有制度化制衡**。这三个模块的 B 段补入了作者没给的三条：**谁审计这套系统、员工能否申诉、越界如何被发现**。
- 读取员工通信与工作记录在中国大陆、欧盟等法域受《个人信息保护法》/GDPR 约束。**不构成法律意见。**

**下列请求应当直接拒绝，而不是调用任何模块**：定位某个员工的私人状况（"看看谁在偷偷找工作"）、调取个人私聊内容、用人才识别方法排裁员名单。

---

## 延伸材料（同一仓库内）

- `INDEX.md` — 全景、mermaid 引用图、推荐学习顺序
- `DIGEST.md` — 全书精华长文（约 1.5 万字），用户问"这本书讲了什么"时读它
- `BOOK_OVERVIEW.md` — Adler 四步整书分析，含批判章节
- `verified.md` — 18 条通过单元的 V1/V2/V3 完整判定
- `rejected/` — 50 条被淘汰单元 + 原因 + 去向
- `modules/<模块名>/test-prompts.json` — 该模块的触发精度测试用例
