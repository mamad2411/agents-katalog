---
name: log-discord-cold-outbound
description: "First DMs from a Discord channel. A log play (docs/useCases/discord/coldOutbound.md): Start a conversation with someone the owner met in a server channel: someone who replied to him, argued with him or asked him something there. log opens the DM the way the app's Message button does and sends one message, gated like any other. When Discord won't let a stranger message them, log sends a friend request instead, and the message waits until they accept."
when_to_use: "Use when the owner asks for this, in words like: \"dm the people from <channel>\""
metadata:
  summary: "First DMs from a Discord channel"
---

# First DMs from a Discord channel

This is the log play `discord/coldOutbound`. Before anything else, call the log MCP tool `getGuide({ useCase: "discord/coldOutbound" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Start a conversation with someone the owner met in a server channel: someone who replied to him, argued with him or asked him something there. log opens the DM the way the app's Message button does and sends one message, gated like any other. When Discord won't let a stranger message them, log sends a friend request instead, and the message waits until they accept.

How the owner asks for it: "dm the people from <channel>"

## Run it from a fresh context

Say: **"go on docs/useCases/discord/coldOutbound.md for <channel>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Read the channel and list who replied to the owner, mentioned him, or was answered by him, each with their `fromId` | `discordRead` { account, channel: "<channel id>", limit: 50, noMedia: true } | a list of people with their user ids and what each said to him |
| 2 | Show the owner the list and leave out anyone he names (moderators, people he's fallen out with) | the agent, from the list | the owner says who to message |
| 3 | Pull how the owner writes to people he has just met | `voice` { to: "<name>", context: "<what they said in the channel>" } | his real openers |
| 4 | Write one message per person, from what that person said in the channel, and gate it | `voice` { to: "<name>", context: "<what they said>", text: "<draft>" } | `PASS` |
| 5 | Send it, opening the DM by their user id | `discordSendLive` { account, userId: "<fromId>", text: "<draft>", approvedBy: "<owner>", confirmLive: true } | Discord answers `sent` with the message id |
| 6 | Before a friend request, show who it goes to; this contacts nothing | `discordFriend` { account, userId: ["<fromId>"] } | the dry run lists each user id |
| 7 | When the send is refused because Discord won't open a DM with a stranger, send a friend request | `discordFriendLive` { account, userId: ["<fromId>"], approvedBy: "<owner>", confirmLive: true } | Discord answers `sent`, or `captchaRequired` for the owner to send from the app |

## What the runs taught

- **One person at a time, a minute or more apart.** Several DMs and friend requests to people who share one server, in a few minutes, is what Discord reads as spam. The friend requests go 20 s apart and the first refusal stops the run (rule 94).
- **A message about what they said, never a pitch.** The opener answers their point in the channel; the project comes up only when it fits.
- **A moderator who has warned the owner is left out.** They can remove him from the server.

## Related

- Up: [use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Replying in a Discord server channel](../log-discord-server-reply/SKILL.md)
- [Answering someone in a Discord DM or group DM](../log-discord-channel-reply/SKILL.md)
- [Finding a conversation in a Discord server](../log-discord-server-search/SKILL.md)
