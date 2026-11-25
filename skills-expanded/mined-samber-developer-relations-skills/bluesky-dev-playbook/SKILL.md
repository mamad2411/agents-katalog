---
name: bluesky-dev-playbook
description: "Runs a devtool vendor's, developer advocate's or open-source maintainer's presence on Bluesky - go-or-skip verdict, people versus brand accounts, domain handles and the blue check, starter packs, developer custom feeds, discovery without a central algorithm, block lists, cross-posting from X or Mastodon, what a bot account may do. Use whenever someone asks how to grow a developer audience on Bluesky, set up a devtool company or OSS project account, get into a starter pack or a dev feed, mirror their X account to Bluesky, or why their devtool's Bluesky posts get no reach - even if they only say 'should we be on bsky'. Not for coding bots, feed generators or other AT Protocol apps. Do NOT use for the weekly narrative - use samber/developer-relations-skills@build-in-public."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Bluesky Developer Playbook

You run a vendor's, advocate's or maintainer's presence on Bluesky: a network where reach travels through people, opt-in custom feeds and starter packs, not through one ranked timeline. Every rule below follows from that.

Label every Bluesky claim: **[Bluesky]** when Bluesky's guidelines, docs, protocol spec, blog, official account or public API state it, **[research]** for peer-reviewed studies, **[press]** for reported incidents, **[practitioner]** for tool vendors, third-party docs and reverse-engineering, including your own reading of a Bluesky rule. Never present a practitioner claim as a Bluesky rule. The app ships features monthly: before quoting a number, re-check it in [references/platform-facts.md](./references/platform-facts.md) and, when you can browse, on Bluesky's own pages.

## Refuse these moves

| Tempting move                                                                               | Why it fails                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Port the X playbook: threads tuned for "the algorithm", best posting hour, hook formulas    | The Following feed is chronological and Discover is personalized per user [Bluesky]; topic reach comes from feeds and packs the reader opted into                                                                              |
| Auto-like, auto-follow or auto-reply to anyone who mentions a keyword                       | Automated or bulk interactions that notify a user are spam [Bluesky]; bots may interact only when tagged [Bluesky]                                                                                                             |
| DM dozens of people asking them to follow you, your pack or your project                    | Bulk messages count among the notifying interactions the rules call spam [Bluesky], and by default only people a user follows can DM them [Bluesky]; announce the pack once in a post                                          |
| Ask staff or a Discord to like and repost the launch post; follow/unfollow for follow-backs | The Guidelines ban artificially manipulating social signals [Bluesky]; treat a coordinated staff push as exactly that; readers see the pile-on [practitioner]                                                                  |
| Pay a curator for starter-pack placement, or add people to your pack without asking         | Paid placement unlabelled is undisclosed commercial content [Bluesky]; unconsented additions draw complaints [research]                                                                                                        |
| Run an unattended mirror of the X account                                                   | Crossposted replies make no sense off X, and dropped alt text and x.com links read as "nobody home" [practitioner]                                                                                                             |
| Publish AI-written posts the named person did not rewrite, or lead with "AI-powered"        | AI content and AI branding draw mass blocks and block-list inclusion; Bluesky's own AI assistant became the second most-blocked account [press]. Drafts you produce are starting points the person rewrites in their own voice |
| Collect posts from the firehose for "community insights" or a dataset                       | A one-million-post dataset was pulled within a day over consent [press]; consent is the norm here, not the API's openness                                                                                                      |
| Post sponsored or affiliate content without saying so                                       | Undisclosed commercial content is banned [Bluesky]                                                                                                                                                                             |
| Rename the account or change its display name after it gets the blue check                  | The badge is tied to handle and display name at issue time; changing either drops it until re-verified [Bluesky]                                                                                                               |
| Promise follower growth or "virality"                                                       | Users can opt out of being shown to non-followers in Discover [Bluesky]; the most-liked dev feeds count likes in the hundreds [Bluesky]                                                                                        |

## Match the answer to the request

- Narrow question (can our bot reply, why did the badge vanish, how do I get into a feed): answer it, plus the refusals and limits it touches.
- Presence setup, launch, or "no reach": run the Interview, then deliver the full Output.
- A direct question inside a setup request ("which order?"): answer it in the first lines, then the full Output.
- Coding a bot, feed generator, labeler or "Login with Bluesky" is integration engineering: say it is outside this skill and point at the AT Protocol developer docs; this skill covers only how such an account behaves.
- Hiring posts: the employer-brand plan they serve belongs to samber/developer-relations-skills@tech-employer-branding; post them from a person's account like any other post.

## Interview

One question per message; skip what the request answers. When the user wants one pass, state an assumption per gap.

1. Goal: launch, ongoing presence, a thread already about you, or migrating followers from X or Mastodon?
2. Who will post, under their own name, and how many hours a week? A brand account with no named person is the weakest setup.
3. Where is the audience today: name the language or tool communities, and whether they are visibly on Bluesky (feeds, packs, people).
4. Does the product or messaging lean on AI, scraping or user data? This changes the risk column.
5. Domain the company controls, and whether any account is already verified.
6. Date the result must land by, one-off moment or compounding asset, and the effort ceiling.

## Go or skip

Run this before any setup, and return one verdict:

- **Skip**, and say so, when either holds:
  - no feed, pack or recognizable person in the audience's stack is active on Bluesky;
  - nobody can post as a person for at least an hour a week.
- **Go small** (one person, replies only) when the audience is present but the product or plan is AI-forward or relies on collecting users' posts or data.
- **Go** otherwise.

A skip verdict is a valid output, not a failure.

## Accounts and identity

- **People first.** Advocates, maintainers and engineers post under their own names; the brand account is a hub that reposts their teaching posts a few times a week, announces releases and answers support [practitioner].
- **Domain handles for every official account:** `company.com` for the brand, `name.company.com` subdomains for staff, set with a DNS TXT record on `_atproto` whose value is `did=<the account's DID>`, or the `/.well-known/atproto-did` route, which needs a web server answering on each subdomain [Bluesky]. This is Bluesky's own anti-impersonation advice.
- **Blue check:** apply through Bluesky's form only once the handle and display name are final. Never promise it: Bluesky verifies "notable and authentic" accounts at its discretion [Bluesky].
- **Rebrand once:** rename in one step, pin a post announcing it and keep the old name in the bio for a while; the Guidelines ban "identity churning (changing your account identity to keep followers)" [Bluesky]; one announced rebrand that keeps the old name visible reads as legitimate, repeated renames do not [practitioner].
- **Team-operated hub account:** staff running their employer's own account is not the account selling or sharing the Guidelines ban [practitioner]; each person and tool signs in with its own app password, 2FA on, so access stays revocable.
- **Bot accounts** turn on the bot label in account settings [Bluesky]; also give them their own handle, "bot" in display name and bio, and the human operator's name [practitioner].
- Never squat handles of competitors or projects you do not run; handle-squatting and impersonating brands are banned [Bluesky].

## Engagement surfaces, ranked by value per hour

Efficiency: replies in your stack's existing conversations > inclusion in community starter packs > posting into existing dev custom feeds > your own starter pack > brand-account release posts > your own custom feed > trending topics.

| Surface                                          | Payoff            | What it buys                                                                                                                                                          |
| ------------------------------------------------ | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Replies and quote posts in your field            | compounding       | Follows from people already in the graph; social-proximity ranking favours replies from people near the reader [Bluesky]                                              |
| Community starter packs that include your people | compounding       | The largest follow lever measured: members gained up to 85% more new followers [research]; an upper bound, and it favours accounts already popular                    |
| Existing dev custom feeds                        | one-shot per post | Readers who pinned a topic. Small feeds often name their keyword, hashtag or emoji; large ones often use undocumented rules [practitioner]                            |
| Your own starter pack                            | compounding       | Creators who listed themselves gained up to 117% more new followers, those who did not about 22% [research]; list community people, staff to a few, yourself included |
| Brand hub posts, pinned post, profile links      | compounding       | A place to land; release notes, docs links                                                                                                                            |
| Your own custom feed                             | standing job      | Worth it only when the topic has no feed and someone owns the matching rule; you also become its moderator                                                            |
| Trending topics                                  | rare              | Mostly general news; dev topics seldom trend [practitioner]                                                                                                           |

- **Starved option:** your own custom feed scores high on value for a niche stack with no feed, but costs a standing job, so efficiency never picks it. Promote it when a language or framework has no active feed and a maintainer volunteers to own it.
- **Default rung:** two weeks of replies by named people, then ask a curator to add them to a community pack.
- Re-rank against what the user owns: a maintainer already in a pack skips to posting; a hard launch date promotes feed posts with the right tag.

## What ranking rewards and punishes

**Do more:**

- Posts and replies that start conversations; replies from inside the reader's social neighbourhood rank higher [Bluesky].
- The keyword or tag a dev feed matches, on posts that belong there. When its description names no rule, watch the feed for a week or ask its operator before adding tags [practitioner].
- Alt text on every image and video [practitioner].
- Links to docs, repos and posts: links get the same visibility as other posts and Bluesky does not downrank them [Bluesky].

**Do less:**

- Toxic, off-topic or bad-faith replies: down-ranked in threads, search and notifications [Bluesky].
- Posts users mark "show less" or dislike: they shrink your reach with that user and partly their neighbourhood [Bluesky].
- Hashtag stuffing to reach unrelated feeds: feed operators can remove accounts, readers mute [practitioner].
- Anything that reads as automated: undeclared-bot labelers mark it [practitioner].

## Cadence

1. **Week 0:** domain handles, bios naming the person and employer, pinned post, staff disclosure line ready. Each person keeps a list of searches for their stack's terms (search filters by keyword, people, date and language [Bluesky]); this is the listening tool, never a firehose scrape.
2. **Weeks 1-2:** each person replies daily to what those searches and their stack's feeds surface; no product links unless asked.
3. **Week 3:** for each relevant community pack, ask its curator to consider one named person, with a reason the pack's readers gain, in a public reply first; never ask for your whole team.
4. **Week 4 onwards:** a few original posts a week per person, release posts on the hub, reposts of staff. After about a month of replies, build your own pack from community people you now talk with, each asked first, announced once in a post.
5. **Launch day:** the person who built it posts, the hub reposts, the post uses the feed tag; staff reply to questions, never mass-like. If replies turn hostile, the poster can limit replies or detach quote posts [Bluesky].
6. **Monthly:** check block-list inclusion and labels on your accounts, review referrals, drop surfaces that returned nothing.

## Limits

Per-surface table with each limit's kind and source: [references/platform-facts.md](./references/platform-facts.md) § Limits. The ones that bind most often:

- Starter pack: 150 people, 3 feeds [Bluesky]; curators decide who is in, and blocking a pack's creator removes you from it.
- Each custom feed sets its own entry rule and moderation; its operator can exclude you.
- Block lists and labelers: anyone can list your accounts, and subscribers stop seeing you.
- Bots: post freely on a schedule, interact only when tagged, labelled [Bluesky].
- The write budget (5,000 points per hour, 35,000 per day; a follow or like costs 3 [Bluesky]) is not permission: bulk interactions are spam far below it.

## Cross-posting from X or Mastodon

- **Mastodon:** prefer the opt-in Bridgy Fed bridge over a copy bot. The Mastodon account opts in by following `@bsky.brid.gy@bsky.brid.gy`; some instances block the bridge, so test it from yours; replies from Bluesky users who have not bridged reach you only as an hourly DM digest, so someone still reads Bluesky directly [practitioner: Bridgy Fed's own docs].
- **X:** pick one home network. Cross-post original posts only, rewritten under 300 characters, with alt text and without x.com links; never cross-post replies or quote-tweets. A person reads Bluesky replies daily, or the mirror stops.

## Output

For a full plan, deliver in order: the direct answer when the user asked one; go/skip verdict with the reason; refusals triggered; account and handle plan; surfaces ranked for this user with what moved the order; dated cadence; limits that bind, each with kind and source; the matching templates from [references/templates.md](./references/templates.md) adapted to the user; metrics. Mark every drafted post as a draft for the named person to rewrite, and run it through your preferred humanizer skill.

## Metrics

Bluesky shows no impression or reach counts on posts [practitioner]; measure what is observable.

- Replies, reposts and quote posts per post and per person, not likes alone.
- Follower change in the week after a pack inclusion or feed post. Bluesky notifies a pack's creator only when a new user signs up through it [Bluesky], so pack-driven follows are an estimate, never exact attribution.
- Referral sessions and signups with referrer `go.bsky.app` [Bluesky] plus UTM-tagged links, since some clients strip referrers, against a pre-launch baseline.
- Count of block lists and labelers that list your accounts; any increase after a post is a stop signal.
- Never report raw follower totals as the headline.

## References

- samber/developer-relations-skills@devrel-content-calendar - fitting Bluesky slots into the quarter.
- samber/developer-relations-skills@hackernews-playbook - the other launch-day channel, with its own rules.
- samber/developer-relations-skills@devto-playbook - where the long-form post behind a Bluesky link lives.
- samber/developer-relations-skills@oss-launch - the cross-channel launch plan this post belongs to.
- samber/developer-relations-skills@developer-community-moderation - when a pile-on starts in your replies.
- samber/developer-relations-skills@devrel-analytics - attributing Bluesky referrals to signups.
