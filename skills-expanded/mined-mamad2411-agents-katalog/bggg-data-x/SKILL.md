---
name: bggg-data-x
description: Collect auditable public X/Twitter posts by controlling the user's already logged-in Chrome, searching X's rendered web interface, scrolling visible results, and extracting original post text and metadata from DOM into normalized JSONL. Use for VOC research, social listening, multilingual keyword discovery, competitor monitoring, or historical search when X requires the user's browser session and cookies, credentials, internal GraphQL, paid APIs, or search-engine snippets must not be exported or used. X data layer of the bggg VOC suite (shared project folder; orchestrated by industry-orchestrator, reported by bggg-voc-report).
---

# BGGG X Data

Collect public X posts from the visible, rendered search timeline in the user's logged-in Chrome. Preserve one source package per query, then normalize locally.

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

本 skill 的落点：`config/x_queries.tsv` → `work/x/`（request plan、逐查询 source package）→ `data/raw/x_multi_<date>.jsonl`。

## Workflow

1. Prepare a tab-separated query file:

```text
query	lang	round	max_rows	sort
sample-ingredient lang:en	EN	1	250	latest
ボリュフィリン	JP	1	200	latest
```

Build a deterministic plan:

```bash
python3 scripts/build_query_plan.py \
  --queries config/x_queries.tsv \
  --output work/x/request_plan.json
```

2. Use the Chrome plugin and follow its control skill. Select the user's Chrome explicitly, read its complete browser documentation, and reuse the browser binding. Never inspect or export cookies, local storage, profiles, passwords, or session stores.

3. Open the first planned search URL. Confirm from visible page state that X is signed in and the search timeline is available. If sign-in blocks the page, ask the user to sign in in Chrome; do not switch browser or bypass authentication.

4. For each query, collect only rendered cards from the visible DOM. Follow [references/chrome_collection.md](references/chrome_collection.md) for the exact selectors, extraction function, scroll loop, checkpointing, and failure handling.

5. Save one unmodified query package immediately after each query:

```text
work/x/source_json/001_EN.json
work/x/source_json/002_JP.json
```

Do not postpone all writes until the end of the run.

6. Normalize and validate:

```bash
python3 scripts/normalize_x_dom.py \
  --inputs work/x/source_json/*.json \
  --output data/raw/x_multi_2026-07-26.jsonl \
  --summary work/x/normalize_summary.json \
  --keywords keywords.txt
```

7. Report query hits, unique Tweet IDs, rows by language, missing-text/date/URL counts, duplicate observations, failure reasons, earliest/latest date, and collection limitations.

## Required DOM Contract

Use these selectors only against rendered page content:

```text
post card          article[data-testid="tweet"]
post text          [data-testid="tweetText"]
author block       [data-testid="User-Name"]
canonical link     time[datetime] inside a[href*="/status/"]
timestamp          time[datetime]
engagement         [role="group"][aria-label]
```

Validate the contract on the first query before scaling. If any required selector returns zero while the visible timeline contains posts, stop and inspect the current DOM rather than emitting empty success files.

## Quality and Safety Rules

- Read visible DOM only. Do not intercept, call, or parse X's GraphQL/REST responses.
- Do not read, export, or persist browser cookies, tokens, local storage, credentials, or profile data.
- Preserve exact `text_raw`, Tweet ID, canonical URL, timestamp, author handle, engagement label, query, language hint, and collection time.
- Treat X search as a visible sample, not a complete census. Record `latest` versus `top`, query syntax, date bounds, caps, and stopping reason.
- Deduplicate by Tweet ID after preserving every query observation. Keep all matched queries and language hints in the normalized row.
- Separate consumers, promoters, sponsored UGC, media, and brands before calculating VOC prevalence.
- Prefer multiple narrow queries over one giant OR query. Split large historical searches by month or quarter.
- Use one tab and sequential queries by default. Avoid parallel browser tabs on the same account.
- Stop on challenge pages, suspicious-login prompts, rate limits, or repeated blank timelines. Record the failure and leave account recovery to the user.
- Never post, like, follow, reply, bookmark, or change account settings.
- Finalize every tab opened by the task.

## Scale Guidance

- Default per-query cap: 250 posts.
- Scroll about 1,500 px, then wait 850–1,500 ms.
- Stop after 6 consecutive scrolls without a new Tweet ID.
- Also use a hard scroll cap, such as 180 iterations, to prevent runaway loops.
- For prevalence estimates, disclose X's search visibility limit and the query/date slicing scheme.

## Degradation

If the logged-in Chrome session is unavailable or X blocks search, preserve the query plan and failure log. Do not substitute Tavily or search-engine snippets for original post text. Such tools may discover candidate URLs, but every quote must be revalidated against the original X page before entering the corpus.

## Resources

- `scripts/build_query_plan.py`: validate queries and build encoded X search URLs.
- `scripts/normalize_x_dom.py`: merge per-query packages, parse engagement, deduplicate, and emit normalized JSONL.
- `references/chrome_collection.md`: Chrome extraction loop and checkpoint contract.
- `references/schema.md`: source-package and normalized-row schemas.

