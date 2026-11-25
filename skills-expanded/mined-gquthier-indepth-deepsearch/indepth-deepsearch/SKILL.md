---
name: indepth-deepsearch
description: Runs a full, evidence-graded investigation of any market before you build an offer. Coordinates market awareness and payer sizing, competitor mapping, Meta Ad Library capture, ad and podcast transcription, verbatim banks, customer economics, single-competitor teardowns, rules, gap analysis, segmentation, blind-spot audits and a final deck of proof-labelled truths. Use when the user asks for a "deep search", "in-depth deep search", "market research", "étude de marché", "niche analysis", "analyse de niche", "should I sell X to Y", or wants to choose or validate a niche or understand a market before writing an offer. For one stage only, use the matching deepsearch-* skill.
---

# In-depth Deep Search

Turns "should I sell this to them?" into a dossier where every claim shows how proven it is, and where the unknowns are named as clearly as the facts.

Shared files live in `../_shared/`, relative to this skill's folder. Read `../_shared/evidence-protocol.md`, `../_shared/source-access.md` and `../_shared/agent-brief.md` before you brief anyone. If the buyers are not professionals buying a service, read `../_shared/adapting.md` too.

**Paths.** `$IDS` means `<this skill's base directory>/../_shared`. Run commands from the dossier folder, `research/<slug>/`.

## 1. Frame the decision

Do what you can from the request and from existing files first. Ask only for what you cannot determine, in one short message.

| Input | Why it matters |
|---|---|
| **Target** | Who would buy, split into professions or segments if they differ |
| **Product** | What would be sold, and at what price if one exists |
| **Geography and output language** | Default to the user's language and their home market |
| **The decision** | Choose a niche? Go or no-go? Write an offer? This sets what counts as done |
| **Beliefs to test** | "This target is bigger than that one." Write each as a hypothesis, and try to break it |
| **Scope gates** | For example "don't think about the offer yet" |
| **Competitor to dissect** | Optional. Otherwise pick the one who really spends, after stage 2 |
| **Selection criteria** | If choosing between niches, get them in writing before seeing results |

Write this to `research/<slug>/00-brief.md`. If you are inside a git repository, add `research/` to its `.gitignore` before anything else: a dossier names real businesses and people, and one `git add .` would commit them.

## 2. Pick a depth

| Mode | Runs | Use it when |
|---|---|---|
| **Scout** | Stages 1 and 2 per niche, then a short 8 | You are ranking several niches |
| **Standard** | Stages 1, 2, 3, 4, 5, 7, 8, 9 | One niche is on the table |
| **Abyss** | Standard, plus the teardown and ad transcripts | Real money or a public commitment depends on it |

**Scout output.** One `research/<slug>/` per niche, plus `research/00-comparison.md`: a table with one row per criterion from the brief, one column per niche, each cell with its number and proof label. The short stage 8 runs only the "fairness of comparison" and "who is missing" checks, and the proof count covers those two studies.

Default to Standard unless the user asks for "everything" or "as deep as possible". Tell the user which mode you picked and how long it may take. Long tracks have taken hours in real runs, so give each one a time box (default: 90 minutes).

**When comparing niches, run them at the same depth.** See the protocol, rule 17. A shallow dossier always looks better than a deep one.

## 3. Run the stages

| # | Stage | Skill | Main output | Depends on |
|---|---|---|---|---|
| 1 | Awareness and payers | `deepsearch-market-awareness` | `01-market-awareness.md`, funnel | Brief |
| 2 | Competitor map | `deepsearch-competitors` with `deepsearch-ad-intel` | `02-competitors.md`, `actors.csv`, ad analysis | Brief |
| 3 | Voice of customer | `deepsearch-voice-of-customer` with `deepsearch-transcripts` | `03-psychographic.md`, `03-verbatim-bank.md` | Brief |
| 4 | Rules | `deepsearch-rules` | `04-rules.md` | Brief |
| 5 | Customer economics | `deepsearch-customer-economics` | `05-customer-economics.md` | 1, 3 |
| 6 | Teardown | `deepsearch-competitor-teardown` | `06-teardown-<name>/` | 2 |
| 7 | Gap and segments | `deepsearch-gap-and-segments` | `07-gap.md`, `07-segments.md`, field test | 1 to 6 |
| 8 | Blind spots | `deepsearch-blindspots` | `08-blindspots.md` | All |
| 9 | Truth deck | `deepsearch-truth-deck` | `09-truths.md`, deck, `00-overview.md` | All |

**Order of work:**
1. Write `notes/RESOURCES.md`, with one owner for each limited source.
2. Start stages 1, 2, 3 and 4 together, one agent each, in a single message.
3. Then stage 5, and stage 6 as three parallel tracks.
4. Then stage 7, which reads everything.
5. Give stage 8 to a fresh agent that did not write the studies, so its reading is not anchored.
6. Finish with stage 9, and apply the corrections from stage 8 to the earlier files.

Stages 1, 2, 3, 4, 5 and 6 include a brief you can adapt. For the others, point the agent at the stage's `SKILL.md` and the dossier folder, both by absolute path. Always add the facts already known.

## 4. Workspace

```
research/<slug>/
├── 00-brief.md            decision, beliefs, scope gates, criteria
├── 00-overview.md         two pages, conclusion first
├── 01-market-awareness.md
├── 02-competitors.md
├── actors.csv
├── 03-psychographic.md
├── 03-verbatim-bank.md    kept apart: long banks break PDFs
├── 04-rules.md
├── 05-customer-economics.md
├── 06-teardown-<name>/    00-synthesis, 01-cases, 02-client-ads, 03-delivery-guarantee
├── 07-gap.md
├── 07-segments.md
├── 08-blindspots.md
├── 09-truths.md
├── pdf/
└── notes/                 RESOURCES.md, pages/, transcripts/, comments/, ads/, archive/, bank.json
```

## 5. Keep the dossier honest

- **Corrections travel.** When a study corrects an earlier one, the newer file says so at the top, and the older file gets a one-line pointer. Regenerate PDFs and any packaged copy.
- **Check what your conclusion rests on.** Open the source of the three or four numbers that decide the answer yourself.
- **Run the checks before delivering:**
  ```bash
  python3 "$IDS/scripts/bank.py" verify --bank notes/bank.json --corpus notes --ads "notes/ads/ads_*.jsonl"
  for report in 0*.md 06-teardown-*/*.md; do
    python3 "$IDS/scripts/bank.py" check-report "$report" --bank notes/bank.json --corpus notes --ads "notes/ads/ads_*.jsonl"
  done
  ```
  The corpus is `notes/` because it holds every saved page, transcript, comment and archive. Files or folders that do not exist yet are skipped with a note.
- **State what is missing.** If nobody in the target was interviewed, say that on the first page.

## 6. Share it

`python3 "$IDS/scripts/build_pdf.py" report.md report.pdf --title "..." --subtitle "..." --footer "Confidential"` makes a PDF per study. Leave the verbatim bank out of the PDFs. To send everything to a team, put the PDFs, CSVs and bank in one folder with an index and zip it. Regenerate it after any correction.

Competitor dossiers name real businesses and people, so keep them private unless the user decides otherwise.

## 7. Report back

Short and direct, in the user's language:
- the conclusion, with its level of proof
- the proof count: how many claims are measured, estimated, declared, unknown
- what would change the conclusion
- the cheapest next test
- the file paths
