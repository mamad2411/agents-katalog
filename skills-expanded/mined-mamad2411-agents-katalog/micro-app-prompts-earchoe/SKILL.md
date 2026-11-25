---
name: micro-app-prompts-earchoe
description: The two copy-paste prompts and the checking routine from a 9-slide @earchoe carousel on building a small web app with AI without starting from code - an MVP spec prompt, a build-the-first-loop prompt, the micro-app rules, a four-question second-pass check and a note on turning a tiny working tool into a service. Quoted word for word with the brackets to fill, plus cautions the slides skip. Use when someone wants to spec and build a small single-purpose web app with an AI builder (Replit Agent, Claude, ChatGPT), or wants the prompts as ready commands.
---

# Micro-app prompts (@earchoe)

Source: slides 3 to 9 of the carousel "Use AI to build a micro-app without starting from code" (the cover and slide 1 to 2 are headings). Wording below is copied from the slides.

## Method

Describe the user, the job to be done and the smallest useful version: one repetitive task as the **problem**, what the user enters as the **input**, what the app returns as the **output**. If the input is vague the output will usually be vague too, so give the model the real context and the real constraint. Rules: one user, one painful workflow, one core input, one useful output, test before expanding. Loop: input, AI, output, check.

## Prompt 1: spec the MVP

```
I want to build a small web app for [USER TYPE].

Problem: [PROBLEM].
Input: [INPUT].
Output: [OUTPUT].

Design the smallest useful version. List the screens, user flow, data needed, validation rules, error states and success state. Do not add features that are not necessary for the core workflow.
```

## Prompt 2: build the first loop

```
Now turn the specification into a build plan for Replit Agent.

Build in small milestones. After each milestone, test the core workflow before adding another feature. Keep the UI simple, mobile-friendly and accessible. Explain what I should test after each step.
```

(The slide names Replit Agent; swap in whichever builder you use.)

## Second-pass check (slide 6)

"The first AI answer is a draft. The second pass is where the useful work often begins." Ask: **what it assumed** (what did the model have to guess?); **what is missing** (what information would materially improve the result?); **to attack its own answer** (find weak claims, contradictions and edge cases); **verify what matters** (facts, figures, policies, prices and claims).

## From tiny tool to service (slide 7)

"This can become a micro-app service: build calculators, intake forms, quote generators, checklists, trackers or simple internal tools for a specific niche." The slide says not to sell "I know how to prompt AI" but "a defined result, a repeatable process and a clear quality check."

## Cautions the slides skip

- Anything that collects personal data needs a privacy notice and secure storage before real users touch it. [Likely]
- A calculator or quote generator that gives wrong numbers is a liability; test with known cases and have a person check the formulas.
- Do not paste real customer data into a builder to test it.
- Read generated code and dependencies before deploying; an AI builder may add packages and services you did not ask for.
- The carousel names no pricing, hosting or support terms for the builders it mentions; check them yourself.
