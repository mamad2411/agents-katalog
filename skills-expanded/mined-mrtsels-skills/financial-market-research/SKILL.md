---
name: financial-market-research
description: 金融/量化研究报告撰写工作流。从任务描述 + 阅读材料产出结构化研究报告，覆盖交易所、交易算法、市场微观结构等主题。
version: 1.0.0
---

# Financial Market Research Report

撰写关于金融市场的结构化研究报告。以下为格式约定和步骤。

## 触发条件

用户要求写一份"研究报告"、"research report"、"Task N 报告"，内容涉及交易所、交易算法、暗池、智能路由、市场微观结构、美国/全球股票市场等。
也适用于**带实时市场数据的 brief**（央行利率决议、货币政策、rates 市场快报等）。这类任务强制要求：每个数字必须附上**本次实际抓取过**的 URL；抓不到就明确标 `UNVERIFIED`，绝不编造数字。

## 实时数据获取（写带数字的 brief 时）

先读 [references/euro-area-rates-data-sources.md](references/euro-area-rates-data-sources.md)（ECB / TradingEconomics 抓取配方 + worked example）和 [references/live-market-data-sources.md](references/live-market-data-sources.md)（FRED 无 key CSV 端点、NY Fed 参考利率表、CME/Eurex 合约规格与报价、FedWatch 概率表、BLS CPI——US/rates 市场数据源 + 抓取失败时的备选源）。核心规则：

- **ECB 官网**：`r.jina.ai` 会在 15s networkidle 超时（页面太重），**直接用 curl + Mozilla UA**。决议正文 URL 带 hash（`/press/pr/date/YYYY/html/ecb.mpYYMMDD~<hash>.en.html`），裸猜 `ecb.mpYYMMDD.en.html` 会 404；先抓 decisions 列表页的 `data-snippets` include 文件提取真实链接。
- **TradingEconomics**：curl 直抓即可，数字在标题下方 summary 段落 + Calendar 表（Actual/Previous/Consensus）+ Components 表里；页面导航噪音大，用正则剥标签后定位关键字。
- **多个数字并行抓**：不同来源之间无依赖时同一轮并行 curl，避免串行浪费轮次。

## 步骤

**第 1 步 — 搜集输入**
- 读取用户提供的 task brief / PDF / email / plan
- PDF 为图片格式时：用 PyMuPDF (`fitz`) 逐页导出为 PNG，再用 `vision_analyze` 提取内容
- 邮件内容：通过 agently-cli 搜索 + 读取

**第 2 步 — 构建大纲（plan.md）**
- 按 task brief 中的编号（01, 02, 03...）展开
- 使用中文
- 每节标注子问题（a/b/c 或 i/ii/iii）

**第 3 步 — 撰写报告（report.md）**

### 格式硬性规定

1. **语言：全中文**。术语标注英文括号，如"暗池（Dark Pools）"
2. **直接合并同类项**：当两个实体（Nasdaq / NYSE、开盘 / 收盘）规则基本一致时，不要分别展开说明，直接写"两者一致"或合并成表格
3. **表格 vs 列表的选用规则：**
   - 横向对比（开盘 vs 收盘、盘前 vs 盘后）→ 用表格
   - 简单枚举问题列表 → 用 dot list（`- **标题** — 说明`）
   - 多层级逻辑流程 → 用编号列表（1. 2. 3.），**不用 code block**
4. **时间格式统一为：** `X:XX AM/PM ET`，如 `9:30 AM – 4:00 PM ET`
5. **伪代码**：算法伪代码用 code block（常规 markdown ```），但逻辑流程/步骤用普通编号列表

### 报告结构

- 标题 + 姓名 + 日期 + 截止信息
- 按任务编号分节（01, 02, 03...）
- 每节内按子问题展开
- 结尾可加参考文献

## 变体：带实时市场数据的 Deck / PPTX（实习 Task 类任务）

当交付物是幻灯片 deck 且需要**当前**市场数据（利率、期货报价、央行决议、sell-side 观点）时，走这条管线（`quant-academy/tasks/task-5` 已验证，27 页全过 QA）：

1. **硬数据先抓**：FRED CSV 端点无需 API key — `curl "https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>"`。政策路径（目标区间变化/降息节奏）、收益率曲线、利差全从这里出，绝不靠记忆或训练数据（利率路径经常与记忆不符——2026 年 7 月真实状态是 Fed 维持 3.50–3.75%、ECB 刚加息）。具体系列与备用源见 `references/live-market-data-sources.md`。
2. **并行派发研究子代理**（delegate_task，≤3 并行）：按主题切分（US 政策+市场定价 / 期货合约数据 / EUR 政策）。每个 context 必须写明：① 已知基线（已从 FRED 验证的数字，让子代理验证补充而非重查）；② "每个数字附实际抓取的 URL，无法验证标 UNVERIFIED，禁止凭记忆编数字"；③ 要求把每个抓取页面存到 `/tmp/<name>.txt`。
3. **子代理超时恢复**：某任务超时（600s 上限）不代表数据丢失 — 它的 live transcript（`~/.hermes/cache/delegation/live/<delegation_id>/task-N.log`）和它写的 `/tmp/*.txt` 都还在，直接 grep/读文件恢复，不要重派（见 dynamic-workflow 的 pitfall）。
4. **数据驱动图表**：matplotlib SVG（按 AGENTS.md 要求）+ 同尺寸 PNG 嵌入 pptx；图内注明数据来源与截止日；标注事件（加息/降息、hold）用 `annotate` 并放到曲线空白处，别压数据线。
5. **pptxgenjs 构建**：全部验证过的数字集中在一个 `R` 数据对象（与版面代码分离），用 `rd(value, fallback)` 守卫占位符；**text 数组必须 `{text, options}` 形状**——扁平对象会坍缩成一段 run-on 文本（详见 powerpoint skill 的 pitfall，已在其中）。
   **版式：禁止文字墙**（用户明确批评过"大段文字 不够美观"）——正文区 4+ 条长 bullets 必须拆成视觉块：2×2 卡片网格 / 竖排事实卡 / 深色公式带（`P = 100 − r` 这类核心公式用深色 hero band 突出）。卡片 = 琥珀小标题（9pt 大写）+ 粗体主句（13.5pt）+ ≤2 行短要点（11pt），白底圆角 + 细边框 + 轻阴影。KPI 卡数值超长会 wrap 撞标签——值要短或换行时减小字号。信息密度保持，单行长度砍半。
6. **QA 循环**：`validate.py` → soffice 转 PDF → pdftoppm → 子代理逐页视觉 QA（fresh eyes，专查溢出/重叠/截断）→ 修复重渲染。跑两三轮直到全 PASS，再 commit/push 交付。常犯缺陷自查：卡片/数字卡算出底边（竖排卡总高 ≤ 5.4in，末张别越过 footer）；表格某行 cell 数少于列数 → 渲染成空单元格；长 value wrap 撞卡片标签；图表 annotate 压数据线；用 patch 改大段代码时模糊匹配可能误删相邻 slide 块——改完 `grep -n '// ---- S'` 核对 slide 结构（本次真发生过 S22 被吞）。

## 陷阱

- 不要分别列出 Nasdaq 和 NYSE 的规则，除非两者有显著差异
- 不要在列表流程中使用 code block（除非是真正的伪代码）
- 表格必须简明，横向列数不超过 4 列
- 不要用 `---` 分隔线过度分割内容
- 读完 PDF 后用 `vision_analyze` 而不是直接尝试 text extraction（图片 PDF 无法直接读取）
