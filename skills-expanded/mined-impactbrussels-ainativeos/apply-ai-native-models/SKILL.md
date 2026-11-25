---
name: apply-ai-native-models
description: Use when a founder faces a hard, consequential call and is about to guess - build-or-buy, what to ship, whether to automate something irreversible, whether a slick demo proves anything - or says "should I build this", "is this defensible", "the demo works, can we ship", "talk me through this decision", "what would you do here", "stress-test my plan", or keeps hearing only the answer that flatters the plan. Produces a one-page decision memo scoring the call against the OS's core mental models, with the call made and the riskiest assumption named. The cross-cutting capstone; reach for it at any stage; routes back to start-here.
stage: cross-cutting
function: system
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Apply AI-Native Models

When you ask an AI to justify your idea, it will. That is the structural reason founders guess confidently and wrong: the easiest answer to reach is the one that flatters the plan. This skill makes you run a hard decision through a fixed set of the OS's mental models, in order, so the call is reasoned out and stress-tested rather than rationalised. It is the capstone over the whole build arc, from Frame to Defend.

## The method

Run the decision through every model, in order, and refuse to cherry-pick. Full framework: [`references/mental-models.md`](references/mental-models.md). The models trace the build arc; when the memo points to a stage of work, route back through [`start-here`](../start-here/SKILL.md).

### Step 1: State the decision in one falsifiable sentence
Write the call as a claim that could be proven wrong, not a vibe. "Build our own retrieval layer" is a decision; "improve the product" is not.

### Step 2: Score it against each model, in order
Run the full set. Each model is a one-line test and the trap it prevents. Do not stop at the first one that looks settled.

| Model | The test | The trap it prevents |
|-------|----------|----------------------|
| Remove-the-AI test | Delete the AI: does the thing still break? | Building a feature and pricing it like a moat |
| Architecture-before-code | Is the system designed before any code? | The faster mess that collapses under growth |
| Adversarial-by-default | Have I made the case *against*, not just for? | Confirmation bias the model will happily feed |
| Human-on-the-loop | Is a human set above any irreversible step? | Automating a call that needs a signature |
| Store-the-proprietary, rent-the-replicable | Am I building what compounds, renting what does not? | Pouring effort into the commodity layer |
| A demo is not evidence | What did a real user, not a demo, prove? | Mistaking a working prototype for demand or safety |
| Proof before hype | What survives a web check or a real test? | Shipping a claim that cannot be defended |
| Trust as the currency | Does this earn or spend trust with the buyer? | Winning the demo and losing the market |

### Step 3: Run the adversarial pass on purpose
Make the strongest case the decision is wrong. If you skipped this because the answer "felt right", that is exactly when you needed it.

### Step 4: Make the call and name the riskiest assumption
State the decision, the model that most constrains it, and the single belief that is both most uncertain and most fatal if wrong. That assumption is the next thing to test.

## Output

- A **one-page decision memo**: the decision in one sentence, a score against each of the eight models, the call, and the riskiest assumption named.
- A **route**: the stage of work the memo points to, run back through `start-here`.
- Next: test the riskiest assumption first; if it is a defensibility question, run `moat-strategy`; if a safety one, `eval-and-safety-harness`.

## Constraints

- Name and forbid **cherry-picking the flattering model**: run all eight, in order, even the ones that make the plan look worse. A memo that scores only the models the plan passes is theatre.
- The **adversarial pass is mandatory**. AI supercharges confirmation bias; an unchallenged "yes" is the failure mode, not the result.
- Never state a guess as fact in the memo. A demo is not evidence, and that applies to your own reasoning.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test) ·
[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel) ·
[AI-native vs wrapper](../../dictionary/07-ai-native-business.md#ai-native-vs-wrapper) ·
[human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini).

```
Act as my decision partner, and do NOT just agree with me. I have a hard call to make.
Decision: [ONE_LINER as a claim that could be proven wrong]. Domain: [DOMAIN]. Customer: [ICP].
The riskiest thing I believe: [RISKIEST_ASSUMPTION].
Run my decision through these eight mental models, in order, and score each pass or fail with one
line of reasoning. Do not skip the ones that make my plan look worse:
1. Remove-the-AI test: if I delete the AI, does this still break? If not, it's a feature.
2. Architecture before code: is the system designed before any code gets generated?
3. Adversarial by default: make the STRONGEST case that this decision is wrong.
4. Human on the loop: is a person set above any irreversible step?
5. Store the proprietary, rent the replicable: am I building what compounds and renting the commodity?
6. A demo is not evidence: what did a REAL user (not a demo) actually prove?
7. Proof before hype: what claim here survives a web check or a real test?
8. Trust as the currency: does this earn or spend trust with my buyer?
Then: make the call, name the ONE model that most constrains it, and name the single assumption that
is most uncertain AND most fatal if wrong - that's what I test next.
Give it to me as a one-page memo. Don't flatter the plan.
```
