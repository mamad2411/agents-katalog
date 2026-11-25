---
name: guijios-reply
description: >
  Cross-platform reply and comment drafting. Auto-routes to platform-specific rules
  (GitHub/Reddit/Twitter/HN/general). Use when the user mentions: reply to issue,
  reply to PR, github reply, draft a reply, write a comment, comment on issue,
  reddit reply, analyze comments, twitter reply, help me respond.
---

Cross-platform reply/comment drafting. Auto-routes to the correct platform ruleset based on input.

## Routing

| Input | Mode |
|-------|------|
| GitHub Issue/PR number or link | GitHub mode |
| Reddit comment text/screenshot | Reddit mode |
| Twitter/X content | Twitter mode |
| Other platforms or unspecified | General mode (applies universal principles) |

---

# Part 1: Universal Principles (Shared Across All Platforms)

## Context Assessment (Judge Before Writing)

| Context | Definition | Core Strategy |
|---------|-----------|---------------|
| **Your turf** | You are the maintainer / OP / author | Deliver information |
| **Someone else's turf** | You are a visitor | Contribute experience first, then ask; no self-promotion |
| **Cold DM** | Zero prior relationship, you're reaching out | Reference their specific content to build trust |

### Rules for Someone Else's Turf

- **Contribute before asking.** Share a similar problem or experience, then naturally lead into one question
- **One question per comment.** Multiple questions = interrogation vibes
- **Every question must have clear information value.** Before posting, articulate "what will this answer tell me?" If you can't, rewrite
- **Your profile is your introduction.** No need to introduce yourself in the body text
- **Don't reveal research intent.** Look like "someone who ran into the same problem," not "competing founder mining for intel"

### Rules for Cold DMs

- **Quote their specific words.** Vague references = low reply rate
- **Make it clear you're not selling anything**
- **Give them an easy out.** "No worries if not"
- **Async over calls.** Higher reply rate

## Pre-Send Checklist (5 Steps, Required Every Time)

1. **Intent check:** What information does this comment aim to get? What's the concrete use for us? If you can't answer, rewrite
2. **Fact check:** Verify your own project's technical claims against code; verify quotes against originals
3. **Smell check:** Re-read from the recipient's perspective. Does it read like competitive research? Like AI? Or like someone who naturally ran into the same problem?
4. **Style check:** Run through the blocklist
5. **Compression check:** Can you cut an entire paragraph? Can bullets collapse into prose? Did you restate something the other person already said clearly? When in doubt, cut

## Cross-Platform Blocklist

- Em dashes in body text
- "Thanks for your contribution" / "Thank you for reporting this"
- "Great catch" / "Great question" / "Appreciate the detailed report"
- "the clearest/strongest/best [X] I've seen" (superlative praise)
- "Feel free to..." / "Don't hesitate to..."
- "Happy to discuss further" / "Let me know if you have questions"
- "I'd love to hear your thoughts"
- "I maintain [project name]" as an opener
- @-mentioning multiple people with separate questions in one comment
- "Curious about..." / "I'd be interested to know..." (reveals research intent)
- Any three-part structure. Not just Thank → Answer → Invite, but also: Confirm problem → Restate solution → List asks, Acknowledge → Explain → Close. More than 2 paragraphs in a single comment is a red flag
- Using a bullet list for 2-3 short asks. Real people inline them into a sentence of prose. Bullets only make sense for 4+ independent complex items
- Restating what the other person already said clearly. If they wrote out a solution, don't come back with "you're right, the approach is..." Just move to the next step

## Cross-Platform Dos

- High information density, no filler sentences
- Have an opinion, don't just describe
- Lead with the conclusion, no preamble
- Use contractions (doesn't, won't, btw, iirc, tbh)
- Keep it short. Default is 1-2 sentences. Past 3 sentences, ask yourself: can I cut a paragraph? Past 2 bullets, ask yourself: can these collapse into prose? Only open up the length budget for deep technical discussion

## Strategic Principles

1. **Silence is a weapon** -- not replying ≠ losing
2. **Technical credibility is the only moat**
3. **Convert > Defend** -- spend energy on people who might use your product
4. **Don't explain motives** -- only answer people who genuinely want to know
5. **Don't engage in legal discussions**

---

# Part 2: GitHub Mode

## Input

- Issue/PR number (e.g. #72) or link
- Pasted comment content
- Screenshot

After receiving a number/link, use `gh` commands to read the Issue/PR body and existing comments to understand the full context.

## Workflow

### Step 1: Understand Context

- Issue or PR? Open / Closed / Merged?
- Is the author an external user or yourself?
- How many comments exist? What does the last one say?
- What is the other person's core ask?
- **Assess context: your repo or external repo?**

### Step 2: Draft Reply

Output sendable text. Put strategic reasoning after the reply.

## GitHub Tone Guide

- **Like coworkers chatting on Slack**
- Drop subjects. "Fixed in #77." not "This has been fixed in #77."
- Answer technical questions with technical language, don't dumb it down

### Tone Examples

**Closing an Issue:** `Fixed in #77.`

**Confirming a Bug:** `Yeah this is real. Will add a per-agent semaphore.`

**Feature Request:** `Makes sense. Tracking in #XX.`

**Asking About Use Case:** `What's the use case driving this?`

**Code Review:** `Left a few comments. Main thing is [specific issue].`

**Merging a PR:** `LGTM, merged.`

## GitHub Context Strategies

### Your Repo

| Scenario | Strategy |
|----------|----------|
| External bug report | Confirm the issue + fix plan/status, optionally ask about use case |
| External PR (good quality) | Substantive technical feedback, can ask about use case after merge |
| External PR (poor quality) | Point out specific problems, no vague encouragement |
| Feature request | Decide yes/no, state conclusion, link to tracking issue |
| Repeat contributor | Can ask about use case, don't be overly enthusiastic |
| Low-value issue | Close with one sentence explaining why |

### External Repo

Prohibited:
- "I maintain [project name]" as an opener
- @-mentioning more than two people with separate questions in one comment
- "Curious about..." / "I'd be interested to know..."

Tone examples:

Bad:
> I maintain open-multi-agent, a TS multi-agent framework.
> We took a similar approach to what you're describing.
> @alice I'm curious how you solved X?
> @bob I'd also love to know about Y?

Good:
> Same problem in a TS multi-agent orchestrator. [describe the specific shared problem].
> @alice how much effort did X take to build?

### GitHub Real-World Examples

**Example 1: Closing a bug issue + asking about use case (#72)**

> Fixed in #77.
>
> Good catch on the token budget interaction btw. What are you using this for? Would be useful to know.

**Example 2: Asking a repeat contributor about their use case (#71)**

> Thanks for the second PR. What's the use case driving this?

**Example 3: Joining a discussion under an AutoGen issue (microsoft/autogen#7487)**

> Same problem in a TS multi-agent orchestrator. Coordinator handles decomposition and synthesis but nothing checks goal alignment in between. Blind spot by design.
>
> @msaleme how much engineering effort did the separate integrity node take to build and maintain? Wondering if this is a weekend project or a full team commitment.

Key points: First paragraph contributes experience without self-identification. Second paragraph asks one question with clear information value (quantifying the workaround cost).

**Example 4: Feature request + inviting a PR (#124)**

Bad (three-part AI smell: confirm problem → restate solution → list asks):
> Real gap. `onTrace` shows a tool ran but not what went in/out, so debugging means digging into model server logs.
>
> Proposal looks right: add `input: Record<string, unknown>` and `output: string` to `ToolCallTrace`, pass them in `emitTrace`. Mirrors what `ToolCallRecord` already exposes.
>
> Want to send a PR? Two asks if you do:
> - Keep both fields required, no opt-in flag
> - Add assertions in `tests/trace.test.ts` covering success and error cases

Good (real maintainer):
> Makes sense. Want to PR this? Just add coverage in `tests/trace.test.ts` for both success and error.

Key points: The submitter already spelled out the change, so don't restate the problem or the solution. Just agree, invite the PR, and inline one constraint. Multiple short constraints collapse into prose, no bullets needed.

## GitHub Sending

Execute via `gh issue comment` or `gh pr comment`.

---

# Part 3: Reddit Mode

## Input

- Pasted comment text
- File path containing comments
- Screenshot

## Workflow

### Step 1: Classify Each Comment

| Category | Reply? | Criteria |
|----------|--------|----------|
| Technical question | Yes | Asks about specific implementation, usage, or architecture |
| Real user feedback | Yes | Has actually used the product |
| Positioning/differentiation question | Yes | "How is this different from X" |
| Usage question | Yes | How to install, configure |
| Favorable argument/analogy | Maybe | Someone backing you up; brief acknowledgment |
| Positive recognition | Maybe | Enthusiastic ones get a short thanks, lukewarm ones skip |
| Pure attack/mockery | No | No substantive content |
| Legal/copyright discussion | No | Anything you say will be used against you |
| Self-promotion piggyback | No | Promoting their own project |
| Memes/spectating | No | No substantive content |
| Off-topic | No | Irrelevant |

### Step 2: Draft Replies

```
#### u/username (subreddit) priority

> Original comment quote

**Suggested reply:**
> Reply content

**Rationale:** Strategic intent
```

Summarize no-reply decisions in a table:

```
| User | Content Summary | Why Not Reply |
```

### Step 3: Output Sentiment Summary

Brief summary of overall sentiment, trends, and notable signals.

## Reddit Tone Guide

Reddit users are extremely sensitive to AI-generated text. These rules apply on top of the universal blocklist:

- Addressing every single point the other person made: prohibited (real people pick one or two)
- Structured bullet lists for simple questions: prohibited (use natural paragraphs)
- Excessively polite and positive: prohibited (real people have attitude)
- Casual language allowed: nah, tbh, kinda, yeah, lol
- Tone should sound like chatting with a peer

### Reddit Tone Examples

Bad (AI smell):
> Great question. The framework uses namespaced keys for SharedMemory, so each agent writes to its own namespace -- no cross-agent write conflicts. Reads are global. Would love to hear your thoughts on this approach.

Good (human):
> SharedMemory is namespaced per agent, so writes don't conflict. Reads are global though. Closest to single-writer-per-namespace if you want a label for it.

Bad (AI smell):
> Appreciate the honest feedback. Local model compatibility is still rough -- tool-calling format varies a lot across models. If you have specific errors, happy to look into it.

Good (human):
> yeah local model support is still rough tbh. tool-calling format varies a lot between models and that's where it breaks. if you hit specific errors feel free to open an issue, would be useful to know what breaks first.

---

# Part 4: Twitter/X Mode

## Twitter Tone Guide

- 280 character limit, extreme brevity
- Threads are fine but each tweet must stand alone with information value
- More casual than Reddit
- Emoji OK but don't overdo it
- No hashtag spam

---

# Part 5: General Mode

When the platform isn't listed above (HN, Discord, forums, etc.), apply Part 1 universal principles plus:

- HN: Extreme emphasis on technical depth. Zero tolerance for anything that smells like promotion. More restrained than Reddit
- Discord: Most casual. Emoji reactions can replace text replies
- Forums: Adjust to each community's specific culture

## Sending

Draft complete -> Run the 5-step pre-send checklist -> Ask the user whether to send -> Execute after confirmation.
