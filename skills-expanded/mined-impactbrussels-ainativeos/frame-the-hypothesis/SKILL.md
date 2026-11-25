---
name: frame-the-hypothesis
description: Use when a founder has a vague AI idea and needs to sharpen it into one falsifiable bet before building - when they say "is this worth building", "how do I validate this", "I have an idea for an AI product", "the demo works, what now", "everyone I talk to says they love it", "how do I know if this is real", or are about to build on a hunch. Triggers when the model keeps flattering the idea, or the founder is testing the build instead of the demand. Produces a problem statement, the riskiest assumption scored, a falsifiable hypothesis with a pass/fail bar, and a five-reason devil's-advocate critique. Run after start-here, before map-the-terrain or architect-before-code.
stage: frame
function: product
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Frame the Hypothesis

AI makes prototyping so cheap it hides the question that actually matters: is the problem real? A
working demo proves nothing about demand. This skill turns "I have an AI idea" into "here is the one
assumption that decides whether this is real, and the cheapest experiment that could prove me wrong",
and it forces the model to attack the idea instead of flattering it.

## The method

Sharpen the problem, score the riskiest assumption, write the falsifiable bet, then make the model
attack it. Full anatomy, the uncertainty x fatality rubric, the devil's-advocate protocol, and a worked
example: [`references/hypothesis-craft.md`](references/hypothesis-craft.md).

### Step 1: Sharpen the problem, not the solution
Reframe in the customer's words: who exactly (`[ICP]`) fails to get what painful job done (`[PROBLEM]`),
how do they cope today, and how often does it hurt? Output a one-paragraph problem statement.

### Step 2: Name the riskiest assumption
List the beliefs the idea rests on, then flag the one that is both **most uncertain** and **most fatal
if wrong** (`[RISKIEST_ASSUMPTION]`). Usually problem or demand risk, not technical risk.

### Step 3: Write the falsifiable hypothesis
State it as: *"We believe `[X]`; we'll know we're wrong if `[bar]`."* Commit to the pass/fail bar
**before** running anything. If no result could fail it, it's theatre.

### Step 4: Run the structured devil's advocate
The model will confirm your idea if you let it ([sycophancy](../../dictionary/05-failure-modes.md#sycophancy)).
Instead, make it refute you: "Give five specific reasons this fails, and the cheapest test that would
expose each." Dispatch the `devils-advocate` agent for a harder pass.

## Output

- Problem statement (customer's words) + the assumption stack, riskiest one flagged.
- One falsifiable hypothesis with an explicit pass/fail bar and decision rule.
- The five strongest refutations, and which to test first. Next skill: `map-the-terrain` or `architect-before-code`.

## Constraints

- Adversarial by default: if the model only justifies the idea, the prompt failed. Make it attack.
- Validate problem and demand before solution. Building is not validating.
- Don't invent market numbers; label any figure an assumption to confirm.
- Stay theme-agnostic; the founder supplies the domain.

## Dictionary

[sycophancy](../../dictionary/05-failure-modes.md#sycophancy) ·
[the 40% rule](../../dictionary/07-ai-native-business.md#the-40-rule-sean-ellis-test) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini).

```
Act as a sharp, skeptical AI-native validation coach. My idea: [ONE_LINER]. For: [ICP]. Problem I
think they have: [PROBLEM]. Domain: [DOMAIN].
1. Rewrite the problem in the customer's words: who exactly, what painful job, how they cope now, how often it hurts.
2. List my assumptions, then pick the ONE most uncertain AND most fatal if wrong.
3. Write it as a falsifiable hypothesis: "We believe X; we'll know we're wrong if [bar]." Set the number before I test.
4. Now turn on me: give five specific reasons this idea fails, and the cheapest experiment that would expose each.
Do not flatter the idea. Make me test the problem before the solution, and don't invent market numbers.
```
