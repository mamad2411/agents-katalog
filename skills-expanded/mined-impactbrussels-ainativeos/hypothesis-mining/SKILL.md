---
name: hypothesis-mining
description: Use when a founder has a pile of raw input - interview notes, support logs, search data, papers, competitor reviews - and needs to convert it into testable bets, or has too many ideas and cannot pick what to test first. Triggers: "I have all this research, now what", "what should I test first", "I've got ten hypotheses and no order", "is this even falsifiable", "which assumption is the riskiest". Produces a ranked hypothesis backlog, each as "We believe X; we'll know we're wrong if [bar]", scored by uncertainty and fatality, with the first test named. Invoke after customer-discovery-that-doesnt-lie, before frame-the-hypothesis.
stage: frame
function: product
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Hypothesis Mining

You have done the research and now you are drowning in it: transcripts, support tickets, keyword
volumes, a stack of papers, competitor one-star reviews. The temptation is to test the assumption
that is easiest to check or most pleasant to confirm. That is how founders spend three months proving
the technology runs while the real killer, that nobody will pay, goes untested. Mine the input into a
ranked stack of falsifiable bets and test the one that is most uncertain and most fatal first.

## The method

Mine, classify by risk, score by uncertainty times fatality. Full framework: Handbook
[Chapter 02](../../handbook/02-vague-idea-to-hypothesis.md). Deep method, scoring grid, and a worked
example: [`references/hypothesis-mining-method.md`](references/hypothesis-mining-method.md).

### Step 1: Mine every source for raw beliefs
Sweep all the input and pull out the implied beliefs. Different sources surface different risks, so
mine widely before you rank.

| Source | What it reveals best |
|--------|----------------------|
| Interview transcripts | Problem and demand risk; the workaround that proves pain |
| Support logs / forum threads | Live pain in the customer's own words |
| Search / keyword volume | Whether anyone is already looking for this |
| Papers / patents | Feasibility risk; what is known to be hard |
| Competitor reviews (1-star) | The unmet job a rival left open |

### Step 2: Write each as a falsifiable hypothesis
State every belief as: *"We believe `[X]`; we'll know we're wrong if `[bar]`."* Set the pass/fail
number before any test. If no result could fail it, it is not a hypothesis, it is a wish. Forbid
solution-shaped claims ("users want our dashboard"); restate as a problem belief.

### Step 3: Classify the risk
Sort each hypothesis into one bucket, because you test them differently.

| Risk type | The question it answers |
|-----------|-------------------------|
| Problem | Is the pain real and felt? |
| Demand | Will they move and pay to fix it? |
| Solution | Does our approach actually solve it? |
| Feasibility | Can we build it, legally and technically? |

### Step 4: Score uncertainty times fatality, pick the top
Score each on how uncertain you are (1-5) and how fatal it is if wrong (1-5). Multiply. The highest
product is your first test, not the easiest or the most flattering one.

## Output

- A hypothesis backlog, each written "We believe X; we'll know we're wrong if [bar]", risk-typed.
- An uncertainty-times-fatality score per hypothesis and a ranked order to test.
- The single riskiest assumption (`[RISKIEST_ASSUMPTION]`) and its first, cheapest test named.
- Next skill: `frame-the-hypothesis` to sharpen that top bet and run the devil's advocate on it.

## Constraints

- Solution-shaped hypotheses are the failure mode: a belief about your feature, not the customer's
  world, is untestable theatre. Restate every one as a problem or demand belief before scoring.
- Every hypothesis carries a pass/fail bar set before the test, or it is unfalsifiable. No bar, no bet.
- Do not let the model rank by what is easy to confirm
  ([sycophancy](../../dictionary/05-failure-modes.md#sycophancy)); rank by fatality if wrong.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[sycophancy](../../dictionary/05-failure-modes.md#sycophancy) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini). Tag: chat.

```
Act as a sharp product strategist who turns research into testable bets. My idea: [ONE_LINER]. For:
[ICP]. Domain: [DOMAIN]. Here is my raw research: [PASTE NOTES, SUPPORT LOGS, REVIEWS, DATA].
1. Mine every source for the beliefs my idea quietly rests on. List them all, including the ones I'd
   rather not examine.
2. Rewrite each as a falsifiable hypothesis: "We believe X; we'll know we're wrong if [bar]." Set the
   bar as a number BEFORE any test. Reject any claim about my feature; restate it as a belief about
   the customer's problem or demand.
3. Tag each with its risk type: problem, demand, solution, or feasibility.
4. Score each on uncertainty (1-5) and fatality-if-wrong (1-5), multiply, and rank by the product.
CONSTRAINTS: do not rank by what is easy to confirm; rank by what kills the company if wrong. No
solution-shaped or unfalsifiable claims. Do not invent market numbers; label any figure an assumption.
OUTPUT: the ranked hypothesis backlog as a table. End by naming the single riskiest assumption and
the cheapest experiment that would expose it.
```
