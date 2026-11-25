---
name: discourse-forums-playbook
description: "Runs a developer-tools vendor's own Discourse forum as its operator - categories and tags, trust levels, spam controls, seeding without sock puppets, Solved support categories, what Hot, Top and the summary email reward, and forum SEO (Q&A markup, login-required trap). Use whenever a community team sets up, restructures or revives a product forum on Discourse or a similar self-hosted forum, asks about trust levels or the Solved plugin, why topics go unanswered, or whether threads rank on Google - even if they only say 'our Discourse is dead'. Not for members of someone else's forum. Do NOT use to pick the venue - use samber/developer-relations-skills@developer-community-launch; for a code of conduct or incident, samber/developer-relations-skills@developer-community-moderation."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Discourse Forums Playbook

You run a vendor's own Discourse forum: an async, searchable, member-moderated space the vendor hosts and answers for. Its value compounds only when questions get answered and the answers stay findable. Every rule below protects those two things.

Label every platform claim:

- **[Discourse]**: Discourse's docs, source or shipped defaults state it.
- **[Google]**: Google Search Central states it.
- **[practitioner]**: community managers' experience, or a starting value you set yourself.

Check the live value in the forum's admin settings before quoting a number, when you can read them: defaults are admin-configurable and hosted plans gate some features. Map other self-hosted forums' names for the same concepts (trust tiers, categories, solved answers), and never assume the same thresholds.

## Route first

- No venue chosen yet, generic founding-member strategy, "should we have a forum at all": `samber/developer-relations-skills@developer-community-launch`. This skill starts once Discourse is the venue.
- Code of conduct, enforcement ladder, an incident: `samber/developer-relations-skills@developer-community-moderation`. This skill only configures the platform controls that ladder uses.
- The metric framework and thresholds: `samber/developer-relations-skills@developer-community-health`. This skill names the Discourse reports that feed it.
- Single sign-on with the product account, embedding topics in docs or the product, the forum API and webhooks: `samber/developer-platform-skills@developer-portal-design`.
- A real-time chat server: `samber/developer-relations-skills@discord-community-playbook`.

## Refuse these moves

| Tempting move                                                              | Why it fails                                                                                                                                                                   |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Seed with alt accounts, fake members or staff posting under invented names | Discourse's community manager on its own forum: "a hard no" [practitioner]; members who discover it leave                                                                      |
| Generate dozens of seed topics or answers with AI                          | Google's spam policies name generating many pages without adding value as scaled content abuse [Google]; seed from real questions                                              |
| Launch with login required "until we're ready"                             | The whole site disappears from search, and opening login-only posts later breaches what members agreed to; one forum had to start new public categories instead [practitioner] |
| Open one category per product module on day one                            | Empty rooms announce a dead forum; start with 3-5 and split when one category carries too many unrelated threads [practitioner]                                                |
| Bulk-grant TL3 to imported or new accounts                                 | TL3 links lose nofollow and TL3 can recategorize and rename [Discourse]; grant TL1 through a verified-customer group if needed, earn the rest                                  |
| Queue every member's posts for approval                                    | Answer time is the forum's product; queueing TL0 posts only during a spam wave is fine                                                                                         |
| Enable Solved on every category                                            | Solved switches a category's topics to Q&A markup, and Google wants it only on one-question-with-answers pages [Discourse] [Google]                                            |
| Promise organic traffic as the business case                               | Forum search traffic swings with core updates [practitioner]; sell answered questions first, search as upside                                                                  |
| Buy ads or run a promotion push while topics go unanswered                 | Newcomers arrive as TL0 into silence and do not return; fix answer supply first                                                                                                |
| Auto-post every blog article or release feed as a topic                    | Few distinct posters or likers, so they score low on Hot, and they crowd member questions off Latest; post a few by hand, under the author's name, with one real question      |

## Match the answer to the request

- Narrow question (one setting, one rule, why X ranks): answer it, plus the refusals and limits it touches.
- Setup, revival or exec review: run the Interview, then deliver the full Output. For an exec, open with a two-line verdict.

## Interview

One question per message; skip what the request or the forum itself answers. When the user wants one pass, state an assumption per gap.

1. State: not opened, open under 90 days, established but stalling, or migrating from another forum or GitHub Discussions?
2. Primary job: support deflection, search acquisition, customer peer community, product feedback, or an extension ecosystem?
3. Who answers daily, how many hours a week, in which time zones?
4. Public, customer-only, or mixed content? Any legal or contractual reason a topic must stay private?
5. Hosted plan or self-hosted? Solved, Discourse AI and SSO depend on the hosted tier [Discourse].
6. Deadline, payoff horizon (one-off fix or compounding asset), and hours available.

## Structure: categories, tags, homepage

1. Start with 3-5 categories, each with a one-sentence About post saying what belongs there. A typical vendor set: Support (Q&A), Announcements (staff topics), Show and tell, Feedback, plus the default staff area.
2. Use tags for product area, version and integration, not more categories. Only TL3 and staff create tags by default [Discourse]: pre-create the tag set and require one tag from the product group in Support.
3. Make Categories the homepage until the forum has daily traffic, then switch to Latest [practitioner].
4. Write the pinned welcome or banner topic: what this place is, what to post where, how fast staff answer [Discourse].
5. Rewrite the default guidelines in week one, linking the code of conduct.
6. Decide public versus private per category before launch. Keep anything a customer contract covers in a restricted category from the start.
7. Give a product team moderation of its own category through category group moderation, off by default, instead of full staff rights [Discourse].

## Trust levels: the moderation layer

| Level | Default bar, abbreviated [Discourse]                                                                                                                                          | Use it for                                             |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| TL0   | account created                                                                                                                                                               | sandbox (see Limits)                                   |
| TL1   | 5 topics entered, 30 posts read, 10 min                                                                                                                                       | flagging, personal messages                            |
| TL2   | 15 visit days, 20 topics, 100 posts read, 60 min, 3 replies, 1 like given and received                                                                                        | invites                                                |
| TL3   | 50 of the last 100 days visited, 10 topics replied, 25% of topics and posts read, 20 likes received, 30 given, 5 flagged posts at most; lost when the bar slips unless locked | recategorize, rename, create tags; links lose nofollow |
| TL4   | manual only                                                                                                                                                                   | edit, close, pin                                       |

- Links from everyone below TL3 carry nofollow [Discourse]; Google recommends the same for untrusted users [Google].
- Promote TL4 by hand from TL3 members who already moderate well; that list is your champions pipeline.
- Imported members: carry their old standing as at most TL1-TL2 [practitioner]. A manual TL3 lapses after its 100-day grace period unless locked [Discourse].

## Spam controls, in order [practitioner]

1. Turn on AI spam detection: Discourse enabled it by default on lower hosted tiers, so check the AI settings on any plan; off on self-hosted until Discourse AI and an LLM are configured. It scans the first 3 posts of TL0-TL1 users [Discourse].
2. Add watched words for the spam vocabulary (block, flag or require approval).
3. Block disposable email domains.
4. During a wave, queue TL0 posts only: in the two approval-exempt group settings, replace trust_level_0 with trust_level_1. Trust-level groups are cumulative, so removing TL0 alone queues every member [Discourse].
5. Lower accounts per IP below the default 3 if signups share addresses.
6. Raise TL1 requirements last: it lengthens the sandbox, but day-one spam posts as TL0 anyway.

## Engagement surfaces, ranked by value per hour

Efficiency: answering in a Solved support category > welcome topic and category About posts > a weekly ritual topic > summary email tuning > links from docs, error messages and the product help menu > Show and tell category > announcements > badges and groups.

| Surface                                       | Payoff            | What it buys                                                                       |
| --------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------- |
| Support category with Solved                  | compounding       | Answers that rank and deflect the next ticket; unsolved filter is the triage queue |
| Welcome topic, About posts, guidelines        | compounding       | First-visit clarity on every page view                                             |
| Weekly ritual topic ("what are you building") | compounding       | Habit and member-written content                                                   |
| Summary email                                 | compounding       | Lapsed members pulled back by popular topics                                       |
| Links from docs and the product               | compounding       | Askers arrive where answers live                                                   |
| Show and tell                                 | one-shot per post | Member projects; the only place members self-promote                               |
| Announcements                                 | one-shot          | Release reach; replies stay open for questions                                     |
| Badges, groups, user titles                   | compounding       | Visible status for helpers; staff flair discloses employees                        |

- **The order starves** announcements: a forum full of release posts reads as a press room.
- **Default rung:** Support with Solved plus the welcome topic. A search-acquisition goal promotes docs links and Support; a feedback goal promotes the Feedback category.
- Re-rank against what the user owns: an existing support inbox is a seed source, a large newsletter promotes the summary email.

## What the lists, email and search reward

All list and email mechanics below are from Discourse's source [Discourse].

- **Latest:** order of last reply. A bump moves it here and barely anywhere else.
- **Hot:** likes plus distinct likers and distinct posters in the last 7 days, decayed by topic age (gravity 1.2); closed topics count half; only the top slice of recently active topics shows. More different people taking part beats one person posting more.
- **Top:** log(views), first-post likes, likes per post (capped), log(post count), and a bonus once a topic reaches 10 posts. Long, liked discussions win.
- **Summary email:** weekly by default for absent members, 5 popular topics and 5 posts, stops after 180 days of inactivity; exclude Announcements or noisy tags with the digest suppress settings.
- **Search:** title and first post become the search title and description, so write titles in the asker's words. Other topics carry forum markup; Solved categories carry Q&A markup on every topic, solved or not, so enable it only where every topic is a question [Discourse] [Google].
- **Do less:** self-bumping; staff-only threads; migrating without permalinks (old URLs 404 and lose rankings); moving to a subfolder for SEO, since Google states no preference and Discourse recommends a subdomain [Discourse].
- **AI crawlers:** rate-limited by default, not blocked [Discourse]; block only for a stated reason.

## Cadence

New forum:

1. **Weeks -6 to -2:** recruit 10-50 founding members by name from support, beta and issue history [practitioner]. Run this phase in a category that stays restricted, or tell founders in the invite that their posts go public on launch day.
2. **Weeks -2 to 0:** seed 5-10 real questions from tickets, posted by the asker or by staff under their own names with the asker's consent, each answered and marked solved [practitioner].
3. **Launch week:** link from docs, product help menu, newsletter and signature; announce once.
4. **Days 1-90:** one owner runs a daily pass on unanswered and unsolved topics; welcome each new member's first post; post the weekly ritual topic.
5. **Monthly:** read the admin reports (time to first response, topics with no response, trust level growth) and the search console; promote recurring solved answers into docs; split or merge categories.

Established forum, replacing steps 1-3:

1. **Week 1:** pull baselines from the admin reports; list categories with no new topic in 30 days.
2. **Week 2:** merge dead categories into tags, keep URLs redirecting, post one note explaining the new map.
3. **Week 3:** clear the unanswered backlog: reply, merge duplicates, close stale topics with a note. Never mass-bump.
4. **Weeks 4-6:** invite existing non-staff helpers (TL2-TL3, top repliers) by name into a helper group, adapting the founding-member invite.
5. Then run steps 4-5 above. Plan cover for holidays: a two-person team out together stalls every answer.

## Limits

| Scope              | Limit                                                                                                                                                                                                                                                  | Kind                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| New accounts (TL0) | 3 topics and 10 replies on day one, 2 links, 0 attachments, 30 s between posts                                                                                                                                                                         | enforced default [Discourse] |
| Registration       | 3 new accounts per IP; fast-typed first posts silenced                                                                                                                                                                                                 | enforced default [Discourse] |
| Flags              | spam flags from 3 members, above the hide sensitivity, silence a new user; 5 flaggers close a topic                                                                                                                                                    | enforced default [Discourse] |
| Support category   | one question per topic; the opt-in Support category type sets solved topics to auto-close 2 days after the last reply (plugin default: never). When staff mark the solution, raise it to 7-14 days so the asker can still say it failed [practitioner] | preset [Discourse]           |
| Show and tell      | self-promotion allowed, one topic per project, updates as replies                                                                                                                                                                                      | policed, set by you          |
| Support, Feedback  | no self-promotion; competitors' staff disclose                                                                                                                                                                                                         | policed, set by you          |
| Old topics         | reviving year-old threads to add "+1"                                                                                                                                                                                                                  | policed [practitioner]       |
| Never indexed      | search, user, group and tag-filter pages                                                                                                                                                                                                               | enforced [Discourse]         |

## Diagnose a quiet or unanswered forum

1. Count new topics with no reply after 48 hours. Above about 10% of new topics [practitioner], staffing is the defect, not promotion. A 7-day figure understates the 48-hour one.
2. Count categories with no new topic in 30 days; merge them.
3. Check who answers. Staff writing most answers means either no TL2-TL3 helpers, or staff answering before helpers can; check whether TL2-TL3 members post at all, then try a short delay before staff reply.
4. Check search: inspect a solved topic with `?print`; confirm it is public, canonical and listed in `/sitemap.xml` [Discourse].
5. Check signup friction: login-only content, forced profile fields, or a queue on every first post.

## Output

For a setup or revival plan, deliver in order: refusals triggered; category and tag map with About lines; trust-level and spam settings kept or changed, with the reason; surfaces ranked for this user with what moved; dated cadence; limits that bind; templates from the templates reference, filled for the user's product and run through your preferred humanizer skill; metrics and the stop rule.

## Metrics and stop rule

Set each target from the week-1 baseline; the starting values below are [practitioner] defaults until a baseline exists.

- Median time to first reply under 24 hours; topics with no reply after 48 hours near zero.
- Share of support topics solved.
- Share of solutions written by non-staff, rising quarter on quarter - except when the primary job is support deflection, where staff answering is the design.
- Count of TL2 and TL3 members; new members' first-week post rate.
- Search landings on solved topics, from the search engine's own console.
- Stop rule, new forum: after 90 days with no non-staff solutions and no TL2 growth, fold back per the launch skill's kill criteria.
- Stop rule, established forum: if the primary-job metric from interview question 2 is flat for two quarters, cut categories and scope before adding staff hours.

## References

- [references/templates.md](./references/templates.md) - welcome topic, category About posts, founding-member invite, first-post welcome, solution nudge, duplicate and move notes, weekly ritual topic, seed-from-ticket consent request.
- samber/developer-relations-skills@docs-seo - SEO of the docs site the forum links to.
- samber/developer-relations-skills@developer-troubleshooting-docs - turning recurring solved topics into error-reference pages.
- samber/developer-relations-skills@developer-champions - a formal program for the TL4 and top-helper pipeline.
- samber/developer-platform-skills@github-engagement-playbook - GitHub Discussions, when the audience lives on the repository instead.
