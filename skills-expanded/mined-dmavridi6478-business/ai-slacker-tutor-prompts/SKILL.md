---
name: ai-slacker-tutor-prompts
description: Six prompts from the @ai_slacker "Infinite Private Tutor" series — turns Claude into a compressed, no-mercy tutor for learning any skill fast, instead of a generic explainer. Use when someone wants to learn a skill under time pressure, wants their real gaps exposed instead of reassurance, wants to be dropped into a realistic mistake-first scenario, wants a real 7-day plan tied to a specific outcome, or wants a dense concept translated without jargon. Distinct from the existing `ai-slacker-prompts` (dev-task prompts) and `ai-slacker-premortem` (failure-analysis prompts) skills — this series is about compressing learning curves.
---

# AI Slacker Tutor Prompts

Six prompts from the @ai_slacker "Claude has a mode called Infinite Private Tutor —
it can teach you any skill from zero in 4 hours" series. Each is a distinct
teaching mechanism (curriculum triage, mistake-first practice, jargon-free
translation, outcome-tied planning, gap detection, forced explanation). Paste
the one that matches the situation, filling in the bracketed placeholder(s).

## 1 — THE LEARNING CURVE DESTROYER

Use when: starting a skill from zero, under a hard time limit.

> You are a teacher who only has 4 hours with me and will never see me again. Your only goal is to make me functional in [SKILL] before time runs out. Don't give me theory without use. Don't give me a list. Tell me: what to learn first, what to ignore completely, and what is the one exercise that, if I do it once, puts me ahead of 70% of people who have been studying this for months.

## 2 — THE REAL MISTAKE SIMULATOR

Use when: you understand the theory but haven't been tested against a real situation.

> Don't explain [CONCEPT] to me. Drop me directly into a real situation where I'd have to use it and would probably get it wrong. When I make a mistake, don't give me the answer: ask me a question that forces me to discover where my reasoning broke. Only give me the answer after I've tried at least twice. Repeat this cycle until I get it right without hesitating.

## 3 — THE IMPOSSIBLE LANGUAGE TRANSLATOR

Use when: a piece of content (paper, doc, spec) is too dense/jargon-heavy to parse.

> The content below is confusing to me. Before explaining, tell me: what is the single sentence that, if I understand it, makes the rest make sense on its own? Explain only that sentence first. Use a day-to-day analogy, with no technical terms. Then ask me 3 questions that only someone who truly understood can answer. Don't continue until I pass all three. [PASTE THE CONTENT HERE]

## 4 — THE PERSONAL PATH ARCHITECT

Use when: you have a specific outcome and deadline, not a vague "get better at X" goal.

> My real goal is [GOAL]. It's not to learn [SKILL] in general, it's to achieve [SPECIFIC RESULT] in [TIMEFRAME]. I already know [WHAT YOU ALREADY MASTER]. Based on that, build me a 7-day path. Each day has: a single task that fits in 45 minutes, a clear criterion so I know if I did it right, and what NOT to do that day so I don't waste time. If the whole path doesn't get me to the goal, redo it until it does.

## 5 — THE HIDDEN GAP DETECTOR

Use when: you think you already know a skill and want that checked, not confirmed.

> I think I already master [SKILL]. I want you to prove me wrong. Ask me 5 questions that seem simple but expose the gaps of someone who has never really gone deep. For every answer I give, tell me: what does my answer reveal about what's still missing from my foundation. Don't go easy on me. If I'm shallow, say it straight.

## 6 — THE FORCED FEYNMAN METHOD

Use when: you just studied something and want to know if it actually stuck.

> I just studied [TOPIC]. I'm going to explain to you what I understood as if you were a 10-year-old child. As I explain, stop me at every point where I use jargon without knowing what it means, where I skip a step in the reasoning, or where I oversimplify to the point of being wrong. At the end, tell me exactly what these mistakes reveal about what is still not solid in my head.

## Which one to reach for

| Prompt | Use it when |
|---|---|
| 1 Learning Curve Destroyer | Zero knowledge, hard deadline — need a triage plan, not a course |
| 2 Real Mistake Simulator | Know the theory, need to be tested in a realistic scenario |
| 3 Impossible Language Translator | A specific document/concept is too dense to parse |
| 4 Personal Path Architect | Specific outcome + deadline — need a concrete day-by-day plan |
| 5 Hidden Gap Detector | Think you already know it — want the gaps found, not reassurance |
| 6 Forced Feynman Method | Just studied something — want to know if it actually stuck |

## Related skills in this repo

- **ai-slacker-prompts**: Same source account, different series — 8 dev-task prompts (PRD, design brief, security audit, debugging, tests, refactor, commits, skill creation).
- **ai-slacker-premortem**: Same source account, different series — 5 adversarial premortem prompts for stress-testing a plan before launch.
- **learn-topic**, **learn-feynman**, **teachback**, **micro-curriculum**: Existing single-purpose learning commands in `.claude/commands/` — this skill's prompts are more adversarial/compressed (explicitly "don't go easy on me," "prove me wrong") than those.
