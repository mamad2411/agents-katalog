---
name: stackoverflow-playbook
description: >-
  Runs a developer-tools vendor's public presence on Stack Overflow - product-tag ownership,
  staff answering strategy, affiliation disclosure and self-promotion limits,
  reputation gates, the generative-AI content ban, backlog triage, and canonical self-answered Q&A
  that ranks in search. Use whenever the user mentions their product tag on Stack Overflow, staff
  answering there, unanswered questions in their tag, staff answers flagged as spam, or "is
  Stack Overflow still worth it for our product" - even if they only say "our tag is a mess". Not Stack Internal, ads
  or the Developer Survey. Do NOT use for getting your own docs cited by AI -
  use samber/developer-relations-skills@developer-docs-ai-visibility; for docs error pages use
  samber/developer-relations-skills@developer-troubleshooting-docs.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Stack Overflow playbook

You run a vendor's presence on Stack Overflow: a reference archive that search engines rank and licensed AI assistants retrieve, not a live support queue.

## Rules that get staff accounts flagged

The first four are published in the help center.

- **Disclose in every post** naming your product or employer, including the question half of a self-answered pair. A profile bio does not count.
- **Answer the question, not the product.** Some answers may be about your product, never all. Show the working solution; link-only answers are deleted.
- **No generative AI.** Content "crafted, in part or in whole" by an LLM is banned: deletion with its reputation, warning, suspension on repeat.
- **One person, one account.** No shared or agency accounts. Colleagues never vote on, accept or bounty each other's posts; serial votes are reversed automatically.
- **Hands off others' work.** Never downvote, flag or retag competitors' posts. Never rewrite another author's solution; edits below 2,000 rep that change intent are rejected, and rewrites get rolled back. Post a new answer instead.
- **Never paste one answer on many questions;** flag copies as duplicates. Posts are CC BY-SA 4.0, so reuse others' answers in docs with attribution.

| Rationalization | Why it fails |
| --- | --- |
| "The profile says where they work." | Disclosure belongs in the post. |
| "AI only drafted it; an engineer checked it." | "In part" is covered. Debug with AI privately, write the post yourself. |
| "Ask the team to upvote our canonical." | Coordinated votes are reversed and can suspend every account involved. |

## Interview

One question at a time; skip what the request already answers:

1. Who answers, how many accounts are new, what reputation each?
2. Tag state: questions, unanswered, highest-view threads? If unknown, run the Data Explorer query in the templates.
3. Where do bugs, feature requests and account issues go today?
4. Goal: deflect support, be cited in search and AI answers, or wind down? Anyone planning AI drafting?
5. Hours per week, and the date a result must show by.

## Decide the posture

Monthly new questions sit under 1% of the 2014 peak. The archive still ranks in search, is licensed to Google and OpenAI, and third-party studies find it among domains AI assistants cite for how-to queries. Restate "clear the backlog" as owning the high-view threads.

- **Curate** (default): new questions still arrive monthly; goal is citation or deflection.
- **Maintain**: under about 2 hours a week; canonicals and tag excerpt only.
- **Exit**: almost no new questions; excerpt points to your channels, update top-viewed answers once, stop.

## Engagement surfaces, ranked by value per hour

Efficiency: tag excerpt and wiki > self-answered canonical > new answer on a high-view outdated thread > duplicate flags > new-question rotation == Staging Ground review (one new question each, same cost) > bounty. A citation goal promotes canonicals, a deflection goal the rotation, a deadline under a month keeps the first three.

| Surface | Payoff | Value | Low effort | Rep gate |
| --- | --- | --- | --- | --- |
| Tag excerpt and wiki: routing, links to canonicals | compounding | ++ | +++ | any, peer-reviewed |
| Self-answered canonical per recurring support theme | compounding | +++ | + | 15 |
| New answer on a high-view thread with outdated answers | compounding | +++ | + | 1 |
| Duplicate flags onto a canonical | compounding | ++ | ++ | 15 flag, 3,000 vote |
| New questions answered within 48 h; Staging Ground review | one-shot | + | + | 1; reviewer gate on live page |
| Bounty on a hard, high-view thread | one-shot | + | ++ | 75, from the poster's own rep |

Answering the backlog oldest-first is deleted, not ranked: the most hours on threads nobody reads. Join a Collective only if your technology already has one.

This order starves reputation-building. Only a gold tag badge (1,000 score, 200 answers in the tag) closes duplicates alone; 3,000 rep is one of three votes, and colleagues never supply the others. Promote badge-building when most of the backlog is repeats.

## What the ranking rewards

Published by Stack Overflow:

- More correct new answers on old threads: accepted answers are no longer pinned above higher-scored ones.
- Fewer bulk edits: every edit, answer or bounty bumps the thread to the Active tab. Batch weekly.
- Fewer thin answers: downvoted, closed or deleted posts trigger automatic answer bans.

Practitioner reverse-engineering, unconfirmed: titles quoting the literal error string rank best; high-view threads are what searchers and AI retrievers hit.

## Limits

| Limit | Value | Type |
| --- | --- | --- |
| Flag, upvote, self-answer / comment / create tag | 15 / 50 / 1,500 rep | enforced |
| Edit unreviewed / tag synonym / close vote | 2,000 / 2,500 / 3,000 rep | enforced |
| Links, posting rate, daily flags and votes | limited for new accounts, capped daily | enforced |
| Six spam or abusive flags | post deleted, -100 rep | enforced |
| AI content, undisclosed affiliation | deletion, suspension | enforced on report |
| Share of own-product answers | "some but not all" | policed |

Thresholds move; check the live privileges page. Reputation is per site; disclosure applies everywhere:

- **Stack Overflow**: product answers allowed; "which tool should I use" is off-topic.
- **Software Recommendations**: recommendations on-topic if the answer meets every stated requirement.
- **Portuguese, Russian, Spanish, Japanese Stack Overflow**: separate tags; answer in that language.
- **Meta Stack Overflow**: tag policy and merges after a rename; no promotion.

## Cadence

1. **Week 1, route.** On your support page and tag excerpt: how-to and error questions to Stack Overflow; bugs, requests, "why" and "when" to your own channels.
2. **Weeks 1-2, new accounts.** Answering needs no reputation; start in the product tag. 200 rep on any Stack Exchange site adds 100 on every other.
3. **Week 2, triage the backlog:**
   1. Sort by views; ignore the near-zero-view tail.
   2. Cluster by root cause; one canonical each, flag the rest as duplicates.
   3. Deprecated versions: one migration answer as duplicate target.
   4. Bugs posted as questions: workaround, disclosed link to the public issue.
   5. Account or billing: a 50+ rep steward comments the support route and flags to close.
4. **Daily 15 minutes, rotating:** tag feed (`/feeds/tag/<tag>`) into chat; one assignee per question.
5. **Weekly 1-2 hours, steward:** Unanswered by views, tag wiki edits, the update batch.
6. **Quarterly:** 5-10 canonicals for the top support-ticket themes; search first and answer an existing thread when one exists.

## Measure

Targets are self-set; Stack Overflow publishes no vendor-tag benchmark.

- Answer rate under 30 days (start at 90%); median time to first answer (one business day).
- Canonical coverage of the top 20 ticket themes; views on canonicals; monthly AI-citation spot check.
- Hygiene, pass threshold zero: spam flags, AI deletions, undisclosed-affiliation comments, rejected edits.

## Output

In order: direct answers to the user's questions; posture with its predicate; ranked actions with owner, hours, rep gate; backlog clusters with canonicals, assumed ones marked; routing table; filled templates with technical bodies left for staff; metric baseline or its query. Read [references/templates.md](references/templates.md) for disclosure lines, canonical Q&A, redirect comments, tag excerpt and wiki, and the Data Explorer query.

## References

- samber/developer-relations-skills@developer-troubleshooting-docs - docs error pages each canonical mirrors.
- samber/developer-relations-skills@developer-feedback-loop - where bug reports and requests from the tag go.
- samber/developer-relations-skills@developer-community-health - measuring Stack Overflow beside other channels.
- samber/developer-platform-skills@github-engagement-playbook - when bugs and requests redirect to GitHub.
