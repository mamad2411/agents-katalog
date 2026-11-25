---
name: video2wiki
description: Turn a video link (Xiaohongshu / Bilibili / Douyin / YouTube) or an existing noisy web-clipping into a clean structured note that is ingested into the user's Obsidian LLM-Wiki vault (repository root). Use when the user invokes /video2wiki, drops a video URL or a clippings/ file and asks to 转成笔记 / 整理 / 沉淀 / 归档 / ingest, or asks to backfill the clippings folder. Downloads audio with yt-dlp, transcribes locally with faster-whisper, writes a structured source page, then runs the Karpathy-style wiki ingest. Adapted from the lark-video2note pattern but lands in Obsidian instead of Lark.
---

# video2wiki

把视频（或一个只有"视频壳子"的剪藏）变成**结构化笔记**并**沉淀进 wiki**。
落点是本地 Obsidian，全程离线、无需任何账号/API key。

## Step 0 — 先读两份手册

1. 读 `AGENTS.md`（vault 根目录；wiki 的总规范、ingest 流程、页面 frontmatter）。
2. 读 `.cursor/skills/wiki/SKILL.md`（Query/Lint/output 约定）。

本 skill 是 AGENTS.md §4.1 ingest 流程的**视频专用前置管道**：它负责把视频还原成文字，之后完全走标准 ingest。

## 输入形态

- 一条视频 URL（小红书 / B站 / 抖音 / YouTube），或分享口令文本
- 一个 `clippings/*.md` 文件（脚本会自动从 frontmatter 的 `source:` 抠出真实 URL）
- "把 clippings 全部回填" → 见末尾「批量回填」

## 四步管道

所有脚本在 vault 根目录 `<VAULT_ROOT>` 下运行。工作目录用 `output/.video_work/<slug>/`。

### 1. 下载音频 — `fetch.py`

```bash
python .cursor/skills/video2wiki/scripts/fetch.py \
  --clipping "clippings/<文件>.md" \
  --out "output/.video_work/<slug>"
# 或 --url "<视频URL>"
```

- 输出一行 JSON：`file / title / platform / author / duration_s / source_url / size_bytes`。
- **exit 2 = 这不是视频**（图文笔记/纯文章）：停止本管道，改为直接读 clipping 文本做去噪 ingest。
- **exit 1 = 真失败**：多半是需要登录态。让用户用浏览器扩展导出 `cookies.txt`，再加 `--cookies-file <路径>` 重试（别用 `--cookies-browser chrome`——Windows 上 Chrome 运行时会锁 cookie 库）。
- 默认不带 cookies；多数带 `xsec_token` 的小红书公开链接可直接下。

### 2. 本地转写 — `transcribe.py`

```bash
python .cursor/skills/video2wiki/scripts/transcribe.py \
  --audio "<上一步的 file>" \
  --out "raw/transcripts/<YYYY-MM-DD>-<slug>.md" \
  --model small --lang zh \
  --title "<title>" --source-url "<source_url>" --platform <platform> --author "<author>"
```

- 产出**带时间戳的逐字稿** → `raw/transcripts/`（这是不可变的"内容真相"层）。
- 模型默认 `small`（速度/质量平衡）。质量不够时换 `--model medium`；有 N 卡用 `--device cuda --compute-type float16`。
- `--author` 优先用 clipping frontmatter 里的作者（yt-dlp 抓的 author 常为 unknown）。

### 3. 撰写结构化笔记 → `wiki/sources/`

读 `raw/transcripts/` 的逐字稿，按下面的模板写一篇 markdown 到
`wiki/sources/<YYYY-MM-DD>-<slug>.md`。**这就是用户日常阅读的"成品笔记"。**

frontmatter：

```yaml
---
type: source
subtype: video
tags: [由内容决定]
created: <date>
updated: <date>
sources: [../../raw/transcripts/<...>.md]
source_url: <原视频链接>
platform: xhs | bilibili | douyin | youtube
author: "<作者>"
duration: "MM:SS"
status: mature
---
```

正文结构（借鉴 lark-video2note 的 11 块，改为 Obsidian markdown + callout）：

```markdown
# <视频标题>

> [!info] 来源
> 平台 <平台> · 作者 <author> · 时长 <MM:SS> · [原视频](<source_url>)
> 逐字稿：[[../../raw/transcripts/<slug>]]

> [!abstract] 执行摘要
> 3-5 行，讲清作者**真正想说什么**（不是流水账）。

## 核心论点
一句话立场。

## 完整论证链路
按视频推进切 4-6 个小节（## 二级标题）。**以叙述段落为主**，bullet 只在真正并列/分步时用，且每条写完整句子，bullet 间要有衔接句。

## 名词解释
只解释 2-4 个真正生僻的术语，用大白话 + 类比；跳过 CLI/PR/ROI 这种常识。

> [!quote] 金句
> 最多 3 句，选最能代表作者核心立场 / 最锐利的原话。

## 逐字稿（分章节）
按 5-7 个主题切分，每个 `### [MM:SS] 小标题`，下面用引用块放该段原文。
（口误温和指出，但逐字稿原文不改。）
```

撰写要求（重要，决定笔记是否"能看"）：
- **叙述优先**，别堆 bullet；让人能顺着读懂作者的推理。
- 名词解释要"看了能懂"：类比 + 实例，不要词典式定义。
- 金句 ≤ 3 句，宁缺毋滥。
- 忠于逐字稿，不要脑补视频里没说的内容；whisper 可能有错别字/同音误识，结合上下文修正理解但别杜撰。

### 4. Ingest — 接入标准 wiki 流程

按 AGENTS.md §4.1 完成：
1. 跟用户简述 3-5 个 key takeaways。
2. 扫描 `wiki/index.md`，更新/新建相关 `entities/ concepts/ topics/` 页面（用 `[[双链]]` 互连）。
3. 更新 `wiki/index.md`（在 Sources 类目加该笔记，必要时加新概念/实体条目）。
4. 在 `wiki/log.md` **顶部**追加：`## [YYYY-MM-DD] ingest | <标题>（video）`，列出新建/修改的页面。
5. 跑一次 `wiki broken`（即 `python tools/wiki.py` 已精简，可用 `wiki lint`）自查链接。
6. 向用户汇报：成品笔记路径、触及的页面、发现的矛盾或新问题。

## slug 约定

`<YYYY-MM-DD>-<标题精简>`，中文可保留，去掉空格和特殊符号。三层文件同 slug 对应：
`output/.video_work/<slug>/`（临时音频）、`raw/transcripts/<date>-<slug>.md`、`wiki/sources/<date>-<slug>.md`。

## 三层落点（务必分清）

| 文件 | 性质 | 谁写 |
| --- | --- | --- |
| `clippings/<原>.md` | 不可变·原始噪音剪藏（线索） | 用户(Web Clipper) |
| `raw/transcripts/<slug>.md` | 不可变·逐字稿（内容真相） | transcribe.py |
| `wiki/sources/<slug>.md` | 成品结构化笔记 | LLM(本 skill) |
| `wiki/entities|concepts|topics/` | 跨视频综合 | LLM(ingest) |

`output/.video_work/` 里的 mp4 是临时文件，ingest 成功后可删（逐字稿已留底）。

## 批量回填 clippings

用户确认样本质量满意后，再批量处理 `clippings/` 里其余视频：
- **逐条**跑完整管道（下载→转写→撰写→ingest），一条 ingest 完再下一条，保证 index/log 增量一致。
- 每条之间向用户简报，遇到 exit 2（非视频）的跳过并记录。
- 大批量时转写耗时较长，先告知用户预计时间。

## 关键约束

1. **绝不改 `clippings/` 和 `raw/`**（含 transcripts）。
2. 每条视频 ingest 必须更新 `index.md` 和 `log.md`。
3. 转写有错别字是正常的——理解时结合上下文，但**不要在成品笔记里编造**逐字稿没有的内容。
4. 小红书 author 常缺失，优先用 clipping frontmatter 里的作者名。
5. 一次只深入处理一条，保持人可监督（用户偏好 sample-then-batch）。
