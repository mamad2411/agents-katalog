---
name: ime-lexicon-build
description: |
  搜索并生成行业/专业/定制词库。真源是归档 industry-dict：
  3 路搜术语（有 argo 用 argo，否则通用搜索）→ 按该行业自己的分类补
  → clean_dict 清洗 → txt。产线才用材料/工艺/设备/检测/现场。
  触发：生成行业词库、做词库、行业术语、XX行业的词、定制词库、
  industry-dict、导入微信输入法、给我做个XX行业的词库。
---

# build — 搜索 + 创建行业词库

父技能：`ime-lexicon`。本文件就是归档的 `industry-dict`（原 `~/.agents/skills/industry-dict`，2026-08-14 瘦身进 Claude 归档）。不要再单独恢复顶层技能。

查询和分类骨架在 `scripts/search.py` 的 `SCHEMAS` / `QUERY_BY_SCHEMA`。产线、投资、内容、求职各用自己的，不要互相套。

## 何时用

- 给一个行业，要一份能进微信自定义词库的 txt
- 已有旧词库 / 现场词要合并
- 不要灌通用全量细胞词库

## 工作流（industry-dict 原 6 步）

### 1. 确认行业

行业名越具体越好（「锂电池」「猪场养殖」「法律」）。输出默认 `微信输入法词库/行业词库_<行业>.txt`。只给行业名就开工，不追问路径。

### 2. 搜术语（防幻觉）

```bash
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" search \
  --topic 锂电池
```

默认打印 3 路查询和当前后端命令。探测顺序：

1. **argo**：本机有 `argo` CLI，或存在 `~/.agents/skills/argo/scripts/search.py`
2. **通用搜索**：`ddgs text`（CLI `--run` 兜底）
3. **宿主搜索**：上面都没有时，代理用当前环境的通用搜索工具（`web_search` / WebSearch）跑同一组 3 路查询，把 title/snippet 存成 json 或 txt，再 `--from`

用户要现在生成时加 `--run --out /tmp/术语.txt`。`--engine generic` 可强制走兜底。snippet 太短再抓正文（argo 用 `argo fetch`；通用搜索只吃 snippet，别卡死）。

不要在本技能里另写 HTTP 爬虫。

### 3. 按该行业的分类补（每类大约 20–40）

先看 `search --topic` 打出来的 `schema`，再补。不要把产线五类套到投资或内容上。

| 骨架 | 分类 | 适用 |
| --- | --- | --- |
| 制造 | 材料 / 工艺 / 设备 / 检测 / 现场 | 锂电、化工、产线 |
| 投资 | 品种 / 策略 / 平台 / 指标 / 圈内 | 基金、股票、理财 |
| 内容 | 体裁 / 流程 / 平台 / 数据 / 圈内 | 自媒体、知乎、公众号 |
| 求职 | 环节 / 文书 / 平台 / 条件 / 圈内 | 简历、面试 |
| 通用 | 术语 / 流程 / 工具 / 指标 / 圈内 | 对不上上面时 |

2–8 字优先，最长 12；OCV、ETF、CTR 这类缩写留；「的/是/工作」不写；组合词优于单字。

补的词带分类：`--term 品种:可转债` 或词表行 `可转债	品种`。制造行业仍写 `材料:磷酸铁锂`。

### 4. 清洗输出

搜索提取 + 模型补充 + `--from` 旧表，进同一清洗：

```bash
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" build \
  --topic 锂电池 \
  --from /tmp/术语.txt \
  --term 材料:磷酸铁锂 \
  --term 检测:OCV
```

清洗真源：`scripts/clean_dict.py`（归档原规则）。`build` 再多滤叠词和短语气助词。standalone `clean_dict.py a.txt b.txt` 保持归档行为。

默认写 txt（一行一词，微信：设置 → 自定义词库 → 导入）。`--out foo.tsv` 才写中间表。stdout 会打 `cat	品种	N` 这类，未标分类的进 `未分类`。

同时写出三层：

| 层 | 文件 | apply |
| --- | --- | --- |
| 核心 | `*_核心.tsv` | 可以。必须有拼音 |
| 扩展 | `*_扩展.tsv` | 可以。含多音字（行/长/重…） |
| 大词库 | `*_大词库.tsv` | **禁止**。无拼音、细胞源 |

有本机 `pypinyin` 时会给无拼音的词补全拼。补不出的进大词库。

可选种子（先下载研究词库）：

```bash
python3 .../ime_lexicon.py build --topic 投资理财 --seed thuocl:财经 --seed thuocl:IT
```

THUOCL 在 `微信输入法词库/研究/06-清华THUOCL/data/`。只当种子，再按 schema 人工裁到几百条。

### 5. 圈内词（不许跳过）

> 通用词库已生成（N 词）。圈内黑话、自家简称、栏目名无法自动生成。有旧词库或要补的词，把路径或列表发来再合并。

制造行业把「圈内」理解成车间土话即可。

用户给了旧表就再跑一遍 `build --from` 新表+旧表。

### 6. 导入

- 微信官方：自定义词库导入 txt，建议 1 万以内。
- 豆包 / WeType 文件层：只用 `*_核心.tsv` + `*_扩展.tsv`，optimize `--profile industry` 后 staging。`import --budget <剩余槽>`（剩余槽先跑 `detect` 实读，槽数随豆包版本变，不要背数字）。大词库与第三方全量词库不准 apply。

## 验收

一般行业 150–400 词。抽 15 个应全是真术语，错 1 个以上重做。有旧行业表时重合 40–70% 算方向对，<30% 偏了。太少说明搜索没搜到位。

