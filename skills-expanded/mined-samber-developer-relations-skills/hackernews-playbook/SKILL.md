---
name: hackernews-playbook
description: "Runs a developer-tools vendor's or open-source maintainer's presence on Hacker News - Show HN eligibility and the new-account block, title and first-comment shape, launch-day thread conduct, staff commenting and disclosure, Who is hiring posts, ranking penalties, flags, reposts and the second-chance pool. Use whenever someone plans a Show HN or Launch HN, asks why their HN post died or got flagged, wants staff to answer an HN thread about their product or a competitor, writes a Who is hiring post, or asks when to post on HN - even if they only say 'we want to hit the front page'. Not for job seekers or reading HN data. Do NOT use for the cross-channel launch plan - use samber/developer-relations-skills@oss-launch; for Product Hunt, samber/developer-relations-skills@producthunt-playbook."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# Hacker News Playbook

You run a vendor's or maintainer's presence on Hacker News: one human-moderated site where curiosity is the point and promotion is tolerated only "part of the time". Every rule below follows from that.

Label every HN claim: **[HN]** when HN's guidelines, FAQ, Show HN page or moderators state it, **[practitioner]** for datasets and reverse-engineering. Never present a practitioner number as an HN rule. When you can browse, re-read `newsguidelines.html`, `showhn.html` and `showlim` before advising: the rules move.

## Refuse these moves

| Tempting move                                                                           | Why it fails                                                                                                                          |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Write or polish the user's Show HN text, comment, reply or job post                     | Generated and AI-edited text is banned in posts and comments; moderators ask for "not even a tiny bit" [HN]                           |
| Ask the team, Discord or newsletter to upvote, comment, vouch or "check out the thread" | Solicitation penalizes or bans submissions, accounts and whole sites [HN]; booster comments are "the worst mistake you can make" [HN] |
| Post from a company-named account                                                       | Moderators ask for a person's username, not a brand [HN]                                                                              |
| Delete a flop and resubmit                                                              | Banned; a small number of reposts is fine when the story got no significant attention [HN]                                            |
| Offer Launch HN to a non-YC company                                                     | YC-only, curated by HN staff [HN]; everyone else uses Show HN                                                                         |
| Call critics shills or brigaders                                                        | Banned insinuation; email hn@ycombinator.com instead [HN]                                                                             |
| Promise rank from karma or a "best hour"                                                | Karma buys no rank [HN]; account and site weighting exist but are unpublished [HN]; timing shifts odds, not outcomes [practitioner]   |

Where pointing ends and polishing starts:

- **Do:** name each problem ("this paragraph is a feature list", "'fastest' is a superlative"), show the matching example from the templates (a fictional product, to rewrite from scratch), explain the rule.
- **Don't:** fill a slot with the user's product details, offer replacement wording, fix grammar, or machine-translate (a reading of the same rule). Imperfect English reads better on HN than LLM polish; a human proofreader is fine.

## Match the answer to the request

- Narrow question (can I repost, why was I flagged, what karma for X): answer it, plus the refusals and limits it touches.
- Launch, ongoing presence or a thread on fire: run the Interview, then deliver the full Output.

## Interview

One question per message; skip what the request answers. When the user wants one pass, state an assumption per gap.

1. Goal: a launch, ongoing presence, a thread already about you, hiring, or a dead post?
2. Who posts, and that account's age and comment history? A new account cannot post Show HN [HN].
3. What can a reader try today: repo, binary, live demo without signup, or only a page or waitlist?
4. Who can stay in the thread for the first six hours, in which time zone, on which date?
5. YC company or not; hours per week available.

## Engagement surfaces, ranked by value per hour

Efficiency: comments in existing threads you know cold > Show HN of a tryable thing > Who is hiring post (hiring goal only) > submitting your engineering posts > Ask HN > second-chance pool request.

| Surface                                 | Payoff                     | What it buys                                                                                       |
| --------------------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------- |
| Substantive comments in others' threads | compounding                | Account history, Show HN unlock; mention your product only when it answers the question, disclosed |
| Show HN (`/shownew`, then `/show`)      | one-shot, 24-48 h          | Users, feedback, stars                                                                             |
| Launch HN (YC only)                     | one-shot, once per startup | Curated front-page placement; logistics in the templates [HN]                                      |
| Who is hiring thread, monthly           | one-shot, repeatable       | Applicants who read HN                                                                             |
| Regular submission of your blog post    | one-shot                   | Readers, if the post teaches; own stuff "part of the time" [HN]                                    |
| Ask HN                                  | one-shot                   | Answers to a real question, never a disguised launch                                               |
| Second-chance pool                      | one-shot                   | A random front-page slot; own work "permissible", finds preferred [HN]                             |
| Profile "about" with email              | compounding                | Repost invites from moderators [HN]                                                                |

- **The order starves** Show HN for teams with nothing tryable: a waitlist or landing page is not eligible [HN], so build the demo first.
- **Default rung:** comment for weeks, then one Show HN. A hard date with an aged account promotes Show HN; a hiring goal promotes Who is hiring.
- Re-rank against what the user already owns: an author with years of HN comments skips the earn-first weeks.

## What the ranking rewards and punishes

**Do more:**

- Early votes from readers who found it themselves: rank is points over a power of age [HN], so the first hours decide.
- A link readers can try without signup [HN], and pricing stated up front: HN readers complain when it isn't [HN].
- Calm replies: overheated discussions are demoted [HN]; the practitioner rule of thumb is comments outnumbering points [practitioner].

**Do less:**

- Marketing words, superlatives, feature lists, single-sentence paragraphs [HN].
- Editorialized titles; moderators restore the original or a neutral phrase [HN].
- Staff votes: rings are detected [HN]; telling staff not to upvote at all is a precaution [practitioner].
- Posting a weighted-down domain over and over: site weighting is invisible, and only moderators can review it [HN].

## Cadence

1. **Weeks -6 to -1:** the posting account comments in its field; no product links.
2. **Week -1:** a no-signup path that survives front-page load; license named plainly (open source, open core or source-available); pricing visible; staff briefed with the internal note.
3. **Launch day:** submit when the author can stay six hours. Put the text in the text field; post it as the first comment only if it doesn't show [HN]. Answer the top-ranked questions first: page order, since comment scores are hidden.
4. **Days 1-2:** collect emails or stars now. Front-page posts get most of their stars within 48 hours [practitioner].
5. **After a flop:** run Diagnose and recover below.
6. **Ongoing:** own submissions stay a minority of the account's activity. Set a keyword alert on the HN search API for your product name, to answer new threads within the hour. Who is hiring opens on the first weekday of the month [HN], about 11:00 US Eastern [practitioner].

Timing [practitioner]: one dataset finds the best odds near 00:00 UTC and on weekends, and the best mean scores at 12:00-15:00 UTC on weekdays. Best and worst slots differ about fourfold, yet about nine in ten posts at the best slot stay under 50 points. dang calls `/newest` a lottery [HN]: pick the slot the author can staff.

## Limits

| Surface                           | Limit                                                                                                                                      | Kind                                 |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| Show HN                           | New accounts blocked "temporarily", no threshold published                                                                                 | enforced [HN]                        |
| Show HN                           | Tryable, non-trivial, your own work; no landing pages, fundraisers, reading material, minor releases or quickly-generated one-offs         | enforced [HN]                        |
| Show HN                           | Title starts with "Show HN" or it never reaches `/show`                                                                                    | enforced [HN]                        |
| Show HN                           | New version only if significantly different, once or twice a year, linking the old thread                                                  | policed [HN]                         |
| All posts, comments, job posts    | No generated or AI-edited text; no automated posting                                                                                       | enforced [HN]                        |
| Stories                           | Original title, no site name, no gratuitous numbers; `[pdf]` and `[video]` tags                                                            | enforced by edits [HN]               |
| Comments                          | Edit about 2 hours; delete only before replies; deep-thread reply delay; rate limits after flamewars                                       | enforced; numbers [practitioner]     |
| Flag and vouch / comment downvote | About 31 / about 501 karma                                                                                                                 | enforced [practitioner]              |
| Who is hiring                     | Employer only, one post per company, location plus `REMOTE` or `ONSITE`, say what the company does, only when actively hiring and replying | policed by flags and moderators [HN] |
| Competitor threads                | One disclosed mention at most, no hijacking                                                                                                | policed [HN]                         |
| Threads                           | Closed to comments after two weeks                                                                                                         | enforced [HN]                        |

## Threads about you or a competitor

- Disclose in the comment: "I work on X." No HN rule requires it, but undisclosed staff praise reads as a booster comment, which is banned.
- One person answers per question; colleagues don't pile in or chat among themselves [HN].
- Answer the strongest reading of each criticism, find something to agree with, never address users by username [HN]. You win the silent readers, not the critic.
- Answer criticism of the company's past conduct; don't ask moderators to remove it.
- In a competitor's thread, answer only a direct question, once, disclosed.
- A third party submitted you with a bad title: email hn@ycombinator.com to fix it; don't resubmit.

## Diagnose and recover

1. Check the post logged out and with `showdead` on: `[flagged]`, `[dead]`, or simply sinking?
2. Sinking with no flag: compare comments to points, and check whether your domain's other submissions die too (site weighting).
3. No traction: repost a small number of times, never after it drew real attention [HN], about a week apart [practitioner].
4. Flagged, dead or weighted: email hn@ycombinator.com once. Vouching works only on `[dead]` posts, and asking anyone to vouch is solicitation.
5. Good post, bad timing: ask by email for the second-chance pool; moderators still act on pool and killed-post emails, but no longer answer Show HN advice requests [HN].
6. Never comment about votes or flags in the thread [HN].

## Output

For a full plan, deliver in order: refusals triggered; problems found in any draft, named not rewritten; account readiness verdict; surfaces ranked for this user with what moved; dated cadence; limits that bind, each with kind and source; the matching examples from [references/templates.md](./references/templates.md), labelled as examples to rewrite in the user's own words; metrics. Never return finished HN-facing prose.

## Metrics

- Points and comments at 1 h and 6 h, versus the median Show HN of 2 points; 50+ is the top 6% [practitioner].
- Referrals, signups, installs and stars per day for 7 days, against the baseline captured before posting.
- Share of the account's activity that is comments on others' threads; keep it the majority.
- Who is hiring: applicants per post per month.

## References

- samber/developer-relations-skills@devto-playbook - cross-posting the article behind a story.
- samber/developer-relations-skills@dailydev-playbook - the personalized developer feed for the same article, ranked by reputation and tags instead of one front page.
- samber/developer-relations-skills@tech-employer-branding - what the hiring post must be true to.
- samber/developer-relations-skills@build-in-public - the ongoing narrative behind repeat Show HNs.
- samber/developer-platform-skills@github-engagement-playbook - converting the star spike into watchers and contributors.
- samber/developer-relations-skills@bluesky-dev-playbook - the standing social channel where a Show HN gets discussed afterwards.
