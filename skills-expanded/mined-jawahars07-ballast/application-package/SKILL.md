---
name: application-package
description: Turn one job description into a complete, tracked application package - evaluation report, tailored CV and cover letter, compiled and verified PDFs, and a tracker row. Orchestrates jd-analyser, cv-tailor and human-voice in order. Stops before submission, always.
---

# Application Package

The full pipeline for one role: evaluate honestly, build only if it is worth building, verify
everything, log it, and hand it to the human to send.

**This skill never submits an application.** It prepares. The human sends.

## Prerequisite

Run **`jd-analyser`** first, before loading anything else. It separates stated requirements from
post-hire responsibilities and returns the positioning brief. Build from that brief, not from
your own read of the JD.

Skipping this step is how a role that exists to *train* someone gets mis-built as a role that
requires an expert.

## Files this skill expects

```
facts.md                  the only source of claimable facts
profile.yml               constraints, exclusions, deal-breakers
applications.tsv          the tracker
reports/                  one report per evaluated role
output/cvs/               cv-<slug>.tex and .pdf
output/cover-letters/     cl-<slug>.tex and .pdf
```

Scaffold from `examples/` if these do not exist. Never invent the user's background to fill a gap.

## Workflow

### 1. Quick score, immediately

One line, before any other work:

`**<Company> — <Role>. FIT X/100 (<band>, <confidence> confidence).** <one-sentence reason>`

That line comes straight from `jd-analyser` Step 0. If a gate failed, it says BLOCKED and names the gate.

Then stop and wait. Do not build documents until the user says go. Most roles should not be
built, and finding that out in ten seconds is the point.

### 2. Verify the posting is actually live

Never trust a search result or a cached link. Open the posting. A page showing only a navbar and
a footer means the role is closed — mark it discarded and stop.

Prefer a real browser or a scraping tool over a plain fetch; most job boards render client-side
and a naive fetch returns an empty shell that looks like a dead posting when it is not.

### 3. Write the evaluation report

`reports/{NNN}-{company-slug}-{YYYY-MM-DD}.md`, in blocks:

| Block | Contents |
|---|---|
| **A. Role** | Company, title, location, duration, contract, source URL, date checked |
| **B. Requirements** | The BAR table from `jd-analyser`, with per-item verdicts |
| **C. Evidence map** | Which `facts.md` line backs which requirement |
| **D. Gaps** | Honest, specific, named. **This is the only place gaps are ever written down** |
| **E. Score** | Eligibility (PASS or the failed gate), the FIT scorecard table with every category, credit and point, the confidence level, and the up-to-three honest improvements |
| **F. Positioning** | The four-line brief the documents must be built from |
| **G. Recommendation** | build / don't build / need info first |

**Block D is internal.** Gaps live in the report, for the user's own judgement. They never
appear in the CV or the cover letter. When a JD exposes a real gap, the answer is to find a
genuinely stronger proof point, not to write an apologetic paragraph about the weak one.

### 4. Build the documents

Hand off to **`cv-tailor`**, which loads **`human-voice`** before writing a bullet. Both are
mandatory, every build. Working from memory on voice is a documented failure, not a theoretical one.

### 5. Verify, and state the numbers

Run `cv-tailor`'s ATS pass and `human-voice`'s Part 2 scan. Then report actual results:

> "1 page. All six headings found in order. 0 hidden characters. plain/layout delta 0.
> 0 ligature glyphs. Backed keyword coverage 9/10 (90%),
> 0 unbacked terms present. 0 banned terms. 0 em-dashes."

Never write "should be fine" or "looks good". Either you ran the check and have a number, or you
did not run it and say so.

### 6. Add the tracker row

`applications.tsv` is tab-separated, one row per application:

```
num	date	company	role	source	url	status	score	report
```

**The `num` column is the tracker's own next row — max(num) + 1.** It is *not* the report's
number. Reusing a report number here silently overwrites an unrelated row, which is a real bug
that has happened. Read the file, find the max, add one.

The `score` column holds `FIT/20` to one decimal (FIT 72 → `3.6`), so a tracker built on a
5-point scale keeps sorting correctly. The full FIT lives in the report.

Statuses, and only these: `Evaluated` · `Applied` · `Screening` · `Interview` · `Offer` ·
`Rejected` · `Withdrawn` · `Discarded`.

### 7. Present, do not send

Show the user, in this order:

1. **FIT** — number, band, confidence, and the flag that drove the recommendation
2. **Document scorecard** from `cv-tailor` — every row a number, backed keyword coverage first
3. **Writing improvements** — at most three, quoted line and replacement
4. **Paths** — report, CV PDF, cover-letter PDF
5. **Honest gaps** — from Block D, for their eyes only

Then stop.

## Standing rules

- **Fabrication is the cardinal sin.** A fact not in `facts.md` does not go on a document, ever.
  If a JD names a tool the user genuinely uses but `facts.md` does not list, **update `facts.md`
  first, then the CV.** Never the other way round. That ordering is what prevents drift, and it
  exists because reversing it has caused real bugs twice.
- **Quality over volume.** One properly verified package beats five rushed ones. A day that
  produced five mediocre applications and no verification is a bad day.
- **Never submit autonomously**, even if asked to "just send them all".
- **Convert relative dates to absolute** everywhere. "Last Tuesday" is useless in six months.
