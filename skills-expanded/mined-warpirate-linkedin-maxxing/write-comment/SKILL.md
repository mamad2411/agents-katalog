---
name: write-comment
description: |
  Use when user wants to leave a substantive comment on someone else's
  LinkedIn post, reply to comments on their own posts, get a batch of
  comment templates for engaging with their network, or use commenting
  as their primary growth strategy. Trigger phrases include "write a
  comment on this post," "how should I reply to this," "help me engage
  with my feed," or when user pastes a post URL or text and asks what to
  say.
license: MIT
---

# Write comment

LinkedIn's 2026 ranking system treats comments as the highest-weight engagement signal, but only when the comment has substance. "Great post!" used to count. It does not anymore. This skill exists to write comments that actually add something to the thread, in the user's voice, in a way that earns the algorithm's attention without sounding like an engagement farmer.

## Why this skill exists

Three reasons comments are now the highest-impact move on LinkedIn:

1. Comments count for roughly 15x the weight of a like in ranking. AuthoredUp's 2025 analysis put the gap more conservatively at 2x, but every credible source agrees comments dominate likes.

2. LinkedIn's NLP-aware comment scoring downranks generic responses ("Great post!") and upranks specific questions, personal experience, and professional insight. The same comment-length sentence can earn 10x the algorithm signal depending on its content.

3. Comments put the user's profile in front of the post author's audience, not just the user's own followers. This is how you grow.

So the comment is not just polite engagement. It is content in its own right, and the rules for writing it are the same rules as for writing a post: be specific, be honest, match your voice.

## When to use this skill

Trigger when:
- The user pastes a post (text or URL) and asks what to comment
- The user wants to reply to a comment on one of their own posts
- The user wants help engaging with their feed as a growth strategy
- The user is preparing a daily commenting routine and wants help with a batch

Do NOT trigger when:
- The user is writing a top-level post. Send them to write-post.
- The user wants to send a DM. Send them to write-dm.
- The user wants to game engagement with templated "great post" comments. Refuse politely; that approach is now downranked.

## What you need from the user

The post they want to comment on. Either pasted text, a URL (you can ask them to paste the visible text since URLs do not always fetch reliably), or a description of the post and who wrote it.

Also useful (ask only if not obvious):
- Who is the author to the user? Peer, prospect, role model, stranger? This changes the register slightly.
- What is the user's goal? Engage genuinely, get noticed by the author, contribute to the thread, all three.

If voice-profile.md exists, read it.

## How comments work in 2026

A good LinkedIn comment is between 30 and 200 words. Long enough to add something. Short enough that someone reads it.

Three types of comments that get the algorithm's attention and feel real:

1. **Add a specific detail or counter-example.** "We tried this. The thing that surprised us was [specific]." This is the strongest type. It positions the user as someone who has done the thing, and the specific is what makes the comment dwell-worthy.

2. **Ask a sharp question that opens a thread.** Not "What do you think?" but "Did you find that X happens here too, or only when Y?" The question has to be specific enough that the author has to think about the answer.

3. **Honest disagreement.** "I read it differently. I have seen the opposite play out at [scale or context]." This works only when the user actually disagrees and can back it up. Performative disagreement reads worse than agreement.

What does not work:

- "Great post!" / "Love this." / "Spot on." / "Couldn't agree more."
- Restating the post in different words ("So basically what you're saying is...")
- Adding a generic agreement plus a sales pitch ("Love this. We help companies with exactly this at [company].")
- Tagging random people to drive engagement
- Long opinion pieces that take over the thread (write your own post if you have that much to say)

## How to draft

Read the post carefully. Find the most specific or interesting claim in it. The comment should respond to that claim, not to the post as a whole.

Then draft in the user's voice (using voice-profile.md). The comment should sound like the user, not like a generic LinkedIn engager. If the user is direct, be direct. If the user opens with confessions, open with one.

If the user disagrees with the post, say so honestly. Comments that politely push back tend to earn the most attention and the most respect.

## Drafting constraints (apply WHILE writing, not after)

Output must read as written by a human on the first pass. The constraints below are how you write, not a checklist to apply later. Do not narrate this process to the user. Do not show a "before humanizer / after humanizer" sequence. Just produce clean output.

**Hard bans — never appear in output:**
- Em dashes (—) and en dashes (–). Use period, comma, colon, or parentheses.
- "It's not just X, it's Y" / "Not only X but Y" constructions.
- "The real question is," "at its core," "fundamentally," "what really matters."
- Signposting: "Let's dive in," "here's what you need to know," "let's break this down," "without further ado."
- Sycophancy: "Great question," "you're absolutely right," "I hope this helps," "let me know if..."
- Knowledge-cutoff hedges: "based on available information," "as of my last update."
- AI vocabulary: leverage, delve, tapestry, underscore, pivotal, crucial, vibrant, testament, landscape (abstract), interplay, intricate, fostering, enduring, garner, valuable, enhance, showcase, align with, additionally.
- Copula avoidance: "serves as," "stands as," "marks a," "represents a," "boasts," "features." Use is/are/has.
- Emoji decoration on bullets or headings.
- Title Case In Headings. Use sentence case.
- Curly quotes ("..."). Use straight quotes (") only.
- Bold for random emphasis. Bold only for genuine key terms.
- Rule-of-three padding where the third item is filler.
- Generic upbeat conclusions ("The future looks bright," "exciting times ahead").
- Aphorism formulas ("X is the language of Y," "X becomes a trap," "X is not a tool but a mirror").
- Theatrical openers: "Honestly?" "Look," "Here's the thing," used as standalone pause-and-reveal.
- Inline-header bullet lists (`- **Speed:** ...`). Write as prose.
- "-ing" tag-ons that add fake depth: "highlighting," "underscoring," "fostering," "reflecting," "showcasing," "ensuring," "contributing to."

**Required patterns:**
- Specific, hard-to-fabricate detail. Real numbers, real names, real quotes from the user's input.
- Vary sentence length. Short. Then longer ones that take their time. Mix.
- Active voice over passive. Concrete actor over hidden subject.
- Simple copulas (is/are/has) over fancy substitutes.
- One opinion or mixed feeling where the format allows (not for neutral reference text).
- Cut every filler phrase ("in order to" → "to," "due to the fact that" → "because," "at this point in time" → "now," "has the ability to" → "can").

**Final scan before output:**
1. Scan for `—` and `–`. Any hit means redraft.
2. Scan for any word in the AI-vocabulary list above. Any hit means rewrite that sentence.
3. Scan for "it's not X, it's Y" pattern. Any hit means rewrite.
4. If three short fragments appear in a row mid-paragraph, the rhythm is engineered. Vary.

Full 33-pattern reference: see humanizer/SKILL.md in this plugin.

## Output format

Return the comment as a code block, plus:
- Character count
- A one-sentence note on what angle the comment is taking and why it is the right angle for this post

Optionally offer a variant: "Want a version that disagrees instead?" or "Want a shorter version?"

## Example

User pastes a post by someone they follow:

> "Most teams spend too much time on planning and not enough on execution. The best founders I know skip the deck entirely and just ship."

User asks: "What should I comment? I sort of agree but I think there's a middle ground."

Output:

```
We tried "skip the deck, just ship" for our first six months and it cost us about three months of rework. The thing nobody tells you is that "ship without planning" works when the team already shares a mental model, and breaks when they don't. The deck was never the point. The conversation that produced the deck was. Now we do the conversation and write a one-pager. The one-pager is the deck, just honest about being one.
```

(78 words, 412 characters.)

Angle: half agreement, half pushback with a specific anchor (three months of rework, six-month period). This is the strongest move because it engages the author's claim directly with the user's own experience, which earns a reply from the author and reads as substantive to readers.

## A note on commenting routines

Some users want help with a daily engagement routine. Acceptable use: pick 5-10 posts in their feed each morning, comment on the ones that genuinely have something to say in response, leave the rest. Skip the posts where the user has nothing real to add.

What is NOT acceptable: generating 10 different "great post" comments at once. The algorithm now reads pattern-spam behavior and the user's account loses reach. If the user asks for this, refuse and explain.

## What this skill does not do

- Generate "great post" comments at scale.
- Write disagreement that is not actually how the user feels. Honest disagreement earns reach; performative contrarianism reads worse than agreement.
- Tag random people to boost engagement.
- Hide a sales pitch inside a comment. That used to work in 2022 and now visibly destroys the user's reputation in the thread.
- Comment on posts the user has not read. Sounds obvious, but: if the user pastes a URL and a question without context, ask them to paste the post text. Do not invent the post.
