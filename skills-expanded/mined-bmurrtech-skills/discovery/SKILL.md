---
name: discovery
description: >
  Stakeholder discovery that turns meetings, transcripts, and notes into
  evidence-scored use cases ranked P0–P3 (KPFS: impact, pain, feasibility,
  sentiment). Use to prep a meeting's questions, capture a meeting, brief or
  re-score a use case, or rank all use cases. Not for PRDs, ADRs, tickets, or
  intake documents.
disable-model-invocation: true
---

# discovery

Work like a detective: listen for *pain*, demand *evidence*, and name every *gap*
instead of guessing. A use case is ranked only when all four dimensions have
evidence behind them.

## 1. Mode

Use the mode the user named; otherwise infer from the request and bundle state.
Run several modes in a row only when asked (e.g. capture then brief).

| Mode | When | Load |
|---|---|---|
| **prep** | Before or during a meeting: what to listen for and ask | [prep-questions.md](references/prep-questions.md) · [scoring.md](references/scoring.md) |
| **capture** | Notes or transcript from one meeting | [capture-template.md](references/capture-template.md) · [kpi-catalog.md](references/kpi-catalog.md) |
| **brief** | Write or re-score per-use-case briefs; answers to earlier asks | [brief-template.md](references/brief-template.md) · [scoring.md](references/scoring.md) · [kpi-catalog.md](references/kpi-catalog.md) |
| **rank** | Order every brief in the bundle | [ranking-template.md](references/ranking-template.md) · [scoring.md](references/scoring.md) |

Every mode that writes also follows [okf-discovery.md](references/okf-discovery.md).

**Done when:** one mode is stated (ask once if still ambiguous).

## 2. Home

`docs/discovery/<team>/`. A user-named path wins. Otherwise reuse a folder whose
slug matches the team/client/engagement (case-insensitive; `-` `_` space equal)
or that already holds this work. Two plausible folders → ask once. None → create
a 2–4 token kebab slug from the user's words (no dates); if no name is given,
ask once with examples (team, client, company).

**Done when:** the bundle path is stated, plus any reuse choice.

## 3. Run the mode

### prep

Read existing briefs in the bundle. Emit need-to-know + questions per
`prep-questions.md`, open brief gaps first. Optionally seed an empty capture.

**Done when:** every dimension K/P/F/S has at least one tagged line or is marked
already evidenced.

### capture

Write `YYYY-MM-DD-<slug>.md` from the capture template. Fill only evidenced
cells. Open questions start with linked briefs' open asks.

**Done when:** the capture exists, blanks are still blank, and the registry
section is present (empty until brief).

### brief

If the user names a meeting summary and a capture exists, refresh the capture
first. Target the named brief; otherwise write one brief per distinct use case
from the capture, reusing a brief on a title match. Ambiguous target → state the
guessed path once.

1. Band K/P/F/S or leave null; record blockers and the weakest F area (`scoring.md`).
2. Run `scripts/priority_score.py` on the touched briefs and copy its fields.
3. Fill gaps: top missing, plus tagged asks ordered most blocking first.
4. Re-score: change only the dimensions the new evidence touches; history logs
   was→now for dims and priority.
5. Patch the source capture's registry row for every brief touched.

**Done when:** every targeted brief has scorer-sourced priority fields, a gap
table, and a new history row, and the registry rows match the briefs.

### rank

Collect K/P/F/S from every `UseCase` in the bundle, run the scorer once, and
write `YYYY-MM-DD-ranking.md` in scorer order. List stale briefs under Re-brief.

**Done when:** the ranking lists every brief exactly once (ranked or
needs-discovery), and the team index plus `catalog.json` are refreshed.

## 4. Hand-off

End with one next action:

- **Open gaps:** brief path · top missing · numbered `[K|P|F|S]` asks · "answer
  here or rerun `/discovery brief` on this file". Questions only.
- **Ready:** point the top use case(s) at **`create-prd`** or the team's intake.

**Done when:** exactly one next action is stated.

## Boundaries

- Never invent people, emails, measures, approvals, or bands. Unknown stays null.
- Never hand-compute BV, DR, Overall, or priority. If the scorer fails, report the error and stop.
- Do not clear needs-discovery without new evidence; unclear answers get a clarifying question.
- Do not paste transcripts into the bundle. Cite their paths.
- Do not author PRDs, ADRs, tickets, intake, or design docs.
- Do not design solutions (hosting, auth, architecture) during discovery.

## Further reading

- How-to: [docs/how-to-discovery.md](https://github.com/bmurrtech/skills/blob/main/docs/how-to-discovery.md)
- Script vs LLM: [knowledge/skill-scripts.md](https://github.com/bmurrtech/skills/blob/main/knowledge/skill-scripts.md)
