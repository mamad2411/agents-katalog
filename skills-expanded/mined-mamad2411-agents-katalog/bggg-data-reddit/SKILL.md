---
name: bggg-data-reddit
description: Collect auditable Reddit search results and full comment trees at scale, preserve the source JSON, and normalize posts and comments into analysis-ready JSONL. Use for VOC, market research, community discovery, keyword snowballing, or any task that needs Reddit post and comment text without inventing unavailable fields. Reddit data layer of the bggg VOC suite (shared project folder; orchestrated by industry-orchestrator, reported by bggg-voc-report).
---

# BGGG Reddit Data

Use Reddit's public JSON listings through a logged-in or public Chrome tab when direct shell access is blocked. Save every response before transforming it, then normalize locally with the bundled script.

## VOC Project Layout（bggg 系列共用）

bggg VOC 系列 skill（bggg-data-amazon / bggg-data-reddit / bggg-data-x / bggg-voc-report / industry-orchestrator）共用一个项目文件夹，让多平台数据规整到同一处、下游分析零改路径。开工先确定项目根目录 `<project>`（用户指定，或新建 `voc-<产品或主题slug>/`），并从 `<project>` 根目录执行本 skill 的全部命令（下文相对路径都基于它）：

```text
<project>/
  PROJECT.md            # 研究简报 + 决策日志（编排 skill 维护；单独使用可省）
  config/               # 采集目标：amazon_targets.tsv / reddit_queries.tsv / x_queries.tsv / keywords.txt
  work/<platform>/…     # 各平台原始证据、attempt 日志、request plan、manifest
  data/raw/             # 各平台规范化 JSONL（统一行契约，分析共用层）
  data/clean|coded/     # 下游清洗与编码（industry-orchestrator 维护）
  output/               # 报告与交付物（bggg-voc-report 写 output/report/）
```

本 skill 的落点：`config/reddit_queries.tsv` → `work/reddit/`（request plan 与 manifest）+ `data/raw/source_json/`（未修改源响应）→ `data/raw/reddit_<lang>_<date>.jsonl`。

## Workflow

1. Define a small query file and build a request plan:

```bash
python3 scripts/build_request_plan.py \
  --queries config/reddit_queries.tsv \
  --output work/reddit/request_plan.json
```

Use tab-separated columns `query`, `lang`, and `round`. `lang` and `round` are optional.

2. Open `https://www.reddit.com/` in Chrome. Fetch each planned URL from that Reddit page with same-origin `fetch`, including pagination through `data.after`. Do not read or export browser cookies, local storage, profile data, or credentials.

3. Save each unmodified response under `data/raw/source_json/` and append one manifest row per saved file. Follow [references/chrome_same_origin.md](references/chrome_same_origin.md) for the browser loop and manifest format.

4. Rank directly relevant parent posts by engagement and topical fit. Download complete comment trees for the highest-value parents with `/comments/{post_id}.json?limit=500&depth=10&sort=top&raw_json=1`. Treat replies as clustered under their parent thread; do not count thousands of replies from one viral thread as independent market prevalence.

5. Normalize and validate:

```bash
python3 scripts/normalize_reddit.py \
  --manifest work/reddit/source_manifest.jsonl \
  --output data/raw/reddit_EN_2026-07-25.jsonl \
  --summary work/reddit/normalize_summary.json
```

6. Report query count, parent-post count, comment count, unique rows, deleted/removed rows skipped, unresolved `more` nodes, HTTP failures, and parent-thread concentration.

## Quality Rules

- Keep raw source JSON immutable. Write retries to new files rather than overwriting evidence.
- Use the Reddit fullname (`t3_…` or `t1_…`) as `native_id`; derive `source_id` with SHA-256.
- Preserve exact `text_raw`. Put translations or labels in downstream clean/coded files.
- Skip `[deleted]`, `[removed]`, empty bodies, ads, and promoted posts; count every exclusion.
- Search listings are discovery samples, not complete census data. Record sort, time window, query, page cursor, and collection time.
- Stop pagination only when `after` is null, the requested cap is reached, or repeated cursors/no-new-ID protection fires.
- Respect login walls, rate limits, and challenge pages. Back off and record the failure; never bypass authentication or change the user's account.
- Deduplicate exact native IDs first. Use similarity dedupe only in a later cleaning stage so raw evidence remains auditable.
- For prevalence statistics, cap or weight rows per parent thread and disclose the rule.

## Degradation

If Chrome same-origin fetching is unavailable, try a normal public Reddit JSON request with a conservative user agent. If it is blocked, deliver the request plan and collection manifest with the exact failure; do not substitute search-engine snippets for full Reddit comments.

## Resources

- `scripts/build_request_plan.py`: create deterministic search request and manifest templates.
- `scripts/normalize_reddit.py`: parse saved search listings and nested comment trees into JSONL.
- `references/chrome_same_origin.md`: Chrome collection loop, checkpointing, and manifest contract.
- `references/schema.md`: normalized row and audit requirements.
