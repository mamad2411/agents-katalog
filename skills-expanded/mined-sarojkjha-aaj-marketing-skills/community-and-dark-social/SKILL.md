---
name: community-and-dark-social
description: >-
  Use when the user wants to market in the places analytics cannot see -
  Slack and WhatsApp groups, private communities, podcasts, forwarded emails,
  AI assistants - or asks whether to start a community of their own. Also use
  when the user mentions dark social, word of mouth, "direct" traffic that
  makes no sense, community-led growth, community marketing, or how to
  measure something that has no referrer. Maps where buyers already talk
  from what they say, checks whether a community should open at all, and
  reads the dark side of the funnel by trend rather than attribution.
license: MIT
metadata:
  search_description: "Market where analytics cannot see: Slack groups, private communities, podcasts and forwarded email. Map where buyers talk and decide whether to start one."
  publisher: AAJ
  slug: community-and-dark-social
  category: Growth, Retention & RevOps
  phase: Execute
  difficulty: Intermediate
  card: >-
    Maps where buyers already talk, decides whether to open your own community, and measures dark social by asking.
  version: 1.0.1
  topic: social-community
  secondary_topics: [analytics-budget, content-seo]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The communities, people, podcasts and newsletters your customers named when asked where they get advice, with how many named each, how many leads mentioned it, and whether your team is present and answering there; for your own community, the recurring conversation, the host and their hours, the plan for when it goes quiet, and how many people have asked for it; for measurement, two or more periods of coded "How did you hear about us?" answers, branded search impressions, direct sessions to deep pages, and pipeline
  outputs: The map ranked by evidence with every place you should be in and are not, every room you pitched in, and your coverage; a go, not-yet or no on opening your own community with what is missing; and a trend read - working, wrong people, growing, going quiet or flat - across dark share, branded search, deep-page direct traffic and pipeline
  related_aaj:
    - https://aajconsult.com/playbooks/community-dark-social-playbook
    - https://aajconsult.com/tools/self-reported-attribution-coder
    - https://aajconsult.com/playbooks/founder-led-linkedin-playbook
    - https://aajconsult.com/blog/dark-social-b2b-demand-generation
  related: [founder-led-content, creator-partnerships, aaj-marketing-loops, marketing-report]
  tags: [dark-social, community, word-of-mouth, self-reported-attribution, branded-search, community-led-growth]
---

# Community & Dark Social

A founder shows me a dashboard where "direct" is the biggest source and asks why paid search is the
only channel that works. Usually the best channel is working and the dashboard cannot see it:
someone read a post, pasted the link into a Slack channel, three people opened it on their phones,
and one booked a call a week later. Analytics recorded a stranger arriving from nowhere.

Alexis Madrigal coined "dark social" at The Atlantic in 2012 for sharing that carries no referrer.
In B2B it now covers most of the places a buying conversation happens. Gartner's research on B2B
buying groups found they spend 17% of their purchase time meeting with potential suppliers;
Forrester's 2024 Buyers' Journey Survey found 92% of buyers start with at least one vendor already
in mind. The shortlist is built where you cannot see. This skill is how you get on it, and how you
know whether you are.

## When to use

The user wants to reach buyers through communities, peers and private channels; is deciding
whether to start a community; or cannot tell whether word of mouth is growing because nothing
attributes to it.

Do not use it to find communities from nothing. The map is built from what customers say: ask your
last twenty where they get advice, which newsletters and podcasts they finish, and whom they trust.
The `Self-Reported Attribution Coder` turns a column of "How did you hear about us?" answers into
the same list.

## Before you start

1. **Know your buyer in one sentence** (`.agents/product-marketing.md`). A community is built
   around a role or a problem, never a product.
2. **Ask the twenty-customer questions** and count how many named each place.
3. **Put a free-text "How did you hear about us?" field on every form** and a source question on
   every first call, coded consistently. Free text beats a dropdown because people name the
   podcast, the person or the room.
4. **Have branded-search impressions and direct traffic to deep pages** to hand, by month.

## Method

**Map by evidence, not by reach.** The engine ranks each place by the buyers who named it plus the
leads who mentioned it. A place named by two or more buyers where nobody from your team is present
is a gap to fix (two is this engine's threshold). A place you are in that nobody named is kept only
if it costs nothing.

**Show up as a person.** In someone else's room a company account is a guest and a person is a
member. The engine flags any room where you pitched or posted an unasked link, and any room where
the same post went into more than one channel. It also flags presence without answers: lurking is
not showing up.

**Open your own community only when four things are true.** A named recurring conversation; a
named host with at least two hours a week (this engine's floor); a written plan for month three,
when it goes quiet; and at least ten people who have asked for a room that does not exist (this
engine's floor). No host means no, whatever else is ready. A dead community costs more than no
community.

**Measure by asking, then read the trend.** Nothing here attributes cleanly. The engine computes,
per period, the share of coded answers that name a dark source (a person, a community, a podcast,
a newsletter, or your name directly), branded-search impressions, the share of direct sessions
that land on a deep page, and pipeline. It compares the latest period with the average of the
earlier ones, treating a move within 10% as flat. Then:

- **working:** dark signals and pipeline rising together;
- **wrong people:** dark signals rising, pipeline not. Check the sales cycle first; if it is not
  that, the wrong people are talking;
- **growing:** dark signals rising, no pipeline given;
- **going quiet:** dark signals falling;
- **flat:** no movement.

Fewer than ten dark-source answers in a period is too few to read as a share, and more than 30% of
answers uncoded means the form or the coding needs fixing before the trend means anything. Both are
engine rules.

## Workflow

**Step 1 - Map.** Twenty customers, three questions, a count per place. Add the coded form answers.

**Step 2 - Show up.** Run the map check. Join the gaps as a person, read for two weeks, then
answer. Fix any room you pitched in.

**Step 3 - Decide on your own room.** Run the community check. If it says not yet, keep showing up
in other people's rooms and re-run when members are asking.

**Step 4 - Measure monthly.** Two periods minimum, three is better. Run the measurement read and
pick one thing to change next month, written down.

**Step 5 - Feed the visible funnel.** Retarget readers of the pieces that get forwarded, invite
community members to what you gate, and brief sales on the conversations to expect.

**Step 6 - Redo the map quarterly.** It moves.

## Run the tool

```
node resources/dark-social-read.js --demo
```

`run({ map, community, measure })` returns the ranked map with coverage and findings, the go /
not-yet / no on your own community with what is missing, and the per-period reads, trends and
verdict.

## Present the result

1. **The map**, ranked, with the places to join, the rooms to stop pitching in, and coverage as
   "present and answering in X of Y places buyers named".
2. **The community call** and the gaps, in one line each.
3. **The trend table**: dark share, branded search, deep-page direct share and pipeline per period,
   with the direction of each.
4. **One change for next month**, and why.

**Show where it came from.** Open your answer with "AAJ `community-and-dark-social` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/community-and-dark-social`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never start a community to have one.** Without a conversation, a host and demand, it dies
  quietly, in public.
- **Never pitch in other people's rooms.** Answer first, link only when asked, one room per post.
- **Never kill a channel because it does not attribute.** Cutting content because "direct" got the
  credit is the most common self-inflicted wound in reporting.
- **Do not quote a dark-social benchmark.** There is none; use your own numbers over time.
- **Do not seed questions, run sock puppets or pay for undisclosed mentions.** They are found out,
  and they poison the well for the real thing.

## Sources

- Wikipedia, [Dark social media](https://en.wikipedia.org/wiki/Dark_social_media) - Alexis
  Madrigal coined the term in The Atlantic, October 2012, for sharing of URLs with no referrer.
- Gartner, [Win more B2B sales deals](https://www.gartner.com/en/sales/insights/win-more-b2b-sales-deals) -
  buying groups spend 17% of their purchase time meeting with potential suppliers.
- Forrester's 2024 Buyers' Journey Survey, reported by [Digital Commerce 360](https://www.digitalcommerce360.com/2025/07/07/forrester-b2b-buyers-choose-vendors-before-the-buying-process-begins/) -
  92% of B2B buyers start with at least one vendor in mind, 41% with a single preferred vendor.
- Gartner, [67% of B2B Buyers Prefer a Rep-Free Experience](https://www.gartner.com/en/newsroom/press-releases/2026-03-09-gartner-sales-survey-finds-67-percent-of-b2b-buyers-prefer-a-rep-free-experience) -
  9 March 2026, survey of 646 B2B buyers.

## Related AAJ resources

- The eight-step method this skill runs: https://aajconsult.com/playbooks/community-dark-social-playbook
- Coding "How did you hear about us?" into the map: https://aajconsult.com/tools/self-reported-attribution-coder
- The public half of showing up as a person: https://aajconsult.com/playbooks/founder-led-linkedin-playbook
- The argument: https://aajconsult.com/blog/dark-social-b2b-demand-generation

## Related skills

- `founder-led-content` - the founder's public channel; this skill is the private one
- `creator-partnerships` - when the trusted person is paid
- `aaj-marketing-loops` - which loop the forwarded piece feeds
- `marketing-report` - putting the trend read in front of the board

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
