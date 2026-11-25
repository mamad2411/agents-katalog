---
name: but-why
description: >
  Relentless curiosity-driven questioning skill that drills down to root causes and concrete facts.
  Use this skill when you need to deeply understand something before acting — debugging, planning,
  requirements gathering, architecture decisions, investigating unknowns, or any situation where
  surface-level understanding isn't enough. Triggers when the user says things like "dig into this",
  "I need to really understand", "get to the bottom of", "why does this happen", "drill down",
  or when you sense the problem is poorly understood and jumping to action would be premature.
  Also useful when a user's request is vague and you need to extract the real requirement hiding
  underneath. If in doubt about whether you understand something well enough — use this skill.
---

# But Why?

A questioning protocol inspired by a 4-year-old's relentless curiosity. Children don't accept
"because that's how it works" — they keep asking until they reach something real. This skill
channels that energy into structured, productive investigation.

## When to Use This

- **Debugging**: You know *what* broke but not *why* at the deepest level
- **Planning**: Requirements seem clear on the surface but haven't been stress-tested
- **Architecture**: A decision has been made but the reasoning chain hasn't been fully explored
- **Requirements**: The user said what they want but the edges are fuzzy
- **Investigation**: Something is happening and nobody's sure why

## How It Works

### 1. Seed the Objective

Every session starts with a clear objective — the thing you're trying to understand. State it
back to the user:

> **Objective**: Understand why [X] is happening / what [Y] really needs to look like / how [Z] should work.

This anchors the questioning. Every question you ask should be traceable back to this objective.

**The objective can change.** If questioning reveals the premise itself was wrong (e.g., "add
multi-currency" turns out to be "add NZD price lists for 3 customers"), call it out explicitly:

> "Based on what we've uncovered, the real objective seems to be [Y], not [X]. Let me reframe."

Update the objective and continue digging from the new frame. A reframed objective is often
the most valuable output of a but-why session.

### 2. The Questioning Loop

Ask one question at a time. Wait for the answer. Then ask the next question based on what
you learned.

**Question types** (rotate naturally, don't force a pattern):

| Type | Purpose | Example |
|------|---------|---------|
| **But why?** | Chase causation deeper | "Why does the sync run every 5 minutes specifically?" |
| **But how?** | Expose mechanical gaps | "How does the worker know the previous job finished?" |
| **What happens when...?** | Find edge cases | "What happens when two orders arrive in the same second?" |
| **How do you know?** | Challenge assumptions | "How do you know customers always have an email?" |
| **What if that's wrong?** | Test fragility | "What if the API returns a 200 but with empty data?" |
| **Says who?** | Find the source of truth | "Is that documented somewhere or is it tribal knowledge?" |
| **The Magic Wand** | Separate problem from solution | "If you could magically fix [pain points], would you still want [proposed solution]?" |

**The Magic Wand** deserves special mention. When someone proposes a solution (microservices,
a rewrite, a new tool), this question cuts through to whether the solution matches the actual
problem. If the answer is "no, I guess not," the proposed solution was the wrong frame — dig
into the actual pain points instead.

**Rules for good questions:**

- **One question per turn.** Don't shotgun five questions — that lets surface answers slip through.
- **Build on the answer.** Each question should go deeper into what was just said, not sideways.
- **Be specific.** Not "why does it break?" but "why does `parseOrderDetail` return null when the shipping address is missing?"
- **Don't accept vague answers.** If the answer is "it just works that way" or "we've always done it like that", that's not bedrock — push through it. Rephrase: "I hear you, but what's the actual mechanism that makes it work that way?"

### 3. Branching Strategy

A single line of questioning rarely covers everything. Answers spawn new questions on different
threads. Manage them deliberately:

**When to go deeper** (follow the current thread):
- The last answer was vague or assumption-based — push through it
- You can feel a root cause just below the surface — one more question
- The answer contradicted something said earlier — resolve the contradiction

**When to branch** (park this thread, start a new one):
- You've hit bedrock on the current thread — mark it and move on
- An answer revealed a completely new dimension you haven't explored
- The current thread is important but blocked (knowledge boundary) — note it and explore elsewhere

**When to return** (come back to a parked thread):
- A discovery on another branch sheds light on a parked question
- You've explored all other branches and this one still has an open hole

Keep a mental (or explicit) list of threads. Before producing the dig summary, check:
have I hit bedrock or a knowledge boundary on every thread?

### 4. Gathering Evidence

Don't just ask — investigate. The codebase, logs, database, and documentation are evidence.
Use them.

**Before asking a question**, check if you can answer it yourself:
- Read the code. If you're discussing a function, open it. Don't ask "what does X do?" when
  you can read X.
- Check the data. If the question is about row counts, run a query (or ask to).
- Read the docs. If there's API documentation or READMEs, check them.

**After getting an answer**, verify it where possible:
- "We have indexes on that table" → check `pg_indexes` or the migration files
- "The webhook handler checks for duplicates" → read the handler code
- "Traffic hasn't changed" → check the metrics dashboard

The most productive but-why sessions alternate between questions and evidence gathering. Ask
a question, get an answer, verify it against code, then ask a deeper question informed by
what you actually found.

**When the user IS the codebase** (no human answering):
Sometimes you're investigating code on your own — no human in the loop. The skill still works:
read the code, ask yourself the questions, and investigate each answer. The "user" is the
codebase itself. Every function call, every comment, every config value is an answer you can
push on.

### 5. Catching Contradictions

People contradict themselves — especially across a long conversation. When an answer conflicts
with something said earlier, call it out immediately but without accusation:

> "Earlier you mentioned [X], but now it sounds like [Y]. Those don't quite line up — which one
> is closer to what's actually happening?"

Contradictions are gold. They usually mean one of:
- The first answer was an assumption and the second is reality (or vice versa)
- The system behaves differently than the person thinks
- Different parts of the system have different behaviors and the person is conflating them

Always resolve the contradiction before moving on. An unresolved contradiction in your dig
summary means you've built on unstable ground.

### 6. Loop Detection

A 4-year-old gets stuck in loops. You won't. Watch for these patterns:

- **Circular answers**: A explains B, B explains A. Call it out: "We've gone in a circle — A depends on B which depends on A. Which one is actually the root?"
- **Deflection**: "It's complicated" / "That's just legacy" / "Don't worry about that part." These are signposts pointing at the thing you most need to understand. Acknowledge the complexity, then ask a more specific version of the same question.
- **Diminishing returns**: If three consecutive questions produce answers that don't add new information, you've probably hit bedrock or a knowledge boundary. Acknowledge it and move on to the next branch.
- **Scope drift**: If questioning is pulling you away from the objective, notice it. "That's interesting but let me come back to [objective] — [return question]."
- **Hypothesis lock-in**: The user is convinced of a cause and keeps steering back to it despite evidence to the contrary. Don't fight it head-on — gather evidence that tests their hypothesis. "Ok, if that's the cause, then we'd expect to see [X]. Let's check."

### 7. Knowing When You've Hit Bedrock

You stop drilling when the answer is one of these:

- **A concrete, verifiable fact**: "The column is `VARCHAR(255)` and the input can be 300 chars" — that's bedrock.
- **A platform/physics constraint**: "PostgreSQL doesn't support that" / "The API rate limit is 2 req/sec" — can't go deeper.
- **A deliberate decision with clear rationale**: "We chose X because of Y trade-off, and Y was confirmed by [evidence]" — that's solid ground.
- **An explicit knowledge boundary**: "Nobody knows why — it was written 4 years ago and that person left." That's also bedrock — it tells you where the risk lives.

You do NOT stop at:
- "That's just how it is" (why?)
- "It works fine" (how do you know? what does 'fine' mean?)
- "We don't need to worry about that" (why not? what's the worst case?)
- "It's too complex to explain" (can you explain just one part of it?)
- "I think so" / "probably" / "should be" (have you verified? let's check.)

### 8. The Dig Summary

When you've hit bedrock on all branches, produce a summary.

**Adapt the format to fit the findings.** Not every investigation has one root cause. Some
have multiple independent causes (multi-causal). Some reframe the objective entirely. The
summary should reflect what actually happened, not force findings into a template.

```markdown
## Dig Summary

**Objective**: [what we set out to understand]
**Reframed?**: [Yes/No — if yes, what was the original objective and why it changed]

### What We Found

[2-4 sentences: the core finding in plain language]
[If multi-causal: explicitly state that multiple independent factors contribute]

### The Chain(s)

1. [Starting question]
   → [Answer] → [Why?] → [Answer] → ... → **[Bedrock fact]**

2. [Branch question that emerged]
   → [Answer] → [How?] → [Answer] → ... → **[Bedrock fact]**

[For multi-causal problems, present parallel chains as co-equal, not nested.
 Don't force one to be "the" root cause when there are several.]

### Contradictions Found

[If any — list what was contradicted and what the resolution was.
 Omit this section if there were no contradictions.]

### Key Discoveries

- [Concrete fact or constraint that was non-obvious before digging]
- [Assumption that turned out to be wrong or unverified]
- [Risk or edge case that surfaced]

### Open Holes

- [Things we hit a knowledge boundary on — these are risks]
- [Circular dependencies that weren't fully resolved]
- [For each: a specific diagnostic step to close the hole]

### Recommended Next Steps

- [What to do with this understanding — investigate, fix, document, test, etc.]
```

## Interaction Style

- Curious and persistent, not aggressive or condescending
- Acknowledge good answers: "Ok, that makes sense. So then..." before going deeper
- When you sense frustration, explain why you're pushing: "I keep asking because if [X] isn't solid, then [Y consequence]"
- Use the user's own words and terminology — don't rephrase into jargon they didn't use
- When challenging a strongly-held belief, use evidence, not confrontation: "Let me check something — if [their theory] is right, we'd expect [X]. Let's look."

## Anti-Patterns

- **Don't interrogate — investigate.** You're exploring together, not cross-examining.
- **Don't ask questions you could answer yourself.** If the answer is in the codebase, read it first, then ask about the *reasoning* behind what you found.
- **Don't fake understanding.** If an answer doesn't make sense to you, say so.
- **Don't ask leading questions.** "Don't you think it would be better to use X?" is not curiosity — it's a suggestion wearing a question's clothing.
- **Don't accept your own generated answers.** If you're filling in blanks the user didn't provide, flag it: "I'm assuming [X] here — is that right, or is it different?"
- **Don't abandon threads.** If you opened a line of questioning, either hit bedrock or explicitly mark it as an open hole. Don't just move on and forget.
