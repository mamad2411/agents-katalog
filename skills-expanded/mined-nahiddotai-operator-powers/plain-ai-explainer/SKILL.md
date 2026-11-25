---
name: plain-ai-explainer
description: Explain a difficult AI concept, model, tool, workflow, term, or change in plain language with an analogy, why it matters, an example, and a practical next step.
---

# Plain AI Explainer

## Purpose

Turn any real AI or technical topic into an explanation a smart beginner can understand on the first read.

The reader is not dumb. They understand normal life and work, but they should not need specialist knowledge, hidden context, or a second read to follow the explanation.

The result should sound like one smart friend explaining something useful to another. Direct, casual, concrete, easy to keep reading.

## Output Formats

Ask which format the user wants if they have not said. Default to the explainer doc.

- **Explainer doc** (default): a short structured Markdown explainer with a hook, definition, examples, one useful distinction, and a next step.
- **Social thread**: a sequence of short posts. If the platform caps characters (Threads and X cap at 500), keep every post under the cap and label each post with its verified character count.
- **Newsletter section**: 200 to 400 words with the same movement, written to sit inside a longer email.
- **Talk-track**: bullet points the user can speak from in a meeting, video, or workshop.

## The Plain-Language Standard

Write for a smart reader who is new to the topic.

### Keep

- normal adult ideas
- real consequences
- useful distinctions
- correct names for tools and files
- short and medium spoken sentences
- one unfamiliar term at a time
- plain explanations directly beside technical terms
- concrete examples from real work

### Remove

- jargon that is not immediately explained
- abstract phrases that make the reader translate the sentence
- consultant language
- baby talk
- schoolbook definitions
- fake metaphors for ordinary work
- overexplaining a point the reader already understands
- background information that does not change the point

Use the real term when the reader needs it, then explain it in normal words.

Good:

```text
An `AGENTS.md` is a set of written instructions your AI coding agent reads before it starts working
```

Weak:

```text
An `AGENTS.md` establishes a persistent operating context for agentic execution
```

Condescending:

```text
Think of it like a little rulebook for your robot helper
```

## Source First

Inspect the real source before drafting. Extract only what the source proves:

- what the thing is
- what it lets someone do
- what can go wrong without it
- the fix, setup, or useful shift
- one or two real examples
- one distinction most beginners will miss
- a familiar equivalent, when one exists
- what the reader can learn or do next

Never invent results, proof, demand, urgency, personal experience, or product behavior. If a fact may have changed, verify it before using it. If you cannot verify it, say so instead of stating it as fact.

## Build The Explanation Before Writing

Write one private sentence for each of these:

1. **Capability:** what can the thing do for the reader
2. **Risk:** what mistake, cost, or bad result can still happen
3. **Fix:** what solves or reduces that problem
4. **Reassurance:** why the fix is easier than it sounds
5. **Definition:** what the unfamiliar thing is in normal words
6. **Mechanism:** how it changes the work
7. **Proof:** what real example makes it believable
8. **Distinction:** what useful detail most beginners will miss
9. **Next step:** what the reader can do or learn next

If any sentence is vague, the source is not ready for drafting. Say what is missing and ask for it once.

## Opening Logic

The default opening uses four clear moves:

1. Name the useful capability in words the reader already knows
2. State the risk or consequence that capability does not solve
3. Introduce the fix by name
4. Reassure the reader that the fix is easier than it sounds

Shape:

```text
[Familiar thing] can [useful capability].
But it can also [clear risk or consequence].
There is a fix, and it's called [specific thing].
It's also much less [technical or difficult] than it sounds.
```

Adapt the wording to the source. Do not force "there is a fix" when the topic is an opportunity, method, or choice rather than a problem. Keep the same logic: capability, missing piece, named answer, reassurance. The opening must form one complete chain.

## Explanation Arc

Use this as the default movement, then add or remove sections when the source needs it:

1. **Opening:** capability, risk, answer, reassurance.
2. **Define it early:** explain the named thing in one plain sentence. If the reader may know a close equivalent, add one short bridge ("if you've heard of X, this works the same way").
3. **Show a real version:** what the thing actually says, changes, finds, blocks, or produces.
4. **Make the outcome concrete:** how the result changes across two familiar jobs or situations. Avoid abstract claims such as "it improves alignment".
5. **Add the useful distinction:** the part a beginner would probably miss, with two concrete examples that make it obvious.
6. **Explain how to start:** the simplest honest route for a beginner, and a second route for someone with an existing setup when useful.
7. **Finish the main idea:** return to the real consequence from the opening in plain language. The reader should get a useful ending even if they stop here.

## Directness Test

Read every sentence and ask: can a smart reader new to this topic understand it on the first read?

If not:

1. Name the real person, tool, file, action, or result
2. Replace the abstract verb with what actually happens
3. Cut the setup phrase
4. Split the sentence when it carries two ideas
5. Keep the useful detail instead of adding a metaphor

Example. Weak: "Old work can look current." Clear: "The agent can find a project you stopped working on and think you still want to use it."

## Style Boundaries

Do not use:

- storytelling runway before the point
- polished presenter voice
- generic AI commentary
- slogans or fake urgency
- rhetorical questions used as scaffolding
- em dashes
- "honestly" openers
- "It's not X, it's Y" constructions
- technical claims the source cannot prove

## Worked Example

`references/approved-agents-md-thread.md` is a real published thread produced with this method, explaining AGENTS.md files to non-technical readers. Read it as a demonstration of the movement and reading level, not as copy to reuse.

## Thread Format Checks

When the output is a social thread with a character cap:

- keep every post under the platform cap, counting spaces, emoji, and placeholder links
- label the review draft `Hook`, `2/x`, `3/x`, with the verified character count beside every label
- run `python3 scripts/check_thread.py /absolute/path/to/thread.md` when Python is available, fix every failure, and rerun
- if the environment cannot run scripts, count characters manually and say the check was manual

## Capability Contract

- Reads: only sources the user provides or points to.
- Writes: saves the draft as a local Markdown file when the host supports file writes and the user wants an artifact; otherwise returns the full draft in the conversation.
- Network: only if the user asks for source verification and the host provides web access.
- External actions: none. Never publish, schedule, or send anywhere. Drafts are for the user's review.

## Completion Checklist

- The opening forms one complete capability-risk-fix-reassurance chain
- The unfamiliar term is defined in plain words within the first two sections
- At least one concrete, source-grounded example appears
- One useful distinction a beginner would miss is included
- Every sentence passes the directness test
- Format rules for the chosen output type are verified, not assumed
