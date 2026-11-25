---
name: log-twitter-niche-map-region
description: "A new region of the niche map, then outbound to it. A log play (docs/useCases/twitter/nicheMapRegion.md): The niche map is the owner's network ([networkMaxing.md](networkMaxing.md)). A region is one world added to it, for example the YC 2026 batches (the founders, their companies and the partners around them). The region's people go through the same niche map pipeline as everyone else: three months of who talks to them, everyone scored, bands set, and each person's closeness to the owner (ring 1 engaged with him, ring 2 talks to his followers, ring 3 follows him, ring 4 new). The outbound then goes to ring 2 first, the warmest people who haven't talked to him yet."
when_to_use: "Use when matt asks for this, in words like: \"for getting accepted into YC ... make a new area of the niche map through the systems we've already made ... the YC world and the funds' world, based on the 26 batch\", \"the YC stuff in and around the boat.dev people and the people involved in GTM tools\", \"pull all of my new followers ... set a budget of like 60$\", \"start with the 43\", \"not just treg but the actual index that we did already\"."
metadata:
  summary: "A new region of the niche map, then outbound to it"
---

# A new region of the niche map, then outbound to it

This is the log play `twitter/nicheMapRegion`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/nicheMapRegion" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

The niche map is the owner's network ([networkMaxing.md](../log-twitter-network-maxing/SKILL.md)). A region is one world added to it, for example the YC 2026 batches (the founders, their companies and the partners around them). The region's people go through the same niche map pipeline as everyone else: three months of who talks to them, everyone scored, bands set, and each person's closeness to the owner (ring 1 engaged with him, ring 2 talks to his followers, ring 3 follows him, ring 4 new). The outbound then goes to ring 2 first, the warmest people who haven't talked to him yet.

How the owner asks for it: "for getting accepted into YC ... make a new area of the niche map through the systems we've already made ... the YC world and the funds' world, based on the 26 batch", "the YC stuff in and around the boat.dev people and the people involved in GTM tools", "pull all of my new followers ... set a budget of like 60$", "start with the 43", "not just treg but the actual index that we did already".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/nicheMapRegion.md for <the world>, <the areas>"**. The agent reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md), loads `getGuide({ topic: "xSending" })`, and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | The region's people from a free public source. For YC: every company page of the batches the owner named (founders, their X handles, the company account, the group partner), pulled slowly. YC's team page gives the partners | the niche map repo's `78_yc_batch.py` (`REPOS/whop/research/nicheMap`), YC's public pages | `data/yc/companies.json`, `people.json`, `partners.json` |
| 2 | Keep only the owner's area: the companies whose one-liner, description or tags fit what he named (GTM tools, the agent-infrastructure world around a company like Boat). Hardware, biotech and the rest are out | a filter over the batch files (`data/yc/focus.json`), checked by hand | the region's people (`focusPeople.json`) and the circles to pull (`circles.json`) |
| 3 | Mark who already engages with the owner (his notifications store) and who he already talks to (the inbox), so a warm person never gets a cold template | the account's `notifications.json` and `inboxSync.json` | each person's closeness and engagement |
| 4 | Say the price before the paid run, and run only to the budget the owner set (rule 41). His new followers can go in the same run | the ledger (`data/run_ledger.json`), `GG_BUDGET` | the owner said yes to a number |
| 5 | The region through the niche map pipeline, with the region's circles beside his followers: their three months of mentions, the new people's profiles, scores, own posts, closeness and bands | `run_new_followers.sh` with `GG_CIRCLES_FILE=data/yc/circles.json`. API-heavy pulls go to Boat sandboxes with the owner's [treg](https://treg.to/?ref=matthewdonse-aebsh) login when his machine is under load; the rest reads the cache locally | `data/final_scores.json` holds the region, with rings and bands |
| 6 | The outbound list: the region's go getters (gates passed; band member, collaborator, sponsor or affiliate) in ring 2 first, then ring 2 around them | `data/yc/goGetters.json` | the list, ranked |
| 7 | One recent post of each person's own to open on: the index holds their posts, and one fresh search each confirms they posted this week. Nothing new: they wait | the index (`search_index.json`, `search_posts.jsonl`), treg's posts search | each with a user id and a post from the last few days |
| 8 | Whether they follow the owner and he follows them | `twitterFollows` | the relationship, for the opener's wording |
| 9 | Each opener the cold DM way ([engagerDms.md](../log-twitter-engager-dms/SKILL.md)): their tweet first, then one line about it, never an ask | the agent | one draft per person |
| 10 | Queue them as dms and check them: house style, and nobody he already talks to on X Chat | `twitterQueueBuild` { action: "dm" }, `twitterQueueCheck` | all pending, none dropped or failed |
| 11 | Gate every opener with the voice gate (his writing across all his conversations), rewriting until it passes | `voice` { to, context, text } | every draft passes |
| 12 | Follow, like the post, then the opener, a few people a day, minutes apart (rule 94) | `twitterFollowLive`, `twitterLikeLive`, the queue run | X's answer is `sent` for each |

## What to know

- **The owner names the batches, the areas and the money.** Never add a world, a batch or a source he didn't say (rule 39).
- **The page reads YC slowly,** about one page every 1.5 s, and keeps every page it read in `data/yc/pages`, so a rerun costs nothing.
- **A dropped write is never retried through.** A 429 or a soft block stops the sends, and the next action waits for the owner (rule 94).
