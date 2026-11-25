---
name: log-twitter-who-needs-you
description: "Finding who needs something from you, or who matters. A log play (docs/useCases/twitter/whoNeedsYou.md): Go through the account's messages and find the people who clearly need something from the owner, or who matter: someone asking for work, a collaboration, a referral, a call; someone well placed (a fund, a big audience, a shared network). It reads what each conversation is about across its whole history, not just the last line, and says how close each one is to money. It sends nothing. What happens next with each person is the owner's call, and the reply itself is [followUps.md](followUps.md)."
when_to_use: "Use when matt asks for this, in words like: \"look through my messages and find someone who clearly needs something off me\", \"summarise everything on my twitter, how likely is it we make money\", \"who's worth following up\"."
metadata:
  summary: "Finding who needs something from you, or who matters"
---

# Finding who needs something from you, or who matters

This is the log play `twitter/whoNeedsYou`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/whoNeedsYou" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Go through the account's messages and find the people who clearly need something from the owner, or who matter: someone asking for work, a collaboration, a referral, a call; someone well placed (a fund, a big audience, a shared network). It reads what each conversation is about across its whole history, not just the last line, and says how close each one is to money. It sends nothing. What happens next with each person is the owner's call, and the reply itself is [followUps.md](../log-twitter-follow-ups/SKILL.md).

How the owner asks for it: "look through my messages and find someone who clearly needs something off me", "summarise everything on my twitter, how likely is it we make money", "who's worth following up".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/whoNeedsYou.md"**, and which account. The agent reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md), loads `getGuide({ topic: "xInbox" })`, and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Who wrote last and is waiting: already in context at session start, read from the local inbox store, nothing fetched | the SessionStart hook | the list is in context |
| 2 | Bring the inbox up to date: the first read takes everything once, every read after only what is new (about 5 s) | `twitterDms` { account, limit: "60" } | every conversation, newest first, with who spoke last |
| 3 | Shortlist: everyone waiting on the owner, plus anyone recent the owner wrote to who answered | `twitterDms` { account, waiting: true, limit: "60" } | a shortlist of handles |
| 4 | Read each shortlisted person in full, old DM thread and X Chat merged, one person at a time | `twitterDms` { account, with: "<handle>" } | their whole thread, oldest first |
| 5 | What the conversation is about beyond the thread: earlier talk about the same thing anywhere | `search` { query, with: "<handle>" } | the matches, with when |
| 6 | Who they are: their bio, role and reach, and whether they're in Twenty | [treg](https://treg.to/?ref=matthewdonse-aebsh)'s X profile read, Twenty | one line per person |
| 7 | Sort them, each with the line that shows it and its time: **needs something from you** (asked for work, a call, help, an answer), **matters** (role, reach, where they could take you), **money** (a concrete need the owner sells, a budget, a referral), **warm** (friendly, nothing asked yet), **no action** (pitches at the owner, spam) | a table for the owner | every person has a row and a suggested next move |
| 8 | The owner says what to do with each one, in their own words | the owner | one instruction per person, then [followUps.md](../log-twitter-follow-ups/SKILL.md) |

## What to know

- Read before judging: the last message alone is a label, not an answer. Quote the line that shows the need and its time ("asked for a call, 29 Oct 21:08").
- Someone pitching the owner (selling ads, a service) is not a buyer. Say so.
- "(could not decrypt)" means X Chat couldn't be opened for that message, not that the person said nothing. Never say "nobody replied" from it.
- Reads go one person at a time. Never read the whole inbox in a loop of calls, and never in the same session as a bulk send (rule 94).
- How likely money is gets said plainly, from what was said. Nothing is inferred that the person didn't say.
