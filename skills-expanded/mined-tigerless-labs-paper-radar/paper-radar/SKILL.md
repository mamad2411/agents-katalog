---
name: paper-radar
description: Scrape AI papers published by 28 big tech companies and AI labs in a given date window, with institutional attribution (lead vs. participating vs. intern). Use when the user asks "what did big tech publish recently", "what AI research has <company> put out", "run the paper radar", or wants to inventory recent arXiv output by company or topic. Also for fact-checking questions like "has <company> published anything on <topic>".
---

# paper-radar — big tech AI paper radar

**Stateless: one run = one window = one report. No paper library is maintained.**
arXiv is the only source of truth, and re-running the same window necessarily produces the same
result — so there is no reason to keep a second copy. Keeping one only adds state that drifts
silently and lives outside version control. The cost is re-scraping the whole window every run
(~1 min for 3 days, ~3 min for 14 days); what you buy is reproducibility.

## Read this first, or you will reach wrong conclusions

**arXiv is the only source organized by posting date.** Every vendor's own publications page is
organized by *publication year / venue*, which structurally cannot answer "what shipped in the last
two weeks" — a data-model difference, not a technical one. Measured:

- **Google Research**: detail pages carry a year only, and the listing is **not chronological**;
  85 titles across the first 8 pages yielded **0** inside a two-week window, and the most recent
  entry's arXiv posting date was three months old
- **Amazon Science**: grouped by year, no per-paper date
- **Microsoft**: `/research/feed/` is an editorially curated blog — ~8% coverage of the same window
- **13 Chinese company sites**: 0 date hits across all of them — those are lab landing pages, not
  paper listings

**The other fact you need: arXiv metadata does not carry author affiliation.**
`<arxiv:affiliation>` fill rate is 1%, Semantic Scholar 7%, and OpenAlex returns **0**
`raw_affiliation_strings` for preprints (measured: 3/3 empty, while the same endpoint returns 34/34
for published Nature papers). The industry-standard pipeline is "publisher deposits an affiliation
string → ML maps it to ROR", and arXiv never deposits that string. **So affiliation has to be
extracted from the paper's own author block.**

## Running it

The scripts live in this skill directory and depend on nothing outside it — pure stdlib, no pip
packages.

```bash
R=<skill-dir>/scripts/paper_radar.py

python3 $R                 # last 3 days
python3 $R --days 14       # last 14 days
python3 $R --from 2026-07-20 --to 2026-08-04
python3 $R --cats cs.AI,cs.CL,cs.LG,cs.CV   # widen categories
python3 $R --no-scrape     # official sources + team names only (seconds — quick company check)
python3 $R -o path.md      # write the report here
python3 $R -o -            # write the report to stdout
```

**Timing**: for a two-week window (~3000 papers), metadata takes ~2 min and author-block fetching
~25 s at 6 workers. A 3-day window finishes inside a minute. **To cover a longer history, widen the
window and re-run — there is no library to query.**

## Where the report goes — you decide, the script does not guess

The script **does not know, and should not know**, where the calling project keeps its research.
With no `-o`, it writes to the current working directory.

**Decide the destination before each run:**

- The user named a path → use it
- This is research worth keeping → write it into that project's research directory, with the window
  in the filename
- You are just checking one fact ("has Xiaomi published on self-evolving AI?") → use `-o -` and
  **leave no file**. A throwaway question that leaves a file behind will masquerade as a research
  record later

## Files

| Path (relative to this skill) | Role |
|---|---|
| `scripts/paper_radar.py` | Pipeline: fetch listing → fetch author blocks → resolve affiliation → write report |
| `scripts/affiliation.py` | **Resolution layer**: superscript mapping + three-tier matching |
| `scripts/data/ror_anchors.json` | 28 labs' ROR IDs + **98 official name variants** (including Chinese) |

The only output is one markdown file (path per above), with a "total hits / of which lead" split.
The skill directory itself produces no files.

## Six stages

```
0 listing      arXiv API: cat × submittedDate → dedupe by ID
1 full text    arxiv.org/html/{id} + Range first 90KB, cut ltx_authors → ltx_abstract      [85%]
2 structure    scan right-to-left for the last position starting an ascending 1,2,3… run
               extract (author, marks[]) · (mark, affiliation) · emails · role markers
3 entity       (a) email domain  (b) ROR name variants  (c) lab alias table
4 grading      lead_orgs = the first author's affiliations (may be several); intern = marker present
5 supplements  Apple RSS · MSR embedded JSON · arXiv team names
6 report       dedupe by key (one paper can arrive from both the author block and an official
               source), write markdown, keep evidence + matched_on
```

## Five disciplines, every one of them paid for in bugs

**1. The author block must be cut strictly at `ltx_abstract`.** Take one character more and the
abstract bleeds in. Measured consequences: `Oracle` 73 papers (all "oracle access"), `MiniMax` 17
(the minimax algorithm), `DeepSeek` 58 (papers merely *mentioning* the model). Cut cleanly, the
median author block is ~201 characters.

**2. The affiliation list must be found right-to-left.** "name + superscript digit" in the author
run and "digit + affiliation" in the affiliation run have identical shape, so a left-to-right scan
parses `Yuchen Zhao 1 Bingxuan Li` as `1 → "Bingxuan Li"`.

**3. Never fall back to "only one company matched, so it leads".** That only tells you the other
affiliations aren't companies you track. Measured misattribution: *Filesystem-Based Memory* is
UIUC-led but was scored Adobe-led because Adobe was the sole match.

**4. A company byline is not a company paper.** Only `*` in the report means lead. Measured over a
two-week window: Google hit 10 papers but **led only 4**; Google DeepMind 7 hits, **2 led**; Adobe
5 hits, **0 led**. Any claim of "N big tech papers" must say which column it means.

**5. State the blind spots before the numbers.**

- **12% of submissions are PDF-only and are invisible** — the hard ceiling of stage 1
- **Apple miss rate ~78%** (its authors frequently omit the affiliation) → patched via the official
  RSS feed. **This supplement is required, not optional**
- When the first author lists several affiliations they cannot be ranked; both get `*`
- `intern` is a marker, not a judgment — whether an intern's paper "counts" is a definitional
  question, surfaced for the caller to decide

## Three layers of error — don't conflate them

| Layer | Problem | What to do when it fails |
|---|---|---|
| **1 extraction** | Can't get the text at all | supplementary sources; **every miss today is in this layer** |
| **2 structure** | Can't map author to affiliation | degrade to a whole-block scan, at reduced precision |
| **3 entity** | Which company is this string | `unmatched` keeps the raw text for the table; **ROR only operates here** |

**ROR is a string-to-ID lookup table; you need the string first.** Measured on two Xiaomi papers:
one had no HTML at all, the other's author block held 8 person names and not one word of
affiliation. ROR cannot save either — only supplementary sources can.

## Why each supplementary source stays

| Source | Role | Evidence |
|---|---|---|
| **Apple RSS** | Corrects a systematic miss, **required** | Two-week window: 2 scraped vs. 9 official — 78% missed |
| **arXiv team names** | Covers "company name sits in the author slot, not the affiliation slot" | `Xiaomi MiMo Team` / `Kimi Team`; added 2 papers, zero redundancy |
| **MSR embedded JSON** | Cross-check probe | 25 scraped vs. 7 official — **redundant**, kept as a within-run control: if an official source has a paper the author block missed, stage 1 is broken |

## When a company shows zero — check in this order

1. **Wrong window** — arXiv indexes 1–2 days late and does not announce on weekends; widen first
2. **Wrong categories** — the default is cs.AI/cs.CL/cs.LG; robotics is cs.RO, vision cs.CV,
   systems cs.SE
3. **Team-name search** — `all:"Xiaomi"` / `"Hunyuan"` / `"Kimi Team"` work;
   **`all:"MiniMax"` is unusable** (5800+ hits from the minimax algorithm) — use `au:"MiniMax"`
4. **Official channels** — Apple RSS, Meta's `ai.meta.com/results/?content_types[0]=publication`
   (note `/research/publications/` returns 400 to plain curl), NVIDIA
   `research.nvidia.com/publications`
5. Only when all of the above are empty may you say "this company published nothing in this window"

## Roadmap

- **Add TeX source as stage 1 tier 2** — untar `arxiv.org/e-print/{id}` and read `\author{}`.
  Verified: papers with no HTML often do have TeX, with superscripts intact. Cheapest available
  coverage gain
- **Within-run health self-check** — put stage 1's author-block hit rate, and the count of
  "official source has it but the author block didn't", straight into the report header. Guards
  against a silent break when arXiv changes its markup (the 78% Apple miss was found by accident).
  **Do not reintroduce stored historical hit rates for this** — the within-run cross-check suffices

## One more thing

**Paper count is supply, not heat.** Measured: of 231 big tech papers in a two-week window, **0**
were discussed on Hacker News, while every HN-discussed paper in the same window came from academia
or a startup. Judging heat requires a separate social signal.
