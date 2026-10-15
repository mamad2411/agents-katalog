---
name: sif-keyword-scout
description: >-
  亚马逊 Sif 关键词情报侦察系统（Skill 1）。用户输入 ASIN，获取 Sif 三张报表（关键词调研/反查流量词/查广告词），
  Python 完成分层、机会评级、缺口分析，三表交叉输出 PD 主攻词单。支持「用户手动导出」与「AI 浏览器导出」两种方式。
  路径通过工作区 .sif-config.json 解析，不写死本机路径。Agent 以亚马逊关键词策略顾问角色解读结果并引导参数。
  若 ASIN 有历史记录则自动触发 sif-keyword-tracker。触发：sif关键词、PD备战关键词、ASIN关键词调研、运行skill1。
---

# Sif 关键词情报侦察（Skill 1）

## Agent 角色

执行本 skill 时，同时阅读并遵循 [`references/amazon-expert-guide.md`](references/amazon-expert-guide.md)：

- 以**亚马逊关键词/PPC 顾问**身份解读结果，参数异常时主动引导用户  
- 不是只跑脚本；S/A 门槛、类目描述、SS/SSS 数量异常时要说明原因并建议修正  

## 人机协同原则（强制）

> **禁止「静默跑完全程」**。本 skill 是顾问 + 自动化，不是批处理脚本。

| 规则 | 说明 |
|------|------|
| 跑前必聊 | 在 `ingest_raw` 或任何 `--mode process` 之前，必须与用户确认 ASIN、阶段、类目、数据来源 |
| 三处卡点 | 见下方「强制暂停点」——**未获用户明确确认前，不得进入下一步** |
| 确认方式 | 用户回复「可以 / 继续 / 用自动值 / 按你说的」等明确许可；沉默或只给 ASIN **不算确认** |
| 异常先停 | sanity check 触发时，先解释原因并给出选项，等用户选后再重跑或继续 |

### 强制暂停点（三处）

| # | 时机 | Agent 做什么 | 用户确认什么 |
|---|------|-------------|-------------|
| **①** | 表1 `compute-thresholds` 之后、`process` 之前 | 展示 S/A 门槛、竞价/集中度中位数；结合**阶段 + 类目**说明是否偏高/偏低 | 维持自动值，或指定 `--s-threshold` / `--a-threshold` |
| **②** | 三表 + 交叉 `--skip-word` 完成后、写 `insights_cross` 之前 | 解读 SSS/SS/S 数量、表3 缺口/离群词；列出建议主攻 SS 清单与应排除词 | 确认主攻方向与是否重跑表3（改类目/`--sv-threshold`） |
| **③** | Skill 2 `compare_versions --skip-word` 完成后、写 `insights_tracker` 之前 | 解读新增/消失/份额变化；给出试投/暂停/调价建议 | 确认是否按建议调整投放，或仅存档观察 |

话术与解读细则 → [`references/amazon-expert-guide.md`](references/amazon-expert-guide.md) 各节。

## 依赖

| 依赖 | 说明 |
|------|------|
| Python | `pip install pandas openpyxl matplotlib python-docx numpy` |
| web-access | **仅方式 B** 需要；第三方 [eze-is/web-access](https://github.com/eze-is/web-access)（作者一泽 Eze，MIT）；路径见 [`references/path-setup.md`](references/path-setup.md) |

> **最终产物**：处理结果目录**仅保留 Excel（`.xlsx`）+ Word（`.docx`）**。
> 图表由脚本生成 PNG 后**内嵌进 Word**，不保留 `charts/` 目录。
> Agent 写的 `insights_*.md` 是中间稿（供 Word 渲染 AI 分析段），生成 Word 后自动删除。

---

## 三种输入方式（Agent 自动判断）

| 方式 | 用户怎么说 | Agent 做什么 |
|------|-----------|-------------|
| **C 直接给路径（最快）** | 发来 3 个 xlsx 路径，或一个下载文件夹 | `ingest_raw.py` 识别表类型 → 复制到标准目录 → 跑处理 |
| **A 手动导出** | 「我自己下好了」或放到指定目录 | 发 [`manual-export-guide.md`](references/manual-export-guide.md)，或 `ingest_raw --from-dir` |
| **B 浏览器导出** | 「你帮我下」 | web-access + [`browser-export-sop.md`](references/browser-export-sop.md) |

**用户直接给文件路径时**：不必再问下载方式，先 `resolve_workspace` → **跑前简报（Step 1）获确认** → 调 `ingest_raw` → 从 Step 5 继续。

```powershell
# 三个路径
python "{scripts.ingest_raw}" --asin {ASIN} --output-dir "{output_dir}" --stage {阶段} --product-category "{类目}" \
  --product-type {标品|非标品} \
  --t1 "D:/Downloads/Sif关键词调研-....xlsx" \
  --t2 "D:/Downloads/asinKeywords_....xlsx" \
  --t3 "D:/Downloads/asinAdKwView_....xlsx"

# 或一个文件夹（自动识别）
python "{scripts.ingest_raw}" --asin {ASIN} --output-dir "{output_dir}" --from-dir "D:/Downloads"
```

---

## Step 0：工作区与路径初始化（每次运行开头）

```powershell
python "{SKILL_SCOUT}/scripts/resolve_workspace.py"
```

解析 JSON，得到 `workspace`、`config_path`、`output_dir`、`download_dir`、`scripts.*`、`web_access` 等。

| 情况 | 动作 |
|------|------|
| `workspace_found: false` | 让用户指定工作区根目录，或复制 `.sif-config.example.json` → `.sif-config.json` |
| `needs_output_dir: true` | **必读** [`first-time-setup.md`](references/first-time-setup.md)，向用户询问输出根目录，**禁止填他人路径** → `--init-output-dir` |
| `needs_download_dir: true` | 仅方式 B：询问浏览器下载目录 → `--init-download-dir`（方式 A/C 可跳过） |
| 返回 `first_time_guide` | 按其中 `steps` 逐条引导，配置完成后再跑 ASIN |

**路径是用户自己的**：打包给他人时只发 `.sif-config.example.json`（空字段）；每人首次使用自己指定 `output_dir`。

详述 → [`references/path-setup.md`](references/path-setup.md) · 首次对话脚本 → [`references/first-time-setup.md`](references/first-time-setup.md)

---

## Step 1：跑前简报（ASIN + 参数 + 用户确认）

**在调用 `ingest_raw` 或处理脚本之前**，完成以下对话并**等待用户确认**：

1. **ASIN**：用户消息含 ASIN → 直接使用；否则先问  
2. **必问参数**（不可跳过）：

```
1. 产品阶段：新品期 / 成长期 / 成熟期？
2. **产品类型**：标品 / 非标品？（决定默认门槛，见 `references/threshold-presets.md`）
3. 精确产品类目（影响表3 缺口词，如「不锈钢保温杯」而非笼统「水杯」）？
```

3. **跑前简报**（用自然语言概括，勿只贴命令）：
   - 本次将产出 4 组 Excel + Word（表1/2/3 + PD 主攻词单）
   - 若有历史 → 额外产出词库更新报告（Skill 2）
   - 数据来源：方式 A / B / C（若用户已给文件路径则说明「直接接入」）
   - 预计会在 **暂停点 ①②** 与你确认门槛与主攻词方向

4. **确认门**：用户明确回复后，才进入 Step 2~3。

类目引导规则 → [`references/amazon-expert-guide.md`](references/amazon-expert-guide.md)

---

## Step 2：检查 ASIN 历史

```powershell
python "{scripts.check_history}" --asin {ASIN} --output-dir "{output_dir}"
```

保存 `has_history`、`prev_path` 供 Step 10 使用。

---

## Step 3：建目录 + 接入原始表

**方式 C（已有文件路径）**：Step 0 后直接调 `ingest_raw`（见上），本步合并完成。

**方式 A/B（尚未有标准命名文件）**：

```powershell
python "{scripts.ingest_raw}" --asin {ASIN} --output-dir "{output_dir}" --stage {阶段} --product-category "{精确类目}" --product-type {标品|非标品}
```

解析 stdout JSON：

| 字段 | 含义 |
|------|------|
| `date` / `run_id` | `YYYYMMDD`，用于文件名后缀 |
| `run_path` | `{ASIN}/{date}` |
| `raw_dir` | 原始数据目录 |
| `result_dir` | 处理结果目录 |
| `raw_files` | 三张原始表标准文件名 |
| `datetime_display` | 写入历史表的实际跑库时刻（含时分） |

目录结构：

```
{output_dir}/{ASIN}/{DATE}/
├── 原始数据/
│   ├── 关键词调研_{DATE}.xlsx
│   ├── 反查流量词_{DATE}.xlsx
│   └── 查广告词_{DATE}.xlsx
└── 处理结果/          ← 最终仅保留 xlsx + docx
    ├── {ASIN}_关键词分层分析_{DATE}.xlsx
    ├── {ASIN}_关键词调研分析报告_{DATE}.docx
    ├── {ASIN}_竞品弱点分析_{DATE}.xlsx
    ├── {ASIN}_竞品弱点分析报告_{DATE}.docx
    ├── {ASIN}_竞品缺口分析_{DATE}.xlsx
    ├── {ASIN}_竞品广告缺口分析报告_{DATE}.docx
    ├── {ASIN}_PD主攻词单_{DATE}.xlsx
    └── {ASIN}_PD主攻词单报告_{DATE}.docx
```

> 中间产物（stats JSON、`insights_*.md`、`charts/`）在 Word 生成后由脚本 `cleanup_intermediate_files` 自动删除。

---

## Step 4：获取三张原始表（仅 A/B 且 Step 3 尚未 ingest 时）

| 方式 | 动作 |
|------|------|
| **C 已有路径** | 跳过，Step 3 的 `ingest_raw` 已完成 |
| **A 手动** | 发 [`manual-export-guide.md`](references/manual-export-guide.md)；用户下完后 `ingest_raw --from-dir` 或 `--t1/--t2/--t3` |
| **B 浏览器** | web-access + [`browser-export-sop.md`](references/browser-export-sop.md)；下完后同样 `ingest_raw` |

处理前必读 → [`references/table-schema.md`](references/table-schema.md)

---

## Step 5：处理表1 → 生成 Word 报告

**计算基准：**

```powershell
python "{scripts.process_table1}" --mode compute-thresholds --input "{raw_dir}/关键词调研_{DATE}.xlsx"
```

向用户展示基准，按 [`amazon-expert-guide.md`](references/amazon-expert-guide.md) 话术询问是否调整 S/A 门槛。

> **暂停点 ①**：用户确认门槛（或明确「用自动值」）后，才执行下方 `process`。

**第一轮（Excel + stats，跳过 Word）：**

```powershell
python "{scripts.process_table1}" --mode process --input "{raw_dir}/关键词调研_{DATE}.xlsx" --output-dir "{result_dir}" --asin {ASIN} --date {DATE} --stage {阶段} --product-type {标品|非标品} [--s-threshold N --a-threshold N --s-conc-max 0.30] --skip-word
```

**Agent 写 AI 分析段（必须做）：**

1. 读取 `*_t1_stats_{DATE}.json`
2. 以亚马逊顾问身份写 **`insights_t1.md`**（仅分析文字，格式见下方「insights 写作规范」）
3. **不要写图表节**，图表由 Word 自动内嵌

**第二轮（生成 Word，自动清理中间文件）：**

```powershell
python "{scripts.process_table1}" --mode process ... --insights-file "{result_dir}/insights_t1.md"
```

产出：`{ASIN}_关键词分层分析_{DATE}.xlsx` + `{ASIN}_关键词调研分析报告_{DATE}.docx`

---

## Step 6 / 7 / 8：表2、表3、交叉分析

流程同表1：先 `--skip-word` → 写 `insights_t2.md` / `insights_t3.md` / `insights_cross.md` → 带 `--insights-file` 重建 Word。

```powershell
# 表2
python "{scripts.process_table2}" --input "..." --output-dir "{result_dir}" --asin {ASIN} --date {DATE} --skip-word
# → 写 insights_t2.md → 去掉 --skip-word 加 --insights-file

# 表3
python "{scripts.process_table3}" --input "..." --output-dir "{result_dir}" --asin {ASIN} --date {DATE} --product-category "{精确类目}" --product-type {标品|非标品} [--sv-threshold 1000] --skip-word

# 交叉（输入必须是**处理后的**三表 Excel，不是原始数据目录）
python "{scripts.cross_analysis}" \
  --t1 "{result_dir}/{ASIN}_关键词分层分析_{DATE}.xlsx" \
  --t2 "{result_dir}/{ASIN}_竞品弱点分析_{DATE}.xlsx" \
  --t3 "{result_dir}/{ASIN}_竞品缺口分析_{DATE}.xlsx" \
  --output-dir "{result_dir}" --asin {ASIN} --date {DATE} --skip-word
```

| 参数 | 何时调 | 说明 |
|------|--------|------|
| `--product-type` | 每次 ASIN | 默认非标品；标品/非标品预设见 `threshold-presets.md` |
| `--sv-threshold` | 小类目缺口词过少 | 0=用预设（非标2000/标品3000），可降至 500–1000 |
| `--product-category` | 每次必问 | 影响词类型判定 |

交叉 `--skip-word` 完成后做 **sanity check**（缺口词为 0、SSS 为 0 等）→ 见 amazon-expert-guide。

> **暂停点 ②**：向用户汇报交叉结果与建议主攻 SS 清单；确认后写 `insights_cross.md` 并生成 PD Word。若需重跑表3，在此停止并调整参数。

表2、表3 的 `insights_t2/t3` 可在暂停点 ② 之前并行撰写；**PD 报告与 cross Word 必须在暂停点 ② 之后**。

### insights 写作规范（供 Word 渲染）

| 写法 | 说明 |
|------|------|
| `## 标题` | 分节标题，会渲染为 Word 二级标题 |
| `- 列表项` | 无序列表 |
| `**加粗**` | 加粗文字 |
| `\| 列 \| 列 \|` | 可选，会转为 Word 表格 |
| `![图](charts/xxx.png)` | **禁止** — 图表由脚本插入 Word |
| `***文字***` | **禁止** — 会显示为乱码星号 |
| `# 总标题` | **禁止** — Word 已有封面标题 |

**TOP5 / 逐词点评（必须）**：每条 = 数据括号 + **策略句**（竞争判断、阶段是否投、匹配方式、与 listing 关系）。禁止「词名：词名，搜索量…」式复读。

**反例**：`- **sofa cover**：sofa cover，搜索量 58321，竞价 $1.04`  
**正例**：`- **sofa cover**（S级，搜索量 58321，竞价 $1.04，集中度 0.22）：核心品类词，集中度低于类目中位；新品期精准小预算试投，与三座规格 listing 匹配再加码。`

### 最终产出（处理结果目录仅保留）

- `{ASIN}_关键词分层分析_{DATE}.xlsx` + `_关键词调研分析报告_{DATE}.docx`
- `{ASIN}_竞品弱点分析_{DATE}.xlsx` + `_竞品弱点分析报告_{DATE}.docx`
- `{ASIN}_竞品缺口分析_{DATE}.xlsx` + `_竞品广告缺口分析报告_{DATE}.docx`
- `{ASIN}_PD主攻词单_{DATE}.xlsx` + `_PD主攻词单报告_{DATE}.docx`

---

## Step 9：更新历史（每次跑完必做，追加一行）

```powershell
python "{scripts.update_history}" --asin {ASIN} --output-dir "{output_dir}" --date {DATE} --run-path "{run_path}"
```

`ASIN历史记录.xlsx` → Sheet **「运行日志」**：**每次运行追加一行**，不覆盖、不合并日期。

| 列 | 说明 |
|----|------|
| 运行时间 | `YYYY-MM-DD HH:MM` |
| 数据日期 | `YYYYMMDD`（文件夹日期） |
| 快照路径 | `{ASIN}/{DATE}/{HHmm}`，同日多次跑库可区分 |

旧版汇总表可用 `--migrate-only` 一次性迁移：

```powershell
python "{scripts.update_history}" --migrate-only --output-dir "{output_dir}"
```

---

## Step 10：条件触发 Skill 2（1~7 天窗口对比）

当 `check_history` 显示该 ASIN **已有 ≥2 次运行** → 执行 Skill 2。

```powershell
python "{scripts.check_history}" --asin {ASIN} --output-dir "{output_dir}" --curr-date {DATE}
```

自动选对比基准：**优先 1~7 天窗口内最近一次**；同日多次则对比同日前一次。

**Skill 2 两轮流程**（与 Skill 1 相同）：

```powershell
# 1) 对比 + stats
python "{scripts.compare_versions}" --auto --output-root "{output_dir}" --output-dir "{result_dir}" --asin {ASIN} --curr-date {DATE} --skip-word

# → 暂停点 ③：解读变化，与用户确认投放策略

# 2) Agent 写 insights_tracker.md → 重建 Word
python "{scripts.compare_versions}" --auto ... --insights-file "{result_dir}/insights_tracker.md"
```

产出：`{ASIN}_词库更新报告_{DATE}.docx`（含数据表 + AI 策略段）

---

## Step 11：汇报

汇报产出路径、SS/SSS 主攻词摘要、是否建议调整参数；首次运行说明下次同 ASIN 会自动对比。

---

## 错误处理

| 错误 | 处理 |
|------|------|
| Python 报错 | 对照 `table-schema.md` 检查表结构，再问用户是否重导出 |
| Sif 未登录 | 方式 B：请用户浏览器登录后继续；或改方式 A |
| 找不到下载文件 | 确认 `download_dir` 或改方式 A |
| 类目/阶段明显不对 | 顾问模式：暂停并引导修正参数 |

## 脚本清单（`scripts/`）

| 脚本 | 用途 |
|------|------|
| `resolve_workspace.py` | 解析配置与全部脚本绝对路径 |
| `ingest_raw.py` | 建目录 + 接入用户文件（任意路径/文件夹） |
| `check_history.py` / `update_history.py` | 历史 ASIN 查询与更新 |
| `process_table1/2/3.py` | 三表处理 |
| `cross_analysis.py` | 三表交叉 → PD 主攻词单 |
| `run_context.py` / `report_utils.py` | 内部模块，不直接调用 |
| `batch_regenerate_word.py` | 开发/批跑：重建 Word；加 `--full-pipeline` 可一键跑完 Skill1+2 |
| `create_mock_sif_exports.py` | 仅开发测试用 mock 数据 |

## 参考文档索引

| 文件 | 用途 |
|------|------|
| [`first-time-setup.md`](references/first-time-setup.md) | **首次使用**：output_dir / download_dir 引导（Agent 必读） |
| [`path-setup.md`](references/path-setup.md) | 工作区、配置、路径解析 |
| [`manual-export-guide.md`](references/manual-export-guide.md) | 方式 A 用户操作指引 |
| [`browser-export-sop.md`](references/browser-export-sop.md) | 方式 B URL/按钮 SOP |
| [`table-schema.md`](references/table-schema.md) | 三张表结构（防出错） |
| [`amazon-expert-guide.md`](references/amazon-expert-guide.md) | 顾问角色与参数引导 |
| [`sop-tables.md`](references/sop-tables.md) | 分级/交叉规则细节 |
