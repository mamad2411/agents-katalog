---
name: research-crawl-rss
description: Batched RSS/Atom/RDF feed crawl from N feed-URLs via Python feedparser; per-feed markdown + manifest.json to caller dir; rolled-up + per-source summary.
---

# Research Crawl RSS

**Argument:** $ARGUMENTS (required, see Runtime Inputs)

If `$ARGUMENTS` is empty or missing required fields, STOP and report which fields are absent.

---

## Preamble

### Runtime Inputs

Parse from `$ARGUMENTS`:

```
--feed-urls=[u1,u2,...]          [JSON-style array of absolute feed URLs (RSS / Atom / RDF), non-empty; each must be an http(s) URL. Singular invocation expressed as a single-element array.]
--raw-output-dir={PATH}          [absolute path to a directory where per-feed rendered markdown files + manifest.json will be written]
--max-items-per-feed={N}         [positive integer per-feed item cap; MUST be ≥ 1, see §1.0 Step 3 + §6.0 row max-items-zero]

# Optional power params (omit when not needed):
--days={N}                       [positive integer recency window in days; default 1]
--max-body-chars={N}             [positive integer per-item body truncation cap; default 8000]
```

Validation rules (before §1.0):

- `--feed-urls`, `--raw-output-dir`, and `--max-items-per-feed` mandatory. If any missing, STOP and report which.
- `--feed-urls` must parse as a non-empty JSON array of strings. Else reject (`feed-urls-malformed`).
- Each entry must be an absolute `http://` or `https://` URL. First failing entry → STOP and report (`feed-urls-malformed`) with the offending value named.
- `--raw-output-dir` must be absolute. Reject relative paths (caller owns path resolution).
- `--max-items-per-feed` must parse as integer ≥ 1. Zero rejected per §6.0 `max-items-zero`.
- `--days` and `--max-body-chars` must parse as positive integers when supplied; defaults 1 and 8000.

If any validation fails, STOP and report which field failed.

### Global References

```
RSS_INGEST_SCRIPT = scripts/rss-ingest.py    # feedparser-via-Bash leaf engine; one batched run over all feeds
```

Leaf does not read tool guides at runtime, the documented pitfalls are already encoded inside `RSS_INGEST_SCRIPT` (browser-UA default load-bearing, `Accept-Encoding: identity` + gzip fallback, HTML-strip before boundary-aware truncation, per-feed cap + newest-first sort-then-slice as the token governor, recency-window filtering on `published`/`updated` dates, dateless-item fallback + `items_dropped_dateless` surfacing, 403 gating classification `cloudflare-waf` vs `cloudflare-js-challenge`, `bozo` + content-type sniff + empty-body soft-failure surfacing, title-only `body_sources:{none}` provenance, `est_tokens` chars/4 budgeting heuristic). RSS fetch is free, $0 per run; the per-feed cap is a context/token governor, not a cost cap.

### Caller Isolation

Pure primitive, no agent spawn, no pipeline agents, no telemetry. The skill runs the feedparser fetch + parse + render directly in whatever context invokes it; the caller absorbs the raw-feed context cost (raw feed items land in the caller's window). Callers crawling many feeds, or composing this leaf alongside other work, wrap the invocation in their own isolation:

```
Agent({subagent_type: "general-purpose", model: "sonnet", prompt: "Invoke /research-crawl-rss with <args>"})
```

Consumer skills document their own isolation choice. The run-pulse composer wraps each source-type leaf in one classifier sub-agent per source-type.

---

## 1.0 Context Capture

### Step 1: Verify raw output directory parent exists

Check the parent directory of `--raw-output-dir` exists. If not, route to §6.0 (`raw-output-parent-missing`). Do not create parents, caller owns path resolution. The `--raw-output-dir` itself MAY or MAY NOT exist; §3.0 Step 1 creates it via `mkdir -p` before the run.

### Step 2: Validate feed URLs and derive per-feed slugs

For each entry in `--feed-urls`: confirm it is an absolute `http(s)` URL. Build `feeds[]` preserving caller order. First entry that fails → route to §6.0 (`feed-urls-malformed`) with the offending value named.

Derive a deterministic slug per feed: lowercase the URL, drop the `http://` / `https://` scheme, replace each run of non-alphanumeric characters with a single `-`, strip leading/trailing `-`, truncate to 50 characters. If two feeds produce the same slug, append `-{ordinal}` to the later one so each feed maps to a distinct file. The slug becomes the feed's TSV name (and the script's output filename).

### Step 3: Validate `--max-items-per-feed` lower bound

Confirm `--max-items-per-feed ≥ 1`. If `--max-items-per-feed == 0`, route to §6.0 (`max-items-zero`): pass a positive integer. The cap is the effective token governor, the script sorts in-window items newest-first then slices to this count, so a large feed backlog clamps to a bounded payload. RSS fetch is free; this is a context cap, not a cost cap.

### Step 4: Build the feeds TSV

Write a tab-separated feed list for the script, one line per feed, `{slug}<TAB>{url}<TAB>` (empty domain column; the leaf does not classify or tag). Write it to a temp path via `mktemp` (e.g., `RSS_FEEDS_TSV=$(mktemp /tmp/rss-feeds-XXXXXX)`, no suffix after the X's; BSD/macOS `mktemp` rejects a template-then-suffix form like `-XXXXXX.tsv`, and the script reads `--feeds-file` by path, not by extension). The window (`--days`), per-feed cap (`--max-items-per-feed`), and body cap (`--max-body-chars`) pass directly to the script; no per-feed query construction is needed (feedparser fetches the whole feed and the script windows + caps internally).

---

## 2.0 Plan & Confirm

Skill runs autonomously, no user pause. Pure primitive; executes directly in the caller's context. Composed leaves never gate parallelization; direct invocations log the execution config and proceed.


State the planned execution config in one structured log statement, then proceed directly to §3.0:

```
## /research-crawl-rss: executing crawl

feeds:                 {feeds[]}                       # N feed URLs in caller-supplied order
raw_output_dir:        {--raw-output-dir}
max_items_per_feed:    {--max-items-per-feed}          # per-feed cap (token governor)
days:                  {--days}                        # default 1
max_body_chars:        {--max-body-chars}              # default 8000
engine:                {RSS_INGEST_SCRIPT}             # feedparser via Bash; $0/run
execution:             direct (pure primitive, no sub-agent spawn); one batched script run over all feeds
```

---

## 3.0 Crawl

Execute the crawl directly, no sub-agent spawn. Run `RSS_INGEST_SCRIPT` once over all feeds (it fetches, windows, caps, and renders per-feed markdown), then parse its manifest to build the per-source return. This step writes raw bytes only, it does NOT classify (which domain, which author), summarize, template-fill, deduplicate across feeds, or follow item links to recover missing bodies; the composing router or domain orchestrator handles all downstream transformation. Cross-feed dedup belongs to the dispatcher / classifier layer, not this leaf; title-only feeds whose bodies are genuinely absent surface `body_sources:{none}` and a downstream layer decides whether to fetch the full body from the item link.

### Inputs (from §1.0)

```
Feeds:                 {feeds[]}                        # N feed URLs in caller-supplied order
Feed TSV:              {RSS_FEEDS_TSV}                  # {slug}<TAB>{url}<TAB> per feed
Raw output dir:        {--raw-output-dir}
Max items per feed:    {--max-items-per-feed}
Window:                last {--days} day(s)
Engine:                {RSS_INGEST_SCRIPT}
```

### Procedure

Execute these steps in order:

```
1. Ensure {--raw-output-dir} exists. Use Bash `mkdir -p {--raw-output-dir}`.

2. Write the feeds TSV from §1.0 Step 4 to {RSS_FEEDS_TSV}.

3. Run the engine once, capturing the manifest to disk:

     python3 {RSS_INGEST_SCRIPT} \
       --feeds-file={RSS_FEEDS_TSV} \
       --out-dir={--raw-output-dir} \
       --days={--days} \
       --max-items={--max-items-per-feed} \
       --max-body-chars={--max-body-chars} \
       > {--raw-output-dir}/manifest.json

   The script writes one markdown file per NON-EMPTY feed into {--raw-output-dir}
   (filename {slug}.md) and prints the JSON manifest to stdout, redirected to
   {--raw-output-dir}/manifest.json. The manifest lists ALL N feeds, including
   empty / gated / errored ones, and is the canonical per-source rollup (the
   dispatcher's volume-driven auto-scaler keys on manifest counts + est_tokens,
   never on file existence). Empty feeds deliberately produce no md file.

   Exit codes: 0 = ran (per-feed failures are captured in the manifest, not the
   exit code); 2 = bad invocation (neither --feeds-file nor --url) → §6.0
   `script-exit-nonzero`; non-zero otherwise (e.g. ModuleNotFoundError for
   feedparser) → §6.0 `script-exit-nonzero` / `feedparser-missing`.

4. Read {--raw-output-dir}/manifest.json. For each record in manifest.feeds[],
   derive the per-feed crawl_status:

     - failed, record.gated is non-null (use the gated label as diagnostic),
                 OR record.error is a hard failure: an HTTPError (404 etc.),
                 "not a feed (...)", "unparseable: ...", or "empty body (...)".
     - empty, record.error is "no items in window" or "feed has zero
                 entries" (feed fetched + parsed cleanly; just no recent items).
                 An empty window is a clean operational outcome, not a failure.
     - clean, record.error is null and record.out_file is present
                 (items_emitted ≥ 1).

5. Build per_source_outputs[], one entry per feed in caller order:

     per_source_outputs[i] = {
       feed_url:        {feeds[i]},
       raw_output_path: {record.out_file},          # null for empty / failed feeds
       item_count:      {record.items_emitted},
       char_count:      {wc -c on record.out_file, or 0 when no file},
       est_tokens:      {record.est_tokens},
       crawl_status:    {"clean" | "empty" | "failed"},   # per-feed
       diagnostic:      {record.gated or record.error when failed; otherwise omit},
     }

6. Compute aggregate fields:

     total_char_count     = sum(entry.char_count for entry in per_source_outputs)
     total_item_count     = sum(entry.item_count for entry in per_source_outputs)
     overall_crawl_status = (
       "clean"   if all entries have crawl_status in {clean, empty}
       else "failed"  if all entries have crawl_status == "failed"
       else "partial"
     )

   Note: `empty` entries do NOT degrade overall status, an empty window is a
   clean outcome. Only mixed clean+failed or all-failed produces
   `partial`/`failed` aggregate.

7. Read-back: confirm {--raw-output-dir}/manifest.json exists and lists N feed
   records. Confirm one md file exists for each entry with crawl_status: clean.
   Mismatch → set overall_crawl_status = "failed" with diagnostic =
   "post-write reconciliation failed: expected N manifest records / M clean files".
```

### Capture

After the read-back (step 7), capture the structured summary as `CRAWL_RETURN` and proceed to §4.0:

```
raw_output_dir:        {--raw-output-dir}
manifest_path:         {--raw-output-dir}/manifest.json
char_count:            <total across all per-feed files>     # aggregate
item_count:            <total emitted across all feeds>       # aggregate
crawl_status:          <clean | partial | failed>             # aggregate
window_days:           {--days}
per_source_outputs:    [<one entry per feed, see step 5>]
diagnostic:            <one-line note when crawl_status != clean; otherwise omit>
```

Do NOT surface raw feed content to the caller, the rendered per-feed markdown is on disk at `{--raw-output-dir}`. §5.0 returns the reference plus summary only.

---

## 4.0 Verify

### Step 1: File-state verification

Verify the raw output directory, manifest, and per-feed files:

- [ ] Directory exists at `--raw-output-dir` (use Bash: `test -d {DIR}`).
- [ ] `manifest.json` exists at `--raw-output-dir` and parses as JSON with `feeds[]` length N.
- [ ] One md file exists at each `CRAWL_RETURN.per_source_outputs[i].raw_output_path` whose `crawl_status == clean`, and that file is non-empty (`char_count > 200`, a single rendered item plus the metadata comment exceeds 200 bytes).
- [ ] Entries with `crawl_status` of `empty` or `failed` carry `raw_output_path: null` (no file), confirm no orphan expectation.

If any check fails (entry status `clean` but file empty/missing, manifest absent or wrong feed count), route to §6.0 (`agent-write-mismatch`).

---

## 5.0 Summary

Return this structured summary to the caller (typically the `/run-pulse` composer):

```
raw_output_dir:        {CRAWL_RETURN.raw_output_dir}
manifest_path:         {CRAWL_RETURN.manifest_path}
char_count:            {CRAWL_RETURN.char_count}            # aggregate
item_count:            {CRAWL_RETURN.item_count}            # aggregate
crawl_status:          {CRAWL_RETURN.crawl_status}          # clean | partial | failed
window_days:           {CRAWL_RETURN.window_days}
per_source_outputs:    {CRAWL_RETURN.per_source_outputs[]}
  # Each entry: { feed_url, raw_output_path, item_count, char_count,
  #              est_tokens, crawl_status (clean|empty|failed per-feed), diagnostic? }
diagnostic:            {CRAWL_RETURN.diagnostic if present}
```

Caller decides next action based on overall `crawl_status` (short-circuit on `failed`; proceed with extraction iteration on `clean` or `partial`) and per-feed `crawl_status` (skip extraction on entries with `crawl_status == failed`; treat `empty` as no-content-this-cycle). The manifest carries per-feed `est_tokens` + counts for the dispatcher's volume-driven auto-scaler. The leaf does not retry, the caller governs retry policy.

---

## 6.0 Error Handling

| Error | Response |
|---|---|
| `--feed-urls`, `--raw-output-dir`, or `--max-items-per-feed` missing from `$ARGUMENTS` | STOP. Report which field is absent. |
| `feed-urls-malformed`, `--feed-urls` does not parse as a JSON array, OR array is empty, OR any entry is not an absolute http(s) URL | STOP. Report the malformed value (the offending entry when per-entry). Caller passes absolute feed URLs. |
| `--raw-output-dir` not an absolute path | STOP. Report the relative path; caller must resolve. |
| `max-items-zero`, `--max-items-per-feed == 0` or not a positive integer | STOP. Report the malformed value; pass a positive integer. The cap is the token governor, an uncapped run is unbounded. |
| `raw-output-parent-missing`, parent directory of `--raw-output-dir` does not exist | STOP. Report the missing parent path. Do not create, caller scaffolds the directory tree before invocation. The `--raw-output-dir` itself MAY or MAY NOT pre-exist; §3.0 Step 1 creates it. |
| A single feed produces `crawl_status: failed` (HTTP error / 404, non-feed HTML, unparseable XML, empty body, or a `gated:cloudflare-waf` / `gated:cloudflare-js-challenge` classification) | The script captures the failure in that feed's manifest record and continues the batch, no md file is written for it. The failure is isolated; aggregate becomes `partial` (or `failed` only if all feeds failed). Per-feed diagnostic (the gated label or error string) surfaces in `per_source_outputs[]`. A `js-challenge` feed is unreachable via any static fetcher, route it to another lane, do not retry here. |
| Crawl produces overall `crawl_status: partial` (some feeds succeeded, others failed) | Proceed to §5.0 normally. Return surfaces overall `partial` + per-feed detail in `per_source_outputs[]`. Caller iterates the array, drops failed entries from downstream extraction, continues with clean entries. |
| Crawl produces `crawl_status: empty` for one or more feeds | Proceed normally. Per-feed entry surfaces `item_count: 0` with `raw_output_path: null` (valid no-recent-items result; the feed was reachable). Empty does NOT degrade aggregate status. |
| `script-exit-nonzero`, the script exits 2 (neither `--feeds-file` nor `--url` passed, indicates a leaf bug in TSV construction) or any non-zero code | Surface the script's stderr verbatim. Exit 2 means the TSV was empty or the `--feeds-file` path was wrong, verify §3.0 Step 2 wrote the TSV. Do not retry without correcting the invocation. |
| `feedparser-missing`, the script aborts with `ModuleNotFoundError: feedparser` | STOP. The runtime dependency is absent. Report the install command `pip install feedparser`; the leaf cannot run without it. |
| `agent-write-mismatch`, a record reports `crawl_status: clean` but the md file is empty/missing, OR `manifest.json` is absent / lists a feed count ≠ N | Surface the mismatch in the return diagnostic. Set the affected entry's `crawl_status: failed`; recompute overall status. File-state on disk (manifest + md files) is authoritative. |
