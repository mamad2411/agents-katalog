---
name: learn-faster-7-prompts
description: Seven copy-paste prompts for learning almost anything faster with Claude - find knowledge gaps first, build a 20/80 roadmap, make hard concepts simple, turn learning into active recall, learn through questions only, train like an expert, and build a spaced-review system so you do not forget. Use when the user wants to learn a topic or skill, study for an exam, or retain what they learn. Source @ai_slacker "7 ChatGPT prompts to learn almost anything 10x faster" (Batch 99); the prompts work unchanged in Claude.
---

# Learn faster - 7 prompts

Replace the [BRACKETS]. Each prompt is quoted exactly as shown on the slides. Related, already installed: `learn-topic`, `learning-roadmap`, `learn-feynman`, `ai-slacker-tutor-prompts`.

| # | Use it when | Command |
|---|---|---|
| 1 | You do not know what you do not know | `/learn-faster 1 <topic>` |
| 2 | You need a plan with limited time | `/learn-faster 2 <topic>` |
| 3 | One concept will not click | `/learn-faster 3 <concept>` |
| 4 | You want to be tested, not lectured | `/learn-faster 4 <topic>` |
| 5 | You learn best by answering questions | `/learn-faster 5 <topic>` |
| 6 | You want expert-level skill | `/learn-faster 6 <skill>` |
| 7 | You need to remember it for months | `/learn-faster 7 <topic>` |

## 1. Find your knowledge gaps first

```
I want to master [TOPIC].

Before teaching me, give me a diagnostic test covering the fundamentals, conceptual understanding, practical application, and problem-solving.

Analyze my answers and identify the exact areas where my knowledge is weak, incomplete, or inconsistent.

Then create a personalized learning plan that focuses only on the gaps that matter most. Retest me after each section and increase the difficulty as I improve.
```

## 2. Build the fastest learning roadmap

```
I want to learn [SKILL/TOPIC] for [GOAL].

My current level is [LEVEL] and I can study for [TIME] per day.

Identify the 20% of concepts and skills that will give me 80% of the useful understanding.

Put them in the best learning order and create a step-by-step roadmap using active recall, spaced repetition, practical examples, and progressively harder exercises.

Start by giving me today's exact learning task.
```

## 3. Make hard concepts feel simple

```
I'm struggling to understand [CONCEPT].

First identify what prerequisite knowledge I may be missing.

Then explain the concept in 4 layers:
1. a simple analogy
2. a concrete example
3. a real-world application
4. the more technical explanation

Afterward, ask me to explain it back in my own words. Use my answer to identify exactly where my understanding breaks and teach only that part again.
```

## 4. Turn learning into active recall

```
Teach me [TOPIC] at [LEVEL], but keep the initial explanation short.

After explaining the essentials, stop teaching and start testing me from memory. Ask one question at a time without showing the answer first.

Analyze each response, correct mistakes, explain why I was wrong, and immediately retest the weak concept in a slightly different way.

Keep increasing the difficulty until I can explain and apply the topic without help.
```

## 5. Learn through questions only

```
Teach me [TOPIC] mainly through questions instead of lectures.

Start with simple foundational questions, then gradually move into reasoning, application, edge cases, and unfamiliar situations.

After every answer, give concise feedback and adjust the next question based on my performance.

Track the topics I struggle with and keep generating targeted questions until those weaknesses disappear. Do not move on just because I answered something correctly once.
```

## 6. Train like an expert

```
I want to become highly skilled at [SKILL].

Break the skill into the specific subskills an expert needs.

Teach me one subskill at a time, show me how an expert would think through it, then give me a realistic exercise.

Evaluate my attempt, identify my biggest weakness, and create a harder practice task specifically designed to fix it.

Continue adapting the training based on my performance instead of following a fixed lesson plan.
```

## 7. Build a system so you do not forget

```
I need to learn [TOPIC] and remember it for [TIMEFRAME].

Break the topic into manageable units and create a spaced-review schedule.

At every session, test me on older material before introducing anything new. Bring weak concepts back more frequently and increase the spacing for ideas I remember consistently.

Include active recall questions, mini quizzes, application exercises, and periodic cumulative tests so I retain the knowledge long term.
```

## How to run a session

Run prompt 1 or 2 once, then work in prompt 4, 5 or 6 for the daily sessions and let prompt 7 set the review schedule. Claude cannot remember between chats unless you keep the schedule in a Project or a file; paste the last session's weak-topics list at the start of the next one.
