---
name: gemini-web-research
description: Delegate substantial web research to Gemini CLI or agy only when explicitly requested. Not for ordinary research or quick searches.
---

# Gemini Web Research

You are the research lead. Gemini workers do the searching and reading; you break the request into questions, read their checked reports, and write the answer. Do not search the web or fetch pages yourself, and do not fill gaps from your own memory. Invoke this skill only when the user asks to use Gemini or `agy` for research.

## How a round runs

```bash
python3 <this skill's directory>/scripts/gemini_research.py '<question 1>' '<question 2>' '<question 3>'
```

One call is one round. Each question becomes an independent Gemini 4 Hydrogen job at high effort, all running in parallel. A round takes 3 to 6 minutes. Run it as a background command when your harness supports that; otherwise run it in the foreground with a timeout of at least 10 minutes.

Each worker must search the web, read the pages it cites, and back every claim with a verbatim quote. The script then checks every job against its trace and prints one report per question:

- **FAILED job**: the worker ran no search or read no pages, so its answer came from memory. Nothing from it is usable.
- **[OK] claim**: the quote was found in a page the worker read. Usable as a fact.
- **[FLAG] claim**: the URL was never read or the quote is not on the page. Not a fact.
- **Unconfirmed**: things the worker could not find on any page it read.

## Pick the tier

Before launching, write one line naming the tier and why. If you are torn between two tiers, pick the higher one. Use exactly these counts:

| Tier | When | Rounds × jobs |
|---|---|---|
| **Easy** | One fact or a few facts with an obvious authoritative source: a version, date, price, link, or "what is X". | 1 round × 2 jobs |
| **Medium** | How something works, a comparison of a few options, or a summary across several sources. | 1 round × 3 jobs |
| **Hard** | Contested, poorly documented, fast-moving or deeply technical; several linked unknowns; or the answer drives a costly decision. | 2 rounds × 3 jobs |

What the jobs cover:

- **Easy**: job 1 asks the question directly. Job 2 asks for the same facts from a different angle, for example from the changelog or package registry instead of the docs, so the two answers check each other.
- **Medium**: three different sub-questions that together answer the request.
- **Hard, round 1**: three different sub-questions, like Medium.
- **Hard, round 2**: written after you read round 1. One job on the most important gap or unconfirmed item. One job on a contradiction between jobs, or on a flagged claim the answer needs. One job that confirms the claim your conclusion rests on from a different source.

## Write each question

- **Self-contained.** The worker has none of your context. Name the thing fully and add what disambiguates it: a URL, the vendor, the version, the date range.
- **One target per job.** No two jobs in a round cover the same ground.
- **Ask for the specific facts you need**, not "everything about X". Never paste the user's whole request in as a question.

## Read the results

- State as fact only [OK] claims. A [FLAG] claim is a lead, not a fact.
- Rerun a FAILED job once with the same question. If it fails again, report it as failed.
- In an Easy round, compare the two jobs. If they disagree, the disagreement is a gap.
- After an Easy or Medium round, if the answer still depends on a gap, a flagged claim or an unconfirmed item, run one more round of exactly one job aimed at it. After a Hard round 2, report remaining gaps as unconfirmed.

## Answer

Give a synthesis, not the raw reports. Link each fact to the URL its [OK] claim came from. Say plainly what stayed unconfirmed.
