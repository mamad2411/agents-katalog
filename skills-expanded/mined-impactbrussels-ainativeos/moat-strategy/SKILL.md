---
name: moat-strategy
description: Use when a founder needs to know what actually defends the company once building is free - when they say "what's my moat", "a competitor could clone this in a weekend", "is my data a moat", "we collect a lot of data", "anyone can rent the same model", "we don't have enough data to compete", "is this defensible", or worries a giant will copy the feature next quarter. Produces a moat thesis (which moat, why durable, what feeds it) and a MOATS-LEDGER entry. Run after measure-ai-native-pmf; feeds capture-learning.
stage: defend
function: ops
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Moat Strategy

The thing you were defending stopped being defensible. You and the giant down the road rent the same model, at the same price, on the same terms; what took a quarter takes a Friday. A wrapper looks identical to a moat on launch day, which is the trap that funds the wrong companies. Three months on, one product is sharper than it was at launch and the other is exactly as good as the day it shipped, while four clones crowd in beside it. The demo could not tell them apart. The loop is the only thing that could.

## The method

Find the loop, rank the moat, ledger it. Full framework: [`references/moat-method.md`](references/moat-method.md). Source: Handbook [Chapter 14](../../handbook/14-moats-data-ecosystems.md). Output destination: [`knowledge-base/MOATS-LEDGER.md`](../../knowledge-base/MOATS-LEDGER.md).

### Step 1: Name the flywheel, or admit you have a feature
Write the one sentence where a customer's use *today* makes the product measurably better *next month*. If you cannot write it, you do not have a moat yet. Spell out the loop: what use produces what proprietary data that makes what better.

### Step 2: Rank the moat type by durability
Pick the moat you are actually building, hardest first.

| Moat type | The test it must pass | Durability |
|-----------|-----------------------|-----------|
| Data flywheel | Does each use compound, widening the gap while a rival catches up? | Highest |
| Vertical / proprietary data | Can a horizontal giant *not* collect this (consent, regulation, sensor, relationship)? | High |
| Data consortium | In a fragmented sector, is the pooled set larger than any member could build, and governed? | High |
| Trust and compliance | Does the audit trail, validation record, or clearance take years and survive scrutiny? | High, slow |
| Brand / switching cost | Does leaving cost the customer real, accumulated work, not just a logo change? | Medium |

### Step 3: Run the Remove-the-AI test on the whole company
Delete the model call. If what is left is a generic chatbot, the moat is rented. If what is left is a flywheel of proprietary data and a record of earned trust, it is load-bearing.

### Step 4: For a fragmented sector, design the consortium
When no single mid-size player holds enough data alone, pool it under written governance before a rival does. Governance is the moat, not the code. Settle who sees what, who owns the model, and how value flows back, *before* anyone uploads a file.

### Step 5: Ledger the moat
Write the entry into `MOATS-LEDGER.md` against the four tracking questions: what compounds, can a giant reach it, what trust asset protects it, and strength (weak / forming / real).

## Output

- A **moat thesis**: which moat, why it is durable, and the loop that feeds it, in plain sentences.
- A **MOATS-LEDGER entry** appended to `knowledge-base/MOATS-LEDGER.md` (append, never overwrite).
- If the sector is fragmented: a **consortium governance sketch** (who sees what, who owns the model, value flow).
- Next: run `capture-learning` after the first real defensibility outcome to bank the dated, sourced lesson.

## Constraints

- Name and forbid the **feature-as-moat**: a clever prompt, a slick UI, or "we collect a lot of data" is high-extractability and copies in a weekend. A data lake that does not feed back is a storage bill, not a loop.
- A flywheel with no compounding loop is not a flywheel. If usage leaves no residue that sharpens the next answer, you have a wrapper with good PR.
- A consortium with no governance written down first will discover the conflicts after the data is mixed. Governed, selective pooling, or nothing.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel) ·
[data consortium](../../dictionary/07-ai-native-business.md#data-consortium) ·
[vertical data moat](../../dictionary/07-ai-native-business.md#vertical-data-moat) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test) ·
[AI-native vs wrapper](../../dictionary/07-ai-native-business.md#ai-native-vs-wrapper)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini).

```
Act as my moat strategist. The model I use is rented; everyone can rent the same one. Help me find
what actually defends the company. Product: [ONE_LINER]. Customer: [ICP]. Domain: [DOMAIN].
1. Make me write my data flywheel in one sentence: where a customer's use TODAY makes the product
   measurably better NEXT MONTH. If I can't, tell me I have a feature, not a moat, and help me find
   the loop. Spell it out: what use -> what proprietary data -> what gets better.
2. Rank the moat I'm actually building, hardest first: data flywheel, vertical/proprietary data,
   data consortium, trust and compliance, or brand/switching cost. For each, apply its test.
3. Run the Remove-the-AI test on the WHOLE company: delete the model call, tell me what's left
   standing that a competitor can't rebuild in a weekend. If the answer is "a generic chatbot", say
   so plainly.
4. If my sector is fragmented and no single mid-size player has enough data alone, sketch a data
   consortium: who sees what, who owns the model, how value flows back - the governance before any
   data is pooled.
5. Write me a ledger entry: what compounds with use, can a horizontal AI giant reach this data,
   what trust/regulatory asset protects it, and the strength (weak / forming / real).
Don't flatter me by calling a feature a moat. End with the single next action.
```
