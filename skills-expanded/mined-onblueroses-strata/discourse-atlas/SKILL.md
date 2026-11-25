---
name: discourse-atlas
description: "Map niche posts and comments across forums, newsletters, and social feeds into a quotable compendium. Use the atlas fleet method for writing rather than people. Trigger on underrated posts, buried comments, small newsletters, threads, or a discourse compendium for a proposal or essay."
---

# Discourse Atlas

Third sibling: `topic-atlas` maps the claims and evidence of a field rather than its writing.

**Goal**: a compendium of niche writing on N topics: low-reach posts, buried comments under famous posts, shortforms, small newsletters, discussion and forecasting threads, and public social posts. Every item quotes its page verbatim, links it, and names the reader's questions it could inform.
**Success means**: every item has a fetched URL, a verbatim quote, a date, a reach figure (karma, likes, or "comment on <parent>") and a why-line; the canon appears only as parents whose comment threads were read; lane coverage sections say what was searched and what was unreachable.
**Stop when**: the merged index exists and the primary has hand-written the top picks. Using the material is the reader's work.

## The one structural rule

As in topic-atlas: fleets write `lanes/`, the merge script writes the index, judgment writes the top layer. No script edits the curated section; the primary reads the ranked index and picks what earns a line.

## Layout

```
$RESEARCH_ROOT/YYYY-MM-DD-<slug>/
├── BRIEF.md          goal, the reader's questions, ruling, lanes, runtime, layout
├── brief-common.md   shared lane brief: niche criteria, canon exclusions, item format,
│                     JSON schema, coverage section, tools per source family, rules
├── gen_briefs.py     topics (name, scope, search terms, seed writers, question ids)
│                     × source families → lanes/*.brief.md
├── lanes/            <lane>.brief.md, <lane>.md (items, then ## Coverage), <lane>.json
├── logs/             per-lane out/err/done, FLEET.txt
├── launch.sh         rolling pool of codex-fast lanes
├── merge.py          dedupe by normalised URL, score, COMPENDIUM.md + json + html
├── CURATED.md        the hand-written top picks, included verbatim by merge.py
└── COMPENDIUM.md     header stats · top picks · by question · by topic · coverage
```

Reuse a prior run's `brief-common.md` and `gen_briefs.py` as templates when available; the layout above is the contract.

## Lanes

A lane is one topic on one source family. Three families, hunted separately because their tools differ:

- **A, specialist forums.** Some mirrors render whole comment threads as plain HTML; forum GraphQL endpoints answer GET queries for comment lists; tag pages and quick-takes list posts regardless of reach. Half the items should be comments: name the canonical parents first, read their threads.
- **B, newsletters and other forums.** Writer archives; well-known roundups mined as link indexes, never as items; discussion forums with search APIs and item permalinks; forecasting comment threads; magazine sites when the piece is not famous.
- **C, social feeds.** Use a public search API when available without login. Where it is not, use search-engine indexing and public status or thread pages; the lane reports what stayed inaccessible.

Explicit search terms per topic go in the brief (a lane whose queries miss a phrasing misses the lane). Seed writers are starting points, not a whitelist; unknown authors are the point.

## Item format

Markdown block plus a JSON array with the same keys: `title, url, author, venue, date, type (post|comment|shortform|thread|note), reach, topic, questions[], quote (25–60 words verbatim), summary, why, niche`. A comment's URL is its permalink, not the post. Unknown fields say `unknown`; nothing is invented.

## Niche criteria

Exclude the canon of the field as items (famous essays, official publications, paper preprints, big roundups); include comments on it. Prefer forum posts under roughly 150 reach points, or under roughly 100 on smaller forums, shortforms, small newsletters, and threads by small accounts; prefer recent work, older only if unusually relevant. "Interesting" means a specific claim with a mechanism, number, case, counterexample or sharp question; not general worry or news.

## Runtime

`codex-fast` (gpt-6-luna, web search on), one lane per brief, a rolling pool, `< /dev/null` on every lane, outputs written incrementally so a timeout loses nothing. Measured bases (pool width, items per lane, social-feed reachability, wall time) belong in the run's BRIEF.md. Lanes here map public writing, not people, so the free `omp-search` route (a free model; the runtime's delegation reference; `quote-check` on its output) is admissible as a lane runner: same brief, `omp-search --cwd "$LANE" "$(cat brief.md)"`, a narrow pool because every `:free` run on the key shares one rate limit. It has not run a discourse fleet yet; `codex-fast` stays the measured default until one run compares yield per lane.

## Merge and curation

`merge.py` normalises URLs (drop utm, www, twitter→x), dedupes, keeps the longest summary, unions question tags, scores (recurrence ×2, +1 comment/thread, +1 dated 2025–26, +1 low reach, +0.5 per question up to 3, +0.5 substantial quote) and writes the index by question and by topic, with every lane's coverage section appended. The primary then reads the ranked index, checks quotes on the page for anything that will be cited, and writes `CURATED.md`: the top picks with a one-line reason each. Publish the html as an artifact when the reader wants to browse.

## Rules

Read-only except a lane's two output files. No logins, no browser automation, no scraping behind walls. Nothing about the reader in any lane output. Quotes verbatim or not at all.
