---
name: discord-community-playbook
description: "Runs a devtool vendor's or open-source maintainer's presence on Discord - its own developer server (onboarding, forum help, announcements, Discovery, web pages) and staff posting in other people's developer servers. Use whenever someone sets up, restructures or grows a Discord server for developers, asks why their Discord is quiet or answers get lost, wants to post in someone else's dev server, or asks about Discord Discovery or Partner/Verified badges - even if they only say 'our Discord'. Not for bots, apps or event servers. Do NOT use for whether to open a community - use samber/developer-relations-skills@developer-community-launch; for moderation or raids, samber/developer-relations-skills@developer-community-moderation; for health metrics, samber/developer-relations-skills@developer-community-health."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Discord Community Playbook

You run a developer product's presence on Discord: chat-first, notification-driven, and governed by two rulebooks at once, Discord's platform policy and each server's own moderators.

Label every claim: **[Discord]** when Discord's support articles, guidelines or community guides state it, **[server]** when one server's published rules state it, **[practitioner]** for project write-ups, reverse-engineering and this playbook's own judgment. Never present a practitioner claim as a Discord rule. When you can browse, re-read the support articles listed in [references/platform-facts.md](./references/platform-facts.md) before quoting a limit or a date: Discord changes features monthly.

## Scope

- **Here:** a server that exists or has been chosen; staff posting in other servers; Discord settings, channel types, limits, policy, metrics.
- **Route out:** whether to open a community, or Discord vs forum vs Slack, to `samber/developer-relations-skills@developer-community-launch`; the code of conduct, AutoMod rules, raids and incident handling to `samber/developer-relations-skills@developer-community-moderation`; a health metric framework across channels to `samber/developer-relations-skills@developer-community-health`.
- **Out of scope:** bots, Discord apps, App Directory listings and API integrations; a server that lives only for one conference or hackathon.

## Refuse these moves

| Tempting move                                                                    | Why it fails                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Run an invite contest: swag, credits or a role for whoever brings the most joins | "Invite rewards" and "join-for-join" are named as banned membership inflation [Discord]                                                                                                                                                                                         |
| Apply for the Discord Partner or Verified badge                                  | Partner is closed to new applications; Verified is games-only, through Steam [Discord]                                                                                                                                                                                          |
| Promise "Discord answers never reach Google" or "they will rank now"             | Both are wrong. Only Discoverable servers (1,000+ members) get Server Web Pages. Channel Summaries there follow admin settings only; individual messages also need each member's setting, off by default in the EU/EEA, UK, Canada, Brazil, Australia and South Korea [Discord] |
| Drop a product link or launch post in another server's #general                  | Commercial posts belong only in channels built for them; tolerance drops as servers grow [server]                                                                                                                                                                               |
| DM members of someone else's server, or have a bot DM every new joiner a pitch   | DMs need the person's in-server permission [server]; join-DM ads are "regarded as spammy" and may breach the ToS [Discord]                                                                                                                                                      |
| Paste an AI-generated answer into another server's help channel                  | Python Discord bans copy-pasted AI answers [server]; elsewhere it reads as drive-by marketing [practitioner]                                                                                                                                                                    |
| Build a 15-20 channel tree and a bot verification gate on day one                | Discord advises native Onboarding and Raid Protection over bot gates, and 4-5 channels per category [Discord]; empty rooms read as a dead server [practitioner]                                                                                                                 |
| Report member count as the result                                                | A join is not activity [practitioner]; Discord's own benchmarks use communicators and new-member retention [Discord]                                                                                                                                                            |
| Answer from a shared brand account                                               | A named person earns trust a logo cannot, and hosts expect staff to say who they are [practitioner]; never automate the account, since self-bots are banned [Discord]                                                                                                           |

## Interview

One question per message; skip what the request already answers. When the user wants one pass, state an assumption per gap and carry on.

1. Job: run your own server, show up in others' servers, or both?
2. Own server state: exists or chosen, member count, age, Community enabled, Discoverable?
3. Who staffs it, how many hours a week, in which time zones?
4. What brings people: support questions, release news, chat, events? How long does a good answer stay useful?
5. Where do your users already talk on Discord, and can they reach it at all (corporate networks and some countries block it)?
6. Date the result must land by, one-off win or compounding asset, and the effort ceiling.

If the answer to 1-2 is "we don't have one and aren't sure we should", stop and route to `developer-community-launch`.

## Engagement surfaces, ranked by value per hour

Efficiency: answering in ecosystem servers your users already use > forum help channel in your server > announcement channel followed into partner servers > hosted Q&A in a host server > scheduled events in your server > Discovery listing > Server Tags.

- value: forum help channel > answers elsewhere == announcements followed > hosted Q&A == Discovery == events == showcase posts == Server Tags. Answers and followed announcements tie because both reach users where they already read. The last five tie because each buys a small or uncertain audience once, or only a badge.
- effort, highest first: Discovery > forum help channel == Server Tags > announcements followed == events > hosted Q&A > answers elsewhere == showcase posts. The forum and Server Tags tie because one costs a weekday owner forever and the other a recurring boost spend. Announcements and events tie at about an hour a week each. Answers and showcase posts cost minutes each.

| Surface                                        | Payoff                               | Value                                                 | Effort                      | Compliance cost                |
| ---------------------------------------------- | ------------------------------------ | ----------------------------------------------------- | --------------------------- | ------------------------------ |
| Answers in others' help channels, disclosed    | compounding (reputation)             | ++                                                    | +++                         | + (host rules)                 |
| Forum help channel with tags, own server       | compounding (archive)                | +++                                                   | - (standing owner)          | + (secrets, web indexing)      |
| Announcement channel others follow, own server | compounding (lands in their servers) | ++                                                    | +                           | ++                             |
| Hosted Q&A in a host server                    | one-shot                             | +                                                     | ++                          | + (host approval)              |
| Scheduled events and Stage, own server         | one-shot, repeatable                 | +                                                     | +                           | ++                             |
| Server Discovery and Server Web Page           | compounding                          | + (experimental Discover tab, sorted by member count) | -- (1,000 members, 8 weeks) | - (member notice, public page) |
| Server Tags on members' profiles               | compounding                          | +                                                     | - (3 boosts)                | ++                             |
| #showcase-style posts elsewhere                | one-shot                             | +                                                     | +++                         | - (frequency caps)             |

- **The order starves** the forum help channel: highest value, standing cost. It moves to first when support questions arrive daily and someone owns them each weekday.
- **Default rung:** two weeks answering in ecosystem servers, then a forum help channel. A hard date (launch, release) promotes announcements and a hosted Q&A; a compounding mandate promotes the forum and Discovery.
- Re-rank against what the user owns: an existing unofficial server can be adopted instead of built from zero (Prisma did, then retired its Slack) [practitioner]; a big partner server promotes channel following; users blocked from Discord at work demote every own-server rung.

## What Discord rewards and punishes

Discord has no ranked feed. Reach comes from notifications, default channel placement and Discovery.

**Do more:**

- Put help in a **forum channel** with required tags: text-channel questions get buried within hours [practitioner: Nuxt, before forums existed]; a forum keeps posts findable and can sync to an indexed home [practitioner: TCGdex]. Posts drop to "Older Posts" after inactivity, 3 days by default [Discord].
- Choose Onboarding default channels deliberately: they decide what every newcomer sees [Discord].
- Publish release notes in an announcement channel: followers' servers receive them, without @everyone [Discord].
- Offer an opt-in releases role through Onboarding and ping it instead of @everyone [practitioner].
- Track joins per invite link, one link per source; Insights shows the top invites and referrers [Discord].
- Aim at Discord's own benchmark: about 30% communicators; about half of members visiting and half of visitors talking [Discord].

**Do less:**

- @everyone and @here: members can suppress them server-wide, then miss what matters [Discord].
- Chat-only reach on large servers: above 2,500 members nobody can get a mobile push for every message, only mentions and role pings push [Discord].
- Extra channels: Discord says too many "spread the conversation too thin"; archive what Insights shows as dead [Discord].
- Anything Trust & Safety treats as spam or inflation: removal from Discovery follows enforcement [Discord].

## Run your own server

1. Enable Community: verified-email level, explicit-media filter, rules channel, moderator-only updates channel [Discord].
2. Rules Screening (up to 16 rules) plus Raid Protection alerts, instead of a bot gate [Discord]. AutoMod rules and the incident ladder belong to `developer-community-moderation`.
3. Start with 7 channels, 5 writable by @everyone, the Onboarding minimum [Discord]: announcements and rules (read-only); general, help forum, introductions, showcase, and off-topic, or a stack forum when you ship several SDKs (writable). Add a channel only when a topic overflows.
4. Onboarding: one question routing by stack, role or job (help, contributing, release news only); Server Guide with 3-5 first tasks [Discord].
5. Help forum post guidelines forbid pasting keys, tokens and customer data; moderators delete leaks at once and ask for rotation. Route account-specific support to a private channel or ticket.
6. Name one owner per weekday for the help forum; mark solved posts with a tag and close them.
7. Weekly: one ritual (release notes, office hours on Stage, show-and-tell). Below 500 members, count weekly posters, forum posts answered and joins per invite (Server Settings > Invites) by hand; from 500, export Insights to CSV monthly, since history stops at 120 days [Discord].
8. At 1,000 members and 8 weeks: decide Discoverable status as a privacy decision first, then a growth one. Check every channel's @everyone View permission: only role-restricted channels stay off the web [Discord]. Announce Web Presence to members, naming which channels feed summaries and which feed messages.

## Show up in other people's servers

1. Read the server's rules channel and promotion page before the first message; rules differ per server.
2. Answer from your own named account, with a server nickname or profile that names your employer. Disclose in any answer that mentions your product, a competitor, or a category you sell in.
3. Answer only what you can answer in full, in the thread, without a link unless the link is the answer. Post answers in your own words: Python Discord bans copy-pasted AI answers [server], and writing them yourself everywhere is the safe default [practitioner].
4. Ask the channel or moderators before anything commercial, stating the intent [server]. Post only after a yes; treat silence as no [practitioner].
5. Use the host's dedicated channels only: jobs, events, showcase, hosted Q&A. Showcase channels often favour individuals and indie work: Reactiflux says so for showcase [server]; a funded vendor asks for hosted Q&A instead [practitioner].
6. Never move a conversation to DMs unless the person invites it.

## Cadence

1. **Weeks 1-2:** answer in 2-3 ecosystem servers, no links to your own product.
2. **Week 2:** your own server live with the 7-channel set, a founding cohort invited by hand.
3. **Weeks 3-6:** weekly ritual; every help post answered the same working day; prune channels nobody visits.
4. **Launch week:** one announcement, published to followers; one event; showcase posts in host servers that allow them, once each.
5. **Monthly:** Insights export or hand count, channel pruning, a check of each host server's rules.
6. **Quarterly:** review Discoverable status, Web Presence channels and moderator 2FA.

When launch day is under two weeks away and staff have no history in a host server: send the moderator ask today, post in showcase channels only after a yes, and carry the launch on your own channels (announcements, docs, release notes). Never compress the earn-first weeks into launch week.

## Limits

| Where          | Limit                                                                                                                                                              | Kind                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| Discord        | Discovery: 1,000+ members, 8+ weeks old, activity criteria (unpublished), moderator 2FA                                                                            | enforced [Discord]     |
| Discord        | Announcement publishes: 10 per hour; one channel follows at most 10 others                                                                                         | enforced [Discord]     |
| Discord        | Onboarding: 7 default channels, 5 writable                                                                                                                         | enforced [Discord]     |
| Discord        | 500 channels, 50 per category, 250 roles, 999 invite codes, 2,000-char messages                                                                                    | enforced [Discord]     |
| Discord        | Insights from 500 members, 120 days of history, alpha and opt-out-able, so counts are partial                                                                      | enforced [Discord]     |
| Discord        | No invite rewards, join-for-join, bought members, unsolicited bulk DMs                                                                                             | enforced [Discord]     |
| Reactiflux     | Commerce only in dedicated channels; jobs only in `#job-board`; episodic content once every 2 weeks; conference posts one per milestone; no DMs without permission | policed [server]       |
| Python Discord | No unapproved advertising, no paid work, no copy-pasted AI answers                                                                                                 | policed [server]       |
| Small servers  | One self-promo channel; once per 24 h to once per 14 days; often no invite links                                                                                   | policed [practitioner] |
| Your server    | Your published rules; apply them to staff first                                                                                                                    | policed                |

Full per-server detail, sources and Discord caps: [references/platform-facts.md](./references/platform-facts.md).

## Output

For a full plan, deliver in order (when the job is others' servers only, drop server setup, Discoverable and own-server metrics): refusals triggered; the job and owner; surfaces ranked for this user, with the interview answer that moved each; server setup or host-server list with each host's rules; Discoverable and Web Presence decision; dated cadence; binding limits with kind and source; adapted templates from [references/templates.md](./references/templates.md); metrics. Run your preferred humanizer skill on every template you adapt before it reaches a channel.

## Metrics

- Communicators / visitors, weekly, against Discord's 30% benchmark and your own baseline.
- New-member retention after a week, and the share of joiners who post in their first week.
- Help forum: share of posts answered the same working day, share answered by non-staff.
- Joins per invite link per source.
- Host servers: answers given, accepted or thanked, and joins from the invite link in your profile.

## References

- samber/developer-relations-skills@developer-office-hours-program - the recurring office hours a Stage event hosts.
- samber/developer-relations-skills@developer-champions - recognising the members who answer in your help forum.
- samber/developer-relations-skills@developer-feedback-loop - routing feature requests out of Discord.
- samber/developer-relations-skills@discourse-forums-playbook - an owned async forum for answers that must live for years.
- samber/developer-relations-skills@developer-troubleshooting-docs - turning repeated help questions into docs pages.
- samber/developer-platform-skills@github-engagement-playbook - GitHub Discussions as the indexed support home beside Discord.
