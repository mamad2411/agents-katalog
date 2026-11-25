---
name: log-twitter-reply-guy-funnel
description: "Reply guy, then the DM, then the ask. A log play (docs/useCases/twitter/replyGuyFunnel.md): The owner's way of getting new people to do something for him (share a post, try a tool): like a run of their posts, reply to them in public, then open a DM on their own post, build on what they say, and only then the ask. In his words: \"you're meant to reply guy them first and foremost. You go on, like a tweet, send a meme to the tweet, and then we're gonna forward the tweet to them as an opener, talking and building on top of it, and then you wait for the reply, and then you say something that's in context that then build on top of the conversation that then funnel them into doing an action.\""
when_to_use: "Use when matt asks for this, in words like: \"reply guy them first and foremost\", \"send a meme to the tweet then forward the tweet to them as an opener\", \"message the people who are new to following me\", \"get it in front of them\", \"funnel them into doing an action\"."
metadata:
  summary: "Reply guy, then the DM, then the ask"
---

# Reply guy, then the DM, then the ask

This is the log play `twitter/replyGuyFunnel`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/replyGuyFunnel" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

The owner's way of getting new people to do something for him (share a post, try a tool): like a run of their posts, reply to them in public, then open a DM on their own post, build on what they say, and only then the ask. In his words: "you're meant to reply guy them first and foremost. You go on, like a tweet, send a meme to the tweet, and then we're gonna forward the tweet to them as an opener, talking and building on top of it, and then you wait for the reply, and then you say something that's in context that then build on top of the conversation that then funnel them into doing an action."

It is [managerMaxxing.md](../log-twitter-manager-maxxing/SKILL.md)'s touches for anyone: new followers, people who engaged, or a list the owner names. People already talking to the owner skip the first touches and go to [getTheAction.md](../log-twitter-get-the-action/SKILL.md).

How the owner asks for it: "reply guy them first and foremost", "send a meme to the tweet then forward the tweet to them as an opener", "message the people who are new to following me", "get it in front of them", "funnel them into doing an action".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/replyGuyFunnel.md for <who> and <the action>"** (for example: the new followers, share https://x.com/matthewsoldit/status/2118876082409725989). The agent reads this page, [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) and [networkMaxing.md](../log-twitter-network-maxing/SKILL.md), loads `getGuide({ topic: "xSending" })` and `getGuide({ topic: "extensions" })`, and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Who: the new followers from the account's notifications, or the people the owner names. Drop anyone already talking to the owner (they go to getTheAction), anyone over 1500 followers (rule 121), the owner's own accounts and anyone the agent memory says never to message | `twitterNotifications` { account }, `twitterDms` { account, with } | a list of new people, each with their user id |
| 2 | Each person's recent original posts, newest first, the ones with a picture or video marked. Someone with no post from the last month has nothing to reply to: hold them and say so | [treg](https://treg.to/?ref=matthewdonse-aebsh) `treg.x.user.posts` { username } | one post per person worth replying to and up to 6 to like, or held |
| 3 | The like run, timed the way @aymanemsi's was: like 3 to 6 of their recent posts, the picture and video posts first, at random gaps of 4 to 60 seconds, the whole run inside 5 minutes and never two at the same gap (rule 94). Follow them a few seconds before the last like. Their notifications fill with the owner's name before the reply lands. The post the reply is on isn't in the run: the reply likes it itself (rule 121) | `twitterLike` { account, tweetUrl }, `twitterLikeLive`, `twitterFollowLive` | each like answered `liked` by X, or the run stopped on a refusal |
| 4 | A reply about their post, with a meme picked to the owner's taste for that moment and uploaded as media. Each reply is about that post alone, so no two read alike (rule 157). Gate every one | `memelordSearch`, `voice` { to, context, text } | every reply passes, and none repeats another |
| 5 | The replies go into the account's one queue, a few minutes apart, each liking the post and following them first (rules 104, 107, 121) | `twitterQueueBuild` { action: "reply" }, `twitterQueueCheck`, `twitterQueueApprove`, `twitterQueuePlan`, `twitterQueueRunLive` | X answers `sent` for each reply |
| 6 | Once a person's reply has landed, the DM: that same post of theirs forwarded first, then one line that builds on it and on the reply. The opener only, never the ask (rule 98), written from their post so no two read alike | `voice` { to, context, text }, `twitterQueueAdd` { action: "dm" } | each opener passes and goes into the same queue |
| 7 | Wait for them to answer. The inbox hook brings each answer in the moment it lands; read their whole thread then | `twitterDms` { account, with } | they answered, or they haven't yet |
| 8 | Answer what they said, in the owner's words for them, building on it: about them and what they're doing, still no ask | `voice` { to, with, context, text }, `twitterDmLive` | the conversation is going |
| 9 | Once they're talking, the ask in context: the action the owner wants (share the post, try the tool), in a way that fits what they said, with the link | `voice` { to, with, context, text }, `twitterDmLive` | they did it, or the owner knows where it stands |

## The like run, from @aymanemsi

On 2026-11-08 @aymanemsi liked a run of the owner's posts. The owner opened the chat with "i think you nearlly blew my phone up lad", and he answered "I like spam liking lol". They were talking within the minute. The owner then had the chat distilled into this page: a person who sees the same name across their notifications looks at who it is, so the reply and the DM that follow land on someone who already knows the name.

- **Their posts with a picture or video first.** The owner: random intervals "would be good for the media based content the most". A like on a post they made something for gets noticed more than one on a text post.
- **His timing, guessed from what X shows.** X bundled his likes into one notification ("Aymane liked 5 of your posts") with one time, so each gap isn't known. What is known: the owner's notification count was 0 at 00:50:27 his time, Aymane followed at 00:55:02, and his last like landed at 00:55:07. So 5 likes and a follow inside 5 minutes, the last like 5 seconds after the follow. The run copies that shape: random gaps of 4 to 60 seconds, all inside 5 minutes, the follow just before the last like.
- **Random gaps, never a burst.** Each gap is drawn fresh, never under the governor's 4 s floor and never two the same: likes fired back to back are what X reads as automation and what rule 94 forbids. Each like and the follow is a write the governor counts.
- **Then the reply.** It comes after the last like, on a post that wasn't liked in the run (the reply likes its own post, rule 121).

## As a state machine (outlined, not built yet)

Each person is one run of a machine in the account's one queue (rules 104, 107). The queue gains a `like` action, and the run picks a new random gap before every like.

```mermaid
stateDiagram-v2
  [*] --> picking
  picking --> held: no post in the last month
  picking --> liking: posts found, media first
  liking --> waiting: liked
  waiting --> liking: random gap of 4 to 60 s, likes left
  waiting --> following: one like left
  following --> liking: a few seconds later
  waiting --> replying: run of 3 to 6 done, inside 5 min
  liking --> stopped: X refused
  replying --> opener: reply sent
  replying --> stopped: X refused
  opener --> listening: opener sent
  listening --> talking: they answered
  talking --> asking: the conversation is going
  asking --> [*]
  held --> [*]
  stopped --> [*]
```

- **picking:** their recent original posts from treg, the picture and video posts first, 3 to 6 to like and one to reply to. With no post from the last month the person is held.
- **liking:** one like through the account's one session. X's answer decides (rule 73). A refusal stops the whole queue and waits for the owner (rule 94).
- **waiting:** a random gap of 4 to 60 seconds, drawn fresh each time, never below the governor's 4 s floor, with the whole run kept inside 5 minutes.
- **following:** before the last like, the follow, then the last like a few seconds later, as Aymane did. The account's one session is held for the run, so no other person's item goes out in the middle of it.
- **replying, opener, listening, talking, asking:** steps 4 to 9 above, unchanged.
- **Held items:** if they message the owner or answer anything mid-run, the run stops liking and the queue holds the next item (rule 109).

## What to know

- **Never skip the reply.** A cold DM with the ask in it to someone who just followed is what X reads as automation, and what the owner never wants. The reply comes first, the opener second, the ask last.
- **No two messages alike.** A reply, opener or ask that repeats another one the account sent in the last 24 hours is refused with `sameAsSent` (rule 157). A template with a different first line is still a template.
- **One play at a time.** Loading this page makes it the session's play, and every log tool's answer says which step it is and what comes next (rule 157).
- Every send counts against the account's writes for the day, and X's own daily limit (344) can come at around 40; spread the people over days. Any refusal stops the run (rule 94).
