---
name: research-crawl-x-posts
description: Batched X/Twitter post crawl from N handles via Apify search mode, with inline X Article body enrichment via a chained second actor; per-handle markdown + rolled-up summary to caller dir.
---

# Research Crawl X Posts

**Argument:** $ARGUMENTS (required, see Runtime Inputs)

If `$ARGUMENTS` is empty or missing required fields, STOP and report which fields are absent.

---

## Preamble

### Runtime Inputs

Parse from `$ARGUMENTS`:

```
--handles=[h1,h2,...]            [JSON-style array of bare X/Twitter handles, non-empty; no leading @, no URL. A leading @ is stripped during normalization. Singular invocation expressed as a single-element array.]
--raw-output-dir={PATH}          [absolute path to a directory where per-handle rendered markdown files will be written]
--max-per-handle={N}             [positive integer per-handle cost-cap; MUST be ≥ 1, see §1.0 Step 3 + §6.0 row max-per-handle-zero]

# Optional power params (omit when not needed):
--days={N}                       [positive integer time window in days; default 1]
```

Validation rules (before §1.0):

- `--handles`, `--raw-output-dir`, and `--max-per-handle` mandatory. If any missing, STOP and report which.
- `--handles` must parse as a non-empty JSON array of strings. Else reject (`handles-malformed`).
- Normalize each handle by stripping a single leading `@`; the remainder must match the X handle shape (1-15 characters, `[A-Za-z0-9_]` only). First failing entry → STOP and report (`handles-malformed`).
- `--raw-output-dir` must be absolute. Reject relative paths (caller owns path resolution).
- `--max-per-handle` must parse as integer ≥ 1. Zero rejected per §6.0 `max-per-handle-zero`.
- `--days` must parse as a positive integer when supplied; default 1.

If any validation fails, STOP and report which field failed.

### Global References

```
APIFY_ACTOR_ID    = apidojo/tweet-scraper           # chosen X/Twitter scraper actor (no-cookie, date-windowed search mode)
APIFY_CALL_ACTOR  = mcp__apify__call-actor           # Actor invocation, waitSecs 0-45 controls inline wait; no `async` flag exists
APIFY_GET_RUN     = mcp__apify__get-actor-run        # run-status polling endpoint (waitSecs blocks server-side until terminal)
APIFY_GET_ITEMS   = mcp__apify__get-dataset-items    # dataset retrieval, projects nested dot-notation fields via fields= (auto-flatten)
APIFY_ARTICLE_ACTOR = fastcrawler/x-twitter-article-to-markdown   # §3.0 Step 3 second-hop, recovers full X Article body that tweet-scraper gutted to a bare t.co (BRONZE PAY_PER_EVENT; tweetIds ≤10/run)
```

Leaf does not read tool guides at runtime, parameter choices in §1.0 Step 4 and the execution procedure in §3.0 already encode the pitfalls (cost-safety cap via per-handle `maxItems`, search-mode date targeting via `from:`/`since:`/`until:` since handle-mode ignores the date window, one Apify run per handle since `maxItems` is per-run-total, `call-actor` with `waitSecs:45` inline + `get-actor-run` poll fallback (no `async` flag), `{noResults}` sentinel filtering, fetch-time narrow-field projection via the `get-dataset-items` `fields=` param, group by `author.userName` for the per-source split).

Article-enrichment pitfalls (§3.0 Step 3, `APIFY_ARTICLE_ACTOR`), all live-confirmed 2026-06-16: pass the HOST tweet id, the tweet's own `id` for a standalone article, `quote.id` for a quoted article, NEVER `article.id` or the `/i/article/{id}` id (both return empty `md`); the actor pads its dataset to a fixed 10-row minimum with mock filler (`{id:0, text:"mock data"}`, no `tweet_id`, no `md`), so keep only rows carrying a `tweet_id` AND a non-empty `md` and discard the rest; cost is a flat per-call floor (output always pads to 10, input caps at 10 → ≤$0.05/call at BRONZE regardless of real-id count), so batch all candidate ids for the whole invocation into one ≤10-id call (chunk into successive ≤10 calls only past 10 candidates); non-article ids return `md:""` (clean negative, zero false positives); Apify is the only path, Exa/Firecrawl cannot reach the login-gated `/i/article/` body.

### Caller Isolation

Pure primitive, no agent spawn, no pipeline agents, no telemetry. The skill runs the Apify calls + dataset render directly in whatever context invokes it; the caller absorbs the MCP dataset context cost (raw tweet items land in the caller's window). Callers crawling many handles, or composing this leaf alongside other work, wrap the invocation in their own isolation:

```
Agent({subagent_type: "general-purpose", model: "sonnet", prompt: "Invoke /research-crawl-x-posts with <args>"})
```

Consumer skills document their own isolation choice. The run-pulse composer wraps each source-type leaf in one classifier sub-agent per source-type.

---

## 1.0 Context Capture

### Step 1: Verify raw output directory parent exists

Check the parent directory of `--raw-output-dir` exists. If not, route to §6.0 (`raw-output-parent-missing`). Do not create parents, caller owns path resolution. The `--raw-output-dir` itself MAY or MAY NOT exist; §3.0 Step 1 creates it via `mkdir -p` before writing the first per-handle file.

### Step 2: Normalize and validate handles

For each entry in `--handles`: strip a single leading `@`, then confirm the remainder matches the X handle shape (1-15 characters, `[A-Za-z0-9_]` only). Build `handles[]` of normalized bare handles preserving caller order. First entry that fails the shape → route to §6.0 (`handles-malformed`) with the offending value named.

### Step 3: Validate `--max-per-handle` lower bound

Confirm `--max-per-handle ≥ 1`. If `--max-per-handle == 0`, route to §6.0 (`max-per-handle-zero`): pass a positive integer. `--max-per-handle` is the per-handle `maxItems` cap. Total estimated cost ≈ `N_handles × max-per-handle × $0.0004` at the BRONZE/paid Apify tier; the FREE tier is 100× ($0.04/tweet) and only safe on a paid plan.

### Step 4: Compute date window and construct per-handle Actor inputs

Compute the window:

```
since = (today - days)  formatted YYYY-MM-DD     # lower bound, inclusive
until = (today + 1 day)  formatted YYYY-MM-DD     # upper bound, EXCLUSIVE, +1 day so today is included
```

For each handle `h` in `handles[]`, build a per-handle Actor input (one run per handle, `maxItems` is per-run-total, so a shared batched run starves trailing handles):

```
ACTOR_INPUT[h] = {
  searchTerms: ["from:{h} since:{since} until:{until}"],
  maxItems: {--max-per-handle},
  sort: "Latest",
  includeSearchTerms: true,
}
```

Cost-safety note: `maxItems` is the only verified-functional cost cap on this Actor. Do NOT add `maxTotalChargeUsd` (untested / non-functional on the sibling Actor; caps silently ignored). Do NOT set `customMapFunction`, the Actor README warns that using it for filtering triggers an automatic ban; filtering happens downstream, not in the input. Targeting MUST use `searchTerms` with `from:`/`since:`/`until:`, the `twitterHandles` + `start`/`end` path silently ignores the date window.

---

## 2.0 Plan & Confirm

Skill runs autonomously, no user pause. Pure primitive; executes directly in the caller's context. Composed leaves never gate parallelization; direct invocations log the execution config and proceed.


State the planned execution config in one structured log statement, then proceed directly to §3.0:

```
## /research-crawl-x-posts: executing crawl

handles:               {handles[]}                      # N normalized handles in caller-supplied order
raw_output_dir:        {--raw-output-dir}
max_per_handle:        {--max-per-handle}                # per-handle maxItems cap
days:                  {--days}                          # default 1
window:                {since} .. {until}                # until exclusive
actor:                 {APIFY_ACTOR_ID}
article_enrichment:    {APIFY_ARTICLE_ACTOR}             # §3.0 Step 3 second-hop; one batched ≤10-id call across all handles, fires only when article candidates exist
execution:             direct (pure primitive, no sub-agent spawn); one Apify run per handle
invocation:            call-actor waitSecs:45 inline → get-actor-run poll if not yet terminal (no `async` param)
```

---

## 3.0 Crawl & Enrich

Execute the crawl directly, no sub-agent spawn. Run the Apify `apidojo/tweet-scraper` Actor once per handle (search-mode, date-windowed), enrich any X Article posts with their full body (Step 3), then write per-handle rendered markdown files into `--raw-output-dir`. This step writes raw bytes only, it does NOT classify (Authored/Reposted/Mentioned), summarize, template-fill, or filter beyond the `{noResults}` sentinel and the per-handle cap; the composing router or domain orchestrator handles all downstream transformation. Article enrichment is raw-recovery, not transformation, it restores the verbatim article body that `apidojo/tweet-scraper` collapsed to a bare `t.co` link; it never classifies or summarizes.

### Inputs (from §1.0)

```
Handles:               {handles[]}                       # N normalized handles in caller-supplied order
Raw output dir:        {--raw-output-dir}
Max per handle:        {--max-per-handle}                 # per-handle maxItems cap
Window:                {since} .. {until}                 # until exclusive
Actor:                 apidojo/tweet-scraper
Actor input (JSON):    {ACTOR_INPUT[h]}                   # one per handle, searchTerms from:{h} since:{since} until:{until}
invocation:            call-actor waitSecs:45 → poll get-actor-run if not terminal
```

The Actor inputs were auto-constructed in §1.0 Step 4. Do NOT substitute different params. Do NOT add `maxTotalChargeUsd`. Invoke via `call-actor` with `waitSecs` (0-45), there is NO `async` flag on the MCP tool. `waitSecs:45` waits inline (this Actor finishes in ~5s, so the run is usually terminal on return); fall back to `get-actor-run` polling only when a run is still running.

### Procedure

Execute these steps in order:

```
1. Ensure {--raw-output-dir} exists. Use Bash `mkdir -p {--raw-output-dir}`.

2. For EACH handle h in handles[] (one Apify run per handle):

   a. Call mcp__apify__call-actor with { actor: apidojo/tweet-scraper,
      input: ACTOR_INPUT[h], waitSecs: 45 }. The MCP tool has NO `async`
      flag, `waitSecs` (0-45) sets the inline wait. Capture `runId`, the
      dataset id at `storages.datasets.default.id`, and `status`. If
      `status === "SUCCEEDED"` already (typical, Actor finishes in ~5s),
      skip step 2b and go straight to step 2c.

   b. If step 2a's run was not yet terminal, poll
      mcp__apify__get-actor-run({ runId, waitSecs: 30 }), the param blocks
      server-side up to 30s per call, re-calling until `status` reaches one of:
      - `SUCCEEDED`, proceed to step 2c.
      - `FAILED` / `ABORTED` / `TIMED-OUT`, this handle's run failed. Skip
        steps 2c-2e; write an empty placeholder file for h (so callers can
        rely on one file per requested handle), set this handle's
        crawl_status: failed with diagnostic = run failure reason, continue
        to the next handle.
      Maximum poll duration per handle: 600 seconds. If still not terminal
      after 600s, abandon polling for h, treat as failed, write placeholder,
      continue with diagnostic = "Actor run exceeded 600s poll budget".

   c. Fetch this run's dataset via mcp__apify__get-dataset-items({
        datasetId: {storages.datasets.default.id}, limit: 1000,
        fields: "id,fullText,text,url,twitterUrl,createdAt,author.userName,isRetweet,isQuote,isReply,isPinned,inReplyToUsername,likeCount,retweetCount,replyCount,quoteCount,viewCount,quote.author.userName,quote.text,quote.id,article.id,article.title,article.previewText,retweet.author.userName,retweet.text,noResults,entities.media.media_url_https,extendedEntities.media.media_url_https,entities.media.type" }).
      - The `fields=` param projects AT FETCH TIME and supports nested
        dot-notation (server auto-flattens parent prefixes), so the raw
        ~198-field payload never enters caller context. This is the
        dataset-read tool's `fields` param, NOT the Actor INPUT `fields[]`
        (which is top-level-only; see step 2e note).
      - `quote.id` + the top-level `article.*` fields are the article-detection
        signals consumed by Step 3 (see step 2e); the rest carry the tweet body
        and structural flags.
      - Paginate via `offset` only when the dataset exceeds 1000 items
        (rare, bounded by max-per-handle).

   d. Filter out sentinel records where `noResults === true`. The remaining
      items are h's tweets. (A handle with no tweets in the window returns
      only the sentinel → tweets array is empty → crawl_status: empty.)

   e. The narrow field set is already projected by step 2c's `fields=` param
      (the raw record otherwise carries ~198 fields). The kept fields:
        id, fullText (fallback `text`), url (fallback `twitterUrl`),
        createdAt, author.userName, isRetweet, isQuote, isReply, isPinned,
        quote.author.userName, quote.text, quote.id, article.id, article.title,
        article.previewText, retweet.author.userName, retweet.text,
        inReplyToUsername, and media URLs
        (entities.media + extendedEntities.media `media_url_https`).
      Note, nested objects use `.text`, not `.fullText`: the nested quote/
      retweet payloads carry `quote.text` / `retweet.text`; `.fullText`
      exists only at the top level (verified via live probe). The
      get-dataset-items `fields=` param resolves all these nested keys; the
      top-level-only limitation belongs to the Apify Actor INPUT `fields[]`,
      not this dataset-read tool.
      Article-detection fields (live-confirmed 2026-06-16): a STANDALONE X
      Article populates a top-level `article` object (`article.id` /
      `article.title` / truncated `article.previewText`) while its `fullText`
      collapses to a bare t.co; a QUOTED article exposes NO `quote.article.*`
      object, only `quote.id` plus a link-collapsed `quote.text`. Both are
      consumed by Step 3.

3. Article-enrichment pass (cross-handle, single batched second-hop). After all
   handles are crawled and projected (Step 2), recover the full body of any X
   Article posts that `apidojo/tweet-scraper` collapsed to a bare t.co link.
   Detection + enrichment run ONCE across all handles' tweets, not per-handle,
   so the fixed cost floor (see Global References) is paid at most once per
   invocation.

   a. Detect article candidates across every projected tweet in this
      invocation. Two shapes, both live-confirmed:
      - STANDALONE authored article: top-level `article.id` present on the
        tweet. Candidate host id = the tweet's OWN `id`. (Free detection via the
        `article` object; the actor is still needed because `article.previewText`
        is truncated.)
      - QUOTED article: `isQuote === true` AND the quoted layer is
        link-collapsed. Mechanical test: strip every t.co/x.com URL and all
        whitespace from `quote.text`; the layer is link-collapsed when the
        residual is empty (no prose remains). Candidate host id = `quote.id`.
        (No `quote.article.*` object exists, so this is the only signal. A
        `quote.text` with residual prose is NOT a candidate, a missed real
        article is cheaper than burning the ≤10-id batch budget, and a false
        candidate that slips through returns `md:""` harmlessly.)
      Build a deduped set CANDIDATE_IDS, and a back-reference recording for each
      candidate id every tweet it belongs to plus whether each occurrence is
      that tweet's OWN body (standalone) or its QUOTED layer, needed for Step 4
      render injection. The same host id can occur in BOTH roles within one
      handle (a self-quote of one's own article); record every occurrence.

   b. If CANDIDATE_IDS is empty, skip enrichment entirely (no actor call, no
      cost); proceed to Step 4 with an empty ARTICLE_MD map.

   c. Enrich in batches of ≤10 ids (APIFY_ARTICLE_ACTOR caps tweetIds at 10).
      For each batch, call mcp__apify__call-actor with { actor:
      APIFY_ARTICLE_ACTOR, input: { tweetIds: [<batch>] }, waitSecs: 45 }. The
      actor takes ~30s; if not terminal on return, poll
      mcp__apify__get-actor-run({ runId, waitSecs: 30 }) up to a 120s budget per
      batch.

   d. Fetch each batch's dataset via mcp__apify__get-dataset-items({ datasetId,
      limit: 20, fields: "tweet_id,md" }). Build ARTICLE_MD as { host_id → md },
      keeping ONLY rows where `tweet_id` is present AND `md` is non-empty.
      Discard the fixed mock-padding rows ({id:0, text:"mock data"}, no
      tweet_id, no md) and empty-`md` rows (non-article ids, clean negative,
      zero false positives).

   e. An article-actor batch that FAILS / ABORTS / TIMES-OUT is NON-FATAL, the
      handle crawls already succeeded. Log a one-line diagnostic, leave those
      ids out of ARTICLE_MD, and let Step 4 fall back to the bare-link render
      for the affected tweets. Never fail the whole invocation on an enrichment
      miss. Set `article_enrichment_status: partial` in that case (else
      `clean`, or `skipped` when CANDIDATE_IDS was empty).

4. For each handle, render its projected tweet array to a markdown file inside
   {--raw-output-dir}. Filename rule:

     filename = `handle-{h}.md`     # h lowercased

   File structure per handle:

   ---
   type: X Posts Crawl Raw
   schema: ephemeral-raw-crawl
   source_tool: apidojo/tweet-scraper
   handle: {h}
   window_start: {since}
   window_end: {until}             # exclusive
   days: {--days}
   crawled_at: {ISO 8601 timestamp of this run}
   apify_run_id: {runId for this handle}
   tweet_count: {N tweets after sentinel filter}
   articles_enriched: {count of DISTINCT article bodies rendered in full for this handle, i.e. |rendered_article_ids| for this handle; back-references and a self-quote's second occurrence do NOT re-count; 0 when none}
   input_params:
     max_per_handle: {--max-per-handle}
   ---

   # X Posts, @{h}

   ## Tweet 1, @{author.userName}, {createdAt date}
   URL: {url}
   Engagement: {likeCount} likes · {retweetCount} reposts · {replyCount} replies · {quoteCount} quotes

   {tweet body, fullText; preserve original line breaks}

   ---

   ## Tweet 2, ...

   Rendering rules:
   - Each tweet is one H2 section separated by horizontal rules (`---`).
   - H2 heading: author handle + tweet date. Body is fullText verbatim
     (preserve newlines; keep bare t.co / x.com URLs as-is).
   - Render-once rule (article bodies): each recovered host id's full body is
     written at most ONCE per handle file, at the first occurrence (in tweet
     render order) where it is SUCCESSFULLY rendered in full. Track a
     `rendered_article_ids` set, adding a host id only when its full body is
     actually written (at render time, on success), NOT at detection time, so
     a first occurrence that hit an enrichment miss (bare-link fallback) never
     blocks a later occurrence from attempting its own full render. A later
     occurrence of an already-rendered host id (the self-quote case, a host id
     that is both a standalone tweet and another tweet's quoted layer) renders a
     one-line back-reference instead of duplicating the body: `Article '{title}'
, full body rendered at Tweet {N} above`, where `{title}` is `article.title`
     for a standalone host or the recovered body's first H1 heading for a quoted
     host (no `quote.article.title` field exists). The set is per-handle by
     design, it resets for each handle file so every file is self-sufficient;
     the same article quoted by two handles renders fully in both files.
   - STANDALONE X Article injection: when the tweet's own `id` is in ARTICLE_MD
     (Step 3, its `fullText` was a bare t.co) and not yet in
     `rendered_article_ids`, replace the body with a `Article, full body
     recovered:` marker line followed by the verbatim `ARTICLE_MD[id]` markdown
     (preserve its headings, links, and image refs), then add `id` to
     `rendered_article_ids`. If `id` is already in `rendered_article_ids`, emit
     the back-reference line per the render-once rule. When the tweet had an
     `article.id` candidate but enrichment missed (`id` not in ARTICLE_MD,
     actor failure/empty), fall back to the verbatim `fullText` (the bare t.co)
     and append ` (article body not recovered)`.
   - Engagement line is one line, dot-separated; omit a count when absent.
   - For a repost (`isRetweet: true`): H2 reflects the ORIGINAL author
     (@{retweet.author.userName}); insert
     `Reposted by: @{author.userName}` between the Engagement line and body;
     body is the original tweet text (retweet.text).
   - For a quote-tweet (`isQuote: true`): H2 reflects the watched handle as
     author; body is their commentary (fullText); the quoted original renders
     below in a blockquote under a `Quoted:` sub-heading showing
     @{quote.author.userName} + quote.text. QUOTED X Article injection: when
     `quote.id` is in ARTICLE_MD (Step 3, the quoted layer was a collapsed
     article) and not yet in `rendered_article_ids`, render the `Quoted:`
     sub-heading line showing @{quote.author.userName}, then the verbatim
     `ARTICLE_MD[quote.id]` markdown as its own block BELOW the sub-heading,
     NOT `>`-prefixed inside the blockquote. The recovered body carries its own
     `#` headings, `>` blockquotes, and `![image]` refs; wrapping it in an outer
     blockquote would mangle that nested markdown, so a quoted article breaks
     out of the blockquote exactly like a standalone one. Fence it between
     `<!-- quoted article: {title} -->` … `<!-- /quoted article -->` HTML
     comment markers so the boundary is unambiguous, then add `quote.id` to
     `rendered_article_ids`. If `quote.id` is already rendered, emit the
     back-reference line per the render-once rule (no second full body). On an
     enrichment miss, keep the bare-t.co `quote.text` in the normal `Quoted:`
     blockquote and append ` (article body not recovered)`.
   - For a reply (`isReply: true`): insert `Reply to: @{inReplyToUsername}`
     between the Engagement line and body.
   - For pinned tweets (`isPinned: true`): append ` (pinned)` to the H2.
   - For media-bearing tweets, render `Media: 1 image | 2 images | 1 video`
     as a one-line reference; do NOT embed media URLs (expiry unverified).
   - Classification (Authored / Reposted / Mentioned / Drop) is NOT performed
     here, the leaf surfaces the structural facts (the isRetweet/isQuote/
     isReply flags via the rendering above, original authors named); the
     caller or classifier sub-agent classifies.

   When `tweet_count: 0` for a handle (no tweets in window, quiet account):
   body has frontmatter + H1 + single line `No tweets returned for this handle
   in the configured window.` Per-handle `crawl_status: empty`, an empty
   window is a clean operational outcome, not a failure.

   When this handle's run failed (step 2b abort path): placeholder carries the
   file-level frontmatter + H1 + single line `Crawl failed for this handle,
   see diagnostic in return summary.` Per-handle `crawl_status: failed`.

5. Build `per_source_outputs[]` array, one entry per handle in caller order:

     per_source_outputs[i] = {
       handle:            {handles[i]},
       raw_output_path:   {--raw-output-dir}/handle-{handles[i]}.md,
       tweet_count:       {len(projected tweets for handles[i])},
       articles_enriched: {count of DISTINCT article bodies rendered in full for this handle = |rendered_article_ids| for this handle; back-references don't re-count},
       char_count:        {wc -c on the rendered file},
       crawl_status:      {"clean" | "empty" | "failed"},   # per-handle
       apify_run_id:      {runId for this handle},
       diagnostic:        {one-line note when crawl_status == failed; otherwise omit},
     }

   Status semantics:
   - `clean`, handle returned ≥1 tweet; run SUCCEEDED.
   - `empty`, handle returned zero tweets in window (only the sentinel).
   - `failed`, this handle's run FAILED/ABORTED/TIMED-OUT; placeholder written.

6. Compute aggregate fields:

     total_char_count        = sum(entry.char_count for entry in per_source_outputs)
     total_tweet_count       = sum(entry.tweet_count for entry in per_source_outputs)
     total_articles_enriched = sum(entry.articles_enriched for entry in per_source_outputs)
     overall_crawl_status = (
       "clean"   if all entries have crawl_status in {clean, empty}
       else "failed"  if all entries have crawl_status == "failed"
       else "partial"
     )

   Note: `empty` entries do NOT degrade overall status, an empty window is a
   clean outcome. Only mixed clean+failed or all-failed produces
   `partial`/`failed` aggregate. Article enrichment never affects
   `crawl_status`, an enrichment miss is logged via `article_enrichment_status`
   (Step 3e), not the crawl aggregate.

7. Read-back: list {--raw-output-dir} and confirm exactly N files exist (one per
   handle). Mismatch → set overall_crawl_status = "failed" with diagnostic =
   "post-write reconciliation failed: expected N files, found M".
```

### Capture

After the read-back (step 7), capture the structured summary as `CRAWL_RETURN` and proceed to §4.0:

```
raw_output_dir:            {--raw-output-dir}
char_count:                <total across all per-handle files>     # aggregate
tweet_count:               <total across all per-handle groups>    # aggregate
articles_enriched:         <total across all handles, see step 6>
article_enrichment_status: <clean | partial | skipped>             # partial = ≥1 actor batch failed (Step 3e); skipped = no candidates
crawl_status:              <clean | partial | failed>              # aggregate
window_start:              {since}
window_end:                {until}                                 # exclusive
per_source_outputs:        [<one entry per handle, see step 5>]
diagnostic:                <one-line note when crawl_status != clean OR article_enrichment_status == partial; otherwise omit>
```

Do NOT surface raw tweet content or the Apify dataset to the caller, both are on disk at `{--raw-output-dir}` (rendered) or in Apify storage (raw JSON, 7-day retention). §5.0 returns the reference plus summary only.

---

## 4.0 Verify

### Step 1: File-state verification

Verify the raw output directory and per-handle files:

- [ ] Directory exists at `--raw-output-dir` (use Bash: `test -d {DIR}`).
- [ ] One file per handle exists at each `CRAWL_RETURN.per_source_outputs[i].raw_output_path`.
- [ ] When `entry.crawl_status == clean`: file is non-empty (`char_count > 200`). File-level frontmatter alone exceeds 200 bytes, so any clean entry must have `char_count > 200`.
- [ ] When `entry.crawl_status == empty`: file is a placeholder with `char_count > 0` (frontmatter + empty-window line).
- [ ] When `entry.crawl_status == failed`: file is present with `char_count > 0` (placeholder body + diagnostic).

If any check fails (entry status `clean` but file empty/missing, file count ≠ N handles), route to §6.0 (`agent-write-mismatch`).

---

## 5.0 Summary

Return this structured summary to the caller (typically the `/run-pulse` composer):

```
raw_output_dir:            {CRAWL_RETURN.raw_output_dir}
char_count:                {CRAWL_RETURN.char_count}            # aggregate
tweet_count:               {CRAWL_RETURN.tweet_count}           # aggregate
articles_enriched:         {CRAWL_RETURN.articles_enriched}     # aggregate count of recovered article bodies
article_enrichment_status: {CRAWL_RETURN.article_enrichment_status}   # clean | partial | skipped
crawl_status:              {CRAWL_RETURN.crawl_status}          # clean | partial | failed
window_start:              {CRAWL_RETURN.window_start}
window_end:                {CRAWL_RETURN.window_end}            # exclusive
per_source_outputs:        {CRAWL_RETURN.per_source_outputs[]}
  # Each entry: { handle, raw_output_path, tweet_count, articles_enriched, char_count,
  #              crawl_status (clean|empty|failed per-handle), apify_run_id, diagnostic? }
diagnostic:                {CRAWL_RETURN.diagnostic if present}
```

Caller decides next action based on overall `crawl_status` (short-circuit on `failed`; proceed with extraction iteration on `clean` or `partial`) and per-handle `crawl_status` (skip extraction on entries with `crawl_status == failed`; treat `empty` as no-content-this-cycle). The leaf does not retry, the caller governs retry policy.

---

## 6.0 Error Handling

| Error | Response |
|---|---|
| `--handles`, `--raw-output-dir`, or `--max-per-handle` missing from `$ARGUMENTS` | STOP. Report which field is absent. |
| `handles-malformed`, `--handles` does not parse as a JSON array, OR array is empty, OR any normalized entry fails the X handle shape (1-15 chars, `[A-Za-z0-9_]`) | STOP. Report the malformed value (the offending entry when per-entry). A leading `@` is stripped before validation; full URLs are rejected, caller passes bare handles. |
| `--raw-output-dir` not an absolute path | STOP. Report the relative path; caller must resolve. |
| `--max-per-handle` does not parse as a positive integer | STOP. Report the malformed value. |
| `max-per-handle-zero`, `--max-per-handle == 0` | STOP. Report the explicit error: pass a positive integer. Zero is forbidden as a cost-safety guard (per-run-total semantics make an uncapped run unbounded). |
| `raw-output-parent-missing`, parent directory of `--raw-output-dir` does not exist | STOP. Report the missing parent path. Do not create, caller scaffolds the directory tree before invocation. The `--raw-output-dir` itself MAY or MAY NOT pre-exist; §3.0 Step 1 creates it. |
| A single handle's run produces `crawl_status: failed` (Apify FAILED / ABORTED / TIMED-OUT, or poll budget exceeded) | Write the placeholder for that handle, continue the remaining handles. The failure is isolated, aggregate becomes `partial` (or `failed` only if all handles failed). Per-handle diagnostic + `apify_run_id` surface in the return for billing audit. Do not retry within this skill. |
| Crawl produces overall `crawl_status: partial` (some handles succeeded, others failed) | Proceed to §5.0 normally. Return surfaces overall `partial` + per-handle detail in `per_source_outputs[]`. Caller iterates the array, drops failed entries from downstream extraction, continues with clean entries. |
| Crawl produces `crawl_status: empty` for one or more handles | Proceed normally. Per-handle entry surfaces `tweet_count: 0` (valid empty-window result for quiet accounts). Empty does NOT degrade aggregate status. |
| Apify monthly hard limit fires mid-run ("Monthly usage hard limit exceeded" from call-actor or get-actor-run) | Set the affected handle's `crawl_status: failed`, diagnostic = "Apify monthly hard limit exceeded, account billing-capped until next cycle". Remaining handles will hit the same limit; mark them failed without re-calling. Skill returns failure/partial to caller; caller escalates to user (billing event). |
| `call-actor` returns a 4xx error (rate limit, invalid input, Actor temporarily disabled) | Set that handle's `crawl_status: failed` with the Apify error code in the diagnostic. Same caller-decides path as failed runs. Do not retry, rate limits resolve on caller-side cool-down; invalid-input errors require caller correction. |
| `article-enrichment-failed`, an `APIFY_ARTICLE_ACTOR` batch returns FAILED / ABORTED / TIMED-OUT, or its dataset is unreadable (Step 3c-3e) | NON-FATAL. The handle crawls already succeeded. Leave the affected ids out of ARTICLE_MD; Step 4 renders the bare-t.co fallback with ` (article body not recovered)` appended. Set `article_enrichment_status: partial` + a one-line diagnostic. Never degrade `crawl_status` or fail the invocation on an enrichment miss. Do not retry within this skill. |
| `agent-write-mismatch`, the render reports an entry's `crawl_status: clean` but the file is empty/missing, OR file count in `--raw-output-dir` ≠ N handles | Surface the mismatch in the return diagnostic. Set the affected entry's `crawl_status: failed`; recompute overall status. File-state on disk is authoritative. |
| The render produces a malformed structured summary (missing fields, wrong shape, `per_source_outputs[]` length ≠ N handles) | List `--raw-output-dir` directly to recover the actual file count. Build a degraded summary from `wc -c` per file + heuristic status detection (empty body → empty, non-empty → clean). Surface the malformed summary in a diagnostic line. |
