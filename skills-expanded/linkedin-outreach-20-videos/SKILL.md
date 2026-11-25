---
name: linkedin-outreach-20-videos
description: Writes and plans LinkedIn outreach (connection requests, DMs and prospecting) using rules weighted by how many of the 20 most-watched videos on the topic repeat each one, and flags where the experts disagree so you can A/B test instead of guessing. Use when the user says "write a LinkedIn DM", "LinkedIn connection request", "LinkedIn prospecting", "cold outreach on LinkedIn", "build a LinkedIn lead list" or "review my LinkedIn message".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /linkedin-outreach

Built from the transcripts of the 20 most-watched videos on LinkedIn outreach in the last 12 months (since 2025-09-14), totaling 301,475 views and 60,351 words. From them, 441 pieces of advice were extracted, and 412 were kept because their verbatim quote was found in the transcript. Those were grouped into 207 distinct themes. The number next to each rule is how many of the 20 videos say it, and sources are in sources.md.

The most repeated rule reached 11 of 20. Treat weights as odds, not laws.

## Inputs
1. Your offer and the specific problem it solves.
2. Your ICP: job titles, industry, geography and company size.
3. Real details on the prospect or list: profile, recent posts, mutual connections, shared groups, recent job changes.
4. Your current volume and channels: connection requests per day and week, and whether you also use email.

Refuse to invent a prospect's posts, mutual connections, groups, job changes or problems. If they are not provided, ask for them or leave a clearly marked placeholder.

## The rules, by weight
### Strong (5 to 11 of 20)
- **Personalize openers; never send generic templated mass messages.** (11/20) Quote a specific line from their recent post, for example "I saw your post on X, especially that bit about AEO versus SEO."
- **Don't pitch or ask for a meeting in first message.** (8/20)
- **Stack filters to narrow lead results.** (6/20) Combine job title, industry and geography. Only 100 pages of 25 leads (2,500) are shown, so refine to about that size.
- **Prioritize prospects showing warm signals like views or engagement.** (6/20) Engagement is the highest level of interest.
- **Cap daily and weekly connection requests to avoid restrictions.** (5/20) Cited limits range from 20 to 30 per day and 100 to 200 per week.
- **Send connection requests without a note.** (5/20) This avoids LinkedIn's personalized-note sending cap. Never put anything salesy in the request. This rule is also A/B tested below.
- **Engage with prospects' posts before reaching out.** (5/20) Comment on a relevant post first, then send a warm DM.
- **Keep outreach messages short, never walls of text.** (5/20) Cited lengths are one to two lines, 150 characters or less, or 3 to 5 sentences.

### Solid (4 of 20)
- **Enrich leads with emails, phones, and other data fields.** (4/20) For example, add a verified work email so you can follow up outside LinkedIn. Never pull data out of LinkedIn itself.
- **Send connection requests selectively, only to ICP prospects.** (4/20) Target co-founders, decision makers or a specific industry.
- **Build commonality via shared connections or groups in openers.** (4/20) For example, "Saw you follow Jill Rally too. Loved her last post on Pipeline Strategy."
- **Build a manually curated, individually imported lead list.** (4/20) One video manually found the first 1,000 people over 1 to 6 months.
- **Combine LinkedIn with email and other channels.** (4/20) Run LinkedIn and email in one sequence.
- **Confirm the prospect has the problem before pitching.** (4/20) For example, "Are your leads coming in predictably or is it a bit hit or miss?"

### Mentioned (3 of 20)
Warm prospects gradually with small yeses · Research prospect's profile, content, and company before messaging · Search mutual contacts' connections for warm referral paths · Avoid duplicate outreach to connected or already-saved leads · Target people who recently changed jobs · Always follow up with a multi-step sequence · Target active LinkedIn users; skip inactive profiles · Use quotes and boolean operators in title searches · Don't sell in InMails; aim only for a reply · Message group members to bypass connection limits

## Where the experts disagree: do not pick, test
| Choice | Side A | Side B |
|---|---|---|
| Note on connection request | Send connection requests without a note (5/20) | Add a personalized note to every connection request (2/20) |
| Voice notes | Use voice notes as first outreach (2/20) | Use voice notes for follow-ups, not first messages (2/20) |
| Timing after acceptance | Wait days after acceptance before messaging (2/20) | Message people right after they accept your connection (2/20) |

## Steps
1. Confirm the four inputs. Ask for any missing prospect details instead of filling them in.
2. Build the list. Stack title, industry and geography filters, and use quotes and boolean operators to exclude wrong titles. Keep only ICP prospects, skip inactive profiles and anyone already connected or saved.
3. Rank the list by warm signals first: profile views, engagement, shared connections or groups, recent job changes.
4. Engage before reaching out. Comment on a relevant post from each top prospect.
5. Send connection requests within the daily and weekly caps the user can confirm. Split the requests between "no note" and "personalized note" as the A/B test.
6. Write the opener. Keep it short, reference a real detail (a line from their post or a shared connection), ask one question that checks whether they have the problem, and do not pitch or ask for a meeting.
7. Plan the follow-up sequence across LinkedIn and email. Choose one open choice from the table (voice note timing or message timing) as the second test, and track replies per variant.
8. Report which rules were applied, each with its weight (for example "Personalize openers, 11/20"), and name which choice is being A/B tested with the two sides.

## Never
- Never claim reply rates, acceptance rates or meetings the user has not measured.
- Never invent posts, mutual connections, groups, job changes or problems for a prospect.
- Never plan connection request volume above the daily and weekly caps cited in the data (20 to 30 per day, 100 to 200 per week).
