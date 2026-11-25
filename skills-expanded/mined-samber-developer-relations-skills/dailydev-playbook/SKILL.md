---
name: dailydev-playbook
description: "Runs a devtool vendor's or maintainer's presence on daily.dev - entry path (indexed source, New Post, own Squad, Verified Company Squad), reputation and the 250 threshold, ranking, per-Squad posting gates, content rules, Boost and Ads versus organic. Use whenever the user mentions daily.dev, a daily.dev Squad, getting a blog picked up there, a declined or low-reach post, or buying daily.dev ads - even if they only say 'our posts there get no views'. Not for feed reading, its API or Career Mode. Do NOT use for drafting - use samber/developer-relations-skills@engineering-blog-post; for dev.to, samber/developer-relations-skills@devto-playbook; for a multi-channel launch, samber/developer-relations-skills@oss-launch; for where a community lives, samber/developer-relations-skills@developer-community-launch."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# daily.dev Playbook

You run a vendor's or maintainer's presence on daily.dev: a personalized developer feed where reach follows the poster's reputation, the reader's followed tags and early reads and upvotes, and where Squad moderators and an automated screen remove pitches.

Label every ranking claim: **[platform]** daily.dev docs and business pages; **[practitioner]** community observation; **[self-set]** a default this skill proposes, with no platform number behind it. daily.dev publishes no ranking formula, weights, decay curve or best posting time; never present one as fact.

## Rules that get vendor content removed or demoted

All enforced by daily.dev [platform]; penalties run demotion, removal, reputation loss (which also cuts future reach), submission restrictions, account or Squad suspension.

- **Company and personal blogs cannot be sources.** Company sources ended in 2024. A company blog reaches the feed only through Squad posts, New Post, a paid Verified Company Squad's RSS auto-post, or an indexed publication that runs the piece unpaid: articles a publication was paid to run are ineligible, labelled or not.
- **Self-promotion as the main purpose** is rejected, and so is content made to rank, earn backlinks or get cited by AI tools (SEO, AEO, GEO). Links inside posts are nofollow. Paid AI-visibility routes: Agent Ads, a Verified Company Squad page open to AI crawlers, and Sponsored Content.
- **AI-generated content**, or text with its characteristics, is rejected; automated screening looks for it.
- **Paid engagement outside official programs**: no paying people, agencies or influencers to post, comment or upvote; no paying Squad admins to publish or pin; no bought upvotes, Awards or followers. Paid reach goes through Boost, ads or Sponsored Content, all labelled.
- **Affiliate and referral links** are banned. Undisclosed ads posing as tutorials or reviews are banned; state the author's affiliation.
- **Reputation farming and multiple accounts** lead to point loss or a ban.
- English only; no shortened or redirected URLs; clickbait titles get demoted, and Plus readers see them rewritten.

| Rationalization                                                 | Why it fails                                                                                                                                                                                                                                                 |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "Our blog has RSS, so suggest it as a source."                  | Company and personal blogs are excluded however good the RSS is; the request burns a review of up to 30 days.                                                                                                                                                |
| "Twelve engineers upvoting in the first hour is just our team." | Coordinated voting reads as manipulation; votes from accounts under 250 reputation also add nothing to the author.                                                                                                                                           |
| "Post it to every big Squad for reach."                         | The composer caps one post at 3 Squads, and each Squad's moderators judge it against their own rules.                                                                                                                                                        |
| "The agency will post and upvote it for us."                    | The guidelines ban posts, comments and votes an agency or influencer places for a client. On a daily.dev Ads plan, daily.dev gives your agency admin and moderator seats on your Verified Company Squad; outside a plan, post from your own named employees. |

## Interview

One question at a time; skip what the request already answers.

1. Who posts: named engineers, a maintainer, a brand account? Current reputation of each?
2. Goal and date: a launch, a standing content channel, or Squad membership?
3. What exists: technical posts (where, with RSS?), a community elsewhere, a daily.dev Squad already?
4. Hours per week, and who answers comments within a day?
5. Paid budget available this quarter, or organic only?

Answers 2, 4 and 5 re-rank the surfaces below; say which answer moved which row.

## Fit verdict

- **Invest:** developers read your stack's tags, you publish technical posts at least monthly, someone answers comments daily.
- **Syndicate only:** an enterprise-buyer audience or thin backlog; claim authorship of posts already indexed, one curated Squad post a week, no paid spend.
- **Launch-first:** a launch date inside four weeks and no reputation yet; see the launch rule under Cadence, organic work in parallel.
- **Skip organic:** no technical content and nobody to answer. daily.dev tells such teams an Ads plan is not a fit and to start with one Sponsored Content post; pick that or build content first.

## Entry path decision

1. Do you run a multi-author developer publication, not a company or personal blog? Suggest it as a source (needs 250 reputation, public RSS, manual review up to 30 days, only new posts pulled).
2. Is the post already on an indexed publication or on DEV? It may be picked up; daily.dev is temporarily prioritizing niche sources, so content from mainstream ones such as DEV may rank lower [platform]. Claim authorship: add `<meta name="twitter:creator" content="@handle">` to the post's head, add the same X handle under Account details on daily.dev, and email support for posts picked up before the claim. You get the listing notice, an author badge and analytics. Being picked guarantees a feed slot, not traffic.
3. Otherwise publish through **New Post** to your profile ("Everyone") plus at most 3 Squads in total, your own Squad included. Docs disagree on whether New Post needs 250 reputation; check the composer. If it blocks, post inside your own Squad, where admins and moderators are never gated.
4. A company that wants its RSS and YouTube auto-posted, a verified seal and day-one discoverability buys a **Verified Company Squad** (sales-assisted, part of every daily.dev Ads plan).

## Engagement surfaces, ranked by value per hour

Efficiency: substantive comments on posts in your tags == author claiming > own public Squad, seeded (only with an audience to invite; otherwise after New Post) > full post via New Post to profile plus relevant Squads > curating others' posts into your Squad with commentary > Squad poll > cross-posting to DEV for indirect pickup > Post or Squad Boost > Verified Company Squad or daily.dev Ads plan > Sponsored Content. The tie is on ratio, not size: comments buy more value for a few hours a week, claiming buys less for minutes, and both keep paying: comment upvotes (+50 each, counted only from voters with 250+ reputation) build the reputation that lifts every later post, and claiming turns posts already indexed into attributed reach.

Compliance cost: bought or coordinated engagement > AI-drafted product posts > pitch-only posts > labelled Boost and ads == comments and claiming.

| Surface                                              | Payoff      | Value | Low effort |
| ---------------------------------------------------- | ----------- | ----- | ---------- |
| Substantive comments in your tags (earn-first)       | compounding | ++    | +++        |
| Author claiming via `twitter:creator`                | compounding | +     | +++        |
| Own public Squad, DevTools or topic category, seeded | compounding | +++   | +          |
| Full technical post, New Post, profile + ≤3 Squads   | one-shot    | ++    | +          |
| Curating others' posts into your Squad, with comment | compounding | +     | ++         |
| Squad poll your users argue about                    | one-shot    | +     | ++         |
| Cross-post to DEV for indirect pickup                | compounding | +     | ++         |
| Post Boost or Squad Boost (self-serve, Cores)        | paid        | +     | +          |
| Verified Company Squad or managed daily.dev Ads plan | paid        | ++    | --         |
| Sponsored Content (one post, guaranteed read floor)  | paid        | +     | -          |

- **Re-rank:** a launch date promotes New Post and a short Boost; a compounding mandate promotes the Squad and curation; under 2 hours a week keep comments, claiming and one curated post.
- **Own Squad value needs an audience to invite.** With none, a regular Squad stays a members-only surface for weeks; rank it below New Post.
- **The order starves** the Verified Company Squad: highest value, sales cycle plus a quarterly commitment. Promote it when you already publish weekly, want auto-posting, and plan to stay for quarters, not weeks.
- Ads plans and Verified Company Squads commit you a quarter at a time, then renew quarterly; a single campaign outside a plan (newsletter-only, in-feed-only) is shaped on request [platform].
- Happening Now is editor-curated; no surface on this list earns a slot there.

## What the ranking rewards

**Do more:**

- Reputation first. High-reputation authors' posts and comments get ranking priority [platform]. Reach 250 through comments before the first product post [self-set].
- Early unique reads and upvotes: the Popular feed weighs reads, upvotes and freshness [platform]; the window length is unpublished.
- Tags that match what your readers follow: personalized feeds match tags, so tags are your targeting [platform].
- Comment threads: Best discussions ranks on commenters' reputation, comment freshness and comment upvotes [platform]. Answer within a day.
- A plain, specific title: clickbait is demoted and rewritten for Plus readers [platform].

**Do less:**

- Teaser posts and pitches: downvote counts are private, but each downvote lowers the post's ranking [platform].
- Teammates upvoting each other's comments: it reads as reputation farming [self-set], and farming costs points or the account [platform].
- Repeat links of the same post across Squads or days: post each link once per Squad [self-set].
- Team upvotes on cue: votes from accounts under 250 reputation move nothing, and coordination reads as manipulation [platform].

## Accounts, Squads and tags

- **Accounts:** post from named people's personal accounts, one account each; the company Squad, not a brand account, carries the brand [self-set]. Multiple accounts per person are banned [platform].
- **Picking Squads:** choose by topic fit, rules card and a gate the poster meets; never by member count. Unknown gate: mark it "check in composer" in the plan.
- **Picking tags:** the stack the reader works in (language, framework, the category your product sits in), checked against the tag page's top posts; never your product name alone.

For per-Squad gates, platform caps and paid-program limits, read [references/limits-and-paid-programs.md](./references/limits-and-paid-programs.md).

## Self-promotion limits

- daily.dev publishes no promotion ratio; the line is "primarily for self-promotion" [platform].
- Third-party Squads set their own posting gate (open, approval, minimum reputation such as 250 or 1,000) and up to 10 rules; read the rules card before posting [platform]. Moderators decline or delete posts against those rules [platform].
- Default ratio: three non-product contributions (comments, curated shares) per product post, per person [self-set].
- In your own Squad you set the rules; keep pitch-free tutorials the majority, since featuring rewards quality posts and active engagement [platform] and members join to learn [self-set].

## Cadence

1. **Weeks 1-3, earn first.** Each poster completes a profile, verifies the company badge with a work email, follows target tags, and comments substantively on 3-5 posts a week. No links in comments. Claim authorship of indexed posts.
2. **Week 2, build the Squad.** Public, the closest category (DevTools for a vendor Squad), image, cover image, description, Stack & Tools, rules, posting mode "Require post approval", Slack integration on so comments reach whoever owns replies. Seed 5-10 curated posts with commentary before inviting anyone.
3. **Week 3, invite.** Share the invitation link to your existing community and newsletter; never pay or incentivize joins.
4. **Weeks 3-8, publish.** One original technical post a week via New Post to profile plus your Squad and at most 2 more; answer every comment within 24 hours. A poster still under 250 by week 4 posts only in your own Squad.
5. **Launch week, week 4 at the earliest.** One strong post plus a Squad poll. Post Boost only if the post earned organic upvotes in its first 24 hours [self-set].
6. **Monthly.** Read post and Squad analytics; drop tags and Squads that drew nothing.

**Launch sooner than week 4:** post once, from the named engineer with the most reputation, into your own Squad plus at most 2 Squads whose gate that account meets. Expect little organic reach, skip Boost unless the 24-hour rule above holds, and treat daily.dev as a follow-up channel for the launch.

## Flagged, declined or removed

1. Stop reposting; a repeat after a decline reads as spam.
2. Read the moderator's decline reason or the Squad rules; fix the post (substance, disclosure, no affiliate link), then resubmit once, since edits need re-approval.
3. Platform removal or reputation drop: contact daily.dev support with the post URL and the fix; review is not guaranteed to reverse.

## Measure

Targets are self-set; daily.dev publishes no organic benchmark for vendors and no rate card.

- Reputation per poster, weekly, until 250.
- Per post at day 3: impressions, unique reach, upvotes, comments, clicks; UTM-tagged links for referral sessions and signups.
- Squad monthly: members, upvote ratio, clicks, new members per Boost.
- On an Ads plan: install the daily.dev conversion pixel for signup and view-through attribution; keep UTMs for organic posts.
- Hygiene, pass threshold zero: declined posts, removals, reputation drops.

## Output

In order: when the user brings a plan, a verdict on each of its items first; fit verdict; entry path with its reason; setup (profiles, badge, claiming, Squad fields and rules); ranked surfaces with what moved; per-post tags and target Squads with each Squad's gate; eight-week cadence with owners and hours; paid decision with the conditions that justify it; the templates from [references/templates.md](./references/templates.md) this plan uses, filled; metrics. Size the cadence to eight weeks even for a one-week request: reputation takes weeks. Run drafts through your preferred humanizer skill.

## References

- samber/developer-relations-skills@engineering-blog-post - writing the post this skill distributes.
- samber/developer-relations-skills@devto-playbook - the DEV cross-post that daily.dev can pick up.
- samber/developer-relations-skills@hackernews-playbook - the other launch-day discussion channel.
- samber/developer-relations-skills@oss-launch - the launch window a daily.dev push belongs to.
- samber/developer-relations-skills@devrel-content-calendar - fitting daily.dev slots into the quarter.
- samber/developer-relations-skills@devrel-analytics - attributing referral signups.
- samber/developer-relations-skills@developer-community-launch - whether a Squad or an owned community should be home.
