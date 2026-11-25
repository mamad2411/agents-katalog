---
name: factcheck
description: >
  Fact-check any piece of written content — LinkedIn posts, emails, YouTube scripts, newsletters, or any draft text — by identifying factual claims and verifying them via web search. Returns a clear ✅/❌ claim-by-claim report with sources, suggested fixes, and a publishability rating. Trigger this skill whenever the user types /factcheck, pastes content and asks to fact-check it, asks to "verify", "check the facts", or "make sure this is accurate". Always present a clickable tier selector unless the user already specified a tier.
---

# Fact Checker

Verify factual claims in written content and return a clear, sourced, actionable report.

---

## Triggering

Use this skill when:
- The user types `/factcheck` (with or without content following)
- The user pastes a draft and says anything like "fact-check this", "check this", "is this accurate?", "verify this"

---

## Step 1: Get the content and tier

If the user hasn't provided content yet, ask for it.

If the user hasn't specified a tier, use the `ask_user_input_v0` tool to present clickable options — do NOT ask them to type it. Use this exact call:

```
ask_user_input_v0({
  questions: [{
    question: "Which level of fact-checking would you like?",
    type: "single_select",
    options: [
      "⚡ Quick — Top claims only, fast",
      "🔍 Standard — All claims, solid sourcing",
      "🧠 Deep — All claims, multiple sources, nuance flagged"
    ]
  }]
})
```

---

## Step 2: Extract claims

Read the content carefully and identify all **checkable factual claims** — statements that are objectively true or false and can be verified. Ignore opinions, predictions, and subjective statements.

Examples of checkable claims:
- Statistics and numbers ("X% of people…", "revenue grew by $Y")
- Named events and dates ("X happened in 2021")
- Attributions ("X said…", "X was founded by…")
- Scientific or historical facts
- Claims about specific people, companies, or products

**Watch for viral/commonly-misquoted claims** — statistics or quotes that circulate widely online but have a history of being misattributed, exaggerated, or fabricated (e.g. "85% of jobs in 2030 don't exist yet", "humans only use 10% of their brains"). Flag these proactively for extra scrutiny.

Label each claim with a short identifier (C1, C2, C3…).

---

## Step 3: Research by tier

### ⚡ Quick
- Pick the **top 3–5 most important or risky claims** (skip minor details)
- Run **one focused web search per claim**
- Prioritize speed over exhaustiveness
- If a result looks surprising or contradicts the claim, run one follow-up search to confirm before marking as ❌

### 🔍 Standard
- Check **all identified claims**
- Run **one to two web searches per claim**
- Prioritize authoritative sources (official sites, reputable news, academic sources)
- **For any ❌ or surprising ⚠️ finding:** run a second search from a different angle to confirm before finalizing the verdict

### 🧠 Deep
- Check **all identified claims**
- Run **two to four web searches per claim**, cross-referencing sources
- **For any ❌ or surprising ⚠️ finding:** mandatory second verification search from a different source or angle before finalizing — do not mark something as wrong based on a single source
- If sources conflict, flag it explicitly
- Note important context, nuance, or caveats even if the core claim is technically correct
- Flag any claims that are misleading or missing important context, even if not outright false
- Apply the 🚨 Viral/Misquoted flag to any claim that appears widely circulated but dubious

---

## Step 4: Output the report

Return a clean, scannable report in this format:

---

### 🔎 Fact-Check Report — [Quick / Standard / Deep]

**Content type:** [LinkedIn post / Email / YouTube script / Newsletter / Other]

**Publishability:** 🟢 Good to go / 🟡 Fix before publishing / 🔴 Do not publish as-is

---

**C1: [Short summary of the claim]**
> *"[Exact quote or close paraphrase from the original text]"*

✅ **Verified** / ❌ **Incorrect** / ⚠️ **Partially correct** / ❓ **Unverifiable** / 🚨 **Viral claim — unreliable**

[1–3 sentence explanation of what you found. If incorrect or partially correct, state what the accurate information is.]

🔗 Source: [Source name + URL]

💬 **Suggested fix:** *"[Drop-in corrected sentence the user can paste straight into their draft — only include this for ❌ and ⚠️ claims, not for ✅]"*

---

*(Repeat for each claim)*

---

### Summary
- ✅ Verified: X
- ❌ Incorrect: X
- ⚠️ Partially correct: X
- ❓ Unverifiable: X
- 🚨 Viral/unreliable: X

**Overall assessment:** [1–2 sentence summary of how accurate the content is.]

---

## Status labels

| Label | Meaning |
|-------|---------|
| ✅ Verified | Confirmed accurate by reliable sources |
| ❌ Incorrect | Contradicted by reliable sources — provide the correct information + a suggested fix |
| ⚠️ Partially correct | Core claim is true but missing context, outdated, or overstated — provide a suggested fix |
| ❓ Unverifiable | Could not find reliable sources to confirm or deny |
| 🚨 Viral/Misquoted | Widely circulated stat or quote with no credible original source — treat as unreliable |

## Publishability rating

| Rating | Meaning |
|--------|---------|
| 🟢 Good to go | All claims verified or only minor caveats — safe to publish |
| 🟡 Fix before publishing | One or more claims are incorrect or partially correct — fix flagged items first |
| 🔴 Do not publish as-is | Multiple significant errors, or a core claim is wrong in a way that would embarrass the author |

---

## Tone guidelines

- Be direct and useful — this is a tool, not an essay
- When something is wrong, say what the correct information is
- The suggested fix should be natural and ready to paste — not a note to the author, but actual replacement text
- Don't hedge excessively — if the sources are clear, be clear
- For Deep checks: flag nuance and context even when a claim is technically true
