---
name: review-post
description: |
  Use when one of user's already-published LinkedIn posts notably
  outperformed or underperformed their median, they want to understand a
  single post in depth before writing a follow-up, or learn from a
  specific recent post. Trigger phrases include "review this post," "why
  did this post flop," "why did this post do so well," "what should I do
  differently next time," "do a postmortem on this post." Per-post
  counterpart to analyze-performance.
license: MIT
---

# Review post

A single post's performance is too noisy to draw firm conclusions from. But a careful read of one post against its data can still surface useful signals: a hook that under-promised, a body that lost the reader at a specific paragraph, a close that asked for the wrong thing, a publication time that missed the user's audience. This skill exists to do that read carefully on one post, in a way that produces something the user can act on the next time they write about a similar angle.

## Why this skill exists

The instinct after a post performs well is to do exactly the same thing again, which works once and then stops working. The instinct after a post flops is to abandon the topic, which often abandons a good idea before it had a fair chance. Both reactions are wrong. The right move is to read the specific post carefully, identify the variables that mattered, and try the same angle with the variables adjusted.

This skill is also where you protect the user from over-learning from one data point. A post can flop because of timing, the day's news, an algorithmic blip, or just the audience not being online. The review should name what we cannot conclude as clearly as what we can.

## When to use this skill

Trigger when:
- One of the user's recent posts significantly outperformed their median
- One of the user's recent posts notably underperformed
- The user wants to understand a specific post before writing a follow-up
- The user is preparing a similar post and wants to learn from a past one
- The user pastes a post and the metrics and asks "what happened here"

Do NOT trigger when:
- The user wants a cross-post pattern analysis. Send to analyze-performance.
- The post just went live and there is not enough data yet (give it at least 48 hours, ideally 5-7 days).

## What you need from the user

1. **The post itself.** Full text, plus the format (text, carousel, video, article). For carousels, ideally the slide-by-slide copy.
2. **The metrics.** Impressions, engagement rate, reactions, comments, shares, dwell time if available, click rate on any link, follower growth from the post.
3. **Context for the post.**
    - When it was published (day, rough time)
    - Whether it was part of a content pillar (if plan-content was run)
    - Whether the user pushed it via DMs to peers or it grew on its own
    - Any unusual circumstances (news cycle, weekend, holiday, time off)
4. **The user's intuition.** Ask: "Before I look at this, what is your gut sense of what worked or did not?" Their intuition is often right, and the review either confirms or challenges it.

If voice-profile.md, content-plan.md, or recent analyze-performance output exist, read them. They provide useful context for what is normal for this user.

## What the review looks at

Walk the post in order. For each section, ask what its job was and whether it did it.

### The hook (first 210 characters)

Did the hook earn the click? Two signals:
- **Expand rate.** If LinkedIn shows it, this is the most direct read. Above the user's median means the hook worked.
- **Impressions vs engagement.** A post with high impressions and low engagement often has a hook that under-promised what the body delivered. Low impressions and high engagement-per-impression suggests the hook attracted the right people but not many of them.

Then read the hook itself. Specific or generic? Curiosity gap or summary? Confession, contrarian claim, specific number, story setup, or one of the failure patterns?

### The body

If you have dwell time data, this is where it shows up. Otherwise, look at comment quality: did the commenters engage with the substance of the post, or with the hook? Comments that respond to the hook ("Love this!") suggest the body did not hold them. Comments that respond to specific points in the body suggest it did.

Read the body itself. Where might a reader have dropped off? A generic paragraph, a confusing turn, an unearned claim, a sudden register change. The user will often know.

### The close

Did the close earn comments? An honest question that the user actually wanted answered tends to drive a particular kind of comment (specific answers). A closer that just stops can drive comments too if the post lands hard. A "thoughts?" closer or a CTA tends to drive few comments and the wrong kind.

### Format

For carousels: which slides got swipe-throughs vs drops? LinkedIn shows aggregate document performance. For video: was the watch-time average above 50% of the video length? Below that suggests the first 10 seconds did not hold.

### Timing and audience

Was the post published when the user's audience is on LinkedIn? Most B2B audiences engage 7-10am and 12-2pm in their local time, Tuesday through Thursday. A post on Friday afternoon performs differently than the same post on Tuesday morning, often by 2-3x.

Was the audience the right one? If the user has 5,000 followers but only 200 are the actual target audience, the engagement-rate-on-target-audience matters more than overall engagement rate.

### What we cannot conclude

End every review with this. Common things we cannot conclude from one post:
- Whether the topic is "right" for this audience (need more posts on the same topic)
- Whether the user should post more or less often (cadence questions need 4+ weeks of data)
- Whether the format is the right one (need to try the same angle in another format)
- Whether the user's voice is working (voice questions are systemic, not per-post)

## Output format

```
# Post review: [post title or hook excerpt]

Published: [date]
Format: [text / carousel / video / article]
Result vs user's median: [X% above/below]

## What worked

- [Specific element that worked, with the evidence that supports it]
- ...

## What did not work

- [Specific element that did not work, with the evidence]
- ...

## Where the post likely lost or gained readers

[A walk through the post pointing at specific paragraphs or slides]

## Three lessons for next time on a similar angle

1. [Specific, actionable. "Open with the specific number from paragraph 3 instead of the generic question." Not "Improve the hook."]
2. ...
3. ...

## What I cannot conclude from this one post

[Honest list of what the data cannot tell us]

## Suggested next step

[Either: "Write the next post on this angle with the changes above" / "Wait for 2-3 more posts on this topic before changing your approach" / specific other guidance]
```

## Example

User pastes a post:
> "I shipped a feature last week and I'm not sure about it. Here are 5 lessons from shipping under uncertainty..."

Metrics:
- 4,200 impressions (user's median is 6,000)
- 1.1% engagement rate (user's median is 2.4%)
- 8 reactions, 0 comments, 1 share
- No dwell time data
- Published Friday 5pm local

User's intuition: "I think the hook didn't work but I'm not sure why."

Output:

```
# Post review: "I shipped a feature last week and I'm not sure about it..."

Published: Friday 5pm local
Format: text
Result vs user's median: 30% below on impressions, 54% below on engagement rate

## What worked

- The first half of the hook ("I shipped a feature last week and I'm not sure about it") is a confession that opens a real curiosity gap. The user's pattern from voice-profile.md confirms confessional opens have worked before.

## What did not work

- The second half of the hook ("Here are 5 lessons from shipping under uncertainty") collapses the curiosity gap immediately. The reader now knows the post is a list of 5 lessons and has to choose whether they want to read them. Most don't.
- "5 lessons" framing is one of the patterns LinkedIn's AI-slop detection now downranks. Posts framed as numbered lessons or "X things I learned" have seen reach drops since the LinkedIn slop crackdown launched.
- Friday 5pm local is the second-worst publish time for B2B content (only Saturday morning is worse). Even a strong post loses about half its reach at this time.
- Zero comments is the most telling number. The post did not give readers anything specific to respond to.

## Where the post likely lost readers

The first 150 characters of the hook would have worked. The next 60 characters ("Here are 5 lessons...") is where readers decided not to expand. The body itself was probably read by people who did expand, but the expand rate was low to begin with.

## Three lessons for next time on a similar angle

1. End the hook on the confession. "I shipped a feature last week and I'm not sure about it." Period. Then let the body deliver the substance. Do not pre-announce the structure.
2. Replace the "5 lessons" framing with the actual specific thing that made you uncertain. Specifics outperform list-frames now.
3. If this topic is worth writing about, publish Tuesday or Wednesday morning. Friday 5pm gives up half your reach before you start.

## What I cannot conclude from this one post

- Whether this topic does not work for your audience. One post on uncertainty in shipping is not enough; the framing was the problem more than the topic.
- Whether you should stop using confessional hooks. The confessional opener was the strongest part of this post.
- Whether your engagement is trending down generally. For that, run analyze-performance across the last 8-12 weeks.

## Suggested next step

Rewrite this post with a confessional hook that lands, drop the list framing, publish Tuesday morning. If that version also flops, then the topic is the question, not the framing.
```

## A note on the user's emotional reaction

A flopped post is uncomfortable. The user may have spent real effort on it. The review should be honest but not punitive. A few rules:

- Lead with what worked, even if the post overall did not. Most flopped posts have at least one element that worked; calling it out matters.
- Frame "did not work" as specific and fixable, not as judgment of the user.
- If the user disagrees with the diagnosis, do not double down. Acknowledge the alternative read and offer to test it on the next post.
- Do not pile on. One review per post. The user gets one diagnosis and then they get to keep posting.

## What this skill does not do

- Predict whether the rewritten version will perform better. The review surfaces hypotheses; the next post tests them.
- Diagnose systemic issues from one post. Voice problems, cadence problems, audience problems are systemic and need analyze-performance.
- Promise improvements from following the lessons. The lessons are bets, not guarantees.
- Re-review the same post multiple times if the user keeps asking. One careful review is the deliverable. After that, the answer is to try a new post and see.
- Review posts the user did not write themselves (e.g., a competitor's post). The skill is for the user's own work. If they want to study someone else's post, that is a different request.
