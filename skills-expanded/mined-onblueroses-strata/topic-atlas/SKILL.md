---
name: topic-atlas
description: "Map what is known about a topic with question-led research lanes, append-only raw output, a hand-curated atlas of sourced claims and disagreements, then a synthesis. Trigger on state-of-field questions, comparisons, or literature and practice scans. No people data."
---

# Topic Atlas

Part of the atlas family. `discourse-atlas` maps niche writing, this one maps what is known about a topic: the claims, the numbers, the mechanisms, the cases, the tools, where sources disagree, and what nobody has settled.

**Goal**: answer the brief's questions from pages someone actually read, and leave a field map that the next session can extend instead of redoing.
**Success means**: every atlas item carries a verbatim quote, its URL, its date and its evidence kind; every lane ends with a coverage section naming what it searched and what it could not reach; every claim the synthesis rests on was spot-checked on its page by the primary; disagreement between sources appears as a listed disagreement, never a silent pick; what the research could not establish is listed under Nulls with what was tried.
**Stop when**: SYNTHESIS.md answers the questions or names the holes, the counts line is current, and OptMem points at the directory.

## Scale to the question

| Size | When | Shape |
|---|---|---|
| **inline** | one line of inquiry settles it: a version, a definition, "does X support Y" | search and fetch in the primary, answer in chat, no directory |
| **fleet** | 3 to 12 separable angles, answer wanted once | directory, lanes, `SYNTHESIS.md`; no `atlas.md` |
| **atlas** | a field the operator will keep returning to, or a second round is already in view | fleet plus curated `atlas.md`, rounds, coverage ledger |

A "X vs Y" question takes three lanes whatever the size: A alone and B alone, neither told it is a comparison, then C seeded with the axes A and B surfaced. Comparative writing is a different population of sources than either solo pass.

Check what is already here before any spend: `$MEMO_CMD recall '<topic regex>'`, then search `$RESEARCH_ROOT` and the local decision corpus. Configure paths in [config.example](../config.example). A hit turns "what are the options" into "what changed since we decided Y".

## The one structural rule

Fleets write only to `raw/`; the atlas and the synthesis are written by hand after review. No script, fleet job or regex edits a curated file. The primary reads lane output critically, spot-checks on the page, and hand-picks what earns a line. Curation is the merge.

## Layout

```
$RESEARCH_ROOT/YYYY-MM-DD-<slug>/
├── BRIEF.md       the questions, the generic context, lanes with their seed queries,
│                  runtime, ruling if one was asked for
├── raw/           briefs/<lane>.md, out/<lane>.md (+ .err), FLEET_PROGRESS, FLEET_DONE;
│                  per round: raw/r2/...; append-only, quote-don't-edit
├── atlas.md       (atlas size) counts line, then curated items by section
├── SYNTHESIS.md   verdict first, then the questions answered, cited to lanes and pages
└── CHECKS.md      what the primary verified on primary pages, date, outcome
```

Reusable patterns from prior runs: a synthesis with a "facts checked today" section, a second round aimed at gaps, and a "what we missed" lane closing each round.

## Item format

```markdown
- **One shared connection may receive any event** — one hub holds the connection and routes
  events. "<verbatim excerpt from a fetched vendor page>" (source URL, source date)
  · evidence: vendor doc · status: checked <date> · bears on Q2
```

- One claim per item. A number carries its unit, its date and what it measured; "2,000 users" without a date is not a number.
- `evidence:` is one of measurement, vendor doc, paper, case, practitioner report, opinion. A model's training is none of these; a finding without a fetched page stays out of the atlas.
- `status:` is `checked <date>` (the primary opened the page and the quote is there), `unchecked` (lane-reported only) or `UNVERIFIED` (the lane could not open a primary page). `contested → D3` points at the disagreement entry.
- Counts line, first line of atlas.md: `items 84 · checked 31 · UNVERIFIED 9 · disagreements 4 · lanes 8/8 reported`. Only checked items are quoted outward.

Sections of atlas.md, in this order, each omitted when empty: Claims · Numbers · Mechanisms · Cases · Tools and projects (stars, licence, last commit, as read on the page and dated) · Disagreements (both sides, each cited) · Open questions · Pointers (people, venues, canon reading; a person here is a pointer to their writing, never a contact: no addresses, no hunt) · Nulls.

## Flow

**Brief.** Write the questions as questions, numbered Q1…Qn; a lane answers questions, not topics. One prior fleet was re-run mid-flight because topic-shaped lanes were too constrained; the ruling was to use the reader's actual questions. State seed queries per lane and license the lane to derive more; a lane whose queries miss a phrasing misses the lane. The context paragraph is generic and public: nothing about the operator, no vault text, no CRM, no private project names, because the default runtime logs prompts. A brief that cannot be made public stays on the subscription tier (below). Ask the operator for a ruling only when lanes or spend would differ materially by the answer; a curiosity question is its own ruling.

**Map.** Round 1 is wide: one lane per angle, 6 to 12 lanes, each a report rather than a list. Lanes are aimed at pages that describe something that happened or was measured; a lane aimed at rosters and overviews returns overviews. Every brief carries the partial-output rule: write the report incrementally, a partial report with a coverage note beats an exhaustive search that times out with nothing.

**Check.** Before anything is curated or quoted: run `quote-check raw/out/*.md > raw/quote-check.tsv` on every round (it fetches the page behind each findings-table row and reports exact, partial, not found; ruling of 2026-11-10: always on free fleets), then open the page behind every item the synthesis will rest on, confirm the quote and the date, record the outcome in `CHECKS.md`. In a prior fleet, all sampled quotes verified, while another synthesis caught a lane's wrong claim about a vendor rate limit by reading the primary page. Grade each lane in one line: reported, thin, failed, off-brief.

**Aim.** Round 2 goes where round 1 left holes: the Nulls, the disagreements, the claims that rest on one source, plus one "what we missed" lane that reads round 1's coverage sections and hunts the adjacent angles. Rounds live in `raw/r2/` and so on; a rerun never overwrites an output file.

**Curate** (atlas size). Grep the atlas before adding; dedup is a curator's grep. An item without a quote stays in `raw/`. A section past ~40 items means the admission test is loose: tighten to what bears on a question.

**Synthesize.** `SYNTHESIS.md` opens with the verdict or the answer, then takes the questions in order, each answered in a few sentences with lane and page citations, then Disagreements, then Nulls with their detection limit (which queries, which sources, which were unreachable) and the strongest remaining route. A null closes nothing; retiring a question is the operator's ruling. Judgment work: runs in the primary, never in a fleet.

**Point.** OptMem `P` pointer to the directory and an `E` event for each fleet completion with the counts; the entity hub if the topic has one. Publish `SYNTHESIS.md` or the atlas as an artifact when the operator wants to browse or share. Commit the research repository.

## Runtime

Default is a free model, because topic briefs are public inputs (the operator ruling 2026-09-17: continual mapping and web-research loops over public inputs run on free models, not the Codex subscription). Free models run only on public inputs, inside a sandbox with no view of the machine, and every quote they return is checked with `quote-check`. `LANE_RUNNER` names the read-only free-model runner; the report is its stdout:

```bash
D="$RESEARCH_ROOT/$SLUG"; POOL="${POOL:?set the pool width}"; RUN="${LANE_RUNNER:?set the lane runner}"
for b in "$D"/raw/briefs/*.md; do
  n=$(basename "$b" .md); o="$D/raw/out/$n.md"
  [ -s "$o" ] && { echo "SKIP $n" >> "$D/raw/FLEET_PROGRESS"; continue; }
  while [ "$(jobs -rp | wc -l)" -ge "$POOL" ]; do wait -n; done
  ( "$RUN" "$(cat "$b")" > "$o" 2> "$D/raw/out/$n.err" \
      && grep -q '## Coverage' "$o" && echo "OK   $n" || echo "FAIL $n" ) >> "$D/raw/FLEET_PROGRESS" 2>&1 &
done; wait; touch "$D/raw/FLEET_DONE"
```

Launch it detached (`nohup … &`) and poll `FLEET_PROGRESS`, so a foreground command limit cannot end the fleet. Rate-limit errors mean the pool is too wide. The success test should accept `## 6. Coverage` as well as `## Coverage`; Luna numbers its sections.

`codex-fast --web-search on --oneshot --file "$b" < /dev/null` (Luna, a wider pool) when the brief must carry something private, when the question needs the subscription model's judgment, or when a free lane came back thin. Claude-side fan-out (`Agent` with `quick-research` or `general-purpose` on sonnet) is the small-fleet path for a few lanes when no directory is wanted; it draws on the session's shared WebSearch budget, which a wide fan-out exhausts quickly. No Fable subagents. Nuanced judgment (which of two contradicting sources is right, what the field is converging on) does not fleet on the bulk tier; it runs in the primary or on sol.

Build the pool as the plain loop with a job-count semaphore above, never `xargs -P` with an exported function: that shape silently drops the job id. Kill a fleet by its directory path. The lane brief template is `references/lane-brief.md`.

## Rules

Read-only everywhere except the lane's own output. No logins, no scraping behind walls, no browser automation, and no brief invites an "alternative way to load" a page. Quotes verbatim or not at all; an unknown field says `unknown`; nothing about the reader in any lane output. Versions, prices, model rosters and APIs turn over within months: the lane records each source's date, and the synthesis says which findings rest on a source old enough to have turned.
