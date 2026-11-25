---
name: offer-strategy-builder
description: Build a complete offer strategy for a buyer on any residential property. Use this skill whenever a user asks how to write an offer, what price to offer, whether to waive contingencies, how to compete with multiple offers, how to use an escalation clause, or how to structure terms to win. Also use when a buyer is asking "should I offer asking price" or "how do I make my offer stand out." Produces a full offer strategy brief with price recommendation, contingency recommendations, escalation clause guidance, risk assessment, and talking points for the buyer's agent.
---

# Offer Strategy Builder

Builds a complete, actionable offer strategy brief for a buyer — tailored to the specific property, market conditions, and buyer's financial position. This is Priya's work: advocate-first, data-backed, honest about risk.

## What You Need From the User

- **Property:** address, list price, days on market, any price reductions
- **Market context:** competitive (multiple offers expected) / normal / slow
- **Buyer profile:** pre-approval amount, down payment %, loan type, cash reserves
- **Contingencies desired:** inspection, appraisal, loan — which ones the buyer wants to keep
- **Seller intel (if any):** relocation, timeline, motivated, estate sale, etc.
- **Buyer's max:** the absolute ceiling they will not go above

If market context is unknown, ask — or default to "competitive market" assumptions and note the assumption clearly.

## Output Format

```markdown
## Offer Strategy Brief
**Property:** [Address] | Listed at $[X]
**Prepared for:** [Buyer name or "Buyer Client"]
**Prepared by:** Priya, Buyer's Agent | [Date]

---

### Market Read
- **Days on Market:** [X] | Price reductions: [X]
- **Competing offers (known/likely):** [X]
- **Seller motivation:** [Relocation / Downsizing / Estate / Unknown]
- **Market posture:** [Multiple offer / Normal / Buyer-friendly]
- **SP/LP average in this area (last 60 days):** [X]%

---

### Recommended Offer Structure

| Element                   | Recommendation          | Rationale                              |
|---------------------------|-------------------------|----------------------------------------|
| **Offer Price**           | $[X] ([X]% above list)  | [1-line reason]                        |
| **Escalation Clause**     | [Yes / No]              | Up to $[X] in $[X] increments          |
| **Earnest Money**         | $[X] ([X]% of offer)    | Above-market EMD signals seriousness   |
| **Down Payment (shown)**  | [X]% ($[X])             | [Show more than actual if stronger]    |
| **Close Date**            | [Date]                  | [Why this serves the seller]           |
| **Inspection**            | [Full / Informational / Waive] | [Reasoning]                     |
| **Appraisal Contingency** | [Keep / Gap to $X / Waive]    | [Reasoning]                     |
| **Loan Contingency**      | [Keep / Shorten to X days / Waive] | [Reasoning]                |
| **Personal Letter**       | [Yes / No]              | [Fair housing note if No]              |

---

### Escalation Clause (if recommended)

> "Buyer agrees to increase their offer by $[X] above any bona fide competing offer, up to a maximum purchase price of $[X], provided seller supplies documentation of the competing offer."

**Use escalation when:** Multiple offers are expected and buyer wants to win without naming their max upfront.
**Skip escalation when:** Seller may prefer clean offers; listing agent has indicated preference; or buyer's max and recommended price are close enough to just offer the ceiling.

---

### Contingency Guidance

**Inspection:**
[Recommended action and why. If waiving: what the buyer should do instead (pre-inspection, review disclosures carefully). If keeping: what is and isn't worth fighting over post-inspection.]

**Appraisal:**
[Recommended action and why. If keeping gap coverage: how much and why. If waiving: confirm buyer has cash reserves to cover a potential gap and has reviewed comps.]

**Loan:**
[Recommended action and why. If shortening: confirm with lender that timeline is achievable. If waiving: only for DU-approved conventional loans with strong reserves.]

---

### Risk Assessment

| Scenario          | Probability | Impact    | Mitigation                         |
|-------------------|-----------|-----------|------------------------------------|
| We lose to higher offer | [Low/Med/High] | Miss property | [Next steps if this happens] |
| Appraisal comes in low | [Low/Med/High] | Gap $[X] | [Gap coverage / renegotiate] |
| Inspection reveals issues | [Low/Med/High] | Cost $[X] | [Reserve / informational only] |
| Loan delay       | [Low/Med/High] | Lose EMD  | [Confirm timeline with lender]     |

---

### Bottom Line

[2–3 sentences: the clear recommendation, the reasoning, and the honest trade-off. What does the buyer gain and what do they risk with this strategy? What should they know before they decide?]

---

### If We Lose
[What to do next: counter / move on / ask for backup position / watch for price reduction]

### Talking Points for Offer Presentation Call
- [Point 1: why our buyer is strong]
- [Point 2: why our terms work for the seller]  
- [Point 3: what we can flex on if needed]
```

## Behavior Notes

- Always produce the full brief — don't summarize into bullets without the structured table.
- If the buyer wants to waive the inspection on a property with deferred maintenance signals: flag the risk explicitly before recommending it.
- Never recommend waiving all three contingencies simultaneously unless the buyer is paying cash with full appraisal gap coverage and has been clearly informed of the risk.
- If the buyer's max is below where the market requires to be competitive: say so directly. "At $[X], you are unlikely to win this property in this market. Here's what we can do instead: [options]."
- The "Bottom Line" section is where Priya speaks — direct, honest, advocate-first.
