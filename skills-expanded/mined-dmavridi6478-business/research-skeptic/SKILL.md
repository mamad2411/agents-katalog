---
name: research-skeptic
description: Six copy-paste prompts that make Claude check whether research is trustworthy instead of just collecting more - find where sources agree, trace a claim to its original source, look for evidence against your conclusion, sort findings into well supported / partially supported / disputed / still unknown, rate source quality, and find the conclusion you are most confident about with the weakest evidence. Use when the user is researching a topic, checking a claim, or about to rely on collected sources. Source @StackFlo "5 Claude prompts to use when researching something" (Batch 99).
---

# Research skeptic - 6 prompts

Principle from the slides: stop collecting information; make Claude help you work out what is actually trustworthy. Quoted as shown; replace the [BRACKETS]. Pair with the existing `/sourcecheck` (claim-by-claim sourcing) and `hyperresearch` (full pipeline). Claude only judges what you paste: it cannot open the sources unless you give it the text or a fetch tool, so say so when it matters.

| # | Prompt | Command |
|---|---|---|
| 1 | Find where sources agree | `/research-skeptic 1 <topic>` |
| 2 | Find the original source | `/research-skeptic 2 <claim>` |
| 3 | Look for evidence against it | `/research-skeptic 3 <conclusion>` |
| 4 | Tell me what is still unknown | `/research-skeptic 4` (then paste research) |
| 5 | Find the weakest source | `/research-skeptic 5` (then paste sources) |
| 6 | The prompt to save | `/research-skeptic 6` |

## 1. Find where sources agree

```
I'm researching: [TOPIC]

Compare the information I've collected below.

What do multiple independent sources agree on?
What appears in only one source?
Where do the sources contradict each other?

Don't treat something as true just because it's repeated.
```
Consensus is useful, but only if the sources are actually independent.

## 2. Find the original source

```
This claim keeps appearing: [CLAIM]

Help me trace it back to the strongest original source.

Prioritise primary research, official data or first-hand documentation over articles that simply repeat the claim.
```
Ten websites repeating one claim can still lead back to one weak source.

## 3. Look for evidence against it

```
Here's the conclusion my research currently points towards: [CONCLUSION]

Actively look for credible evidence that challenges it.

Show me the strongest counter-evidence and explain whether it genuinely weakens my conclusion.
```
Do not only research the answer you want to find.

## 4. Tell me what is still unknown

```
Based on everything I've collected so far: [PASTE RESEARCH]

Separate my findings into:
- WELL SUPPORTED
- PARTIALLY SUPPORTED
- DISPUTED
- STILL UNKNOWN

Tell me what additional evidence would move anything into 'well supported'.
```
Good research should show you where certainty ends.

## 5. Find the weakest source

```
Review these sources critically.

Which ones should I trust MORE and which should I treat cautiously?

Consider:
- WHO PUBLISHED IT
- THE EVIDENCE PROVIDED
- HOW RECENT IT IS
- POSSIBLE CONFLICTS OF INTEREST
- WHETHER CLAIMS LINK BACK TO ORIGINAL EVIDENCE
```
Not every source deserves equal weight.

## 6. The Claude prompt to save (before trusting your research)

```
What conclusion am I currently most confident about - but have the weakest evidence for?
```
Then ask Claude what would actually be needed to verify it. Do not just use AI to find answers; use it to question the evidence.
