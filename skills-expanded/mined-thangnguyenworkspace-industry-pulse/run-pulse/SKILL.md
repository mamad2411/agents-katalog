---
name: run-pulse
description: Watchlist-driven intelligence pipeline, crawl LinkedIn/X/RSS/email via composed leaves, classify and domain-tag in parallel sub-agents, then synthesize one neutral signals brief. The brief is the public core; your relevance + delivery layer attaches at the seam.
---

# Run Pulse

**Argument:** $ARGUMENTS (optional, all flags optional with defaults; see Runtime Inputs)

Crawl four source-types, classify and domain-tag each in parallel classifier sub-agents, then synthesize one neutral **signals brief**: the main thread authors a signals-only, third-person brief that states what happened across your watchlist and why it matters. The brief is the reusable core's final artifact and the handoff point, your own relevance layer (and any delivery) attaches downstream at the seam (§3.0 Step 5).

---

## Preamble

### Runtime Inputs

Parse `$ARGUMENTS` for these optional flags; apply defaults when absent:

```
--days={N}                     [positive integer; default 1; time window passed to every crawl leaf]
--linkedin-max-posts={N}       [positive integer; default 3; per-URL cap for the LinkedIn leaf]
--email-max-per-sender={N}     [positive integer; default 10; per-sender cap for the email leaf]
--x-max-per-handle={N}         [positive integer; default 5; per-handle cap for the X leaf]
--rss-max-items-per-feed={N}   [positive integer; default 15; per-feed cap for the RSS leaf]
```

All flags optional. Invalid values (non-positive integers, malformed) → halt with the matching §6.0 row.

### Global References

All paths are repo-relative (the skill runs with the repo root as the working directory) and are the configuration surface, repoint any of them to your own layout. The `config/` inputs are the working copies you create from the shipped `.example` templates (copy `config/profile.example.md` → `config/profile.md`, each `config/watchlists/{lane}-watchlist.example.md` → `config/watchlists/{lane}-watchlist.md`); `output/` is gitignored and regenerable per run.

```
PROFILE_PATH               = config/profile.md
PROFILE_DOMAIN_ENUM        = config/profile.md §3.0   (the domain enum + scope/boundary classifier contract, the tagging vocabulary)
LINKEDIN_WATCHLIST_PATH    = config/watchlists/linkedin-watchlist.md
EMAIL_WATCHLIST_PATH       = config/watchlists/email-watchlist.md
X_WATCHLIST_PATH           = config/watchlists/x-watchlist.md
RSS_WATCHLIST_PATH         = config/watchlists/rss-watchlist.md
RAW_DIR                    = output/raw/      (gitignored; per-source-type subdirs)
TAGGED_DIR                 = output/tagged/   (gitignored; per-run tagged-output files)
REPORTS_DIR                = output/reports/  (the briefs; gitignored by default, repoint or un-ignore to keep them)
TAGGED_SCHEMA              = schemas/schema-pulse-tagged-output.md
REPORT_SCHEMA              = schemas/schema-pulse-report.md
RUN_DIR                    = output/reports/pulse-report-{report_date}/   (per-run folder)
BRIEF_PATH                 = {RUN_DIR}pulse-report-{report_date}.md   (the neutral signals brief, the public artifact and the handoff to your relevance layer)
L1_TOKEN_BUDGET            = 25000   (per-RSS-worker raw-token budget; drives the RSS volume auto-scaler bin count)
L1_CONCURRENCY_CAP         = 14      (max parallel classifier workers; tune to your harness's concurrency limit)
SOURCES_PER_WORKER         = 30      (per-bin source cap for the count-sharded X + LinkedIn lanes; a dial, not a wall, dial down for wide --days windows, a raised per-source post cap, or the heavier LinkedIn lane. Daily defaults assumed: 5 posts/X-handle, 3/LinkedIn-URL, 1-day window.)
```

This skill composes four pure-primitive leaves (`/research-crawl-linkedin-posts`, `/research-crawl-email`, `/research-crawl-x-posts`, `/research-crawl-rss`); it never calls `mcp__apify__*` or `mcp__claude_ai_Gmail__*` directly. Each leaf owns its API mechanics and pitfalls; context isolation is caller-owned. Architecture: L0 leaves crawl → classifier sub-agents classify + domain-tag (email = one worker; X + LinkedIn count-sharded; RSS volume-auto-scaled) → the main thread synthesizes the neutral signals brief. The heavy, parallelizable reading lives in the sub-agents; the main thread holds only the tagged signal files and the synthesis. The public core ends at the brief, your relevance and delivery layer attaches at the seam documented in §3.0 Step 5.

---

## 1.0 Context Capture

### Step 1: Read the profile

Read `PROFILE_PATH`. Capture `version:` for provenance. Capture §1.0 North Star + Current Bets, §2.0 Skill Targets, §3.0 Domain Interests (`PROFILE_DOMAIN_ENUM`, the tagging vocabulary the classifiers run against), §4.0 Lens Filters, the full lens carried into classification and the synthesis. The profile is your lens; replace its contents to retarget the whole pipeline at a different reader.

### Step 2: Read all four watchlists

Read each watchlist; extract the per-source-type source list and capture its entry count. Flag a source-type empty when its watchlist has no entries (or frontmatter `total_entries: 0`):

- **LinkedIn** (`LINKEDIN_WATCHLIST_PATH`): the canonical-URL column of every §3.0 entry → ordered list of LinkedIn URLs.
- **Email** (`EMAIL_WATCHLIST_PATH`): the URL column (the literal email address) of every §3.0 entry → ordered list of sender addresses.
- **X** (`X_WATCHLIST_PATH`): the URL column (`https://x.com/{handle}`) of every §3.0 entry → extract the **bare handle** from each URL (strip scheme/host + any leading `@`) → ordered list of bare handles. The X leaf takes bare handles, not URLs.
- **RSS** (`RSS_WATCHLIST_PATH`): the `URL` + `Entity Type` columns of every §3.0 Watchlist Entries row → ordered list of `{feed_url, class}` pairs, mapping `URL`→`feed_url` and `Entity Type`→`class` (`Deep-Content Feed`→`deep-content`, `News-Firehose Feed`→`news-firehose`).

If all four watchlists are empty, halt with §6.0 (`all-watchlists-empty`).

### Step 3: RSS crawl-first (volume probe)

Skip when the RSS watchlist is empty. The RSS leaf writes feed bodies to disk via a Python subprocess and returns only a manifest, running it here lands only per-feed counts + token estimates in context, letting the auto-scaler size dispatch from real volume.

Set `rss_raw_dir = output/raw/rss/rss-raw-{report_date}/`. If it already exists, remove it first (`rm -rf {rss_raw_dir}`): it can only be residue from an earlier same-day run, a completed same-day run is caught separately by the `report-already-exists` halt at Step 5, and the dir is gitignored and regenerable, so clearing it prevents stale feed files from a halted run bleeding into this run's binning. Invoke `/research-crawl-rss` via the Skill tool with:

```
--feed-urls=[<all RSS feed_urls>]
--raw-output-dir={rss_raw_dir}
--max-items-per-feed={--rss-max-items-per-feed}
--days={--days}
```

Read the returned summary + the `manifest.json` at `manifest_path`. Capture per-feed `{feed_url, class, items_emitted, est_tokens, crawl_status, raw_output_path}`. Do **not** read the per-feed body files, they stay on disk for the RSS classifier workers. Aggregate `crawl_status: failed` → halt with §6.0 (`rss-leaf-failed`).

### Step 4: Bin the sharded lanes → classifier worker counts (auto-scaler)

Size every lane's classifier dispatch here, never hard-coded. RSS bins by measured token volume (crawl-first probe at Step 3); X and LinkedIn bin by source count (the paid Apify lanes cannot free-probe volume, so they shard on the known watchlist count before crawling); email is always one worker.

**RSS: volume bins** (skip when RSS empty, `N_rss = 0`):

1. Keep feeds with per-feed `crawl_status` in `{clean, empty}`; a per-feed `failed` drops from downstream (surfaced in §5.0).
2. Partition kept feeds by `class`: a `deep-content` group and a `news-firehose` group. The two classes load on different axes (deep = low-count/high-token, news = high-count/low-token), so they never share a bin.
3. Within each group, greedily pack feeds into bins so each bin's summed `est_tokens` stays ≤ `L1_TOKEN_BUDGET`. A single feed whose `est_tokens` alone exceeds the budget gets its own bin (the per-feed `--rss-max-items-per-feed` cap already bounds it). News feeds packed together keep overlapping coverage in one worker's context for consistent tagging.
4. `N_rss` = total RSS bin count. Record each bin's feed list (the bin's `raw_output_path`s) for §3.0 dispatch.

**X + LinkedIn: count bins** (per lane, skip when that lane is empty):

5. For X: `N_x_bins = ceil(x_handle_count / SOURCES_PER_WORKER)`; split the ordered bare-handle list into `N_x_bins` contiguous near-even slices (e.g., 51 handles at 30 → 2 bins of 26 + 25). For LinkedIn: `N_linkedin_bins = ceil(linkedin_source_count / SOURCES_PER_WORKER)`; split the ordered URL list the same way. Record each bin's source slice for §3.0 dispatch. A lane at or under `SOURCES_PER_WORKER` yields exactly one bin, the unsharded case falls out for free.

**Email + concurrency cap:**

6. `N_email` = 1 when email is non-empty, else 0 (email is never sharded, small sender count).
7. `total_workers = N_x_bins + N_linkedin_bins + N_email + N_rss`. If `total_workers > L1_CONCURRENCY_CAP`, cap-merge, merge the smallest bins (start with the lane carrying the most bins, then RSS news bins) until `total_workers ≤ L1_CONCURRENCY_CAP`, and log the cap-hit in §5.0 (a signal to raise the cap or split a watchlist).

### Step 5: Compute paths + cost estimate

- `report_date` = today (ISO).
- `RUN_DIR` = `output/reports/pulse-report-{report_date}/`. If it exists, halt with §6.0 (`report-already-exists`).
- `BRIEF_PATH` = `{RUN_DIR}pulse-report-{report_date}.md`.
- `tagged_dir` = `output/tagged/tagged-{report_date}/`.
- Per-source-type raw dirs: `linkedin_raw_dir`, `email_raw_dir`, `x_raw_dir` = `output/raw/{type}/{type}-raw-{report_date}/` (the RSS dir was created at Step 3).
- Cost estimate (paid crawls only; email + RSS are free): LinkedIn `linkedin_source_count × --linkedin-max-posts × $1.50 / 1000`; X `x_handle_count × --x-max-per-handle × $0.0004`. Realistic ≈ 30-60% of worst case for short `--days` windows.

No scaffold-output-dirs step, each leaf, each classifier worker, and the brief writer `mkdir -p`s its own dated output subdir.

---

## 2.0 Plan & Confirm

### Pre-flight: assert crawl-tool availability

Before presenting the plan (and before any paid dispatch at §3.0), assert the external crawl tools are connected. This is a cheap tool-namespace presence check, not an API call. It fails fast here rather than deep inside the classifier workers, where a disconnected Apify silently ships a LinkedIn + X-less brief with no warning, discovered only after the paid dispatch returns:

- `mcp__apify__*`, required by the LinkedIn + X leaves. Assert only when LinkedIn or X is non-empty. Absent → halt with §6.0 (`apify-unavailable`). Paid sources are load-bearing; this halt is unconditional.
- `mcp__claude_ai_Gmail__*`, required by the email leaf. Assert only when email is non-empty. Absent → the email source-type can drop, but treat the drop as a decision, not an FYI: a lapsed connector silently ships a brief missing the entire email layer. Surface the absence as an explicit reconnect-or-proceed gate folded into the §2.0 plan-confirm pause (see Plan below). Reconnecting is a quick action and no money has been spent at this point, so a silent default-drop forfeits a cheap recovery.

### Plan

Present the planned scope:

```
| Field | Value |
|---|---|
| Days window | {--days} |
| LinkedIn | {linkedin_source_count} URLs × max {--linkedin-max-posts}/URL → {N_linkedin_bins} worker(s)  (or "skipped, empty") |
| Email | {email_sender_count} senders × max {--email-max-per-sender}/sender  (or "skipped, empty", or "dropped, Gmail not connected") |
| X | {x_handle_count} handles × max {--x-max-per-handle}/handle → {N_x_bins} worker(s)  (or "skipped, empty") |
| RSS | {rss_feed_count} feeds → {rss_in_window_items} items in window → {N_rss} worker(s)  (or "skipped, empty") |
| Classifier workers | {total_workers} total ({N_x_bins} X + {N_linkedin_bins} LinkedIn + {N_email} email + {N_rss} RSS); cap {L1_CONCURRENCY_CAP}, cap-merged when a cap-hit fired |
| Cost estimate (paid) | LinkedIn ${linkedin_cost} + X ${x_cost}  (~30-60% realistic); email + RSS free |
| Profile version | v{profile_version_consumed} |
| Brief destination | {BRIEF_PATH} |
```

RSS is already crawled (free) at §1.0 Step 3, so the plan shows its real volume + computed worker count. The paid LinkedIn + X crawls run only after approval, at §3.0.

**Gmail reconnect-or-proceed gate.** When the pre-flight found `mcp__claude_ai_Gmail__*` absent and the email watchlist is non-empty, the plan's Email row reads `dropped, Gmail not connected` and the approval pause carries two options: (1) reconnect the Gmail MCP, then re-run the namespace check and proceed with email included; (2) proceed without email this run. Resolve the choice at this same pause, do not dispatch until it is answered.

Wait for user approval before §3.0.

---

## 3.0 Execute

### Step 1: Dispatch all classifier sub-agents in one message

Dispatch every classifier worker in a **single message** via parallel `Agent({...})` calls, one per LinkedIn bin (`j = 1..N_linkedin_bins`), one email worker, one per X bin (`i = 1..N_x_bins`), plus one per RSS bin (`k = 1..N_rss`). Sequential dispatch loses the parallelism; author all calls in the same response. Skip any empty source-type.

```
Agent({subagent_type: "general-purpose", prompt: <LINKEDIN_WORKER_PROMPT[j]>})  # one per LinkedIn bin j
Agent({subagent_type: "general-purpose", prompt: <EMAIL_WORKER_PROMPT>})         # if email non-empty
Agent({subagent_type: "general-purpose", prompt: <X_WORKER_PROMPT[i]>})          # one per X bin i
Agent({subagent_type: "general-purpose", prompt: <RSS_WORKER_PROMPT[k]>})        # one per RSS bin k
```

Two worker shapes share one classify-tag-write contract, differing only in how they obtain raw:

- **Crawl-and-classify** (LinkedIn / email / X): invoke the source-type's pure-primitive leaf in-worker on the worker's source slice (isolating the Apify / Gmail raw dataset out of the main thread), read the per-source raw files, then classify + domain-tag. X and LinkedIn shard into one worker per count-bin (§1.0 Step 4); email is a single worker over all senders.
- **RSS classifier** (one per bin): the RSS raw is already on disk from §1.0 Step 3; read only the assigned bin's per-feed files, then classify + domain-tag.

**SHARED CLASSIFIER CONTRACT**: embed verbatim in every worker prompt (interpolate `{source_type}`, `{tagged_path}`, `{report_date}`, `{--days}`, `{profile_version}`, and the profile §3.0 enum + §4.0 drop criteria):

```
You are the {source_type} signals classifier-tagger. Classify and domain-tag every item from one source-type, preserve each source's framing, and write ONE tagged-output file. You do NOT assemble the brief and you do NOT dedupe.

# Classify each item: bucket = Authored / Reposted / Mentioned / Drop
- Authored, the watchlist source originated the item.
- Reposted, the source reshared another author's item verbatim. A quote-post with substantive commentary counts as Authored, not Reposted.
- Mentioned, the source is referenced or quoted inside another's item; surface only when the mention adds signal.
- Drop, none of the above, OR matches a profile drop criterion: <embed PROFILE §4.0 Lens Filters drop criteria verbatim, unrelated affiliate/promo, off-topic personal posts, recruiter spam, surface-level news with no implication payload, calendar/event-announcement posts>. Drop items are excluded from the file.

# Domain-tag each survivor: keys from the profile's domain enum
Tag each survivor with one or more domain keys (an item may carry a primary + secondary key). Apply the scope + boundary cross-routing rules verbatim: <embed PROFILE §3.0 domain enum + scope/boundary cross-routing rules verbatim>.

# Preserve framing: do NOT flatten, do NOT dedupe
Write each survivor's compact_summary to capture THIS source's own framing, the angle it took + notable wording, in 1-3 sentences, not a neutral flattened fact. Use no em dashes in compact_summary prose (commas, parentheses, or sentence breaks instead) so none flow into the brief. When multiple of your sources cover the same story, keep each as its own item (repetition is signal; differing framings are insight). Never collapse duplicates.

# Write the tagged-output file (conform to schema-pulse-tagged-output)
mkdir -p the tagged dir, then write to: {tagged_path}
- Frontmatter: type "Pulse Tagged Output"; schema pulse-tagged-output; created/updated/tagged_date {report_date}; tags [pulse, tagged, {source_type}, {report_date}]; alias []; version 1.0; description (source-type + dominant domains); source_type {source_type}; days_window {--days}; source_count {count of every source-instance you successfully crawled, crawl_status clean or empty, not just those that returned items; hard-failed crawls excluded}; item_count {survivors}; profile_version_consumed {profile_version}.
- Body "## 1.0 Tagged Signals": one bullet per survivor,
  - **[{author_class}]** {source} · `{domain-key}`,`{domain-key}` · {item date YYYY-MM-DD}, {compact_summary preserving framing} ↳ {permalink}
  Empty scope → the placeholder line: No items surfaced for {source_type} in {--days}-day window.

# Final report (your last message ONLY: no raw content)
source_type · source_count · item_count (survivors) · bucket counts (Authored/Reposted/Mentioned/Drop) · domain-tag distribution · tagged_path (absolute) · crawl_status · any leaf/read failure.
```

Per-worker crawl preamble prepended to the shared contract:

`LINKEDIN_WORKER_PROMPT[j]` (`source_type=linkedin`, `tagged_path={tagged_dir}/linkedin-tagged-bin-{j}.md`), one per LinkedIn count-bin, scoped to bin `j`'s URL slice:

```
# Obtain raw: crawl via the leaf (isolates the Apify dataset in YOUR context)
Invoke /research-crawl-linkedin-posts via the Skill tool with exactly:
  --source-urls=[{linkedin urls for bin j}]
  --raw-output-dir={linkedin_raw_dir}
  --max-posts={--linkedin-max-posts}
  --posted-limit-date={today − --days at 00:00:00Z, ISO 8601}
Read the returned summary, then Read each per_source_outputs[] file whose crawl_status is clean or empty at its raw_output_path. The raw dataset stays in YOUR context, it never returns to the main thread. source_count = the count of every URL you successfully crawled in your bin (crawl_status clean or empty), not just those that returned items; reachable-but-quiet sources count, hard-failed crawls do not (a bin of 20 URLs where 7 returned no posts in the window still reports source_count: 20). Then apply the shared contract below.
```

`EMAIL_WORKER_PROMPT` (`source_type=email`, `tagged_path={tagged_dir}/email-tagged.md`):

```
# Obtain raw: crawl via the leaf (isolates the Gmail thread bodies in YOUR context)
Invoke /research-crawl-email via the Skill tool with exactly:
  --senders=[{email addresses}]
  --raw-output-dir={email_raw_dir}
  --days={--days}
  --max-per-sender={--email-max-per-sender}
Read the returned summary, then Read each per_source_outputs[] file whose crawl_status is clean or empty. source_count = the count of every sender you successfully crawled in your scope (crawl_status clean or empty), not just those that returned items; reachable-but-quiet sources count, hard-failed crawls do not (a scope of 20 senders where 7 returned no posts in the window still reports source_count: 20). Then apply the shared contract below.
```

`X_WORKER_PROMPT[i]` (`source_type=x`, `tagged_path={tagged_dir}/x-tagged-bin-{i}.md`), one per X count-bin, scoped to bin `i`'s handle slice:

```
# Obtain raw: crawl via the leaf (isolates the Apify dataset in YOUR context)
Invoke /research-crawl-x-posts via the Skill tool with exactly:
  --handles=[{bare handles for bin i}]
  --raw-output-dir={x_raw_dir}
  --max-per-handle={--x-max-per-handle}
  --days={--days}
Read the returned summary, then Read each per_source_outputs[] file whose crawl_status is clean or empty. source_count = the count of every handle you successfully crawled in your bin (crawl_status clean or empty), not just those that returned items; reachable-but-quiet sources count, hard-failed crawls do not (a bin of 20 handles where 7 returned no posts in the window still reports source_count: 20). Then apply the shared contract below.
```

`RSS_WORKER_PROMPT[k]` (`source_type=rss`, `tagged_path={tagged_dir}/rss-tagged-bin-{k}.md`), classifier-only, raw already on disk:

```
# Obtain raw: read your assigned pre-crawled feed files (no crawl; RSS was crawled at §1.0 Step 3)
Read these per-feed files (your bin):
  {newline-separated raw_output_path list for bin k}
source_count = the count of every feed you successfully read in your bin (crawl_status clean or empty), not just those that returned items; reachable-but-quiet feeds count, feeds that failed to fetch do not (a bin of 20 feeds where 7 returned no posts in the window still reports source_count: 20). Then apply the shared contract below.
```

Each X / LinkedIn / RSS bin writes its own `{lane}-tagged-bin-{k}.md` (email writes the single `email-tagged.md`); the synthesis reads every `*tagged*.md` in `tagged_dir`, so multi-bin lanes assemble without change.

### Step 2: Collect summaries + verify tagged files

Block until all workers return. Capture each worker's final-report summary (counts, `tagged_path`, `crawl_status`). For each, Read the tagged file and confirm: it exists; frontmatter conforms to `TAGGED_SCHEMA`; every survivor bullet carries an `author_class` + ≥1 domain key + permalink. Off-shape or missing → surface in §5.0; do not auto-retry. A worker reporting a leaf/crawl failure → route to the matching §6.0 row; surviving source-types proceed.

### Step 3: Author the signals brief

Read every `*tagged*.md` in `tagged_dir` (matches the single `email-tagged.md` plus every `{lane}-tagged-bin-{k}.md` shard). With the profile lens (§1.0 Step 1), author the **signals brief** at `BRIEF_PATH` conforming to `REPORT_SCHEMA`. The brief carries: a coverage strip + §1.0 Executive Summary + §2.0 Per-Domain Pulse + §3.0 Cross-Domain & Cross-Source Patterns. No personal lens, no relevance hooks, no action digest, those belong to your relevance layer downstream of the brief (§3.0 Step 5).

**The brief is the synthesis locus and the public artifact.** This is the layer that adds the implication payload (takeaway + implication + why-it-matters) the tagged files omit by contract, the lens-driven judgment pass. Anything you (or your relevance layer) build downstream stands on the brief, so the hard cross-thread reasoning is finished here: every cross-domain pattern and cross-source convergence is already present and resolved in the brief. The test: a fresh reader given only the brief + one relevance context could write the correct relevance take without re-reading the raw signal. Density, not length, maximum resolved reasoning per token.

**Voice is neutral third-person: forwardable register.** Because the brief is written neutral and personal-free from the start, it IS a forwardable public artifact by construction (no separate scrub pass derives it). No "you"/"your", no reader-specific asides, no "given your work on X" hooks. State facts and implications in neutral analytical voice. Any coach/assistant re-voicing for a specific reader is the relevance layer's job, not the brief's.

**Author section by section, not in one pass.** Create `BRIEF_PATH` first (frontmatter per Step 6 + the coverage strip), then write one section at a time in order (§1.0 → §2.0 → §3.0), appending each via Edit. After writing each section, re-read it and check it against the discipline below (neutral voice, depth, permalink integrity, no em dashes, every-entity-framed) before starting the next. The main thread is the single author, so one neutral narrative voice carries across the brief.

**Cross-source signal: the discipline that defines this layer.** The tagged files preserve each source's framing and do not dedupe, so the same story may arrive from several sources/source-types. Treat that as signal:

- **Repetition = salience.** A story corroborated across many sources is more important, weight it toward §1.0 and toward the top of its §2.0 domain. List the corroborating sources and append a terse spread cue (`across N sources`).
- **Framing divergence = insight.** When corroborating sources frame a story differently, that divergence is the surfaced insight. Give the strongest such convergences full prose in §3.0, name the story, who's carrying it, and specifically how each source's framing differs + what that tells you. A single-domain convergence (one story, many sources, same domain) qualifies as a §3.0 trend.
- Never silently merge corroborating items into one neutral fact, the spread and the divergence are the value.
- **Weigh disconfirming evidence: convergence is not automatically bullish.** When many sources pile onto one story, actively look for the counter-signal in the day's pull and connect it rather than amplifying the consensus (e.g. read a multi-source hype convergence against a groupthink / bubble / "still-unsolved" signal also present that day). Surface the tension; a brief that only echoes the loudest story is weaker than one that names what would falsify it.

**Permalink integrity is non-negotiable.** The tagged files carry a `↳ {permalink}` tail per survivor, carry every one through to the brief. Every §2.0 item ends with its permalink(s) (` · {permalink}`, multi-source items listing one per corroborating source); §3.0 trend prose cites permalinks where useful per the schema shapes. Never summarize links away during assembly: a claim the reader cannot click through to its source fails the brief's core job, and the §4.0 Verify link check halts on a zero-link report. Permalinks flow from the brief into any downstream relevance artifact, so dropping them here breaks the source-link chain.

**No em dashes anywhere.** A hard formatting rule across every section, including item separators. Use commas, parentheses, colons, or sentence breaks instead. The QC gate (Step 4) strips any that remain; the brief ships with zero.

**Title Sentence convention.** A bolded lead opening a §1.0 bullet body or a §3.0 trend body is a Title Sentence: first letter of every word capitalized, ends with a period (e.g., `**The Agentic-Commerce Protocol Race Just Got Real This Week.**`), scannable as a headline alone. Sentence-case bold leads still apply at §2.0 per-item takeaways. Optional closing Title Sentence at §3.0 trends when a sharp takeaway is worth headlining.

**Analytical depth is the bar: second-order analysis, not summary.** Every item earns its place with a non-obvious point: a second-order effect (X happened, so the non-obvious consequence is Y), a hidden tension or trade-off, an incentive read (who benefits from a framing and what that reveals), a cross-item pattern (several items that are secretly one shift), or a contrarian / disconfirming angle. Surface what most readers skim past, the buried detail that is the actual point, and never explain the obvious. Where the day allows, develop one connective idea across sections (plant it in §2.0, use it as the lens in §3.0). Write connected, flowing sentences with transitions, never a telegraphic "takeaway, implication. why." fragment. **Every named entity earns its framing:** when you name a company, product, person, or protocol, give what it is, why it matters, and what trend it signals, never a bare name. The QC gate flags any unframed entity as a fact-dump.

Sections render in this order (full rules at `REPORT_SCHEMA`):

- **Coverage strip.** One blockquote directly under the H1, before §1.0, derived from the survivor counts: `> **Today:** {total} signals · LinkedIn {n} · X {n} · RSS {n} · Email {n} · across {n} domains · {--days}-day window`. Omit any source-type term whose count is 0.
- **§1.0 Executive Summary.** 3-5 scannable headline bullets covering the run's heaviest cross-domain and cross-source patterns; stories corroborated across many sources weight toward the top. Bullet: `**{Title Sentence.}** {2-3 sentence neutral body}. *{italic metadata tail: heaviest domain / trend ref / source-spread like "across 6 sources"}*`. State the claim + a `§3.0` pointer for stories that earn a full trend, do not pre-build §3.0's source-by-source evidence here.
- **§2.0 Per-Domain Pulse.** One H3 per domain (profile §3.0 enum), ordered by item-count (heaviest first); empty domains omit, single-item domains still render. Each H3 opens with a 2-3 sentence neutral intro, then weaves all source-types into one cross-source narrative. Item: `**{takeaway}.** {implication}. {why-it-matters}. {source inline tag(s)} · {permalink}` (no em dashes; sentence-case bold lead, period-separated), with varied depth, marquee items developed with genuine second-order analysis, supporting items kept tight. When corroborated across sources, list the sources + a terse `across N sources` cue. When a domain carries ≥6 items, group its bullets under bold thematic sub-labels named in the intro; thin domains stay flat. Vary the intro opening across domains.
- **§3.0 Cross-Domain & Cross-Source Patterns.** Trends spanning 2+ §2.0 domains OR a single story corroborated across multiple sources/source-types. Each trend: H3 (sentence-case) → Title Sentence claim → 2-3 paragraphs neutral analytical prose (for a cross-source convergence: who's carrying it + how each source frames it differently). Per-trend cap ~400 words. **Minimum 2 Mermaid diagrams across §3.0**: pick the trends with strongest topology fit (convergence-flow, layer-stack, framing-divergence spread); use `<br/>` for node-label line breaks, never `\n`.

Length serves comprehension, not a target: depth and connective reasoning set the length. The only firm rule is the floor: never compress a section to where ideas can't develop. Each section surfacing zero items renders the schema placeholder line.

### Step 4: QC the brief (the gate: dedicated agent, writer-applies-fix loop)

The brief is the synthesis locus, so it carries a quality gate before it is final. Run the §4.0 mechanical checks first, then this QC fix-loop.

**QC gate: dedicated agent.** Spawn one QC sub-agent with the author's full source set: `BRIEF_PATH`; every `*tagged*.md` in `tagged_dir` (the primary grounding set); the four watchlist files (secondary grounding for role/title attributions); and the RSS manifest (`{rss_raw_dir}/manifest.json`, when RSS ran) for frontmatter count reconciliation. A verifier given only the tagged subset over-flags (watchlist-stated roles read as invented; `rss_feed_count` reads as irreconcilable), hand it the full set. It evaluates the brief against the QC checklist (writing quality · narrative flow · context + framing · source attribution · link completeness · logical transitions · factual consistency · em dashes · fact-dump test · neutral-voice integrity · overall readability) and returns structured findings only (JSON: `{"verdict": "clean"|"findings", "findings":[{"section","severity":"block"|"polish","issue","suggested_fix"}]}`), it does not edit the file.

**Fix (writer = the main thread).** The author holds the brief in context, so the author applies the fixes, sub-agents are unreliable editing the written file. Carry adjudicated decisions forward so each pass does new work:

1. Adjudicate each finding. Apply actionable findings to `BRIEF_PATH` via Edit (prioritize `block` over `polish`). To overrule a finding, record it on a running "adjudicated, do not re-flag" list with named evidence (the file + line/field that grounds the overrule); an overrule without named evidence is not allowed, apply the fix instead.
2. Re-run the §4.0 mechanical checks on the patched sections.
3. Re-spawn the QC sub-agent on the patched brief, passing the same full source set AND the running "adjudicated, do not re-flag" list. The agent treats that list as settled.
4. Scope the final pass to verification only, the specific patches plus any remaining `block`-severity issue, not a full re-review.
5. Loop until the QC verdict is `clean` OR 3 passes complete, whichever comes first.

Residual unfixed `block`-severity findings surface in §5.0 (the run still proceeds, the brief is on disk). After the loop, the brief is gated and final.

### Step 5: The seam: hand off to your relevance + delivery layer

This is where the reusable core ends and your layer begins. The skill's job is done once the gated brief is on disk; everything below is the part you implement, and the brief is the contract between the two.

- **IN**: the gated brief at `BRIEF_PATH` (neutral signals markdown per `REPORT_SCHEMA`) plus a relevance context object you supply: a portfolio, a company, a personal project, a startup, a research area, or any domain-specific context. Treat the brief's patterns + per-domain analysis as finished; your layer APPLIES it, it does not re-derive it.
- **PROCESS**: your own relevance logic. Recommended pattern: one sub-agent per context object when several relevance checks run in parallel (the brief in, a relevance take out, each in its own isolated window); an inline check in the main workflow when there are only one or two. The context lever is the same one this pipeline uses, keep the heavy per-context reading out of the orchestrating thread.
- **OUT**: a relevance artifact per context (the repo ships a recommended relevance schema as a shape, not a mandate) plus any downstream steps you own: notify, route, or deliver.
- **Delivery is yours, and the default already happened.** The brief is written to disk at `BRIEF_PATH`, that is the out-of-box delivery, no PDF/email/notify dependency. Rendering to PDF, emailing, or pushing a notification are optional adapters you add; none are part of the core.

`examples/` ships self-contained, swappable reference implementations of this seam (portfolio-relevance and project-relevance) that consume the brief; the core never imports them, so delete or replace them freely. The full extension guide, the context-object model, sub-agent-vs-inline patterns, delivery adapters, and adding a new source-type lane, lives in `docs/extending.md`.

### Step 6: Frontmatter fields

The brief file is created at the start of Step 3 and built up section by section; frontmatter (per `REPORT_SCHEMA`) is written at file creation from captured runtime data: `report_date`, `days_window`, the per-source counts (survivors after Drop, from the worker summaries; X/LinkedIn/RSS summed across bins; `rss_feed_count` from the §1.0 Step 3 manifest), and `profile_version_consumed`.

---

## 4.0 Verify

Re-read `BRIEF_PATH` and run the mechanical structural checks (the gate §3.0 Step 4 references). Confirm:

- Frontmatter carries all required fields per `REPORT_SCHEMA`; per-source counts match the worker summaries.
- A coverage-strip blockquote sits directly under the H1, before §1.0, with counts matching frontmatter.
- The three H2 headings are present in order: `## 1.0 Executive Summary`, `## 2.0 Per-Domain Pulse`, `## 3.0 Cross-Domain & Cross-Source Patterns`. No section structurally absent.
- §1.0 bullets open with a Title Sentence + neutral body + italic metadata tail.
- §2.0 H3 domains are profile-enum names ordered by item-count, each opening with a neutral intro; multi-source items list corroborating sources + `across N sources`; ≥6-item domains sub-labelled.
- §3.0 carries ≥2 ` ```mermaid ` fences (below threshold → warn, do not halt); mermaid uses `<br/>`, never `\n`.
- Link coverage: count `http`-prefixed permalinks across §2.0 + §3.0. Zero → halt with §6.0 (`report-shape-drift`, zero link coverage). Below ~80% of the bullet count → warn.
- No em dashes: count literal `, `. Any present → warn (the QC gate strips them).
- Neutral third-person voice throughout, spot-check three bullets; any "you"/"your" reader-coach framing → drift warning, since the brief must be forwardable.
- Analytical-depth spot-check, three items carry a non-obvious point, not a fact-dump.

Any structural miss → §6.0 (`report-shape-drift`) with the specific failure named.

---

## 5.0 Summary

Report the run:

- Brief: `BRIEF_PATH` (in `RUN_DIR`).
- Per-source-type survivors: `LinkedIn {linkedin_post_count} · Email {email_message_count} · X {x_post_count} · RSS {rss_item_count}`; Drop counts summed across workers.
- Classifier dispatch: `{total_workers} workers ({N_x_bins} X + {N_linkedin_bins} LinkedIn + {N_email} email + {N_rss} RSS)`; note any auto-scaler cap-hit from §1.0 Step 4.
- Per-source-type source counts: `LinkedIn {linkedin_source_count} · Email {email_sender_count} · X {x_handle_count} · RSS {rss_feed_count}`. LinkedIn/X Apify run ids for billing audit where returned.
- QC: passes run + any residual `block`-severity findings (§3.0 Step 4).
- Any tagged-file shape warnings from §3.0 Step 2; any per-source leaf failures.
- Brief size: `{char_count}`.
- One-paragraph teaser quoting the headline pattern from §3.0 (or "Quiet pattern day, no trends surfaced.").

Next: the brief is ready for your relevance layer. Apply it via the seam (§3.0 Step 5), see `examples/` and `docs/extending.md`, or queue `/run-pulse --days=7` for a wider weekly compression run.

---

## 6.0 Error Handling

| Error | Response |
|---|---|
| `--days`, `--linkedin-max-posts`, `--email-max-per-sender`, `--x-max-per-handle`, or `--rss-max-items-per-feed` parses as non-positive integer | Halt. Report which flag failed + the offending value. |
| `missing-watchlist`, a referenced watchlist path does not exist | Halt. Report the missing path. Watchlist files are user-curated; create per `schema-pulse-watchlist` (copy the shipped `.example` template) before retrying. |
| `all-watchlists-empty`, all four watchlists empty | Halt. Nothing to crawl. Populate at least one watchlist before invoking. |
| `apify-unavailable`, the `mcp__apify__*` namespace is absent at the §2.0 pre-flight while LinkedIn or X is non-empty | Halt before any dispatch. Surface: "Apify MCP not connected; configure it (see docs/setup.md), then re-run." The paid LinkedIn + X crawls cannot run without it. The user can re-invoke after connecting, or empty the LinkedIn + X watchlists to run RSS + email only. |
| `output-parent-missing`, the `output/` directory tree cannot be created | Halt. Report the path. Confirm the repo root is writable. |
| `report-already-exists`, `RUN_DIR` exists from an earlier same-day run | Halt. Surface the existing folder; user deletes the prior run folder and re-invokes, or picks a different `--days` window. |
| `rss-leaf-failed`, `/research-crawl-rss` returns aggregate `crawl_status: failed` at §1.0 Step 3 | Halt. Surface the leaf diagnostic. Common cause: all feeds JS-challenge-gated or network failure. Re-invoke after resolving, or proceed by emptying the RSS watchlist for this run. |
| `{linkedin,email,x}-leaf-failed`, a crawl-and-classify worker reports its leaf returned aggregate `crawl_status: failed` | The failed source-type drops from the brief; surviving source-types proceed. Surface the diagnostic in §5.0. LinkedIn/X cause: Apify monthly limit / batch failure. Email cause: Gmail MCP permission denied (first use per spawn context), approve and re-invoke. |
| `tagged-file-shape-drift`, a tagged file fails the §3.0 Step 2 conformance check | Surface the specific drift in §5.0; that source-type's items drop from synthesis. Do not auto-retry. |
| `report-write-failed`, Write to `BRIEF_PATH` fails | Halt. Surface the filesystem error. Likely cause: `RUN_DIR` not writable. |
| `report-shape-drift`, §4.0 Verify finds the written brief does not conform to `REPORT_SCHEMA` | Halt. Surface the specific drift (missing frontmatter field, missing section heading, section structurally absent, zero link coverage). Manual fix or re-invoke; do not silently re-write. |
