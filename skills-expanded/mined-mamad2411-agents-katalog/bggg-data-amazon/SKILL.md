---
name: bggg-data-amazon
description: Collect Amazon.com written product reviews at scale through Woot's public review AJAX route, retain every attempt and error log, reconcile partial runs, and normalize exact review text into auditable JSONL. Use for VOC, competitor review mining, low-star complaint analysis, listing research, or batch ASIN review acquisition without Amazon credentials. Amazon data layer of the bggg VOC suite (shared project folder; orchestrated by industry-orchestrator, reported by bggg-voc-report).
---

# BGGG Amazon Data

Use the verified Woot review endpoint for Amazon US written reviews. This route needs no Amazon login, browser cookie, developer key, or paid scraper API.

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

本 skill 的落点：`config/amazon_targets.tsv` → `work/amazon/<run-date>/`（证据与 manifest）→ `data/raw/amazon_woot_<date>.jsonl`。

## Prepare Targets

Create a tab-separated file:

```text
asin	mode	lang	title
B08422NWYZ	full	EN	Product name
B0XXXXXXXX	basic	EN	Another product
```

Choose modes deliberately:

- `basic`: one unfiltered route, usually up to about 100 written reviews.
- `full`: five star filters, usually up to about 100 per star.
- `max`: five star filters × four sort orders, then exact dedupe; slower and still subject to the endpoint's visible-result ceiling.

Use `full` for the highest-priority products and products where 1–3 star feedback matters. Use `basic` for broad competitive coverage. Do not infer written-review volume from Amazon's total ratings count.

## Acquire and Reconcile

```bash
python3 scripts/run_batch.py \
  --targets config/amazon_targets.tsv \
  --run-dir work/amazon/2026-07-25 \
  --attempts 3 \
  --workers 2
```

The runner:

- saves each attempt JSON plus stdout/stderr logs;
- caps concurrency at two workers;
- treats `Error (filter=` in stderr as a partial-run marker even when exit code is zero;
- marks HTTP/request failures with no collected rows as `failed` instead of publishing an empty partial result;
- marks a successful JSON response with no visible written reviews as `complete_no_reviews`;
- retries with backoff;
- unions every parseable attempt and exact-deduplicates review content;
- writes `acquisition_manifest.json` and one reconciled `ASIN_mode.json` per target.

Never delete failed attempts. They are source evidence and can contain genuine reviews missing from a later retry.

## Normalize

```bash
python3 scripts/normalize_reviews.py \
  --run-dir work/amazon/2026-07-25 \
  --targets config/amazon_targets.tsv \
  --output data/raw/amazon_woot_2026-07-25.jsonl \
  --summary work/amazon/2026-07-25/normalize_summary.json
```

Use `--keywords keywords.txt` to add literal hit labels.

## Quality Rules

- Preserve `Title` and `Text` exactly in upstream JSON. The normalized `text_raw` concatenates them without translation.
- Build a stable SHA-256 content key from author, title, and body because this route often returns `Id=null`.
- Parse the human-readable date in `OriginDescription`. Treat epoch-like `SubmissionDate` values as unreliable unless independently verified.
- Merge the same content across ASIN variants while preserving every observed ASIN in `context.asins`.
- Keep star rating, helpful votes, verified-purchase flag, Vine flag, and media URLs.
- Skip empty bodies and count them. Never fabricate native IDs, dates, authors, or review totals.
- Record selected mode, attempt health, input rows, unique rows, duplicates, parse failures, and per-ASIN counts.
- Validate the first live ASIN before launching a large batch. If the route changes schema, stop and inspect rather than emitting empty success files.
- Use no more than two workers and conservative retries. Back off on timeouts or HTTP errors.

## Known Limits

- Amazon US written reviews only; star-only ratings are unavailable.
- Each filter/sort combination exposes a limited window, commonly around 100.
- A high-volume five-star bucket can remain truncated even in `max` mode.
- Review author/title/body exact dedupe can merge syndicated variant reviews; retain the ASIN list so the merge remains auditable.
- The Woot route is public but not a completeness guarantee. Describe results as collected written reviews, not all customer ratings.
- A valid Amazon ASIN can still be unavailable through Woot. Treat its HTTP 404 as an unsupported target, not proof that the route is globally unavailable.

## Resources

- `scripts/amazon_review_scraper.py`: verified stdlib Woot scraper, retained from `mrlong0129/amazon-review-scraper`.
- `scripts/run_batch.py`: retries, partial detection, checkpointing, and attempt reconciliation.
- `scripts/normalize_reviews.py`: cross-ASIN dedupe and normalized JSONL export.
- `references/schema.md`: target file, raw evidence, and output contract.
- `references/source_and_limits.md`: provenance, tested behavior, and limits.
- `references/upstream_LICENSE`: retained MIT license for the bundled upstream scraper.
