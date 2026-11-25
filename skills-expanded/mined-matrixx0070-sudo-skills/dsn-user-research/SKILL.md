---
name: dsn-user-research
version: 1.0.0
description: Plan and run user research end to end - sharp questions, the right method, unbiased interview guides and usability tasks, and a clean path from sessions to synthesis.
author: matrixx0070
tags: [design, research, interviews, usability-testing, ux, screener]
capabilities: []
---

# User Research

## When to use
Use this when a team is about to build on assumptions, when you need to choose between interviews, surveys, or usability tests, or when someone needs an interview guide or test plan that will not lead the witness. Covers planning through session execution.

**Not for:** analyzing sessions you already ran (use dsn-research-synthesis), A/B test statistics, or research with no decision attached — if nothing changes based on the answer, do not run it.

## Method
1. **Sharpen the question.** Write the one decision this research must inform. If you cannot name the decision, you are not ready to research.
2. **Pick the method.** *Decision:* "why / what matters" → generative interviews; "can they do it" → usability test; "how many / how often" → survey. Match method to question, not to habit.
3. **Recruit.** Define participant profile and screener; state target n and why it suffices (5–8 for qualitative discovery).
4. **Write the guide.** Order broad to specific. Use open, non-leading prompts ("Tell me about the last time..." not "Do you like..."). For usability, write realistic tasks with success criteria — never hint at the path.
5. **Reduce bias.** Separate observation from interpretation, avoid double-barreled and yes/no leading prompts, and stay silent after asking.
6. **Run consistently.** Same intro, consent, and probes each session; capture verbatim quotes and behaviors, timestamped.
7. **Hand to synthesis** with tagged, atomic notes.

## Example
Decision: "should onboarding be a wizard or a checklist?" That is a "can they do it" question → **usability test**. Task: "Set up your first project" with success = project created unaided in under 3 min. Guide asks "Walk me through what you'd do next" (neutral), never "Would the wizard help here?" (leading).

## Pitfalls
- Running research with no decision attached — you generate interesting trivia, not direction.
- Leading questions ("Don't you find this confusing?") that manufacture the answer you expected.
- Hinting the path during usability tasks, which measures your hint instead of the design.
- Filling silence after a question, cutting off the participant's real answer.

## Output format
```
# Research Plan: <topic>
**Decision this informs:** ...
**Method + why:** ...
**Participants:** profile — screener — target n
**Guide:** warm-up → core questions / tasks (with success criteria) → wrap-up
**What to capture:** behaviors, quotes, friction points
```
Keep questions open and neutral; note any assumption the plan is testing.
