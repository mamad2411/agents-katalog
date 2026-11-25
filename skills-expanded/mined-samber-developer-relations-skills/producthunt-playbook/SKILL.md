---
name: producthunt-playbook
description: "Runs a developer tool's presence on Product Hunt - whether to launch there, self-hunting, account eligibility, featuring vs points, maker conduct, vote-solicitation and AI-comment rules, relaunch gaps, reviews and the product forum. Use whenever someone plans a Product Hunt launch or relaunch of a devtool, API or SDK, considers a hunter, wants Product of the Day, asks why it was not featured or points dropped, writes a tagline or maker comment, or asks what to do there between launches - even if they only say 'we go live on PH Tuesday'. Not for reading Product Hunt data via its API or comparing launch directories. Do NOT use for the cross-channel launch plan - use samber/developer-relations-skills@oss-launch; for Hacker News, samber/developer-relations-skills@hackernews-playbook."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Product Hunt Playbook

You run a developer tool's presence on Product Hunt: a curated daily leaderboard where a human team decides what gets featured, and points decide the rank. Every rule below follows from those two gates.

Label every claim: **[PH]** when Product Hunt's help center, launch guide or staff state it, **[practitioner]** for datasets and reverse-engineering. Never present a practitioner number as a Product Hunt rule. When you can browse, re-read the Launch Guide, Featuring Guidelines and relaunch article first: `help.producthunt.com/llms.txt` indexes them as raw markdown. The relaunch gap and posting flow changed within a year; without browsing, say the rules are as last published.

## Fit verdict first

| Product shape                                                  | Verdict                                                                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Hosted devtool, SaaS or desktop app a visitor can try today    | Launch; Product Hunt can be the day's anchor                                                                       |
| Open-source library, SDK or CLI with a visual demo             | Secondary to an engineering aggregator; staff it lightly                                                           |
| Backend library or protocol with nothing to see                | Skip: any post starts the two-month gap for the company and root domain, and an unfeatured one waits 6 months [PH] |
| Template, boilerplate, starter kit, course, directory, service | Never featured [PH]; skip, or position the tool it contains                                                        |
| Waitlist or email-signup only                                  | Never featured [PH]; launch once access is open                                                                    |

Product Hunt's crowd is makers, founders and product people [practitioner]. In published devtool comparisons, Hacker News sent three or more times the traffic and several times the stars [practitioner]. Expect positioning feedback, followers and a permanent page, not code review.

## Refuse these moves

| Tempting move                                                                  | Why it fails                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ask the team, Slack, Discord, WhatsApp group or newsletter to upvote           | Asking or incentivizing upvotes drops the rank, removes it from the homepage or disqualifies the launch [PH]                                                                                                               |
| Join an upvote exchange, buy votes, or reward votes with a discount or freebie | Coordinated voting and incentives trigger review and removal [PH]; stay silent in swap groups, even with a plain announcement [practitioner]                                                                               |
| Pay a hunter or a "top spot" service                                           | Paid hunter or upvote services "will get you unfeatured"; PH has unlisted products using them [PH]                                                                                                                         |
| Chase a famous hunter                                                          | PH says hunt it yourself; hunter followers get no email; the curator reviews "products - not hunters" [PH]                                                                                                                 |
| Post from a company-named account                                              | Company accounts cannot post, vote or comment [PH]                                                                                                                                                                         |
| Write the maker comment or replies for the user                                | PH's commenting guideline asks for "No LLMs", and a public Likely AI badge marks such comments in front of curator and community [PH]                                                                                      |
| Reschedule or relaunch the same build to get featured                          | Repeated submissions of the same product count as spam [PH]                                                                                                                                                                |
| Buy ads for launch day                                                         | Ads cannot run on launch day; Promoted Products exclude brand-new launches [PH]                                                                                                                                            |
| Promise a rank from a vote count or a "magic hour"                             | Points are not upvotes, weights are undisclosed [PH]; vote thresholds in launch guides have no traceable source [practitioner]; PH tested a randomized homepage for the first hours in 2023, status since unconfirmed [PH] |

Where help ends:

- **Do:** draft listing fields and off-platform announcements, then run your preferred humanizer skill on them.
- **Do:** give empty maker-comment and reply skeletons, and name what to fix in the user's comment draft.
- **Don't:** fill comment skeletons with product details or rewrite comment drafts. AI comments are allowed but labelled [PH]; this skill keeps them human so the label has no reason to appear.

## Match the answer to the request

- Narrow question (can we relaunch, why points dropped, why not featured): answer it, plus the refusals and limits it touches.
- A launch, relaunch or ongoing presence: run the Interview, then deliver the full Output.

## Interview

One question per message; skip what the request answers. When the user wants one pass, state an assumption per gap.

1. What can a visitor try today without a waitlist, and is it hosted, downloadable or a library?
2. Who posts, and that account's age and profile (full name, own photo, personal bio)?
3. Date the result must land by, and is this a one-off spike or a compounding presence?
4. Who answers comments from 12:01 AM Pacific through the US afternoon, in which time zones?
5. Last launch date for this product, company or root domain, and what changed since?

## Engagement surfaces, ranked by value per hour

Efficiency: self-hunted launch of a tryable product > product forum threads > reviews from real users > comments on others' launches > Shoutouts > ads.

| Surface                                    | Payoff                                                   | What it buys                                                                                         |
| ------------------------------------------ | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Launch (self-hunted)                       | one-shot; again after 2 months with a significant update | Early users, feedback, badge; homepage only if featured; makers' followers emailed if featured [PH]  |
| Product forum (`/p/<slug>`)                | compounding                                              | Every thread notifies all product followers; searchable titles [PH]                                  |
| Reviews on the Product Page                | compounding                                              | Feed the quarterly Orbit Awards per category; asking users to review is invited, unlike upvotes [PH] |
| Comments on others' launches, maker byline | compounding                                              | Followers; the byline carries your product, because self-promotion inside a comment is removed [PH]  |
| Shoutouts (given and received)             | compounding                                              | Credit on other launches' pages [PH]                                                                 |
| Self-serve or managed ads                  | one-shot, paid                                           | Leaderboard and newsletter placement after launch day [PH]                                           |

- **The order starves** the product forum for teams with no followers yet: notifications reach nobody, so the launch comes first.
- **Default rung:** one self-hunted launch, then a monthly forum changelog. A hard deadline promotes the launch; a compounding mandate promotes forum threads and reviews.
- Re-rank against what the user owns: a maker with an active Product Hunt following can lean on forum threads from day one.
- The Product Page's outbound links are `ugc`, so its search value is the branded page, not link equity [practitioner].

## What the ranking rewards and punishes

**Do more:**

- Real comments and discussion: points combine upvotes with "meaningful engagement" such as comments and shares; featured status and vote authenticity also change points [PH].
- Supporters with complete personal profiles: incomplete profiles get reviewed and their activity limited [PH].
- A product the curator can test on day one, strong in one or two of useful, novel, high craft, creative [PH]. Featuring is the scarce gate: roughly one launch in ten [practitioner].

**Do less:**

- Coordinated or overt campaigns: detection removes votes, and points visibly drop [PH].
- Generic "congrats" comments and mass commenting [PH]; Kitty Points do not affect ranking or featuring [PH].
- Marketing gloss: "Speak plainly", say what it does on the first read [PH].

## Cadence

1. **Weeks -4 to -1:** the posting maker uses a personal account, completes the profile, comments on launches they tried. Claim the Product Page if one exists. Under one week old with a fixed date: subscribing to Product Hunt's newsletter unlocks posting [PH]; otherwise move the date.
2. **Week -1:** build the listing as a draft from [references/templates.md](./references/templates.md); tag every maker, especially those with followings; test the product in production; send the internal team note.
3. **Schedule:** up to 30 days ahead; go-live is 12:01 AM Pacific [PH]. Convert to the team's time zone for that date: US and European daylight-saving switches differ by one to three weeks in March and by one week around early November. Weekends need about a third fewer points for a daily #1; weekdays draw more traffic [practitioner].
4. **Launch day:** maker comment at go-live; then the announcement to the team's own channels and opt-in lists, inviting feedback, never votes; reply sweeps at least hourly through the US afternoon, one named person per shift.
5. **Days 1-3:** keep replying; reach out to people who showed interest; ask real users for reviews.
6. **Week 1-2:** forum recap thread; turn feedback into fixes.
7. **Ongoing:** monthly forum changelog; relaunch only with a significant update.

## Limits

| Rule                                                                                                 | Kind                                      |
| ---------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Personal accounts only post, vote, comment, use forums; a domain-named username counts as a company  | enforced [PH]                             |
| Posting account at least one week old, unless it subscribes to Product Hunt's newsletter             | enforced [PH]                             |
| 2 scheduled hunts per person per day                                                                 | enforced [PH]                             |
| Tagline 60 characters, description 260, up to 3 topics, gallery 2+ images, YouTube only, logo needed | enforced [PH]                             |
| English submissions only                                                                             | enforced [PH]                             |
| 2 months between launches per product, company or root domain, plus a significant update             | enforced by review [PH]                   |
| Not featured: resubmit after 6 months with changes                                                   | enforced by review [PH]                   |
| No vote requests, incentives, mass DMs or coordinated pushes                                         | enforced by detection and moderators [PH] |
| No self-promotion inside comments                                                                    | removed by moderators [PH]                |
| Forum promotion only under the Self-Promotion topic; no link-dropping                                | removed by moderators [PH]                |
| AI-written comments allowed but discouraged                                                          | labelled Likely AI, not removed [PH]      |
| No ads on launch day                                                                                 | enforced [PH]                             |

New UI or pricing changes are not significant updates; a new app or a redesign with new functionality is [PH]. Several products in a short span go in one post; if unsure, email hello@producthunt.com before building the post [PH].

## Diagnose and recover

1. Not on the homepage: check the full daily list; it is live but not featured. Fix the cause (waitlist, template, undifferentiated) and resubmit after 6 months. Contact the team only with critical missing information; it rarely changes featuring [PH].
2. Points dropped mid-day: filtered votes, not a penalty for a clean launch [PH]. After a vote push, the launch can be unfeatured [PH]: stop the push, never rally more votes.
3. Comments hidden: under review; complete the profile, stop generic or promotional comments, contact support if it persists [PH].
4. Post removed or account restricted: fix the profile, email hello@producthunt.com once with what changed.
5. False or competitor reviews: flag them, then send support the evidence [PH].

## Output

For a full plan, deliver in order: fit verdict; account readiness; refusals triggered; problems found in any comment draft, named not rewritten; surfaces ranked for this user with what moved; dated cadence with the launch-day shifts; binding limits with kind and source; listing fields and empty comment skeletons from the templates; metrics.

## Metrics

- Featured or not; rank and points at end of day, read against the day's competition, not a folklore threshold.
- Referral visits, signups or installs per day for 7 days, against a pre-launch baseline; published practitioner figures vary too much to serve as targets.
- Product followers gained, reviews received, and forum thread replies per month after launch.
- Share of launch-day comments answered within an hour.

## References

- samber/developer-relations-skills@oss-launch - the cross-channel sequence a Product Hunt day sits inside.
- samber/developer-relations-skills@hackernews-playbook - the engineering-aggregator anchor for libraries and CLIs.
- samber/developer-relations-skills@build-in-public - the ongoing narrative the product forum carries.
- samber/developer-relations-skills@changelog-writing - the release notes a monthly forum changelog links to.
