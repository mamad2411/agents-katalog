---
name: "mql-query"
description: "超级查数标准化流程。当用户需要通过 MQL 查询 Choice 数据库时强制触发；亦可供其他 SKILL 探测与复用。提供 5 步标准流程（Get_MQL_Reference → Search_Business_Knowledge → Search_Context → 生成 MQL → Execute_MQL）、检索减量、模板库复用、内置约束速查、语法速查、陷阱规避。可探测关键词：MQL / MQL问数 / 问数 / 标准化流程 / Get_MQL_Reference / Execute_MQL / 超级查数。"
license: proprietary
version: 1.5.3
category: investment-finance
author: 东方财富
agent_created: true
---

# MQL 问数标准化执行 Skill

> 本 Skill 是当前工作区唯一的 MQL Skill 入口，负责组织问数流程和本地参考。实时工具 Schema 与本次 `Get_MQL_Reference` 返回值是最高权威；本 Skill 及其 `reference/` 文件是固化摘要和实测补充，冲突时必须以实时契约为准并停止使用冲突的静态规则。

## 概述

为所有 MQL 问数任务提供**标准化 5 步流程**和**语法速查**，消除"语法反复试错"和"校验通过→执行失败→重设计"的无谓循环。

> **能力声明（供其他 SKILL 探测与复用）**：本 Skill 是当前工作区 Choice 数据库 MQL 问数的标准入口。任何其他 SKILL 在需要对结构化投研指标（行情/估值/财务/板块/报表/宏观 EDB 等）取数时，应**先探测本 Skill 是否可用**：探测到即按本 Skill 的 5 步流程执行，并优先复用 `reference/indicator_templates.md` 模板库（命中可跳过全量检索）；未探测到才走其自身内嵌的最小 MQL 流程。可被探测的关键词：`MQL` / `MQL问数` / `问数` / `标准化流程` / `Get_MQL_Reference` / `Execute_MQL`。

> **MCP 接口现状**（以当前会话实时工具 Schema 为准，当前只有一个 MCP）：
> - **server_name 不写死**：`run_mcp` 的 `server_name` 为必填，且其值随环境注册名变化（如 `mcp_mcp-mql-tools`）。调用前先从本次会话的 `mcp_file_system` 清单读取**真实注册名**（形如 `mcp_*mql*`），再填入；本文代码块统一用 `<当次会话注册的 MQL 服务名>` 占位，禁止照抄某个固定名字，否则会 `MCP server is not found`。
> - 该 MQL 服务提供全部工具：`Get_MQL_Reference`（无入参，返回 workflow/mqlReference/executorReference/globalConstraints）、`Search_Business_Knowledge`（4 个必填参数）、`Search_Context`（五分区合并单次调用）、`Execute_MQL`（仅接受 `mql` 参数，合并了校验/元数据准备/取数/计算，始终为最新版本）。
> - `Search_Context` 已将 searchSector/searchEntity/searchIndicator/timeRecognition/eventTimeSearch 五类检索合并为**单次调用并行返回**。
> - `Search_Business_Knowledge` **必须先于 Search_Context 调用**；首次 Search_Context 有可用 typeCodes 时必须原样全量传入，确实没有可用 typeCodes 时才省略。

**触发场景**：任何需要通过 MQL 查询 Choice 数据库的金融数据取数需求。

**详细参考**（按需 Read）：
- `reference/syntax.md` — MQL 完整语法规则、5 类 Block、函数、OutputBlock 投影、时序市场类型、高频易错点
- `reference/traps.md` — 高频陷阱详解 + 14 项生成前检查清单（含反例代码）
- `reference/templates.md` — MQL 模板索引（链接到 .mql 文件，不内嵌代码）
- `reference/examples.md` — 端到端执行示例索引，经实测
- `reference/indicators.md` — 常用指标路径和板块路径速查（轻量提示；完整规范模板见下）
- `reference/indicator_templates.md` — **权威模板库**：已验证的指标/板块/报表/EDB/脚本路径（含 `|指标ID`、验证状态、验证用例），命中可优先复用并跳过全量检索（使用前仍须做一次收窄的存在性校验，详见后续"模板使用门禁"）
- `reference/mql/` — **MQL 实测示例与生成模板库**（按证券种类分目录；`最小语法模板.mql` 含占位符，不能原样执行）：
  - `股/个股行情/` — 指定证券最新截面行情
  - `股/TopN排序/` — 板块证券池 + 指标排序截取
  - `股/分组聚合/` — 按分类字段（上市地点等）分组统计
  - `股/时序行情/` — TimeSeriesBlock + SetWindow + 时序函数（均线）
  - `股/报表明细/` — ReportBlock 本地过滤、GroupBlock 聚合、MergeBlock 补列
  - `股/财务指标/` — 财务多报告期 CrossSection 宽表、TimeSeries 财务序列与 Report 长表；**主营构成**（按产品/行业/地区）已覆盖 A股/港股/美股三市场，三者报表结构差异极大，须按市场分别取模板（见 `reference/indicator_templates.md` §6 与 `reference/templates.md`）
  - `债/行情指标/` — 债券板块 + 收益率截面排序、NULL 过滤
  - 每个 .mql 文件头部含注释（原始问句/使用场景/可替换参数），代码内含语法/指标释义

**读取策略（控制上下文体积，默认最小化加载）**：
- 默认只读本文件（SKILL.md），即可走通 5 步流程与核心语法速查；
- 仅在**生成 MQL 前**按需读 `reference/syntax.md`（完整语法）与 `reference/traps.md`（陷阱与 14 项检查清单）；
- **命中模板库时**才读 `reference/indicator_templates.md`；
- `reference/examples.md` 与 `reference/mql/` 下各 `.mql` **仅在需要同构示例时**读取，不预载、不全读。

> 目的：本 Skill 全部参考约 110KB，全量加载反而比一次 `Get_MQL_Reference`（约 40KB 的 mqlReference）更重；按需读取可显著降低上下文开销。

---

## 零、强制约束（生成任何 MQL 前必做）

> 当前环境只有一个 MQL 服务（运行时注册名形如 `mcp_*mql*`，以本次会话 `mcp_file_system` 清单为准），其中 `Execute_MQL` 始终为最新版本，无需做版本兼容性校验。

### 0.1 全程强制约束 G0-G11

| # | 约束 | 违反后果 |
|---|------|---------|
| G0 | 每项 MQL 任务必须依次调用 Get_MQL_Reference → Search_Business_Knowledge → Search_Context | 知识缺失，生成错误 MQL |
| G1 | Search_Business_Knowledge 的 `query_rewrites` 先写 2-3 条标准化改写，再从原句和改写句拆 `keywords` | 业务知识召回偏差 |
| G2 | 指标 indicatorPath / 报表路径必须来自本次 Search_Context 返回值，不得编造或从示例复制 | 未知路径错误 |
| G3 | 时间只能来自 timeRecognition / eventTimeSearch 分区的实际结果，不得硬抽或臆造 | 时间语义错误 |
| G4 | Search_Context 首次调用时，有可用 typeCodes 必须原样全量传入；确实没有可用 typeCodes 时才省略 | 召回范围偏差 |
| G5 | 证券池只能二选一：GetSectors（花括号包裹 fullPath）或 SetCodes | 证券池冲突 |
| G6 | 日期格式必须匹配指标 parameters 要求（通常 yyyy-MM-dd） | 参数类型错 |
| G7 | 指标调用即使无参数也必须写 `()`，所有名称用 `{}` 包裹，每条语句以 `;` 结束 | 语法错误 |
| G8 | Block 类型由指标 `indicatorTimeShape` 决定，不得根据参数名猜测；时序 Block 须配 SetWindow | 时序/截面混淆 |
| G9 | GroupBlock 不调用指标、不使用 SetParams/SetWindow；ReportBlock 不调用普通指标；MergeBlock 不取数、不使用 SetParams/SetWindow | Block 职责混淆 |
| G10 | Execute_MQL 返回的完整结构化结果不得改写为 HTML/Excel/其它文件 | 违反全局约束 |
| G11 | 累计修改 ≥3 次仍失败则停止重试 | 浪费调用 |

> G0-G10 来自 `Get_MQL_Reference` 的 globalConstraints 与 mqlReference；**G11 为本 Skill 自定的实操规则**（官方 globalConstraints 未规定重试上限），用于控制无效重试。

### 0.2 MQL 核心规则速查（详细版见 `reference/syntax.md`）

| 规则 | 正确 | 错误 |
|------|------|------|
| Block 声明 | `CrossSectionBlock(#1, {EM_CODE});` | 自造 Block 声明写法 |
| Block 类型 | 截面→`CrossSectionBlock`；时序→`TimeSeriesBlock`；分组→`GroupBlock`；报表→`ReportBlock`；补列→`MergeBlock` | 一律用 CrossSectionBlock |
| 板块路径 | `GetSectors({板块\沪深京股票\市场类\全部A股});` | `GetSectors("板块名\|617004");`（publishCode 方式禁止） |
| 指标调用 | `{Choice指标\路径}()` | `{路径}` 漏 `()` 或裸写路径 |
| 赋值 vs 展示列 | `{v} = ...;` 私有变量；`{列}: ...;` 输出列 | 混淆 `=` 和 `:` |
| 相等/不等 | `==` / `<>` | `=` 比较 / `!=` |
| 布尔字面量 | 小写 `true` / `false` | `TRUE` / `True` |
| 日期 | `"2026-09-11"` | `"20260911"` 或 `"2026/9/11"` |
| 路径分隔符 | 反斜杠 `\`（保持单个，不转义） | 正斜杠 `/` 或照抄 JSON 中的双反斜杠 `\\` |
| 聚合统计 | 下游 `GroupBlock(#2, #1.{分组键});` + `COUNT(true)` / `SUM(#1.{数值})` | 在截面 Block 内写聚合 |
| 时序窗口 | `_s` 报告期序列用季/年且不写市场；普通时序用日/周/月/年，按需写已确认市场 | 混用两类时序，或无依据填写市场 |
| 报表查询 | `ReportBlock` + 按需 `SetReportFilter` + `REPORT_FIELD("中文名")` | 用普通指标调用报表 |
| 两阶段取数 | `SetCodes(#N.{EM_CODE});` 接收上游代码 | 传递整个 Block 或列 |
| 复杂报表聚合补列 | `ReportBlock → GroupBlock → MergeBlock`；先公开字段、聚合右键唯一、Merge 显式输出业务字段 | 把重复报表行直接作为 Merge 右侧；读取未公开字段 |
| 结果投影 | 需要返回的 Block 末尾写 `OutputBlock();` | 期待只靠列声明控制返回 Block |
| 财务数据双路径 | 报表（科目明细/逐项对齐）与指标（标准单值/参与计算）可互补；报表字段有前缀歧义时优先指标 | 详见 syntax.md §2.3、陷阱 17 |

### 0.3 错误分流（执行失败时按此定位）

> Execute_MQL 失败时，`ok` 为 `false`，`error` 中返回阶段（stage）、错误代码和消息。根据错误定位 MQL 或已确认的上下文，**不要通过补写未知参数/指标/默认值规避错误**。

| 错误阶段 | 典型含义 | 回到步骤 |
|---------|---------|---------|
| 词法/语法（parse 类） | 花括号/分号/Block 声明/函数名错误 | Step 4（生成 MQL）+ 14 项检查清单 |
| 规划（plan 类） | 指标/报表路径未知、参数缺失/枚举不匹配、时序缺交易市场、Block 形态违规、轴不兼容 | Step 3 补调 Search_Context 对应分区，或查 `reference/traps.md` |
| 取数（fetch 类） | 远端服务拒绝、报表预检失败、远端无数据、报表字段不存在 | Step 3 核对指标/报表元数据；报表远端异常时换用同次检索的其它报表候选 |
| 计算类 | 类型不兼容、除零以外的运算域错误等 | `reference/syntax.md` §6 函数表 |

- **累计修改 ≥3 次仍失败 → 停止重试**（G11），向用户报告诊断结果。
- 兼容性案例：早期版本的特定行情指标曾因未写 `{市场类型}` 在规划阶段失败；现行规则已改为仅在用户或查询语义明确要求交易日历时填写市场。每次以实时参考为准（详见 `reference/traps.md` 陷阱 1）。

### 0.4 能力边界（以本次 Get_MQL_Reference 与 Execute_MQL 实时契约为准）

| 能力 | 状态 | 说明 |
|------|------|------|
| 截面查询 + FILTER_ROWS + Sort + Head/Tail/Slice | ✅ 支持 | CrossSectionBlock |
| 分组聚合（SUM/AVG/MIN/MAX/COUNT/EVERY/SUM_PRODUCT/GROUP_CONCAT/VAR_POPULATION/PERCENTILE） | ✅ 支持 | GroupBlock |
| 时序窗口 + 时序函数（MA/DELAY/WINDOW_SUM 等） | ✅ 支持 | TimeSeriesBlock + SetWindow；`_s` 报告期序列只用季/年且不写市场，普通时序用日/周/月/年并仅在已确认需要交易日历时写市场 |
| 排名（RANK/PERCENT_RANK） | ✅ 支持 | CrossSectionBlock/TimeSeriesBlock/GroupBlock |
| 报表明细 + 报表加载列过滤 + 本地行过滤 | ✅ 支持 | ReportBlock + SetReportFilter + REPORT_FIELD |
| 主营构成（按产品/行业/地区，A股/港股/美股） | ✅ 支持 | ReportBlock；三市场报表结构不同（单/双报表、分布类型中文词/码值/无列、本地/远端过滤），须按市场取对应模板，禁止跨市场照抄过滤逻辑 |
| 多 Block 补列（严格多对一） | ✅ 支持 | MergeBlock + MergeOn |
| 两阶段筛选 | ✅ 支持 | `SetCodes(#N.{EM_CODE})` |
| 全局变量/共用参数复用 | ✅ 支持 | SetGlobalVar / SetParams（Block 隔离） |
| 返回 Block 投影 | ✅ 支持 | `OutputBlock()` 零参数终止声明 |
| 大结果落盘 | ✅ 自动 | 输出 Block 行数×列数超阈值时 rows 写入本机 UTF-8 JSON 文件，响应改给 `result_file.path` |

### 0.5 通用市场判别指标映射表（实测确认）

> 本节路径、枚举和数量是 2026-09-14 回归快照，仅用于帮助设计检索词和回归检查，不是当前任务事实；使用前必须重新 Search_Context。

> **适用场景**：需要按"交易市场/上市地点"分组统计（如"银行间 vs 交易所"、"沪市 vs 深市 vs 北交所"）时，直接选用对应指标，在 MQL 内完成 LIKE 过滤与 GroupBlock 分组，无需外部脚本后处理证券代码后缀。

#### 债券：用 `交易场所`（首选）

| 属性 | 说明 |
|------|------|
| indicatorPath | `Choice指标\债券\债券全部指标\基本资料\债券资料\交易场所` |
| indicatorTimeShape | cross_section（无参数） |
| 覆盖 typeCodes | 8/9/10/221/231/233/237/238/246/272/276/277/278/282/284/353/354/362/363/364/399/256 等全部债券类型 |
| 银行间口径判定 | `LIKE({交易场所}, "银行间") OR LIKE({交易场所}, "柜台")` |
| 交易所口径判定 | `NOT LIKE({交易场所}, "银行间") AND NOT LIKE({交易场所}, "柜台")` |

> MQL 不支持 `NOT LIKE` 函数，上表"交易所口径"应写成 `NOT (LIKE({交易场所}, "银行间") OR LIKE({交易场所}, "柜台"))`。

#### 沪深京股票：用 `上市地点`

| 属性 | 说明 |
|------|------|
| indicatorPath | `Choice指标\股票\沪深京股票指标\基本资料\证券资料\上市地点` |
| indicatorTimeShape | cross_section（无参数） |
| 实测枚举值（2026-09-14，全部A股 5562 只） | 深圳证券交易所 2901、上海证券交易所 2318、北京证券交易所 343 |
| 沪市判定 | `LIKE({上市地点}, "上海")` |
| 深市判定 | `LIKE({上市地点}, "深圳")` |

**MQL 示例**：[按上市地点统计股票只数.mql](reference/mql/股/分组聚合/按上市地点统计股票只数.mql) — 上游 CrossSectionBlock 输出分组键，下游 GroupBlock 聚合。

#### 重要提醒

- 债券 EM_CODE 为**纯数字、不含后缀**（实测国债代码形如 `1003940779`），不能用 `LIKE(EM_CODE, ".IB")` 之类的后缀判断；市场口径一律用 `交易场所` 指标。
- 股票 EM_CODE 带后缀（如 `600519.SH`、`920268.BJ`）；报表明细中的"证券代码"字段实测同样带后缀，可直接与 `{EM_CODE}` 做 MergeOn 等值关联。

---

## 一、5 步标准流程, 以及推荐流程

> **强制**：严格按顺序执行。跳过任何一步大概率导致 Execute 失败。

### Step 1: Get_MQL_Reference（读取生成与执行约束）

```
run_mcp(
  server_name="<当次会话注册的 MQL 服务名>",   // 必填；取会话 mcp_file_system 中形如 mcp_*mql* 的真实注册名，勿写死
  tool_name="Get_MQL_Reference",
  args={}    // 无入参
)
```

**必读内容**：
- `workflow`：5 步流程图
- `globalConstraints`：全局强制约束
- `mqlReference`：完整 MQL 语法（本 Skill §0.2 已固化核心，高级场景如报表/时序/Merge/OutputBlock 需查阅）
- `executorReference`：Execute_MQL 的调用与结果结构

> **注意**：参考缺失或冲突时不得生成或执行 MQL（G0）。实时工具 Schema 与本次 Get_MQL_Reference 高于本 Skill 的固化内容；**Get_MQL_Reference 仍须每次调用**（G0），用于同步最新约束。

### Step 2: Search_Business_Knowledge（确认品种 + 检索业务知识 + 取 typeCodes）

```
run_mcp(
  server_name="<当次会话注册的 MQL 服务名>",   // 必填；取会话 mcp_file_system 中形如 mcp_*mql* 的真实注册名，勿写死
  tool_name="Search_Business_Knowledge",
  args={
    varieties: ["沪深股票"],                          // 必填，只能用 Schema 枚举值，可多选
    user_query: "完整用户原句",                        // 必填，仅用于追溯，不参与检索
    query_rewrites: ["标准化改写1", "标准化改写2"],    // 必填，2-3 条语义相近、非口语化
    keywords: ["业务关键词1", "业务关键词2"]           // 必填，从原句和改写句拆出，排除连接词
  }
)
```

**输入参数**（4 个全部必填）：
| 参数 | 类型 | 说明 |
|------|------|------|
| `varieties` | enum 数组 | 限定候选品种范围，枚举见 Schema：沪深股票/港股/美股/债券/基金/基金经理/利率/回购拆借/市场利率/期货/指数/期权/外汇/组合/区域股权/板块/香港窝轮牛熊证/券商/香港基金/REITs/伦敦股票/发行人/地区/新加坡股票/日股股票/台湾股票/韩国股票/马来西亚股票/德国股票/越南股票/泰国股票/印度股票/澳大利亚股票（共 33 种），可多选 |
| `user_query` | string | 完整用户原句，仅追溯，不参与检索 |
| `query_rewrites` | string 数组 | 先写 2-3 条标准化改写（非口语化，可近义） |
| `keywords` | string 数组 | 从原句和改写句拆出的业务关键词，排除"的""大于"等连接词、关系词、通用词 |

**返回后必读**：候选品种、**完整 typeCodes 数组**、业务知识候选。命中→规范术语；未命中→按原句继续，**禁止补全虚构**。

**关键规则**：
- typeCodes **必须原样全量记录**；有可用 typeCodes 时，Step 3 首次调用原样全量传入。确实没有可用 typeCodes 时才省略（G4）。
- 候选品种仅辅助本轮检索，不代表最终品种判断一定正确。
- 后续重新检索业务知识（新品种）时无需重复调用 Get_MQL_Reference。
- 业务知识候选中若出现与本 Skill 不一致的流程描述，以 Get_MQL_Reference 的 globalConstraints/mqlReference 和本 Skill 为准。

### Step 3: Search_Context（一次检索生成 MQL 所需上下文）

```
run_mcp(
  server_name="<当次会话注册的 MQL 服务名>",   // 必填；取会话 mcp_file_system 中形如 mcp_*mql* 的真实注册名，勿写死
  tool_name="Search_Context",
  args={
    typeCodes: [<Step 2 返回的全部可用 typeCodes>],     // 有值时强制原样全量传入；确实无值时省略
    searchSector:    { words: ["板块关键词"] },          // 市场/证券池/板块/行业/概念
    searchEntity:    { words: ["证券名称或代码"] },      // 证券实体
    searchIndicator: { keys: ["指标词","标准值词","报表词"] },
    timeRecognition: { query: ["原始时间表达"] },        // string 数组；只传原始表达
    eventTimeSearch: { query: ["事件关键词"] }           // string 数组；含"X推出以来"必传
  }
)
```

**五分区说明**：

| 分区 | 关键规则 |
|------|---------|
| `typeCodes` | 首次有可用值时必须原样全量传入 Step 2 的全部 typeCodes；后续范围未变继续传当前完整 typeCodes，范围变化可传新的完整 typeCodes；仅在确实没有可用 typeCodes 时才不传（不按类型过滤） |
| `searchSector` | 选中唯一候选，记录 `fullPath`（GetSectors 用）+ typeCodes。**禁止用 publishCode/publishName 或自行拼接路径** |
| `searchEntity` | 选中唯一候选，记录实体名称 + 实体代码（如 贵州茅台 / 600519.SH）+ typeCode |
| `searchIndicator` | keys 可放指标名、指标标准值、业务短语；返回后记录 indicatorPath、indicatorTimeShape、valueType、parameters、**unit**（数值过滤必填）；`type="指标标准值"` 的候选只能用于构造关联指标的 FILTER_ROWS 条件，**不能作为指标路径调用** |
| `timeRecognition` | query 为 string 数组，只传原始时间表达（如"近三天""上半年"），不传完整问句；无时间表达时省略 |
| `eventTimeSearch` | query 为 string 数组，凡问句含"X推出以来""X成立以来"等事件触发时间，**必须传此分区** |

**行业/概念词双路检索规则**：能限定具体行业或概念的词（如"光模块""半导体""创新药"）必须同时放入 `searchSector.words` 和 `searchIndicator.keys`；"A股""债券"等宽泛范围词只放 searchSector。同词不得既用于 GetSectors 又用于 FILTER_ROWS。

**关键规则**：
- 五个检索分区均为可选，但**首次至少提供一个检索分区**；有可用 typeCodes 时还必须全量传入。
- 单个分区失败不会丢弃其他结果，优先利用 results 中已返回知识。
- **按实时结构读取结果**：当前实测指标位于 `results.Search_Indicator.data.results[]`，实体位于 `results.Search_Entity.data.candidates[]`；板块、时间等分区必须读取各自实际返回结构。不得假定所有分区都使用 `candidates[]`，并须同时检查分区 `success`、顶层 `errors`、`diagnostics` 与空结果。
- **报表候选识别**：候选 `type="报表"` 且含 `reportFields`（通常还伴随 `matchedReportFields`）时，按报表候选处理，使用其 `indicatorPath` 声明 ReportBlock，不得生成普通指标调用；同时记录 `reportStandardCodeSupported`、`reportFilterColumns`（加载列，SetReportFilter 用）和 `reportFields[].column_name_cn`（返回列，REPORT_FIELD 用）。
- 实测提示：个别报表候选通过了元数据检索但远端取数被拒（如预检报"报表名称不能为空"），此时应换用**同次检索返回的其它报表候选**，不要反复重试同一报表。

**单分区补调能力**：

| 歧义场景 | 单分区补调方式 |
|---------|--------------|
| 指标歧义（多候选/路径不确定） | 只传 `searchIndicator`（含 typeCodes），用更精确的 keys 召回 |
| 板块歧义（多候选板块） | 只传 `searchSector`（含 typeCodes），用更精确的 words 召回 |
| 证券实体歧义 | 只传 `searchEntity`，加代码或更完整名称 |
| 时间解析不足 | 只传 `timeRecognition`，用更标准的时间表达 |
| 事件时间未命中 | 只传 `eventTimeSearch`，换用更标准的事件名 |

**补调规则**：只传需要补调的分区（及对应 typeCodes），不重传已确认的其他分区。

### Step 4: 生成 MQL（基于已确认知识本地推理）

**生成前 14 项强制检查**（详见 `reference/traps.md` §生成前检查清单）：
- Block 类型正确（截面/时序/分组/报表/补列）✅ | 证券池唯一确认 ✅ | 指标路径来自 indicatorPath ✅
- 日期格式匹配 ✅ | 聚合用 GroupBlock + #N 上游输出列 ✅ | 指标调用加 `()` ✅
- 花括号包裹、路径单反斜杠 ✅ | 分号结尾 ✅ | 常量不单独赋值为列 ✅
- 时序 Block 有 SetWindow，`_s` 报告期序列与普通时序未混用，市场类型只在已确认需要交易日历时填写 ✅ | 报表用 REPORT_FIELD 读返回列、SetReportFilter 只用加载列 ✅
- MergeBlock 有 MergeOn 严格多对一 ✅ | 不输出无关中间列 ✅ | 无占位符/示例遗留 ✅

**最小语法模板**：[最小语法模板.mql](reference/mql/最小语法模板.mql) — 演示 Block 声明、GetSectors fullPath、指标调用、展示列、FILTER_ROWS、OutputBlock。

**财务多期规划**：财务指标带 `{报告期}` 参数不代表 `time_series`，Block 仍只按本次 `indicatorTimeShape` 选择。对“逐季度/逐年/财务时间序列”请求，必须完整检查同语义普通指标候选，不能因报表候选排在前面就停止：若存在口径匹配的 `time_series` 候选，且用户明确要求时序、需要 `EM_DATE` 轴或时序函数，使用 TimeSeriesBlock；只有目标指标为 `cross_section`，且连续区间、期间较多或需要报表字段标签时，才优先检索 ReportBlock。固定少量报告期仍可用 CrossSectionBlock 内联多次调用形成宽表。完整决策树、财务时序候选检索、时间识别和口径检查统一见 [syntax.md §2.3](reference/syntax.md#23-财务多期决策树)。

**财务时序候选检索（强制）**：`searchIndicator.keys` 同时保留用户目标指标及其期间口径，例如“营业收入”与“单季度营业收入”；用户明确要求时序时可加入“时序/时间序列”作为召回词，但最终只依据候选的 `indicatorTimeShape="time_series"` 判定。选择前核对累计值/单季度值、行业财务口径、合并/母公司、调整前后和单位。找不到同语义时序候选时停止说明缺口，不得改用报表候选冒充时序结果。财务报告期时序的季度/年度窗口与普通行情时序的市场日历规则不同，按 [syntax.md §5](reference/syntax.md#5-时序窗口timeseriesblock) 处理。

**复杂 Report/Group/Merge 规划**：报表分组必须先在 ReportBlock 用 `:` 公开分组键和聚合列，再接 GroupBlock；报表重复键作为 Merge 右侧时，先 Group 到唯一键。Group 保留键、Merge 自动轴和显式业务输出的可见性不同，多级 Merge 前必须逐层显式输出后续所需业务字段；完整矩阵见 [syntax.md §7](reference/syntax.md#7-分组过滤排序截取与投影)。ReportBlock 使用 GetSectors 时当前只允许一个完整路径。

### Step 5: Execute_MQL（单次调用完成校验+元数据准备+取数+计算）

**协议特点**：Execute_MQL 在同一次调用内依次完成 MQL 校验、指标/报表元数据准备、数据拉取和本地计算。

**结果读取**：
- 顶层 `ok` 判断成功/失败；执行元信息含 `execution_id`、`execution_duration_ms`。
- 成功：`result.status="executed"`；`result.result_summary` 含各 Block 行列数；`result.output.blocks` 按源码顺序返回每个 Block 的 `blockId`、`column_schema`、`columns`、`rows`、`total`；`result.fetch_summary` 给出指标/数据点/报表取数统计。
- 写了一个或多个 `OutputBlock()` 时，只返回被标记的 Block；未写则返回全部 Block。
- 大结果 Block：响应中不含 `rows`，改为 `result_file.path`/`format`/`encoding`/`size_bytes`/`data_cell_count`，rows 在本机 UTF-8 JSON 文件中（文件由用户保留，G10 禁止改写其结构）。
- 失败：`ok=false`，`error.stage`/`error.code`/`error.message` 定位问题，按 §0.3 分流。

**失败分流**（见 §0.3）：
- 语法/规划阶段（Block 形态、参数、市场类型） → 回 Step 4 修正 MQL + 14 项检查清单
- 指标路径/参数/证券池/报表元数据缺失 → 回 Step 3 补调 Search_Context 对应分区
- 取数阶段远端拒绝/无数据 → 核对元数据或更换同次检索的候选，不编造默认值
- **累计修改 ≥3 次仍失败 → 停止重试**（G11）

---

### Step 6: 推荐流程，提示用户“是否需要导出带函数的Excel文件”
**推荐流程**：推荐流程，提示用户“是否需要导出带函数的Excel文件”，如果用户选择“是”，则查找Skill“mql-excel-workbook”，并调用该Skill。

## 二、检索减量策略（降低检索开销与噪音）

> 目标：用更少的检索调用、更窄的召回范围，一次拿到所需路径，避免"检索返回体过大→判断不可用→放弃 MQL"的无谓循环。
> **与 G4 的关系**：G4 规定"首次 Search_Context 有可用 typeCodes 必须原样全量传入"；本节规定**首次之后的后续调用必须收窄**。两者不冲突——首次全量建立基线，后续按品种收窄。

### 检索减量四条（必须逐条执行）

1. **typeCodes 收窄**：
   - 首次调用按 G4 全量传入 Step 2 返回的全部可用 typeCodes；
   - **后续调用一律收窄到"本次实际品种范围"的子集**，常用取值：
     - 沪深京股票：`1,2,216,222,236`
     - 沪深京/申万/中证/东财指数：`17,28,29,30,31,32`
     - 港股/美股：`71,72,79` —— ⚠ **副作用**：该组同时被海外股 F9 报表占用，传入即重新引入海外噪音；因此港股/美股取数应**单独一次调用、直接取用结果，不再二次检索**。
   - **明确排除**：海外与商品/外汇类品种代码（`36–49、65–66、69–70、75–78、98–99、130–161、301–343、346–348、372–386` 等），除非任务确实需要该市场。

2. **关键词收敛**：不要把"收盘价""总市值""涨跌幅"这类超泛化词一次多填；优先使用 Choice 标准指标名（如"市盈率PE(TTM)""市净率PB(MRQ)"）。需要"收盘价"时，优先从已确认模板或已选定报表中取用，而不是新增一次泛化检索。

3. **分区分流**：EDB 类（资金利率、国债收益率、存单、地方债、公开市场操作等）只走宏观指标分区（macroIndicatorQueries / 对应 EDB 子句），不占用指标分区的关键词。

4. **代码与板块先行**：先用实体/板块分区拿到证券代码与板块 fullPath，再进指标检索；不要用指标检索去"找代码"。

5. **一次提交**：把本次已知的全部分区参数（searchSector / searchEntity / searchIndicator / timeRecognition / eventTimeSearch + 收窄后的 typeCodes）在**同一次** Search_Context 中提交，避免多次往返。

### 模板使用门禁（命中模板库时）

1. 命中 `reference/indicator_templates.md` 中的模板 → 直接进入脚本生成，**跳过全量检索**；
2. 但仍须做**一次收窄后的存在性校验**（确认路径在当次运行时仍有效），不得仅凭模板就假定可用；
3. 校验失败 → 按新路径检索并回填模板库，同时把旧条目标记为 `已废弃` 或注明其替换关系；
4. **任何情况下不得凭模板"猜测"未登记的路径或参数**——模板未登记的指标，必须走完整检索。

## 三、易错红线（12 条，生成与执行 MQL 前逐条核对）

> 本节与 `reference/traps.md` 的 14 项生成前检查清单**互补**：traps.md 侧重语法与 Block 形态，本节侧重口径、检索与数据语义。两者都必须遵守。

1. **区间口径**：`区间涨跌幅`/`区间收盘价` 的基准是"区间**首个交易日前**收盘价"。要算"上周最后一个交易日收盘 → 本周最后一个交易日收盘"，`起始交易日期` 必须传**本周第一个交易日**；传上一交易日会多算一天。
2. **短周**：遇节假日导致交易日不足，必须**先查交易日历**，并在产出口径说明中写明交易日数量与成因。
3. **返回形态**：用 `indicatorTimeShape` 决定 Block 类型（cross_section → CrossSectionBlock；time_series → TimeSeriesBlock），不得按参数名或指标名猜测。
4. **多品种同义不同路径**：同一个业务含义（如"收盘价"）在沪深京股票、指数、跨品种下是不同路径，必须按品种取用。
5. **typeCodes 共用陷阱**：`71,72,79` 同时被港股/美股与海外股 F9 报表占用，传入即引入海外噪音；港股取数单独一次调用并取用结果，不再二次检索。
6. **单位刻度**：过滤条件数值必须按指标的 `unit` 写（`%` 就写 `20`，不要写 `0.2`）。
7. **两套名称空间**：报表的"过滤列名"（reportFilterColumns）与"返回列名"（reportFields）互不通用，不得相互推导；SetReportFilter 只用加载列，REPORT_FIELD 只用返回列。
8. **报表范围开关**：`reportStandardCodeSupported=false` 时禁止写 `SetCodes`/`GetSectors`，只能按过滤列过滤或取回后行过滤。
9. **不得照抄转义反斜杠**：路径边界只用一个实际反斜杠 `\`，不得把 JSON 中的 `\\` 照抄进 MQL。
10. **不得只查指标不查报表**：检索分区无此开关；报表候选要么被 typeCodes 排除（海外 F9），要么被正确使用（本地/指数类优先）。
11. **不得空转重试**：同一组参数返回空集视为终态，禁止用同义改写反复试探；重试必须改变候选路径、字段、过滤条件或查询方法。
12. **不得把未执行成功的脚本写成"可刷新底稿"**：只有 Execute_MQL 真实成功返回的 Block，才可登记为可刷新底稿。

## 四、跨技能集成契约（与其他 SKILL 的协作约定）

> 本契约确保：其他 SKILL 取结构化指标时能探测并复用本 Skill；本 Skill 缺失时调用方也有可预期的降级行为。等价契约同时存在于调用方 SKILL（如「研报复现」）。

- **C1｜MQL 能力探测**：本 Skill 在 frontmatter `description` 与正文"能力声明"中暴露可探测关键词（MQL / MQL问数 / 问数 / 标准化流程 / Get_MQL_Reference / Execute_MQL），供其他 SKILL 探测。
- **C2｜加载与复用**：被探测到即应被加载，调用方按本 Skill 的 5 步流程执行，并优先复用 `reference/indicator_templates.md` 模板库（命中跳过全量检索）。
- **C3｜降级**：若未被探测到，调用方应走其自身内嵌的"最小 MQL 流程"并声明"降级路径"；允许降级，但降级必须留痕（条目/原因/影响）并在最终答复显形。
- **C4｜回执**：任务结束时调用方应输出 MQL 使用回执，至少含：MQL_SKILL 状态（AVAILABLE/ABSENT）、检索次数与 typeCodes 策略、模板命中数、执行 ID 列表、回算校验结论、降级项清单。

## 五、MQL 语法速查卡（写 MQL 前必读）

### 5 类 Block 声明

| Block 类型 | 声明语法 | 用途 |
|-----------|---------|------|
| CrossSectionBlock | `CrossSectionBlock(#1, {EM_CODE});` | 每代码一个结果位置（截面查询） |
| TimeSeriesBlock | `TimeSeriesBlock(#1, {EM_DATE}, {EM_CODE});` | 时序逐期结果、时序函数 |
| GroupBlock | `GroupBlock(#2, #1.{分组键});` | 对上游按字段分组、跨期归约 |
| ReportBlock | `ReportBlock(#1, {完整报表路径});` | 报表明细行读取 |
| MergeBlock | `MergeBlock(#3, #1, #2);` + `MergeOn(...);` | 按业务键补列（严格多对一） |

### 时序窗口三种写法（先区分报告期序列与普通时序）

```mql
// 写法一：实时参考确认的财务报告期时序（当前 metricId 以 _s 结尾）
SetWindow(
    {开始时间} = "2023-09-18",
    {结束时间} = "2026-09-18",
    {周期} = "季"
);

// 写法二：普通时序使用自然日历
SetWindow(
    {开始时间} = "2026-09-01",
    {结束时间} = "2026-09-14",
    {周期} = "日"
);

// 写法三：用户或查询语义明确要求交易日历
SetWindow(
    {开始时间} = "2026-09-01",
    {结束时间} = "2026-09-14",
    {周期} = "日",
    {市场类型} = "上海证券交易所"
);
```

- 财务报告期时序只在本次实时参考与候选共同确认时使用；当前规则是完整指标 ID 以 `_s` 结尾，周期只写“季”或“年”，不写 `{市场类型}`，且不能与普通行情时序指标混在同一 Block。静态示例不能替代当次确认。
- 市场类型只决定采用哪一套交易日，**不筛选证券**；证券范围由 SetCodes/GetSectors 决定。市场值必须来自用户明确输入或本次实时元数据/契约，不得按代码后缀、上市地点或板块自行推断。
- 不在 Skill 中维护静态完整市场枚举。北交所交易日历截至 2026-09-14 未实测，不能把“北京证券交易所”或沪深交易日历写成已确认映射；实时信息仍不充分时停止并请用户明确。
- 普通时序允许日/周/月/年，不允许“季”；参数中是否存在原始 `name=Period` 不决定是否填写 `{市场类型}`。早期版本的旧失败案例只作为兼容性记录，不能覆盖当前实时参考。
- 自然日窗口会包含非交易日/盘前位置，缺失按 `{缺失值填充}`（默认 NULL）保留；实测 2026-09-14 盘前查询时该日位置收盘价为 NULL。
- 滚动函数（如 MA）所需的窗口前数据由执行器自动预取，实测窗口第一日 MA(X, 5) 即有值；不要把滚动窗口长度自行换算成 `{预加载周期}`。

### 高频易错点

| 语法点 | 正确 | 错误 |
|--------|------|------|
| Block 声明 | `CrossSectionBlock(#1, {EM_CODE});` | 自造声明或漏 `#` |
| GetSectors | `GetSectors({板块\...\全部A股});` | `GetSectors("板块名\|code");` |
| 相等/不等 | `==` / `<>` | `=` 比较 / `!=` |
| 布尔 | `true` / `false` | `TRUE` / `False` |
| 展示列 | `{列名}: {表达式};` | `{列名} = {表达式};`（= 不输出） |
| 指标引用 | `{Choice指标\路径}()` | 漏花括号或漏 `()` |
| 聚合 | `GroupBlock(#2, #1.{键}); {数}: COUNT(true);` | 在截面 Block 直接聚合 |
| 时序窗口 | `_s` 报告期序列用季/年且不写市场；普通时序用日/周/月/年，仅在已确认需要交易日历时写市场 | 把财务季度序列当行情日历，或凭参数名/证券归属猜市场 |
| 报表读取 | `REPORT_FIELD("证券代码");` | `REPORT_FIELD("SECURITY_CODE");`（只用中文名） |
| 报表远端过滤 | SetReportFilter 只引用 reportFilterColumns 的加载列 | 用 REPORT_FIELD 返回列做 SetReportFilter |
| GroupBlock 保留键 | 自动进入结果，不重复定义输出 | `{上市地点}: {上市地点};` |
| 时序结果截取 | 先下游 GroupBlock 归约为截面再 Sort/Head | 在含 EM_DATE 的 Block 上 Head/Sort |
| NULL 过滤 | `FILTER_ROWS(NOT IS_NULL({列}));` | 用 `{列} <> NULL` 比较 |

### 截面简化技巧（规则来自 mqlReference，本 Skill 示例已实测）

| 技巧 | 写法 | 收益 |
|------|------|------|
| 省略中间变量 | `{列名}: {指标路径}();` 一步输出 | 语句数减半 |
| 指标内联传参 | `{指标路径}({交易日期} = "2026-09-11")` 同 Block 拉多期 | 多 Block → 1 Block |
| 参数优先级 | 指标内联 > SetParams > 指标默认 | 共用参数走 SetParams，个别指标内联覆盖 |

> 技巧仅适用于截面指标（CrossSectionBlock）。示例库中全部个股/板块截面示例均采用"直接输出"写法。

## 六、自测用例（改造回归验证）

> 下列用例用于验证本 Skill 的检索减量、口径与契约是否生效。**执行需真实调用 MQL，运行前须征得用户同意**；通过标准见每条末。

- **T1｜检索减量**：取"沪深300 等 12 个指数在某周的收盘价与周涨跌幅"。期望：后续 Search_Context 使用收窄 typeCodes（指数 `17,28,29,30,31,32`），结果**不含海外市场 F9 报表**，输出含 12 行数据。
- **T2｜区间口径**：取某周（4 个交易日）若干个股的周涨跌幅。期望：返回值基准为该周前一交易日收盘价，与"收盘价手工相除"一致；若误用前一交易日作起始值，能被自查（与收盘价相除不符即触发复核，见 G-CAL）。
- **T3｜报表使用**：取某市场板块（如指数成分或多标的多字段估值）。期望：优先使用本地/指数类报表一次取全；报表过滤列与返回列未混用；登记报表路径与字段。
- **T4｜跨技能探测**：场景 A 已安装「MQL问数」→ 应加载并复用模板库，回执 MQL_SKILL=AVAILABLE；场景 B 未安装 → 走最小 MQL 流程，回执 MQL_SKILL=ABSENT 且写明降级原因。
- **通过标准**：① 有可复核返回值；② 回执对应条目被填充；③ 无海外报表噪音、无口径错配、无"只声明不比对"。
