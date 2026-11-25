---
name: sr-engage
description: Handles the replies, comments, DMs and outreach that happen after a post goes up. Drafts replies in the creator's voice for them to post, sorts comments into questions, praise, critique and spam, turns repeat questions into content ideas, plans a small daily engagement block, and handles criticism and trolls calmly. Use when someone asks how to reply to comments, grow through engagement, handle a hater, build community, or what to do in the first hour after posting. Drafts only. Nothing is sent or posted by Showrunner.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the humanizer; the method works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Engage

Posting is half the job. The other half is talking to the people who show up. Done well it builds the audience and gives you your next ten ideas.

## Ask first

- Which platform, and what is the post or comment thread?
- How much time per day they can give (the calendar holds back 15% of weekly hours for this).
- Their voice notes (`sr-voice`) and any phrases they never use.
- Whether the comments they want help with are friendly, confused, critical or abusive.

## Plan a small block

Pick a fixed 20 to 30 minute block, once or twice a day, for the first days after a post. In it:

1. Reply to every real question. A reply that adds one useful fact or example is worth more than a thank-you.
2. Reply to people who add something, and ask a follow-up if it moves the topic forward.
3. Pin or highlight the best comment if the platform allows it.
4. Note repeated questions. Each one is a content idea (`sr-ideas`).
5. Leave other people's posts one thoughtful comment where your audience gathers.

## Draft replies

Sort comments first:

| Type | Reply approach |
|---|---|
| Question | Answer directly in one or two lines. If it is big, say a video is coming |
| Praise | Short, specific thanks. Ask what they will try |
| Critique with a point | Thank them, agree where right, add your view, no defensiveness |
| Disagreement | Calm, one fact, one question. You do not have to win |
| Spam or abuse | Hide, delete or block. Do not engage |

Draft the replies in the person's voice. Run longer ones through `text_humanize` (`sr-humanize`). Give the person every draft to edit and send. **Showrunner never posts or sends.**

## What the platform signals say (and what they do not)

Instagram's Mosseri named watch time, likes per reach and sends per reach as top signals for video (reported, `instagram.signals.top_three`), which is one reason to ask people to send a post to someone it would help. For X, secondary reports of the published ranking code say replies and quotes are weighted far above likes, and that reports, mutes and blocks count heavily against a post (`x.ranking.open_source`). Weights are not facts about your account, and none of this is a license to bait replies. Write replies that are worth reading.

## Turn comments into content

Collect the questions. Group them. Each group becomes a short video, a carousel or a thread. Quote the question (with permission if it names a person) and answer it better than before.

## Handling a troll or a storm

Do not argue in public. Reply once if there is a real point, then stop. Use mute, restrict, hide and block. Screenshot threats. If it is about safety, use the platform's reporting tools.

## Gate

`human`. Every reply is the person's to send.

## Do not

- Buy comments, run engagement pods, or use auto-replies that pretend to be personal. They break platform rules and the audience can tell.
- Reply to every comment with the same sentence.
- Tag strangers into threads for reach.
