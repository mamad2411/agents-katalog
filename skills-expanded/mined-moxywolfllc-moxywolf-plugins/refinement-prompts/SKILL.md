---
name: refinement-prompts
description: Structured diagnostic prompts for refining written content based on specific quality issues. Use when reviewing drafts, improving content clarity, or addressing feedback about passages that are too abstract, hedged, AI-sounding, need stories, need opinion, or require technical unpacking. Triggers refine this, make this better, improve this passage, sounds too AI, too generic, needs more voice.
license: Proprietary - MoxyWolf LLC
---

# Refinement Prompts

Diagnostic prompts organized by content problem type. Use these to identify the specific issue with a passage and ask the right follow-up question to fix it.

## Usage Pattern

1. **Identify the problem**: What's wrong with the passage? (too abstract, too hedged, sounds like AI, etc.)
2. **Select the appropriate prompt**: Use one of the diagnostic questions below
3. **Get the answer**: Wait for the specific detail, story, or opinion
4. **Rewrite**: Apply the answer to fix the passage

---

## When Passage is Too Abstract

**Problem signals**: Generic claims, no specifics, could apply to anyone, lacks concrete detail

**Diagnostic prompts**:
- "Give me a number, a name, or a date."
- "What did this look like in practice?"
- "Who specifically did this happen to?"

**Example exchange**:
- **Before**: "The results were significant."
- **Prompt**: "Give me a number."
- **Answer**: "Response rates jumped from 12% to 47%."
- **After**: "Response rates jumped from 12% to 47%."

---

## When Passage is Too Hedged

**Problem signals**: Excessive qualifiers (may, might, could, perhaps), covering all bases, no clear position

**Diagnostic prompts**:
- "Do you actually believe this or are you covering your ass?"
- "What's the version without the qualifiers?"
- "If you were arguing this at a bar, how would you say it?"

**Example exchange**:
- **Before**: "This approach might potentially offer some advantages in certain contexts."
- **Prompt**: "What's the version without the qualifiers?"
- **Answer**: "This approach works better."
- **After**: "This approach works better."

---

## When Passage Sounds Like AI

**Problem signals**: Formal register, perfectly balanced, no personality, forbidden phrases (e.g., "it's worth noting"), academic tone

**Diagnostic prompts**:
- "Read this out loud. Where do you stumble?"
- "What word would you never use?"
- "How would you text this to a friend?"

**Example exchange**:
- **Before**: "It's worth noting that this methodology yields favorable outcomes."
- **Prompt**: "How would you text this to a friend?"
- **Answer**: "This method just works."
- **After**: "This method just works."

---

## When Passage Needs Story

**Problem signals**: Explanation without example, abstract teaching, missing the human element, no lived experience

**Diagnostic prompts**:
- "When did you first realize this?"
- "Who taught you this the hard way?"
- "What's the worst example you've seen?"

**Example exchange**:
- **Before**: "Proper validation prevents errors."
- **Prompt**: "What's the worst example you've seen?"
- **Answer**: "A client deployed without validation and their system accepted 'banana' as a phone number. Cost them three days of cleanup."
- **After**: "A client deployed without validation. Their system accepted 'banana' as a phone number. Three days of cleanup later, they learned."

---

## When Passage Needs Opinion

**Problem signals**: Neutral explanation, "some believe" constructions, presenting all sides equally, no stakes

**Diagnostic prompts**:
- "What pisses you off about this?"
- "What do the idiots get wrong?"
- "If you could grab someone by the collar about this, what would you say?"

**Example exchange**:
- **Before**: "There are various perspectives on survey design."
- **Prompt**: "What do the idiots get wrong?"
- **Answer**: "They ask leading questions and wonder why nobody trusts their data."
- **After**: "Most survey designers ask leading questions, then wonder why nobody trusts their data."

---

## The Unpacking Aside Mechanism

For passages that are too vague or hand-wavy but would clutter the main argument if fully expanded.

### Structure

**Part 1: Inline marker**

Add a parenthetical reference in the main text:

Format: `(see "Unpacking: [Topic]" below)`

Example:
- **Before**: "Conversational AI is software that holds actual conversations."
- **After**: "Conversational AI is software (see "Unpacking: What's Actually in the Stack" below) that holds actual conversations."

**Part 2: P.S. section at end of article**

Add a post-script section after the main signature:

```
–

P.S. – Unpacking: [Topic Name]

[Detailed technical explanation in voice – specific, concrete, 
showing actual implementation knowledge. This is where you prove 
you built the thing, not just read about it.]
```

**Multiple unpacks**: Stack them as P.S., P.P.S., P.P.P.S., etc.

```
P.S. – Unpacking: What's Actually in the Stack
[content]

P.P.S. – Unpacking: Why Context Windows Matter
[content]
```

### When to Use Unpacking

Use unpacking when:
- A term or concept is too technical for the main flow but readers might want detail
- You're making a claim that requires technical proof but the proof would derail the narrative
- The main audience doesn't need the depth, but a subset would appreciate it
- You want to signal expertise without being pedantic

**Diagnostic prompts for unpacking**:
- "What's the technical reality behind this? Walk me through the actual implementation."
- "Who's this unpack for? The curious reader or the technical skeptic?"
- "What details prove you actually built this versus just read about it?"

### Why This Works

- AI doesn't do structural innovation like P.S. sections
- Signals "I actually know how this works" without cluttering the main argument
- Readers who want depth get it; skimmers aren't punished
- The format itself is a credibility marker

---

## Refinement Workflow

When working with a draft:

1. **Invite selection**: "Select any passages that need work and tell me what's wrong."

2. **Classify the problem**: Match the feedback to one of the categories above

3. **Ask the diagnostic prompt**: Use the exact question from the relevant section

4. **Wait for the answer**: Get the specific detail, story, number, or opinion

5. **Rewrite the passage**: Show before/after

6. **Confirm**: "Better? Or still off?"

7. **Move to next passage**: Repeat until all selections are refined

---

## Quick Reference

| Problem | Ask |
|---------|-----|
| Too abstract | "Give me a number, name, or date." |
| Too hedged | "What's the version without qualifiers?" |
| Sounds like AI | "How would you text this to a friend?" |
| Needs story | "What's the worst example you've seen?" |
| Needs opinion | "What pisses you off about this?" |
| Needs unpacking | "Walk me through the actual implementation." |
