---
name: case-study-builder
description: Builds customer case studies on a situation → intervention → measurable result spine, with a ready interview question list, a hard metric-verification rule (no unverified numbers ship), and deliberate pull-quote selection. Use when the user asks to "write a case study", "customer story", "success story", "turn this interview into a case study", or needs proof assets for sales. Don't use for deploying that proof on a sales page — that's landing-page-copywriter.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Case Studies, Proof, Customer Stories, Interviews]
    related_skills: [landing-page-copywriter, linkedin-content-pack, deep-research-brief, brand-voice-guardian, content-repurposer]
---

# Case Study Builder

Produces case studies a skeptical buyer believes: a real customer in a specific situation, the exact intervention, and results stated as verified numbers with their source — or not stated at all. Every study runs on the situation → intervention → result spine, and every pull quote earns its placement by carrying either emotion or a number.

## When to Use

- The user has a customer win (interview notes, call transcript, metrics, or just a name to interview) and wants a publishable case study.
- Sales needs proof assets and raw material exists.
- The user asks for "interview questions for a case study" — step 2 stands alone.
- **Not for:** placing the finished proof into page copy (`landing-page-copywriter`), spinning it into social posts (`content-repurposer`, `linkedin-content-pack`), or general market research (`deep-research-brief`).

## Quick Reference

| Action | Rule |
|---|---|
| Spine | Situation (before, stakes) → Intervention (what changed, how) → Result (measured after) |
| Metric rule | A number ships only with source + timeframe + customer confirmation; else `[UNVERIFIED — do not publish]` |
| Interview | Use the step 2 question list; record answers verbatim where possible |
| Pull quotes | 2–3 max; each carries emotion or a number; verbatim, trimmed with "…" only |
| Approval | Customer sign-off on quotes + numbers before publication — human manages |
| Length | 500–900 words body + headline + summary box |

## Procedure

1. **Gather** — confirm: the customer (name, role, company, permission status), what the product/intervention was, raw material available (transcript, notes, metrics, emails), and where the study will live. No raw material yet → deliver step 2's interview kit as the output and stop there.
2. **Interview kit** — supply this question list (adapt names, keep the shape):
   - Situation: "What was breaking before?" / "What did that cost you — time, money, morale?" / "What had you already tried?"
   - Intervention: "What made you pick this?" / "What did the first week look like?" / "What almost stopped you?"
   - Result: "What number moved, from what to what, over what period?" / "Where does that number come from?" / "What surprised you?"
   - Quote bait: "If a peer asked whether this was worth it, what would you tell them?"
3. **Extract the spine** — from the material, write one sentence per stage: situation, intervention, result. If the result sentence has no number, go get one (ask the user/customer) or plan an outcome-described-honestly study — do not decorate with fake precision.
4. **Verify every metric** — for each number: source (dashboard, report, customer statement), timeframe, and baseline. Log them in the metric ledger. Anything unconfirmed is tagged `[UNVERIFIED — do not publish]` in-text and listed with exactly what confirmation is needed. "Roughly doubled" confirmed beats "103%" invented.
5. **Select pull quotes** — from verbatim material only. Pick 2–3 that carry feeling ("I stopped dreading Mondays") or numbers ("we cut review time from 3 days to 4 hours"). No verbatim quotes available → mark `[QUOTE PENDING customer approval]`; never compose a quote and attribute it.
6. **Draft** — headline states the result ("[Customer] cut [metric] by [X] in [time]"), summary box (3 bullets: who, what, result), then the spine in 500–900 words. Specifics over superlatives; the customer is the hero, the product is the tool.
7. **Deliver + approval route** — assemble the Output Template including the metric ledger and an approval checklist. Publication waits for customer sign-off; the human runs that step.

## Output Template

```
# [Customer] [verb] [metric change] in [timeframe]

**Summary** — Who: [customer, role, company] | Challenge: [one line] | Result: [verified number + timeframe]

## The situation
[before-state with stakes, in the customer's words where possible]

## The intervention
[what changed, how adoption actually went, including one honest friction point]

## The result
[verified numbers with baseline + timeframe; qualitative wins after the numbers]

> "[Pull quote 1 — verbatim]" — [Name, Role]
> "[Pull quote 2 — verbatim]" — [Name, Role]

---
**Metric ledger:** [metric → source → timeframe → confirmed by]
**Approval checklist (human):** [ ] quotes approved  [ ] numbers approved  [ ] logo/name usage approved
```

## Pitfalls

- **Invented precision** — "40% improvement" appears because it sounds better than "meaningfully faster". Recovery: run the step 4 ledger; any number without source + timeframe + confirmation is replaced with the honest qualitative phrasing or tagged `[UNVERIFIED — do not publish]`.
- **Composed quotes** — a quote gets "cleaned up" into words the customer never said. Recovery: diff every quote against the transcript; trims marked with "…" are fine, new words are not — revert or mark `[QUOTE PENDING]`.
- **Missing before-state** — the study opens with the win, so the win has no weight. Recovery: rebuild from the step 3 spine; if the situation sentence is empty, ask the situation questions from step 2 before drafting further.
- **Product-hero syndrome** — the draft reads like a brochure; the customer disappears. Recovery: count sentence subjects in each section; if the product leads more than the customer, rewrite with the customer as actor and the product as instrument.
- **Publishing before sign-off** — the study ships and the customer objects to a number or their name. Recovery: the approval checklist is part of the deliverable; if published early, notify the human to pull it and route approval immediately.

## Verification

- [ ] Spine complete: situation, intervention, and result each land in one clear sentence before the draft exists
- [ ] Every published number appears in the metric ledger with source, baseline, timeframe, and confirmation
- [ ] Zero `[UNVERIFIED]` numbers in publishable text; pending items listed with what would confirm them
- [ ] 2–3 pull quotes, all verbatim-traceable or explicitly `[QUOTE PENDING]`
- [ ] Headline states the verified result; body 500–900 words
- [ ] Approval checklist attached; publication marked as blocked on customer sign-off
