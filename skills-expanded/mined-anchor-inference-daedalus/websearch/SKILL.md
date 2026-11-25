---
name: websearch
description: How to search without looping: score the difficulty, derive a follow-up budget, fix one window and language up front, dedupe across backends, never invent an identifier, and stop. Use before the second search of a turn, or any research task with more than one question.
---
# Searching with a stopping rule

`WebSearch` answers from whichever backend is configured (SearXNG, DuckDuckGo, Serper, Tavily,
Exa, Keenable — it says which one answered, and `WebFetch` reads a result in full). What it cannot
give you is a *method*, and the failure it invites is not a bad result: it is the fourth
rephrasing of a query that already answered the question two rounds ago.

**You are the ranker.** Read the hits yourself and decide what is useful. Do not hand the
search loop to a subagent: a helper returns a list you then have to re-judge, which costs a
context and buys nothing. Hand over *reading* — "fetch these five pages and summarise them
against this question" — not searching.

## Set the query up before the first call

1. **Build the terms out of the operator's words and what earlier results actually said.**
   Padding ("best 2026 comprehensive guide") lowers result quality. Never invent an expansion for
   an acronym you have not seen expanded, and never invent an identifier — a version number, a
   CVE, a model name, a DOI, an issue number. If you do not have it, that is what you search for.
2. **Score the difficulty 1–10, and take the follow-up budget from it.** 1–3 → no follow-up round
   at all; 4–7 → one; 8–10 → two. The budget is a hard cap, not a target: you may spend less.
3. **Resolve one window and one language now**, and inherit them on every call of this loop.
   `time_range="month"` for something that changes weekly, nothing at all for a stable question;
   `language` when the answer is likely written in that language. Never widen the window halfway
   through to make a thin result set look better — report the thin set.
4. **Decide what "enough" looks like** before you start: two independent sources that agree, or
   one primary source (the project's own docs, the release notes, the code).

## Run and rank

1. Run the initial search. Add `domains` when you know where the answer lives
   (`domains="docs.python.org"`); prefer one broad query over three narrow ones you will have to
   reconcile.
2. **Dedupe across backends.** The same page arrives under different URLs: match on the exact URL,
   then on the canonical one (drop `utm_*`, trailing slashes, `#fragment`, `m.` and `amp.`
   prefixes), then on the exact title. A result that appears twice is not confirmation.
3. **If the first round covers the question, stop and answer.** Fast and slightly incomplete beats
   an exploratory sweep. Prefer few strong sources to many weak ones.
4. **Otherwise spend one follow-up round on one concrete gap** — a name, a version, an error
   string, a subtopic that the first round surfaced but did not answer. Calls for the same gap are
   one round. Never spend a round merely rephrasing: if the same terms failed, the terms are not
   the problem, the source is — try `WebFetch` on a primary site, or a different backend.
5. **Read before claiming.** A snippet is a reason to open a page, never evidence on its own. A
   claim that matters in your reply comes from a page you fetched, with the link beside it.

## The hard cap

Plan against **two complete search loops per turn**. If a genuinely different question forces a
third, run it in shallow mode — the initial search only, no follow-ups. Refuse a fourth: answer
from what you have and say plainly what is still unknown. "I could not find X" after six honest
searches is a useful answer; a seventh search is not.

Zero results is information. Report it as "nothing found for these terms in this window" — never
as "this does not exist", and never by silently retrying the identical query.
