---
name: start-here
description: Use when a founder is unsure where to begin or what to do next on an AI build - when they say "where do I start", "I want to build with AI", "is my idea AI-native or a wrapper", "what's the next step", "should I add a billing page now", "I have an idea but no plan", "I'm overwhelmed", or are about to pour months into the exciting work instead of the riskiest. Triggers on any founder lost on the build arc or asking which skill to run. Produces the Remove-the-AI verdict, their stage, and exactly one next skill to run.
stage: cross-cutting
function: system
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Start Here

Founders rarely fail for lack of effort; they fail by pouring months into the wrong thing for the
stage they're at. This skill's only job is to tell you where you are and the single next thing to do,
then get out of the way. It also runs the one test that decides whether you're building a company or a
feature.

## The method

Diagnose the stage, run the Remove-the-AI test, route to one skill. Full build-arc map, the test in
full, the symptom-to-skill table, a worked diagnosis, and anti-patterns:
[`references/stage-diagnosis.md`](references/stage-diagnosis.md).

### Step 1: Run the Remove-the-AI test
Ask: *take the AI out of your product, does it still work?* If yes, you have an [AI feature, not an
AI-native company](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test). Before anything
else, find the closed loop that would make it break without the intelligence. If there isn't one, that
is the work.

### Step 2: Locate the stage
Place the founder on the build arc by what they can't yet answer:

| If they can't answer… | They're at | Run next |
|-----------------------|-----------|----------|
| "What's the sharp, falsifiable bet?" | **Frame** | `frame-the-hypothesis` |
| "Who's the market, and where's the regulatory/competitive wedge?" | **Frame** | `map-the-terrain` |
| "What's the system, before any code?" | **Architect** | `architect-before-code` |
| "How do I build it with agents without it collapsing?" | **Build** | `agentic-build-loop` |
| "How is this safe enough to act on a human?" | **Trust** | `eval-and-safety-harness` |
| "What's the smallest agent that proves the loop?" | **Ship** | `design-the-mva` |
| "Is it actually working?" | **Grow** | `measure-ai-native-pmf` |

### Step 3: Route to the earliest unvalidated assumption
When two stages fit, send them upstream. The highest-value work is almost always the riskiest belief
they haven't tested yet, not the most exciting one.

## Output

- The result of the Remove-the-AI test, stated plainly (native or wrapper, and what's missing).
- The founder's current stage and the **one** skill to run next, with a one-line reason.

## Constraints

- Route to exactly one next skill. A list of five is the same as no answer.
- Don't skip the Remove-the-AI test to be encouraging: a wrapper diagnosed early saves months.
- Stay theme-agnostic; the founder supplies the domain.

## Dictionary

[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test) ·
[AI-native vs wrapper](../../dictionary/07-ai-native-business.md#ai-native-vs-wrapper) ·
[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini).

```
Act as my AI-native build coach. My idea: [ONE_LINER]. Who it's for: [ICP]. Domain: [DOMAIN].
1. Run the "Remove-the-AI test": if I take the AI out, does my product still work? If yes, tell me
   I have a feature not an AI-native company, and help me find the closed loop that would make it
   break without the intelligence.
2. Diagnose my stage: Frame, Architect, Build, Trust, Ship, Grow, or Defend - based on the riskiest
   thing I can't yet answer.
3. Tell me the ONE next thing to do, and why it's the highest-value work right now. Just one.
Don't flatter me; route me to the earliest unvalidated assumption.
```
