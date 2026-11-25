---
name: pmjob-product-sense-case
description: Run a practice product sense case on an open product or design question and produce the written case, notes on your answer against a rubric you can see and a practice log line. Use for "run pmjob-product-sense-case", "practise a product sense question", "product design interview practice", "how would you improve this product", "design a product for this user", "my answers sound like a framework", "whiteboard exercise practice", "give me an open product question", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Product Sense Case

## When To Use
You know the steps by heart and your answers still sound like a recited framework. A product sense round or a design exercise is coming, and you want to answer one open question in full, be challenged on it, and see which parts of the answer were there. It answers one question: did I make choices about users and needs, or did I list things?

## When Not To Use
Not for choosing measures or explaining a metric that moved: use Metrics Case. Not for a question that hands you a list of options and asks what to cut: use Prioritisation and Execution Case. If the question starts from an app that already exists, use App Critique.

## Inputs
- The round as the recruiter described it, in their words, the length they gave you, and a question source: the product from your Company Research Brief, a product you use, or "give me a generic open question".
- One or two pieces of your own shipped work you might honestly draw on, as evidence rows if you have them.
If you have none of this, I start from a generic open question with a time box you set, and mark the output as a first draft.

## Approach
The round is named in public employer interview guides; the order below is the common product design case order, and its shape is the Double Diamond from the Design Council: widen on users and needs, commit, then widen on options, commit again. Those guides describe what interviewers listen for: a clear structured start before any idea, an ambiguous problem broken down, a conversation in which you ask for guidance and adjust, the core customer problem stated plainly with the reason behind each decision, and who you would work with and what it costs them to build. For designers they add trade-offs held when a constraint changes, and the business value of the product as well as the design. The failure this prevents is skipping the first commit: no user chosen, no need chosen, then eight features.

## Workflow
1. I ask up to three questions: which question source, what time box the recruiter gave (you set it, I never assume one), and whether you answer in text, as a whiteboard exercise you describe, or in voice mode, where you speak your answer aloud and I reply in speech. This is practice only, never for use during a real interview.
2. I play a stand-in interviewer: I give the question, answer clarifying questions briefly, then stay quiet while you answer in full. Work in this order: clarify and state the goal; say who it is for and name the user groups; choose one group and say why; name their needs and choose one; give several options; pick one and state the trade-off; say in one or two lines how you would know it worked.
3. Four moves keep it from sounding recited: one sentence of point of view before the structure; every list ends in a choice with a reason; one detail from your own shipped work where it honestly applies; one thing you are deliberately leaving out.
4. I ask two or three follow-ups of the kind the guides describe: I challenge a choice, change a constraint, or ask "why that one". Adjusting is part of the answer; defending everything is not.
5. I write up your case in your words, then show the rubric: eight rows, each marked present, thin or missing, with your own words quoted as the evidence. No number, no total, no comment on you.
6. You redo the one weakest part in your own facts and reasoning. I do not supply a model answer to memorise. I add a log line: date, question, what to practise again.

## Output Format
```markdown
# Product Sense Practice Case
Question: [question] | Time box: [minutes you set] | Mode: [text / whiteboard / voice] | Date: [date]
## Your answer, in order
- Goal: [your words] | User groups, the one chosen and why: [your words]
- Needs, the one chosen and why: [your words] | Options: [your words]
- The pick and its trade-off: [your words] | How you would know it worked: [your words] | Left out on purpose: [your words]
## Notes on the answer
| Rubric row | Status | Your words as evidence |
|---|---|---|
| Goal stated | [present / thin / missing] | [quote] |
| Users named and one chosen with a reason | [status] | [quote] |
| Need or problem chosen with a reason | [status] | [quote] |
| More than one option | [status] | [quote] |
| Trade-off named and a choice made | [status] | [quote] |
| How you would know it worked | [status] | [quote] |
| Responded to the challenge and adjusted | [status] | [quote] |
| Who you would involve | [status] | [quote] |
## What to practise again
[Date] | [Question] | [The one part redone, and what to repeat next time]
## Decision
You decide whether to repeat this question type or move to the next round's practice, by [date].
```

## Done When
- The answer table holds your words, with a chosen user group and a chosen need, each with its reason.
- Every rubric row has a status and a quote, or says "nothing said".
- The weakest part has been redone by you, and the log line is written.

## Quality Bar
- The rubric is a stand-in built from public guides, not any employer's scoring sheet. Notes describe the answer, with no number, no verdict on you and no comparison with other candidates.
- "How you would know it worked" stays at one or two lines; measurement has its own practice.
- Details from your past work appear only if you supplied them. Nothing is invented to make the answer richer.
- Practice only: you do the thinking, the redo is in your own reasoning, and Claude is never used during a real interview.

## Next
Run pmjob-metrics-case (Metrics Case) to practise the analytical round.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
