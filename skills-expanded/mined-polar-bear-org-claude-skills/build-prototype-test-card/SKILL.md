---
name: build-prototype-test-card
description: Writes a Prototype Test Card that sorts the beliefs behind your idea by how much rides on each and how little evidence it has, then puts one belief on a card with the task, who sees it, one observable measure and a pass line you set and date before anything is built. Use for "run build-prototype-test-card", "write a test card", "what does this prototype need to prove", "which assumption do I test first", "set the pass line before I build", "what result would make us stop", "riskiest assumption", "how will I know the prototype worked", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Test Card

## When To Use
The prototype is about to be built and nobody can say what result would make you stop. Everyone expects it to "go well". This skill answers: which belief does the prototype test, what will you watch for, and what result counts as a pass?

## When Not To Use
If the prototype is built and the question is what it does not prove, run Prototype vs Production Note. If the doubt is whether an AI feature holds up on inputs nobody picked, run AI Prototype Input Check. If there is no agreed question yet, run Problem Frame.

## Inputs
- The idea and the question it answers (the Idea One-Pager, if you have one).
- What you already know and where it came from: sessions, support themes, usage data.
- Which real target users you can reach, and roughly how many.
If you have none of this, I start from the idea in one sentence and mark the output as a first draft.

## Approach
The Test Card (Strategyzer, https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card) asks four questions in order: what needs to be true for the idea to work, how you will test whether it is true or false, what you will measure, and what success looks like. Before the card comes a sort of every belief the idea depends on, a common practitioner step, so you test what could sink the idea and not what is easiest to test. The failure this prevents: a round of friendly sessions, a room that "loved it", and a pass line written afterwards to fit what happened.

## Workflow
1. Ask at most three questions: what is the idea and what do you plan to build; which real target users can you reach; which role reads the result and decides what happens next?
2. List every belief the idea depends on: about the need, the behaviour, the willingness to switch. Sort each on two questions: how much rides on it, and how little evidence is there? Take the one that is high on both, even when another is easier to test.
3. What needs to be true: write that belief as "[target users] will [behaviour] because [reason]". One belief per card. "And" means two cards.
4. How you will test it: name the task a user will attempt and who sees it. Real target users only, never colleagues and never the leaders who asked for the idea.
5. What you will measure: one behaviour that can be seen in a session, such as completed the task or chose it over the current way. "Liked it" and "said they would use it" are not measures.
6. What success looks like: you set the threshold and date it now, before anything is built. I do not propose a pass line once results exist. No threshold, no test.
7. Check the card can fail: say what result would make you drop the belief. If no result would, write the belief again until one does. Then send the card to the role who decides.

## Output Format
```markdown
# Prototype Test Card
**Idea:** [name] | **Card written on:** [date, before the build] | **Decider:** [role]
## Beliefs behind the idea
| Belief | How much rides on it | Evidence so far and its source | Test first? |
|---|---|---|---|
| [belief] | [high / medium / low] | [evidence, or none] | [yes / no] |
## Card [number]
| Question | Entry |
|---|---|
| What needs to be true | [target users] will [behaviour] because [reason] |
| How we will test it | [task], attempted by [number] real target users, [where and how] |
| What we will measure | [one behaviour seen in a session] |
| What success looks like | [threshold, set by the builder on [date]] |
**Would make us drop the belief:** [result]
**After the sessions:** no result is written on this card. Counts per task go in the Usability Test Findings; the reading against this pass line goes on the Prototype Learning Card.
## Decision
[Decider, by role] agrees the belief and the pass line by [date], before the build starts. After the sessions the line is read exactly as written here, on the Prototype Learning Card.
```

## Done When
- Every belief is sorted on both questions, the one chosen is high on both, and each card holds one belief with no "and" in it.
- The measure is a behaviour a person can see, not an opinion.
- The pass line carries a date earlier than the first build session.
- The card names a result that would make you drop the belief.

## Quality Bar
- The threshold is yours. I can ask what would change your mind; I never fill the number in.
- No results invented or predicted, and enthusiasm in a meeting is never counted as a result. What the prototype cannot show is written at handover, not here.
- The card holds the plan and the pass line, never the result: counts per task belong to Usability Test Findings and the reading against the line to Prototype Learning Card. Nothing on it rates a participant.
- A pass means the belief held in this test. It does not make the prototype ready for anyone to rely on.
- Real target users test the belief; the builder sets the pass line before the build and nobody moves it after.

## Next
Run build-prototype-brief (Prototype Brief) to decide how real the prototype must be to test this belief.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
