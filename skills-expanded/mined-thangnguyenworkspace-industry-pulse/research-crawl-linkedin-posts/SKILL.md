---
name: research-crawl-linkedin-posts
description: Batched LinkedIn post crawl from N URLs via Apify; per-source markdown to caller dir; rolled-up + per-source summary.
---

# Research Crawl LinkedIn Posts

**Argument:** $ARGUMENTS (required, see Runtime Inputs)

If `$ARGUMENTS` is empty or missing required fields, STOP and report which fields are absent.

---

## Preamble

### Runtime Inputs

Parse from `$ARGUMENTS`:

```
--source-urls=[URL1,URL2,...]   [JSON-style array of canonical LinkedIn URLs, non-empty; each entry one of 6 supported shapes per §1.0 Step 2. Singular invocation expressed as a single-element array.]
--raw-output-dir={PATH}          [absolute path to a directory where per-source rendered markdown files will be written]
--max-posts={N}                  [positive integer per-URL cost-cap; MUST be ≥ 1, see §1.0 Step 3 + §6.0 row max-posts-zero]

# Optional power params (omit when not needed):
--posted-limit={ENUM}            [any | 1h | 24h | week | month | 3months | 6months | year]
--posted-limit-date={ISO}        [ISO 8601 timestamp lower-bound cutoff, e.g., 2026-04-21T00:00:00Z]
--include-quote-posts={BOOL}     [default true]
--include-reposts={BOOL}         [default true]
--scrape-reactions={BOOL}        [default false; opt-in only, charges extra per post]
--scrape-comments={BOOL}         [default false; opt-in only, charges extra per post]
--max-reactions={N}              [default 5; 0 = unlimited (asymmetric with --max-posts: 0)]
--max-comments={N}               [default 5; 0 = unlimited]
```

Validation rules (before §1.0):

- `--source-urls`, `--raw-output-dir`, and `--max-posts` mandatory. If any missing, STOP and report which.
- `--source-urls` must parse as non-empty JSON array of strings. Else reject (`source-urls-malformed`).
- Each URL must be valid HTTP(S) with host ending in `linkedin.com`. First failing URL → STOP and report (`source-urls-malformed`).
- `--raw-output-dir` must be absolute. Reject relative paths (caller owns path resolution).
- `--max-posts` must parse as integer ≥ 1. Zero rejected per §6.0 `max-posts-zero`, Actor treats `maxPosts: 0` as literal zero (returns no posts), not unlimited.

If any validation fails, STOP and report which field failed.

### Global References

```
APIFY_ACTOR_ID    = harvestapi/linkedin-profile-posts    # locked Actor choice, no-cookie LinkedIn post extraction, $1.50/1k posts (FREE/BRONZE tier), verified 2026-05-05; price is publisher-set and has drifted before ($2 → $1.50), re-verify via mcp__apify__fetch-actor-details (output: {pricing: true}) before high-volume runs
APIFY_CALL_ACTOR  = mcp__apify__call-actor               # Actor invocation, waitSecs 0-45 controls inline wait; no `async` flag exists
APIFY_GET_RUN     = mcp__apify__get-actor-run            # run-status polling endpoint (waitSecs blocks server-side until terminal)
APIFY_GET_ITEMS   = mcp__apify__get-dataset-items        # dataset retrieval, projects nested dot-notation fields via fields= (auto-flatten; bare parent key for array/object fields)
```

Leaf does not read tool guides at runtime, parameter choices in §1.0 Step 4 and the execution procedure in §3.0 already encode the pitfalls (cost-safety cap via `maxPosts`, `call-actor` with `waitSecs:45` inline + `get-actor-run` poll fallback (no `async` flag), dataset id read from `storages.datasets.default.id`, fetch-time narrow-field projection via the `get-dataset-items` `fields=` param (bare parent key for array/object fields), filter dataset by `type === "post"`, group by `query.targetUrl` for per-source split).

### Caller Isolation

Pure primitive, no agent spawn, no pipeline agents, no telemetry. The skill runs the Apify call + dataset render directly in whatever context invokes it; the caller absorbs the MCP dataset context cost (up to 1000+ items per batch land in the caller's window). Callers crawling large batches, or composing this leaf alongside other work, wrap the invocation in their own isolation:

```
Agent({subagent_type: "general-purpose", model: "sonnet", prompt: "Invoke /research-crawl-linkedin-posts with <args>"})
```

Consumer skills document their own isolation choice. The run-pulse composer wraps each source-type leaf in one classifier sub-agent per source-type.

---

## 1.0 Context Capture

### Step 1: Verify raw output directory parent exists

Check parent directory of `--raw-output-dir` exists. If not, route to §6.0 (`raw-output-parent-missing`). Do not create parents, caller owns path resolution. The `--raw-output-dir` itself MAY or MAY NOT exist; §3.0 Step 1 creates it via `mkdir -p` before writing the first per-source file.

### Step 2: Validate URL shape per-URL across array

Parse each URL in `--source-urls` and confirm its path matches one of six supported LinkedIn URL shapes. Apply rules in order; first match wins per URL:

| URL pattern | Detected type | Notes |
|---|---|---|
| `/in/{slug}` (optional trailing slash, optional `?` query) | `profile` | Person profile; `targetUrls` accepts. |
| `/company/{slug}` | `company` | Company page; `targetUrls` accepts. |
| `/showcase/{slug}` | `showcase` | Company showcase page; `targetUrls` accepts. |
| `/school/{slug}` | `school` | School/university page; `targetUrls` accepts. Same entity's `/school/` and `/company/` feeds are 100% identical (verified 2026-05-05), prefer canonicalizing to `/company/{slug}`; if both shapes ever pass through, dedupe output by post `id`, never by input-URL string. |
| `/posts/{slug}` | `post` | Individual post URL; returns the single post. Non-existent slugs resolve to a null-content stub, not an error, detect via `content === null && author.id === null`. |
| `/feed/update/urn:li:activity:{N}` | `activity` | Activity-feed URL; returns the referenced activity. Same null-content stub behavior as `post` for dead activity-IDs. |

Build `url_types[]` parallel to `--source-urls` ordering. Each entry ∈ {`profile`, `company`, `showcase`, `school`, `post`, `activity`}, preserved as per-source diagnostic metadata in the return summary.

If any URL fails to match, route to §6.0 (`unsupported-url-shape`) with offending URL named. Actor accepts these inputs but returns 0-result with $0.001 charge per URL, refusing upfront prevents silent-failure mode.

### Step 3: Validate `--max-posts` lower bound

Confirm `--max-posts ≥ 1`. If `--max-posts == 0`, route to §6.0 (`max-posts-zero`) with explicit error: Actor treats `maxPosts: 0` as literal zero (returns no posts), not unlimited. Asymmetric with `maxReactions: 0` / `maxComments: 0` (which DO mean unlimited). Note: `--max-posts` is per-URL cap; total estimated cost ≈ `N_urls × max-posts × $1.50/1k` at FREE/BRONZE Apify-Store tier.

### Step 4: Construct Apify Actor input

Build Actor input JSON from parsed `$ARGUMENTS`. Include optional fields only when caller supplied them; publisher defaults apply otherwise.

```
ACTOR_INPUT = {
  targetUrls: {--source-urls},          # full array, one batched call
  maxPosts: {--max-posts},               # per-URL cap
  # Optional fields, include only when caller supplied:
  postedLimit: {--posted-limit},
  postedLimitDate: {--posted-limit-date},
  includeQuotePosts: {--include-quote-posts},
  includeReposts: {--include-reposts},
  scrapeReactions: {--scrape-reactions},
  scrapeComments: {--scrape-comments},
  maxReactions: {--max-reactions},
  maxComments: {--max-comments},
}
```

Cost-safety note: `maxPosts` is the only verified-functional cost cap on this Actor. Do NOT add `maxTotalChargeUsd`, verified non-functional on `harvestapi/linkedin-profile-posts` (publisher did not implement `ACTOR_MAX_TOTAL_CHARGE_USD` env-var honoring; caps silently ignored). Per-URL spend ≈ `maxPosts × $1.50/1k` at FREE/BRONZE Apify-Store tier; batch spend ≈ `N_urls × maxPosts × $1.50/1k`.

---

## 2.0 Plan & Confirm

Skill runs autonomously, no user pause. Pure primitive; executes directly in the caller's context. Composed leaves never gate parallelization; direct invocations log the execution config and proceed.


State the planned execution config in one structured log statement, then proceed directly to §3.0:

```
## /research-crawl-linkedin-posts: executing crawl

source_urls:             {--source-urls}                 # N URLs in caller-supplied order
url_types:               {url_types[]}                   # parallel array, length N
raw_output_dir:          {--raw-output-dir}
max_posts:               {--max-posts}                   # per-URL cap
actor:                   {APIFY_ACTOR_ID}
actor_input:             {ACTOR_INPUT}                   # targetUrls = full array; one batched call
execution:               direct (pure primitive, no sub-agent spawn)
invocation:              call-actor waitSecs:45 inline → get-actor-run poll if not yet terminal (no `async` param)
```

---

## 3.0 Crawl

Execute the crawl directly, no sub-agent spawn. Run the Apify `harvestapi/linkedin-profile-posts` Actor across the N source URLs in a single batched call, then write per-source rendered markdown files into `--raw-output-dir`. This step writes raw bytes only, it does NOT extract, summarize, template-fill, restructure, or filter posts by author; the composing router or domain orchestrator handles all downstream transformation.

### Inputs (from §1.0)

```
Source URLs:             {--source-urls}              # N URLs in caller-supplied order
URL types:               {url_types[]}                # parallel array (profile|company|showcase|school|post|activity)
Raw output dir:          {--raw-output-dir}
Max posts cap:           {--max-posts}                # per-URL
Actor:                   harvestapi/linkedin-profile-posts
Actor input (JSON):      {ACTOR_INPUT}                # targetUrls is the FULL array, one batched call
invocation:              call-actor waitSecs:45 → poll get-actor-run if not terminal
```

The Actor input was auto-constructed in §1.0 Step 4. Do NOT substitute different params. Do NOT add `maxTotalChargeUsd`, verified non-functional on this Actor; cost safety relies entirely on `maxPosts`. Invoke via `call-actor` with `waitSecs` (0-45), there is NO `async` flag on the MCP tool (the top-level input schema is `additionalProperties:false`, so an `async` field is rejected client-side). `waitSecs:45` waits inline; harvestapi runs typically finish in ~20s but can run longer on wide windows, so fall back to `get-actor-run` polling when a run is not yet terminal.

### Procedure

Execute these steps in order:

```
1. Ensure {--raw-output-dir} exists. Use Bash `mkdir -p {--raw-output-dir}`.

2. Call mcp__apify__call-actor with the assigned actor + input + waitSecs: 45.
   The MCP tool has NO `async` flag, `waitSecs` (0-45) sets the inline wait.
   Capture `runId`, `status`, and the dataset id at `storages.datasets.default.id`
   (NOT `defaultDatasetId`, that field does not exist on the return). If
   `status === "SUCCEEDED"` already (typical, harvestapi finishes in ~20s),
   skip step 3 and go straight to step 4.

3. If step 2's run was not yet terminal, poll mcp__apify__get-actor-run({ runId,
   waitSecs: 30 }), the param blocks server-side up to 30s per call, re-calling
   until `status` reaches one of:
   - `SUCCEEDED`, proceed to step 4.
   - `FAILED` / `ABORTED` / `TIMED-OUT`, the entire batch failed. Skip steps 4-7;
     write empty placeholder files for each input URL (so callers can rely on
     {--raw-output-dir} containing one file per requested URL), set per-URL
     `crawl_status: failed` with diagnostic = batch failure reason, jump to step 8.

   Maximum poll duration: 600 seconds (10 minutes). If still not terminal after 600s,
   abandon polling, treat as batch failure, write empty placeholders, jump to step 8
   with diagnostic = "Actor run exceeded 600s poll budget".

4. Fetch the dataset via mcp__apify__get-dataset-items({
     datasetId: {storages.datasets.default.id},
     limit: 1000,
     fields: "type,id,linkedinUrl,shareUrn,shareLinkedinUrl,entityId,query.targetUrl,query.sessionId,author,postedAt,content,contentAttributes,engagement,postImages,postVideo,article,document,newsletterTitle,newsletterUrl,header,repostedBy,repostedAt,repostId,repost"
   }).
   - The `fields=` param projects AT FETCH TIME and supports nested dot-notation
     (the server auto-flattens scalar parent prefixes), so the raw ~425-field /
     ~150KB-per-batch payload never enters caller context. This is the
     dataset-read tool's `fields` param, NOT the Actor INPUT `fields[]` (which is
     top-level-only).
   - CRITICAL, array/object fields must be requested as the BARE PARENT KEY, not a
     dotted child: `author`, `engagement` (carries `engagement.reactions[]`),
     `postImages`, `postVideo`, `article`, `document`, `header`, and especially
     `repost` (the recursive quoted-post subtree). A dotted child of any of these
     (e.g. `repost.author.name`, `engagement.reactions.type`) is silently dropped,
     verified via live probe. The grouping key `query.targetUrl` IS a scalar and
     resolves via dot-notation.
   - Read the post count from this call's `totalItemCount`, NOT the inline
     `storages.datasets.default.itemCount` on the call-actor return, which is
     captured mid-run and under-reports.
   - The PROJECTED dataset can still exceed the MCP tool's inline return cap on
     larger batches (≈83KB at 3 URLs × 8 posts) and auto-spill to a tool-results
     file instead of returning inline. Read it off-context (`jq` over the spill
     file, or a targeted Read), do NOT assume the projected items land inline.
     The `fields=` win is keeping the ~425-field RAW payload out of context, not
     guaranteeing the projected slice fits the return cap.
   - Paginate via `offset` when dataset > 1000 items. With N_urls × max_posts post
     items expected (plus optional reaction/comment sibling items), large batches
     across many URLs may exceed 1000.

5. Filter dataset to `item.type === "post"`. Sibling `type: "reaction"` and
   `type: "comment"` items are present when scrapeReactions/scrapeComments are true;
   they are NOT posts and must be excluded from the rendered post list.

6. Group post items by `query.targetUrl`. Each post item carries a `query` object
   identifying which input URL produced it. Build a map:

     groups = { URL1: [post, post, ...], URL2: [...], ..., URLN: [...] }

   Initialize the map keyed by ALL N input URLs, URLs that returned zero posts
   (empty windows, restricted profiles) map to empty arrays. This guarantees one
   output file per input URL.

7. For each input URL, render its post array to a markdown file inside
   {--raw-output-dir}. Filename rule:

     filename = `{url_type}-{url-slug}.md`

   where `url_type` comes from the parallel `url_types[]` array and `url-slug` is
   derived from the URL path's last meaningful segment:
   - `/in/{slug}` → `profile-{slug}.md`
   - `/company/{slug}` → `company-{slug}.md`
   - `/showcase/{slug}` → `showcase-{slug}.md`
   - `/school/{slug}` → `school-{slug}.md`
   - `/posts/{slug}` → `post-{slug}.md`
   - `/feed/update/urn:li:activity:{N}` → `activity-{N}.md`

   Slug normalization: lowercase; strip trailing slashes and query strings.
   Type prefix structurally prevents collisions between different source types.

   File structure per source:

   ---
   type: Crawl Output
   schema: ephemeral-raw-crawl
   source_tool: harvestapi/linkedin-profile-posts
   source_url: {this URL}
   url_type: {this URL's url_type}
   crawl_run_at: {ISO 8601 timestamp of this batch run}
   apify_run_id: {runId}
   apify_dataset_id: {storages.datasets.default.id}
   post_count: {N posts in this URL's group after type-filter}
   input_params:
     max_posts: {--max-posts}
     # other input fields when caller supplied them
   ---

   # LinkedIn Posts, {source_url}

   ## Post 1, {author.name} ({author.publicIdentifier or author.universalName}), {postedAt.date}
   URL: {linkedinUrl}
   Engagement: {engagement.likes} likes · {engagement.comments} comments · {engagement.shares} shares
   Reactions: {compact reaction-type breakdown when present, else omit line}

   {post body, preserve original line breaks; render images/videos/articles as
   inline references; render reposts/quotes as nested blockquotes}

   ---

   ## Post 2, ...

   Rendering rules (field paths verified live against harvestapi output; same as singular invocation):
   - Each post is one H2 section separated by horizontal rules (`---`).
   - Heading includes `author.name`, the author handle (`author.publicIdentifier`,
     falling back to `author.universalName` when null, companies populate
     universalName, not publicIdentifier), and the post date (`postedAt.date`).
   - URL line uses the bare LinkedIn permalink (`linkedinUrl`).
   - Body text is the top-level `content` field; preserve original line breaks; bare
     lnkd.in URLs stay as-is.
   - Engagement line is one line, dot-separated, from `engagement.likes` /
     `engagement.comments` / `engagement.shares`.
   - Reactions line included only when the `engagement.reactions[]` breakdown
     (array of `{type, count}`) is non-empty.
   - Reshare detection, two DISTINCT shapes; check in this order:
     - VERBATIM REPOST, `repostedBy` object present (and `header.text` reads
       "… reposted this"). Top-level `author`/`content`/media are the ORIGINAL post
       (flattened); H2 reflects the ORIGINAL author; insert
       `Reposted by: {repostedBy.name} ({repostedBy.publicIdentifier or repostedBy.universalName})`
       between the Engagement/Reactions line and body.
     - QUOTE-SHARE, top-level `repostId` present + a nested `repost` object (a full
       recursive post). H2 reflects the resharing source as author; body is the
       resharer's own commentary (top-level `content`); the quoted original renders
       below in a blockquote under a `Quoted:` sub-heading showing `repost.author.name`
       (+ handle via `repost.author.publicIdentifier or .universalName`) and
       `repost.content`.
     - Otherwise, native post (neither `repostedBy` nor `repost` present).
   - Media (each a distinct key; render a one-line `Media:` reference; do NOT embed
     URLs, they carry ~24h expiry):
     - `postImages[]` → `N image(s)`
     - `postVideo` object (`{thumbnailUrl, videoUrl}`) → `1 video`
     - `article` object (`{title, link, …}`) → render the article title + link on one line
     - `document` object (`{title, totalPageCount, …}`) → `document (N pages)`

   When `post_count: 0` for a URL (no posts in window, restricted profile, empty
   feed): body has frontmatter + H1 + single line `No posts returned for this
   source in the configured window.` Per-source `crawl_status: clean`, empty
   results from real-but-quiet sources differ from Actor failures.

   When the batch-level Actor failed (step 3 abort path), per-source placeholders
   carry the file-level frontmatter + H1 + single line `Crawl failed at batch
   level, see diagnostic in return summary.` Per-source `crawl_status: failed`.

8. Build `per_source_outputs[]` array, one entry per input URL in caller order:

     per_source_outputs[i] = {
       source_url:      {URLs[i]},
       raw_output_path: {--raw-output-dir}/{filename for URLs[i]},
       url_type:        {url_types[i]},
       post_count:      {len(groups[URLs[i]])},
       char_count:      {wc -c on the rendered file},
       crawl_status:    {"clean" | "failed"},        # per-source, NOT aggregate
       diagnostic:      {one-line note when crawl_status != clean; otherwise omit},
     }

9. Compute aggregate fields:

     total_char_count     = sum(entry.char_count for entry in per_source_outputs)
     total_post_count     = sum(entry.post_count for entry in per_source_outputs)
     overall_crawl_status = (
       "clean"    if all entries have crawl_status == "clean"
       else "failed"   if all entries have crawl_status == "failed"
       else "partial"
     )

10. Read-back: list {--raw-output-dir} and confirm exactly N files exist (one per
    input URL). Mismatch → set overall_crawl_status = "failed" with diagnostic =
    "post-write reconciliation failed: expected N files, found M".
```

### Capture

After the read-back (step 10), capture the structured summary as `CRAWL_RETURN` and proceed to §4.0:

```
raw_output_dir:        {--raw-output-dir}
char_count:            <total across all per-source files>   # aggregate
post_count:            <total across all per-source post groups>
crawl_status:          <clean | partial | failed>            # aggregate
apify_run_id:          {runId}
per_source_outputs:    [<one entry per input URL, see step 8>]
diagnostic:            <one-line note when crawl_status != clean; otherwise omit>
```

Do NOT surface raw markdown content or the Apify dataset to the caller, both are on disk at `{--raw-output-dir}` (rendered) or in Apify storage (raw JSON, 7-day retention). §5.0 returns the reference plus summary only.

---

## 4.0 Verify

### Step 1: File-state verification

Verify raw output directory and per-source files:

- [ ] Directory exists at `--raw-output-dir` (use Bash: `test -d {DIR}`).
- [ ] One file per input URL exists at each `CRAWL_RETURN.per_source_outputs[i].raw_output_path`.
- [ ] When `entry.crawl_status == clean`: file is non-empty (`char_count > 200`). File-level frontmatter alone exceeds 200 bytes, so any clean entry must have `char_count > 200`.
- [ ] When `entry.crawl_status == failed`: file is a placeholder with `char_count > 0` (placeholder body); missing file violates the one-file-per-URL invariant and routes to `agent-write-mismatch`.

If any check fails (entry status `clean` but file empty/missing, file count ≠ N input URLs), route to §6.0 (`agent-write-mismatch`).

---

## 5.0 Summary

Return this structured summary to the caller (typically the `/run-pulse` composer):

```
raw_output_dir:        {--raw-output-dir}
char_count:            {CRAWL_RETURN.char_count}            # aggregate
post_count:            {CRAWL_RETURN.post_count}            # aggregate
crawl_status:          {CRAWL_RETURN.crawl_status}          # clean | partial | failed
apify_run_id:          {CRAWL_RETURN.apify_run_id}
per_source_outputs:    {CRAWL_RETURN.per_source_outputs[]}
  # Each entry: { source_url, raw_output_path, url_type, post_count, char_count,
  #              crawl_status (clean|failed per-source), diagnostic? }
diagnostic:            {CRAWL_RETURN.diagnostic if present}
```

Caller decides next action based on overall `crawl_status` (short-circuit on `failed`; proceed with extraction iteration on `clean` or `partial`) and per-source `crawl_status` (skip extraction on entries with `crawl_status == failed`; drop or retry per its own policy). Leaf does not retry, caller governs retry policy.

**Attribution caveat**: a profile/company feed mixes the owner's own posts with reposts of third-party content (rendered with a `Reposted by:` line or a `Quoted:` sub-heading per the §3.0 reshare-detection rules); consumers must attribute each post by its rendered author, never by which source file it sits in, before treating content as the profile owner's words.

---

## 6.0 Error Handling

| Error | Response |
|---|---|
| `--source-urls`, `--raw-output-dir`, or `--max-posts` missing from `$ARGUMENTS` | STOP. Report which field is absent. |
| `source-urls-malformed`, `--source-urls` does not parse as JSON array, OR array is empty, OR any URL is not a valid HTTP(S) URL with host ending in `linkedin.com` | STOP. Report the malformed value (the offending URL when per-URL). |
| `--raw-output-dir` not an absolute path | STOP. Report the relative path; caller must resolve. |
| `--max-posts` does not parse as a positive integer | STOP. Report the malformed value. |
| `max-posts-zero`, `--max-posts == 0` | STOP. Report the explicit error: Actor treats `maxPosts: 0` as literal zero (returns no posts), not unlimited. Asymmetric with `maxReactions: 0` / `maxComments: 0` (which DO mean unlimited). Caller must pass a positive integer. |
| `unsupported-url-shape`, one or more URLs in the array have host `linkedin.com` but path matches none of the 6 supported shapes (e.g., `/groups/...`, `/events/...`, legacy `?mid=...`) | STOP. Report the offending URL(s). Actor accepts these inputs but returns 0-result with $0.001 charge per URL, refusing upfront prevents the silent-failure mode. |
| `raw-output-parent-missing`, parent directory of `--raw-output-dir` does not exist | STOP. Report the missing parent path. Do not create, caller scaffolds the directory tree before invocation. The `--raw-output-dir` itself MAY or MAY NOT pre-exist; §3.0 Step 1 creates it. |
| Crawl produces overall `crawl_status: failed` (batch-level Apify FAILED / ABORTED / TIMED-OUT, or poll budget exceeded) | Proceed to §5.0 with the failure summary. Return to caller with overall `crawl_status: failed` + diagnostic + per-source entries all marked failed + `apify_run_id` (for billing audit). Caller decides retry / drop. Do not retry within this skill. |
| Crawl produces overall `crawl_status: partial` (some per-source entries succeeded, others failed) | Proceed to §5.0 normally. Return surfaces overall `partial` + per-source detail in `per_source_outputs[]`. Caller iterates the array, drops failed entries from downstream extraction, continues with clean entries. |
| Crawl produces `crawl_status: clean` for an entry but `post_count: 0` | Proceed normally. Per-source entry surfaces `post_count: 0` (valid empty-window result). Caller decides whether to retry (transient batch flakiness, observed once 2026-05-04, did not reproduce on the 2026-05-05 verification sweep; defensively documented), drop the source, or accept as-is (deleted profile, restricted, empty window). |
| The render produces a malformed structured summary (missing fields, wrong shape, `per_source_outputs[]` length ≠ N input URLs) | List `--raw-output-dir` directly to recover actual file count. Build a degraded summary from `wc -c` per file + heuristic status detection (empty → failed, non-empty → clean). Surface the malformed summary in a diagnostic line. |
| `agent-write-mismatch`, the render reports an entry's `crawl_status: clean` but file is empty/missing, OR file count in `--raw-output-dir` ≠ N input URLs | Surface the mismatch in the return diagnostic. Set affected entry's `crawl_status: failed`; recompute overall status. File-state on disk is authoritative. |
| Apify monthly hard limit fires mid-run (returns "Monthly usage hard limit exceeded" error from call-actor or get-actor-run) | Set overall `crawl_status: failed`, diagnostic = "Apify monthly hard limit exceeded, account billing-capped until next cycle". Skill returns failure to caller; caller decides whether to escalate to user (likely yes, billing event). |
| `call-actor` returns 4xx error (rate limit, invalid input, Actor temporarily disabled) | Set overall `crawl_status: failed` with the Apify error code in diagnostic. Same caller-decides path as failed runs. Do not retry, rate limits resolve on caller-side cool-down; invalid-input errors require caller correction. |
