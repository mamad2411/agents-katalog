---
name: stock-deep-research
description: 面向上市公司生成全面、体系化研究报告。本技能是「单家上市公司深度研究」的第一入口，优先级高于通用金融总览类技能：当用户要求对单家上市公司做深度分析、深度研究、个股分析、公司研究、公司一页纸、一页纸研究、股票研究报告，或要求覆盖公司近况跟踪、催化事件、券商核心推荐逻辑、业务拆分、产销链、供应链、研发实力、财务分析、盈利预测与估值等维度的个股分析时，务必第一时间优先加载本技能。
version: 2.7.3
agent_created: true
---

# 公司一页纸

为单家上市公司生成机构级中文「公司一页纸」研究报告。报告只做数据展示、业务归因与风险提示，不给投资建议、评级、目标价或股价方向判断。

> **本文件是入口与索引，不是全部内容。** 流程细则、数据契约、合规红线、脚本用法分别在 `reference/` 下的专项文档里（见文末 References）。
> 执行时**按需读取**对应文档，不要一次性加载全部。

## Scope

- 支持：沪深京证券（`.SZ` / `.SH` / `.BJ`）与港股（`.HK`）。
- 不支持：美股、其他市场、已退市公司、上市状态非正常的证券。遇到不支持对象时说明原因并停止，不输出半成品。
- 多公司请求：每家公司单独出一份报告，禁止合并成一份。

## 两条数据通道（各自独立、不可互换）

| 通道 | 负责的内容 | 入口 |
|---|---|---|
| 资讯检索（`mx_finance_search`） | **9 个章节的全部「文字描述部分」**（11 个场景） | 本会话直接调用 MCP 工具；11 个场景**无依赖 → 分 3 批并发（每批 3–4 个）** → 落盘 `raw/{scene}.json` → `scripts/news_api.py` 归一化 |
| MQL（妙想查询语言） | 章节 0 前置 + **3/4/5/6/7/8 的表格与图表数据** | **命中固化表** → 零检索直取（跳过两轮检索，只留 `Get_MQL_Reference` 做版本校验）<br>**未命中** → `Get_MQL_Reference` → `Search_Business_Knowledge` → `Search_Context` → `Execute_MQL` |
| 事件库（`mx_api_invoke`） | 章节 1「催化事件时间表」（已发生事件 + 预期事件） | 直接调用 `mx_api_invoke(apiId=newsEventSearch)`（已发生事件库）与 `mx_api_invoke(apiId=futureEventSearch)`（未来事件库）→ 落盘 `raw/事件库_*.json`；规程见 [reference/事件库-取数规范.md](reference/事件库-取数规范.md) |

章节 ↔ 来源的逐行对应表、零检索快车道、通道边界硬约束见 [reference/数据通道与来源对应.md](reference/数据通道与来源对应.md)。

## 执行主线（九步，完整版见 [reference/执行工作流.md](reference/执行工作流.md)）

1. **归一化输入**：代码必须带交易所后缀；4-5 位纯数字补港股五位，6 位走沪深京候选；名称换码必须走 MQL `searchEntity`，不得靠记忆。
2. **版本校验**：`Get_MQL_Reference` + 读 `Execute_MQL` 工具描述里的执行器版本；读不到版本即停止。
3. **查固化表决定取数路径**：[reference/MQL-报表路径固化表.md](reference/MQL-报表路径固化表.md)（或 `--list`）命中走零检索，未命中走完整检索。
4. **资讯检索取全 11 个场景**：分 3 批并发 → 落盘 `raw/{scene}.json` → `news_api.py --all --with-meta` 一次归一化为 `{{ZWSMSJ}}`；章节 1 催化事件时间表**另调事件库接口**（已发生事件库 `newsEventSearch` / 未来事件库 `futureEventSearch`，见 [reference/事件库-取数规范.md](reference/事件库-取数规范.md)）。
5. **按市场读分章节 MQL 清单**：沪深京 / 港股各一份；需换汇再读汇率规则。
6. **章节 3-8 的表格与图表只走 MQL**：**用 `--script <批次名>` 一次成型生成脚本（Block 编号连续、参数顺序固定），不手写 Block**；不得回退旧妙想中台 HTTP 接口或凭记忆补路径/参数/字段名。
7. **逐章生成**：只读该章 prompt；每章输入 = 该章资讯检索文本 + 该章 MQL 数据。
8. **渲染与校验**：`build_report.py` 渲染自包含 HTML → `validate_report.py` 校验；**P0 失败不得交付**；通过后用 `render_markdown.py` 由**同一份 `data.json`** 生成会话正文——**回复正文即报告内容本身**（章节 1-9 + 各表），另加 1 行文件指引。
9. **溯源**：资讯类内容挂 hover+click 溯源锚点（数据来自各章 `sources`）。

> 超时与重复调用：单次调用最长等待 1200 秒；同一 `query` 累计调用不超过 2 次；超时或非 0 退出码即停止本轮，禁止后台执行、禁止改写 `query` 或更换标的重试。

## 必须遵守的五条不变式

- **结构**：1-9 一级章节标题在任何数据情况下都齐全；二级小节/图表/正文在数据缺失时**整段不渲染**，且不输出任何解释性空状态（即"保留标题、仅不出正文"）。
- **无交付后记**：报告正文止于章节 9 与页脚，**禁止**在其后追加「数据缺口与口径声明」「交付说明」「未包装/未补数」等任何声明性后记（无论在报告内还是会话回复里）；数据缺失只体现为"整段不渲染"，口径说明只出现在版式内的表注/页脚，不向外另行声明。
- **会话回复 = 报告正文**：交付时的会话回复，正文部分必须是**与 HTML 同源同值的报告内容**——按 Markdown 输出章节 1-9（含章节 3 简介表、4.2 分板块表、7.2 主要财务指标表、8.1 一致预测表），推荐直接用 `scripts/render_markdown.py` 由同一份 `data.json` 生成；全文只允许再加 **1 行文件指引**（HTML 文件名）与**至多 1 行免责**。**禁止**把执行过程、校验结果、数据缺口/降级/口径说明、工具与报表名、交付话术写进会话回复。细则见 [reference/输出契约与数据契约.md](reference/输出契约与数据契约.md) §1。
- **8.1 一致预测表**：沪深京固定 **10 个指标行**（港股 9 行——无 `基准股本` 数据源），行名与行序逐字固定、**一行都不得少返回**；某期无值即**单元格留空、整行照常渲染**。
- **交付前校验**：`scripts/validate_report.py` 的 P0 全部通过才允许交付。

细则见 [reference/输出契约与数据契约.md](reference/输出契约与数据契约.md)；合规红线（禁目标价/评级、禁占位符与伪空状态、禁情绪化用词、零幻觉）与三级降级见 [reference/合规与降级.md](reference/合规与降级.md)。

## Scripts

五个脚本均为**必需**，且都在工作流中被直接调用：

| 脚本 | 职责 |
|---|---|
| `scripts/news_api.py` | 章节**文字描述**资讯归一化（算窗口 → 读 `raw/{scene}.json` → 窗口兜底 → 同源去重 → `showTime` 倒序 → `chunk` 拼接 → 落盘 `{{ZWSMSJ}}`）；**不发起网络请求**，检索由 Agent 调 `mx_finance_search` 完成 |
| `scripts/mql_api.py` | MQL 一次成型拼装 + 返回数据加工（单位换算 / 汇率折算 / "其他"客户供应商二次计算）；内置固化表注册表 `PINNED_REPORTS`、批次脚本 `SCRIPTS`、自检 `check_mql_script` |
| `scripts/build_report.py` | 从结构化 `data.json` 渲染自包含 HTML（CSS / SVG 图表 / 溯源码 `#srcdata` + JS） |
| `scripts/render_markdown.py` | 由**同一份 `data.json`** 渲染**会话正文 Markdown**（章节 1-9 + 各表，与 HTML 同源同值）；交付时直接作为会话回复正文，见 `输出契约与数据契约.md` §1 |
| `scripts/validate_report.py` | 交付前 P0 校验（章节齐全性、禁用词、占位符、伪空状态、评级/目标价、8.1 指标行齐全） |

```bash
PY=python

# 0) Agent 侧（检索）：分 3 批并发调用 mx_finance_search（每批 3–4 个场景，禁止逐个串行），
#    把返回条目结构化为 raw/1.json、raw/2.json、raw/3.1.json … raw/9.json

# 章节文字描述：一次归一化全部 11 个场景（推荐）
$PY scripts/news_api.py --company "宁德时代" --raw-dir "raw" --all --with-meta --out "text_宁德时代.json"

# —— 取数脚本一次成型（Block 编号自动连续 + 加载列参数顺序固定）——
$PY scripts/mql_api.py --scripts                                    # 列出全部脚本（批次）名
$PY scripts/mql_api.py --script 批次2 --code 300476.SZ --out mql_批次2.txt
$PY scripts/mql_api.py --script 批次3 --code 300476.SZ --report-date 2025-12-31
$PY scripts/mql_api.py --script 章节8  --code 09992.HK --market 港股
$PY scripts/mql_api.py --report 客户供应商 --code 300476.SZ --params   # 打印加载列固定顺序
$PY scripts/mql_api.py --check mql_批次2.txt                          # 语法自检
$PY scripts/mql_api.py --list                                        # 列出全部已固化报表

$PY scripts/build_report.py --input data.json --out "胜宏科技(300476.SZ)股票研究_20260922.html"
$PY scripts/validate_report.py --file "胜宏科技(300476.SZ)股票研究_20260922.html"
$PY scripts/render_markdown.py --input data.json --out "会话正文.md"   # 会话正文（与 HTML 同源同值）
```

脚本用法细则（脚本名与批次对应、自检项、待补项补录流程）见 [reference/取数脚本一次成型.md](reference/取数脚本一次成型.md)。

## References

| 文件 | 何时读取 |
|---|---|
| [reference/执行工作流.md](reference/执行工作流.md) | **每次任务开始必读**；九步完整流程、超时与重复调用约束、MQL 批次编排指针 |
| [reference/数据通道与来源对应.md](reference/数据通道与来源对应.md) | **每次任务开始必读**；两条通道分工、零检索快车道、章节↔来源逐行对应、通道边界硬约束 |
| [reference/MQL-报表路径固化表.md](reference/MQL-报表路径固化表.md) | **优先读**；F9 常用报表的实测固化路径/字段/枚举，命中即零检索直取 |
| [reference/MQL-取数规程.md](reference/MQL-取数规程.md) | 取数前必读；MQL 工作流（§2A 零检索 / §2B 完整检索）、版本校验、Block、路径、字段、报告期（§11） |
| [reference/取数脚本一次成型.md](reference/取数脚本一次成型.md) | 生成 MQL 前必读；`--script` / `--params` / `--check` 用法、脚本名↔批次对应、待补项补录流程 |
| [reference/资讯检索-取数规范.md](reference/资讯检索-取数规范.md) | 取数前必读；**11 个章节文字描述场景**的 `mx_finance_search` 检索句式、并发批次编排（§10.1）、`raw/{scene}.json` 落盘契约、加工、降级 |
| [reference/事件库-取数规范.md](reference/事件库-取数规范.md) | 章节 1 取数前必读；催化事件时间表两个事件库接口（`newsEventSearch` / `futureEventSearch`）、取值映射与降级 |
| [reference/输出契约与数据契约.md](reference/输出契约与数据契约.md) | 组装 `data.json` 与交付前；输出契约、章节变量表、`{{ZWSMSJ}}` 结构、关键报告期规则 |
| [reference/合规与降级.md](reference/合规与降级.md) | 全程；优先级、禁止项（目标价/评级/占位符/情绪化用词/零幻觉）、缺失数据三级降级 |
| [reference/市场路由与取值范围.md](reference/市场路由与取值范围.md) | 输入归一化、市场路由、上市状态校验 |
| [reference/沪深京-分章节MQL清单.md](reference/沪深京-分章节MQL清单.md) | 沪深京公司取数 |
| [reference/港股-分章节MQL清单.md](reference/港股-分章节MQL清单.md) | 港股公司取数 |
| [reference/汇率换算规则.md](reference/汇率换算规则.md) | 港股非人民币报表折人民币 |
| [reference/报告版式与图表规范.md](reference/报告版式与图表规范.md) | 渲染、表格、图表、页脚 |
| [reference/章节示例对照表.md](reference/章节示例对照表.md) | 需要对齐样例颗粒度时读取 |
| [reference/prompts/00-通用约束.md](reference/prompts/00-通用约束.md) | 逐章生成前**先读**；零幻觉 / 合规用词 / 格式禁止项 / 降级策略 / 数字格式的**公共基线** |
| [reference/prompts/*.md](reference/prompts/) | 逐章生成前读取对应文件（第 5 章需读 `05.1` **和** `05.2`）；各章只写特有约束 |
| `agents/openai.yaml` | 宿主默认提示词（非运行时必读） |
