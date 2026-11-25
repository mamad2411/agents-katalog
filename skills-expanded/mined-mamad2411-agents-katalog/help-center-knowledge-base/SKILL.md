---
name: help-center-knowledge-base
description: When the agent needs a help center, knowledge base, support documentation, FAQ architecture, or self-serve support content — docs that deflect tickets because users actually find and follow them.
department: Support
source: helm
---

# Help Center & Knowledge Base

You build help centers like the support-content leads whose deflection numbers are real: articles written from actual tickets (not imagined questions), structured for the panicked scanner, and maintained on the product's release rhythm — because a help center is the support agent that answers instantly at 3 AM, or it's a decoration that teaches users to skip straight to the ticket form.

## Operating principles

1. **Tickets are the syllabus.** The article backlog comes from ticket-theme mining (the top 20 recurring questions by volume = the first 20 articles, in that order), search-log mining (what users searched IN the help center and didn't find — the highest-intent gap list there is), and release notes (every feature ships WITH its article, not three weeks later). Writing articles from the org chart's imagination produces a beautiful library of answers to questions nobody asks.
2. **Write for the scanning, stressed user**: title = the user's own phrasing of the problem, question-form where natural ("Why didn't my invoice send?" beats "Invoice delivery troubleshooting") · the answer's FIRST LINE answers the question (the inverted pyramid — context after, never before) · numbered steps with the exact UI words and one screenshot per confusing fork · one article = one task (the mega-article answering six things ranks for none and helps nobody mid-panic) · reading level: short sentences, zero internal jargon (users don't know your feature codenames).
3. **Structure follows the user's journey, search does the heavy lifting**: 5–8 top categories max (Getting started · Billing · [core job areas] · Troubleshooting · Account) · but design for the truth that 70%+ arrive by SEARCH — so: titles keyworded by user vocabulary, synonyms in the body ("cancel" AND "delete" AND "close account"), and the search-zero-results report reviewed monthly as a content order form.
4. **Every article is instrumented and owned**: was-this-helpful votes + view counts + the ticket-deflection link (tickets that arrive WITH the article already viewed = the article failed; read those tickets to learn why) · owner + last-verified date per article (the SOP discipline applied outward) · stale screenshots are trust acid — the release checklist includes "which articles does this change break?"
5. **The help center feeds the loop both ways**: support agents link articles instead of retyping answers (and where no article exists, the ticket's answer BECOMES the draft — the cheapest content pipeline there is: answer once in the ticket, twice in the KB, never a third time) · recurring article themes feed product ("the top article by traffic is a UX confession — the feature that needs a manual needs a redesign").

## Workflow

1. **Mine the syllabus**: ticket themes ranked by volume × repetitiveness · search gaps · the upcoming release list → the prioritized backlog.
2. **Set the templates**: how-to (goal → steps → expected result → related) · troubleshooting (symptom → likely causes in order of probability → fix each → when to contact us) · concept/FAQ (question → first-line answer → detail) · release-note article.
3. **Write the top 20** per the scanning rules; internal-jargon pass + a cold-user test on the 5 most critical (same discipline as SOPs: watch someone follow it).
4. **Wire the instrumentation**: helpfulness votes, search analytics, the agent article-insertion habit (macro tooling), the ticket-form deflection layout (suggested articles as the user types their subject).
5. **Operate the rhythm**: weekly — new articles from this week's novel tickets · monthly — search-zero report + bottom-10 helpfulness rewrite list · per-release — the breakage sweep + the new feature's article shipping WITH the feature.

## Output contract

Deliver: the mined backlog with volume evidence · category architecture (≤ 8) · the four templates · the top-20 articles drafted per the rules · instrumentation plan (votes, search reports, deflection tracking) · the weekly/monthly/per-release maintenance rhythm with owners.

## Quality bar

- Every article: user-phrased title, first-line answer, one task, owner + verified date.
- The backlog traces to ticket/search evidence — zero articles written from imagination.
- Search-zero results reviewed monthly and shrinking; release day never breaks a screenshot silently.
