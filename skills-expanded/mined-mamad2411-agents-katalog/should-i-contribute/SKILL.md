---
name: should-i-contribute
description: "Research any open-source repository end to end and answer the core question — SHOULD YOU contribute to it? — with a GO / NO-GO / GO-IF verdict backed by evidence: snapshot, momentum, contribution landscape (PR acceptance rates, outside-contributor merge rates, first-timer outcomes), issue health, governance, community sentiment, and a final go/no-go recommendation. Use when the user asks 'should I contribute to X', wants a before-I-contribute due-diligence check on a project, asks whether a project accepts outside PRs, wants contribution-health numbers like PR merge rates or stale-PR counts, or asks for a deep dive on an open-source codebase's health and dynamics before investing time in it."
---

# Should I Contribute? — repository contribution research

Research ANY open-source repository and produce a detailed analysis report: what it is, how healthy it is, how it actually treats outside contributors, what a PR/issue from a stranger would experience — and, at the end, a clear GO / NO-GO / GO-IF verdict on whether YOU should contribute. The core insight: PR *acceptance* is a much better signal of open-source health than PR *volume* — a project can look busy while quietly ignoring everyone outside the core team.

## Output contract

Deliver ONE markdown report with these sections (see Report template at the end):

1. Executive summary — 3-6 bullet verdict (GO / GO-IF / NO-GO) with the headline numbers
2. Snapshot — identity, stats, license, stack
3. Momentum — is the project alive and shipping?
4. Contribution landscape — the core: open-PR census, age buckets, outside-author share, merge rates, first-timer outcomes
5. Issue health — open issues, stale bugs, "documented bug with unmerged fix" search
6. Governance & maintainability — docs, templates, who actually merges, bus factor
7. Community sentiment — HN/Reddit/Discord signals, maintainer quotes
8. Risks & opportunities for the requester
9. Methodology & caveats — every number gets its source and sample

Every claim MUST be grounded in a number you computed or a quote you read. No vibes.

## Setup

### Target and API access (GitHub, the common case)

- ALWAYS set the target explicitly first: `REPO="owner/name"` (e.g. `REPO="anomalyco/opencode"`). Use `$REPO` in every request. Do NOT rely on `{owner}/{repo}` placeholders — gh only expands those inside a cloned repo or with `-R`.
- `gh` CLI authenticated → 5,000 req/hr. USE IT if available: `gh api "repos/$REPO/..."`. If `gh` is not authenticated, `gh auth login` or fall back to curl with a token: `curl -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$REPO/..."`.
- Raw unauthenticated curl → **60 req/hr core, 10/min search**. The full analysis needs ~20-40 requests. Budget them; do NOT repeat paginated calls wastefully. If you hit 403 rate-limit, authenticate or shrink the sample.
- Always request `per_page=100` (max). Paginate via the `Link: rel="next"` header or `&page=N`. Stop when a page returns fewer than `per_page` items.
- **Renamed/transferred repos**: if a search query 422s with "cannot be searched", the repo was likely renamed — GitHub search doesn't index redirect targets. Resolve the canonical name first: `gh api "repos/$REPO" --jq .full_name` (e.g. `sst/opencode` → `anomalyco/opencode`) and redo all queries with it.

### Non-GitHub hosts

- GitLab: `https://gitlab.com/api/v4/projects/<url-encoded-path>` — mirrors: `merge_requests?state=opened&per_page=100`, `issues`, `releases`; MR merged state: `state=merged`; author identity via `author.username` vs `members/all` (auth required).
- Self-hosted / no API: shallow clone (`git clone --depth=1`) and analyze `git log` — you lose PR-level data; say so in the report.

## Phase 1 — Snapshot

```bash
REPO="owner/name"
gh api "repos/$REPO" --jq '{name, description, language, license: (.license.spdx_id // null), stars: .stargazers_count, forks: .forks_count, open_issues: .open_issues_count, archived, pushed_at, created_at, homepage, topics, default_branch, visibility}'
gh api "repos/$REPO/languages" --jq 'to_entries | sort_by(-.value) | .[:6]'
gh api "repos/$REPO/community/profile" --jq '{health_percentage, files: (.files | with_entries(.value = (.value | type == "object"))) }'
```

Community profile is gold: it reveals whether CONTRIBUTING.md, CODE_OF_CONDUCT, issue/PR templates, README exist — the on-ramp for outsiders. Note `pushed_at` (last commit to default branch).

Read `README.md` (top ~80 lines) and `CONTRIBUTING.md` if present — verbatim quotes from these go in the report. Extract: what is it, who is it for, install/usage, contribution workflow promised vs actual (later phases measure the gap).

## Phase 2 — Momentum

```bash
# 52 weeks of commit counts
gh api "repos/$REPO/stats/commit_activity" --jq '[.[] | .total] | {sum: add, weeks_with_commits: (map(select(. > 0)) | length), last_8_weeks: .[-8:]}'
# Releases (cadence + recency)
gh api "repos/$REPO/releases?per_page=30" --jq '.[] | {tag_name, published_at}'
# Contributor distribution (bus factor: how concentrated is the work?)
# PAGINATE ALL PAGES (per_page=100, page 1..N until empty) — page 1 alone is NOT the contributor base.
gh api "repos/$REPO/contributors?per_page=100&page=1"
# then accumulate; compute: {total: length, top5, top1_share: .[0].contributions / (map(.contributions)|add) * 100}
# Budget fallback: if >10 pages and rate-limited, label the stat "of the first N contributors" — never present as total.
```

Interpretation:
- 6+ months of commits every week + releases in the last 3 months → alive. Watchdog: release gap > 6 months on a popular repo = zombie or big-bang rewrite incoming.
- top-1 contributor > 40% of commits → bus-factor 1; contributions carry personal-review risk.
- Read the last 3 release notes briefly (breaking changes, direction).

## Phase 3 — Contribution landscape (THE core)

Compute ALL of these — they are the heart of the report.

### 3a. Open-PR census

```bash
# All open PRs: paginate per_page=100, page=1,2,... until an empty page; accumulate into one JSON array.
gh api "repos/$REPO/pulls?state=open&per_page=100&page=1"
# Cross-check the accumulated total against search (exact total_count):
gh api "search/issues?q=repo:$REPO+is:pr+is:open&per_page=1" --jq '.total_count'
# Fields per PR: number, title, author_association, created_at, user.login, draft, merged_at (null), labels
```

Compute, from the FULL open set:
- total open PRs
- **outside-core share**: count `author_association` in `NONE | FIRST_TIMER | FIRST_TIME_CONTRIBUTOR | CONTRIBUTOR` vs `MEMBER | OWNER | COLLABORATOR`
- **age buckets**: open longer than 30 days, 90 days, 180 days (from `created_at`)
- **stale queue**: open PRs with no maintainer activity in 30d (approximation: no timeline/review comments; if too costly, report age buckets only and say so)
- draft PR share

### 3b. Closed-PR merge rate (exact, sampled on CLOSED-AT)

WARNING: `pulls?state=closed` sorts by **created_at** (desc), not closed_at — fetching its pages gives "most recently CREATED closed PRs", NOT "last closed". Never call that sample "last N closed".

EXACT method — partition the window into day (or week) slices, fetch EVERY result in each slice, dedupe, aggregate. Ordering becomes irrelevant and the 1,000-result search cap is avoided. This is the tested implementation (run via python3):

```python
import json, subprocess, datetime
from collections import Counter
repo = "owner/name"; days = 90                      # <-- set these
end = datetime.date.today(); start = end - datetime.timedelta(days=days)

def iso(d):  # day-only bounds ("closed:A..B") are INCLUSIVE of both full days and span B-A+1 days —
    return d.strftime("%Y-%m-%dT00:00:00Z")  # use explicit hour bounds for a true half-open [A, B)

def search(q, page=1):
    url = f"search/issues?q={q}&per_page=100&page={page}"
    out = subprocess.run(["gh", "api", url], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[:300])
    return json.loads(out.stdout)

items, seen = [], set()
for d in range(days):
    s = start + datetime.timedelta(days=d)
    q = f"repo:{repo}+is:pr+is:closed+closed:{iso(s)}..{iso(s + datetime.timedelta(days=1))}"
    r = search(q)                                    # page 1 doubles as the total_count probe
    total = r["total_count"]
    assert total <= 1000, f"slice {s} too large ({total}) — split it by hour and recurse"
    page = 1
    while True:
        its = r.get("items", []) if page == 1 else search(q, page).get("items", [])
        for it in its:
            if it["number"] not in seen:
                seen.add(it["number"]); items.append(it)
        if len(its) < 100: break
        page += 1
        r = None

# INVARIANT: fetched population must equal the aggregate closed: total_count.
# Both use half-open [start 00:00Z, end 00:00Z) — exactly `days` full days (through
# yesterday). If they differ, there is a slice gap — do NOT report rates until it matches.
last = end - datetime.timedelta(days=1)
agg = search(f"repo:{repo}+is:pr+is:closed+closed:{iso(start)}..{iso(end)}")["total_count"]
assert len(items) == agg, f"fetched {len(items)} != aggregate {agg} — gap in slicing, abort rates"

merged = [i for i in items if i.get("pull_request", {}).get("merged_at")]
if items:
    print(f"window {start}..{last}: n={len(items)} merged={len(merged)} rate={len(merged)/len(items)*100:.1f}%")
else:
    print(f"window {start}..{last}: n=0 (no PRs closed in window)")
# Funnel cross-tab (3d): merged vs closed-unmerged per author_association bucket.
tab = Counter((i["author_association"], "merged" if i.get("pull_request", {}).get("merged_at") else "unmerged") for i in items)
for (assoc, outcome), n in sorted(tab.items()):
    print(f"{assoc:24s} {outcome:9s} {n}")
```

Bash-only alternative for the per-day iteration (GNU date): `NEXT=$(date -d "$D +1 day" +%F)` — never string-concatenate dates. Also fetch the exact aggregate counts and require them to match your accumulation (same invariant; define the window FIRST). NOTE: `closed:A..B` with day-only bounds is INCLUSIVE of both full days (spans B-A+1 days) — use explicit `T00:00:00Z` hour bounds for half-open windows:

```bash
REPO="owner/name"; START=$(date -d "90 days ago" +%Y-%m-%d); END=$(date -d yesterday +%Y-%m-%d)
# per-day slice: closed:${D}T00:00:00Z..$(date -d "$D +1 day" +%Y-%m-%d)T00:00:00Z
# aggregates over the same half-open [START 00:00Z, today 00:00Z) window:
gh api "search/issues?q=repo:$REPO+is:pr+is:closed+closed:${START}T00:00:00Z..$(date -d "$END +1 day" +%Y-%m-%d)T00:00:00Z&per_page=1" --jq '.total_count'
gh api "search/issues?q=repo:$REPO+is:pr+is:merged+closed:${START}T00:00:00Z..$(date -d "$END +1 day" +%Y-%m-%d)T00:00:00Z&per_page=1" --jq '.total_count'
```

Compute (state window and accumulated n, e.g. "all 262 PRs closed 2026-08-04..08-10"):
- merged vs closed-unmerged counts (cross-check with the two `total_count`s above)
- **overall merge rate** = merged / sample
- **outside-author merge rate**: merged where author_association is outside (NONE/CONTRIBUTOR/FIRST_*)
- **core-author merge rate** for contrast (MEMBER/OWNER/COLLABORATOR)
- **first-timer outcomes**: of closed-unmerged, how many were FIRST_TIME_CONTRIBUTOR/FIRST_TIMER? Of merged, how many?
- **time-window drill-down** (monthly trick): last fully-elapsed month, merged count and outside merges that month. Derive the month dynamically — never hardcode it:

```bash
LAST_MONTH=$(date -d "$(date +%Y-%m-01) -1 day" +%Y-%m)          # last completed month (GNU date; macOS: date -v1d -v-1d +%Y-%m)
START="${LAST_MONTH}-01"; END=$(date -d "${LAST_MONTH}-01 +1 month -1 day" +%Y-%m-%d)
gh api "search/issues?q=repo:$REPO+is:pr+is:merged+merged:${START}..${END}&per_page=1" --jq '.total_count'
gh api "search/issues?q=repo:$REPO+is:pr+is:closed+closed:${START}..${END}&per_page=1" --jq '.total_count'
```

These totals alone cannot split outside vs core merges — the split needs per-item data, so run the 3b day-slice loop over the month window (or `merged:${START}..${END}` items) and classify by `author_association`. State in Methodology which you did.

Budget reality check: full 90-day chunking ≈ 90+ requests (1 per day slice, plus one per extra 100-item page) — fine with authed `gh` (5,000/hr); with unauth curl (60/hr) shrink the window to 7-14 days (fewer slices, exact within it) and LABEL it: "exact for the last N days only". Only if rate limits make even that impossible, fall back to `pulls?state=closed` pages labeled "most recently CREATED closed PRs — created-order approximation, NOT last closed".

Never sample with `sort=updated` / `sort=created` on search — ordering there is relevance/activity-based and is empirically unusable for rates (measured: 0/100 merged by `updated desc` in a window whose true rate was 41%).

### 3c. Author-association decoding

GitHub's `author_association` field on PRs/issues:

| Value | Meaning |
|---|---|
| OWNER | repo owner |
| MEMBER | org member / core team |
| COLLABORATOR | explicitly added collaborator |
| CONTRIBUTOR | has a prior merged PR |
| FIRST_TIME_CONTRIBUTOR | first PR on the repo (has committed before) |
| FIRST_TIMER | very first GitHub interaction |
| NONE | never engaged |

Outside/core split for the report: outside = `NONE` + `FIRST_TIMER` + `FIRST_TIME_CONTRIBUTOR` + `CONTRIBUTOR`; core = `MEMBER` + `OWNER` + `COLLABORATOR`. State the split in the report's Methodology. Caveat: `COLLABORATOR` can include invited community members — check repo collaborators when the count is material.

### 3d. The first-timer funnel

The most damning number: of PRs closed WITHOUT merging, how many were first-time contributors.

GitHub search does NOT support `author_association:` as a qualifier (it 422s), but search result items carry `author_association` — so compute the funnel from the slice-accumulated items of 3b (deduped by number, classified via `.pull_request.merged_at`). The 3b Python already prints this cross-tab; if you accumulated items in a JSON file instead, aggregate with:

```bash
# items.json = accumulated 3b items. Merged status MUST come from .pull_request.merged_at (top-level is null in search results).
jq -r 'group_by(.author_association)[] | "\(.[0].author_association): total=\(length) merged=\(map(select(.pull_request.merged_at != null)) | length)"' items.json
```

If you need a bigger funnel population, extend the window with more day slices (3b step 2).

Report: "of N closed-unmerged PRs in the window, M were by first-timers (FIRST_TIMER/FIRST_TIME_CONTRIBUTOR); of the merged ones, K were first-timers." Also check the 20 most recently MERGED PRs' authors (from the 3b items, sort by `.pull_request.merged_at` descending — no other ordering is valid): any outside names repeated? Repetition = pipeline actually works for newcomers.

## Phase 4 — Issue health

```bash
# Exact open-issue total (search total_count is exact; issue items are capped at 1000):
gh api "search/issues?q=repo:$REPO+is:issue+is:open&per_page=1" --jq '.total_count'
# Census items: paginate ALL open pages (issues endpoint mixes in PRs — filter .pull_request == null)
gh api "repos/$REPO/issues?state=open&per_page=100&page=1"   # pages 1..N until empty; accumulate
# then compute: count, with_bug_label, oldest bug-labeled items
```

- total open issues (note: repo metadata `open_issues_count` includes PRs — use the search total_count above, or your accumulated census)
- **bug-label backlog** and its age: these are the "documented bugs with unmerged PRs sitting that fix them" claims. Do NOT assume a label literally named "bug" — discover the repo's bug-like label(s) first (`gh api "repos/$REPO/labels?per_page=100"` and pick e.g. `bug`, `kind/bug`, `:bug:`), then for the top 5 oldest bug-labeled issues find PRs that actually reference them. A bare `search/issues?q=<number>` hit is FULL-TEXT — it proves nothing about linkage; the reliable source is the issue timeline's `cross-referenced` events (a PR that mentions the issue shows up as `source.issue` with `pull_request` set):
  ```bash
  gh api -H "Accept: application/vnd.github.mockingbird-preview+json" \
    "repos/$REPO/issues/$N/timeline?per_page=100" \
    --jq '[.[] | select(.event == "cross-referenced" and .source.issue.pull_request != null) | .source.issue.number][]' \
  | while read -r n; do
      gh api "repos/$REPO/pulls/$n" --jq \
        '{number, state, merged: (.merged == true), closes_issue: ((.body // "") | test("(?i)(fix(es|ed)?|clos(es|ed)?|resolv(es|ed)?)\\s+#'"$N"'"))}'
    done
  ```
  A closed-but-unmerged PR with a body closing-ref is exactly the finding you want; an open one is a "sitting fix PR" — both open AND closed states matter. If the timeline returns nothing (issue closed by direct commit), fall back to `search/issues?q=repo:$REPO+is:pr+<issue_number>` as CANDIDATES ONLY, and verify each PR body the same way before claiming linkage. State which label(s) you used in Methodology.
- **response proxy** (cheap): of the last 30 open issues, how many have a non-bot maintainer comment? (Use `issues/{n}/timeline` only on a small sample — expensive.)
- stale-bot presence: does the repo run a stale-issue bot? (search issues for the `stale` label, or check `.github/workflows`). A stale bot with a short window explains low open counts — normalize for it.

## Phase 5 — Governance & maintainability

- Read `.github/` contents: CONTRIBUTING.md (promised workflow), issue/PR templates, CODEOWNERS (who reviews what), FUNDING.yml, CI workflows (do they run on PRs from forks? look for the `pull_request` trigger).
- **Who actually merges**: search result items do NOT carry `merged_by` — fetch it per PR from a capped sample of the 30 most recently merged items of the 3b accumulation:
  ```bash
  jq -r '[.[] | select(.pull_request.merged_at != null)] | sort_by(.pull_request.merged_at) | reverse | .[:30][] | .number' items.json | while read -r n; do
    gh api "repos/$REPO/pulls/$n" --jq '.merged_by.login'
  done | sort | uniq -c | sort -rn
  ```
  One person merging everything = single-gate risk. Bot merges (dependabot/renovate) inflate merge rates — EXCLUDE `user.type == "Bot"` from outside-contributor stats and note it. (Do not use `pulls?state=closed` pages for this — they are created-ordered.)
- License check: OSI-approved (MIT/Apache/GPL...) vs source-available (SSPL/ELv2/BUSL/"fair use") — "open source only in name" has a license dimension. Read the LICENSE file if non-standard.
- **Openness signals**: newcomer labels (`good first issue`, `help wanted`) with recent PRs by new authors; maintainer response to contribution questions; any "we don't accept PRs" language in docs/issues (quote it).

## Phase 6 — Community sentiment

```bash
# HN threads (Algolia API, no auth needed). Derive the bare name from $REPO — no literal placeholders:
NAME="${REPO#*/}"   # e.g. anomalyco/opencode -> opencode
curl -s "https://hn.algolia.com/api/v1/search?query=$NAME&tags=story&hitsPerPage=10"
curl -s "https://hn.algolia.com/api/v1/search?query=$NAME&tags=comment"
```

- Read the top HN thread(s); quote 1-2 comments verbatim with links — a quoted comment claiming the project is "open source in name only" is the canonical finding.
- Reddit/Discord/Matrix: `web_search` for `"{repo}" reddit` and `"{repo}" maintainers`; check the project's community link in README.
- **Maintainer acknowledgment check**: search issues/PRs/discussions for maintainer comments admitting a contribution bottleneck ("small team", "PRs welcome but we prioritize the roadmap"). If found, quote and link — e.g. "even their maintainers acknowledge that this is a problem".

## Phase 7 — Synthesis: the verdict

| Signal | GO | GO-IF (conditions) | NO-GO |
|---|---|---|---|
| Outside merge rate | > 15% | 5-15% | < 5% |
| Open PR age | most < 30d | 30-50% older than 90d | majority older than 90d |
| Outside share of open PRs | any | mostly outside | overwhelmingly outside with near-zero merges |
| First-timer outcomes | some merge | few merge | closed-without-merge pattern |
| Maintainer response | engages issues/PRs | selective | acknowledges bottleneck or silent |
| Community docs | CONTRIBUTING + templates real | present, stale | missing or contradictory |

Name the verdict explicitly — this is the answer to "should I contribute?":
- **GO** — outside PRs merge at healthy rates; maintainers respond; a contribution has a realistic path. Contribute.
- **GO-IF** — contributing is viable only under conditions; state them (e.g. "small, well-scoped bug fixes merge; features don't" / "wait until maintainer staffing changes" / "drive-by PRs ignored but issues get linked fixes"). Contribute IF the conditions hold.
- **NO-GO** — outside PRs mostly ignored, single-gate merges, ghost town, or license/governance blocks real contribution (the opencode case: "open source in name only"). Don't invest.

Then answer the requester's actual question directly ("should I contribute?" / "is this good to adopt?" / "what would my PR experience be?") with 3-6 risk/opportunity bullets, each carrying its evidence.

## Report template

```markdown
# Should I Contribute? — {owner}/{repo}

**Verdict: {GO | GO-IF | NO-GO}** · researched {date} · sample sizes in Methodology

## Executive summary
- …

## Snapshot
| field | value | | field | value |
|---|---|---|---|

## Momentum
commits/wk (52w), releases, bus factor …

## Contribution landscape
| metric | value |
|---|---|
| open PRs | N (M outside core) |
| open >30d / >90d | … |
| merge rate (closed in {window}, n={sample}) | … |
| outside-author merge rate | … |
| first-timer merge rate | … |
| closed-unmerged first-timers | … |

## Issue health
…

## Governance & maintainability
…

## Community sentiment
> quote (source link)

## Risks & opportunities
…

## Methodology & caveats
- endpoints used, sample sizes, research date, rate-limit constraints
- author_association split definition
- bot-exclusion rules
- known blind spots (mirror/fork contributions, private core branch, etc.)
```

## Caveats — read before reporting

- Unmerged ≠ rejected: PRs get superseded, closed by staleness, or merged via maintainer re-commit. Always sample the actual `merged_at` field; never infer from labels.
- **`pulls?state=closed` sorts by created_at, NOT closed_at** — never call a pulls-page sample "last N closed". Use the slice-based `closed:` window (3b) for exact closed-at sampling.
- **Search result items report merged status at `.pull_request.merged_at`** — top-level `.merged_at` is always null in search results. And never sample with `sort=updated`/`sort=created`: ordering is relevance/activity-based and empirically unusable for rates.
- **Search caps item results at 1000 per query** — `total_count` stays exact, but per-item breakdowns need window slicing (day/week chunks ≤ 1000, full pagination, dedupe by number) per 3b.
- Bot authors (dependabot, renovate, GitHub Actions) inflate merge rates and contributor counts — exclude `user.type == "Bot"` and note it.
- Small repos: n < 30 closed PRs → say "sample too small for rate" instead of quoting a misleading percentage.
- Rate limits: unauthenticated GitHub is 60 core req/hr + 10/min search. Budget: snapshot (3) + momentum (3+) + open-PR pages + **closed-window day slices (1 req/day + one per extra 100-item page ≈ 8-10 req for 7 days, ~90+ for 90 days)** + searches (2-4) ≈ 25-45 for the short-window variant. On 403, authenticate or shrink the window — never fabricate numbers.
- Numbers decay: state the research date; merge rates move.
- Forks and mirrors: contribution may happen in a separate repo (e.g., a "community edition") — check the README's repo links before concluding.

## Workspace etiquette

- The report is the deliverable: save it as `should-i-contribute-{repo}.md` when the user wants a saved artifact, otherwise print it.
- Keep the raw JSON you computed from (optionally) — reference it in Methodology.

