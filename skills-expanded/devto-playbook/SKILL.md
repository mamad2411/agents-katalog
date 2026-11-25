---
name: devto-playbook
description: "Runs a devtool vendor's, DevRel team's or open-source maintainer's presence on DEV Community (dev.to) - organization account, cross-posting with canonical_url and RSS import, tag rules and tag moderators, AI-disclosure tiers, promotion and backlink limits, feed ranking, Top 7 and Billboards. Use whenever the user mentions dev.to or DEV Community, cross-posting a blog there, a removed tag, a flagged or low-reach dev.to post, or a dev.to launch - even if they only say 'our dev.to posts get three reactions'. Not for administering a Forem instance. Do NOT use for drafting the article - use samber/developer-relations-skills@engineering-blog-post; for Hacker News, samber/developer-relations-skills@hackernews-playbook; for Substack, samber/developer-relations-skills@substack-playbook."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.3"
---

# dev.to Playbook

You run a vendor's or maintainer's presence on DEV Community: a peer-learning site where readers, trusted members and tag moderators punish marketing faster than the feed rewards it.

Label every ranking claim: **[platform]** DEV pages and staff posts; **[code default]** open-source Forem code, which DEV can override; **[practitioner]** community data and judgement.

## Rules that get vendor posts removed or buried

- **Full post on DEV.** Terms ban posts that "merely reference an external link that contains the full post", and content "designed primarily for the purposes of promotion or creating backlinks".
- **Backlinks.** A post whose main purpose is backlinks risks suspension; the AI guidelines exempt company-blog links only when the post sits under the company's DEV organization.
- **AI tier on every post:** Hand Written, AI-Assisted, Fully Autonomous. Low-effort undisclosed AI, or synthetic output passed off as firsthand experience, risks suspension. The AI guidelines also bar AI-assisted posts that promote a business "including your own" or exist mainly for personal brand. When a post names your product, keep it human-written until the live guidelines say otherwise.
- **No AI-written comments.** Translation, grammar and assistive tools are the exception.
- **No engagement manipulation** [platform, llms.txt]. Reaction weight ramps from zero to full over an account's first 10 days [code default]. A group of heavy reactors (50+ reactions a quarter) sending 80% of them to the same few authors gets its reputation halved [code default].
- **RSS import:** tick "Mark the RSS source as canonical URL"; it is opt-in. Imports land as drafts, the first four blog categories become tags, and each draft keeps the original post's date. Delete the `date:` line before publishing an old post, or it publishes back-dated, outside the signed-in feed, permanently [code default].
- **Tags follow their sidebar rules, not their size.** A tag moderator can remove a tag; the author cannot re-add it.
- **Disclose affiliate links** in the post.

| Rationalization                                      | Why it fails                                                                                    |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| "The canonical points home, so a teaser is fine."    | Canonical covers duplication, not the substantial-content rule.                                 |
| "Our org byline makes the product pitch legitimate." | The org exempts a backlink, not promotion; AI-assisted promotion stays barred.                  |
| "AI drafted it, a human approved it."                | Approval alone keeps it Fully Autonomous; only a meaningful human rewrite makes it AI-Assisted. |

## Interview

One question at a time; skip what the request already answers.

1. Who posts: a named engineer, a maintainer, a company account? Any DEV organization yet?
2. Goal: adoption from a launch, a standing tutorial channel, hiring, or a sponsored campaign? By what date?
3. Where the original lives: own blog with RSS, docs site, or DEV only? How old is the backlog?
4. Hours per week, and who can answer comments within a day?

Answers 2 and 4 re-rank the surfaces below; say which answer moved which row.

## Fit verdict

- **Invest:** a product one developer can try alone, tutorials or build logs to share, someone answering comments daily.
- **Syndicate only:** enterprise-buyer audience or docs-site content; canonical-ticked import, new posts only, comments answered weekly, giving up most of the four-day ranking window.
- **Skip:** nobody can answer comments; unanswered posts and teasers cost reputation and earn nothing.

## Engagement surfaces, ranked by value per hour

Efficiency: comments on others' posts in your tags == organization setup with its sidebar call-to-action > full tutorial or build log under the organization > #discuss thread > series > #showdev or #news launch post > DEV Challenge entry > promoted Billboard, DEV Ads, Takeover or sponsored challenge. The tie holds because both take an hour and keep paying: one earns standing, the other is the link DEV places on every org post for you.

Compliance cost: AI-drafted product posts > teaser or link-heavy posts > labelled paid placements == organization call-to-action.

| Surface                                                            | Payoff      | Value | Low effort |
| ------------------------------------------------------------------ | ----------- | ----- | ---------- |
| Substantive comments in your tags (earn-first)                     | compounding | ++    | +++        |
| Organization: members, branding, sidebar CTA with clicks           | compounding | ++    | +++        |
| Full tutorial or build log, organization byline                    | compounding | +++   | +          |
| #discuss question your users argue about                           | one-shot    | ++    | ++         |
| Series (front matter `series:`)                                    | compounding | ++    | +          |
| #showdev launch, #news release with a summary                      | one-shot    | ++    | +          |
| DEV Challenge entry with the challenge tag                         | one-shot    | +     | ++         |
| Promoted Billboard (Pro Tools), Ads, Takeover, sponsored challenge | paid        | +     | --         |

- **Re-rank:** a launch date promotes #showdev, #news and #discuss; a compounding mandate promotes series and tutorials; under 2 hours a week, keep comments and new-post syndication only.
- **The order starves** sponsored challenges: highest reach, highest cost. Promote one when the product has a free tier a weekend builder can use.
- Listings are gone; Billboards replaced them, free beside your own organization's posts, paid when promoted [platform].

## What the ranking rewards

**Do more:**

- Publish when you can answer comments for two days. Default hotness gives recency bonuses for 96 hours, then cuts reaction points to half after 4 days and an eighth after 7 [code default].
- Heart good comments on your own post: an author's reaction to a comment there counts five times [code default].
- Topical consistency: the signed-in feed matches each reader's interest embedding and followed tags [platform, staff post].
- A cover image: the featured slot requires one [code default]; the #top7 page says weekly picks rest on editorial feedback, traffic and engagement [platform].
- All four tag slots, each chosen by its rules [platform].

**Do less:**

- Asking for unicorns: all public reactions score the same [code default].
- Links from a new or low-badge account: the spam labeler weighs account age, badges and history [platform, staff post; code default].
- Links to a domain other posts got downvoted for: domain reputation is shared, so one teammate's spam poisons the domain for everyone [code default].
- The same title a third time in a day: automatic spam label [code default].
- Undisclosed or heavy AI: readers can down-rank AI tiers in their feed [platform].

## Tags

- **#showdev:** your project or company launch; "not overly corporate or salesy".
- **#news:** a launched or updated product, library or service, with a brief summary and the source.
- **#contributorswanted:** contributor requests.
- **#opensource:** running projects, licensing, advocacy; project promotion, announcements and contributor requests banned.
- **#beginners:** beginners to programming or to a language, not "new to our tool"; a 1-2 sentence plug at the end allowed.
- **#discuss:** a question, prompt or topic that starts a discussion.
- **Language and framework tags:** focused content; add the framework tag.

For limits, rate caps and source labels, read [references/templates-and-limits.md](./references/templates-and-limits.md).

## Flagged, removed or buried

1. Stop re-posting; a repeat makes it worse.
2. Check for a removed tag or moderator comment, and fix the post against the tag rule.
3. Appeal once, at dev.to/appeal (signed in) or support@dev.to, with the fix described; a human reviews it.

## Cadence

1. **Weeks 1-2, earn first.** Each poster comments substantively on 3-5 posts a week in the target tags [practitioner]. Create the organization from a personal account; members join with their own accounts. No links.
2. **Week 3, wire syndication.** RSS import into the organization per the rules above; publish the best drafts one at a time. The rest stay on the blog.
3. **Weeks 3-8, publish.** One full post every one or two weeks; answer every comment within 24 hours.
4. **Launch week, week 5 at the earliest.** A date before that shortens earn-first, never skips it. One story-led #showdev post plus a #discuss question; teammates comment with substance, never react on cue.
5. **Monthly.** Read the organization dashboard; drop tags that drew nothing.

## Measure

Targets are self-set; DEV publishes no vendor benchmark.

- Organization and author followers, monthly; CTA clicks and referral sessions to the canonical page.
- Reactions and comments per post at day 4, not day 30.
- Hygiene, pass threshold zero: removed tags, spam labels, moderator comments, AI-disclosure notes.

## Output

In order: fit verdict; setup (organization, members, CTA, RSS); ranked surfaces with what moved; per-post tags with each rule; eight-week cadence with owners and hours; filled templates from [references/templates-and-limits.md](./references/templates-and-limits.md); metrics. Run drafts through your preferred humanizer skill.

## References

- samber/developer-relations-skills@engineering-blog-post - writing the post this skill publishes.
- samber/developer-relations-skills@oss-launch - the launch window a #showdev post belongs to.
- samber/developer-relations-skills@hackernews-playbook - the other launch-day channel.
- samber/developer-relations-skills@dailydev-playbook - daily.dev, which indexes DEV and picks up posts that gain traction there.
- samber/developer-relations-skills@substack-playbook - a newsletter-first alternative.
- samber/developer-relations-skills@medium-playbook - the other cross-posting channel.
- samber/developer-relations-skills@devrel-content-calendar - fitting dev.to slots into the quarter.
- samber/developer-relations-skills@devrel-analytics - attributing referral signups.
- samber/developer-relations-skills@bluesky-dev-playbook - sharing the article on Bluesky through starter packs and dev feeds.
