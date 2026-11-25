---
name: meeting-miner
description: Mine one meeting or call for decisions, useful insight, content, messaging, communication feedback, and next actions. Use multiple calls only for meeting-specific comparison.
---

# Meeting Miner

This skill is for operators who run meetings in a small business with clients, partners, prospects, collaborators, or community members.

## What This Skill Does

Meeting Miner goes beyond summaries and action points. It turns transcripts into practical insight the user can use in content, messaging, offers, sales conversations, client delivery, and communication.

Use it when the input is:

- Pasted transcript text
- One or more transcript files
- Meeting notes from any recorder or notes tool, a doc, or another source
- Transcripts available through an MCP connector
- A mix of notes, transcript snippets, call summaries, and meeting metadata

## Core Principle

Do not stop at "what happened." Find what the meeting can improve.

Every run should help the user make at least one concrete move:

- Write a better post, newsletter, email, or script
- Improve offer language, positioning, scope, pricing, or proof
- Explain their work more clearly next time
- Understand why calls are being won, lost, delayed, or misunderstood
- Choose a useful follow-up action

## Input Handling

First identify what the user gave you:

- Single transcript: analyze it directly.
- Multiple transcripts: look for repeated patterns across calls.
- Files: read the files first, then analyze them.
- MCP source: use the available connector tools to retrieve the transcript or meeting notes before analyzing.
- Thin notes: say the input is light, extract what you can, and suggest what to include next time.
- Unknown outcome: avoid pretending a call was won or lost. Review buying signals and hesitations, then ask for outcome labels if the user wants a true won-vs-lost review.

If the user does not choose a mode, run the default `Full Meeting Miner` pass.

## Always Start With This Line

At the top of the output, include:

`Here is what I found in this meeting beyond the summary.`

Then continue with the selected output format.

## Mode Selection

Choose the closest mode from the user's wording:

- `Full Meeting Miner`: broad request for insight, "mine this", "what can I use from this", or no mode selected.
- `Content Ideas`: newsletter, Threads, LinkedIn, video, post, email, article, or content ideas.
- `Messaging And Offer`: offer, positioning, pricing, sales page, objections, product, service, copy, or how people describe the problem.
- `Communication Review`: improve communication, presentation, articulation, facilitation, coaching, consulting, demos, or sales calls.
- `Won Vs Lost Calls`: sales calls, discovery calls, why deals won/lost, close rate, buyer hesitation, pitch improvement.

Ask at most one question if the user has not given enough context. If there is enough to proceed, proceed.

## Mode 1: Full Meeting Miner

Use when the user asks for insight broadly or does not choose a mode.

Output:

```markdown
# Meeting Miner Report

Here is what I found in this meeting beyond the summary.

## 1. Useful Meeting Context
[2-4 bullets on who/what the meeting was about, without over-summarizing.]

## 2. Content Ideas
[3-7 ideas grounded in what someone actually said, asked, resisted, wanted, or misunderstood.]

For each:
- Idea:
- Source moment:
- Why it could work:
- Format: newsletter / Thread / short post / video / email

## 3. Messaging And Offer Clues
[Phrases, objections, desired outcomes, unclear moments, and buying language.]

Include:
- Words to reuse:
- Confusing parts:
- Offer, pricing, or product clue:
- Suggested fix:

## 4. Communication Review
[How the operator explained, guided, presented, or handled the room.]

Include:
- What landed:
- Where the explanation got muddy:
- Better way to say it next time:
- Practice note:

## 5. Won Vs Lost Call Notes
[Only if deal/client outcome is known. Otherwise say what extra context is needed.]

Include:
- Buying signals:
- Hesitations:
- Missing proof:
- Next sales or messaging move:

## 6. Best Next Move
[One practical action the user should take next.]
```

## Mode 2: Content Ideas

Use when the user asks for newsletter, Threads, LinkedIn, video, post, email, article, or content ideas.

Rules:

- Only suggest ideas grounded in the transcript.
- Avoid generic AI or business advice.
- Preserve the other person's language when useful.
- Turn repeated questions, confusion, objections, and strong reactions into topics.
- Include why the idea would be useful to a real reader, not just why it is interesting.

Output:

```markdown
# Content Ideas From The Call

Here is what I found in this meeting beyond the summary.

## Best Ideas
[5-10 ideas.]

For each idea:
- Topic:
- Source moment:
- Why it matters:
- Suggested format:
- First angle:
```

## Mode 3: Messaging And Offer

Use for offers, sales pages, pricing, product positioning, service packaging, buyer language, objections, unclear value, or copy.

Rules:

- Use plain words like `messaging`, `offer`, `pricing`, `package`, and `words people use`.
- Pull exact phrases when available.
- Separate what the other person said from your recommendation.
- Look for the difference between how the operator describes the offer and how the other person describes the problem.
- Notice where the buyer asks for a smaller, clearer, faster, cheaper, safer, or more specific version of the offer.

Output:

```markdown
# Messaging And Offer Clues

Here is what I found in this meeting beyond the summary.

## Words To Reuse
[Exact words or close paraphrases. Mark exact quotes clearly.]

## What They Seem To Want
[Outcomes, relief, risks, or decisions they care about.]

## Objections Or Hesitations
[Concerns, doubts, delays, confusion, or missing proof.]

## Offer Or Pricing Clues
[What this suggests about package, price, proof, scope, timing, or product.]

## Suggested Messaging Fix
[Plain-language recommendation the user can try on a page, call, post, or proposal.]
```

## Mode 4: Communication Review

Use when the user wants to improve how they explain, present, sell, coach, consult, facilitate, or run sessions.

Rules:

- Be kind and useful.
- Do not nitpick one awkward line.
- Focus on repeated patterns or moments that affected clarity, trust, energy, or direction.
- Give a better version the user can say next time.
- If reviewing a month or batch of calls, produce 5 clear takeaways.

Output:

```markdown
# Communication Review

Here is what I found in this meeting beyond the summary.

## What Worked
[Specific parts where the user explained, guided, listened, or clarified well.]

## Where It Got Muddy
[Specific moment or pattern where the explanation, structure, or next step became less clear.]

## Better Way To Say It
[Rewrite one explanation in the user's likely voice.]

## 5 Takeaways For Next Month
[Short, practical takeaways that improve communication, presentation, and articulation.]

## Practice Note
[One small exercise before the next call.]
```

## Mode 5: Won Vs Lost Calls

Use when the user provides sales calls, discovery calls, client calls, partner calls, consultation calls, or asks why something was won, lost, delayed, or not converted.

Rules:

- If outcome is missing, say: "I can review buying signals and hesitations, but I need to know which calls won or lost for a true comparison."
- Compare won calls against lost calls when possible.
- Avoid corporate sales jargon.
- Focus on what changed the buyer's confidence, clarity, urgency, or trust.
- Suggest a better next-call move, not a generic sales tactic.

Output:

```markdown
# Won Vs Lost Call Review

Here is what I found in this meeting beyond the summary.

## Buying Signals
[Moments where interest, urgency, fit, trust, or decision-readiness showed up.]

## Hesitations
[Moments where confusion, delay, price concern, weak fit, or missing proof showed up.]

## Where The Pitch Got Muddy
[Specific explanation, offer, proof, pricing, or next-step gap.]

## Messaging Or Offer Fix
[Plain-language adjustment.]

## Next Call Move
[One thing to try next time.]
```

## Helpful Behavior

- Be specific. Tie every insight to a moment in the transcript.
- If exact quotes are available, include short quotes.
- If transcript text is messy, work with it and say what you can infer.
- If there are multiple speakers, track who said what where possible.
- If there are no clear insights, say that and explain what kind of call would be better to mine.
- Do not invent customer language, buyer intent, or deal outcomes.
- Do not write generic summaries unless the user asks.
- Keep the tone practical, friendly, and plain.

## Suggested Opening Questions

Ask at most one question if needed:

- "Do you want the full Meeting Miner pass, or should I focus on content, messaging, communication, or won vs lost calls?"
- "If this is for won vs lost calls, which calls were won and which were lost?"

If the user already gave enough context, proceed.

## Capability Contract

- Reads: only transcripts, notes, and files the user pastes, attaches, or points to. If the user names a connector (a meeting-notes MCP, a drive), use it only when the host actually provides it; otherwise ask the user to paste the transcript instead of pretending to fetch it.
- Writes: saves the report as a local Markdown file when the host supports file writes and the user wants an artifact; otherwise the full report is returned in the conversation.
- Network: none required.
- External actions: none. Never sends follow-ups, emails, or messages; drafts are for the user to use.
- Privacy: transcripts often contain other people's words. The analysis stays in the conversation; nothing is sent to any update server.
