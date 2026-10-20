---
name: ai-slacker-premortem
description: Five adversarial premortem prompts from @ai_slacker — run before any launch, strategy commit, or major decision. Covers forensic failure analysis, failure ranking, plan rebuilding, competitor attack angle, and measurable tripwires.
---

# Premortem Prompts

Source: @ai_slacker
Run these **before** committing to a launch, strategy, or major decision — not after.
A premortem assumes the plan has already failed and works backwards from failure.

---

## Slide 1 — The Premortem Prompt

Forensic failure analyst. Forces month-by-month autopsy tied to details you actually gave.

```
You're a forensic failure analyst. My plan: [describe it in full, with timeline, budget, and what success looks like]. It's 6 months from today and this plan failed completely. Write the autopsy. Give me the 7 most likely causes of death, ranked, and for each: what killed it, how it unfolded month by month, the assumption I held that allowed it, and the first warning sign I'd have seen. Every failure traces back to a detail I gave you or you cut it. No generic advice. Never reassure me.
```

---

## Slide 2 — The Verdict

Forces ranking of failures and surfaces the hidden assumption.

```
From those [N] failures, tell me which is MOST LIKELY and which is MOST DANGEROUS, and explain why they're different. Then name the single biggest hidden assumption I'm making that I don't realise is an assumption. Be blunt. If my plan has a fatal flaw, say the words.
```

**What this surfaces:** the difference between "common" failure and "catastrophic" failure — they are usually not the same item.

---

## Slide 3 — The Rebuild

Rewrites the plan with every failure mode closed off, plus a pre-launch checklist with walk-away criteria.

```
Rewrite my plan with every one of those failure modes closed off. Show me what changed and why. Then give me a pre-launch checklist of 3 to 5 things I must verify before I execute anything, and tell me what result on each would mean I should walk away entirely.
```

---

## Slide 4 — The Adversary

Play the competitor. Surfaces timing vulnerabilities and moves you've already discounted.

```
Now play the person who benefits most from my plan failing — a competitor, a rival, someone who wants my spot. You've seen my plan. Tell me exactly where you'd attack it, what you'd do the week I launch, and the move I'd never see coming.
```

**What this surfaces:** competitive blind spots, timing vulnerabilities, and the moves you've already discounted as "unlikely."

---

## Slide 5 — The Tripwire

One measurable signal per failure mode, with the exact week to check.

```
For each failure mode, give me one measurable signal that would tell me it's starting to happen, and the exact week I should check for it. I want tripwires, not vibes.
```

---

## Full premortem sequence (combined)

```
I want to run a premortem on this plan before I commit to it.

My plan: [paste your full plan here]

Step 1 — THE PREMORTEM PROMPT
You're a forensic failure analyst. It's 6 months from today and this plan failed completely. Write the autopsy. Give me the 7 most likely causes of death, ranked, and for each: what killed it, how it unfolded month by month, the assumption I held that allowed it, and the first warning sign I'd have seen. Every failure traces back to a detail I gave you or you cut it. No generic advice. Never reassure me.

Step 2 — THE VERDICT
From those 7 failures, tell me which is MOST LIKELY and which is MOST DANGEROUS, and explain why they're different. Then name the single biggest hidden assumption I'm making that I don't realise is an assumption. Be blunt. If my plan has a fatal flaw, say the words.

Step 3 — THE REBUILD
Rewrite my plan with every one of those failure modes closed off. Show me what changed and why. Then give me a pre-launch checklist of 3 to 5 things I must verify before I execute anything, and tell me what result on each would mean I should walk away entirely.

Step 4 — THE ADVERSARY
Now play the person who benefits most from my plan failing — a competitor, a rival, someone who wants my spot. You've seen my plan. Tell me exactly where you'd attack it, what you'd do the week I launch, and the move I'd never see coming.

Step 5 — THE TRIPWIRE
For each failure mode, give me one measurable signal that would tell me it's starting to happen, and the exact week I should check for it. I want tripwires, not vibes.
```

---

## When to use this

- Before a product launch
- Before committing to a pricing change
- Before signing a contract or partnership
- Before a major hiring or resourcing decision
- Before a public announcement or campaign launch
- At the start of a new quarter's strategy

## What to do with the output

1. Take The Adversary's attack and ask: "What would make this attack fail?"
2. Take the Most Dangerous failure and build one explicit mitigation into the plan.
3. Take the Hidden Assumption and either validate it with evidence or rewrite the plan without it.
4. Set calendar reminders for every tripwire date The Tripwire names.
