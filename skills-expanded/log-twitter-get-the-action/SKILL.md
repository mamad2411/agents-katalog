---
name: log-twitter-get-the-action
description: "Getting people to do the thing: retweet, like, try it. A log play (docs/useCases/twitter/getTheAction.md): The owner needs people to do one action for him: retweet a post, like it, try the tool. This page goes through everyone talking to him, tells him in plain words what each conversation is about, and gets each of them a message that answers what they said and asks for the action. All of it goes out through the account's one queue."
when_to_use: "Use when matt asks for this, in words like: \"get me all them people who liked it ... yo cool to see that you liked that, would you give that a wee retweet\", \"notifications: people who like, comment, reply\", \"go through all the people there who need a message\", \"get them to retweet the thing\", \"would you do me a favour and give it a wee retweet\", \"I need them to retweet it so I can get some inbound leads\", \"I don't know what they're even talking about, explain the context\", \"make them do the action I need\", \"get the full context of everything on the account at the time of sending the message\"."
metadata:
  summary: "Getting people to do the thing: retweet, like, try it"
---

# Getting people to do the thing: retweet, like, try it

This is the log play `twitter/getTheAction`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/getTheAction" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

The owner needs people to do one action for him: retweet a post, like it, try the tool. This page goes through everyone talking to him, tells him in plain words what each conversation is about, and gets each of them a message that answers what they said and asks for the action. All of it goes out through the account's one queue.

The owner should never be blind to a conversation. Before anything is sent, he gets one line per person: who they are, what the conversation is about, and where it's at. Without that line, nothing goes out for that person.

How the owner asks for it: "get me all them people who liked it ... yo cool to see that you liked that, would you give that a wee retweet", "notifications: people who like, comment, reply", "go through all the people there who need a message", "get them to retweet the thing", "would you do me a favour and give it a wee retweet", "I need them to retweet it so I can get some inbound leads", "I don't know what they're even talking about, explain the context", "make them do the action I need", "get the full context of everything on the account at the time of sending the message".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/getTheAction.md"**, with the action and its link (for example: retweet https://x.com/matthewsoldit/status/2116868115028120050). The agent reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md), loads `getGuide({ topic: "xSending" })`, and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Everyone waiting on the owner, plus the people who opened or reacted to his last message | `twitterDms` { account, waiting: true, limit: "200", json: true } | the list, with followUps |
| 1b | Everyone who engaged with the post: who liked it, reposted it, replied or quoted it. Likes are private on X's public API, so the likers come from the account's own notifications; reposters, replies and quotes also come from [treg](https://treg.to/?ref=matthewdonse-aebsh)'s X reads (`/2/tweets/<id>/retweeted_by`, a `conversation_id:<id>` search, `/2/tweets/<id>/quote_tweets`) | `twitterNotifications` { account, type }, treg | every engager, with what they did |
| 2 | Drop the noise: spam, someone pitching their own tool, notification bots, a group the owner didn't start. Say in one line what was dropped and why | the agent | a list of real people |
| 3 | Read each real person's **full context** right now, never from memory or an earlier read: their old DM thread and X Chat merged (read from X, so it includes anything the owner sent them from his phone or outside log), and everything they did on the account's posts (liked, retweeted, replied with what they said, quoted, mentioned, followed), which the same call reads from a fresh notifications pull. One `twitterDms` call at a time, never a burst of reads (rule 104). Someone who already did the action is thanked for it, never asked for it (rule 109) | `twitterDms` { account, with: "<handle>" } | everything they've said and done with the account |
| 4 | **Tell the owner what each conversation is about**: one table row per person with who they are (their work), what the conversation is about (what each side offered or asked), and where it's at (their last message, word for word). Facts from the thread only | the agent, in chat | the owner can see every conversation at a glance |
| 5 | Someone who engaged with the post gets it said back to them and the next small action: liked it, "yo cool to see you liked that, would you give it a wee retweet"; reposted it, "cheers for the retweet, give it a try if you get a minute <the tool's link>"; replied to it, answer the reply then ask. They started it, so the small ask can go in the first message (matt, 2026-11-01): the gate's openerOnly score doesn't hold these back, but every other score must pass. Draft one message per person: first answer what they last said, in a line about them or their work, then the ask in the owner's words ("would you do me a favour and give the video a wee retweet <link>", plus why, "trying to get it in front of the right people"). Every draft reads differently | `voice` { to, with, context } for the owner's lines first | one draft per person |
| 6 | Gate each draft against the same person, and rewrite until it passes. If a draft fails twice for asking too soon (a thin conversation), hold that person and say so in step 4's table | `voice` { to, with, context, text } | the gate passes, or the person is held |
| 7 | Everyone who passed goes into the account's **one** queue as dms, together with anything else that queue is already sending. Never a second queue or run beside it (rule 107), never a loop of single sends (rule 104), never a hand-run command (rule 106) | `twitterQueueAdd` { queue, targets, action: "dm", by: "matt" }, or with no queue going `twitterQueueBuild`, `twitterQueueApprove`, `twitterQueuePlan`, `twitterQueueRunLive` { keepOpen: true } | the run is going, every item planned |
| 7b | Right before each send the queue reads that person's full context again and holds the item (`held`, with what changed) when anything happened since it was drafted. Redraft a held item from the new context, gate it, and put it back with `twitterQueueEdit` (stop the run with `jobCancel` first, then run it again). Never edit the queue file by hand and never send around the queue | `twitterDms` { with }, `voice`, `twitterQueueEdit` { queue, n, text, by: "matt" } | every held item redrafted or dropped |
| 8 | When someone answers, tell the owner what they said; when they've done the action, say so | the inbox hook, `twitterDms` { with } | the owner knows who did it |

## What to know

- **No two asks read alike.** On 2026-11-07, 18 share-asks for /rea-looksmaxxing each ended "just put this out <link> / could you share it its open sourced haha" with only the first line changed: the voice gate reads each one alone, so a "lad" and a "haha" passed them all. A send now repeats nothing the account sent in the last 24 hours, and a queue no item of its own, or it is refused `sameAsSent` (rule 157). Write each ask from that person's thread, in a way that fits them.
- **Load this page before the first send.** It becomes the session's play: every log tool's answer then names the step it is and the next one, and a send as the owner with no play loaded is refused `playMissing` (rule 157). New people who aren't talking to the owner yet aren't this page: they go to [replyGuyFunnel.md](../log-twitter-reply-guy-funnel/SKILL.md) (reply to their post first, then the opener, then the ask).
- **Read the threads from the .db,** never by fanning out reads to X: the conversation store and `~/.logCli/log.db` already hold every thread, and the inbox hook says how fresh it is (rule 136). On 2026-11-07 a helper read 22 threads from X one by one and added about 24 requests to the account for nothing.
- **When the queue's send-time gate holds every short ask,** the owner's "send it" is `twitterDmLive` with `overGate` for each message, one at a time and a minute or two apart; `sameAsSent` still applies (rules 152, 157).
- **A meme can carry the nudge.** For someone who said they'd do it and went quiet ("bet will do"), a [Memelord](https://www.memelord.com/sign-up?ref=kfwut9wc) meme that fits the moment goes on the first message as an image (`twitterDmLive` { media: "<meme url>" }), then the nudge in the owner's words: 2026-11-02, @gabesweats got Waiting Skeleton with "me waiting on your bug report / you break it yet lad". Find it with `memelordSearch`, gate the text with `voice` as always.
- **At the cap, only the owner can lift it.** `force: true` on the read and the send goes past the governor for that call when the owner says so (rule 86); the governor still counts each request.

- **The owner's ask is the point.** Don't drop it to make a message softer. Put it after a line that answers them, so it reads like a mate asking a favour.
- **Full context at the time of sending, every time.** What someone did a minute ago changes what you say: they liked it, retweeted it, replied, or the owner messaged them from his phone. Read it with `twitterDms` { with } before drafting, and the queue reads it again before each send and holds anything that changed (rule 109).
- **The context line comes first, every time.** The owner has said he doesn't know what half the conversations are about. Step 4's table is what he reads, so keep it plain and short.
- A meeting, a deal or a promise is never made for the owner here. If someone asks for one, say it in step 4 and leave it to him.
- Use only facts from the thread. Never invent where a deal is up to.
- The link goes in as a plain URL. Every line of a draft is one message (rule 90).
- Everything is sent through the account's one X session (rule 105), and the answer's `xSession` names it.
