---
name: paper-scout
description: 按研究方向自动检索前沿论文与开源项目，输出链接 + 结构化拆解（问题动机/方法/结果/局限/与本人方向的关系）。当用户说"找论文"、"检索前沿"、"最近有什么研究"、"paper scout"、"论文雷达"、"survey 最新进展"，或需要为某个 topic（如 agent、多模态、RLHF）收集近期工作时使用。
when_to_use: 用户需要针对某个研究方向/关键词获取最新论文或开源项目及拆解描述
argument-hint: <研究方向或关键词，如 "LLM agent memory">
---

# Paper Scout — 前沿论文与项目检索拆解

## Overview

围绕一个研究方向，并行检索 arXiv 论文与 GitHub 项目，筛选后按统一模板输出"链接 + 拆解"，可选落盘为雷达文档。

## Workflow

### 1. 确定主题

- 参数即主题；若为空，先问一次用户的研究方向，不要猜。
- 把主题展开为 2–4 个英文关键词变体（arXiv 只认英文），例如 "agent memory" → `LLM agent memory`、`agent long-term memory`、`memory module language model`。

### 2. 检索论文（脚本，必做）

```
python <skill-dir>/scripts/fetch_arxiv.py "<英文关键词>" --max 15 --sort relevance
python <skill-dir>/scripts/fetch_arxiv.py "<英文关键词>" --max 15 --sort submittedDate
```

- relevance 抓经典代表作，submittedDate 抓最新（各跑一次，合并去重）。
- 无结果时放宽关键词重试一次；报 SSL 错误时设置 `HTTPS_PROXY` 后重试。
- 日期近 6 个月、且与主题强相关的优先入选。

### 3. 检索项目（WebSearch + 可选 gh）

- WebSearch：`"<topic>" github 2026`、`<topic> open source framework site:github.com`。
- 若本机已登录 gh：`gh api search/repositories -f q="<topic> stars:>500" -f sort=updated --jq '.items[] | [.full_name,.stargazers_count,.description] | @tsv' | head -15`（访问 GitHub 可能需 `export HTTPS_PROXY=http://127.0.0.1:7897`）。
- 每个项目记录：仓库链接、star 量级、最近更新时间、与论文的关系（若有，给论文链接）。

### 4. 筛选与拆解

- 选 5–8 篇论文 + 3–5 个项目；剔除与主题弱相关、纯综述（除非用户要）、已被更新的同团队版本。
- 按 `references/breakdown-template.md` 的模板逐条拆解。仅依据摘要/README 的信息要标注"（仅基于摘要）"，不确定就说不确定，禁止编造实验数字。
- 需要更细节时对单篇用 WebFetch 抓 `https://arxiv.org/abs/<id>` 页面。

### 5. 输出

- 默认直接在对话中输出报告：开头一行给出主题与检索范围，然后"论文"、"项目"两节，最后"趋势小结"（3–5 条跨论文共性观察）。
- 用户要求保存时，写入工作目录 `论文雷达-<主题简称>.md`，同名文件已存在则追加"更新记录"小节而非覆盖。

## Resources

- `scripts/fetch_arxiv.py` — arXiv API 检索，输出紧凑条目（stdlib + 可选 certifi，无其他依赖）。
- `references/breakdown-template.md` — 论文/项目拆解模板与写作规则。
