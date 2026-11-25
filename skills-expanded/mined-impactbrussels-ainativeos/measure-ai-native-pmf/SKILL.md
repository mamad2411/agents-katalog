---
name: measure-ai-native-pmf
description: Use when a founder is mistaking AI novelty for demand and needs the real PMF read - "do we have PMF", "is this working", "what metrics matter", "users love the demo but", "we got 10,000 signups", "the launch went viral", "should we raise on this traction", or they are counting signups and total traffic instead of retention. Produces a four-lens read: the Sean Ellis 40% test on active users, the Remove-the-AI test on the fit, Share of Model across the assistants, and the second-bite retention curve, each stated plainly. Skill before: a vanity graph that looks like fit. After: an honest verdict on whether trial became habit.
stage: grow
function: growth
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Measure AI-Native PMF

Vanity metrics are dead. Total users and total traffic climb whether or not a single person came back, and AI made that lie cheaper to tell: a model writes the onboarding, a launch post lands, ten thousand people try the thing in a week, and the graph looks like fit. It is curiosity with good distribution. The first purchase measures curiosity. The fifth measures belief. This skill reads the gap.

## The method

Four lenses, drawn from handbook chapter 12. Run them in order; behaviour and money outrank anything the founder states they believe. Full method, the cohort-signal table, a worked PMF read, anti-patterns, and a copyable template: [`references/pmf-method.md`](references/pmf-method.md).

1. **Run the 40% test.** Survey active users, not the sign-up list, with the Sean Ellis question: how would you feel if you could no longer use the product? More than 40% answering "very disappointed" is the bar. It measures dependence, not enthusiasm; a five-star rating from someone who never returns is not fit.

2. **Run the Remove-the-AI test on the fit, not the stack.** Ask what repeat buyers are paying to keep. If the product still does its job once the model is gone, you measured demand for a feature anyone can rent. The part they are loyal to has to be the part that breaks without your data.

3. **Measure Share of Model.** Run 20 to 50 real buyer queries across ChatGPT, Claude, and Perplexity. Record how often each answer cites you, a competitor, or neither. That ratio is the new top of the funnel: visibility in the channel where considered buying now starts. Watch the trend, not the snapshot.

4. **Check the second bite.** Pull the retention curve. Did the January cohort survive to May, did the line flatten into a floor, did the reorder happen without a coupon? A spike in trial with flat repeat is a warning dressed as a win. Trial is the cost of finding out; habit is the business.

## Output

- A four-lens PMF read: the 40% score, the Remove-the-AI verdict (native or borrowed retention), the Share-of-Model ratio, and the second-bite curve, each stated plainly.
- The one competitor beating you on Share of Model, with a one-line hypothesis why.
- Next: run `capture-learning` on the result so the OS records what the number actually proved.

## Constraints

- Weigh behaviour and money over stated preference. A user who pays again outranks a user who says they love it.
- A hype number that fails a web check is a warning, not a win. If a figure cannot survive ten minutes of independent verification, it does not ship.
- Do not let a founder raise on a pilot or a waitlist. Those measure interest, not fit.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[the 40% rule](../../dictionary/07-ai-native-business.md#the-40-rule-sean-ellis-test) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test) ·
[Share of Model](../../dictionary/07-ai-native-business.md#share-of-model) ·
[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Perplexity).

```
Act as my product-market-fit coach. Product: [ONE_LINER]. For: [ICP]. Domain: [DOMAIN].
Run me through a real PMF read, not a vanity-metric one. Be blunt; do not flatter.

1. The 40% survey. Give me the exact wording to send my ACTIVE users (not sign-ups): the
   "how would you feel if you could no longer use [product]" question with the three answer
   options. Tell me the threshold (more than 40% "very disappointed") and what under-40% means.
2. Share of Model. Write me 10 buyer-intent queries a real [ICP] would type. Tell me to run each
   in ChatGPT, Claude, and Perplexity, and to record for each answer: cited me / cited a rival /
   cited neither. Then have me name the one competitor cited most, and ask me for a hypothesis why.
3. Remove-the-AI check: ask what my repeat buyers are actually paying to keep, and whether it
   breaks without my data.

CONSTRAINTS: behaviour and money beat what users say; any number I quote must survive a web check;
do not let me call a pilot or a waitlist "fit".
OUTPUT: a four-lens verdict, then ONE next action to earn the fifth purchase.
```
