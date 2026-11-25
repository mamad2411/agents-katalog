---
name: log-twitter-notifications
description: "Seeing who engaged with your posts. A log play (docs/useCases/twitter/notifications.md): After a post goes out, people like it, repost it, reply, quote it and follow you. This page pulls all of that from the account's X notifications, new and back through the history, keeps it on this machine, and gives the agent a list of who did what on which post. It sends nothing."
when_to_use: "Use when matt asks for: seeing who engaged with your posts."
metadata:
  summary: "Seeing who engaged with your posts"
---

# Seeing who engaged with your posts

This is the log play `twitter/notifications`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/notifications" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

After a post goes out, people like it, repost it, reply, quote it and follow you. This page pulls all of that from the account's X notifications, new and back through the history, keeps it on this machine, and gives the agent a list of who did what on which post. It sends nothing.

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/notifications.md for <account>"**, or "who liked <post url>", or "who engaged since <date>". The agent then reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | Session check | `twitterSessionCheck` | `loggedIn` |
| 1 | Read what is new | `twitterNotifications` { account } | `notificationSync` says `caughtUp`, or a page cap |
| 2 | The first time only, page back through the history | `twitterNotifications` { account, full: true } | `historyDone`, or run it again later for the rest |
| 3 | Ask what you need from what is kept, calling nothing | `twitterNotifications` { account, stored: true, type, since, post } | the rows, `counts` by kind and `engagers` ranked by how much each person did |
| 4 | Act on who engaged through the page for that job | [engagerDms.md](../log-twitter-engager-dms/SKILL.md), [engagementReplies.md](../log-twitter-engagement-replies/SKILL.md), [networkMaxing.md](../log-twitter-network-maxing/SKILL.md) | that page's own done |

Each row is one person doing one thing: `kind` (like, repost, reply, quote, follow, mention, other), `handle` and `userId`, `followsYou`, which of the account's posts (`postId`, `postUrl`, `postText`), when (`at`), and for a reply or quote their own tweet (`tweetUrl`, `text`). `type` is likes, reposts, replies, quotes, follows or all; `post` takes a post id or url.

## What to know

- **One read, many pages, one session.** The read goes through the account's one X session, its engine host, never a session of its own (rule 105), and is one call on the account, so the queue's sends wait for it and it waits for them (rule 104). Pages are 40 notifications, 4 to 11 s apart, each through the account's governor. A 429 or a governor stop ends the read and keeps what came; nothing reads again until the owner says so (rule 94). Another run sending on the same account shares the same governor.
- **X decides how far back.** `--full` goes on from where the last one stopped, 25 pages a run by default (`pages`), until X gives no more.
- **Aggregated notifications are opened up.** "@a and 12 others liked your post" is kept as one row per person, and the account's own actions are never kept.
- **Kept, not synced anywhere.** The rows live in `~/.logCli/twitter/<account>/notifications.json`, never in Twenty.

## What X shows

X shows the likes on the account's own posts only, never on someone else's.
