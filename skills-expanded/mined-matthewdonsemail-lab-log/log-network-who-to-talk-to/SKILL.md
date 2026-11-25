---
name: log-network-who-to-talk-to
description: "Who to talk to next. A log play (docs/useCases/network/whoToTalkTo.md): Your network is everyone around your own accounts, each in a ring kept live from what the watchers store: 1 engaged with you (a one-to-one chat counts, a group doesn't), 2 talks to your followers or ring-1 people, 3 follows you, 4 known. Rings are per person: accounts the owner linked (`log people link`) count once, at their closest ring, with every account and the platform each tie came from. Ask for one platform alone or all of them. It needs no research files. An imported research folder adds each person's band (what they could be to you), fit and the leaders whose circles they are in. One query answers who to talk to next: the people one step from you whom you haven't talked to yet, ring 2 first. Each comes with why: their ring and its reason, the circles, who already connects you, and their last post. The ones y"
when_to_use: "Use when the owner asks for this, in words like: \"who in my network should I talk to\", \"who's in my network\", \"who do I need to speak to\"."
metadata:
  summary: "Who to talk to next"
---

# Who to talk to next

This is the log play `network/whoToTalkTo`. Before anything else, call the log MCP tool `getGuide({ useCase: "network/whoToTalkTo" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Your network is everyone around your own accounts, each in a ring kept live from what the watchers store: 1 engaged with you (a one-to-one chat counts, a group doesn't), 2 talks to your followers or ring-1 people, 3 follows you, 4 known. Rings are per person: accounts the owner linked (`log people link`) count once, at their closest ring, with every account and the platform each tie came from. Ask for one platform alone or all of them. It needs no research files. An imported research folder adds each person's band (what they could be to you), fit and the leaders whose circles they are in. One query answers who to talk to next: the people one step from you whom you haven't talked to yet, ring 2 first. Each comes with why: their ring and its reason, the circles, who already connects you, and their last post. The ones you pick go to the first-DM steps of [networkMaxing.md](../log-twitter-network-maxing/SKILL.md).

How the owner asks for it: "who in my network should I talk to", "who's in my network", "who do I need to speak to".

## Run it from a fresh context

Say: **"go on docs/useCases/network/whoToTalkTo.md"**. The agent reads this page and runs the steps. Nothing is sent until step 5, and then only after the owner's yes for each person.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | How many people sit in each ring, live, per platform and combined, who is linked across platforms and who is only suggested. Add `platform` when the owner names one | `networkStatus` { platform } | the ring counts, and whether a research folder was imported |
| 2 | Only when the owner has a research folder that is new or changed: read it into log.db (replaces the last import, local only), then rebuild the graph and verify it (see below) | `networkImport` { from } | its counts, and verify says the graph holds what log.db derives |
| 3 | Ask the graph for the ranked list, with the query below as is, and the same `platform` as step 1 if any | `relateQuery` { cypher, platform } | up to 25 rows, ring 2 first |
| 4 | Show each person and why: their ring, its reason (`why`) and the platform it came from (`tieFrom`), their linked accounts (`accounts`), their band when imported, the leaders whose circles they are in, who in those circles already chats with you (`sameCircleTalksToYou`) and who mentioned them (`mentionedBy`), and their last post. The owner picks who | the agent | the owner's picks |
| 5 | For each pick, the first-DM steps of [networkMaxing.md](../log-twitter-network-maxing/SKILL.md) (steps 7 to 11): follow, like the post, then the opener, gated by the voice gate, each send only after the owner says yes | networkMaxing's steps 7 to 11 | X's answer is `sent` for each |

### The query

Everyone in rings 1 to 3, plus imported people, merged with your chat identities by X handle. A linked person shows once, at their closest ring; with `platform`, only that platform's accounts and rings. Imported people need band `collaborator` or `member` and the research's gates; anyone you already have a DM with, on any linked account, is left out. They are ranked ring 2 first, then 1, 3 and 4, then shared circles, fit and recency of their last post:

```cypher
MATCH (i:Identity) WHERE NOT i.owner AND (i.inNetwork OR i.ring < 4) AND ($platform = '' OR i.platform = $platform) AND coalesce(i.passesGates, true) AND (i.band IS NULL OR i.band IN ['collaborator', 'member']) AND NOT (i)-[:SAID|MEMBER_OF]->(:Room {kind: 'dm'}) OPTIONAL MATCH (i)-[:LINKED_TO]->(p:Person) WITH i, p WHERE p IS NULL OR (NOT coalesce(p.dm, false) AND ($platform <> '' OR p.lead = i.key)) WITH i, p, CASE WHEN p IS NULL OR $platform <> '' THEN i.ring ELSE p.ring END AS ring OPTIONAL MATCH (i)-[:IN_CIRCLE_OF]->(l:Leader) WITH i, p, ring, count(DISTINCT l) AS circles, collect(DISTINCT l.handle)[0..5] AS leaders ORDER BY CASE ring WHEN 2 THEN 0 WHEN 1 THEN 1 WHEN 3 THEN 2 ELSE 3 END, circles DESC, coalesce(i.fit, 0) DESC, coalesce(i.lastPostAtMs, 0) DESC LIMIT 25 OPTIONAL MATCH (i)-[:IN_CIRCLE_OF]->(:Leader)<-[:IN_CIRCLE_OF]-(c:Identity)-[:SAID]->(:Room {kind: 'dm'}) WITH i, p, ring, circles, leaders, collect(DISTINCT c.handle)[0..3] AS sameCircleTalksToYou OPTIONAL MATCH (m:Identity)-[:MENTIONED]->(i) WITH i, p, ring, circles, leaders, sameCircleTalksToYou, collect(DISTINCT m.handle)[0..3] AS mentionedBy RETURN coalesce(p.name, i.handle) AS who, i.handle AS handle, i.platform AS platform, ring, CASE WHEN p IS NULL OR $platform <> '' THEN i.ringReason ELSE p.ringReason END AS why, CASE WHEN p IS NULL OR $platform <> '' THEN i.platform ELSE p.ringPlatform END AS tieFrom, p.accounts AS accounts, i.band AS band, circles, leaders, sameCircleTalksToYou, mentionedBy, i.fit AS fit, i.themes AS themes, i.followsOwner AS followsYou, i.lastPost AS lastPost, i.lastPostAtMs AS lastPostAtMs ORDER BY CASE ring WHEN 2 THEN 0 WHEN 1 THEN 1 WHEN 3 THEN 2 ELSE 3 END, circles DESC, coalesce(fit, 0) DESC, coalesce(lastPostAtMs, 0) DESC
```

## What to know

- **The graph after an import:** `relateBuild` {} projects log.db, your network included, into a new graph file, and `relateVerify` {} checks every count against log.db.

- **Rings:** 1 engaged with you (like, reply, quote, repost, mention, a one-to-one DM from them), 2 replies to or names your followers or ring-1 people (a ring-1 person's linked account counts too), 3 follows you, 4 known. A chat with more than two members is a group, on every platform. They move as each event is stored, so the graph has them within a second while the graph owner runs. Ring 2 comes first because one introduction reaches them.
- **The graph owner keeps it current:** `relateStatus {}` says how far behind log.db the graph is; when its owner isn't running, `relateStatus { owner: start }` starts it, and `relateStatus { owner: stop }` stops it only when the owner asks.
- **Bands:** `member` could buy, `collaborator` could make things with you; `sponsor`, `affiliate`, `amplifier`, `audience` and `skip` are left out of this query.
- **Suggested, not linked:** pairs `networkStatus` lists as suggested are counted as separate people until the owner says yes to `peopleLink`; never treat them as one.
- **Why, not just who:** never pitch from the band. The opener is about them and their last post, as in networkMaxing.
- A person in `sameCircleTalksToYou` already chats with you and shares a circle with them: ask the owner whether to ask that person for an intro instead of a cold opener.
- New conversations reach the graph on its next update, so the people now in a chat drop out of the list by themselves; `relateBuild` forces a full build.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [The Relate graph](https://github.com/matthewdonsemail-lab/log/blob/main/docs/relateGraph.md)
- [Network maxing](../log-twitter-network-maxing/SKILL.md)
