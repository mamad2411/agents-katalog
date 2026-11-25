---
name: customer-discovery-that-doesnt-lie
description: Use when a founder is running customer interviews and wants the truth, not applause - when they say "everyone loves it", "I talked to fifteen people and they're all interested", "how do I validate this with users", "I fed my call notes to the model and it says strong demand", "they said they'd definitely use it", or are about to build off interview enthusiasm. Produces a discovery question script, a transcript-extraction template, a ranked pain list, and the one belief to test next. Invoke after frame-the-hypothesis, before hypothesis-mining.
stage: frame
function: product
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Customer Discovery That Doesn't Lie

Talk is cheap, and AI made it cheaper. The people you interview are polite, and the model you hand
the transcripts to is agreeable, so two lies stack into one dangerous object: a discovery process
that feels rigorous and confirms exactly what you hoped. The friction that used to protect you, the
slow read of every transcript by hand, is gone. Design the disconfirmation back in on purpose, or
your research will only ever grant you the permission you came for.

## The method

Discovery built to disconfirm, in the Mom-Test posture. Full framework: Handbook
[Chapter 04](../../handbook/04-customer-discovery.md). Deep method, tables, and a worked example:
[`references/discovery-method.md`](references/discovery-method.md).

### Step 1: Write a script that asks about the past, not the hypothetical
A good question is one the customer cannot answer with a compliment. Ask what they did, paid for,
and worked around last month, never what they would do with your idea.

| Bad question (invites a lie) | Good question (extracts a fact) |
|------------------------------|----------------------------------|
| "Would you use a tool that did X?" | "Walk me through the last time you hit `[PROBLEM]`. What did you do?" |
| "Do you think this is a good idea?" | "What have you tried to fix this? What did you pay for it?" |
| "How much would you pay?" | "What does the current workaround cost you in time or money?" |

### Step 2: Interview to advance, not to be liked
A compliment is not data. Seek a commitment that costs the customer something: time, a referral,
access, money, a follow-up booked. No advance means no real interest, however warm the call felt.

### Step 3: Extract facts from raw transcripts, never a mood summary
Feed the model the raw transcripts and forbid the average. Make it pull every concrete claim and
tag who said it, then score each pain on four axes: severity, frequency, current workaround, and
willingness-to-pay signal. The signal lives in the edge case, not the centre of mass.

### Step 4: Run the adversarial pass so you cannot hear only what you want
Never ask the model whether the interviews support you, or it will
([sycophancy](../../dictionary/05-failure-modes.md#sycophancy)). Order the inverse: "Based only on
what these people actually said, give the five most likely reasons they will not pay, ranked, each
with an exact quote." Take the top reason and name the cheapest test of it.

## Output

- A discovery question script (past-tense, fact-seeking) and a transcript-extraction template.
- A ranked pain list scored on severity, frequency, workaround, and willingness-to-pay signal.
- The five ranked reasons they won't pay, and the single belief to test next.
- Next skill: `hypothesis-mining` to turn the ranked pains into falsifiable bets.

## Constraints

- Counting compliments as validation is the failure mode here. Only a commitment that costs the
  customer something counts as evidence; stated enthusiasm counts as zero.
- Adversarial by default: if the model only justified the idea, the prompt failed. Make it refute you.
- Weight revealed behaviour above stated preference, always. What they pay for beats what they say.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[sycophancy](../../dictionary/05-failure-modes.md#sycophancy) ·
[the 40% rule](../../dictionary/07-ai-native-business.md#the-40-rule-sean-ellis-test) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini). Tag: chat.

```
Act as a sceptical customer-discovery coach trained on The Mom Test. My idea: [ONE_LINER]. For:
[ICP]. Problem I think they have: [PROBLEM]. Domain: [DOMAIN].
1. Write me 8 interview questions that ask about the customer's PAST behaviour, never about my idea
   or a hypothetical. No question a person can answer with a compliment.
2. Tell me, for each interview, what concrete commitment to ask for (time, a referral, access,
   money, a next meeting) so I learn whether interest is real, not polite.
3. Here are my raw notes: [PASTE TRANSCRIPTS]. Do NOT summarise the mood. Extract every concrete
   claim, tag who said it, and score each pain on severity, frequency, current workaround, and any
   willingness-to-pay signal. Put supporting and opposing evidence in two columns.
4. Now turn on me: based ONLY on what these people said, give the five most likely reasons they
   will NOT pay, ranked, each with an exact quote.
CONSTRAINTS: do not flatter the idea; do not average away the outlier; treat a compliment as zero
evidence and a costly commitment as real.
OUTPUT: the question script, the scored pain table, the five ranked reasons. End by naming the ONE
belief I should test next and the cheapest experiment that would expose it.
```
