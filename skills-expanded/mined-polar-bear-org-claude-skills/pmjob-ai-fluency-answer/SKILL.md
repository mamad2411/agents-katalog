---
name: pmjob-ai-fluency-answer
description: Build your answer to "how do you use AI in your work" from two or three real examples, with an example table, a two minute version, a thirty second version and honest answers to the follow-up questions, and no tool list. Use for "run pmjob-ai-fluency-answer", "how do you use AI in your work", "AI fluency interview question", "the ad asks for AI fluency", "I have never had AI in my title", "my AI answer is a list of tools", "prepare my AI answer", "show AI skills as a product manager", part of the Claude Guide for Product Interviews Pack by 90n.
---

# AI Fluency Answer

## When To Use
The ad asks for AI fluency, your title has never had AI in it, and your answer is a list of tools. You have used AI in real product work, and you need to say how you decide what to hand over, how you brief it and what you check. The question it answers: what do I say, from my own work, when they ask how I use AI?

## When Not To Use
Not for what AI you may use as a candidate: Candidate AI Use Plan holds that. When they want to see something, AI Work Sample builds the one piece to show. If you have no real example yet, this skill will not supply one: do one small real task in your current work first, then come back.

## Inputs
- Two or three things you really did with AI in product work, in rough notes: the task, what you asked for, what came back, what you changed.
- The line of the ad or the recruiter's words about AI, quoted, and your Career Evidence Inventory if an example is already a row.
If you have none of this, I start from one task you describe from memory and mark the output as a first draft.

## Approach
The answer is organised by the four competencies named in Anthropic Academy's course AI Fluency: Framework & Foundations: Delegation, Description, Discernment, Diligence. The public course page names the four and does not define them, so the plain-word readings below are this skill's own working reading, not the course's definitions. The judgment: interviewers learn little from which tools you opened and a great deal from what you rejected. The failure it prevents is the answer with no failure in it, which sounds like an advert.

## Workflow
1. I ask up to three questions: what does the ad or the recruiter say about AI, in their words; which two or three tasks did you really use AI for in product work (research synthesis, a first draft of a spec, a competitive scan, a prototype, an analysis); where did it fail you.
2. Each example becomes one row with four columns in plain words. Delegation: what you gave to AI, what you kept, and why. Description: how you briefed it (context, examples, constraints, the format you asked for). Discernment: what you checked, what you rejected or changed, and how you could tell. Diligence: what you took responsibility for (accuracy, confidential data, telling others AI was used). Then the outcome and "where it failed me". I ask about an empty cell once; if it stays empty, it stays empty.
3. The thin test. An example with nothing under Discernment is dropped or labelled thin. One failure is required: a time the output was wrong, generic or risky, and what you did about it. With fewer than two full rows, the answer is labelled thin and says so.
4. I shape the answer in four moves: one line of stance (how you decide what to hand over), the strongest example told through the four, the failure, and what you would do in this role. The four words need not be said aloud: they structure the answer and prove nothing by themselves.
5. Two lengths as speaking notes, not a script: about two minutes and about thirty seconds. The short one keeps the stance, one check you made and the failure. No tool list: a tool is named only inside an example where it mattered. No claim of building AI products unless an evidence row shows it.
6. I prepare the follow-ups with your honest answer in one line each: how do you check its output, what would you never give it, how did it change your team's work, what about confidential data.
7. Last pass: employer and customer data come out of every example, colleagues appear by role, and any outcome number without a source goes back to words. Then say it aloud once. This is preparation: in the interview the answer is yours to give, without Claude.

## Output Format
```markdown
# AI Fluency Answer
Role: [title] | What they ask about AI: "[line quoted]" | Date: [date] | Status: [first draft, thin or ready]
## Examples
| ID | Task | Delegation: what I gave AI, what I kept, why | Description: how I briefed it | Discernment: what I checked and changed | Diligence: what I answered for | Outcome | Where it failed me | Evidence row |
|---|---|---|---|---|---|---|---|---|
| A1 | [task] | [gave, kept, why] | [context, examples, constraints, format] | [check, change, how I could tell] | [accuracy, data, who I told] | [in words, a number only with a source] | [what went wrong, what I did] | [E-ID or "none"] |
## Long version, about two minutes
- Stance: [one line on how I decide what to hand over and what to keep]
- Example [ID] through the four: [speaking notes]
- The failure, then this role: [what happened, what I did, what I would do here]
## Short version, about thirty seconds
[Stance, one check I made, the failure, in three or four sentences of notes.]
## Follow-up questions
| Question | My honest answer in one line |
|---|---|
| How do you check its output? | [answer] |
| What would you never give it? | [answer] |
| How did it change your team's work? | [answer or "it has not yet"] |
| What about confidential data? | [answer] |
## Decision
You decide which example leads and which failure you tell, and you say the long version aloud once by [date].
```

## Done When
- Two or three real examples each fill all four columns, or the answer is labelled thin.
- One failure is in both versions, and no list of tools appears: any tool named sits inside an example.
- Each follow-up has a one line answer you would say as written.

## Quality Bar
- The plain-word readings of the four competencies are presented as a working reading, never as the course's own definitions.
- Notes about the answer only. Nothing here measures you, and the word "thin" describes an example.
- No confidential employer or customer data in any example; colleagues by role.
- Speaking notes in your words, nothing to memorise line by line. A small true example outweighs a large vague one.
- Only AI work you really did, including where it failed; no example is invented or enlarged.

## Next
Run pmjob-ai-work-sample (AI Work Sample) to have something to show.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
