---
name: foreign-literature-search
description: >
  外文学术文献检索工具（社会科学方向）。基于 OpenAlex 开放 API（无需机构账号、无需 API key），
  执行三阶段检索：①主体联合检索（最具体组主检索+其他组后置文本过滤，实现真正 AND 语义）
  ②独立补充检索（研究对象背景文献 + 核心理论文献）③汇总去重分类 Excel。
  同步生成 WoS/Scopus 布尔检索式供有机构权限的用户使用。
  触发条件：用户提到需要检索外文/英文/SSCI文献、检索国外学术数据库、帮我搜英文文献、
  foreign literature search、检索 SSCI/SCI 论文等。
---

# 外文学术文献检索工具（OpenAlex 主力版）

调用 Python 脚本（`scripts/openalex_search.py`）通过 **OpenAlex 开放 API** 执行全自动检索，
无需机构账号、无需 API key、无需浏览器。

## 依赖安装

```bash
pip install openpyxl
```

> OpenAlex API 无需注册，每秒最多 10 次请求，脚本已内置限速。

---

## Step 0: 解析输入并制定检索策略

### 0.1 关键词组设计原则

从研究选题中提取 **2-3 个核心概念组**，每组内扩展同义词（`+` 分隔），组间取 AND 交集。

**关键注意**：过滤组的词语应足够**具体**，避免使用 "meaning"、"identity" 这类极泛词（会在所有社科文献中出现）。优先使用复合短语：

| 避免（太泛） | 改用（更具体） |
|------------|--------------|
| `meaning` | `meaning of work + work meaning + meaningful work` |
| `identity` | `occupational identity + worker identity + professional identity` |
| `control` | `labor control + algorithmic control + managerial control` |
| `change` | `livelihood change + occupational transition + career change` |

**选题示例**："快车司机的生计变迁与意义建构"

```
组1（研究对象，主检索）：gig economy + platform labor + ride-hailing + Uber driver + DiDi
组2（核心议题，后置过滤）：meaning of work + work meaning + occupational identity + livelihood
```

### 0.2 上位概念兜底

若某组词过于精确（新兴概念、特定群体），主动加入上位概念：

| 精确词 | 上位概念兜底 |
|--------|------------|
| `ride-hailing driver` | `+ gig worker + platform worker + precarious worker` |
| `meaning-making` | `+ identity work + self-concept + sensemaking` |
| `algorithmic management` | `+ digital labor + platform capitalism` |

### 0.3 向用户确认策略

执行前列出检索方案，等用户确认：

```
【主体联合检索】
组1（主检索）：gig economy + platform labor + ride-hailing + Uber driver
组2（后置过滤）：meaning of work + work meaning + occupational identity + livelihood

【独立补充检索】（主检索完成后必做）
补充A（研究对象背景）：precarious work + informal economy × labor market + working conditions
补充B（核心理论）：identity work + sensemaking + meaning-making × labor + work + occupation

WoS 布尔检索式（同步生成，供有机构权限用户使用）
```

---

## Step 0.5: 生成 WoS / Scopus 布尔检索式

在执行脚本之前，根据关键词组生成标准布尔检索式，输出给用户备用：

**Web of Science（SSCI）**：
```
TS = ("gig economy" OR "platform labor" OR "ride-hailing" OR "Uber driver")
AND TS = ("meaning of work" OR "occupational identity" OR "livelihood" OR "worker identity")
AND WC = (Sociology OR "Industrial Relations" OR "Labor Relations")
```

**Scopus**：
```
TITLE-ABS-KEY("gig economy" OR "platform labor" OR "ride-hailing")
AND TITLE-ABS-KEY("meaning of work" OR "occupational identity" OR "livelihood")
AND SUBJAREA(SOCI OR PSYC OR ECON OR BUSI)
```

---

## Step 1: 执行主体联合检索

```bash
python3 /Users/songyiping/.claude/skills/foreign-literature-search/scripts/openalex_search.py \
  --keywords "gig economy + platform labor + ride-hailing + Uber driver" \
  --keywords "meaning of work + work meaning + occupational identity + livelihood" \
  --max-results 100 \
  --topic "快车司机生计变迁与意义建构" \
  --category "直接相关（平台劳动×意义建构）" \
  --color "D9E1F2" \
  --output-dir ~/Downloads
```

**脚本工作原理**：
1. 以词数最少（最具体）的组作为**主检索**，对每个同义词调用 OpenAlex API，合并结果（OR 逻辑）
2. 对每篇论文的 title+abstract 做**后置文本过滤**：确保包含其他每个组的至少一个词
3. 若过滤后 < 20 篇，自动放宽为"任意一个额外组匹配"
4. 按被引量降序排列，输出前 N 篇

**参数说明**：

| 参数 | 说明 |
|------|------|
| `--keywords` | 关键词组，每个 `--keywords` 为一组，组内 `+` 分隔同义词 |
| `--max-results` | 最多返回篇数（默认100） |
| `--year-from` / `--year-to` | 年份范围（如 `--year-from 2010`） |
| `--no-soc-filter` | 关闭社会科学 concept 过滤（默认开启） |
| `--min-quartile` | 最低期刊分区要求，如 `--min-quartile Q2` 只保留Q1/Q2期刊 |
| `--no-journal-stats` | 跳过期刊分区查询（加快速度，不推荐） |
| `--category` | 文献类别标签（用于最终 Excel 分类） |
| `--color` | Excel 行颜色，蓝=`D9E1F2`，绿=`E2EFDA`，黄=`FFF2CC`，橙=`FCE4D6` |
| `--output-file` | 指定输出路径 |
| `--topic` | 检索主题（用于文件名） |

**Excel 输出列说明**：

| 列名 | 说明 |
|------|------|
| JCR分区 | Q1-Q4，基于精选内置期刊表（无*号）或2yr影响因子估算（有*号） |
| 中科院分区 | 1区-4区，同上来源 |
| 2yr影响因子 | OpenAlex source API 返回的近2年平均被引率（≈ 2yr IF） |
| 被引量 | 论文总引用次数 |

> **分区数据说明**：内置表覆盖约50个社科核心期刊（含ASQ、ASR、AJS、Human Relations等），未覆盖的期刊通过 OpenAlex 影响因子估算分区（带 `*` 标记）。JCR/中科院官方分区以最新年度为准，请自行核实。

---

## Step 2: 独立补充检索（必做）

主检索完成后，对各核心概念分别做独立检索，获取间接相关文献：

**补充检索 A：研究对象背景文献**
```bash
python3 /Users/songyiping/.claude/skills/foreign-literature-search/scripts/openalex_search.py \
  --keywords "precarious work + informal work + gig worker + platform worker" \
  --keywords "labor market + working conditions + employment + job quality" \
  --max-results 60 \
  --topic "快车司机生计变迁与意义建构" \
  --category "间接相关-劳动条件背景" \
  --color "E2EFDA" \
  --output-file ~/Downloads/外文补充A_劳动背景.xlsx
```

**补充检索 B：核心理论文献**
```bash
python3 /Users/songyiping/.claude/skills/foreign-literature-search/scripts/openalex_search.py \
  --keywords "identity work + sensemaking + meaning-making + self-concept" \
  --keywords "labor + work + occupation + employment" \
  --max-results 60 \
  --topic "快车司机生计变迁与意义建构" \
  --category "间接相关-意义/身份认同理论" \
  --color "FFF2CC" \
  --output-file ~/Downloads/外文补充B_意义理论.xlsx
```

> 补充检索结果不足 20 篇时不强制调整，但结果为 0 时需替换词汇后重试。

---

## Step 3: 汇总合并——输出统一分类 Excel

所有检索完成后，将全部 Excel 文件合并去重，生成统一的分类 Excel：

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from pathlib import Path

files = {
    "直接相关（平台劳动×意义建构）":     ("D9E1F2", "~/Downloads/外文文献检索_快车司机生计变迁_YYYYMMDD.xlsx"),
    "间接相关-劳动条件背景":              ("E2EFDA", "~/Downloads/外文补充A_劳动背景.xlsx"),
    "间接相关-意义/身份认同理论":         ("FFF2CC", "~/Downloads/外文补充B_意义理论.xlsx"),
}

all_rows = []
seen_titles = set()
orig_headers = None  # 从第一个文件读取真实表头，不硬编码

for category, (color, filepath) in files.items():
    wb = openpyxl.load_workbook(Path(filepath).expanduser())
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if orig_headers is None:
        orig_headers = list(rows[0])  # 实际表头：序号(0), 文献类别(1), 标题(2), ...
    for row in rows[1:]:
        title = str(row[2] or "").strip()  # 标题固定在索引2
        if title and title not in seen_titles:
            seen_titles.add(title)
            # 用正确的 category 覆盖原行的文献类别（索引1），保留其余列原样
            all_rows.append((color, category) + tuple(row[2:]))
    wb.close()

wb_out = openpyxl.Workbook()
ws_out = wb_out.active
ws_out.title = "外文文献汇总"

# 直接使用从文件读取的真实表头，避免硬编码导致列名错位或重复
ws_out.append(orig_headers)
for cell in ws_out[1]:
    cell.font = Font(bold=True, color="FFFFFF", size=11)
    cell.fill = PatternFill(fill_type="solid", fgColor="1F4E79")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

for seq, row_data in enumerate(all_rows, 1):
    color, category = row_data[0], row_data[1]
    ws_out.append((seq, category) + row_data[2:])  # 用新序号替换原序号
    fill = PatternFill(fill_type="solid", fgColor=color)
    for cell in ws_out[ws_out.max_row]:
        cell.fill = fill
        cell.alignment = Alignment(vertical="top", wrap_text=True)

# 列宽按实际列数动态设置（原始文件有14列）
col_widths = [5, 28, 45, 22, 22, 8, 8, 10, 6, 8, 36, 36, 30, 60]
for i, w in enumerate(col_widths[:len(orig_headers)], 1):
    ws_out.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
for row in ws_out.iter_rows(min_row=2):
    ws_out.row_dimensions[row[0].row].height = 65
ws_out.freeze_panes = "A2"
ws_out.auto_filter.ref = ws_out.dimensions

ws2 = wb_out.create_sheet("分类统计")
ws2.append(["文献类别", "颜色", "篇数"])
color_desc = {"D9E1F2": "蓝-直接相关", "E2EFDA": "绿-背景文献", "FFF2CC": "黄-理论文献", "FCE4D6": "橙-扩展视角"}
for cat, (color, _) in files.items():
    cnt = sum(1 for r in all_rows if r[1] == cat)
    ws2.append([cat, color_desc.get(color, color), cnt])
ws2.append(["合计（去重后）", "", len(all_rows)])
for cell in ws2[1]: cell.font = Font(bold=True)

output_path = "~/Downloads/外文文献汇总_快车司机生计变迁_YYYYMMDD.xlsx"
wb_out.save(Path(output_path).expanduser())
print(f"[✓] 已保存: {output_path}（共 {len(all_rows)} 篇）")
```

---

## Step 4: 报告结果

检索完成后向用户报告：
- 各轮检索篇数（含 API 总量参考）
- 去重后总篇数、各类别分布
- 汇总文件路径（打开文件）
- 提醒用户在 WoS/Scopus 补充机构数据库检索

```bash
open ~/Downloads/外文文献汇总_*.xlsx
```

---

## 颜色约定

| 类别 | 颜色 | hex |
|------|------|-----|
| 直接相关 | 蓝 | `D9E1F2` |
| 间接相关-背景 | 绿 | `E2EFDA` |
| 间接相关-理论 | 黄 | `FFF2CC` |
| 间接相关-扩展 | 橙 | `FCE4D6` |

---

## 常见问题

| 现象 | 原因与处理 |
|------|-----------|
| 结果中有不相关文献 | 过滤组使用了太泛的单词（如 "meaning"）→ 改用复合短语如 "meaning of work" |
| 结果 < 20 篇 | 主检索词太精确 → 加入上位概念（如加 "gig worker + platform worker"） |
| SSL/连接错误 | 网络波动，脚本自动重试3次；若持续失败稍等后重试 |
| 摘要为空 | OpenAlex 部分论文无摘要数据（属正常现象） |
| 顶刊标注 ⭐ | 期刊名匹配 ASQ、Human Relations、Organization Studies 等内置顶刊列表 |
